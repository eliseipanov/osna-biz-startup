# docs/sprints/sprint_17_final_export_fix.md

## Sprint 17: Fix Selective Export

**Context:**
Fix the AttributeError and ensure the export respects UI filters.

**Task for Agent Kilo:**
In `admin/app.py`, replace the `export_products` route logic with:
1. Find the `product_view` from `admin._views`.
2. Get arguments: `v_args = product_view._get_list_extra_args()`.
3. Fetch data: `count, products = product_view.get_list(page=0, sort_column=v_args.sort, sort_desc=v_args.sort_desc, search=v_args.search, filters=v_args.filters, page_size=10000)`.
4. Pass `products` to `export_products_to_excel_sync(db.session, tmp.name, products=products)`.