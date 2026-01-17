# Sprint-19-Medium-Priority-Improvements.md
**Date:** January 17, 2026
**Goal:** Implement medium-priority improvements for better performance and maintainability

## Medium Priority Improvements

### 1. Refactor Excel Manager Duplicate Code
- **File:** `core/utils/excel_manager.py`
- **Issue:** Sync and async versions have 90% identical code
- **Fix:** Create base class or shared functions to eliminate duplication
- **Testing:** Both sync and async functions work identically

### 2. Product List Pagination
- **File:** `admin/app.py:248`
- **Issue:** Fetches all products at once (page_size=10000) - inefficient
- **Fix:** Implement proper pagination (e.g., 50 items per page)
- **Testing:** Admin product list loads faster, shows page controls

### 3. Localization Support
- **Files:** `bot/keyboards/main_menu.py`, `core/models.py`
- **Issue:** Only Ukrainian language support
- **Fix:** Add German translations for bot keyboards and product fields
- **Testing:** Bot responds in German when user language is German

### 4. API Documentation
- **File:** `docs/API.md` (new)
- **Issue:** No API documentation
- **Fix:** Create basic API documentation for admin endpoints
- **Testing:** Documentation accessible and accurate

### 5. Database Indexes
- **File:** `core/models.py`
- **Issue:** No indexes on frequently queried fields
- **Fix:** Add indexes to `Product.availability_status`, `Product.category_id`, `User.language_pref`
- **Testing:** Query performance improved (measure with EXPLAIN)

## Deployment Notes
- Run database migrations for new indexes
- Update environment variables if needed
- Test in staging before production

## Files to Modify
- core/utils/excel_manager.py
- admin/app.py
- bot/keyboards/main_menu.py
- core/models.py
- docs/API.md (new)