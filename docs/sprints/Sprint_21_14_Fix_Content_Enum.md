# Sprint 21.14: Fix Content Localization (Enum Stringification)

**Issue:** Categories and Products are stuck in Ukrainian because the code compares an Enum object with a string "de".

**Tasks:**

1. **Update `bot/handlers/store.py`**:
   - In all localized helper functions (`get_localized_category_name`, `get_localized_product_name`, `get_localized_product_description`), ensure you handle the language parameter correctly.
   - **Fix:** Before comparing, convert the language to string if it is an Enum, or simply ensure the caller passes `user.language_pref.value`.
   - Recommended fix at the start of handlers:
     `user_language = user.language_pref.value if user and user.language_pref else "uk"`

2. **Verify all content outputs**:
   - Ensure `show_categories`, `show_category_products`, and `update_product_message` all use the `.value` of the language preference.

**Definition of Done:**
- If user language is 'de' in DB, categories show German names.
- If user language is 'de' in DB, products show German names.