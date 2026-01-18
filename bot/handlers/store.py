import sqlalchemy
from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from core.database import async_session
from core.models import Category, Product, CartItem, User, Translation, AvailabilityStatus
from bot.utils import TranslationFilter, get_translation
from datetime import datetime
import os

router = Router()

# Helper function to get localized product name
def get_localized_product_name(product: Product, language: str = "uk") -> str:
    """Get product name in user's language, fallback to Ukrainian if German not available."""
    if language == "de" and product.name_de:
        return product.name_de
    return product.name or "Unnamed Product"

# Helper function to get localized product description
def get_localized_product_description(product: Product, language: str = "uk") -> str:
    """Get product description in user's language, fallback to Ukrainian if German not available."""
    if language == "de" and product.description_de:
        return product.description_de
    return product.description or ""

# Helper function to get localized category name
def get_localized_category_name(category: Category, language: str = "uk") -> str:
    """Get category name in user's language, fallback to Ukrainian if German not available."""
    if language == "de" and category.name_de:
        return category.name_de
    return category.name or "Unnamed Category"

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

@router.message(TranslationFilter("catalog_button"))
async def show_categories(message: Message):
    """Handle catalog button clicks in both languages and show category selection."""
    try:
        async with async_session() as session:
            # Get user language preference
            user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
            user_language = user.language_pref.value if user and user.language_pref else "uk"

            # Get all categories
            categories = await session.scalars(select(Category))
            categories = categories.all()

            if not categories:
                error_msg = "Категорії не знайдено." if user_language == "uk" else "Kategorien nicht gefunden."
                await message.answer(error_msg)
                return

            # Create inline keyboard with localized category names
            builder = InlineKeyboardBuilder()
            for category in categories:
                category_name = get_localized_category_name(category, user_language)
                builder.button(
                    text=category_name,
                    callback_data=f"category_{category.id}"
                )

            builder.adjust(2)  # 2 columns

            header_text = "🥩 <b>Оберіть категорію:</b>" if user_language == "uk" else "🥩 <b>Wählen Sie eine Kategorie:</b>"

            await message.answer(
                header_text,
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
            # Get user language preference
            user = await session.scalar(select(User).where(User.tg_id == callback.from_user.id))
            user_language = user.language_pref.value if user and user.language_pref else "uk"

            # Get category and its products
            category = await session.get(Category, category_id)
            if not category:
                error_msg = "Категорію не знайдено." if user_language == "uk" else "Kategorie nicht gefunden."
                await callback.answer(error_msg)
                return

            # Get products in this category that are in stock (Many-to-Many join)
            products = await session.scalars(
                select(Product)
                .join(Product.categories)
                .where(Category.id == category_id)
                .where(Product.availability_status == AvailabilityStatus.IN_STOCK)
            )
            products = products.all()

            if not products:
                error_msg = "У цій категорії немає товарів." if user_language == "uk" else "Keine Produkte in dieser Kategorie."
                await callback.answer(error_msg)
                return

            # Send products as cards
            for product in products:
                try:
                    # Build product card caption with localized content
                    product_name = get_localized_product_name(product, user_language)
                    product_description = get_localized_product_description(product, user_language)

                    # Get localized price label
                    price_label = await get_translation("price_label", user_language)

                    # Translate unit for German users
                    unit_display = "kg" if user_language == "de" and product.unit == "кг" else product.unit

                    caption = f"<b>{product_name}</b>\n\n"
                    if product_description:
                        caption += f"{product_description}\n\n"
                    caption += f"💶 {price_label}: {product.price} €/{unit_display}"

                    # Create inline keyboard for quantity control
                    builder = InlineKeyboardBuilder()

                    # Check if user has this product in cart
                    user_cart_item = await session.scalar(
                        select(CartItem)
                        .where(CartItem.user_id == user.id)
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
                    back_text = "⬅️ Назад до категорій" if user_language == "uk" else "⬅️ Zurück zu Kategorien"
                    builder.button(text=back_text, callback_data="back_to_categories")

                    # Check if user has items in cart
                    cart_count = await session.scalar(
                        select(sqlalchemy.func.count())
                        .select_from(CartItem)
                        .where(CartItem.user_id == user.id)
                    )

                    if cart_count > 0:
                        cart_text = "🛒 Перейти до кошика" if user_language == "uk" else "🛒 Zum Warenkorb"
                        builder.button(text=cart_text, callback_data="go_to_cart")

                    # Send product card with better error handling
                    try:
                        if product.image_path and os.path.exists(f"static/uploads/{product.image_path}"):
                            photo = FSInputFile(f"static/uploads/{product.image_path}")
                            await callback.message.answer_photo(
                                photo=photo,
                                caption=caption,
                                reply_markup=builder.as_markup(),
                                parse_mode="HTML"
                            )
                        else:
                            # Send text-only message if no image
                            await callback.message.answer(
                                caption,
                                reply_markup=builder.as_markup(),
                                parse_mode="HTML"
                            )
                    except Exception as image_error:
                        # If image sending fails, send text-only as fallback
                        print(f"Image error for product {product.id}: {image_error}")
                        await callback.message.answer(
                            caption,
                            reply_markup=builder.as_markup(),
                            parse_mode="HTML"
                        )

                except Exception as product_error:
                    print(f"Error displaying product {product.id}: {product_error}")
                    # Continue with next product instead of failing completely
                    continue

            await callback.answer()
    except Exception as e:
        print(f"Error in show_category_products: {e}")
        await callback.answer("Сталася помилка при завантаженні товарів.")

# Quantity control handlers
@router.callback_query(F.data.startswith("increase_"))
async def increase_quantity(callback: CallbackQuery):
    if not is_order_allowed():
        await callback.answer("Замовлення на цю суботу закрито!", show_alert=True)
        return

    try:
        product_id = int(callback.data.split("_")[1])
        tg_user_id = callback.from_user.id

        async with async_session() as session:
            # Get user object first
            user = await session.scalar(select(User).where(User.tg_id == tg_user_id))
            if not user:
                await callback.answer("Користувача не знайдено.")
                return

            # Get or create cart item using internal user ID
            cart_item = await session.scalar(
                select(CartItem)
                .where(CartItem.user_id == user.id)
                .where(CartItem.product_id == product_id)
            )
            
            if cart_item:
                cart_item.quantity += 1.0
            else:
                cart_item = CartItem(
                    user_id=user.id,
                    product_id=product_id,
                    quantity=1.0
                )
                session.add(cart_item)

            await session.commit()

            # Update message to show new quantity
            await update_product_message(callback.message, product_id, user.id)
            await callback.answer(f"Додано до кошика. Кількість: {cart_item.quantity}")
    except Exception as e:
        await callback.answer("Сталася помилка при оновленні кошика.")

@router.callback_query(F.data.startswith("decrease_"))
async def decrease_quantity(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[1])
        tg_user_id = callback.from_user.id

        async with async_session() as session:
            # Get user object first
            user = await session.scalar(select(User).where(User.tg_id == tg_user_id))
            if not user:
                await callback.answer("Користувача не знайдено.")
                return

            # Get cart item using internal user ID
            cart_item = await session.scalar(
                select(CartItem)
                .where(CartItem.user_id == user.id)
                .where(CartItem.product_id == product_id)
            )
            
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1.0
                    await session.commit()

                    # Update message to show new quantity
                    await update_product_message(callback.message, product_id, user.id)
                    await callback.answer(f"Зменшено кількість. Кількість: {cart_item.quantity}")
                else:
                    await session.delete(cart_item)
                    await session.commit()

                    # Update message to show new quantity
                    await update_product_message(callback.message, product_id, user.id)
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
            # Get user language preference
            user = await session.scalar(select(User).where(User.tg_id == callback.from_user.id))
            user_language = user.language_pref.value if user and user.language_pref else "uk"

            # Get all categories
            categories = await session.scalars(select(Category))
            categories = categories.all()

            if not categories:
                error_msg = "Категорії не знайдено." if user_language == "uk" else "Kategorien nicht gefunden."
                await callback.answer(error_msg)
                return

            # Create inline keyboard with localized category names
            builder = InlineKeyboardBuilder()
            for category in categories:
                category_name = get_localized_category_name(category, user_language)
                builder.button(
                    text=category_name,
                    callback_data=f"category_{category.id}"
                )

            builder.adjust(2)  # 2 columns

            header_text = "🥩 <b>Оберіть категорію:</b>" if user_language == "uk" else "🥩 <b>Wählen Sie eine Kategorie:</b>"

            await callback.message.edit_text(
                header_text,
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
            # Get user language preference
            user = await session.scalar(select(User).where(User.tg_id == user_id))
            user_language = user.language_pref.value if user and user.language_pref else "uk"

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

            # Build updated caption with localized content
            product_name = get_localized_product_name(product, user_language)
            product_description = get_localized_product_description(product, user_language)

            # Get localized price label
            price_label = await get_translation("price_label", user_language)

            # Translate unit for German users
            unit_display = "kg" if user_language == "de" and product.unit == "кг" else product.unit

            caption = f"<b>{product_name}</b>\n\n"
            if product_description:
                caption += f"{product_description}\n\n"
            caption += f"💶 {price_label}: {product.price} €/{unit_display}"

            # Create updated inline keyboard
            builder = InlineKeyboardBuilder()

            if is_order_allowed():
                builder.button(text="-", callback_data=f"decrease_{product.id}")
                cart_text = f"В кошику: {current_quantity}" if user_language == "uk" else f"Im Warenkorb: {current_quantity}"
                builder.button(text=cart_text, callback_data="qty")
                builder.button(text="+", callback_data=f"increase_{product.id}")
            else:
                builder.button(text="-", callback_data="disabled")
                cart_text = f"В кошику: {current_quantity}" if user_language == "uk" else f"Im Warenkorb: {current_quantity}"
                builder.button(text=cart_text, callback_data="qty")
                builder.button(text="+", callback_data="disabled")

            builder.adjust(3)

            # Add navigation buttons
            builder.row()
            back_text = "⬅️ Назад до категорій" if user_language == "uk" else "⬅️ Zurück zu Kategorien"
            builder.button(text=back_text, callback_data="back_to_categories")

            # Check if user has items in cart
            cart_count = await session.scalar(
                select(sqlalchemy.func.count())
                .select_from(CartItem)
                .where(CartItem.user_id == user_id)
            )

            if cart_count > 0:
                cart_btn_text = "🛒 Перейти до кошика" if user_language == "uk" else "🛒 Zum Warenkorb"
                builder.button(text=cart_btn_text, callback_data="go_to_cart")

            # Edit the original message with better error handling
            try:
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
            except Exception as edit_error:
                print(f"Error editing message for product {product_id}: {edit_error}")
    except Exception as e:
        print(f"Error updating product message: {e}")