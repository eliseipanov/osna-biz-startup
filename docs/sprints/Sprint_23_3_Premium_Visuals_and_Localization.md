# Sprint 23.3: WebApp Premium Visuals and Multi-language API

**Objective:** Fully localize the WebApp discovery screen, fix missing images, and add the Hero Header.

## Task 1: UI Translation API (admin/routes.py)
- Create an API endpoint `GET /api/ui/translations?lang=uk/de`.
- Logic: Fetch ALL keys from the `Translations` table and return them as a JSON dictionary: `{"key": "value"}`.
- This will allow the WebApp to display "Select Region", "Farm Types", etc., in the user's language.

## Task 2: Pass Language to WebApp
- In `bot/keyboards/main_menu.py`, update the WebApp URL to include the user's language:
  `url=f"{NGROK_URL}/webapp?lang={user_language}"`

## Task 3: Premium Header and Images (templates/webapp/index.html)
- **Hero Header:** Add a section at the top with the 21:9 image (`/static/uploads/hero.jpg`). 
- **Dynamic Text:** Replace all English labels with JavaScript variables that load from `/api/ui/translations`.
- **Farm Cards:** 
  - Add an `<img>` tag to each farm card. 
  - Source: `/static/uploads/{farm.image_path}`. 
  - If `image_path` is empty, show a stylish placeholder with the first letter of the Farm name.
- **Localization:** 
  - Use `farm.description_uk` or `farm.description_de` based on the URL parameter.
  - Use `region.name` or `region.name_de` for the regions list.

## Task 4: Fix Routes (admin/routes.py)
- Clean up the end of the file (remove system tags/comments left by previous AI sessions).
- Ensure all API responses return absolute paths for images.

## Definition of Done:
- WebApp opens in the language selected by the user in the bot.
- All titles (Select Region, Farm Types) are translated.
- Farm cards display their real photos from the database.
- The Hero image is displayed at the top.