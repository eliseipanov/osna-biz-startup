# Sprint 25.1: Hotfix - Cart Logic & UI Accessibility

**Objective:** Fix the "0.0 Total" bug by storing product prices in the cart state (preventing data loss on navigation), and drastically improve the UI accessibility for the Sticky Footer and Scroll-to-Top button.

## Task 1: Redesign Cart Data Structure (`templates/webapp/index.html`)
The current simple state `{id: qty}` causes the "0.0 Total" bug when navigating between categories because prices are lost.

1.  **New Structure:** Change `cartState` to store full item details:
    ```javascript
    cartState = {
        "12": { "qty": 2, "price": 5.50, "name": "Sausage" },
        "15": { "qty": 1, "price": 4.00, "name": "Meat" }
    }
    ```
2.  **Refactor `addToCart`:** Update function to accept the full `product` object (price, name) and save it to `localStorage`.
3.  **Refactor `getCartTotal`:** Calculate total strictly from `cartState` stored prices, NOT from the currently visible product list.
4.  **Migration:** Add a check on load: if `cartState` contains old format (numbers only), clear it to prevent errors.

## Task 2: Sticky Footer Overhaul (Clickable & Visible)
The current footer is "invisible" and hard to click.

1.  **Interaction:** Make the **entire** `#sticky-cart` container clickable. Clicking anywhere on the bar calls `showCartView()`.
2.  **Visuals:**
    *   Add a top border: `border-t-4 border-gold`.
    *   Background: Darker, high contrast (`bg-gray-900`).
    *   Text: Larger font (`text-xl`).
    *   Add a prominent arrow or icon: "🛒 View Cart ➔".
3.  **Layout:** Ensure it sits *on top* of all content (`z-50`).

## Task 3: "Grandmother-Friendly" Scroll-to-Top
1.  **Size:** Increase size significantly (e.g., `w-16 h-16` or `64px`).
2.  **Icon:** Large, bold arrow.
3.  **Position:** Ensure it does not overlap with the Sticky Footer (move it up slightly).

## Definition of Done
*   Cart Total remains correct (not 0.0) even after closing and reopening the app.
*   The bottom bar is fully clickable and clearly visible (High Contrast).
*   Scroll-to-Top button is large and easy to hit.