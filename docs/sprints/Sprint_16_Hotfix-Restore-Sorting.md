# Hotfix: Restore Missing Table Sorting

## Issue:
Enabling sorting for relationships (Category/Farm) caused all other columns (ID, Name, Price, etc.) to lose their sorting functionality.

## Correction:
Update `column_sortable_list` in `ProductView` to include ALL essential fields alongside relationships:
- `id`
- `name_uk`
- `sku`
- `price`
- `availability_status`
- `('category', 'category.name_uk')`
- `('farm', 'farm.name')`

## Expected Result:
- All column headers should be clickable and sortable again.
- Category and Farm should sort by their respective names.