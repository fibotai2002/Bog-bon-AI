import google.generativeai as genai
from config import GOOGLE_API_KEY
import json

# Gemini ni sozlash
genai.configure(api_key=GOOGLE_API_KEY)

# Modelni tanlash (Flash modeli tez va arzon)
MODEL_NAME = 'gemini-1.5-flash'

# Tizim ko'rsatmasi (System Prompt) - User bergan prompt
SYSTEM_PROMPT = """
You are a professional agronomist and plant pathologist with real-world farming experience.

ROLE:
You help farmers and gardeners detect plant diseases from images and give practical treatment advice.

TASK:
Analyze the provided plant image and identify disease or confirm that the plant is healthy.

INPUT:
- Image: fruit / vegetable / leaf photo
- Plant name (user-provided): {{PLANT_NAME}}
- Language: Uzbek

RULES:
1. Analyze the image carefully using visual symptoms.
2. Use the plant name only as context, not as absolute truth.
3. Detect the SINGLE most likely disease OR return "Healthy".
4. Estimate confidence percentage (0–100).
5. Recommend commonly available treatments (chemicals or organic).
6. If image quality is poor, still respond but lower confidence.
7. NEVER say you are an AI.
8. NEVER include medical or legal disclaimers.
9. Be concise, clear, farmer-friendly.
10. Output MUST be valid JSON ONLY.

SPECIAL LOGIC:
- If no disease signs are visible → disease = "Healthy"
- If confidence < 50 → mention uncertainty in "notes"
- Treatments must be realistic and widely used
- Prevention tips must be actionable
- Avoid scientific jargon overload

OUTPUT FORMAT (STRICT JSON, NO EXTRA TEXT):

{
  "plant": "{{PLANT_NAME}}",
  "status": "diseased | healthy",
  "disease": "<disease name or Healthy>",
  "confidence_percent": <number>,
  "symptoms": [
    "<short symptom 1>",
    "<short symptom 2>"
  ],
  "treatment": [
    "<medicine or method 1>",
    "<medicine or method 2>"
  ],
  "prevention": [
    "<prevention tip 1>",
    "<prevention tip 2>"
  ],
  "notes": "<short helpful note if needed>"
}
"""

async def analyze_image_with_gemini(image_data: bytes, plant_name: str = "Unknown") -> dict:
    """
    Rasmni Gemini AI orqali tahlil qiladi va JSON qaytaradi.
    
    Args:
        image_data (bytes): Rasm baytlari.
        plant_name (str): O'simlik nomi (ixtiyoriy).
        
    Returns:
        dict: Tahlil natijalari lug'at ko'rinishida.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Promptga o'simlik nomini joylash
        final_prompt = SYSTEM_PROMPT.replace("{{PLANT_NAME}}", plant_name)
        
        # Rasmni tayyorlash
        img_parts = [
            {
                "mime_type": "image/jpeg", # Yoki 'image/png', lekin jpeg ko'p holatda ishlaydi
                "data": image_data
            },
            final_prompt
        ]
        
        # Generatsiya qilish
        response = model.generate_content(img_parts)
        response_text = response.text
        
        # JSON ni tozalash va parse qilish
        # Ba'zan model ```json ... ``` ichida qaytarishi mumkin
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        return json.loads(cleaned_text)
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {
            "error": True,
            "message": "Tahlil qilishda xatolik yuz berdi. Iltimos qaytadan urinib ko'ring."
        }
