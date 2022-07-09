"Module to declare handlers related with personal lessons."
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext


async def get_lessons(message: types.Message, state: FSMContext):
    "Answers available personal lessons"
    logger.debug(f"Student {message.from_user} requests available personal \
        lessons.")
    # TODO send available personal lessons
    await message.answer("Личных занятий нет.")
