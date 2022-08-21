from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from core.utils import keyboard_utils

all_keyboards = {}


#  basic keyboards


def kb_student_menu():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Курсы"),
        KeyboardButton("Репетиторы"),
        KeyboardButton("Занятия"),
        KeyboardButton("Корзина"),
        KeyboardButton("Материалы")
    )
    return kb_student


def kb_menubasket():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Курсы"),
        KeyboardButton("Репетиторы"),
        KeyboardButton("Занятия"),
        KeyboardButton("Очистить корзину"),
        KeyboardButton("Материалы")
    )
    return kb_student


#  course keyboards

async def kb_course_select_with_desc(course_id):
    kb_student = InlineKeyboardMarkup()
    await keyboard_utils.add_course_packages_to_kb(kb_student, course_id)
    keyboard_utils.add_course_desc_to_kb(kb_student, course_id)
    return kb_student


async def kb_course_select_without_desc(course_id: int) -> None:
    kb_student = InlineKeyboardMarkup()
    await keyboard_utils.add_course_packages_to_kb(kb_student, course_id)
    return kb_student


def kb_course_desc(course_id):
    kb_student = InlineKeyboardMarkup()
    keyboard_utils.add_course_desc_to_kb(kb_student, course_id)
    return kb_student


#  personal keyboards


def kb_personal_desc(teacher_id: int, subject_name: str) -> InlineKeyboardMarkup:
    kb_show_desc = InlineKeyboardMarkup()
    keyboard_utils.add_personal_desc_to_kb(kb_show_desc, teacher_id, subject_name)
    return kb_show_desc


def kb_personal_select_with_desc(teacher_id: int, subject_name: str) -> InlineKeyboardMarkup:
    kb_add_lesson = InlineKeyboardMarkup()
    keyboard_utils.add_contact_to_kb(kb_add_lesson, teacher_id, subject_name)
    keyboard_utils.add_personal_desc_to_kb(kb_add_lesson, teacher_id, subject_name)
    return kb_add_lesson


def kb_personal_select_without_desc(teacher_id: int, subject_name: str) -> InlineKeyboardMarkup:
    kb_add_lesson = InlineKeyboardMarkup()
    keyboard_utils.add_contact_to_kb(kb_add_lesson, teacher_id, subject_name)
    return kb_add_lesson


# materials keyboards

def kb_materials(tg_id: int):
    kb_student = InlineKeyboardMarkup()
    keyboard_utils.add_materials(kb_student, tg_id)
    return kb_student


def kb_show_course_materials(tg_id, course_id: int):
    kb_student = InlineKeyboardMarkup()
    keyboard_utils.add_course_materials(kb_student, tg_id, course_id)
    return kb_student


async def kb_show_personal_subjects(tg_id: int):
    kb_student = InlineKeyboardMarkup()
    await keyboard_utils.add_subjects(kb_student, tg_id)
    return kb_student


all_keyboards["menu"] = kb_student_menu
all_keyboards["menubasket"] = kb_menubasket
all_keyboards["course_select_without_desc"] = kb_course_select_without_desc
all_keyboards["course_select_with_desc"] = kb_course_select_with_desc
all_keyboards["course_desc"] = kb_course_desc
all_keyboards["personal_select_with_desc"] = kb_personal_select_with_desc
all_keyboards["personal_select_without_desc"] = kb_personal_select_without_desc
all_keyboards["materials"] = kb_materials
all_keyboards["show_course_materials"] = kb_show_course_materials
all_keyboards["show_personal_subjects"] = kb_show_personal_subjects
