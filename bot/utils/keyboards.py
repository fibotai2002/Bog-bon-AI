"""
Bot klaviaturalari
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot.utils.locales import get_text

def get_start_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """
    /start uchun inline keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("menu_leaf", lang), callback_data="target:leaf"),
            InlineKeyboardButton(text=get_text("menu_fruit", lang), callback_data="target:fruit"),
        ],
        [
            InlineKeyboardButton(text=get_text("menu_stem", lang), callback_data="target:stem"),
            InlineKeyboardButton(text=get_text("menu_insect", lang), callback_data="target:insect"),
        ],
        [
            InlineKeyboardButton(text=get_text("menu_help", lang), callback_data="help"),
            InlineKeyboardButton(text=get_text("menu_plans", lang), callback_data="plans"),
        ]
    ])
    return keyboard

def get_tutorial_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """
    Tutorial uchun inline keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_start_using", lang), callback_data="start_using"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_skip_tutorial", lang), callback_data="skip_tutorial"),
        ]
    ])
    return keyboard

def get_settings_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """
    Settings uchun inline keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text("btn_change_language", lang), callback_data="change_lang"),
        ],
        [
            InlineKeyboardButton(text=get_text("btn_back", lang), callback_data="back_to_start"),
        ]
    ])
    return keyboard

def get_language_keyboard() -> ReplyKeyboardMarkup:
    """
    Til tanlash uchun keyboard
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbek (Lotin)"), KeyboardButton(text="🇺🇿 Ўзбек (Кирилл)")],
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇸 English")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

