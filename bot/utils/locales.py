"""
Bot uchun lokalizatsiya matnlari (Uz, Uz-Cyrl, Ru, En)
"""

TEXTS = {
    "uz": {
        "lang_name": "O'zbek (Lotin)",
        "gemini_lang_instruction": "Javob O'zbek tilida (Lotin alifbosida) bo'lsin.",
        
        "choose_lang": "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык / 🇺🇸 Select language",
        "welcome_register": "👋 Assalomu alaykum! Botdan foydalanish uchun ro'yxatdan o'ting.",
        "ask_name": "✍️ <b>Ismingizni kiriting:</b>",
        "ask_phone": "📞 <b>Telefon raqamingizni yuboring:</b>\nPastdagi tugmani bosing 👇",
        "btn_phone": "📱 Kontaktni yuborish",
        "ask_region": "📍 <b>Qaysi viloyatdansiz?</b>",
        "register_success": "✅ <b>Tabriklaymiz! Siz ro'yxatdan o'tdingiz.</b>",
        "register_info": "👤 Ism: {name}\n📞 Tel: {phone}\n📍 Hudud: {region}",
        "photo_prompt": "Endi ekin qismini tanlang va tahlilni boshlang! 👇",
        
        "menu_leaf": "🍃 Barg",
        "menu_fruit": "🍎 Meva",
        "menu_stem": "🌿 Poya",
        "menu_insect": "🐛 Hashorot",
        "menu_help": "ℹ️ Yordam",
        "menu_plans": "💎 Tariflar",
        
        "btn_back": "🔙 Ortga",
        "btn_menu": "🏠 Menyu",
        
        "thinking": "🤔 Agronom o'ylamoqda...",
        "analyzing": "Tahlil qilinmoqda...",
        "send_photo": "📸 Aniqroq tahlil uchun rasm yuboring.",
        "text_advice_error": "Uzr, tushunmadim. Iltimos, rasm yuboring.",
        "error_image_download": "❌ Rasm yuklab olinmadi. Qayta urinib ko'ring.",
        "error_processing": "❌ Xatolik yuz berdi. Qayta urinib ko'ring.",
        
        "analysis_header": "📌 <b>Taxmin:</b>",
        "confidence": "📊 <b>Ishonch:</b>",
        "pharmacy_title": "🗣 <b>Vetaptekadan so'rang:</b>",
        "recipe_title": "🧴 <b>Retsept (10L suvga):</b>",
        "agrotechnics": "⚡️ <b>Agrotexnik tavsiyalar:</b>",
        "safety": "❗️ <b>Eslatma:</b>",
        "pro_promo": "💎 <b>PRO tarifda batafsil tahlil!</b>",
        "top_diagnosis": "🧠 <b>TOP TAXMINLAR:</b>",
        "visual_signs": "Belgilar",
        "biologic": "🌿 <b>Biologik usullar:</b>",
        "severity": "📊 Zarar darajasi",
        "admin_copy": "📋 <b>AGRONOM UCHUN (COPY-PASTE):</b>",
        "welcome_back": "👋 Assalomu alaykum, <b>{name}</b>!\n\n🌾 <b>Agro AI Bot</b>ga xush kelibsiz!",
        "welcome_desc": "Ekinlaringizni tahlil qilish uchun rasm yuboring:",
        "again_prompt": "📸 Yana rasm yuboring yoki bo'lim tanlang:",
        
        "startup_notification": "🔄 <b>Bot qayta ishga tushdi</b>\n\n⚠️ Texnik ishlar tufayli bot bir muddat to'xtab turgan. Noqulaylik uchun uzr so'raymiz!\n\n👨‍💻 Dasturchi: @fibotai\n\n✅ Bot endi to'liq ishlayapti. Davom eting!",
        
        "tutorial_title": "📚 <b>Botdan qanday foydalanish?</b>",
        "tutorial_step1": "1️⃣ <b>Ekin qismini tanlang</b>\n🍃 Barg, 🍎 Meva, 🌿 Poya yoki 🐛 Hashorot",
        "tutorial_step2": "2️⃣ <b>Yaxshi rasm oling</b>\n• Yaxshi yoritilgan joyda\n• Yaqindan va aniq\n• Kasallik/zarar ko'rinib tursin",
        "tutorial_step3": "3️⃣ <b>Tahlilni oling</b>\nAI bir necha soniyada tahlil qiladi va tavsiyalar beradi",
        "tutorial_footer": "✅ Tayyor! Endi botdan foydalanishingiz mumkin.",
        "btn_start_using": "🚀 Ishlatishni boshlash",
        "btn_skip_tutorial": "⏭ O'tkazib yuborish",
        
        "settings_menu": "⚙️ <b>Sozlamalar</b>",
        "btn_change_language": "🌐 Tilni o'zgartirish",
        "language_changed": "✅ Til muvaffaqiyatli o'zgartirildi!"
    },

    "uz_cyrl": {
        "lang_name": "Ўзбек (Кирилл)",
        "gemini_lang_instruction": "Жавоб Ўзбек тилида (Кирилл алифбосида) бўлсин.",
        
        "choose_lang": "Тилни танланг",
        "welcome_register": "👋 Ассалому алайкум! Ботдан фойдаланиш учун рўйхатдан ўтинг.",
        "ask_name": "✍️ <b>Исмингизни киритинг:</b>",
        "ask_phone": "📞 <b>Телефон рақамингизни юборинг:</b>\nПастдаги тугмани босинг 👇",
        "btn_phone": "📱 Контактни юбориш",
        "ask_region": "📍 <b>Қайси вилоятдансиз?</b>",
        "register_success": "✅ <b>Табриклаймиз! Сиз рўйхатдан ўтдингиз.</b>",
        "register_info": "👤 Исм: {name}\n📞 Тел: {phone}\n📍 Ҳудуд: {region}",
        "photo_prompt": "Энди экин қисмини танланг ва таҳлилни бошланг! 👇",
        
        "menu_leaf": "🍃 Барг",
        "menu_fruit": "🍎 Мева",
        "menu_stem": "🌿 Поя",
        "menu_insect": "🐛 Ҳашорот",
        "menu_help": "ℹ️ Ёрдам",
        "menu_plans": "💎 Тарифлар",
         
        "btn_back": "🔙 Ортга",
        "btn_menu": "🏠 Меню",
        
        "thinking": "🤔 Агроном ўйламоқда...",
        "analyzing": "Таҳлил қилинмоқда...",
        "send_photo": "📸 Аниқроқ таҳлил учун расм юборинг.",
        "text_advice_error": "Узр, тушунмадим. Илтимос, расм юборинг.",
        "error_image_download": "❌ Расм юклаб олинмади.",
        "error_processing": "❌ Хатолик юз берди.",

        "analysis_header": "📌 <b>Тахмин:</b>",
        "confidence": "📊 <b>Ишонч:</b>",
        "pharmacy_title": "🗣 <b>Ветаптекадан сўранг:</b>",
        "recipe_title": "🧴 <b>Рецепт (10Л сувга):</b>",
        "agrotechnics": "⚡️ <b>Агротехник тавсиялар:</b>",
        "safety": "❗️ <b>Эслатма:</b>",
        "pro_promo": "💎 <b>PRO тарифда батафсил таҳлил!</b>",
        "top_diagnosis": "🧠 <b>ТОП ТАХМИНЛАР:</b>",
        "visual_signs": "Белгилар",
        "biologic": "🌿 <b>Биологик усуллар:</b>",
        "severity": "📊 Зарар даражаси",
        "admin_copy": "📋 <b>АГРОНОМ УЧУН (COPY-PASTE):</b>",
        "welcome_back": "👋 Ассалому алайкум, <b>{name}</b>!\n\n🌾 <b>Agro AI Bot</b>га хуш келибсиз!",
        "welcome_desc": "Экинларингизни таҳлил қилиш учун расм юборинг:",
        "again_prompt": "📸 Яна расм юборинг ёки бўлим танланг:",
        
        "startup_notification": "🔄 <b>Бот қайта ишга тушди</b>\n\n⚠️ Техник ишлар туфайли бот бир муддат тўхтаб турган. Ноқулайлик учун узр сўраймиз!\n\n👨‍💻 Дастурчи: @fibotai\n\n✅ Бот энди тўлиқ ишлаяпти. Давом етинг!",
        
        "tutorial_title": "📚 <b>Ботдан қандай фойдаланиш?</b>",
        "tutorial_step1": "1️⃣ <b>Экин қисмини танланг</b>\n🍃 Барг, 🍎 Мева, 🌿 Поя ёки 🐛 Ҳашорот",
        "tutorial_step2": "2️⃣ <b>Яхши расм олинг</b>\n• Яхши ёритилган жойда\n• Яқиндан ва аниқ\n• Касаллик/зарар кўриниб турсин",
        "tutorial_step3": "3️⃣ <b>Таҳлилни олинг</b>\nAI бир неча сонияда таҳлил қилади ва тавсиялар беради",
        "tutorial_footer": "✅ Тайёр! Энди ботдан фойдаланишингиз мумкин.",
        "btn_start_using": "🚀 Ишлатишни бошлаш",
        "btn_skip_tutorial": "⏭ Ўтказиб юбориш",
        
        "settings_menu": "⚙️ <b>Созламалар</b>",
        "btn_change_language": "🌐 Тилни ўзгартириш",
        "language_changed": "✅ Тил муваффақиятли ўзгартирилди!"
    },

    "ru": {
        "lang_name": "Русский",
        "gemini_lang_instruction": "Ответ на Русском языке.",
        
        "choose_lang": "Выберите язык",
        "welcome_register": "👋 Здравствуйте! Пожалуйста, зарегистрируйтесь для использования бота.",
        "ask_name": "✍️ <b>Введите ваше имя:</b>",
        "ask_phone": "📞 <b>Отправьте ваш номер телефона:</b>\nНажмите кнопку ниже 👇",
        "btn_phone": "📱 Отправить контакт",
        "ask_region": "📍 <b>Из какого вы региона?</b>",
        "register_success": "✅ <b>Поздравляем! Вы зарегистрированы.</b>",
        "register_info": "👤 Имя: {name}\n📞 Тел: {phone}\n📍 Регион: {region}",
        "photo_prompt": "Теперь выберите часть растения и начните анализ! 👇",
        
        "menu_leaf": "🍃 Лист",
        "menu_fruit": "🍎 Плод",
        "menu_stem": "🌿 Стебель",
        "menu_insect": "🐛 Насекомое",
        "menu_help": "ℹ️ Помощь",
        "menu_plans": "💎 Тарифы",
        
        "btn_back": "🔙 Назад",
        "btn_menu": "🏠 Меню",
        
        "thinking": "🤔 Агроном думает...",
        "analyzing": "Идет анализ...",
        "send_photo": "📸 Отправьте фото для точного анализа.",
        "text_advice_error": "Извините, не понял. Пожалуйста, отправьте фото.",
        "error_image_download": "❌ Не удалось скачать фото.",
        "error_processing": "❌ Произошла ошибка.",

        "analysis_header": "📌 <b>Прогноз:</b>",
        "confidence": "📊 <b>Уверенность:</b>",
        "pharmacy_title": "🗣 <b>Спросите в агроаптеке:</b>",
        "recipe_title": "🧴 <b>Рецепт (на 10л воды):</b>",
        "agrotechnics": "⚡️ <b>Агротехника:</b>",
        "safety": "❗️ <b>Примечание:</b>",
        "pro_promo": "💎 <b>Подробный анализ в тарифе PRO!</b>",
        "top_diagnosis": "🧠 <b>ТОП ПРОГНОЗЫ:</b>",
        "visual_signs": "Признаки",
        "biologic": "🌿 <b>Биологические методы:</b>",
        "severity": "📊 Степень поражения",
        "admin_copy": "📋 <b>ДЛЯ АГРОНОМА (COPY-PASTE):</b>",
        "welcome_back": "👋 Здравствуйте, <b>{name}</b>!\n\n🌾 Добро пожаловать в <b>Agro AI Bot</b>!",
        "welcome_desc": "Отправьте фото для анализа:",
        "again_prompt": "📸 Отправьте еще фото или выберите раздел:",
        
        "startup_notification": "🔄 <b>Бот перезапущен</b>\n\n⚠️ Из-за технических работ бот был временно недоступен. Приносим извинения за неудобства!\n\n👨‍💻 Разработчик: @fibotai\n\n✅ Бот теперь полностью работает. Продолжайте!",
        
        "tutorial_title": "📚 <b>Как пользоваться ботом?</b>",
        "tutorial_step1": "1️⃣ <b>Выберите часть растения</b>\n🍃 Лист, 🍎 Плод, 🌿 Стебель или 🐛 Насекомое",
        "tutorial_step2": "2️⃣ <b>Сделайте хорошее фото</b>\n• В хорошо освещенном месте\n• Крупным планом и четко\n• Чтобы было видно болезнь/повреждение",
        "tutorial_step3": "3️⃣ <b>Получите анализ</b>\nИИ проанализирует за несколько секунд и даст рекомендации",
        "tutorial_footer": "✅ Готово! Теперь можете пользоваться ботом.",
        "btn_start_using": "🚀 Начать использование",
        "btn_skip_tutorial": "⏭ Пропустить",
        
        "settings_menu": "⚙️ <b>Настройки</b>",
        "btn_change_language": "🌐 Изменить язык",
        "language_changed": "✅ Язык успешно изменен!"
    },

    "en": {
        "lang_name": "English",
        "gemini_lang_instruction": "Answer in English.",
        
        "choose_lang": "Select Language",
        "welcome_register": "👋 Hello! Please register to use the bot.",
        "ask_name": "✍️ <b>Enter your name:</b>",
        "ask_phone": "📞 <b>Send your phone number:</b>\nPress the button below 👇",
        "btn_phone": "📱 Send Contact",
        "ask_region": "📍 <b>Where are you from?</b>",
        "register_success": "✅ <b>Congratulations! You are registered.</b>",
        "register_info": "👤 Name: {name}\n📞 Phone: {phone}\n📍 Region: {region}",
        "photo_prompt": "Now select a plant part and start analysis! 👇",
        
        "menu_leaf": "🍃 Leaf",
        "menu_fruit": "🍎 Fruit",
        "menu_stem": "🌿 Stem",
        "menu_insect": "🐛 Insect",
        "menu_help": "ℹ️ Help",
        "menu_plans": "💎 Plans",
        
        "btn_back": "🔙 Back",
        "btn_menu": "🏠 Menu",
        
        "thinking": "🤔 Agronomist is thinking...",
        "analyzing": "Analyzing...",
        "send_photo": "📸 Send a photo for accurate analysis.",
        "text_advice_error": "Sorry, I didn't understand. Please send a photo.",
        "error_image_download": "❌ Failed to download photo.",
        "error_processing": "❌ An error occurred.",

        "analysis_header": "📌 <b>Prediction:</b>",
        "confidence": "📊 <b>Confidence:</b>",
        "pharmacy_title": "🗣 <b>Ask at pharmacy:</b>",
        "recipe_title": "🧴 <b>Recipe (per 10L water):</b>",
        "agrotechnics": "⚡️ <b>Agrotechnical advice:</b>",
        "safety": "❗️ <b>Note:</b>",
        "pro_promo": "💎 <b>Detailed analysis in PRO plan!</b>",
        "top_diagnosis": "🧠 <b>TOP PREDICTIONS:</b>",
        "visual_signs": "Signs",
        "biologic": "🌿 <b>Biological methods:</b>",
        "severity": "📊 Severity",
        "admin_copy": "📋 <b>FOR AGRONOMIST (COPY-PASTE):</b>",
        "welcome_back": "👋 Hello, <b>{name}</b>!\n\n🌾 Welcome to <b>Agro AI Bot</b>!",
        "welcome_desc": "Send a photo for analysis:",
        "again_prompt": "📸 Send another photo or choose a section:",
        
        "startup_notification": "🔄 <b>Bot Restarted</b>\n\n⚠️ The bot was temporarily unavailable due to maintenance. We apologize for the inconvenience!\n\n👨‍💻 Developer: @fibotai\n\n✅ The bot is now fully operational. Continue!",
        
        "tutorial_title": "📚 <b>How to use the bot?</b>",
        "tutorial_step1": "1️⃣ <b>Select plant part</b>\n🍃 Leaf, 🍎 Fruit, 🌿 Stem or 🐛 Insect",
        "tutorial_step2": "2️⃣ <b>Take a good photo</b>\n• In well-lit area\n• Close-up and clear\n• Show disease/damage clearly",
        "tutorial_step3": "3️⃣ <b>Get analysis</b>\nAI will analyze in seconds and provide recommendations",
        "tutorial_footer": "✅ Ready! You can now use the bot.",
        "btn_start_using": "🚀 Start Using",
        "btn_skip_tutorial": "⏭ Skip",
        
        "settings_menu": "⚙️ <b>Settings</b>",
        "btn_change_language": "🌐 Change Language",
        "language_changed": "✅ Language changed successfully!"
    }
}

DEFAULT_LANG = "uz"

def get_text(key: str, lang: str = DEFAULT_LANG) -> str:
    """Matnni olish"""
    return TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key, key)
