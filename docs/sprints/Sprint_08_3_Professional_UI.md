# Sprint 08.3: Professional Localization & Admin UI Cleanup
**Goal:** Replace primitive text fields with structured data and fix usability.

1. **User Model Cleanup:**
   - Replace `language_pref` text field with a Choice field (Enum: 'uk', 'de').
   - **CRITICAL:** Hide `password_hash` from the Admin list view and use a proper Password field in the edit form (hashing on save).

2. **Localization System:**
   - Create a `Translation` model: `key` (String, unique), `value_uk` (Text), `value_de` (Text).
   - This will store all UI strings (buttons, labels, bot messages).

3. **Multilingual CMS (Static Pages):**
   - Update `Page` model: Add `title_de`, `content_de`, `seo_title_uk/de`, `seo_description_uk/de`.

4. **Seeding:**
   - Populate the `Translation` table with initial UI strings for the bot and website.