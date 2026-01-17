# Sprint 21.9: Architectural Cleanup & Routing Fix

**Objective:** Fix the crash on /start, resolve function name conflicts in keyboards, and centralize translation logic.

**Tasks:**

1. **Centralize Helpers:**
   - Create a new file `bot/utils.py`.
   - Move `TranslationFilter` class and `get_translation` function there to avoid code duplication in start.py and store.py.

2. **Fix Keyboard Conflict (`bot/keyboards/main_menu.py`):**
   - REMOVE the duplicate synchronous `get_main_menu_keyboard` function.
   - Keep ONLY the `async def get_main_menu_keyboard(user_language)`.
   - Remove the "(WebApp Placeholder)" suffix from the button text (use clean DB values).

3. **Fix Routing and Imports:**
   - In `bot/handlers/start.py`: Import `TranslationFilter` and `get_main_menu_keyboard` correctly. 
   - In `bot/handlers/store.py`:
     - Remove the generic `handle_catalog_message` that has no filter.
     - Apply `@router.message(TranslationFilter("catalog_button"))` to the `show_categories` function.
     - Ensure it uses the centralized `TranslationFilter`.

4. **Onboarding logic:**
   - Ensure `start_handler` properly awaits the async keyboard and uses the centralized translation helper.

**Definition of Done:**
- /start command works without errors.
- Buttons are localized correctly based on the language in the DB.
- No duplicate code for filters in handlers.