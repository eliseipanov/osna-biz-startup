# Sprint 23.4: WebApp Localization and Dynamic UI

**Objective:** Ensure all labels and buttons in the WebApp are correctly translated using the UI API.

## Task 1: Update HTML IDs (templates/webapp/index.html)
- Add unique IDs to all translatable elements:
  - Header Title -> `id="ui-title"`
  - Select Region Header -> `id="ui-select-region"`
  - Farm Types Header -> `id="ui-farm-types"`
  - Available Farms Header -> `id="ui-available-farms"`
  - Buttons (Meat, Vegetables, Fish) -> `id="btn-meat"`, `id="btn-veg"`, `id="btn-fish"`

## Task 2: JavaScript Localization Logic
- Update the `loadTranslations()` function:
  - It must parse `lang` from `window.location.search`.
  - After fetching JSON from `/api/ui/translations`, it must update the `.innerText` of every element by its ID.
  - Example: `document.getElementById('ui-select-region').innerText = translations['webapp_select_region'];`

## Task 3: Farm Type Translation
- Ensure the three filter buttons use keys: `type_meat`, `type_vegetables`, `type_fish` from the database instead of English text.

## Task 4: Subtitle Localization
- Add a translation key `webapp_subtitle` (Premium Farm Products / Premium Farm-Produkte) to the DB and use it in the Hero section.

## Definition of Done:
- Opening WebApp with `?lang=de` results in a fully German interface (including Region and Farm Type titles).
- Opening with `?lang=uk` results in a fully Ukrainian interface.