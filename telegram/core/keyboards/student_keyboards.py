from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

all_keyboards = {}


def kb_student_menu():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Выбрать курсы"),
        KeyboardButton("Выбрать индивидуальные занятия"),
        KeyboardButton("Мое расписание"),
        KeyboardButton("Корзина")
    )
    return kb_student


def kb_course_select_with_desc():
    kb_student = InlineKeyboardMarkup(row_width=2)
    kb_student.add(
        InlineKeyboardButton(text="Добавить стандарт", callback_data="standard"),
        InlineKeyboardButton(text="Добавить ПРО", callback_data="pro"),
        InlineKeyboardButton(text="Подробнее", callback_data="course_desc")
    )
    return kb_student


def kb_course_select_without_desc():
    kb_student = InlineKeyboardMarkup(row_width=2)
    kb_student.add(
        InlineKeyboardButton(text="Добавить стандарт", callback_data="add_course_standard"),
        InlineKeyboardButton(text="Добавить ПРО", callback_data="add_course_pro"),
    )
    return kb_student


def kb_course_desc():
    kb_student = InlineKeyboardMarkup()
    kb_student.add(InlineKeyboardButton(text="Подробнее", callback_data="course_desc"))
    return kb_student


def kb_menubasket():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Выбрать курсы"),
        KeyboardButton("Выбрать индивидуальные занятия"),
        KeyboardButton("Мое рассписание"),
        KeyboardButton("Очистить корзину")
    )
    return kb_student


def add_personal_desc_to_kb(kb: InlineKeyboardMarkup, lesson_id: str) -> None:
    kb.add(InlineKeyboardButton(text="Подробнее", callback_data="personal_desc:" + lesson_id))


def kb_personal_desc(id: str) -> InlineKeyboardMarkup:
    kb_show_desc = InlineKeyboardMarkup()
    add_personal_desc_to_kb(kb_show_desc, id)
    return kb_show_desc


def kb_personal_select_with_desc(lesson_id: str) -> InlineKeyboardMarkup:
    _kb_add_lesson = InlineKeyboardMarkup()
    _kb_add_lesson.add(InlineKeyboardButton(text="Добавить",
                                            callback_data="add_personal:" + lesson_id))
    add_personal_desc_to_kb(_kb_add_lesson, lesson_id)
    return _kb_add_lesson


all_keyboards["menu"] = kb_student_menu
all_keyboards["course_select_without_desc"] = kb_course_select_without_desc
all_keyboards["course_select_with_desc"] = kb_course_select_with_desc
all_keyboards["course_desc"] = kb_course_desc
all_keyboards["menubasket"] = kb_menubasket
all_keyboards["personal_select_with_desc"] = kb_personal_select_with_desc
all_keyboards["personal_desc"] = kb_personal_desc
