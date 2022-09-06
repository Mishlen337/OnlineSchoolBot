"Module to declare handlers related with personal lessons."
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from core.config import config
from core.utils.messages import TUTOR_MESSAGE
from core.keyboards.student_keyboards import all_keyboards
from . handlers_utils import formatting

from db.student import personal_lesson
from db.employee import user
from db.utils import exceptions

"""select e.name, e.patronymic, e.surname, es.subject_name, es.individual_price
    from employee_subject as es
        join employees as e on es.employee_id = e.id
where es.role = 'personal_teacher' and es.available = True;"""


async def get_tutors(message: types.Message, state: FSMContext):
    "Answers available tutors"
    logger.debug(f"Student {message.from_user} requests available tutors.")
    try:
        personal_teacher_list = await personal_lesson.get_available_teachers()
        if personal_teacher_list:
            await message.answer("Доступные репетиторы:")
            for teacher in personal_teacher_list:
                msg_text = TUTOR_MESSAGE.format(
                    teacher_name=teacher['teacher_name'],
                    teacher_patronymic=teacher['teacher_patronymic'] if teacher['teacher_patronymic'] != None else '',
                    teacher_surname=teacher['teacher_surname'],
                    subject_name=teacher['subject_name']
                )
                await message.answer(
                    msg_text,
                    reply_markup=all_keyboards['personal_select_with_desc'](teacher["teacher_id"],
                                                                            teacher["subject_name"]),
                    parse_mode="HTML"
                )
        else:
            await message.answer("Доступных репетиторов нет.")
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")


async def show_tutor_description(callback: types.CallbackQuery):
    """Sends event description into chat

    :param callback: Callback instance
    :type callback: types.CallbackQuery
    """
    teacher_id = int(callback.data.split(":")[1])
    subject_name = callback.data.split(":")[2]
    logger.debug(f"Sending description of tutor {teacher_id} {subject_name} to user {callback.from_user}")
    try:
        description = await personal_lesson.get_personal_teacher_description(teacher_id, subject_name)
    except exceptions.NoSuchTutor:
        await callback.answer("Данные преподаватель больше недоступен.")
        return
    except exceptions.ConnectionError:
        await callback.answer("Упс. Что-то пошло не так")
        return
    text_list = callback.message.text.split('\n')
    text = ''
    for i in range(2):
        text += formatting(text_list[i])
    if len(text_list) != 2:
        text += '<b>'
        for i in range(2, len(text_list)):
            text += text_list[i] + '\n'
        text += '</b>'
    await callback.message.edit_text(
        f"{text}\n{description}", parse_mode='HTML',
        reply_markup=all_keyboards["personal_select_without_desc"](teacher_id, subject_name))


async def contact_tutor(callback: types.CallbackQuery):
    teacher_id = int(callback.data.split(":")[1])
    subject_name = callback.data.split(":")[2]
    logger.debug(f"Guest {callback.from_user} chose to contact {teacher_id} {subject_name}")
    try:
        tg_id = (await user.get_user_tg_id(teacher_id))["tg_id"]
    except exceptions.ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
    if tg_id:
        if callback.from_user.username:
            await callback.message.bot.send_message(
                tg_id,
                f"Ученик @{callback.from_user.username} хочет взять у вас урок по предмету <b>{subject_name}</b>. Свяжитесь с ним для назначения времени.",
                parse_mode="HTML")
            await callback.message.answer("Спасибо, что выбрали индивидуальное занятие, скоро с вами свяжется преподаватель и согласует удобное время.\n Время занятия появится в рассписании.")
        else:
            await callback.message.answer("Укажите ваш username в настройках телеграмма, чтобы преподаватель мог с вами связаться.")

    else:
        await callback.message.answer("Пока с преподавателем неудалось связаться. Попробуйте чуть позже.")
