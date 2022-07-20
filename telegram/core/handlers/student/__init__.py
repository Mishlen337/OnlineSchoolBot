"""Package to declare student's handlers."""
from aiogram import Dispatcher
from loguru import logger
from core.filters.guest_filters import CallBackFilter
from . import courses, personal_lessons, personal_schedule, basket


def setup(dp: Dispatcher):
    "Setups handlers for student."
    logger.debug("Start student's handlers registration.")
    dp.register_message_handler(courses.get_courses, regexp="Выбрать курсы",
                                state="student_main")
    dp.register_message_handler(personal_lessons.get_lessons,
                                regexp="Выбрать индивидуальные занятия",
                                state="student_main")
    dp.register_message_handler(personal_schedule.get_schedule,
                                regexp="Мое расписание",
                                state="student_main")
    dp.register_message_handler(basket.get_basket, regexp="Корзина",
                                state="student_main")
    dp.register_callback_query_handler(
        personal_lessons.show_lesson_description,
        CallBackFilter("show_desc"),
        state="student_main"
    )
    dp.register_callback_query_handler(
        personal_lessons.add_lesson,
        CallBackFilter("add"),
        state="student_main"
    )
    logger.debug("End student's handlers registration.")
