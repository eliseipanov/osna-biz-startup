from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton(text="🥩 Каталог"), KeyboardButton(text="🛒 Кошик")],
        [KeyboardButton(text="📋 Мої замовлення"), KeyboardButton(text="👤 Профіль")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, persistent=True)