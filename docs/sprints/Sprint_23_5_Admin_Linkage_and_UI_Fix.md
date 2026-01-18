# Sprint 23.5: Admin Linkage and WebApp UI Polish

**Objective:** Enable linking Farms to Regions in the Admin panel and clean up visual artifacts in the WebApp.

## Task 1: Update Admin Visibility (admin/admin_views.py)
- **Locate `FarmView`**:
  - Add `'region'` to the `column_list`.
  - Add `'region': 'Регіон'` to the `column_labels`.
- This will allow the user to select a Region from a dropdown list when editing a Farm.

## Task 2: Clean WebApp Template (templates/webapp/index.html)
- **Emoji Removal**: Remove all hardcoded emojis (🥩, 🥕, 🐟) from the HTML buttons (`farm-type-btn`). Labels must come strictly from the `/api/ui/translations` API.
- **Region Display**: In the JavaScript `loadFarms` function, replace the usage of `farm.location` with the farm's associated region name if available.
- **Design Check**: Ensure that if a translation for a farm type button is missing, it displays a fallback string instead of nothing.

## Task 3: Robust API Filtering (admin/routes.py)
- **Update `api_farms`**: Ensure that the `farm_type` filter is case-insensitive (convert both DB value and request parameter to lowercase during comparison).
- **Data Enrichment**: Ensure the farm object returned by the API includes the `region_name` (fetched from the related Region model).

## Task 4: Code Hygiene
- Check the end of `admin/app.py` and `admin/routes.py` for any non-Python tags (like </content>) and remove them.

## Definition of Done:
- The user can select a Region for a Farm in the Admin panel.
- The WebApp shows only one emoji per category button.
- Selecting a Region in the WebApp correctly filters and displays the linked farms.