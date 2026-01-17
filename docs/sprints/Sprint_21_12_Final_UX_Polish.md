# Sprint 21.12: Final UX Polish and Language Toggle Fix

**Context:** The language toggle causes a "User not found" error and shows hardcoded Ukrainian text. We need to fix the caller identity and localize the hints.

**Tasks:**

1. **Fix "User not found" in `bot/handlers/start.py`**:
   - In `toggle_language`, when calling `profile_handler(callback.message)`, the handler looks for `message.from_user.id`, which is the BOT's ID.
   - Refactor `profile_handler` to accept an optional `user_id` argument. If not provided, fallback to `message.from_user.id`.
   - In `toggle_language`, pass `callback.from_user.id` explicitly to the profile update logic.

2. **Remove Hardcoded Hints**:
   - Replace the string "Оберіть розділ нижче 👇" with a database lookup for the key: `choose_section_hint`.
   - Ensure this applies to both `start_handler` and the language toggle refresh logic.

3. **Cleaner Refresh Logic**:
   - After a language switch, update the existing Profile message (using `edit_text`) instead of sending a new one.
   - Send the new Main Menu keyboard with the localized hint once.

**Definition of Done:**
- Toggling language does not trigger "User not found".
- All hints ("Choose section below") are localized correctly.
- No redundant welcome messages after switching language.