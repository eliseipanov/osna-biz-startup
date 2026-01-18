# Sprint 23.7: Premium Navigation, Category Carousel, and UI Contrast

**Objective:** Implement category-based navigation within each Farm and fix UI visibility issues.

## Task 1: UI Contrast and Localization (templates/webapp/index.html)
- **Buttons Fix**: Update 'Enter Shop' buttons. They must have a gold border (`border: 2px solid #D4AF37`) and clear gold text on hover. Ensure they don't merge with the card background.
- **Dynamic Labels**: Replace all remaining English text (Back to Farms, Enter Shop) with translations fetched from the API.

## Task 2: Farm Catalog Hierarchy (The "Shop" View)
- When a Farm is selected:
  1. **Hide** the Hero image or shrink it to a small banner.
  2. **Category Carousel**: Below the header, show a horizontal scroll of Categories that contain products for THIS specific farm. 
  3. **Visuals**: Use `Category.image_path` (1:1) for the carousel items.
  4. **Behavior**: Clicking a category filters the vertical product list below. Add an "All" category at the start.

## Task 3: Farm Sorting Logic (admin/routes.py)
- Update `api_farms`: Sort farms so that those with images and active status appear first.

## Task 4: Enhanced Product API (admin/routes.py)
- Update `api_products`: Ensure it can filter by BOTH `farm_id` and `category_id` simultaneously.

## FORBIDDEN ACTIONS:
- STRICT RULE: Do NOT run or modify any files in 'scripts/'.
- STRICT RULE: Do NOT add system tags (</content>) to the code.

## Definition of Done:
- The WebApp feels like a professional store: Farm -> Categories -> Products.
- All buttons are highly visible and localized.
- Categories show their real photos in a horizontal scroll.