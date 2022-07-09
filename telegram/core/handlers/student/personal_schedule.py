"""Module to declare handlers related with personal schedule."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext


async def get_schedule(message: types.Message, state: FSMContext):
    "Answers student's personal schedule."
    logger.debug(f"Student {message.from_user} requests personal schedule.")
    # TODO send personal schedule
    await message.answer("В расписании ничего нет.")
