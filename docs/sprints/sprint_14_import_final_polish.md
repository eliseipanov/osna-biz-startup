# Sprint 14: Final Polish for Excel Manager

## Tasks
1. Link Relationships by Name:
   - During import, if `category_name` or `farm_name` is provided, find the corresponding ID in the database and link the product.

2. Handle SQL_ASCII Encoding (Crucial):
   - Our PostgreSQL database uses `SQL_ASCII`. To prevent mojibake (broken characters) in Excel:
   - When Exporting: Ensure strings from DB are handled as: `value.encode('latin-1').decode('utf-8')` if they contain non-ASCII characters.
   - When Importing: Ensure strings from Excel are stored correctly to match this behavior.

3. Availability Status:
   - Map string values from Excel (e.g., 'IN_STOCK') to the `AvailabilityStatus` Enum before saving to the database.

## Instructions for Kilo
In `excel_manager.py`, pay special attention to the encoding. Since the DB is SQL_ASCII, SQLAlchemy might return mangled strings. Use the manual decode/encode bridge we used in the Admin View formatters to ensure product names like 'Шинка' stay readable in the XLSX file and after re-import.