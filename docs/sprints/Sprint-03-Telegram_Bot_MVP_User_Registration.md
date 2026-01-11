# Sprint 03: Telegram Bot MVP & User Registration

## 🎯 Goal
Create a basic Telegram bot using `aiogram 3.x` that greets the user and automatically registers/updates them in the PostgreSQL database.

## 🛠 Technical Specifications
1. **Entry Point:**
   - Create `bot/main.py`.
   - Initialize `Dispatcher` and `Bot` using `BOT_TOKEN` from `.env`.
2. **Handlers:**
   - Create `bot/handlers/start.py`.
   - Implement a `/start` command handler:
     - Check if the user exists in the `users` table via `tg_id`.
     - If not, create a new record. If yes, update the `full_name`.
     - Reply with: "Привіт, [Name]! Вітаємо в Osnabrück Farm Connect. Реєстрація успішна."
3. **Database Integration:**
   - Use `get_session()` from `core.database` for DB operations within handlers.
4. **Middlewares (Optional but recommended):**
   - Ensure a clean way to pass the DB session to handlers.

## ✅ Definition of Done
- `bot/main.py` starts without errors.
- When I send `/start` to the bot, a new record appears in the `users` table.
- Provide complete code for `bot/main.py` and `bot/handlers/start.py`.