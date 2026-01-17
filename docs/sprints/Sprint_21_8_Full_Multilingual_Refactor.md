# Sprint 21.8: Full Technical Refactor of Localization and Routing

**Objective:** Eliminate all hardcoded strings, resolve router conflicts, and implement a robust multilingual UI.

## 1. Required Translation Keys (Reference)
The database contains the following keys in the `translations` table. Use ONLY these:
- `catalog_button`, `profile_button`, `cart_button`, `orders_button`, `impressum_button`
- `name_label`, `phone_label`, `balance_label`, `change_lang_btn`
- `welcome_message`, `on_request`, `unit`, `availability`

## 2. Implementation: Custom Translation Filter
In `bot/handlers/start.py` (or a utils file), implement this EXACT filter class to handle multilingual buttons:

```python
class TranslationFilter(BaseFilter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: Message) -> bool:
        async with async_session() as session:
            trans = await session.scalar(select(Translation).where(Translation.key == self.key))
            if not trans: return False
            return message.text in [trans.value_uk, trans.value_de]