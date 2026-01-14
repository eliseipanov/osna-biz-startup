## Sprint 17: Fix AttributeError in Export Route

**Issue:**
The previous implementation used `admin.get_view('product')`, which does not exist in Flask-Admin, causing an `AttributeError`.

**Correction:**
1. In `admin/app.py`, locate the `export_products` route.
2. Replace the failing line with a direct reference to the registered `ProductView` instance.
3. Access the filtered query correctly:
   - Use `product_view = None` and iterate through `admin._views` to find the one with the endpoint `product`.
   - Or, more simply, use the already initialized `ProductView` class instance if available in the scope, or retrieve it from the admin object's view list.
4. Call `product_view.get_query()` to get the base query and apply the filters using `product_view.get_filters()`.

**Task for Agent Kilo:**
- Fix the `AttributeError` by correctly retrieving the `Product` view instance from the `admin` object.
- Ensure the query passed to `export_products_to_excel_sync` is valid and filtered.