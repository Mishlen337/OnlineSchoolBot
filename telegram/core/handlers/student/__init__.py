"""Package to declare student's handlers."""
from aiogram import Dispatcher
from loguru import logger
from . import courses, personal_lessons, personal_schedule, basket
from core.filters.guest_filters import CallBackFilter

def setup(dp: Dispatcher):
    "Setups handlers for student."
    logger.debug("Start student's handlers registration.")
    dp.register_message_handler(courses.get_courses, regexp="Выбрать курсы",
                                state="student_main")
    dp.register_message_handler(personal_lessons.get_lessons,
                                regexp="Выбрать индивидуальные занятия",
                                state="student_main")
    dp.register_message_handler(personal_schedule.get_schedule,
                                regexp="Мое рассписание", state="student_main")
    dp.register_message_handler(basket.get_basket, regexp="Корзина",
                                state="student_main")
    dp.register_callback_query_handler(courses.callback_detail,CallBackFilter("detail"),
                               state="student_main")
    dp.register_callback_query_handler(courses.callback_standard,CallBackFilter("standard"),
                                       state="student_main")
    dp.register_callback_query_handler(courses.callback_pro,CallBackFilter("pro"),
                                       state="student_main")
    logger.debug("End student's handlers registration.")
