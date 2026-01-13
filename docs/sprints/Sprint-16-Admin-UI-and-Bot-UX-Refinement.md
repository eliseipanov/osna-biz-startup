# Sprint 16: Admin UI Excellence & Hierarchical Bot UX

## 1. Flask-Admin Enhancements
- **Sorting:** Update `ProductView` in `admin/app.py` to enable sorting for relationships.
  - Set `column_sortable_list` to include `('category', 'category.name_uk')` and `('farm', 'farm.name')`.
- **Inline Editing:** Add `column_editable_list = ['price', 'availability_status', 'unit']` for rapid data entry.
- **Price Display:** Ensure prices in the admin list view are displayed with a comma separator (e.g., `5,40 €`).

## 2. Filtered Excel Export
- **Dynamic Query:** Modify the `/admin/export_products` route in `admin/app.py`.
- **Logic:** Extract filter parameters from `request.args` (Flask-Admin filter format).
- **Execution:** Pass the filtered query (instead of all products) to `export_products_to_excel_sync`. If no filters are present, export the full list.

## 3. "Premium" Telegram Bot UI
- **Hierarchy:** Implement navigation flow: `Farms` -> `Categories (filtered by Farm)` -> `Product List` -> `Product Detail`.
- **Visual Style:** - Use `InlineKeyboardMarkup` for all navigation.
  - Product Card: Bold headers, clean descriptions (UK/DE), and prices formatted with commas.
  - Navigation: Add "Back" buttons at every level to ensure smooth UX.
- **Order Flow:** Implement "Add to Cart" and a checkout process that notifies the Manager (Alexey) and the Driver with full order details.

## 4. Content & Localization
- Ensure all 4 categories and 23 products have full UK/DE descriptions.
- Validate that the `safe_encode_for_sql_ascii` function correctly handles German umlauts (ü, ö, ä) during export/import.