# Sprint 22.6: Restore Bot/Excel Logic and Purge Code Garbage

**Objective:** Fix crashes in Bot and Excel after schema changes and strictly prevent system tags from entering source files.

## Task 1: Fix Bot Catalog Logic (bot/handlers/store.py)
- **Issue:** The query still looks for `Product.category_id` which was removed.
- **Fix:** Update the query in `show_category_products` to use a Join.
- **Logic:** `select(Product).join(Product.categories).where(Category.id == category_id)`.
- **Note:** Ensure it filters only `AvailabilityStatus.IN_STOCK`.

## Task 2: Update Excel Manager (core/utils/excel_manager.py)
- **Export Logic:** In `export_products_to_excel_sync`, replace `category_name` with a string containing all product categories separated by commas.
- **Import Logic:** In `import_products_from_excel_sync`, parse the category string (split by comma), find the Category objects in the DB, and assign the list to `product.categories`.

## Task 3: CRITICAL Code Hygiene
- **Issue:** System tags (like </content>, </xai:function_call>) are appearing INSIDE .py files.
- **Strict Requirement:** You MUST NOT write any text to source files that is not valid Python code. Verify the end of every file you modify (`admin/app.py`, `admin/routes.py`, etc.) and REMOVE any trailing system tags or markdown artifacts.

## Definition of Done:
- Bot shows products correctly for both languages.
- Excel Export/Import successfully handles multiple categories.
- No non-Python characters/tags exist in the source code files.