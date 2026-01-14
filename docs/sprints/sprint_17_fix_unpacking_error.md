## Sprint 17: Fix Unpacking Error in get_list

**Issue:**
The code failed with `ValueError: not enough values to unpack (expected 5, got 2)` because `get_list()` in Flask-Admin returns a tuple of only two elements: `(count, data)`.

**Correction:**
1. In `admin/app.py`, update the `export_products` route.
2. Change the unpacking line to: `count, products = product_view.get_list(0, None, None, None, None)`.
3. Pass this `products` list directly to the export function.

**Task for Agent Kilo:**
- Correct the `get_list` unpacking logic in `admin/app.py`.
- Ensure the `products` list is correctly passed to `export_products_to_excel_sync`.