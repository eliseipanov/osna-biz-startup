# Hotfix: Complete Sorting for ProductView

## Issue:
The German name field (`name_de`) and measurement units (`unit`) are currently not sortable.

## Correction:
Update `column_sortable_list` in `ProductView` (`admin/app.py`) to include these fields.