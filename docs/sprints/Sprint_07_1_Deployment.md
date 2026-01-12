# Sprint 07.1: Infrastructure & Alembic Migration
**Project:** Osna-biz-startup

**Task for Kilo:**
1. **Pip Install:** Execute `/var/www/osna-biz-startup/.venv/bin/pip install flask-login flask-wtf email-validator` to support the new security features.

2. **Alembic Migration:**
   - Run `alembic revision --autogenerate -m "Add categories and security"` to detect new models (Category, StaticPage) and new columns (is_admin, password_hash, category_id).
   - Run `alembic upgrade head` to apply changes to the PostgreSQL database.

3. **Admin Setup Script:**
   - Create a script `/var/www/osna-biz-startup/scripts/setup_admin.py`.
   - The script must:
     - Take a Telegram ID and a password as input.
     - Hash the password using `werkzeug.security.generate_password_hash`.
     - Update the corresponding user in the `users` table: set `is_admin = True` and save the `password_hash`.