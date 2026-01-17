import sqlalchemy
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.database import async_session
from core.models import Category, Product, CartItem, User
from datetime import datetime
import os

router = Router()

# Helper function to check if orders are allowed

def is_order_allowed():
    now = datetime.now()
    # Friday 12:00 in Europe/Berlin timezone (UTC+1)
    deadline = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    # Check if today is Friday (4) and current time is past deadline
    if now.weekday() == 4 and now > deadline:
        return False
    return True

# Category selection handler

def get_categories_keyboard():
    builder = InlineKeyboardBuilder()
    # Add categories dynamically from database
    # This will be populated in the actual handler
    return builder.as_markup()

@router.message(F.text == "🥩 Каталог")
async def show_categories(message: Message):
    try:
        async with async_session() as session:
            # Get all categories
            categories = await session.scalars(select(Category))
            categories = categories.all()
            
            if not categories:
                await message.answer("Категорії не знайдено.")
                return
            
            # Create inline keyboard with categories
            builder = InlineKeyboardBuilder()
            for category in categories:
                builder.button(
                    text=category.name,
                    callback_data=f"category_{category.id}"
                )
            
            builder.adjust(2)  # 2 columns
            
            await message.answer(
                "🥩 <b>Оберіть категорію:</b>",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
    except Exception as e:
        await message.answer("Сталася помилка при завантаженні категорій.")

# Category callback handler
@router.callback_query(F.data.startswith("category_"))
async def show_category_products(callback: CallbackQuery):
    try:
        category_id = int(callback.data.split("_")[1])
        
        async with async_session() as session:
            # Get category and its products
            category = await session.get(Category, category_id)
            if not category:
                await callback.answer("Категорію не знайдено.")
                return
            
            # Get products in this category that are in stock
            products = await session.scalars(
                select(Product)
                .where(Product.category_id == category_id)
                .where(Product.availability_status == "IN_STOCK")
            )
            products = products.all()
            
            if not products:
                await callback.answer("У цій категорії немає товарів.")
                return
            
            # Send products as cards
            for product in products:
                # Build product card caption
                caption = f"<b>{product.name}</b>\n\n"
                if product.description:
                    caption += f"{product.description}\n\n"
                caption += f"💶 Ціна: {product.price} €/{product.unit}"
                
                # Create inline keyboard for quantity control
                builder = InlineKeyboardBuilder()
                
                # Check if user has this product in cart
                user_cart_item = await session.scalar(
                    select(CartItem)
                    .where(CartItem.user_id == callback.from_user.id)
                    .where(CartItem.product_id == product.id)
                )
                
                current_quantity = user_cart_item.quantity if user_cart_item else 0
                
                # Add quantity control buttons
                if is_order_allowed():
                    builder.button(text="-", callback_data=f"decrease_{product.id}")
                    builder.button(text=f"В кошику: {current_quantity}", callback_data="qty")
                    builder.button(text="+", callback_data=f"increase_{product.id}")
                else:
                    builder.button(text="-", callback_data="disabled")
                    builder.button(text=f"В кошику: {current_quantity}", callback_data="qty")
                    builder.button(text="+", callback_data="disabled")
                
                builder.adjust(3)
                
                # Add navigation buttons
                builder.row()
                builder.button(text="⬅️ Назад до категорій", callback_data="back_to_categories")
                
                # Check if user has items in cart
                cart_count = await session.scalar(
                    select(sqlalchemy.func.count())
                    .select_from(CartItem)
                    .where(CartItem.user_id == callback.from_user.id)
                )
                
                if cart_count > 0:
                    builder.button(text="🛒 Перейти до кошика", callback_data="go_to_cart")
                
                # Send product card
                if product.image_path and os.path.exists(f"static/uploads/{product.image_path}"):
                    photo = FSInputFile(f"static/uploads/{product.image_path}")
                    await callback.message.answer_photo(
                        photo=photo,
                        caption=caption,
                        reply_markup=builder.as_markup(),
                        parse_mode="HTML"
                    )
                else:
                    await callback.message.answer(
                        caption,
                        reply_markup=builder.as_markup(),
                        parse_mode="HTML"
                    )
            
            await callback.answer()
    except Exception as e:
        await callback.answer("Сталася помилка при завантаженні товарів.")

# Quantity control handlers
@router.callback_query(F.data.startswith("increase_"))
async def increase_quantity(callback: CallbackQuery):
    if not is_order_allowed():
        await callback.answer("Замовлення на цю суботу закрито!", show_alert=True)
        return
    
    try:
        product_id = int(callback.data.split("_")[1])
        user_id = callback.from_user.id
        
        async with async_session() as session:
            # Get or create cart item
            cart_item = await session.scalar(
                select(CartItem)
                .where(CartItem.user_id == user_id)
                .where(CartItem.product_id == product_id)
            )
            
            if cart_item:
                cart_item.quantity += 1.0
            else:
                cart_item = CartItem(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=1.0
                )
                session.add(cart_item)
            
            await session.commit()
            
            # Update message to show new quantity
            await update_product_message(callback.message, product_id, user_id)
            await callback.answer(f"Додано до кошика. Кількість: {cart_item.quantity}")
    except Exception as e:
        await callback.answer("Сталася помилка при оновленні кошика.")

@router.callback_query(F.data.startswith("decrease_"))
async def decrease_quantity(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[1])
        user_id = callback.from_user.id
        
        async with async_session() as session:
            # Get cart item
            cart_item = await session.scalar(
                select(CartItem)
                .where(CartItem.user_id == user_id)
                .where(CartItem.product_id == product_id)
            )
            
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1.0
                    await session.commit()
                    
                    # Update message to show new quantity
                    await update_product_message(callback.message, product_id, user_id)
                    await callback.answer(f"Зменшено кількість. Кількість: {cart_item.quantity}")
                else:
                    await session.delete(cart_item)
                    await session.commit()
                    
                    # Update message to show new quantity
                    await update_product_message(callback.message, product_id, user_id)
                    await callback.answer("Товар видалено з кошика.")
            else:
                await callback.answer("Товар не знайдено в кошику.")
    except Exception as e:
        await callback.answer("Сталася помилка при оновленні кошика.")

# Navigation handlers
@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: CallbackQuery):
    try:
        async with async_session() as session:
            # Get all categories
            categories = await session.scalars(select(Category))
            categories = categories.all()
            
            if not categories:
                await callback.answer("Категорії не знайдено.")
                return
            
            # Create inline keyboard with categories
            builder = InlineKeyboardBuilder()
            for category in categories:
                builder.button(
                    text=category.name,
                    callback_data=f"category_{category.id}"
                )
            
            builder.adjust(2)  # 2 columns
            
            await callback.message.edit_text(
                "🥩 <b>Оберіть категорію:</b>",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
            await callback.answer()
    except Exception as e:
        await callback.answer("Сталася помилка при поверненні до категорій.")

@router.callback_query(F.data == "go_to_cart")
async def go_to_cart(callback: CallbackQuery):
    await callback.answer("Функціонал кошика ще не реалізовано.")

# Helper function to update product message with new quantity
async def update_product_message(message: Message, product_id: int, user_id: int):
    try:
        async with async_session() as session:
            # Get product and cart item
            product = await session.get(Product, product_id)
            cart_item = await session.scalar(
                select(CartItem)
                .where(CartItem.user_id == user_id)
                .where(CartItem.product_id == product_id)
            )
            
            if not product:
                return
            
            current_quantity = cart_item.quantity if cart_item else 0
            
            # Build updated caption
            caption = f"<b>{product.name}</b>\n\n"
            if product.description:
                caption += f"{product.description}\n\n"
            caption += f"💶 Ціна: {product.price} €/{product.unit}"
            
            # Create updated inline keyboard
            builder = InlineKeyboardBuilder()
            
            if is_order_allowed():
                builder.button(text="-", callback_data=f"decrease_{product.id}")
                builder.button(text=f"В кошику: {current_quantity}", callback_data="qty")
                builder.button(text="+", callback_data=f"increase_{product.id}")
            else:
                builder.button(text="-", callback_data="disabled")
                builder.button(text=f"В кошику: {current_quantity}", callback_data="qty")
                builder.button(text="+", callback_data="disabled")
            
            builder.adjust(3)
            
            # Add navigation buttons
            builder.row()
            builder.button(text="⬅️ Назад до категорій", callback_data="back_to_categories")
            
            # Check if user has items in cart
            cart_count = await session.scalar(
                select(sqlalchemy.func.count())
                .select_from(CartItem)
                .where(CartItem.user_id == user_id)
            )
            
            if cart_count > 0:
                builder.button(text="🛒 Перейти до кошика", callback_data="go_to_cart")
            
            # Edit the original message
            if product.image_path and os.path.exists(f"static/uploads/{product.image_path}"):
                await message.edit_caption(
                    caption=caption,
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
            else:
                await message.edit_text(
                    text=caption,
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
    except Exception as e:
        print(f"Error updating product message: {e}")