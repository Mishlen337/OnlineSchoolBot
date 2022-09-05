from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from db.employee import homeworks
from db.utils import exceptions
from core.utils import employee_messages


async def get_homeworks(message: types.Message, state: FSMContext):
    """Answers done homeworks."""
    logger.debug(f"Employee {message.from_user} requests .")
    try:
        personal_lessons_list = await homeworks.get_personal_lessons_homeworks(message.from_user.id)
        webinars_list = await homeworks.get_webinars_homeworks(message.from_user.id)
        group_lessons_list = await homeworks.get_group_lessons_homeworks(message.from_user.id)
        if personal_lessons_list:
            await message.answer('Персональные занятия:')
            for lesson in personal_lessons_list:
                tg_username = (await message.bot.get_chat_member(
                    lesson['student_tg_id'], lesson['student_tg_id'])).user.username
                await message.answer(employee_messages.HOMEWORKS_PERSONAL.format(
                    subject_name=lesson['subject_name'],
                    student_surname=lesson['student_surname'] if lesson['student_surname'] is not None else '',
                    student_name=lesson['student_name'] if lesson['student_name'] is not None else '',
                    student_patronymic=lesson['student_patronymic'] if lesson['student_patronymic'] is not None else '',
                    tg_username='@' + tg_username if tg_username is not None else '',
                    begin_at=lesson['begin_at'].strftime("%d-%m-%Y %H:%M"),
                    end_at=lesson['end_at'].strftime("%d-%m-%Y %H:%M"),
                    homework_link=lesson['homework_link']
                ), parse_mode='HTML', disable_web_page_preview=True)
        if webinars_list:
            await message.answer('Вебинары:')
            for lesson in webinars_list:
                tg_username = (await message.bot.get_chat_member(
                    lesson['student_tg_id'], lesson['student_tg_id'])).user.username
                if lesson['format'] == 'онлайн':
                    await message.answer(employee_messages.HOMEWORKS_WEBINARS_ONLINE.format(
                        course_name=lesson['course_name'],
                        theme=lesson['theme'],
                        format=lesson['format'],
                        begin_at=lesson['begin_at'].strftime("%d-%m-%Y %H:%M"),
                        end_at=lesson['end_at'].strftime("%d-%m-%Y %H:%M"),
                        homework_link=lesson['homework_link'],
                        student_surname=lesson['student_surname'] if lesson['student_surname'] is not None else '',
                        student_name=lesson['student_name'] if lesson['student_name'] is not None else '',
                        student_patronymic=lesson['student_patronymic'] if lesson['student_patronymic'] is not None else '',
                        tg_username='@' + tg_username if tg_username is not None else '',
                    ), parse_mode='HTML', disable_web_page_preview=True)
                elif lesson['format'] == 'запись':
                    await message.answer(employee_messages.HOMEWORKS_WEBINARS_RECORD.format(
                        course_name=lesson['course_name'],
                        theme=lesson['theme'],
                        format=lesson['format'],
                        homework_link=lesson['homework_link'],
                        student_surname=lesson['student_surname'] if lesson['student_surname'] is not None else '',
                        student_name=lesson['student_name'] if lesson['student_name'] is not None else '',
                        student_patronymic=lesson['student_patronymic'] if lesson['student_patronymic'] is not None else '',
                        tg_username='@' + tg_username if tg_username is not None else '',
                    ), parse_mode='HTML', disable_web_page_preview=True)
        if group_lessons_list:
            await message.answer('Групповые занятия:')
            for lesson in group_lessons_list:
                tg_username = (await message.bot.get_chat_member(
                    lesson['student_tg_id'], lesson['student_tg_id'])).user.username
                await message.answer(employee_messages.HOMEWORKS_GROUP_LESSONS.format(
                    course_name=lesson['course_name'],
                    group_type=lesson['group_type'],
                    theme=lesson['theme'],
                    begin_at=lesson['begin_at'].strftime("%d-%m-%Y %H:%M"),
                    end_at=lesson['end_at'].strftime("%d-%m-%Y %H:%M"),
                    homework_link=lesson['homework_link'],
                    student_surname=lesson['student_surname'] if lesson['student_surname'] is not None else '',
                    student_name=lesson['student_name'] if lesson['student_name'] is not None else '',
                    student_patronymic=lesson['student_patronymic'] if lesson['student_patronymic'] is not None else '',
                    tg_username='@' + tg_username if tg_username is not None else '',
                ), parse_mode='HTML', disable_web_page_preview=True)
        if not personal_lessons_list and not webinars_list and not group_lessons_list:
            await message.answer("Домашек для проверки нет!")
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")
