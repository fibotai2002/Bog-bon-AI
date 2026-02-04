import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from bot.handlers import start, image_analysis

# Loglarni sozlash
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    """
    Botni ishga tushirish funksiyasi.
    """
    # Bazani yaratish (inishalizatsiya)
    from bot.database.setup import init_db
    await init_db()

    # Bot va Dispatcher obyektlarini yaratish
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Middleware ulash
    from bot.middlewares.db_middleware import DbSessionMiddleware
    dp.update.middleware(DbSessionMiddleware())

    # Routerlarni ulash
    dp.include_router(start.router)
    dp.include_router(image_analysis.router)

    print("Bog'bon AI ishga tushdi... 🚀")
    
    # Webhookni o'chirish
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Pollingni boshlash
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
