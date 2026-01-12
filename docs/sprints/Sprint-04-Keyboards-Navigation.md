# Sprint-04-Keyboards-Navigation.md

## ℹ️ Status Update for Agent Kilo
Manual fixes were applied to the project. Please update your local memory for the following files:
1. `migrations/env.py` — Completely rewritten for async support and `.env` loading.
2. `migrations/versions/2026_01_12_initial.py` — Created manually (contains `users`, `products`, `orders` tables).
3. `bot/handlers/start.py` — Updated to use `async_session()` context manager.

---

## 🎯 Goal
Implement a button-based navigation system to replace text commands.

## 🛠 Technical Specifications

### 1. New Keyboard Module
- **File:** `bot/keyboards/main_menu.py`
- **Content:** Create a function `get_main_menu_keyboard()` that returns a `ReplyKeyboardMarkup`.
- **Buttons:** - Row 1: `["🥩 Каталог", "🛒 Кошик"]`
  - Row 2: `["📋 Мої замовлення", "👤 Профіль"]`
- **Settings:** `resize_keyboard=True`, `persistent=True`.

### 2. Update Start Handler
- **File:** `bot/handlers/start.py`
- **Change:** Import the new keyboard and add it to the `message.answer` call in `start_handler`.
- **Message:** "Вітаємо в Osnabrück Farm Connect! Оберіть розділ нижче 👇"

### 3. Catalog Placeholder
- **File:** `bot/handlers/catalog.py` (New file)
- **Content:** - Create a new Router.
  - Add a handler for `F.text == "🥩 Каталог"`.
  - Response: *"Завантажую актуальний прайс від фермерства Homeyer... 🥩"*

### 4. Main Entry Point
- **File:** `bot/main.py`
- **Change:** Include the new `catalog.router`.

## ✅ Definition of Done
- After sending `/start`, the user sees the permanent menu buttons.
- Clicking "🥩 Каталог" triggers the placeholder response.
- No code fragments: provide full updated files for each change.