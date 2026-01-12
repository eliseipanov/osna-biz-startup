# Sprint 13: Fixing Database Context & Image Rendering

## Context
1. The Excel export fails with `greenlet_spawn` because the synchronous Flask app attempts to call an async SQLAlchemy core via `asyncio.run()`.
2. Image previews in the list view appear as raw HTML text instead of actual images because the column output is escaped.

## Tasks
1. Fix Greenlet Error (Export/Import):
- In `admin/app.py`, refactor the export/import routes.
- Use a synchronous database connection for Flask-Admin or implement a proper bridge to the async core that doesn't break the SQLAlchemy session context.
- Ensure the `ExcelManager` calls are handled safely within the Flask request cycle.

2. Fix Image Previews (MarkupSafe):
- In `admin/app.py`, update the `column_formatters` for `ProductView`, `CategoryView`, and `FarmView`.
- Wrap the `<img>` tag output in `markupsafe.Markup()` to prevent HTML escaping.
- Example: `return Markup(f'<img src="{path}" ...>')`.

3. Code Hygiene:
- Verify that NO `extra_html` variables remain in `app.py`.
- Ensure all UI logic is strictly inside the templates created in the previous step.

## Instructions for Kilo
We are on Flask-Admin 2.0.2. The database is `postgresql+asyncpg`. The 'greenlet_spawn' error is the priority. For images, use `from markupsafe import Markup` to allow HTML rendering in the list columns.