# Sprint 22.9: Default Sorting by ID

**Objective:** Implement consistent numeric sorting for the product list and Excel export.

## Task 1: Update ProductView in admin/admin_views.py
- Locate the `ProductView` class.
- Add the following attribute:
  `column_default_sort = ('id', False)`
- This ensures that the base query for the UI and the `get_list()` method (used in export) always orders items by ID ascending (1, 2, 3...).

## Definition of Done:
- The Admin product list is sorted by ID by default.
- The exported Excel file displays products in numeric order by ID.