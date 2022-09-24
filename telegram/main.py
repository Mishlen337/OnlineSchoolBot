"""Module to declare fastApi web server to get webhooks from telegram."""
import uvicorn

from aiogram import types, Dispatcher, Bot
from aiogram.utils.exceptions import ChatNotFound
from fastapi import FastAPI

from core.config import config, bot, dp
from core import handlers, filters
from db.student import user
from db.utils import exceptions
from loguru import logger

app = FastAPI()

WEBHOK_PATH = "/bot"
NOTIFICATION_PATH = "/notification"


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


@app.post(NOTIFICATION_PATH)
async def bot_notification(notification: dict):
    """Send notification to all students or to particular student

    Args:
        notification (dict): notification message

    dict keys:
        token
        message with parse mode - HTML
        users - list of tg_usernames, tg_user_ids or all
    """
    logger.debug(notification)
    if notification["token"] != config.NOTIFICATION_TOKEN:
        return {"message": "wrong notification token"}, 403

    logger.debug(f"Sending notification - {notification}")

    if notification["users"] == "all":
        try:
            students = await user.get_all_users()
            for st in students:
                try:
                    await bot.send_message(st["tg_id"], notification["message"], parse_mode="HTML")
                    logger.debug(f"Message was sent to {st}")
                except ChatNotFound:
                    logger.debug(f"Couldn't sent message to {st} not found")
            return {"message": "ok"}, 200
        except exceptions.ConnectionError:
            return {"message": "internal error"}, 500


@app.on_event("shutdown")
async def on_shutdown():
    """Closes all connections."""
    await dp.bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == "__main__":
    uvicorn.run(app, host=config.TG_HOST, port=config.HOST_PORT)
