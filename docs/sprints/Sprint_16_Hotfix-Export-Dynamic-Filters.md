# Hotfix: Correct Filter Application in Export

## Issue:
The `export_products` route manually looks for hardcoded keys like `flt0_category`, but Flask-Admin uses dynamic keys (e.g., `flt1_0`). This causes the filters to be ignored.

## Correction:
In `admin/app.py`, within the `export_products` route, do not parse `request.args` manually. Instead, use the `ProductView`'s existing logic to get the filtered query:

1. Access the `ProductView` instance (or its logic).
2. Use `admin_view.get_query()` which automatically respects all active filters and search terms from `request.args`.
3. Pass the resulting `query` to `export_products_to_excel_sync`.

## Key Change:
Replace manual `if 'fltX_Y' in request.args` checks with a dynamic query builder that follows Flask-Admin's internal filtering state.