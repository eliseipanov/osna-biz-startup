# Sprint-04.1-Fix-Imports.md

## ⚠️ Problem
Bot fails to start with `ImportError: cannot import name 'catalog' from 'bot.handlers'`.

## 🛠 Task
1. **Update `bot/main.py`:**
   Change the imports from:
   `from bot.handlers import start, catalog`
   To:
   ```python
   from bot.handlers.start import router as start_router
   from bot.handlers.catalog import router as catalog_router

2. Update Router registration: Instead of dp.include_router(start.router) and dp.include_router(catalog.router), use:

Python

dp.include_router(start_router)
dp.include_router(catalog_router)

3. Definition of Done
Provide the full corrected content of bot/main.py!
No changes to __init__.py needed if imports are direct.