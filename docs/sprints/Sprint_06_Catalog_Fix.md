# Sprint 06: Catalog Database Integration
**Target File:** `/var/www/osna-biz-startup/bot/handlers/catalog.py`

**Task for Kilo:**
Kilo, update the file `/var/www/osna-biz-startup/bot/handlers/catalog.py` to fetch real data from the database.
1. Import `select` from `sqlalchemy`.
2. Import `async_session` from `core.database` and `Product` from `core.models`.
3. In `catalog_handler`, use `async with async_session()` to fetch all products where `is_available=True`.
4. Format the output as a list: `Name - Price €/unit` using HTML.
5. Provide the full updated file.