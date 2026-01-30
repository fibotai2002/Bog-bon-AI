"""
/start komandasi va inline tugmalar handler
"""

import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import is_user_registered, get_user_lang
from bot.utils.keyboards import get_start_keyboard
from bot.handlers.registration import start_registration
from bot.utils.locales import get_text

logger = logging.getLogger(__name__)

# Router yaratish
router = Router()

# FSM States
class DiagnosisStates(StatesGroup):
    """Tahlil uchun state'lar"""
    waiting_for_photo = State()  # Rasm kutilmoqda
    waiting_for_notes = State()  # Qo'shimcha ma'lumot kutilmoqda (optional)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    /start komandasi
    """
    user_id = message.from_user.id
    
    # Registratsiya tekshiruvi
    if not is_user_registered(user_id):
        await start_registration(message, state)
        return

    # State'ni tozalash
    await state.clear()
    
    user_lang = get_user_lang(user_id)
    user_name = message.from_user.first_name or "Foydalanuvchi"
    
    welcome_text = get_text("welcome_back", user_lang).format(name=user_name) + "\n\n"
    welcome_text += get_text("welcome_desc", user_lang) + "\n\n"
    welcome_text += get_text("photo_prompt", user_lang)

    await message.answer(
        welcome_text,
        reply_markup=get_start_keyboard(user_lang),
        parse_mode="HTML"
    )
    
    logger.info(f"User {message.from_user.id} /start bosdi (lang={user_lang})")

@router.callback_query(F.data.startswith("target:"))
async def target_selected(callback: CallbackQuery, state: FSMContext):
    """
    Ekin qismi tanlanganda
    """
    target_type = callback.data.split(":")[1]
    
    # State'ga saqlash
    await state.update_data(target_type=target_type)
    await state.set_state(DiagnosisStates.waiting_for_photo)
    
    target_names = {
        "leaf": "🍃 Barg",
        "fruit": "🍎 Meva",
        "stem": "🌿 Poya",
        "insect": "🐛 Hashorot"
    }
    
    target_name = target_names.get(target_type, target_type)
    
    response_text = f"""✅ Tanlandi: <b>{target_name}</b>

📸 Endi rasm yuboring!

<b>Yaxshi rasm uchun tavsiyalar:</b>
• Yaxshi yoritilgan joyda oling
• Yaqindan va aniq
• Kasallik/zarar ko'rinib tursin
• Agar barg bo'lsa, orqa tomonini ham ko'rsating

Rasmni yuborganingizdan so'ng tahlil boshlanadi..."""
    
    await callback.message.edit_text(
        response_text,
        parse_mode="HTML"
    )
    
    await callback.answer()
    
    logger.info(f"User {callback.from_user.id} {target_type} tanladi")

@router.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    """
    Yordam xabari
    """
    help_text = """ℹ️ <b>YORDAM</b>

<b>Bot qanday ishlaydi?</b>

1️⃣ Ekin qismini tanlang (barg, meva, poya, hashorot)
2️⃣ Zararlangan joyning rasmini yuboring
3️⃣ AI tahlil qiladi va natija beradi

<b>Tariflar:</b>

🆓 <b>FREE</b> - Asosiy tahlil
💎 <b>PRO</b> - Batafsil tahlil + tavsiyalar
🏢 <b>BUSINESS</b> - PRO + agronom formati

<b>Komandalar:</b>
/start - Boshidan boshlash
/plan - Sizning tarifingiz
/help - Yordam

<b>Savol-javob:</b>
Texnik yordam: @your_support"""
    
    await callback.message.edit_text(
        help_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_start")]
        ]),
        parse_mode="HTML"
    )
    
    await callback.answer()

@router.callback_query(F.data == "plans")
async def show_plans(callback: CallbackQuery):
    """
    Tariflar haqida ma'lumot
    """
    plans_text = """💎 <b>TARIFLAR</b>

🆓 <b>FREE (Bepul)</b>
• TOP-1 taxmin
• Asosiy tavsiyalar
• Xavfsizlik eslatmasi

💎 <b>PRO</b>
• TOP-3 taxmin
• Batafsil tahlil
• Vizual belgilar
• Tekshiruv savollari
• Zarar darajasi
• Kimyoviy yo'nalish (sinflar)
• Agrotexnika tavsiyalari

🏢 <b>BUSINESS (Agro AI servis)</b>
• PRO'dagi hammasi
• Agronom uchun shablon
• Admin kanaliga yuborish
• Tarix va statistika

<b>Tarifni o'zgartirish:</b>
Bog'laning: @your_sales"""
    
    await callback.message.edit_text(
        plans_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_start")]
        ]),
        parse_mode="HTML"
    )
    
    await callback.answer()

@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    """
    Bosh menyuga qaytish
    """
    await state.clear()
    
    user_id = callback.from_user.id
    user_lang = get_user_lang(user_id)
    
    welcome_text = get_text("welcome_back", user_lang).format(name=callback.from_user.first_name) + "\n\n"
    welcome_text += get_text("welcome_desc", user_lang) + "\n\n"
    welcome_text += get_text("photo_prompt", user_lang)
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_start_keyboard(user_lang),
        parse_mode="HTML"
    )
    
    await callback.answer()

@router.callback_query(F.data.in_(["start_using", "skip_tutorial"]))
async def handle_tutorial_buttons(callback: CallbackQuery):
    """
    Tutorial tugmalarini qayta ishlash
    """
    user_id = callback.from_user.id
    user_lang = get_user_lang(user_id)
    
    welcome_text = get_text("welcome_back", user_lang).format(name=callback.from_user.first_name) + "\n\n"
    welcome_text += get_text("welcome_desc", user_lang) + "\n\n"
    welcome_text += get_text("photo_prompt", user_lang)
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_start_keyboard(user_lang),
        parse_mode="HTML"
    )
    
    await callback.answer()

@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    /help komandasi
    """
    help_text = """ℹ️ <b>YORDAM</b>

<b>Bot qanday ishlaydi?</b>

1️⃣ Ekin qismini tanlang (barg, meva, poya, hashorot)
2️⃣ Zararlangan joyning rasmini yuboring
3️⃣ AI tahlil qiladi va natija beradi

<b>Komandalar:</b>
/start - Boshidan boshlash
/plan - Sizning tarifingiz
/help - Yordam"""
    
    await message.answer(help_text, parse_mode="HTML")
