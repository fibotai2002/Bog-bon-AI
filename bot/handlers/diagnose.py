"""
Rasm tahlili handler (Lokalizatsiya bilan)
"""

import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, PhotoSize
from aiogram.fsm.context import FSMContext

from bot.handlers.start import DiagnosisStates
from bot.config import get_user_plan, PLAN_FREE, PLAN_PRO, PLAN_BUSINESS, ADMIN_CHANNEL_ID, get_user_lang
from bot.gemini_client import gemini_client
from bot.utils.images import download_telegram_photo, process_image, validate_image_quality
from bot.utils.templates import (
    format_free_response,
    format_pro_response,
    format_business_response,
    format_admin_channel_message,
    format_image_quality_error
)
from bot.utils.keyboards import get_start_keyboard
from bot.utils.locales import get_text

logger = logging.getLogger(__name__)

# Router yaratish
router = Router()

async def animate_processing(message: Message, lang: str = "uz"):
    """Tahlil jarayonini animatsiya qilish"""
    frames = ["⏳", "🔎", "🧪", "📝", "🤔"]
    idx = 0
    base_text = get_text("analyzing", lang)
    try:
        while True:
            await asyncio.sleep(1.5)
            try:
                await message.edit_text(f"{frames[idx % len(frames)]} {base_text}")
                idx += 1
            except Exception:
                pass
    except asyncio.CancelledError:
        pass

@router.message(DiagnosisStates.waiting_for_photo, F.text)
async def handle_diagnosis_text(message: Message, state: FSMContext):
    """Matnli murojaatni tahlil qilish"""
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    user_text = message.text
    
    # "O'ylayapman" xabari
    processing_msg = await message.answer(get_text("thinking", lang))
    
    # Gemini text request
    advice = await gemini_client.get_text_advice(user_text, lang=lang)
    
    if advice:
        await processing_msg.edit_text(advice, parse_mode="Markdown")
    else:
        await processing_msg.edit_text(get_text("text_advice_error", lang))

    # Rasm so'rash
    prompt = get_text("send_photo", lang)
    await message.answer(
        prompt,
        reply_markup=get_start_keyboard(lang)
    )

@router.message(DiagnosisStates.waiting_for_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext, bot: Bot):
    """
    Rasm qabul qilish va tahlil qilish
    """
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    
    # State'dan ma'lumotlarni olish
    data = await state.get_data()
    target_type = data.get("target_type", "leaf")
    
    logger.info(f"User {user_id} rasm yubordi: target_type={target_type}, lang={lang}")
    
    # Boshlang'ich xabar
    processing_msg = await message.answer(f"⏳ {get_text('analyzing', lang)}")
    
    # Animatsiyani ishga tushirish
    animation_task = asyncio.create_task(animate_processing(processing_msg, lang))
    
    try:
        # Eng katta rasmni olish
        photo: PhotoSize = message.photo[-1]
        
        # Rasmni yuklab olish
        image_bytes = await download_telegram_photo(bot, photo.file_id)
        if not image_bytes:
            animation_task.cancel()
            await processing_msg.edit_text(get_text("error_image_download", lang))
            return
        
        # Rasmni qayta ishlash
        processed = await process_image(image_bytes)
        if not processed:
            animation_task.cancel()
            await processing_msg.edit_text(get_text("error_processing", lang))
            return
        
        processed_bytes, metadata = processed
        
        # Rasm sifatini tekshirish (Warning only)
        # Hozircha "quality_issues" ni tarjima qilmaymiz (texnik info), lekin user message locales da bor
        
        # Gemini'ga yuborish
        analysis_result = await gemini_client.analyze_image(
            processed_bytes,
            target_type,
            user_notes="",
            lang=lang
        )
        
        # Animatsiyani to'xtatish
        animation_task.cancel()
        
        if not analysis_result:
            await processing_msg.edit_text(get_text("error_processing", lang))
            return
        
        # Foydalanuvchi tarifini olish
        user_plan = get_user_plan(user_id)
        
        # Tarifga qarab javob formatlash (LANG bilan)
        if user_plan == PLAN_FREE:
            response_text = format_free_response(analysis_result, lang)
        elif user_plan == PLAN_PRO:
            response_text = format_pro_response(analysis_result, lang)
        elif user_plan == PLAN_BUSINESS:
            response_text = format_business_response(analysis_result, user_id, target_type, lang)
        else:
            response_text = format_free_response(analysis_result, lang)
        
        # Javobni yuborish
        await processing_msg.edit_text(response_text, parse_mode="HTML")
        
        # BUSINESS tarif uchun admin kanaliga yuborish (bu o'zgarmasdan qoladi)
        if user_plan == PLAN_BUSINESS and ADMIN_CHANNEL_ID:
            try:
                admin_msg = format_admin_channel_message(analysis_result, user_id, target_type)
                await bot.send_photo(
                    chat_id=ADMIN_CHANNEL_ID,
                    photo=photo.file_id,
                    caption=admin_msg,
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Admin kanaliga yuborishda xato: {e}")
        
        # Yana rasm yuborish taklifi
        prompt = get_text("again_prompt", lang)
        await message.answer(
            prompt,
            reply_markup=get_start_keyboard(lang)
        )
        
        # State da qolamiz: waiting_for_photo
        await state.set_state(DiagnosisStates.waiting_for_photo)
        
    except Exception as e:
        animation_task.cancel()
        logger.error(f"Tahlil xatosi: {e}", exc_info=True)
        
        # Foydalanuvchiga oddiy xabar
        await processing_msg.edit_text(get_text("error_processing", lang))
        
        # Adminga to'liq hisobot yuborish
        try:
            from bot.config import ADMIN_IDS
            error_report = (
                f"🚨 <b>XATOLIK HISOBOTI</b>\n\n"
                f"👤 User: {user_id}\n"
                f"📝 Lang: {lang}\n"
                f"🎯 Target: {target_type}\n\n"
                f"❌ Error:\n<code>{str(e)[:3500]}</code>"
            )
            for admin_id in ADMIN_IDS:
                await bot.send_message(chat_id=admin_id, text=error_report, parse_mode="HTML")
        except Exception as admin_err:
            logger.error(f"Adminga xato yuborishda muammo: {admin_err}")

@router.message(DiagnosisStates.waiting_for_photo)
async def handle_unknown_content(message: Message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    await message.answer(
        get_text("send_photo", lang),
        reply_markup=get_start_keyboard(lang)
    )

@router.message(F.photo)
async def handle_photo_without_state(message: Message):
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    await message.answer(
        get_text("photo_prompt", lang), # "Qismni tanlang..."
        reply_markup=get_start_keyboard(lang),
        parse_mode="HTML"
    )
