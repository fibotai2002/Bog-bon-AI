from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.database.models import User

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    """
    /start buyrug'iga javob beradi va foydalanuvchini bazaga qo'shadi.
    """
    user = message.from_user
    
    # User borligini tekshirish
    result = await session.execute(select(User).where(User.id == user.id))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        # Yangi user qo'shish
        new_user = User(
            id=user.id,
            full_name=user.full_name,
            username=user.username
        )
        session.add(new_user)
        await session.commit()
        welcome_text = (
            f"Assalomu alaykum, {user.full_name}! 🌱\n\n"
            "Men **Bog'bon AI**man. O'simliklaringizdagi kasalliklarni aniqlashda yordam beraman.\n"
            "Menga kasallangan o'simlik rasmini yuboring."
        )
    else:
        # User mavjud
        welcome_text = f"Qaytganingizdan xursandman, {user.full_name}! 🌿\nRasmni yuboravering."
        
    await message.answer(welcome_text, parse_mode="Markdown")
