# Sprint 21.16: Force Language Synchronization on Start

**Issue:** Returning users see Ukrainian menu even if their DB profile is set to German. Language toggle is out of sync on the first click.

**Tasks:**

1. **Fix `start_handler` in `bot/handlers/start.py`**:
   - IMMEDIATELY after fetching the `user` from DB, create a variable `current_lang = user.language_pref.value if user.language_pref else "uk"`.
   - Use THIS `current_lang` to generate the Welcome message and the Main Menu. Do not rely on FSM state for existing users.

2. **Fix `toggle_language` Logic**:
   - Before toggling, re-fetch the user from the DB to get the ABSOLUTE current state.
   - Ensure the `new_language` calculation is based on `user.language_pref.value`.
   - Update the UI only AFTER the `session.commit()`.

3. **Global Translation Helper Check**:
   - Ensure `get_translation` doesn't have a hardcoded "uk" fallback that overrides the user's real choice.

**Definition of Done:**
- If Admin shows 'de', the bot MUST greet the user in German on /start.
- The first click on "Change Language" works correctly and shows the right alert.