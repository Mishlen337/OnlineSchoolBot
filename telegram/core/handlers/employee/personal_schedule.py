"""Module to declare handlers related with personal schedule."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from db.employee import schedule
from db.utils import exceptions
from core.utils import employee_messages


async def get_schedule(message: types.Message, state: FSMContext):
    """Answers employees's personal schedule."""
    logger.debug(f"Employee {message.from_user} requests personal schedule.")
    try:
        personal_lessons_list = await schedule.get_personal_lessons_schedule(message.from_user.id)
        webinars_list = await schedule.get_webinars_schedule(message.from_user.id)
        group_lessons_list = await schedule.get_group_lessons_schedule(message.from_user.id)
        if personal_lessons_list:
            lesson_info = 'Персональные занятия:\n'
            for lesson in personal_lessons_list:
                tg_username = (await message.bot.get_chat_member(
                    lesson['student_tg_id'], lesson['student_tg_id'])).user.username
                lesson_info += employee_messages.SCHEDULE_INFO_PERSONAL.format(
                    subject_name=lesson['subject_name'],
                    student_surname=lesson['student_surname'] if lesson['student_surname'] is not None else '',
                    student_name=lesson['student_name'] if lesson['student_name'] is not None else '',
                    student_patronymic=lesson['student_patronymic'] if lesson['student_patronymic'] is not None else '',
                    tg_username='@' + tg_username if tg_username is not None else '',
                    begin_at=lesson['begin_at'].strftime("%d-%m-%Y %H:%M"),
                    end_at=lesson['end_at'].strftime("%d-%m-%Y %H:%M"),
                    broadcast_link=lesson['broadcast_link']
                )
            await message.answer(text=lesson_info, parse_mode='HTML', disable_web_page_preview=True)
        if webinars_list:
            lesson_info = 'Вебинары:\n'
            for lesson in webinars_list:
                lesson_info += employee_messages.SCHEDULE_INFO_WEBINARS.format(
                    course_name=lesson['course_name'],
                    theme=lesson['theme'],
                    subject_name=lesson['subject_name'],
                    begin_at=lesson['begin_at'].strftime("%d-%m-%Y %H:%M"),
                    end_at=lesson['end_at'].strftime("%d-%m-%Y %H:%M"),
                    broadcast_link=lesson['broadcast_link']
                )
            await message.answer(text=lesson_info, parse_mode='HTML', disable_web_page_preview=True)
        if group_lessons_list:
            lesson_info = 'Групповые занятия:\n'
            for lesson in group_lessons_list:
                lesson_info += employee_messages.SCHEDULE_INFO_GROUP_LESSONS.format(
                    course_name=lesson['course_name'],
                    group_type=lesson['group_type'],
                    theme=lesson['theme'],
                    subject_name=lesson['subject_name'],
                    begin_at=lesson['begin_at'].strftime("%d-%m-%Y %H:%M"),
                    end_at=lesson['end_at'].strftime("%d-%m-%Y %H:%M"),
                    broadcast_link=lesson['broadcast_link']
                )
            await message.answer(text=lesson_info, parse_mode='HTML', disable_web_page_preview=True)
        if not personal_lessons_list and not webinars_list and not group_lessons_list:
            await message.answer("В расписании ничего нет.")
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")
