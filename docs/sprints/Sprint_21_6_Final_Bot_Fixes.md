# Sprint 21.6: Final Bot Onboarding and Store Fixes

Context: The onboarding flow is not saving data correctly, and the store handler returns errors for German users. We need to stabilize this before moving to WebApp.

Tasks for Code Agent:

Task 1: Refine Onboarding in bot/handlers/start.py
- When user starts onboarding:
- Step 1 (Language): Ensure the chosen language (uk/de) is saved to the User.language_pref field in DB IMMEDIATELY after selection.
- Step 2 (Name): Instead of asking for a name, show: "We see you as [Telegram Name]. Use this name for orders?"
- If user clicks "Yes", use their TG name. If "Change", let them type a new one.
- Step 3 (Agreement): Show a success message that data is saved and they can edit it in Profile.

Task 2: Fix Store Errors in bot/handlers/store.py
- The error "Error loading products" usually happens because of FSInputFile or missing data.
- Ensure that if product.name_de is empty, the code falls back to product.name (Ukrainian).
- Wrap the image sending logic in a tighter try-except. If image is missing, send text-only caption instead of failing.
- Ensure the async session is properly managed when iterating over products.

Task 3: Main Menu Update in bot/keyboards/main_menu.py
- Update the main menu to reflect our new hybrid plan.
- Buttons: [ 🥩 Open Catalog (WebApp Placeholder) ], [ 👤 Profile ], [ ℹ️ Impressum ].
- Note: For now, keep the "Open Catalog" as a regular button that triggers the current store logic, but mark it in code for future WebApp integration.

Definition of Done:
- New users can complete onboarding without frustration.
- Language preference is correctly saved in the database.
- Clicking a category shows products for both UK and DE users without "Error" popups.