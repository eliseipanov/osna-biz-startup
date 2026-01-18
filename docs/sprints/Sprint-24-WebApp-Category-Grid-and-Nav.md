# Sprint 24: WebApp Category Grid & Bot Navigation Restore

**Objective:** Replace the Category Slider with a user-friendly 2-column Grid (Tile layout) for better overview, and restore navigation buttons in the Telegram Bot to provide direct access to the Cart.

## Task 1: WebApp Category Grid (`templates/webapp/index.html`)
Refactor the Category display logic to replace the Slider/Carousel with a **2-column Grid**.

1.  **Grid Layout:**
    *   Container: Use CSS Grid with 2 columns (`grid grid-cols-2 gap-4`).
    *   **Card Design:**
        *   Shape: Square (`aspect-square`).
        *   Background: Category Image (`object-cover`, full width/height).
        *   Overlay: Dark semi-transparent layer (`bg-black bg-opacity-50`) over the whole image to ensure text readability.
        *   Text: Category Name centered horizontally and vertically (`flex items-center justify-center`). Style: Gold, Bold, Large.
    *   **Interaction:** Clicking a tile selects the category and loads products below.
    *   **Active State:** The selected category tile must have a distinct Gold Border (`border-2 border-gold`) or visual highlight.

2.  **JavaScript Logic (`loadCategories` & `renderCategories`):**
    *   **Remove "All" Item:** Do not manually inject the "All" placeholder item. Render only categories fetched from the API.
    *   Render the grid items dynamically.
    *   Ensure clicking a tile updates `selectedCategory` and calls `loadProducts()`.

## Task 2: Restore Bot Menu Buttons (`bot/keyboards/main_menu.py`)
Update the `get_main_menu_keyboard` function to include "Cart" and "Orders" buttons.

1.  **Layout:**
    *   Row 1: `[ 🥩 Catalog ]` (Opens WebApp Home)
    *   Row 2: `[ 🛒 Cart ]` | `[ 📋 Orders ]`
    *   Row 3: `[ 👤 Profile ]` | `[ ℹ️ Impressum ]`
2.  **Cart Button Logic:**
    *   Must use `WebAppInfo`.
    *   URL: Append `?start_mode=cart` to the WebApp URL (e.g., `.../webapp?lang=uk&start_mode=cart`).
3.  **Orders Button:**
    *   Standard `KeyboardButton` (placeholder text response is fine for now).

## Task 3: WebApp Routing Logic (`templates/webapp/index.html`)
Implement basic client-side routing to handle the `start_mode` parameter.

1.  **HTML Structure:**
    *   Ensure a container `<div id="cart-view" class="hidden">` exists.
    *   Add a placeholder header "Your Cart is Empty" inside it.
2.  **JS Initialization:**
    *   In `DOMContentLoaded`, parse `window.location.search`.
    *   If `start_mode === 'cart'`:
        *   Hide `#discovery-view` and `#shop-view`.
        *   Show `#cart-view`.

## Constraints
*   **Images:** Use existing 400x400 category images; they fit perfectly in square tiles.
*   **Style:** Maintain the Dark/Gold/Graphite theme.
*   **Clean Code:** Remove old Slider HTML/CSS/JS code to avoid clutter.

## Definition of Done
*   WebApp displays categories as a 2x2 grid (Tiles) with centered text.
*   Clicking a tile highlights it and filters products.
*   Bot menu shows Cart and Orders buttons.
*   Clicking "Cart" in Telegram opens WebApp directly on the Cart screen.