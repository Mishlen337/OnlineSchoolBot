"""Module to declare handlers related with personal schedule."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.utils.messages import SCHEDULE_INFO_COURSE

mathematics = {'id': 0,
               'name': 'Математика подготовка к ЕГЭ',
               'course_subject_name': 'Математика',
               'teacher_subject_name': 'Галаган Гомункулич Васильевич',
               'price_course': '100 рублей',
               'begin_at': '21.08.2022 в 21:00',
               'end_at': '22.08.2023',
               'broadcast_link': 'https://youtu.be/HwhrPZuNJTY',
               'Basket': False,
               'Selected': True}
physics = {'id': 1,
           'name': 'Физика подготовка к ЕГЭ',
           'course_subject_name': 'Физика',
           'teacher_subject_name': 'Калинина биг босс абудаби',
           'price_course': '100 рублей',
           'begin_at': '21.08.2022 в 21:00',
           'end_at': '22.08.2023',
           'broadcast_link': 'https://youtu.be/HwhrPZuNJTY',
           'Basket': False,
           'Selected': True}
informatics = {'id': 2,
               'name': 'Информатика подготовка к ЕГЭ',
               'course_subject_name': 'Информатика',
               'teacher_subject_name': 'Измайлов Марат Айратович',
               'price_course': '100 рублей',
               'begin_at': '21.08.2022 в 21:00',
               'end_at': '22.07.2023',
               'broadcast_link': 'https://youtu.be/HwhrPZuNJTY',
               'Basket': False,
               'Selected': True}

lessons_list_personal = [mathematics, physics]
lessons_list_web = [informatics]

async def get_schedule(message: types.Message, state: FSMContext):
    """Answers student's personal schedule."""
    logger.debug(f"Student {message.from_user} requests personal schedule.")
    # TODO send personal schedule
    # TODO send web shedule
    num_subjects = len(lessons_list_personal) + len(lessons_list_web)
    if num_subjects > 0:
        lesson_info = 'Персональные занятия:\n'
        for lesson in lessons_list_personal:
            lesson_info += SCHEDULE_INFO_COURSE.format(
                name=lesson['name'],
                course_subject_name=lesson['course_subject_name'],
                teacher_subject_name=lesson['teacher_subject_name'],
                begin_at=lesson['begin_at'],
                broadcast_link=lesson['broadcast_link']
            )
        await message.answer(text=lesson_info, parse_mode='HTML')
        lesson_info = 'Вебинары:\n'
        for lesson in lessons_list_web:
            lesson_info += SCHEDULE_INFO_COURSE.format(
                name=lesson['name'],
                course_subject_name=lesson['course_subject_name'],
                teacher_subject_name=lesson['teacher_subject_name'],
                begin_at=lesson['begin_at'],
                broadcast_link=lesson['broadcast_link']
            )
        await message.answer(text=lesson_info, parse_mode='HTML')
    else:
        await message.answer("В расписании ничего нет.")
