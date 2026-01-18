# Sprint 22.3: Final Admin Cleanup and Route Removal

**Objective:** Clean up admin/app.py by removing all redundant logic that has been moved to admin_views.py and routes.py.

## Tasks:

1. **Purge `admin/app.py`**:
   - REMOVE all `@app.route` handlers (login, logout, export_products, import_products, paypal_simulate).
   - REMOVE the `LoginForm` class definition.
   - REMOVE the `UserView`, `ProductView`, `FarmView`, `CategoryView`, `TransactionView`, and `SecureModelView` class definitions (they are now in admin_views.py).
   - REMOVE redundant imports that are no longer used in app.py (redirect, url_for, flash, check_password_hash, etc.).

2. **Final Structure of `admin/app.py`**:
   - It should ONLY contain: App initialization, DB setup, LoginManager config, Blueprint registration, and Admin views registration.

3. **Fix `admin/routes.py` Imports**:
   - Ensure it imports `db` correctly from `app` without creating a circular dependency (use `from app import db` inside the functions or at the top if handled correctly).

4. **Verify Consistency**:
   - Ensure `login_manager.login_view` is set to `'admin_api.login'`.

**Definition of Done:**
- admin/app.py is less than 100 lines of code.
- No duplicate route handlers exist in the project.
- Pylance/VS Code shows zero errors in app.py.