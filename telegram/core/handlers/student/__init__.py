"""Package to declare student's handlers."""
from aiogram import Dispatcher
from aiogram import types
from loguru import logger
from core.filters.guest_filters import CallBackFilter
from . import courses, personal_lessons, personal_schedule, basket, materials


def setup(dp: Dispatcher):
    "Setups handlers for student."
    logger.debug("Start student's handlers registration.")
    # main
    dp.register_message_handler(courses.get_courses, regexp="Курсы",
                                state="student_main")
    dp.register_message_handler(personal_lessons.get_tutors,
                                regexp="Репетиторы",
                                state="student_main")
    dp.register_message_handler(personal_schedule.get_schedule, regexp="Занятия",
                                state="student_main")
    dp.register_message_handler(basket.get_basket, regexp="Корзина",
                                state="student_main")
    dp.register_message_handler(basket.clear_basket, regexp="Очистить корзину",
                                state="student_main")
    dp.register_message_handler(materials.get_materials, regexp="Материалы",
                                state="student_main")

    # course order
    dp.register_callback_query_handler(courses.callback_desc, CallBackFilter("course_desc"),
                                       state="student_main")
    dp.register_callback_query_handler(courses.callback_add_course, CallBackFilter("add_course"),
                                       state="student_main")

    # personal lesson order
    dp.register_callback_query_handler(
        personal_lessons.show_tutor_description,
        CallBackFilter("personal_desc"),
        state="student_main"
    )
    dp.register_callback_query_handler(
        personal_lessons.contact_tutor,
        CallBackFilter("add_personal"),
        state="student_main"
    )

    # materials
    dp.register_callback_query_handler(materials.get_webinar_course_materials, CallBackFilter("add_webinar_materials"),
                                       state="student_main")
    dp.register_callback_query_handler(materials.get_personal_materials, CallBackFilter("add_personal_materials"),
                                       state="student_main")
    dp.register_callback_query_handler(materials.get_webinar, CallBackFilter("show_webinar_materials"),
                                       state="student_main")
    dp.register_callback_query_handler(materials.get_personal_lessons, CallBackFilter("show_personal_materials"),
                                       state="student_main")
    dp.register_callback_query_handler(materials.get_group_course_materials, CallBackFilter("add_group_materials"),
                                       state="student_main")
    dp.register_callback_query_handler(materials.get_group_lessons, CallBackFilter("show_group_materials"),
                                       state="student_main")

    # payments
    dp.register_pre_checkout_query_handler(basket.checkout_process,
                                           state="student_main")
    dp.register_message_handler(basket.successful_payment,
                                content_types=types.ContentType.SUCCESSFUL_PAYMENT,
                                state="student_main")

    dp.register_callback_query_handler(basket.choose_group, CallBackFilter("choose_group"),
                                       state="student_main")

    # schedule
    dp.register_message_handler(personal_schedule.get_schedule,
                                regexp="Мое расписание",
                                state="student_main")

    logger.debug("End student's handlers registration.")
