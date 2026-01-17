from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy import select

from core.database import async_session
from core.models import User, StaticPage, Translation
from bot.keyboards.main_menu import get_main_menu_keyboard
from bot.utils import TranslationFilter, get_translation

router = Router()

# FSM States for onboarding
class OnboardingStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_agreement = State()
    waiting_for_name_confirmation = State()
    waiting_for_name_input = State()
    waiting_for_phone = State()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    full_name = message.from_user.full_name

    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            # If user exists and has completed onboarding (has phone), show main menu
            if user and user.phone:
                main_menu = await get_main_menu_keyboard(user.language_pref or "uk")
                welcome_text = await get_translation("welcome_message", user.language_pref or "uk")
                choose_hint = await get_translation("choose_section_hint", user.language_pref or "uk")
                await message.answer(f"{welcome_text} {choose_hint}", reply_markup=main_menu)
                return

            # Start onboarding flow for new users or incomplete profiles
            await state.update_data(tg_id=tg_id, full_name=full_name)

            # Language selection
            builder = InlineKeyboardBuilder()
            builder.button(text="🇺🇦 Українська", callback_data="lang_uk")
            builder.button(text="🇩🇪 Deutsch", callback_data="lang_de")

            await message.answer(
                "🌍 <b>Виберіть мову / Choose language:</b>\n\n"
                "🇺🇦 Українська\n"
                "🇩🇪 Deutsch",
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
            await state.set_state(OnboardingStates.waiting_for_language)

    except Exception as e:
        await message.answer("Сталася помилка при реєстрації. Спробуйте ще раз.")

# Language selection callback
@router.callback_query(OnboardingStates.waiting_for_language, F.data.startswith("lang_"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[1]  # "uk" or "de"
    await state.update_data(language_pref=language)

    # Save language preference immediately to database
    data = await state.get_data()
    try:
        async with async_session() as session:
            # Get or create user
            user = await session.scalar(select(User).where(User.tg_id == data["tg_id"]))

            if not user:
                user = User(
                    tg_id=data["tg_id"],
                    full_name=data["full_name"]
                )
                session.add(user)

            # Save language preference immediately
            user.language_pref = language
            await session.commit()
    except Exception as e:
        # Continue with onboarding even if DB save fails
        pass

    # Show legal agreement
    if language == "uk":
        text = (
            "📋 <b>Правила використання системи</b>\n\n"
            "Ласкаво просимо до Osnabrück Farm Connect!\n\n"
            "Ця система допомагає місцевим фермерам з Оснабрюка "
            "продавати свіжі продукти українській громаді.\n\n"
            "🔒 <b>Політика конфіденційності:</b>\n"
            "Ваші дані використовуються тільки для обробки замовлень.\n\n"
            "📞 <b>Контакти:</b>\n"
            "Для питань звертайтеся до адміністратора.\n\n"
            "Натисніть кнопку нижче, щоб погодитися з правилами."
        )
        agree_text = "✅ Згоден з правилами"
    else:
        text = (
            "📋 <b>Nutzungsbedingungen</b>\n\n"
            "Willkommen bei Osnabrück Farm Connect!\n\n"
            "Dieses System hilft lokalen Bauern aus Osnabrück, "
            "frische Produkte an die ukrainische Gemeinschaft zu verkaufen.\n\n"
            "🔒 <b>Datenschutz:</b>\n"
            "Ihre Daten werden nur zur Auftragsabwicklung verwendet.\n\n"
            "📞 <b>Kontakte:</b>\n"
            "Bei Fragen wenden Sie sich an den Administrator.\n\n"
            "Drücken Sie die Schaltfläche unten, um den Bedingungen zuzustimmen."
        )
        agree_text = "✅ Ich stimme den Bedingungen zu"

    builder = InlineKeyboardBuilder()
    builder.button(text=agree_text, callback_data="agree")

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await state.set_state(OnboardingStates.waiting_for_agreement)
    await callback.answer()

# Agreement callback
@router.callback_query(OnboardingStates.waiting_for_agreement, F.data == "agree")
async def process_agreement(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language_pref", "uk")
    telegram_name = data.get("full_name", "User")

    # Show success message and suggest Telegram name
    if language == "uk":
        text = (
            "✅ <b>Дякуємо за згоду!</b>\n\n"
            f"👤 Ми бачимо вас як: <b>{telegram_name}</b>\n\n"
            "Використовувати це ім'я для замовлень?"
        )
        yes_text = "✅ Так, використовувати це ім'я"
        change_text = "✏️ Змінити ім'я"
    else:
        text = (
            "✅ <b>Vielen Dank für Ihre Zustimmung!</b>\n\n"
            f"👤 Wir sehen Sie als: <b>{telegram_name}</b>\n\n"
            "Dieses Namen für Bestellungen verwenden?"
        )
        yes_text = "✅ Ja, diesen Namen verwenden"
        change_text = "✏️ Namen ändern"

    builder = InlineKeyboardBuilder()
    builder.button(text=yes_text, callback_data="name_yes")
    builder.button(text=change_text, callback_data="name_change")

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await state.set_state(OnboardingStates.waiting_for_name_confirmation)
    await callback.answer()

# Name confirmation handlers
@router.callback_query(OnboardingStates.waiting_for_name_confirmation, F.data == "name_yes")
async def process_name_yes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    telegram_name = data.get("full_name", "User")

    # Use Telegram name
    await state.update_data(real_name=telegram_name)
    await proceed_to_phone(callback.message, state)
    await callback.answer()

@router.callback_query(OnboardingStates.waiting_for_name_confirmation, F.data == "name_change")
async def process_name_change(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language = data.get("language_pref", "uk")

    if language == "uk":
        text = "👤 <b>Введіть ваше справжнє ім'я та прізвище:</b>\n\nНаприклад: Іван Петренко"
    else:
        text = "👤 <b>Geben Sie Ihren vollständigen Namen ein:</b>\n\nBeispiel: Ivan Petrenko"

    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(OnboardingStates.waiting_for_name_input)
    await callback.answer()

# Name input handler
@router.message(OnboardingStates.waiting_for_name_input)
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if len(name) < 2:
        data = await state.get_data()
        language = data.get("language_pref", "uk")

        if language == "uk":
            await message.answer("❌ Ім'я повинно містити принаймні 2 символи. Спробуйте ще раз:")
        else:
            await message.answer("❌ Der Name muss mindestens 2 Zeichen enthalten. Versuchen Sie es erneut:")
        return

    await state.update_data(real_name=name)
    await proceed_to_phone(message, state)

# Phone input handler (both contact and text)
@router.message(OnboardingStates.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await finalize_onboarding(message, state, phone)

@router.message(OnboardingStates.waiting_for_phone)
async def process_phone_text(message: Message, state: FSMContext):
    phone = message.text.strip()

    # Basic phone validation
    if not phone or len(phone) < 7:
        data = await state.get_data()
        language = data.get("language_pref", "uk")

        if language == "uk":
            await message.answer("❌ Будь ласка, введіть коректний номер телефону:")
        else:
            await message.answer("❌ Bitte geben Sie eine gültige Telefonnummer ein:")
        return

    await finalize_onboarding(message, state, phone)

async def proceed_to_phone(message: Message, state: FSMContext):
    # Request phone number
    data = await state.get_data()
    language = data.get("language_pref", "uk")

    if language == "uk":
        text = "📱 <b>Надішліть ваш номер телефону:</b>\n\nНатисніть кнопку нижче або введіть номер вручну."
        button_text = "📱 Надіслати номер телефону"
    else:
        text = "📱 <b>Senden Sie Ihre Telefonnummer:</b>\n\nDrücken Sie die Schaltfläche unten oder geben Sie die Nummer manuell ein."
        button_text = "📱 Telefonnummer senden"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_text, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(OnboardingStates.waiting_for_phone)

async def finalize_onboarding(message: Message, state: FSMContext, phone: str):
    data = await state.get_data()

    try:
        async with async_session() as session:
            # Get or create user
            user = await session.scalar(select(User).where(User.tg_id == data["tg_id"]))

            if not user:
                user = User(
                    tg_id=data["tg_id"],
                    full_name=data["full_name"]
                )
                session.add(user)

            # Update user data
            user.language_pref = data["language_pref"]
            user.full_name = data["real_name"]  # Override with real name
            user.phone = phone

            await session.commit()

        # Clear state
        await state.clear()

        # Show success message and main menu
        language = data.get("language_pref", "uk")
        main_menu = await get_main_menu_keyboard(language)
        welcome_text = await get_translation("welcome_message", language)

        if language == "uk":
            success_text = (
                "🎉 <b>Реєстрація завершена!</b>\n\n"
                "✅ Ваші дані збережено. Тепер ви можете переглядати каталог продуктів та робити замовлення.\n\n"
                "👤 Ви можете змінити свої дані в розділі <b>Профіль</b>."
            )
        else:
            success_text = (
                "🎉 <b>Registrierung abgeschlossen!</b>\n\n"
                "✅ Ihre Daten wurden gespeichert. Sie können jetzt den Produktkatalog durchsuchen und Bestellungen aufgeben.\n\n"
                "👤 Sie können Ihre Daten im Bereich <b>Profil</b> ändern."
            )

        await message.answer(success_text, reply_markup=main_menu, parse_mode="HTML")

    except Exception as e:
        await message.answer("Сталася помилка при збереженні даних. Спробуйте ще раз.")

# Impressum handler
@router.message(TranslationFilter("impressum_button"))
async def handle_impressum_message(message: Message):
    """Handle impressum button clicks in both languages."""
    await impressum_handler(message)

async def impressum_handler(message: Message):
    try:
        async with async_session() as session:
            # Get impressum from StaticPage table
            impressum_page = await session.scalar(
                select(StaticPage).where(StaticPage.slug == "impressum")
            )

            if impressum_page:
                # Get user language preference
                user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))
                language = user.language_pref if user else "uk"

                if language == "uk":
                    title = impressum_page.title_uk or impressum_page.title
                    content = impressum_page.content_uk or impressum_page.content
                else:
                    title = impressum_page.title_de or impressum_page.title
                    content = impressum_page.content_de or impressum_page.content

                text = f"<b>{title}</b>\n\n{content}"
            else:
                text = "ℹ️ <b>Impressum</b>\n\nІнформація про компанію буде додана найближчим часом."

            await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer("Сталася помилка при завантаженні інформації.")

# Profile handler
@router.message(TranslationFilter("profile_button"))
async def handle_profile_message(message: Message):
    """Handle profile button clicks in both languages."""
    await profile_handler(message)

async def profile_handler(message: Message, user_id: int = None):
    """Show user profile with balance, name, phone and language toggle."""
    try:
        async with async_session() as session:
            # Use provided user_id or fallback to message sender
            target_user_id = user_id or message.from_user.id
            user = await session.scalar(select(User).where(User.tg_id == target_user_id))

            if not user:
                await message.answer("Користувача не знайдено.")
                return

            # Get localized labels
            user_language = user.language_pref or "uk"

            name_label = await get_translation("name_label", user_language)
            phone_label = await get_translation("phone_label", user_language)
            balance_label = await get_translation("balance_label", user_language)
            change_lang_btn = await get_translation("change_lang_btn", user_language)

            # Format profile message
            profile_text = f"👤 <b>{await get_translation('profile_title', user_language)}</b>\n\n"
            profile_text += f"{name_label}: {user.full_name or 'Не вказано'}\n"
            profile_text += f"{phone_label}: {user.phone or 'Не вказано'}\n"
            profile_text += f"{balance_label}: {user.balance:.2f} €\n"

            # Create inline keyboard with language toggle
            builder = InlineKeyboardBuilder()
            builder.button(text=change_lang_btn, callback_data="toggle_language")

            await message.answer(
                profile_text,
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )

    except Exception as e:
        await message.answer("Сталася помилка при завантаженні профілю.")

# Language toggle callback
@router.callback_query(F.data == "toggle_language")
async def toggle_language(callback: CallbackQuery):
    """Toggle user's language preference between UK and DE."""
    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == callback.from_user.id))

            if not user:
                await callback.answer("Користувача не знайдено.")
                return

            # Toggle language
            new_language = "de" if user.language_pref.value == "uk" else "uk"
            user.language_pref = new_language

            await session.commit()

            # Get confirmation message in new language
            if new_language == "de":
                confirm_msg = "Sprache zu Deutsch gewechselt! 🇩🇪"
            else:
                confirm_msg = "Мову змінено на українську! 🇺🇦"

            await callback.answer(confirm_msg, show_alert=True)

            # Update the existing profile message with new language
            await profile_handler(callback.message, user_id=callback.from_user.id)

            # Send updated main menu in new language (single message, no duplicates)
            main_menu = await get_main_menu_keyboard(new_language)
            choose_hint = await get_translation("choose_section_hint", new_language)
            await callback.message.answer(choose_hint, reply_markup=main_menu)

    except Exception as e:
        await callback.answer("Помилка при зміні мови.")