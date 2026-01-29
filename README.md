# 🌾 Agro AI Telegram Bot

Ekin kasalliklari va zararkunandalarini aniqlash uchun AI (Gemini) yordamchisi.

## Xususiyatlar

- 📸 **Rasm tahlili**: Barg, meva, poya yoki hashorot rasmini tahlil qiladi
- 🧠 **AI Diagnostika**: Google Gemini 1.5 Flash modeli yordamida aniq taxminlar
- 💎 **Tariflar tizimi**:
  - **FREE**: Asosiy tahlil va tavsiyalar
  - **PRO**: Batafsil tahlil, kimyoviy yo'nalishlar, vizual belgilar
  - **BUSINESS**: Agronomlar uchun maxsus format va admin integratsiyasi
- ⚡️ **Tezkor va Xavfsiz**: Rasmlar optimallashtiriladi, xavfsizlik qoidalariga rioya qilinadi

## O'rnatish

1.  **Repositoryni klonlash** (yoki fayllarni yuklab olish):
    ```bash
    git clone https://github.com/username/agro-ai-bot.git
    cd agro-ai-bot
    ```

2.  **Virtual muhit yaratish**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

3.  **Kutubxonalarni o'rnatish**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfiguratsiya**:
    - `.env` faylini tahrirlang (hozirda API kalitlar o'rnatilgan)
    - `ADMIN_IDS` ga o'z Telegram ID ingizni qo'shing (botda `/start` bosganda loglarda chiqadi yoki @userinfobot orqali olsangiz bo'ladi)

5.  **Botni ishga tushirish**:
    ```bash
    python3 -m bot.main
    ```

## Foydalanish

1.  Botga `/start` bosing
2.  Ekin qismini tanlang (Barg/Meva/Poya/Hashorot)
3.  Rasm yuboring
4.  Natijani oling!

Tarifni o'zgartirish (Admin uchun):
`/setplan <user_id> <plan>` (masalan: `/setplan 123456789 PRO`)
Statistika (Admin uchun):
`/stats`

## Texnologiyalar

- Python 3.10+
- aiogram 3.x
- Google Generative AI (Gemini)
- Pillow (Image Processing)

## Muallif
Agro AI Team
