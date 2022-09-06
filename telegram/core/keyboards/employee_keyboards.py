from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

all_keyboards = {}


def kb_employee_menu():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Занятия"),
        KeyboardButton("Проверка дз")
    )
    return kb_student


def kb_check_homework(tg_id, tip, lesson_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(
        text="Проверить дз",
        callback_data="check_homework:" + tip + ':' + str(tg_id) + ':' + str(lesson_id))
    )
    return kb


all_keyboards["check_homework"] = kb_check_homework
all_keyboards["menu"] = kb_employee_menu
