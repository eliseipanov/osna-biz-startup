# Sprint 07.5: Populate Categories and Link Products
**Project:** Osna-biz-startup

**Task for Kilo Code Agent:**
The database is currently missing the actual category records. We need to update and run the seeding script to ensure categories exist before products are linked to them.

1. **Update `scripts/seed_db.py`**:
   - Ensure it first creates the categories: `Schwein`, `Rind`, `Wurst`, `Mix`.
   - Ensure it correctly assigns `category_id` to each of the 23 products based on their names/types.

2. **Execute Seeding**:
   - Run `/var/www/osna-biz-startup/.venv/bin/python3 scripts/seed_db.py`.