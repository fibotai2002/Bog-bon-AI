"""
Foydalanuvchi registratsiyasi (Lokalizatsiya bilan)
"""

import logging
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from bot.config import update_user_data, set_user_lang, get_user_lang
from bot.utils.locales import get_text
from bot.utils.keyboards import get_start_keyboard

logger = logging.getLogger(__name__)

router = Router()

class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_region = State()

REGIONS = [
    "Toshkent shahri", "Toshkent viloyati", "Andijon", "Buxoro", 
    "Farg'ona", "Jizzax", "Xorazm", "Namangan", "Navoiy", 
    "Qashqadaryo", "Qoraqalpog'iston", "Samarqand", "Sirdaryo", "Surxondaryo"
]

def get_region_keyboard():
    """Viloyatlar uchun inline klaviatura"""
    keyboard = []
    row = []
    for i, region in enumerate(REGIONS):
        row.append(InlineKeyboardButton(text=region, callback_data=f"reg:{region}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def start_registration(message: types.Message, state: FSMContext):
    """Registratsiyani boshlash - to'g'ridan-to'g'ri ism so'rash"""
    user_id = message.from_user.id
    
    # Default til: O'zbek (Lotin)
    set_user_lang(user_id, "uz")
    await state.update_data(lang="uz")
    
    await state.set_state(RegistrationStates.waiting_for_name)
    
    # Multilingual welcome
    welcome = "👋 Assalomu alaykum! / Здравствуйте! / Hello!\n\n"
    welcome += "🌾 <b>Agro AI Bot</b>ga xush kelibsiz!\n\n"
    welcome += get_text("ask_name", "uz")
    
    await message.answer(
        welcome,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )



@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    """Ismni qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    name = message.text.strip()
    if len(name) < 3:
        await message.answer("⚠️ " + get_text("ask_name", lang)) # Simple fallback
        return
    
    await state.update_data(name=name)
    await state.set_state(RegistrationStates.waiting_for_phone)
    
    # Telefon so'rash tugmasi
    btn_text = get_text("btn_phone", lang)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn_text, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        get_text("ask_phone", lang),
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.message(RegistrationStates.waiting_for_phone, F.contact)
@router.message(RegistrationStates.waiting_for_phone) # Text handler
async def process_phone(message: types.Message, state: FSMContext):
    """Telefon raqamni qabul qilish"""
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    phone = ""
    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text.strip()
        if not phone.startswith("+") and not phone.isdigit():
            await message.answer("⚠️ " + get_text("ask_phone", lang), parse_mode="HTML")
            return
            
    await state.update_data(phone=phone)
    await state.set_state(RegistrationStates.waiting_for_region)
    
    await message.answer(
        get_text("ask_region", lang),
        reply_markup=get_region_keyboard(), # Viloyatlar hozircha lokalizatsiya qilinmagan (Lotin)
        parse_mode="HTML"
    )

@router.callback_query(RegistrationStates.waiting_for_region, F.data.startswith("reg:"))
async def process_region(callback: types.CallbackQuery, state: FSMContext):
    """Viloyatni qabul qilish va tutorial ko'rsatish"""
    from bot.utils.keyboards import get_tutorial_keyboard
    
    region = callback.data.split(":")[1]
    
    # Ma'lumotlarni olish
    data = await state.get_data()
    lang = data.get("lang", "uz")
    
    data.update({
        "region": region,
        "is_registered": True
    })
    
    # Bazaga saqlash
    user_id = callback.from_user.id
    update_user_data(user_id, data)
    
    await state.clear()
    
    # Success message
    msg = get_text("register_success", lang) + "\n\n"
    info = get_text("register_info", lang).format(
        name=data["name"],
        phone=data["phone"],
        region=region
    )
    
    await callback.message.edit_text(
        f"{msg}{info}",
        parse_mode="HTML"
    )
    
    # Tutorial ko'rsatish
    tutorial_text = get_text("tutorial_title", lang) + "\n\n"
    tutorial_text += get_text("tutorial_step1", lang) + "\n\n"
    tutorial_text += get_text("tutorial_step2", lang) + "\n\n"
    tutorial_text += get_text("tutorial_step3", lang) + "\n\n"
    tutorial_text += get_text("tutorial_footer", lang)
    
    await callback.message.answer(
        tutorial_text,
        reply_markup=get_tutorial_keyboard(lang),
        parse_mode="HTML"
    )
    
    await callback.answer()
