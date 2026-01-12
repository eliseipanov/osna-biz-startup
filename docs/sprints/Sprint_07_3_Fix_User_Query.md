# Sprint 07.3: Fix User Query in Login Route
**File:** `/var/www/osna-biz-startup/admin/app.py`

**Task for Kilo Code Agent:**
The login route fails because it uses `User.query`, which doesn't exist in our SQLAlchemy 2.0 setup. We must use a synchronous-style execution or a scoped session compatible with Flask-Admin.

**Code Update:**
Replace the line:
`user = User.query.filter_by(tg_id=int(form.username.data)).first()`

With this logic (using our session):
```python
        # Correct SQLAlchemy 2.0 way for our setup
        from sqlalchemy import select
        from core.database import SessionLocal # Or the sync engine if Flask-Admin is sync
        
        with SessionLocal() as session:
            user = session.execute(select(User).where(User.tg_id == int(form.username.data))).scalar_one_or_none()

___________________________________________________________
Note: Ensure User and select are imported in admin/app.py.