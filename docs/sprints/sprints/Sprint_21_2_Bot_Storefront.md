# Sprint 21.2: Premium Bot Storefront (Inline UI)

**Context:** We are replacing the old text catalog with a professional Inline interface where users can add items to their cart directly.

**Tasks:**
1. **Create `bot/handlers/store.py`**:
   - Register a new router and include it in `bot/main.py`.
   - Update `🥩 Каталог` handler: show Inline buttons for all **Categories** (Schwein, Rind, etc.).
   - Handle Category click: Show products in that category as "Cards".

2. **Product "Card" Logic**:
   - For each product in the category, send:
     - Image (if `image_path` exists in `static/uploads/`).
     - Caption: `<b>Name</b>\nDescription\nPrice: 10,00 €/unit`.
   - Inline Keyboard for each card: `[ - ] [ In Cart: X ] [ + ]`.

3. **Cart Logic (Database Integration)**:
   - When user clicks `+` or `-`:
     - Update `CartItem` table in DB for this `user_id` and `product_id`.
     - Use `callback_query.answer` to show a quick notification.
     - Update the message text/keyboard to show the new quantity without re-sending the photo.

4. **Deadline Check**:
   - Create a helper `is_order_allowed()` that checks if current time is before Friday 12:00.
   - If after deadline, buttons `+`/`-` should show a popup: "Orders for this Saturday are closed!".

5. **Navigation**:
   - Add a "Back to Categories" button under the product list.
   - Add a "🛒 Go to Cart" button that appears if the cart is not empty.

**Note:** For units like 'шт' or 'пакунок', increments should be 1.0. For 'кг', consider increments of 0.5 or 1.0 (for now, keep it 1.0 for simplicity).