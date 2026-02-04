import google.generativeai as genai
from config import GOOGLE_API_KEY
import json

# Gemini ni sozlash
genai.configure(api_key=GOOGLE_API_KEY)

# Modelni tanlash (Flash modeli tez va arzon)
MODEL_NAME = 'gemini-3-pro-preview'

import time
from config import GOOGLE_API_KEY, GOOGLE_API_KEY_2

# Tizim ko'rsatmasi (System Prompt) - o'zgarishsiz qoladi...
SYSTEM_PROMPT = """
You are a friendly and experienced gardener/agronomist (Bog'bon ota).

ROLE:
You analyze plant images and give VERY SPECIFIC, PRACTICAL advice to farmers in UZBEK.

TASK:
Identify the disease/pest and provide a structured recipe and instructions.

INPUT:
- Image: plant photo
- Plant name: {{PLANT_NAME}}

RULES:
1. Language: Uzbek (Latin).
2. Be precise. If it's a pest like "Oq qanot", say it.
3. Your output MUST be in the exact JSON format below.
4. "pharmacy_query": This is a sentence the farmer can say at the pharmacy. It must be in the first person ("Aka, pomidorimni...").
5. "recipe": specific drug names and dosages for 10L water.
6. "agrotechnical": physical/mechanical methods (yellow sticky traps, weeding, etc).
7. "warning": safety advice.

OUTPUT FORMAT (STRICT JSON):
{
  "plant": "{{PLANT_NAME}}",
  "disease_name": "<Disease Name> (<Russian/Common Name if exists>)",
  "confidence": <number 0-100>,
  "pharmacy_query": "<Text to say at pharmacy. Example: 'Aka, pomidorimni oq qanot bosib ketdi. Mospilan yoki Teppeki bering.'>",
  "recipe": [
    "<Drug Name>: <Dosage> (<Instruction>)",
    "<Drug Name 2>: <Dosage> (<Instruction>)"
  ],
  "agrotechnical": [
    "<Method 1>",
    "<Method 2>"
  ],
  "warning": "<Safety warning text>"
}
"""

async def analyze_image_with_gemini(image_data: bytes, plant_name: str = "Unknown") -> dict:
    """
    Rasmni Gemini AI orqali tahlil qiladi (Fallback bilan).
    """
    start_time = time.time()
    
    # 1-urinish: Asosiy kalit bilan
    try:
        print("Gemini: Asosiy API kalit ishlatilmoqda...")
        genai.configure(api_key=GOOGLE_API_KEY)
        result = await _generate(image_data, plant_name)
        result['duration'] = round(time.time() - start_time, 2)
        return result
    except Exception as e:
        print(f"Gemini Primary Error: {e}")
        import traceback
        traceback.print_exc() # Batafsil xatolikni chiqarish
        
        # 2-urinish: Zaxira kalit bilan (agar mavjud bo'lsa)
        if GOOGLE_API_KEY_2:
            try:
                print("Gemini: Zaxira API kalitga o'tilmoqda...")
                genai.configure(api_key=GOOGLE_API_KEY_2)
                result = await _generate(image_data, plant_name)
                result['duration'] = round(time.time() - start_time, 2)
                return result
            except Exception as e2:
                print(f"Gemini Secondary Error: {e2}")
        
        return {
            "error": True,
            "message": "Tahlil qilish imkoni bo'lmadi (API xatolik). Iltimos keyinroq urinib ko'ring."
        }

async def _generate(image_data: bytes, plant_name: str) -> dict:
    """Yordamchi funksiya: so'rovni yuborish va natijani parse qilish"""
    model = genai.GenerativeModel(MODEL_NAME)
    final_prompt = SYSTEM_PROMPT.replace("{{PLANT_NAME}}", plant_name)
    
    img_parts = [
        {"mime_type": "image/jpeg", "data": image_data},
        final_prompt
    ]
    
    response = model.generate_content(img_parts)
    cleaned_text = response.text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
        
    return json.loads(cleaned_text)
