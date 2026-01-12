# Sprint 08: Final Infrastructure Expansion
**Project:** Osna-biz-startup

**STEP 1: Database Model Updates (`core/models.py`)**
- **User:** Add `email` (String, unique), `username` (String, unique, without '@'), `password_hash` (String, nullable), `phone` (String, nullable), `language_pref` (String, default='de'), and `admin_notes` (Text).
- **Category & Product:** Add `name_de` (String) and `description_de` (Text) to support multi-language content.
- **Order Model:** Ensure status Enum includes: `NEW`, `VERIFIED`, `PROCUREMENT`, `IN_DELIVERY`, `COMPLETED`, `CANCELLED`. Ensure fields for `delivery_address` and `contact_phone` are present.
- **GlobalSettings:** Create a Key-Value table for global configs (SMTP, Telegram Manager Channel ID, etc.).

**STEP 2: Database Migration (Alembic)**
- Run `alembic revision --autogenerate -m "Expand models for auth, multi-language and workflow"`.
- Run `alembic upgrade head`.

**STEP 3: Admin UI & Auth (`admin/app.py`)**
- Update the login route to allow authentication via `email` OR `username`.
- Ensure all new fields (de_translations, phone, emails) are editable in the Flask-Admin interface.
- Use `SessionLocal` context managers for all synchronous DB operations.