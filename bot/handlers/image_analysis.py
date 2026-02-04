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
    wait_msg = await message.reply("Rasm tahlil qilinmoqda... ⏳\nTahlil 1-3 minut vaqt olishi mumkin.")
    
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
    JSON natijani rasmga (skrinshot) mos formatda chiqaradi.
    """
    # 1. Taxmin va Ishonch
    disease = data.get('disease_name', 'Aniqlanmadi')
    confidence = data.get('confidence', 0)
    
    text = f"📌 **Taxmin:** {disease}\n"
    text += f"📊 **Ishonch:** {confidence}%\n\n"
    
    # 2. Vetaptekadan so'rang
    if data.get("pharmacy_query"):
        text += "🗣 _Vetaptekadan so'rang:_\n"
        text += f"_{data['pharmacy_query']}_\n\n"
        
    # 3. Retsept
    if data.get("recipe"):
        text += "🥛 **Retsept (10L suvga):**\n"
        for item in data["recipe"]:
            text += f"• {item}\n"
        text += "\n"
        
    # 4. Agrotexnik tavsiyalar
    if data.get("agrotechnical"):
        text += "⚡ **Agrotexnik tavsiyalar:**\n"
        for item in data["agrotechnical"]:
            text += f"• {item}\n"
        text += "\n"
        
    # 5. Eslatma
    if data.get("warning"):
        text += f"❗️ **Eslatma:** {data['warning']}\n\n"
        
    # 6. PRO tarif (statik matn)
    text += "💎 **PRO tarifda batafsil tahlil va ko'proq tavsiyalar!**"
        
    return text
