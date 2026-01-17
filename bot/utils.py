from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import select
from core.database import async_session
from core.models import Translation

# Centralized Translation Filter for multilingual button handling
class TranslationFilter(BaseFilter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: Message) -> bool:
        async with async_session() as session:
            trans = await session.scalar(select(Translation).where(Translation.key == self.key))
            if not trans: return False
            return message.text in [trans.value_uk, trans.value_de]

# Centralized translation helper function
async def get_translation(translation_key: str, user_language: str = "uk") -> str:
    """Get translation for the given key in user's language."""
    try:
        async with async_session() as session:
            translation = await session.scalar(
                select(Translation).where(Translation.key == translation_key)
            )
            if translation:
                if user_language == "de" and translation.value_de:
                    return translation.value_de
                return translation.value_uk or translation_key
    except Exception as e:
        print(f"Error getting translation for {translation_key}: {e}")
    return translation_key