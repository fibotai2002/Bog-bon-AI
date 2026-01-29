"""
Tarif boshqaruvi handler
"""

import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import (
    get_user_plan,
    set_user_plan,
    is_admin,
    PLAN_FREE,
    PLAN_PRO,
    PLAN_BUSINESS
)

logger = logging.getLogger(__name__)

# Router yaratish
router = Router()

@router.message(Command("plan"))
async def cmd_plan(message: Message):
    """
    Foydalanuvchi tarifini ko'rsatish
    """
    user_id = message.from_user.id
    current_plan = get_user_plan(user_id)
    
    plan_info = {
        PLAN_FREE: {
            "emoji": "🆓",
            "name": "FREE (Bepul)",
            "features": [
                "✅ TOP-1 taxmin",
                "✅ Asosiy tavsiyalar",
                "✅ Xavfsizlik eslatmasi",
                "❌ Batafsil tahlil",
                "❌ Kimyoviy yo'nalish",
                "❌ Agronom formati"
            ]
        },
        PLAN_PRO: {
            "emoji": "💎",
            "name": "PRO",
            "features": [
                "✅ TOP-3 taxmin",
                "✅ Batafsil tahlil",
                "✅ Vizual belgilar",
                "✅ Tekshiruv savollari",
                "✅ Zarar darajasi",
                "✅ Kimyoviy yo'nalish (sinflar)",
                "✅ Agrotexnika tavsiyalari",
                "❌ Agronom formati"
            ]
        },
        PLAN_BUSINESS: {
            "emoji": "🏢",
            "name": "BUSINESS (Agro AI)",
            "features": [
                "✅ PRO'dagi hammasi",
                "✅ Agronom uchun shablon",
                "✅ Admin kanaliga yuborish",
                "✅ Tarix va statistika",
                "✅ Prioritet qo'llab-quvvatlash"
            ]
        }
    }
    
    info = plan_info.get(current_plan, plan_info[PLAN_FREE])
    
    message_text = f"""{info['emoji']} <b>Sizning tarifingiz: {info['name']}</b>

<b>Imkoniyatlar:</b>
"""
    
    for feature in info["features"]:
        message_text += f"{feature}\n"
    
    message_text += "\n"
    
    # Upgrade taklifi
    if current_plan == PLAN_FREE:
        message_text += "💎 <b>PRO tarifga o'tish:</b>\n"
        message_text += "Ko'proq ma'lumot va professional tavsiyalar!\n"
        message_text += "Bog'laning: @your_sales\n"
    elif current_plan == PLAN_PRO:
        message_text += "🏢 <b>BUSINESS tarifga o'tish:</b>\n"
        message_text += "Agronom formati va maxsus xizmatlar!\n"
        message_text += "Bog'laning: @your_sales\n"
    
    await message.answer(message_text, parse_mode="HTML")
    
    logger.info(f"User {user_id} /plan ko'rdi: {current_plan}")

@router.message(Command("setplan"))
async def cmd_setplan(message: Message):
    """
    Tarif o'rnatish (faqat adminlar uchun)
    """
    user_id = message.from_user.id
    
    # Admin tekshiruvi
    if not is_admin(user_id):
        await message.answer("❌ Bu komanda faqat adminlar uchun!")
        return
    
    # Komanda formatini tekshirish
    # Format: /setplan <user_id> <plan>
    parts = message.text.split()
    
    if len(parts) != 3:
        await message.answer(
            "❌ Noto'g'ri format!\n\n"
            "<b>To'g'ri format:</b>\n"
            "<code>/setplan &lt;user_id&gt; &lt;plan&gt;</code>\n\n"
            "<b>Misollar:</b>\n"
            "<code>/setplan 123456789 PRO</code>\n"
            "<code>/setplan 987654321 BUSINESS</code>\n\n"
            "<b>Mavjud tariflar:</b>\n"
            "• FREE\n"
            "• PRO\n"
            "• BUSINESS",
            parse_mode="HTML"
        )
        return
    
    try:
        target_user_id = int(parts[1])
        new_plan = parts[2].upper()
        
        # Tarif nomini tekshirish
        if new_plan not in [PLAN_FREE, PLAN_PRO, PLAN_BUSINESS]:
            await message.answer(
                f"❌ Noto'g'ri tarif: {new_plan}\n\n"
                "Mavjud tariflar: FREE, PRO, BUSINESS"
            )
            return
        
        # Tarifni o'rnatish
        old_plan = get_user_plan(target_user_id)
        set_user_plan(target_user_id, new_plan)
        
        await message.answer(
            f"✅ Tarif o'zgartirildi!\n\n"
            f"👤 User ID: <code>{target_user_id}</code>\n"
            f"📊 Eski tarif: {old_plan}\n"
            f"📊 Yangi tarif: {new_plan}",
            parse_mode="HTML"
        )
        
        logger.info(f"Admin {user_id} user {target_user_id} tarifini o'zgartirdi: {old_plan} -> {new_plan}")
        
    except ValueError:
        await message.answer("❌ User ID raqam bo'lishi kerak!")
    except Exception as e:
        logger.error(f"Tarif o'rnatish xatosi: {e}")
        await message.answer(f"❌ Xato: {e}")

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """
    Statistika (faqat adminlar uchun)
    """
    user_id = message.from_user.id
    
    # Admin tekshiruvi
    if not is_admin(user_id):
        await message.answer("❌ Bu komanda faqat adminlar uchun!")
        return
    
    from bot.config import USER_DB
    
    # Statistika hisoblash
    total_users = len(USER_DB)
    
    plan_counts = {
        PLAN_FREE: 0,
        PLAN_PRO: 0,
        PLAN_BUSINESS: 0
    }
    
    for user_data in USER_DB.values():
        plan = user_data.get("plan", PLAN_FREE)
        plan_counts[plan] = plan_counts.get(plan, 0) + 1
    
    stats_text = f"""📊 <b>STATISTIKA</b>

👥 <b>Jami foydalanuvchilar:</b> {total_users}

<b>Tariflar bo'yicha:</b>
🆓 FREE: {plan_counts[PLAN_FREE]}
💎 PRO: {plan_counts[PLAN_PRO]}
🏢 BUSINESS: {plan_counts[PLAN_BUSINESS]}

<b>Konversiya:</b>
PRO: {plan_counts[PLAN_PRO] / total_users * 100 if total_users > 0 else 0:.1f}%
BUSINESS: {plan_counts[PLAN_BUSINESS] / total_users * 100 if total_users > 0 else 0:.1f}%
"""
    
    await message.answer(stats_text, parse_mode="HTML")
    
    logger.info(f"Admin {user_id} statistika ko'rdi")
