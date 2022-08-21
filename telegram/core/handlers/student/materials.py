from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.keyboards.student_keyboards import all_keyboards
from db.student.course import get_full_and_partly_purchased_courses
from db.student.material import get_webinar_materials, get_personal_lessons_materials
from core.utils.messages import INFO_COURSE_MATERIALS, INFO_WEBINARS, INFO_PERSONAL_LESSONS


async def get_materials(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} requests materials.")
    await message.answer(text='Выберите какие материалы вы хотите получить: ',
                         reply_markup=all_keyboards["materials"](message.from_user.id))

async def get_course_materials(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials courses.")
    tg_id = int(callback.data.split(':')[1])
    try:
        materials_course = await get_full_and_partly_purchased_courses(tg_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    logger.debug(materials_course)
    if materials_course:
        for crs in materials_course:
            text = INFO_COURSE_MATERIALS.format(
                course_name=crs["course_name"],
                teacher_name=crs['teacher_name'],
                teacher_patronymic=crs['teacher_patronymic'] if crs['teacher_patronymic'] != None else '',
                teacher_surname=crs['teacher_surname'])
            await callback.message.answer(text=text,
                                          reply_markup=all_keyboards["show_course_materials"](
                                              tg_id=tg_id,
                                              course_id=crs["course_id"]),
                                          parse_mode='HTML')
            await callback.answer()
    else:
        await callback.message.answer("Доступных материалов курсов нет")
        await callback.answer()

async def get_webinar(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials webinars.")
    tg_id, course_id = map(int,callback.data.split(':')[1:])
    try:
        web_list = await get_webinar_materials(tg_id, course_id)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    if web_list:
        await callback.message.answer(callback.message.text)
        for web in web_list:
            text = INFO_WEBINARS.format(
                theme=web["theme"],
                format=web["format"],
                begin_at=web["begin_at"].strftime("%d-%m-%Y %H:%M"),
                end_at=web["end_at"].strftime("%d-%m-%Y %H:%M"),
                record_link=web["record_link"] if web["record_link"] is not None else '-',
                material_link=web["material_link"] if web["material_link"] is not None else '-',
                homework_link=web["homework_link"] if web["homework_link"] is not None else '-'
            )
            await callback.message.answer(text=text, parse_mode='HTML')
        await callback.answer()
    else:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()

async def get_personal_materials(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials for personal lessons.")
    tg_id = int(callback.data.split(':')[1])
    await callback.message.edit_text(text=callback.message.text,
                                     reply_markup=await all_keyboards["show_personal_subjects"](tg_id))

async def get_personal_lessons(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Student {callback.from_user} requests materials for personal lessons.")
    data = callback.data.split(':')
    tg_id, teacher_id, subject_name = int(data[1]), int(data[2]), data[3]
    try:
        personal_list = await get_personal_lessons_materials(tg_id,teacher_id,subject_name)
    except ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
        await callback.answer()
        return
    if personal_list:
        for pers in personal_list:
            text = INFO_PERSONAL_LESSONS.format(
                subject_name=subject_name,
                begin_at=pers["begin_at"].strftime("%d-%m-%Y %H:%M"),
                end_at=pers["end_at"].strftime("%d-%m-%Y %H:%M"),
                record_link=pers["record_link"] if pers["record_link"] is not None else '-',
                material_link=pers["material_link"] if pers["material_link"] is not None else '-',
                homework_link=pers["homework_link"] if pers["homework_link"] is not None else '-'
            )
            await callback.message.answer(text=text, parse_mode='HTML')
        await callback.answer()
    else:
        await callback.message.answer("Записи уроков с данным преподавателем отсутствуют")
        await callback.answer()
