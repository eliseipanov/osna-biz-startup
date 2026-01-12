# Sprint 11: Robust Admin & Data Safety

## 1. UI & Templates
- Move all inline HTML from `admin/app.py` to `admin/templates/admin/`.
- Create `admin/templates/admin/master.html` to override the Flask-Admin layout.
- Implement a Dark/Light mode toggle (Bootstrap 5.3) with `localStorage` persistence.
- Add 50px image thumbnails to the Product list table.
- Add sidebar filters (Category, Farm, Status) and search (Name, SKU).

## 2. Excel Exchange (Safe & Detailed)
- Update `core/utils/excel_manager.py` to use pandas for `.xlsx`.
- Replace sidebar "Import" MenuLink with buttons directly above the Product table.
- Implement Atomic Imports: If any row fails, roll back all changes (`db.session.begin_nested()`).
- Return a detailed report: "Row X: [Error Message]" or "Success".
- Matching Logic: Match by `id` first, then by `sku`.