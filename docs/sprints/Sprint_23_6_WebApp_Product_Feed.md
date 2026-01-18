# Sprint 23.6: WebApp Product Feed and Type Mapping

**Objective:** Map farm types to localized strings and implement the transition from Farm selection to the Product Catalog.

## Task 1: Map Farm Types (templates/webapp/index.html)
- Update the JavaScript `loadFarms` function. 
- Instead of displaying `farm.farm_type` directly, map it to a translation key: `type_{farm.farm_type}` (e.g., if type is 'poultry', fetch 'type_poultry').
- Use the `/api/ui/translations` API to get the localized label.

## Task 2: Implement Navigation Logic
- Add a "View State" to the WebApp. By default, it shows "Discovery" (Farms). 
- When a user clicks "Enter Shop" on a Farm card:
  1. Hide the Farm list/Discovery UI.
  2. Show a new section: **Product Feed**.
  3. Fetch products for the selected Farm using: `/api/catalog/products?farm_id=X`.
- Add a "⬅️ Back to Farms" button at the top of the Product Feed.

## Task 3: Product Feed UI (Premium Scroll)
- Create a vertical list of Product Cards in the WebApp.
- **Card Design**:
  - Image (80% width, rounded corners).
  - Title & Price (Gold accent).
  - Description (Silver accent).
  - **Quantity Controls**: `[ - ] [ 0 ] [ + ]` (interactive buttons).
- Ensure localized names (`name_de` / `name`) are used based on the `?lang=` parameter.

## Task 4: API Update (admin/routes.py)
- Ensure `GET /api/catalog/products` accepts an optional `farm_id` parameter to filter products by producer.

## FORBIDDEN ACTIONS (CRITICAL):
- **STRICT RULE**: Do NOT run or modify any files in the `scripts/` directory, including `seed_db.py`.
- **STRICT RULE**: Do NOT add any system tags like `</content>` or `</xai:function_call>` to the source code.

## Definition of Done:
- Farm cards show types in the user's language (e.g., "🍗 Птиця та яйця").
- Clicking a Farm opens a beautiful vertical feed of its products.
- Product names and descriptions match the selected language (UK/DE).