# Sprint 15: Fix Admin Export & Dynamic Filename

## Context
The export button in `app.py` currently redirects (302) without downloading the file because the temporary file is deleted too early in the `finally` block.

## Tasks for Kilo:
1. **Fix `export_products` in `app.py`**:
   - Remove the `try...finally` block that unlinks the file immediately.
   - Import `datetime` from `datetime`.
   - Use `datetime.now()` to generate a timestamp for the filename.
   - Set the download name format to `products_YYYYMMDD_HHMM.xlsx`.
   
2. **Implementation Detail**:
```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
filename = f"products_{timestamp}.xlsx"
return send_file(tmp.name, as_attachment=True, download_name=filename)