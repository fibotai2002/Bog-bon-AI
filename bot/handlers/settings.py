"""
Settings handler - til o'zgartirish va boshqa sozlamalar
"""

import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from bot.config import get_user_lang, set_user_lang
from bot.utils.locales import get_text
from bot.utils.keyboards import get_settings_keyboard, get_language_keyboard, get_start_keyboard

logger = logging.getLogger(__name__)

router = Router()

class SettingsStates(StatesGroup):
    waiting_for_language = State()

@router.message(Command("settings"))
async def cmd_settings(message: Message):
    """
    /settings komandasi
    """
    user_id = message.from_user.id
    user_lang = get_user_lang(user_id)
    
    settings_text = get_text("settings_menu", user_lang)
    
    await message.answer(
        settings_text,
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "change_lang")
async def change_language(callback: CallbackQuery, state: FSMContext):
    """
    Til o'zgartirish
    """
    user_lang = get_user_lang(callback.from_user.id)
    
    await state.set_state(SettingsStates.waiting_for_language)
    
    await callback.message.edit_text(
        get_text("choose_lang", user_lang),
        reply_markup=None
    )
    
    await callback.message.answer(
        "🌐 Tilni tanlang / Выберите язык / Select language:",
        reply_markup=get_language_keyboard()
    )
    
    await callback.answer()

@router.message(SettingsStates.waiting_for_language)
async def process_language_change(message: Message, state: FSMContext):
    """
    Yangi tilni qabul qilish
    """
    text = message.text
    lang_code = "uz"
    
    if "O'zbek (Lotin)" in text:
        lang_code = "uz"
    elif "Ўзбек (Кирилл)" in text:
        lang_code = "uz_cyrl"
    elif "Русский" in text:
        lang_code = "ru"
    elif "English" in text:
        lang_code = "en"
    else:
        await message.answer("⚠️ Iltimos, klaviaturadan tanlang.")
        return
    
    # Tilni saqlash
    user_id = message.from_user.id
    set_user_lang(user_id, lang_code)
    
    await state.clear()
    
    # Tasdiqlash xabari
    confirmation = get_text("language_changed", lang_code)
    
    await message.answer(
        confirmation,
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Bosh menyuga qaytish
    welcome_text = get_text("welcome_back", lang_code).format(name=message.from_user.first_name) + "\n\n"
    welcome_text += get_text("welcome_desc", lang_code) + "\n\n"
    welcome_text += get_text("photo_prompt", lang_code)
    
    await message.answer(
        welcome_text,
        reply_markup=get_start_keyboard(lang_code),
        parse_mode="HTML"
    )
    
    logger.info(f"User {user_id} changed language to {lang_code}")
