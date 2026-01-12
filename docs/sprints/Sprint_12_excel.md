# Sprint 12: Proper Excel Exchange (XLSX)

## Context
We are replacing the default CSV export with a robust XLSX system in the osna-biz-startup project. The goal is to integrate core/utils/excel_manager.py directly into the Admin UI.

## Tasks
1. Analyze and Refactor Export:
- Update ProductView in admin/app.py to use .xlsx exclusively.
- Route the export action through the pandas-based logic in core/utils/excel_manager.py.

2. Implement Import UI & Logic:
- Remove the old sidebar "Import" link if it exists.
- Add a visible "Import Excel" button/action directly above the Product table.
- Implement matching logic: ID first, then SKU.

3. Safety First:
- Ensure the import process is wrapped in a database transaction (atomic).
- Analyze the current Flask-Admin version to find the best way to override the list view template for the button.

## Instructions for Kilo
Analyze the current state of admin/app.py and excel_manager.py before coding. Use Linux/WSL paths. If you encounter version conflicts or path issues, ask for clarification.