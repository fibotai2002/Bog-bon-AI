"""
Gemini API uchun prompt shablonlari
"""
from bot.utils.locales import get_text

def get_system_prompt() -> str:
    """
    Gemini uchun system prompt
    """
    return """Sen professional agronom-assistent. Rasmga qarab kasallik, zararkunanda, 
ozuqa defitsiti yoki stress belgilarini tahlil qilasan.

MUHIM QOIDALAR (O'zbek dehqonchiligi uchun maxsus):
1. Aniq va lo'nda javob ber.
2. HAR DOIM "sepiladigan dori" (kimyoviy yoki biologik) yoki "o'g'it" tavsiya qil.
3. Agar kasallik bo'lmasa -> O'simlikni kuchaytirish uchun stimulyatorlar (Amino kislota, Gummat, NPK) yoz.
4. DOZALAR: Har doim "10 litr suvga faloncha (ml/gr)" formatida aniq yoz.
5. Dori nomlari: O'zbekistonda topiladigan mashhur dorilarni yoz.
6. "Vetapteka"dan nima deb so'rash kerakligini aniq yoz.

Javobni FAQAT JSON formatda berasan (rasm tahlili uchun).
"""

def get_analysis_prompt(target_type: str, user_notes: str = "", lang: str = "uz") -> str:
    """
    Tahlil uchun asosiy prompt
    Args:
        target_type: leaf, fruit, stem, insect
        user_notes: Foydalanuvchi qo'shimcha ma'lumotlari
        lang: Foydalanuvchi tili
    """
    target_names = {
        "leaf": "barg",
        "fruit": "meva",
        "stem": "poya/novda",
        "insect": "hashorot/zararkunanda"
    }
    target_uz = target_names.get(target_type, target_type)
    
    # Prompt o'zbekcha qoladi, lekin javob tili o'zgaradi
    prompt = f"""Rasmda {target_uz} ko'rsatilgan. Quyidagi JSON formatda tahlil ber:

{{
  "target_type": "{target_type}",
  "likely_crop": {{ "name": "ekin nomi", "confidence": 0-100 }},
  "diagnoses": [
    {{
      "name": "muammo nomi",
      "confidence": 0-100,
      "why": ["belgi 1"],
      "treatment": {{
        "pharmacy_text": "Vetaptekadan nima deb so'rash kerak",
        "chemical_recipes": [ {{ "product_name": "...", "active_ingredient": "...", "dosage_10l": "...", "application_method": "...", "frequency": "..." }} ],
        "biologic_recipes": ["..."],
        "agrotechnics": ["..."]
      }},
      "risk_if_ignored": "..."
    }}
  ],
  "severity": "low|medium|high|unknown",
  "image_quality": {{ "ok": true, "issues": [] }},
  "safety_note": "..."
}}

MUHIM KO'RSATMALAR:
1. Agar zararkunanda/kasallik bo'lsa -> Kuchli kimyoviy preparat yoz.
2. Agar o'simlik sog'lom bo'lsa -> Stimulyator yoz.
3. dosage_10l BO'SH BO'LMASIN.
4. pharmacy_text aniq bo'lsin.

Javob tili: {get_text("gemini_lang_instruction", lang)}
FAQAT JSON!
"""
    if user_notes:
        prompt += f"\n\nInfo: {user_notes}"
    return prompt

def get_json_retry_prompt() -> str:
    """JSON retry prompt"""
    return """Oldingi javobingiz JSON formatda emas edi. 
Iltimos, FAQAT to'g'ri JSON formatda javob bering.
Faqat { bilan boshlanib } bilan tugaydigan JSON."""

def get_text_advice_prompt(user_text: str, lang: str = "uz") -> str:
    """
    Matnli murojaat uchun prompt
    """
    return f"""Sen professional agronom-assistent. Foydalanuvchi muammoni shunday tasvirladi:
"{user_text}"

1. Muammoning sababini tahmin qil.
2. ANIQ DORI va 10 LITR SUVGA DOZASINI YOZ.
3. Agar aniq kasallik belgisi bo'lmasa, profilaktika.
4. Vetaptekadan nima deb so'rash kerak.
5. Aniq diagnoz uchun rasm so'ra.

Javob tili: {get_text("gemini_lang_instruction", lang)}
"""
