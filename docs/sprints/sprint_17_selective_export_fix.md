## Sprint 17: Fix Selective Export Filtering Logic

**Issue:**
The export currently downloads ALL products even when filters are active in the Admin UI. This happens because `get_query()` is called without applying the active filters from `request.args`.

**Requirements:**
1. **Apply Filters to Query:** In `admin/app.py`, the `export_products` route must not only get the view but also apply the filters. Use:
   `view = next(v for v in admin._views if v.endpoint == 'product')`
   `index_view_data = view.get_list(0, None, None, None, None)`
   This is the standard Flask-Admin way to get the exact filtered data.
2. **Data Extraction:** Extract the products from the `index_view_data[1]` (which is the actual filtered queryset).
3. **Consistency:** Ensure the resulting list is passed to `export_products_to_excel_sync`.

**Task for Agent Kilo:**
- Modify the `export_products` route to correctly apply current session filters before generating the Excel file.
- Ensure that if "Свинина" is selected in the UI, only "Свинина" appears in the Excel.