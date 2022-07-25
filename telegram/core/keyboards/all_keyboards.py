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

def ib_student_tarifselect_1():
    kb_student = InlineKeyboardMarkup(row_width=2)
    kb_student.add(
        InlineKeyboardButton(text="Добавить стандарт",callback_data="standard"),
        InlineKeyboardButton(text="Добавить ПРО",callback_data="pro"),
        InlineKeyboardButton(text="Подробнее", callback_data="detail")
    )
    return kb_student

def ib_student_tarifselect_2():
    kb_student = InlineKeyboardMarkup(row_width=2)
    kb_student.add(
        InlineKeyboardButton(text="Добавить стандарт",callback_data="standard"),
        InlineKeyboardButton(text="Добавить ПРО",callback_data="pro"),
    )
    return kb_student

def ib_student_detail():
    kb_student = InlineKeyboardMarkup()
    kb_student.add(InlineKeyboardButton(text="Подробнее", callback_data="detail"))
    return kb_student

def kb_student_menubasket():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Выбрать курсы"),
        KeyboardButton("Выбрать индивидуальные занятия"),
        KeyboardButton("Мое рассписание"),
        KeyboardButton("Очистить корзину")
    )
    return kb_student

def add_show_desc_to_kb(kb: InlineKeyboardMarkup, lesson_id: str) -> None:
    kb.add(InlineKeyboardButton(text="Подробнее", callback_data="show_desc:" + lesson_id))


def kb_show_lesson_description(id: str) -> InlineKeyboardMarkup:
    kb_show_desc = InlineKeyboardMarkup()
    add_show_desc_to_kb(kb_show_desc, id)
    return kb_show_desc


def kb_add_lesson(lesson_id: str) -> InlineKeyboardMarkup:
    _kb_add_lesson = InlineKeyboardMarkup()
    _kb_add_lesson.add(InlineKeyboardButton(text="Добавить", callback_data="add:" + lesson_id))
    add_show_desc_to_kb(_kb_add_lesson, lesson_id)
    return _kb_add_lesson


all_keyboards["student_menu"] = kb_student_menu
all_keyboards["student_tarifselect_1"] = ib_student_tarifselect_1
all_keyboards["student_detail"] = ib_student_detail
all_keyboards["student_tarifselect_2"] = ib_student_tarifselect_2
all_keyboards["student_menubasket"] = kb_student_menubasket
all_keyboards["add_lesson"] = kb_add_lesson
all_keyboards["show_desc"] = kb_show_lesson_description
