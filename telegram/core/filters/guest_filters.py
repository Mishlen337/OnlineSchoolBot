"""Module to declare guest filters."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.filters import BoundFilter


class CallBackFilter(BoundFilter):
    """Class to filter callbacks."""

    key = "callback_status"

    def __init__(self, status):
        self.status = status
        logger.debug("Callback initialization")

    async def check(self, callback: types.CallbackQuery) -> bool:
        "Checks whether status of the event is right."
        logger.debug(f"Full callback name: {callback.data}")
        callback_status = callback.data.split(":")[0]
        logger.debug(f"{callback_status}")
        return callback_status == self.status
