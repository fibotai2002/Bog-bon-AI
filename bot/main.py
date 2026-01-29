"""
Bot entry point
"""

import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import start, diagnose, plan, registration, admin

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot):
    webhook_url = os.getenv("WEBHOOK_URL")
    
    # Render.com automatic URL detection
    if not webhook_url and os.getenv("RENDER_EXTERNAL_URL"):
        webhook_url = os.getenv("RENDER_EXTERNAL_URL") + "/webhook"
        
    if webhook_url:
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")

async def main():
    """
    Botni ishga tushirish
    """
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(registration.router)
    dp.include_router(start.router)
    dp.include_router(diagnose.router)
    dp.include_router(plan.router)
    dp.include_router(admin.router)
    
    # Startup hook
    dp.startup.register(on_startup)

    # Run mode check
    run_mode = os.getenv("RUN_MODE", "polling")
    
    if run_mode == "webhook":
        logger.info("Starting in WEBHOOK mode...")
        
        # Webhook server settings
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        )
        
        app = web.Application()
        webhook_requests_handler.register(app, path="/webhook")
        setup_application(app, dp, bot=bot)
        
        port = int(os.getenv("PORT", 8080))
        web.run_app(app, host="0.0.0.0", port=port)
        
    else:
        # Polling defaults
        logger.info("Starting in POLLING mode...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        if os.getenv("RUN_MODE") == "webhook":
             # Webhook mode doesn't need asyncio.run here as web.run_app handles it
             # But since main() has logic for both, we need to adapt slightly or just call main directly properly
             # main() is async, web.run_app is blocking.
             # The standard way for aiogram webhook is different from polling structure.
             # Let's refactor slightly to separating blocking web.run_app call.
             asyncio.run(main())
        else:
             asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")
    except Exception as e:
        logger.error(f"Kutilmagan xato: {e}", exc_info=True)
