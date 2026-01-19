# Sprint 25: WebApp Cart Logic, Persistence & UI

**Objective:** "Bring the Cart to Life". Implement JavaScript logic to store cart items in `localStorage`, create a "Sticky Footer" for quick cart access, implement a "Scroll to Top" button, and finalize the Checkout data handoff.

## Task 1: JavaScript Cart Logic (`templates/webapp/index.html`)
Implement a robust `cartState` object and functions:
1.  **State Structure:** `{ productId: quantity }` (e.g., `{ "12": 2, "5": 1 }`).
2.  **Persistence:** Save `cartState` to `localStorage` on every change. Load it on page start (`DOMContentLoaded`).
3.  **Functions:**
    *   `addToCart(id, qty)`
    *   `removeFromCart(id)`
    *   `getCartTotal()` (Calculate total sum based on product prices).
    *   `getCartCount()` (Total number of items).
4.  **Sync:** When loading the Product Feed, buttons (`+/-`) must reflect the stored state (e.g., if I bought 2 steaks, left, and came back — it should show "2").

## Task 2: Sticky Footer (Floating Cart)
Add a fixed bar at the bottom of the screen (`#sticky-cart`).
1.  **Visibility:** Hidden if cart is empty. Visible if items > 0.
2.  **Content:**
    *   Total items count (e.g., "3 items").
    *   Total Price (e.g., "45.50 €").
    *   Button: "View Cart" (Opens `#cart-view`).
3.  **Style:** Dark background (opacity 95%), Gold text, z-index high.

## Task 3: Scroll to Top Button
1.  **UI:** Small circular button with an Up Arrow (⬆️).
2.  **Position:** Bottom-right, just above the Sticky Footer.
3.  **Logic:** Hidden initially. Becomes visible after scrolling down 300px. Clicking it smooth-scrolls to top.

## Task 4: Finalize Cart View (`#cart-view`)
Replace the "Empty" placeholder with a real list when items exist.
1.  **List Items:** Show Name, Unit Price, Quantity controls (`- 1 +`), Total for item.
2.  **Delete:** Logic to remove item if quantity goes to 0.
3.  **Grand Total:** Display final sum at the bottom.
4.  **Checkout Button:**
    *   **Action:** `Telegram.WebApp.sendData(JSON.stringify(orderData))`.
    *   **Data Structure:** `{"items": [{"id": 1, "qty": 2, "price": 10.5}, ...], "total": 21.0}`.
    *   **Translation:** Label button as `translations.webapp_checkout` (add key if missing, fallback "Checkout").

## Definition of Done
*   Cart data survives page reload (localStorage).
*   Sticky Footer appears when products are added.
*   Scroll to Top works.
*   "Cart View" shows correct items and total price.
*   Clicking "Checkout" closes the WebApp (data sending logic implemented in JS).