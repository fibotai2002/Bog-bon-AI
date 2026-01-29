"""
Bot klaviaturalari
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
