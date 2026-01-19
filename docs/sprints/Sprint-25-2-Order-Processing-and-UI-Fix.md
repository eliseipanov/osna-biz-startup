# Sprint 25.2: Order Processing Handler & Final UI Polish

**Objective:** Implement the Bot handler to receive and save WebApp orders to the database, fix UI overlap issues (padding), style the Checkout button, and apply full localization using a dedicated delta-seed script.

## Task 1: Bot Order Handler (`bot/handlers/order.py`)
Create a new file `bot/handlers/order.py` (and register it in `main.py`) to handle incoming WebApp data.

1.  **Trigger:** `F.web_app_data`.
2.  **Logic:**
    *   Parse `message.web_app_data.data` (JSON payload).
    *   **Database Action (Atomic):**
        *   Create new `Order` (user_id, status='NEW', total_price).
        *   Iterate items and create `OrderItem` records.
        *   **Crucial:** Use `async_session` and commit changes.
    *   **Response:** Send a message to the user using translation keys:
        `webapp_order_msg_header`
        `Order #ID`
        `Sum: X €`
        `webapp_order_msg_contact`

## Task 2: UI Spacing Fix (`templates/webapp/index.html`)
Fix the issue where the Sticky Footer covers the last product/buttons.

1.  **Add Padding:** Apply `padding-bottom: 8rem` (Tailwind `pb-32`) to the main container or the specific lists (`#products-list` and `#cart-view`).
2.  **Result:** User must be able to scroll past the last item so it sits clearly *above* the Sticky Footer.

## Task 3: Checkout Button Styling
Transform the "Checkout" text link into a proper button.
*   **Style:** `w-full bg-gold text-black font-bold py-4 rounded-lg text-lg uppercase tracking-wider hover:bg-yellow-500 shadow-lg`.

## Task 4: Safe Localization Update (Delta Script)
**CRITICAL:** DO NOT TOUCH `scripts/seed_db.py`.

1.  **Create Script:** `scripts/seed_translations_sprint25.py`.
2.  **Logic:** Check if key exists. If yes -> Update value. If no -> Insert.
3.  **Data:**
    *   `webapp_items_label`: "Товарів:" / "Artikel:"
    *   `webapp_view_cart`: "До кошика" / "Zum Warenkorb"
    *   `webapp_total_label`: "Всього:" / "Gesamt:"
    *   `webapp_checkout_btn`: "Оформити замовлення" / "Bestellen"
    *   `webapp_empty_title`: "Кошик порожній" / "Warenkorb leer"
    *   `webapp_empty_desc`: "Додайте смачненького!" / "Fügen Sie Produkte hinzu!"
    *   `webapp_order_msg_header`: "✅ Замовлення отримано!" / "✅ Bestellung erhalten!"
    *   `webapp_order_msg_contact`: "Менеджер зв'яжеться з вами." / "Ein Manager wird Sie kontaktieren."

## Task 5: JS Update
Update `index.html` to use these keys.
*   Sticky Footer format: `${translations.webapp_items_label} ${count} | ${total} €`
*   Checkout Button: `translations.webapp_checkout_btn`

## Definition of Done
*   Clicking "Checkout" creates a real `Order` in DB and triggers a Bot message.
*   UI has proper spacing (nothing hidden behind footer).
*   All new UI elements are localized via database keys using the specific values provided above.