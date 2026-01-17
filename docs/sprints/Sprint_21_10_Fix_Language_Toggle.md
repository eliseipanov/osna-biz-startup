# Sprint 21.10: Fix Language Toggle Logic

**Issue:** Language switch only works once because of incorrect Enum vs String comparison in the database query.

**Task:**
1. **In `bot/handlers/start.py`**, find the `toggle_language` function.
2. **Update the toggle logic**:
   - Instead of `user.language_pref == "uk"`, use `user.language_pref.value == "uk"` or compare with the Enum class directly.
   - Example: `new_language = "de" if user.language_pref.value == "uk" else "uk"`
3. **Verify**:
   - Ensure the `User` model is correctly updated and the main menu is refreshed after the toggle.

**Definition of Done:**
- User can toggle between UK and DE multiple times in one session.