"""Module to declare fastApi web server to get webhooks from telegram."""
import uvicorn

from aiogram import types, Dispatcher, Bot
from fastapi import FastAPI

from core.config import config
from core.config import bot, dp
from core import handlers
from core import filters
from loguru import logger

app = FastAPI()

WEBHOK_PATH = "/bot"


@app.on_event("startup")
async def on_startup():
    """Initializes filters, middlewares, handlers and webhook."""
    await bot.set_webhook(url=config.WEBHOOK_URL + WEBHOK_PATH)
    filters.setup(dp)
    handlers.setup(dp)


@app.post(WEBHOK_PATH)
async def bot_webhook(update: dict):
    """Process update from tg

    Args:
        update (dict): update from tg
    """
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    try:
        await dp.process_update(telegram_update)
    except Exception as e:
        await bot.send_message(config.MODERATOR_TG_ID, "EXCEPTION!!!! NEED HEELP!!!")
        logger.error(e)

    # await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    """Closes all connections."""
    await dp.bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == "__main__":
    uvicorn.run(app, host=config.TG_HOST, port=config.HOST_PORT)
