# Sprint-04.2-Emergency-Cleanup.md

## ⚠️ CRITICAL FAILURE: ImportError
You updated `bot/handlers/start.py` to use `Router`, but you failed to update `bot/main.py` correctly. It still tries to import `register_start_handlers`, which no longer exists. This is a violation of the task to provide working code.

## 🛠 Task
1. **Fix `bot/main.py`:** - Remove ALL references to `register_start_handlers`.
   - Use ONLY direct router imports:
     ```python
     from bot.handlers.start import router as start_router
     from bot.handlers.catalog import router as catalog_router
     ```
   - Register them using `dp.include_router(start_router)` and `dp.include_router(catalog_router)`.
2. **Review all files:** Ensure consistency between handlers and the main entry point.

## ✅ Definition of Done
- Provide the COMPLETE and CORRECT file for `bot/main.py`.
- Provide the COMPLETE and CORRECT file for `bot/handlers/start.py` (to ensure it matches).
- The bot must start without `ImportError`.