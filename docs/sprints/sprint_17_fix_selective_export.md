## Sprint 17: Fix Selective Export Functionality

**Context:**
The current export logic in `admin/app.py` is broken because it manually parses `request.args` using hardcoded indices (flt0_0, etc.). This makes selective export unreliable. We need to use Flask-Admin's internal query generation to ensure the exported file matches exactly what the user sees on the screen.

**Requirements:**
1. **Dynamic Filter Capture:** Update the `export_products` route in `admin/app.py`. Instead of manual parsing, use the `ProductView` instance to get the filtered query: `query = admin.get_view(Product).get_query()`.
2. **Apply Active Filters:** Ensure `get_query()` is combined with `request.args` so that search results and filters (Category, Farm, Status) are respected in the export.
3. **Execute Sync:** The `export_products_to_excel_sync` function in `core/utils/excel_manager.py` must execute this generated query within the current `db.session`.

**Task for Agent Kilo:**
- Refactor `export_products` in `admin/app.py` to be truly dynamic and filter-aware.
- Ensure `core/utils/excel_manager.py` handles the incoming filtered query object correctly.
- Do not break the existing `safe_encode_for_sql_ascii` logic.