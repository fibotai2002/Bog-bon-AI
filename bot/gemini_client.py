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
from bot.config import GEMINI_API_KEYS, GEMINI_MODEL, GEMINI_TIMEOUT, GEMINI_MAX_RETRIES
from bot.prompts import get_analysis_prompt, get_json_retry_prompt, get_text_advice_prompt
# from bot.utils.images import encode_image_base64

# Logging sozlash
logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self):
        if not GEMINI_API_KEYS:
            logger.error("GEMINI_API_KEYS topilmadi!")
            raise ValueError("GEMINI_API_KEYS sozlanmagan")
            
        self.api_keys = GEMINI_API_KEYS
        self.current_key_index = 0
        self._configure_genai()
        
    def _configure_genai(self):
        """Hozirgi kalit bilan Gemini ni sozlash"""
        current_key = self.api_keys[self.current_key_index]
        genai.configure(api_key=current_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        # Kalitni xavfsiz log qilish (oxirgi 4 ta belgi)
        masked_key = f"...{current_key[-4:]}" if len(current_key) > 4 else "***"
        logger.info(f"Gemini Client sozladi. Key index: {self.current_key_index} ({masked_key}), Model: {GEMINI_MODEL}")

    def _rotate_key(self):
        """Keyingi kalitga o'tish"""
        if len(self.api_keys) <= 1:
            return False
            
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.warning(f"API Key almashtirilmoqda... Yangi index: {self.current_key_index}")
        self._configure_genai()
        return True

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
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse xatosi: {e}. Raw text: {response_text[:100]}...")
                # Retry logic or fallback could go here
                return None
                
        except Exception as e:
            logger.error(f"Gemini tahlil xatosi: {e}", exc_info=True)
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
        Gemini'dan javob olish (Retry va Key Rotation bilan)
        """
        try:
            contents = [prompt]
            if image_part:
                contents.append(image_part)

            # Max retries (API xatolari uchun)
            # Biz har bir urinishda muvaffaqiyatsiz bo'lsa kalitni almashtirib ko'rishimiz mumkin
            # Yoki faqat ma'lum xatolarda. 
            # Oddiylik uchun: har qanday Exception da keyingi kalitni sinab ko'ramiz
            
            # Umumiy urinishlar soni: (Keys count) * (Retries per key)
            # Lekin juda ko'p kutmaslik uchun cheklaymiz
            max_total_attempts = len(self.api_keys) * (GEMINI_MAX_RETRIES + 1)
            # Yoki shunchaki 3-4 marta urinib ko'ramiz
            
            for attempt in range(max_total_attempts):
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
                    
                    # Agar bu oxirgi urinish bo'lmasa, kalitni almashtirib ko'ramiz
                    if attempt < max_total_attempts - 1:
                        rotated = self._rotate_key()
                        if rotated:
                            await asyncio.sleep(1) # Kichik pauza
                        else:
                            # Agar boshqa kalit bo'lmasa va retries tugagan bo'lsa
                            if attempt >= GEMINI_MAX_RETRIES:
                                logger.error("Barcha urinishlar va kalitlar tugadi.")
                                return None
                                
            return None
            
        except Exception as e:
            logger.error(f"Gemini generate fatal xatosi: {e}")
            return None

# Global client
gemini_client = GeminiClient()
