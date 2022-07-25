"Module to declare handlers related with personal lessons."
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from core.utils.messages import PERSONAL_LESSON_MESSAGE
from core.keyboards.student_keyboards import all_keyboards

temp_personal_lessons_available = [
    {"lesson_id": "0", "teacher_name": "Кристина Мячина", "lesson_title": "Химия",
     "place": "Zoom", "desc": "Занятие по химии"},
    {"lesson_id": "1", "teacher_name": "Соня Калинина", "lesson_title": "Шизика",
     "place": "Zoom", "desc": "Занятие по обществознанию"},
    {"lesson_id": "2", "teacher_name": "Рустам Ризванов", "lesson_title": "Физика",
     "place": "Zoom", "desc": "Занятие по физике"}
]

# {"tg_id": "id", "selected_lessons": [selected_lessons_ids]}
users_selected_lessons = []


async def get_lessons(message: types.Message, state: FSMContext):
    "Answers available personal lessons"
    logger.debug(f"Student {message.from_user} requests available personal lessons.")
    if temp_personal_lessons_available:
        await message.answer("Доступные личные занятия:")
        user_selected_lessons = []
        if users_selected_lessons:
            try:
                temp_id = next(
                    (i for i, item in enumerate(users_selected_lessons) if item["tg_id"] == f"{message.from_user.id}"),
                    None)
                user_selected_lessons = users_selected_lessons[temp_id]["selected_lessons"]
            except:
                logger.debug(f"Student {message.from_user} selected 0 personal lessons.")
        for lesson in temp_personal_lessons_available:
            selected = lesson["lesson_id"] in user_selected_lessons
            msg_text = PERSONAL_LESSON_MESSAGE.format(
                teacher_name=lesson["teacher_name"],
                lesson_title=lesson["lesson_title"],
                place=lesson["place"],
            )
            if selected:
                msg_text += "\n<em>Вы записаны на это мероприятие</em>"
            reply_markup = (
                all_keyboards["personal_select_with_desc"](lesson["lesson_id"])
                if not selected
                else all_keyboards["personal_desc"](lesson["lesson_id"])
            )
            await message.answer(
                msg_text,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
    else:
        await message.answer("Личных занятий нет.")


async def show_lesson_description(callback: types.CallbackQuery):
    """Sends event description into chat

    :param callback: Callback instance
    :type callback: types.CallbackQuery
    """
    lesson_id = callback.data.split(":")[1]
    logger.debug(f"Sending description of event {lesson_id} to user {callback.from_user}")

    temp_id = next(
        (i for i, item in enumerate(temp_personal_lessons_available) if item['lesson_id'] == f"{lesson_id}"),
        None)
    target_lesson = temp_personal_lessons_available[temp_id]
    await callback.message.answer(
        target_lesson['lesson_title'] + "\n" + target_lesson["teacher_name"] + "\n" + target_lesson['desc'])


async def add_lesson(callback: types.CallbackQuery):
    lesson_id = callback.data.split(":")[1]
    logger.debug(f"Guest {callback.from_user} chose to add {lesson_id}")
    user_selected_lessons = []
    user_list_id = -1
    if users_selected_lessons:
        try:
            temp_id = next(
                (i for i, item in enumerate(users_selected_lessons) if item["tg_id"] == f"{callback.from_user.id}"),
                None)
            user_list_id = temp_id
            user_selected_lessons = users_selected_lessons[temp_id]["selected_lessons"]
        except:
            logger.debug(f"Student {callback.from_user} selected 0 personal lessons.")
    added = lesson_id in user_selected_lessons
    if added:
        logger.debug(f"Event {lesson_id} was added before by guest {callback.from_user}")
        await callback.message.delete_reply_markup()
        await callback.message.edit_text(
            callback.message.text + "\nВы выбрали это мероприятие раньше"
        )
    else:
        user_selected_lessons.append(lesson_id)
        if user_list_id >= 0:
            users_selected_lessons[user_list_id]["selected_lessons"] = user_selected_lessons
        else:
            users_selected_lessons.append({"tg_id": f"{callback.from_user.id}",
                                           "selected_lessons": user_selected_lessons})
        logger.debug(f"Event {lesson_id} was successfully added by guest {callback.from_user}")
        await callback.message.edit_text(callback.message.text + "\n\nВы выбрали это мероприятие")
        reply_markup = all_keyboards["personal_desc"](f"{lesson_id}")
        await callback.message.edit_reply_markup(reply_markup=reply_markup)
