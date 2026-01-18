# Sprint 21.15: Final Bot Polish (Profile, Price, and Units)

**Context:** Fix the remaining localization gaps: Profile is stuck in Ukrainian, "Price" label and "кг" unit are not localized.

**Tasks:**

1. **Fix Profile Localization in `bot/handlers/start.py`**:
   - In `profile_handler`, ensure you extract the string value of the language:
     `user_lang = user.language_pref.value if user.language_pref else "uk"`
   - Use this `user_lang` for all `get_translation` calls in the profile.
   - Ensure the title uses the `profile_title` key from the database.

2. **Localize Price and Units in `bot/handlers/store.py`**:
   - In product cards, replace the hardcoded "Ціна" with `get_translation("price_label", user_language)`.
   - Implement unit translation: if `user_language == 'de'` and `product.unit == 'кг'`, display "kg".

3. **General Check**:
   - Ensure no hardcoded Ukrainian strings remain in `profile_handler` or product cards.

**Definition of Done:**
- Profile shows "Ihre Angaben" and German labels for German users.
- Product cards show "Preis: X €/kg" for German users.
- Language toggle correctly refreshes the Profile text and the Main Menu.