# Sprint 07: Security, Categories and CMS Foundation
**Project:** Osna-biz-startup
**Paths:** `/core/models.py`, `/admin/app.py`

**Goal:** Implement administrative security, product categorization, and static pages for legal compliance (Impressum/Data Policy).

**Task for Kilo:**
1. **Update `core/models.py`:**
   - Create `Category` class: `id`, `name` (String), `slug` (String, unique), `image_url` (String), `description` (Text).
   - Update `Product` class: Add `category_id` (ForeignKey to `categories.id`).
   - Update `User` class: Add `password_hash` (String, nullable) and `is_admin` (Boolean, default=False).
   - Create `StaticPage` class: `id`, `title` (String), `slug` (String, unique), `content` (Text).

2. **Update `admin/app.py`:**
   - Setup `Flask-Login` and `Werkzeug` security (generate_password_hash, check_password_hash).
   - Implement a basic `LoginForm` and a `/login` route.
   - Secure all `ModelView` classes: overwrite `is_accessible` to return `True` only if `current_user.is_authenticated` and `current_user.is_admin`.
   - Register `Category` and `StaticPage` views in the Admin interface.

3. **Requirements:**
   - Use the existing `async_session` logic where applicable or adapt for Flask-Admin's synchronous needs.
   - Do not break existing database connections.