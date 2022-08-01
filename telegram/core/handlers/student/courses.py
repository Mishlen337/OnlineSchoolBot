"""Module to declare handlers related with courses."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.utils.messages import SELECT_INFO_COURSE
from core.keyboards.student_keyboards import all_keyboards

from db.student import course, order
from db.utils import exceptions


async def get_courses(message: types.Message, state: FSMContext):
    """Answers available courses."""
    logger.debug(f"Student {message.from_user} requests available courses.")
    course_list = []
    try:
        course_list = await course.get_courses(message.from_user.id)
        if course_list:
            await message.answer("Сообщение о скидке.")
            for crs in course_list:
                msg_text = SELECT_INFO_COURSE.format(
                    course_name=crs['course_name'],
                    subject_name=crs['subject_name'],
                    teacher_name=crs['teacher_name'],
                    teacher_patronymic=crs['teacher_patronymic'],
                    teacher_surname=crs['teacher_surname'],
                    begin_at=crs['begin_at'].strftime("%d-%m-%Y"),
                    end_at=crs['end_at'].strftime("%d-%m-%Y"),
                )
                match(crs['status']):
                    case 'неоплачено':
                        await message.answer(
                            f"{msg_text}Курс находится в корзине", parse_mode="HTML",
                            reply_markup=all_keyboards["course_desc"](crs['course_id']))
                    case 'оплачено':
                        await message.answer(
                            f"{msg_text}Курс оплачен", parse_mode="HTML",
                            reply_markup=all_keyboards["course_desc"](crs['course_id']))
                    case _:
                        await message.answer(
                            f"{msg_text}", parse_mode="HTML",
                            reply_markup=await all_keyboards["course_select_with_desc"](
                                crs['course_id']))
        else:
            await message.answer("Курсы отсутствуют.")
    except exceptions.ConnectionError:
        await message.answer("Упс. Что то пошло не так")
        return


async def callback_desc(call: types.CallbackQuery):
    # TODO task is to send teacher questionnaires (or links to them)
    text = call.message.text
    if (text.find('Курс находится в корзине') != -1) or ((text.find('Курс уже выбран')) != -1) or \
            (text.find('Выбран тариф') != -1):
        await call.message.edit_text(
            f"{text}\nhttps://telegra.ph/Izmajlov-Aleksandr-Ajratovich-07-14",
            parse_mode="HTML")
    else:
        await call.message.edit_text(
            f"{text}\nhttps://telegra.ph/Izmajlov-Aleksandr-Ajratovich-07-14",
            parse_mode="HTML",
            reply_markup=all_keyboards["course_select_without_desc"]())


async def callback_add_course(call: types.CallbackQuery):
    course_id = call.data.split(":")[1]
    package_name = call.data.split(":")[2]
    response_message = None

    try:
        await order.add_course_package(call.from_user.id, int(course_id), package_name)
        response_message = f"\n<b>Добавлен в корзину.\n<b>Выбран пакет: </b>{package_name}</b>"
    except exceptions.NoSuchCoursePackage:
        await call.message.delete()
        await call.answer(
                "Невозможно выбрать пакет этого курса, так как он больше не существует",
                show_alert=True,
        )
        return
    except exceptions.OrderCourseExists as e:
        if e.args[0]["status"] == 'оплачен':
            response_message = f"\n<b>Курс оплачен.\n<b>Выбраный ранее пакет: </b>{e.args[0]['package_name']}</b>"
        else:
            response_message = f"\n<b>Курс ранее добавлен в корзину.\n<b>Выбраный ранее пакет: </b>{e.args[0]['package_name']}</b>"
    except exceptions.ConnectionError:
        await call.message.answer("Упс. Что то пошло не так")
        return

    text = call.message.text
    if text.find('https') != -1:
        text1 = text[:text.find('https')]
        text2 = text[text.find('https'):]
        await call.message.edit_text(
            f"{text1}{response_message}"
            f"{text2}", parse_mode="HTML")
    else:
        await call.message.edit_text(
            f"{text}{response_message}",
            parse_mode="HTML", reply_markup=all_keyboards["course_desc"](course_id))
