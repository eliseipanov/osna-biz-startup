# Sprint 24: WebApp UX Overhaul & Bot Navigation Restore

**Objective:** Improve WebApp usability by implementing a focused Category Hero Slider and restore navigation buttons in the Telegram Bot to provide direct access to the Cart.

## Task 1: WebApp Category Hero Slider (`templates/webapp/index.html`)
Refactor the Category display logic to replace the small scrolling list with a large, focused Slider.

1.  **UI Layout:**
    *   Create a container for the active category card.
    *   Add large Left (`<`) and Right (`>`) navigation arrows on the sides.
    *   **Active Card Content:**
        *   Large Image (Aspect Ratio 16:9 or similar).
        *   Overlay/Subtitle: Category Name (Gold).
        *   Below Image: Category Description (Silver).
    *   **Interaction:** Clicking the arrows cycles through categories. Clicking the central image selects that category (loading its products).

2.  **JavaScript Logic:**
    *   Maintain `currentCategoryIndex` state.
    *   Implement `renderCategorySlider()` function to update the DOM based on the current index.
    *   Ensure "All" category is included in the rotation or clearly accessible.

## Task 2: Restore Bot Menu Buttons (`bot/keyboards/main_menu.py`)
Update the `get_main_menu_keyboard` function to include "Cart" and "Orders" buttons again.

1.  **Layout:**
    *   Row 1: `[ 🥩 Catalog ]` (Opens WebApp Home)
    *   Row 2: `[ 🛒 Cart ]` | `[ 📋 Orders ]`
    *   Row 3: `[ 👤 Profile ]` | `[ ℹ️ Impressum ]`
2.  **Cart Button Logic:**
    *   Must use `WebAppInfo`.
    *   URL: Append `?start_mode=cart` to the WebApp URL (e.g., `.../webapp?lang=uk&start_mode=cart`).
3.  **Orders Button:**
    *   For now, standard `KeyboardButton` (no WebApp yet, or placeholder).

## Task 3: WebApp Routing Logic (`templates/webapp/index.html`)
Implement basic client-side routing to handle the `start_mode` parameter.

1.  **HTML Structure:**
    *   Add a new container `<div id="cart-view" class="hidden">`.
    *   Add a placeholder header "Your Cart is Empty" inside it.
2.  **JS Initialization:**
    *   In `DOMContentLoaded`, parse `window.location.search`.
    *   If `start_mode === 'cart'`:
        *   Hide `#discovery-view`.
        *   Show `#cart-view`.
        *   Update the active state of any bottom navigation (if present).

## Constraints
*   **No Database Changes:** Use existing models.
*   **Translations:** Use existing translation keys (`cart_button`, `orders_button`).
*   **Style:** Maintain the Dark/Gold/Graphite theme.

## Definition of Done
*   WebApp displays a single large Category card with navigation arrows instead of a small list.
*   Bot menu shows Cart and Orders buttons.
*   Clicking "Cart" in Telegram opens WebApp directly on the Cart screen (placeholder).