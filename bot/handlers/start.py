from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    /start buyrug'i uchun handler.
    """
    user_name = message.from_user.first_name
    text = (
        f"Assalomu alaykum, {user_name}! 🌱\n\n"
        "Men **Agro AI** botman. Menga o'simlik, meva yoki sabzavot rasmini yuboring "
        "va men uning kasalligini aniqlab, davolash bo'yicha maslahat beraman.\n\n"
        "Boshlash uchun rasm yuboring! 📸"
    )
    await message.answer(text, parse_mode="Markdown")
