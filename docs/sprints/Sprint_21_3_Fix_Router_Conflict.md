# Sprint 21.3: Fix Router Conflict and Store Imports

**Issue:** 
- The bot still shows the old text catalog because `catalog_router` is registered before `store_router`.
- `bot/handlers/store.py` has a missing import for `sqlalchemy.func`.

**Tasks:**
1. **Update `bot/main.py`**:
   - REMOVE or comment out `from bot.handlers.catalog import router as catalog_router`.
   - REMOVE or comment out `dp.include_router(catalog_router)`.
   - Ensure ONLY `store_router` handles the catalog logic.

2. **Fix Imports in `bot/handlers/store.py`**:
   - Add `import sqlalchemy` at the top of the file to fix the `sqlalchemy.func.count()` NameError.

**Verification:**
- Save files and restart the bot.
- Pressing `🥩 Каталог` should now show Inline buttons with Categories.