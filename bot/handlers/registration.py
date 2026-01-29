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
    waiting_for_lang = State()
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
    """Registratsiyani boshlash"""
    await state.set_state(RegistrationStates.waiting_for_lang)
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbek (Lotin)"), KeyboardButton(text="🇺🇿 Ўзбек (Кирилл)")],
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇸 English")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык / 🇺🇸 Select language",
        reply_markup=keyboard
    )

@router.message(RegistrationStates.waiting_for_lang)
async def process_lang(message: types.Message, state: FSMContext):
    """Tilni qabul qilish"""
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
        await message.answer("Please select a language from the keyboard.")
        return
        
    # Tilni saqlash
    user_id = message.from_user.id
    set_user_lang(user_id, lang_code)
    
    await state.update_data(lang=lang_code)
    await state.set_state(RegistrationStates.waiting_for_name)
    
    await message.answer(
        get_text("ask_name", lang_code),
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
    """Viloyatni qabul qilish va tugatish"""
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
    prompt = get_text("photo_prompt", lang)
    
    await callback.message.edit_text(
        f"{msg}{info}\n\n{prompt}",
        parse_mode="HTML",
        # Hali get_start_keyboard lang ni qo'llab quvvatlamaydi, lekin argument bersak xato bermasligi uchun default kerak
        # Hozircha bo'sh qo'yib keyin yangilayman
    )
    
    # Alohida message bilan menyu (inline keyboard update qilish qiyin bo'lsa)
    # Bu yerda biz edit_text qilyapmiz. 
    # Keyingi stepda keyboards.py update bo'lgach ishlaydi.
    try:
        await callback.message.edit_reply_markup(reply_markup=get_start_keyboard(lang))
    except TypeError:
        # Agar get_start_keyboard hali argument qabul qilmasa (update bo'lmagan)
        await callback.message.edit_reply_markup(reply_markup=get_start_keyboard())
