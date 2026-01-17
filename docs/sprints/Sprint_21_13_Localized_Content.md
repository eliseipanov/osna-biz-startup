# Sprint 21.13: Use Localized Fields for Categories and Products

**Objective:** Ensure that content displays in German using the model's dedicated German fields when the user's language is set to 'de'.

**Tasks:**

1. **Category Localization (`bot/handlers/store.py`):**
   - In `show_categories` and `back_to_categories`, fetch the `User` to determine `language_pref`.
   - If `language_pref == 'de'`, display `category.name_de`.
   - Fallback to `category.name` only if `category.name_de` is null or empty.

2. **Product Localization (`bot/handlers/store.py`):**
   - In `show_category_products` and `update_product_message`, use the user's language preference.
   - Display `product.name_de` and `product.description_de` for German users.
   - Use `product.name` and `product.description` as a fallback.

3. **Data Integrity:**
   - Use the attributes directly from the `Category` and `Product` models in `core/models.py`. 
   - Do not add new keys to the `Translations` table for specific product names.

**Definition of Done:**
- Clicking 'Katalog' in German mode shows category names in German (e.g., Schwein).
- Product cards in German mode show German titles and descriptions.
