## Sprint 17: Final Fix for Selective Export (Proper get_list arguments)

**Context:**
The current export fails to filter because `product_view.get_list` is called with `None` arguments, which bypasses Flask-Admin's filtering logic.

**Requirements:**
1. **Dynamic Argument Capture:** In `admin/app.py`, the `export_products` route must retrieve active filters, search, and sort parameters from the request before calling `get_list`.
2. **Correct get_list call:**
   - Use `view.get_filters_arg()` to get active filter values.
   - Use `view.get_sort_column_default()` or capture sort from `request.args`.
   - Call `get_list` using these captured parameters instead of `None`.
3. **Excel Manager Sync:** Ensure `export_products_to_excel_sync` in `core/utils/excel_manager.py` accepts the `products` list (not a query) as implemented in the last iteration.

**Task for Agent Kilo:**
- Update `admin/app.py` to properly resolve `sort_column`, `sort_desc`, `search`, and `filters` from the `product_view` methods.
- Call `count, products = product_view.get_list(0, sort_column, sort_desc, search, filters, page_size=9999)`.
- This will ensure the exported Excel matches the screen exactly.