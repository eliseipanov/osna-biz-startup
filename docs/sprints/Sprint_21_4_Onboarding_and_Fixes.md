# Sprint 21.4: Onboarding Flow and Store Fixes

**Context:** The store buttons are failing, and we need a proper registration flow for legal compliance (GDPR/Germany).

**Tasks:**
1. **Fix `bot/handlers/store.py`**:
   - Replace `InputFile` with `FSInputFile` from `aiogram.types`.
   - Fix the `sqlalchemy.func.count()` logic (ensure it uses the current session properly).
   - Ensure image paths are absolute or correctly resolved relative to the project root.

2. **Implement Onboarding FSM in `bot/handlers/start.py`**:
   - When a NEW user sends `/start`:
     - **Step 1: Language.** Inline buttons (🇺🇦 Українська / 🇩🇪 Deutsch).
     - **Step 2: Legal.** Show a short text about the system + link to Impressum/Rules. Button "✅ Згоден з правилами".
     - **Step 3: Profile.** Ask for "Справжнє ім'я та прізвище" (text input).
     - **Step 4: Contact.** Request phone number via `KeyboardButton(request_contact=True)`.
   - Update `User` record in DB with this data.

3. **Impressum Handler**:
   - Add a command `/impressum` or a button in Profile that shows legal information from the `StaticPage` table.