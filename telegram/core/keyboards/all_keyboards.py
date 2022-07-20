from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
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
all_keyboards["add_lesson"] = kb_add_lesson
all_keyboards["show_desc"] = kb_show_lesson_description
