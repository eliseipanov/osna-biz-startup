# Sprint 22.8: Final Export Fix using get_list

**Objective:** Restore search and filter functionality in Export to Excel by using official Flask-Admin methods and resolving the AttributeError.

## Tasks:

1. **Fix Imports in `admin/routes.py`**:
   - Ensure `from sqlalchemy.orm import joinedload` is imported at the top.

2. **Refactor `export_products` Route in `admin/routes.py`**:
   - Find the `ProductView` instance as before.
   - **Remove** manual calls to `_search`, `_filters`, and `_order_by`.
   - **Implementation Logic**:
     1. Call `v_args = product_view._get_list_extra_args()` to capture active UI state.
     2. Call the official method: 
        `count, products = product_view.get_list(page=0, sort_column=v_args.sort, sort_desc=v_args.sort_desc, search=v_args.search, filters=v_args.filters, page_size=10000)`
     3. This method automatically applies all search terms (e.g., "Яло") and filters while ignoring UI pagination limits.
     4. Pass the resulting `products` list to `export_products_to_excel_sync`.

3. **Code Hygiene**:
   - Strictly ensure no system tags (like </content>) are appended to the file.

## Definition of Done:
- Export button works without 500 error.
- Search terms (like "Яло") and Filters are correctly reflected in the exported Excel file.
- The Excel file contains all matching records (up to 10,000), not just the current page.