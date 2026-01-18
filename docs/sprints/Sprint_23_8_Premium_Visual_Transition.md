# Sprint 23.8: Premium UI, iOS Expand and Visual Feed

**Objective:** Implement full-screen mode for iOS, fix view transitions, and create a visual-first product feed.

## Task 1: WebApp Initialization (templates/webapp/index.html)
- Add Telegram WebApp SDK: `<script src="https://telegram.org/js/telegram-web-app.js"></script>`.
- In JavaScript, call `window.Telegram.WebApp.ready()` and `window.Telegram.WebApp.expand()`. This will fix the half-screen issue on iOS.

## Task 2: View State Management (The "Clean" Transition)
- Create two main containers: `<div id="discovery-view">` and `<div id="shop-view" class="hidden">`.
- **Discovery View**: Contains Hero Header, Regions, Farm Types, and Farm List.
- **Shop View**: Contains ONLY the "Back" button, Farm Info (Name/Desc), Category Carousel, and Product Feed.
- **Logic**: When entering a shop, hide the ENTIRE Discovery View. No more double headers or region lists.

## Task 3: Visual Category Carousel
- Instead of generating categories from products, fetch them from a new API: `GET /api/catalog/categories?farm_id=X`.
- **UI**: Horizontal scroll of cards.
- **Design**: Image (horizontal 21:9 or 16:9), Title OVER the image with a dark gradient overlay.

## Task 4: Instagram-Style Product Feed
- **Layout**: Vertical scroll of large cards.
- **Image**: Square (1:1), 100% width of the card.
- **Caption**: Below the image, show Name (Gold), Price (Gold), and Description (Silver).

## Task 5: Localization and Key Mapping
- You MUST use the `webapp_` prefix for all keys:
  - 'webapp_enter_shop', 'webapp_back_to_farms', 'webapp_all_items', 'webapp_farm_types', etc.
- Map Farm Types correctly: `type_meat`, `type_vegetables`, etc.

## Task 6: API Update (admin/routes.py)
- Ensure `GET /api/catalog/categories` supports a `farm_id` parameter to return only categories used by that farm.
- Ensure all API results are sorted by `id` ASC.