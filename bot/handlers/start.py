from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy import select

from core.database import async_session
from core.models import User, StaticPage
from bot.keyboards.main_menu import get_main_menu_keyboard

router = Router()

# FSM States for onboarding
class OnboardingStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_agreement = State()
    waiting_for_name = State()
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
                await message.answer("Вітаємо в Osnabrück Farm Connect! Оберіть розділ нижче 👇", reply_markup=get_main_menu_keyboard())
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

    if language == "uk":
        text = "👤 <b>Введіть ваше справжнє ім'я та прізвище:</b>\n\nНаприклад: Іван Петренко"
    else:
        text = "👤 <b>Geben Sie Ihren vollständigen Namen ein:</b>\n\nBeispiel: Ivan Petrenko"

    await callback.message.edit_text(text, parse_mode="HTML")
    await state.set_state(OnboardingStates.waiting_for_name)
    await callback.answer()

# Name input handler
@router.message(OnboardingStates.waiting_for_name)
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
        if language == "uk":
            welcome_text = "🎉 <b>Реєстрація завершена!</b>\n\nТепер ви можете переглядати каталог продуктів та робити замовлення."
        else:
            welcome_text = "🎉 <b>Registrierung abgeschlossen!</b>\n\nSie können jetzt den Produktkatalog durchsuchen und Bestellungen aufgeben."

        await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")

    except Exception as e:
        await message.answer("Сталася помилка при збереженні даних. Спробуйте ще раз.")

# Impressum handler
@router.message(F.text == "ℹ️ Impressum")
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