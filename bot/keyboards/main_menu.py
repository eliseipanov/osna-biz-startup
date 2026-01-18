from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from sqlalchemy import select
from core.database import async_session
from core.models import Translation

async def get_main_menu_keyboard(user_language="uk"):
    """Get main menu keyboard with localized button labels from database."""
    try:
        async with async_session() as session:
            # Fetch translations for main menu buttons
            catalog_trans = await session.scalar(
                select(Translation).where(Translation.key == "catalog_button")
            )
            profile_trans = await session.scalar(
                select(Translation).where(Translation.key == "profile_button")
            )
            impressum_trans = await session.scalar(
                select(Translation).where(Translation.key == "impressum_button")
            )

            # Get localized text based on user language
            catalog_text = (catalog_trans.value_de if user_language == "de" and catalog_trans.value_de
                          else catalog_trans.value_uk if catalog_trans else "🥩 Catalog")

            profile_text = (profile_trans.value_de if user_language == "de" and profile_trans.value_de
                          else profile_trans.value_uk if profile_trans else "👤 Profile")

            impressum_text = (impressum_trans.value_de if user_language == "de" and impressum_trans.value_de
                            else impressum_trans.value_uk if impressum_trans else "ℹ️ Impressum")

            keyboard = [
                [KeyboardButton(text=catalog_text, web_app=WebAppInfo(url=f"https://7568db916eec.ngrok-free.app/webapp?lang={user_language}"))],
                [KeyboardButton(text=profile_text)],
                [KeyboardButton(text=impressum_text)]
            ]
            return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, persistent=True)
    except Exception as e:
        # Fallback to hardcoded English if database error
        keyboard = [
            [KeyboardButton(text="🥩 Catalog", web_app=WebAppInfo(url=f"https://7568db916eec.ngrok-free.app/webapp?lang={user_language}"))],
            [KeyboardButton(text="👤 Profile")],
            [KeyboardButton(text="ℹ️ Impressum")]
        ]
        return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, persistent=True)