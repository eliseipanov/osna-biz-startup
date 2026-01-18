# Sprint 22.4: Circular Dependency and Database Access Fix

**Objective:** Resolve the 'AttributeError: db' and circular import issues by implementing the shared extensions pattern.

## Task 1: Create Shared Extensions Module
- Create `admin/extensions.py`.
- Define global instances of `db` (SQLAlchemy), `login_manager` (LoginManager), and `limiter` (Limiter) in this file.
- These instances should not be bound to the app immediately: `db = SQLAlchemy()`, etc.

## Task 2: Refactor admin/app.py (Application Factory)
- Remove local definitions of `db`, `login_manager`, and `limiter`.
- Import these instances from `extensions.py`.
- Initialize them using the `init_app(app)` pattern:
  - `db.init_app(app)`
  - `login_manager.init_app(app)`
  - `limiter.init_app(app)`
- Ensure `admin` (Flask-Admin) still uses `db.session` correctly.

## Task 3: Fix admin/routes.py and admin/admin_views.py
- Remove the `init_db` function and `@admin_api.before_app_request` hook from `routes.py`.
- Import `db`, `login_manager`, and `limiter` from `extensions.py` in both files.
- Use `db.session` directly for all database operations.
- Ensure `LoginForm` and all routes correctly reference the shared instances.

## Definition of Done:
- Flask server starts without `AttributeError`.
- Admin panel is accessible via browser.
- PayPal simulation and Export/Import features work using the shared database session.