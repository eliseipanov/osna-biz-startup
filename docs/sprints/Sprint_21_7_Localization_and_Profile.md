# Sprint 21.7: Deep Localization, Profile and Language Switching

**Context:** The bot currently has router conflicts and hardcoded English labels. We need to synchronize everything with the Translations table and implement a functional Profile with a language toggle.

**Tasks:**

1. **Conflict Removal:**
   - Delete the file `bot/handlers/catalog.py` entirely.
   - Remove `catalog_router` from `bot/main.py` (imports and registration).

2. **Smart Translation Filters:**
   - In `bot/handlers/store.py` and `bot/handlers/start.py`, do NOT use hardcoded filters like `F.text == "🥩 Каталог"`.
   - Implement a mechanism to check if the user's message matches the translation of `catalog_button`, `profile_button`, or `impressum_button` from the database for BOTH languages (uk/de).

3. **Functional Profile Logic:**
   - Update the handler for `profile_button`.
   - Fetch the user's `full_name`, `phone`, and `balance` from the database.
   - Format the message using localized labels: `name_label`, `phone_label`, `balance_label`.

4. **Language Toggle Implementation:**
   - Add an Inline button to the Profile message: `change_lang_btn`.
   - When clicked, switch the user's `language_pref` (UK -> DE or DE -> UK).
   - Show an alert/message that the language has changed and refresh the main menu.

5. **Fix Store Logic for German Users:**
   - Ensure `show_category_products` in `bot/handlers/store.py` correctly handles the `AvailabilityStatus.IN_STOCK` Enum comparison.
   - Ensure localized names/descriptions use fallback to Ukrainian if the German version is missing.

6. **Cleanup:**
   - Replace all remaining English UI strings (like "Open Catalog" or "Success") with corresponding values from the `Translations` table.

**Definition of Done:**
- Old `catalog.py` is gone.
- Bot responds to both "🥩 Каталог" and "🥩 Katalog" correctly.
- Profile shows real balance and phone.
- Language can be switched via Profile without deleting the user.