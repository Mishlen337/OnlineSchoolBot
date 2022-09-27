"""Module to declare fastApi web server to get webhooks from telegram."""
import uvicorn

from aiogram import types, Dispatcher, Bot
from aiogram.utils.exceptions import ChatNotFound
from fastapi import FastAPI, File, UploadFile, Form

from typing import Optional

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
async def bot_notification(token: str = Form(),
                           message: str = Form(),
                           image: Optional[UploadFile] = File(None, media_type="image/jpeg"),
                           users: str = Form()):
    """Send notification to all students or to particular student

    Args:
        request (Request): request object
        properties (dict): notification message
    """
    if token != config.NOTIFICATION_TOKEN:
        return {"message": "wrong notification token"}, 403

    logger.debug(f"Sending notification - {message}")

    if users == "all":
        try:
            students = await user.get_all_users()
            if image:
                for st in students:
                    try:
                        await bot.send_photo(chat_id=st["tg_id"],
                                             photo=image.file.read(),
                                             caption=message,
                                             parse_mode="HTML")
                        logger.debug(f"Image with caption was sent to {st}")
                    except ChatNotFound:
                        logger.debug(f"Couldn't sent image with caption to {st} not found")
                return {"message": "ok"}, 200
            else:
                for st in students:
                    try:
                        await bot.send_message(chat_id=st["tg_id"],
                                               text=message,
                                               parse_mode="HTML")
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
