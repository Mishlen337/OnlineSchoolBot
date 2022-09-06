from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from db.employee import homeworks
from db.utils import exceptions
from core.utils import employee_messages
from core.keyboards import employee_keyboards


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
                await message.bot.send_document(
                    message.from_user.id,
                    lesson["done_homework_file_id"],
                    reply_markup=employee_keyboards.all_keyboards["check_homework"](message.from_user.id, "les", lesson["id"]))

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
                await message.bot.send_document(
                    message.from_user.id,
                    lesson["done_homework_file_id"],
                    reply_markup=employee_keyboards.all_keyboards["check_homework"](message.from_user.id, "web", lesson["id"]))

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

                await message.bot.send_document(
                        message.from_user.id,
                        lesson["done_homework_file_id"],
                        reply_markup=employee_keyboards.all_keyboards["check_homework"](message.from_user.id, "group", lesson["id"]))

        if not personal_lessons_list and not webinars_list and not group_lessons_list:
            await message.answer("Домашек для проверки нет!")
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")


async def check_homework(callback: types.CallbackQuery, state: FSMContext):
    logger.debug(f"Employee {callback.from_user} wants to check homework")
    mass = callback.data.split(':')
    tip, tg_id, lesson_id = mass[1], int(mass[2]), int(mass[3])
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text="Назад")
    keyboard.add(button)
    await callback.message.reply(
        text="Прикрепите файл проверенного дз. Проверить Домашнее задание можно один раз. Либо нажмите кнопку <b>назад</b>",
        parse_mode="HTML",
        reply_markup=keyboard)
    await state.update_data(
        tip=tip,
        tg_id=tg_id,
        lesson_id=lesson_id
    )
    await state.set_state("employee_check_homework")
    await callback.answer()


async def back_to_menu(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись в главное меню",
        reply_markup=employee_keyboards.all_keyboards["menu"]())
    await state.set_state("employee_main")
    await state.reset_data()


async def send_checked_homework(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} wants to send homework")
    data = await state.get_data()
    try:
        match data["tip"]:
            case "web":
                await homeworks.check_webinar_homework(data["tg_id"], data["lesson_id"], message.document.file_id)
            case "les":
                await homeworks.check_personal_homework(data["tg_id"], data["lesson_id"], message.document.file_id)
            case "group":
                await homeworks.check_group_lesson_homework(data["tg_id"], data["lesson_id"], message.document.file_id)
        await message.answer("Проверенное домашнее задание успешно прикреплено!", reply_markup=employee_keyboards.all_keyboards["menu"]())
    except exceptions.AccessError:
        await message.answer("Ошибка. Вы не можете проверить данное дз.", reply_markup=employee_keyboards.all_keyboards["menu"]())
    except exceptions.CheckError:
        await message.answer("Ошибка. Домашнее задание было проверено.", reply_markup=employee_keyboards.all_keyboards["menu"]())
    except ConnectionError:
        await message.answer("Упс. Что-то пошло не так", reply_markup=employee_keyboards.all_keyboards["menu"]())
    await state.set_state("employee_main")
    await state.reset_data()


async def error_send_checked_homework(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} error wants to send")
    await message.answer("Прикрепите файл, чтобы проверить домашнее задание или нажмите кнопку <b>назад</b>",
                         parse_mode="HTML")

