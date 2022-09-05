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


all_keyboards["menu"] = kb_employee_menu
