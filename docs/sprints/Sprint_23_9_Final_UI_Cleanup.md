# Sprint 23.9: Final WebApp UI Cleanup and Professional Polish

**Objective:** Fix double headers, eliminate broken template literals in HTML, and sync emojis with the database for a professional "Boutique" look.

## Task 1: View Hierarchy Fix (templates/webapp/index.html)
- Move the main `<header class="relative">...</header>` block (Hero image with "FARM CONNECT" title) INSIDE the `<div id="discovery-view">`.
- **Purpose**: This ensures that when the user enters a shop (Shop View), the main hero image completely disappears, making room for the Farm-specific info.

## Task 2: Fix Broken HTML Translations
- Remove all literal `${translations.webapp_...}` text from the HTML tags (specifically for the Back button and Categories header).
- **Implementation**:
  - Replace the Back button text with: `⬅️ <span id="ui-btn-back"></span>`.
  - Replace the Categories header text with: `<span id="ui-label-categories"></span>`.
- **JS Update**: In `loadTranslations()`, inject the correct text using:
  `document.getElementById('ui-btn-back').innerText = translations['webapp_back_to_farms'] || 'Back';`
  `document.getElementById('ui-label-categories').innerText = translations['webapp_farm_types'] || 'Categories';`

## Task 3: Clean Emojis from JavaScript
- Update the `generateFarmTypeButtons()` function.
- **Action**: Completely remove the `emoji` property and the `${farmType.emoji}` logic from the `innerHTML` string. 
- **Requirement**: Labels must come 100% from the database (e.g., "🥩 М'ясо"). Do not add icons in the code to avoid duplication.

## Task 4: Carousel and 'All' Button Polish
- Ensure the "All" category button in `loadCategories()` uses the `webapp_all_items` key correctly.
- Ensure the horizontal carousel displays category names clearly overlayed on images.

## Task 5: Code Hygiene
- Verify that no system tags (like </content>) are present in the final file.

## Definition of Done:
- Discovery View shows the Hero image; Shop View hides it.
- All UI text (Back, Categories, All) is correctly localized without showing raw code.
- No double emojis are present on the farm type buttons.