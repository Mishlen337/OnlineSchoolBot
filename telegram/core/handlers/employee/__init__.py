from aiogram import Dispatcher
from aiogram import types
from loguru import logger

from . import auth, personal_schedule, homework
from core.filters.guest_filters import CallBackFilter
# from core.filters.employee_filters import BoundFilter


def setup(dp: Dispatcher):
    "Setups handlers for employee."
    logger.debug("Start employee's handlers registration.")
    dp.register_message_handler(auth.get_contact,
                                content_types="contact",
                                state="employee_telephone")
    dp.register_message_handler(auth.get_contact_error,
                                state="employee_telephone")
    dp.register_message_handler(personal_schedule.get_schedule,
                                state="employee_main", regexp="Занятия")
    dp.register_message_handler(homework.get_homeworks,
                                state="employee_main", regexp="Проверка дз")

    dp.register_callback_query_handler(homework.check_homework, CallBackFilter("check_homework"),
                                       state="employee_main")
    dp.register_message_handler(homework.send_checked_homework, state="employee_check_homework",
                                content_types=types.ContentTypes.DOCUMENT)
    dp.register_message_handler(homework.back_to_menu, state="employee_check_homework", regexp="Назад")
    dp.register_message_handler(homework.error_send_checked_homework, state="employee_check_homework")
    logger.debug("End employee's handlers registration.")
