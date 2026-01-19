import json
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from core.database import async_session
from core.models import Order, OrderItem, OrderStatus, User, Translation

router = Router()

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """Handle order data from WebApp checkout."""
    try:
        # Parse the WebApp data
        order_data = json.loads(message.web_app_data.data)

        user_id = message.from_user.id

        async with async_session() as session:
            # Get user
            user = await session.scalar(
                select(User).where(User.tg_id == user_id)
            )

            if not user:
                await message.reply("❌ User not found. Please restart the bot.")
                return

            # Create order
            order = Order(
                user_id=user.id,
                status=OrderStatus.NEW,
                total_price=order_data['total']
            )
            session.add(order)
            await session.flush()  # Get order ID

            # Create order items
            for item in order_data['items']:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['id'],
                    quantity=item['qty'],
                    price_at_time=item['price']
                )
                session.add(order_item)

            await session.commit()

            # Get translations for response
            header_trans = await session.scalar(
                select(Translation).where(Translation.key == "webapp_order_msg_header")
            )
            contact_trans = await session.scalar(
                select(Translation).where(Translation.key == "webapp_order_msg_contact")
            )

            header_text = (header_trans.value_de if message.from_user.language_code == "de" and header_trans.value_de
                          else header_trans.value_uk if header_trans else "✅ Order received!")
            contact_text = (contact_trans.value_de if message.from_user.language_code == "de" and contact_trans.value_de
                           else contact_trans.value_uk if contact_trans else "A manager will contact you.")

            # Send confirmation message
            response_text = f"{header_text}\n\n"
            response_text += f"Order #{order.id}\n"
            response_text += f"Sum: {order_data['total']:.2f} €\n\n"
            response_text += contact_text

            await message.reply(response_text)

    except json.JSONDecodeError:
        await message.reply("❌ Invalid order data received.")
    except Exception as e:
        print(f"Error processing order: {e}")
        await message.reply("❌ Error processing your order. Please try again.")