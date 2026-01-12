# Sprint 08.4: UI Bugfix & Navigation
1. **Fix String Representation:** Add `__str__` method to `Product` model in `core/models.py` returning `self.name`. This will fix the object references in Category multi-select.
2. **Add Logout Route:** Create a `/admin/logout` route in `admin/app.py` using `logout_user()` to allow clean session termination.
3. **Admin UI:** Add a simple "Logout" link to the admin header.

4. **Custom 404 Page:** - Create a global error handler for 404 errors.
   - Design a simple, user-friendly 404 template (using Bootstrap for clean look).
   - Use `Translation` keys for the 404 message ("Page not found" / "Сторінку не знайдено").