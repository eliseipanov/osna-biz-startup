# Sprint-04.3-Fix-Registration-Logic.md

## ⚠️ Problem
The bot crashes with `IntegrityError (UniqueViolationError)` on `/start` because it tries to INSERT a user that already exists in the database.

## 🛠 Task
1. **Update `bot/handlers/start.py`:**
   - Rewrite the `start_handler` logic.
   - Use `await session.scalar(select(User).where(User.tg_id == message.from_user.id))` to check if the user exists.
   - **IF** user exists: Just send the welcome message with the keyboard.
   - **ELSE**: Create a new `User` object, add it, commit, and then send the message.
2. **Imports:** Ensure `select` is imported from `sqlalchemy`.

## ✅ Definition of Done
- The bot no longer crashes when a registered user sends `/start`.
- The main menu keyboard is shown in both cases (new and existing user).
- Provide the COMPLETE file `bot/handlers/start.py`.