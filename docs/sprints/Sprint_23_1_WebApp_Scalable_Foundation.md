# Sprint 23_1: WebApp Scalable Foundation and Premium UI

**Objective:** Implement Regions, update Farm models for scalability, and create the basic Premium WebApp interface.

## Task 1: Scalability Models (core/models.py)
1. **Create `Region` Model**:
   - Fields: `id` (PK), `name` (String), `name_de` (String), `slug` (String, unique).
2. **Update `Farm` Model**:
   - Add `region_id = Column(Integer, ForeignKey("regions.id"), nullable=True)`.
   - Add `farm_type = Column(String(50))` (e.g., 'meat', 'vegetables', 'fish').
   - Establish relationship: `Region.farms <-> Farm.region`.

## Task 2: API and Admin Updates
1. **admin/admin_views.py**: Add `RegionView` and update `FarmView` to include the new fields.
2. **admin/routes.py**: 
   - Create a route `GET /webapp` that renders `webapp/index.html`.
   - Create API `GET /api/catalog/regions` to return all regions.
   - Update `GET /api/catalog/farms` to allow filtering by `region_id` and `farm_type`.

## Task 3: WebApp Premium Shell (templates/webapp/index.html)
1. Create a basic HTML5 template using **Tailwind CSS** (via CDN).
2. **Design System**:
   - Background: Graphite (`#121212`)
   - Text/Dividers: Silver (`#E0E0E0`)
   - Primary/Action/Price: Gold (`#D4AF37`)
   - Font: **'Montserrat'** (import from Google Fonts).
3. **Layout Structure**:
   - Header with localized Title (e.g., "FARM CONNECT") and a placeholder for Logo.
   - A scrollable list of Regions and Farm Types.
   - A placeholder for the Farm list.

## Task 4: Bot Integration (bot/keyboards/main_menu.py)
1. Update `get_main_menu_keyboard`:
   - Change the 'Catalog' button to use `types.WebAppInfo(url="https://7568db916eec.ngrok-free.app/webapp")`.
   - Ensure the button text is fetched from the database ('catalog_button' key).

## Task 5: Database Seed
- Create a temporary script or update `scripts/seed_db.py` to add at least 1 Region (Osnabrück) and 2-3 placeholder Farms of different types (Vegetables, Fish).

## Definition of Done:
- Running 'python admin/app.py' and clicking the button in the bot opens a Dark/Graphite/Gold web page.
- The database schema is updated to support multiple Regions and Farm types.