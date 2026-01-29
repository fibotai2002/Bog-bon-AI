"""
Gemini API Client
Rasmlarni tahlil qilish uchun
"""

import logging
import os
import json
import asyncio
from typing import Optional, Dict, Any
import google.generativeai as genai
from bot.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TIMEOUT, GEMINI_MAX_RETRIES
from bot.prompts import get_analysis_prompt, get_json_retry_prompt, get_text_advice_prompt
# from bot.utils.images import encode_image_base64

# Logging sozlash
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY topilmadi!")
            raise ValueError("GEMINI_API_KEY sozlanmagan")
            
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        logger.info(f"Gemini Client ishga tushdi: model={GEMINI_MODEL}")

    async def analyze_image(self, image_bytes: bytes, target_type: str, user_notes: str = "", lang: str = "uz") -> Optional[Dict[str, Any]]:
        """
        Rasmni tahlil qilish
        
        Args:
            image_bytes: Rasm fayli baytlari
            target_type: Ekin qismi (leaf, fruit, stem, insect)
            user_notes: Foydalanuvchi izohlari
            lang: Foydalanuvchi tili
            
        Returns:
            JSON javob (dict) yoki None (xatolik bo'lsa)
        """
        try:
            # Rasmni tayyorlash
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_bytes
            }
            
            # Promptni olish (LANG bilan)
            prompt = get_analysis_prompt(target_type, user_notes, lang=lang)
            logger.info(f"Prompt tayyorlandi: target={target_type}, notes={bool(user_notes)}, lang={lang}")
            
            # So'rov yuborish
            response_text = await self._generate_content(prompt, image_part)
            
            if not response_text:
                return None
            
            # JSON parse qilish
            try:
                # Markdown tozalash (```json ... ```)
                clean_text = response_text.replace("```json", "").replace("```", "").strip()
                result = json.loads(clean_text)
                logger.info("JSON muvaffaqiyatli parse qilindi")
                return result
            except json.JSONDecodeError:
                logger.warning("JSON parse xatosi. Qayta urinib ko'ramiz (Self-correction).")
                # Retry prompt bilan qayta so'rash (rasmsiz, faqat context)
                # Lekin Gemini vision chat history contextni talab qiladi.
                # Hozircha oddiy retry qilamiz (generate_content o'zi retry qilmaydi agar format xato bo'lsa)
                # Kelajakda: chat session ishlatish mumkin.
                return None
                
        except Exception as e:
            logger.error(f"Gemini tahlil xatosi: {e}", exc_info=True)
            return None
    
    async def get_text_advice(self, user_text: str, lang: str = "uz") -> Optional[str]:
        """
        Matnli maslahat olish
        """
        try:
            prompt = get_text_advice_prompt(user_text, lang=lang)
            return await self._generate_content(prompt)
        except Exception as e:
            logger.error(f"Text advice xatosi: {e}")
            return None

    async def _generate_content(self, prompt: str, image_part: Optional[dict] = None) -> Optional[str]:
        """
        Gemini'dan javob olish (Retry bilan)
        """
        try:
            contents = [prompt]
            if image_part:
                contents.append(image_part)

            # Retry logikasi bilan
            for attempt in range(GEMINI_MAX_RETRIES + 1):
                try:
                    response = self.model.generate_content(
                        contents,
                        request_options={"timeout": GEMINI_TIMEOUT}
                    )
                    
                    if response and response.text:
                        return response.text.strip()
                    
                    logger.warning(f"Bo'sh javob (urinish {attempt + 1})")
                    
                except Exception as e:
                    logger.warning(f"Generate xatosi (urinish {attempt + 1}): {e}")
                    if attempt == GEMINI_MAX_RETRIES:
                        raise
            
            return None
            
        except Exception as e:
            logger.error(f"Gemini generate xatosi: {e}")
            return None

# Global client
gemini_client = GeminiClient()
