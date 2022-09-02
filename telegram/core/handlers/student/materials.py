from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.keyboards.student_keyboards import all_keyboards
from db.student import course
from db.student import material
from core.utils import messages
from db.student.personal_lesson import get_selected_personal_teachers


def formatting(string: str) -> str:
    state, change = map(str, string.split(':'))
    return state + ': ' + '<b>' + change + '</b>' + '\n'


async def get_materials(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} requests materials.")
    await message.answer(text='Выберите какие материалы вы хотите получить: ',
                         reply_markup=all_keyboards["materials"](message.from_user.id))


async def get_webinar_course_materials(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests courses for webinar materials.")
    tg_id = int(callback.data.split(':')[1])
    await callback.message.answer("Выберите курс для просмотра материалов <b>вебинаров</b>.",
                                  parse_mode="HTML")
    try:
        materials_course = await course.get_full_and_partly_purchased_courses(tg_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    logger.debug(materials_course)
    if materials_course:
        for crs in materials_course:
            text = messages.INFO_WEBINAR_COURSE_MATERIALS.format(
                course_name=crs["course_name"],
                teacher_name=crs['teacher_name'],
                teacher_patronymic=crs['teacher_patronymic'] if crs['teacher_patronymic'] is not None else '',
                teacher_surname=crs['teacher_surname'])
            await callback.message.answer(text=text,
                                          reply_markup=all_keyboards["show_webinar_materials"](
                                              tg_id=tg_id,
                                              course_id=crs["course_id"]),
                                          parse_mode='HTML')
            await callback.answer()
    else:
        await callback.message.answer("Доступных материалов курсов нет")
        await callback.answer()


async def get_webinar(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials webinars.")
    tg_id, course_id = map(int, callback.data.split(':')[1:])
    await callback.message.answer("Материалы <b>вебинаров</b>:", parse_mode="HTML")
    try:
        web_list = await material.get_webinar_materials(tg_id, course_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    if web_list:
        form = callback.message.text.split('\n')
        text = ''
        for string in form:
            text += formatting(string)
        await callback.message.answer(text=text, parse_mode='HTML')
        for web in web_list:
            if web["format"] == 'онлайн':
                text = messages.INFO_WEBINARS_ONLINE.format(
                    theme=web["theme"],
                    format=web["format"],
                    begin_at=web["begin_at"].strftime("%d-%m-%Y %H:%M"),
                    end_at=web["end_at"].strftime("%d-%m-%Y %H:%M"),
                    record_link=web["record_link"] if web["record_link"] is not None else '-',
                    material_link=web["material_link"] if web["material_link"] is not None else '-',
                    homework_link=web["homework_link"] if web["homework_link"] is not None else '-'
                )
            else:
                text = messages.INFO_WEBINARS_RECORD.format(
                    theme=web["theme"],
                    format=web["format"],
                    record_link=web["record_link"] if web["record_link"] is not None else '-',
                    material_link=web["material_link"] if web["material_link"] is not None else '-',
                    homework_link=web["homework_link"] if web["homework_link"] is not None else '-'
                )
            await callback.message.answer(text=text, parse_mode='HTML', disable_web_page_preview=True)
        await callback.answer()
    else:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()


async def get_personal_materials(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials for personal materials.")
    tg_id = int(callback.data.split(':')[1])
    await callback.message.answer("Выберите преподавателя для просмотра материалов <b>индивидуальных занятий</b>.",
                                   parse_mode="HTML")
    try:
        personal_teachers_list = await get_selected_personal_teachers(tg_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    if personal_teachers_list:
        for pers in personal_teachers_list:
            text = messages.INFO_PERSONAL_TEACHERS.format(
                teacher_surname=pers["teacher_surname"],
                teacher_name=pers["teacher_name"],
                teacher_patronymic=pers["teacher_patronymic"] if pers["teacher_patronymic"] is not None else '',
                subject_name=pers["subject_name"]
            )
            await callback.message.answer(
                text=text,
                reply_markup=all_keyboards["show_personal_materials"](tg_id, pers["teacher_id"], pers["subject_name"]),
                parse_mode='HTML')
        await callback.answer()
    else:
        await callback.message.answer("У вас отсутствуют персональные занятия")
        await callback.answer()


async def get_personal_lessons(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials for personal lessons.")
    data = callback.data.split(':')
    tg_id, teacher_id, subject_name = int(data[1]), int(data[2]), data[3]
    await callback.message.answer("Материалы <b>индивидуальных занятий</b>:", parse_mode="HTML")
    try:
        personal_list = await material.get_personal_lessons_materials(tg_id, teacher_id, subject_name)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    if personal_list:
        form = callback.message.text.split('\n')
        text = ''
        for string in form:
            text += formatting(string)
        await callback.message.answer(text=text, parse_mode='HTML')
        for pers in personal_list:
            text = messages.INFO_PERSONAL_LESSONS.format(
                begin_at=pers["begin_at"].strftime("%d-%m-%Y %H:%M"),
                end_at=pers["end_at"].strftime("%d-%m-%Y %H:%M"),
                record_link=pers["record_link"] if pers["record_link"] is not None else '-',
                material_link=pers["material_link"] if pers["material_link"] is not None else '-',
                homework_link=pers["homework_link"] if pers["homework_link"] is not None else '-'
            )
            await callback.message.answer(text=text, parse_mode='HTML', disable_web_page_preview=True)
        await callback.answer()
    else:
        await callback.message.answer("Записи уроков с данным преподавателем отсутствуют")
        await callback.answer()


async def get_group_course_materials(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests courses for group lessons materials.")
    tg_id = int(callback.data.split(':')[1])
    await callback.message.answer("Выберите курс для просмотра материалов <b>групповых занятий</b>.",
                                  parse_mode="HTML")
    try:
        materials_course = await course.get_pro_purchased_courses(tg_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    logger.debug(materials_course)
    if materials_course:
        for crs in materials_course:
            text = messages.INFO_GROUP_COURSE_MATERIALS.format(
                course_name=crs["course_name"],
                teacher_name=crs['teacher_name'],
                teacher_patronymic=crs['teacher_patronymic'] if crs['teacher_patronymic'] is not None else '',
                teacher_surname=crs['teacher_surname'])
            await callback.message.answer(text=text,
                                          reply_markup=all_keyboards["show_group_materials"](
                                              tg_id=tg_id,
                                              course_id=crs["course_id"]),
                                          parse_mode='HTML')
            await callback.answer()
    else:
        await callback.message.answer("Доступных материалов курсов нет")
        await callback.answer()


async def get_group_lessons(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials group lessons.")
    tg_id, course_id = map(int, callback.data.split(':')[1:])
    await callback.message.answer("Материалы <b>групповых занятий</b>:", parse_mode="HTML")
    try:
        group_lessons_list = await material.get_group_lessons_materials(tg_id, course_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    if group_lessons_list:
        form = callback.message.text.split('\n')
        text = ''
        for string in form:
            text += formatting(string)
        await callback.message.answer(text=text, parse_mode='HTML')
        for lesson in group_lessons_list:
            text = messages.INFO_GROUP_LESSONS.format(
                theme=lesson["theme"],
                begin_at=lesson["begin_at"].strftime("%d-%m-%Y %H:%M"),
                end_at=lesson["end_at"].strftime("%d-%m-%Y %H:%M"),
                record_link=lesson["record_link"] if lesson["record_link"] is not None else '-',
                material_link=lesson["material_link"] if lesson["material_link"] is not None else '-',
                homework_link=lesson["homework_link"] if lesson["homework_link"] is not None else '-'
            )
            await callback.message.answer(text=text, parse_mode='HTML', disable_web_page_preview=True)
        await callback.answer()
    else:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
