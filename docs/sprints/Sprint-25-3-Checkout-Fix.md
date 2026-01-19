# Sprint 25.3: Hotfix - Checkout Interaction & Localization

**Objective:** Make the Checkout button clickable (fix event delegation), ensure visibility (yellow background), and localize the "View Cart" text in the sticky footer.

## Task 1: Fix Checkout Click (`templates/webapp/index.html`)
The current click listener fails because the button contains a span.
**Update the Event Listener:**
```javascript
// Checkout button fix
if (e.target.id === 'checkout-btn' || e.target.closest('#checkout-btn')) {
    handleCheckout();
}

Task 2: Sticky Footer Localization (templates/webapp/index.html)
The "View Cart" text is hardcoded and never updated.
HTML: Add ID to the span: <span>View Cart ➔</span> -> <span id="view-cart-label">View Cart ➔</span>.
JS (updateStickyFooter): Add this line inside the if (count > 0) block:
code
JavaScript
document.getElementById('view-cart-label').textContent = 
    `${translations.webapp_view_cart || 'View Cart'} ➔`;

    Task 3: Button Visibility (templates/webapp/index.html)
Replace custom bg-gold with standard Tailwind classes for guaranteed rendering.
Target: Both #checkout-btn and #sticky-cart (border).
Change: bg-gold -> bg-yellow-500 (for backgrounds), border-gold -> border-yellow-500, text-gold -> text-yellow-500.
Cart View Button: Add text-black to #checkout-btn to ensure contrast.
Definition of Done
Clicking ANY part of the "Checkout" button works.
The button is bright yellow.
The footer says "До кошика" (or German equivalent).