from aiogram import Router, F, types
from aiogram.types import ContentType
from bot.services.gemini import analyze_image_with_gemini
import io

router = Router()

@router.message(F.photo)
async def handle_photo(message: types.Message, bot):
    """
    Rasm xabarlarini qabul qiladi va tahlil qiladi.
    """
    # Foydalanuvchiga kutib turishini aytish
    wait_msg = await message.reply("Rasm tahlil qilinmoqda... Iltimos kuting ⏳")
    
    try:
        # Rasmni yuklab olish
        photo = message.photo[-1] # Eng yuqori sifatlisi
        file_io = io.BytesIO()
        await bot.download(photo, destination=file_io)
        image_bytes = file_io.getvalue()
        
        # Caption dan o'simlik nomini olish (agar bo'lsa)
        plant_name = message.caption if message.caption else "Noma'lum"
        
        # Gemini orqali tahlil qilish
        result = await analyze_image_with_gemini(image_bytes, plant_name)
        
        if result.get("error"):
            await wait_msg.edit_text(result["message"])
            return

        # Natijani formatlash
        response_text = format_analysis_result(result)
        
        # Javobni yuborish
        await wait_msg.delete()
        await message.answer(response_text, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Handler Error: {e}")
        await wait_msg.edit_text("Xatolik yuz berdi. Iltimos keyinroq urinib ko'ring.")

def format_analysis_result(data: dict) -> str:
    """
    JSON natijani chiroyli o'qiladigan matnga aylantiradi.
    """
    status_icon = "🟢" if data.get("status") == "healthy" else "🔴"
    
    text = f"**Tahlil Natijasi:**\n\n"
    text += f"🌿 **O'simlik:** {data.get('plant', 'Noma\\'lum')}\n"
    text += f"{status_icon} **Holati:** {data.get('status', '').title()}\n"
    text += f"🦠 **Kasallik/Tashxis:** {data.get('disease', 'Aniqlanmadi')}\n"
    text += f"📊 **Aniqlik:** {data.get('confidence_percent', 0)}%\n\n"
    
    if data.get("symptoms"):
        text += "**Belgilar:**\n"
        for symptom in data["symptoms"]:
            text += f"- {symptom}\n"
        text += "\n"
        
    if data.get("treatment"):
        text += "**Davolash:**\n"
        for treat in data["treatment"]:
            text += f"💊 {treat}\n"
        text += "\n"
        
    if data.get("prevention"):
        text += "**Oldini olish:**\n"
        for prev in data["prevention"]:
            text += f"🛡 {prev}\n"
        text += "\n"
        
    if data.get("notes"):
        text += f"💡 **Qo'shimcha:** {data['notes']}"
        
    return text
