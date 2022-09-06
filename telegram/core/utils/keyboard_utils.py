from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from db.student import course


def add_course_desc_to_kb(kb: InlineKeyboardMarkup, course_id: int) -> None:
    kb.add(InlineKeyboardButton(text="Подробнее", callback_data="course_desc:" + str(course_id)))


async def add_course_packages_to_kb(kb_student: InlineKeyboardMarkup, course_id: int) -> None:
    packages_list = await course.get_course_packages(course_id)
    kb_student.row_width = (len(packages_list) if len(packages_list) > 0 else 1)
    for package in packages_list:
        kb_student.add(
            InlineKeyboardButton(
                text=package["package_name"],
                callback_data="add_course:" + str(course_id) + ":" + package["package_name"]),
        )


def add_personal_desc_to_kb(kb: InlineKeyboardMarkup, teacher_id: int, subject_name: str) -> None:
    kb.add(InlineKeyboardButton(
        text="Подробнее",
        callback_data="personal_desc:" + str(teacher_id) + ':' + subject_name))


def add_contact_to_kb(kb: InlineKeyboardMarkup, teacher_id: int, subject_name: str) -> None:
    kb.add(InlineKeyboardButton(
        text="Связяться",
        callback_data="add_personal:" + str(teacher_id) + ':' + subject_name))


def add_materials(kb: InlineKeyboardMarkup, tg_id: int) -> None:
    kb.row_width = 1
    kb.add(
        InlineKeyboardButton(text="Вебинары", callback_data="add_webinar_materials:" + str(tg_id)),
        InlineKeyboardButton(text="Индивидуальные занятия", callback_data="add_personal_materials:" + str(tg_id)),
        InlineKeyboardButton(text="Групповые занятия", callback_data="add_group_materials:" + str(tg_id))
    )


def add_webinar_materials(kb: InlineKeyboardMarkup, tg_id, course_id: int) -> None:
    kb.add(InlineKeyboardButton(
        text="Показать материалы",
        callback_data="show_webinar_materials:" + str(tg_id) + ":" + str(course_id))
    )


def add_personal_materials(kb: InlineKeyboardMarkup, tg_id, teacher_id: int, subject_name: str) -> None:
    kb.add(InlineKeyboardButton(
        text="Показать материалы",
        callback_data="show_personal_materials:" + str(tg_id) + ":" + str(teacher_id) + ":" + subject_name)
    )


def add_group_materials(kb: InlineKeyboardMarkup, tg_id, course_id: int) -> None:
    kb.add(InlineKeyboardButton(
        text="Показать материалы",
        callback_data="show_group_materials:" + str(tg_id) + ":" + str(course_id))
    )


async def add_course_groups(kb: InlineKeyboardMarkup, tg_id, course_id: int) -> None:
    group_list = await course.get_course_groups(course_id)
    for group in group_list:
        kb.add(
            InlineKeyboardButton(
                text=group["type"],
                callback_data="choose_group:" + str(tg_id) + ":" + str(group["id"])),
        )


def add_homework(kb: InlineKeyboardMarkup, tg_id, id: int, tip: str, group_lesson_id=None) -> None:
    kb.add(InlineKeyboardButton(
        text="Сдать ДЗ",
        callback_data="pass_homework:" + tip + ':' + str(tg_id) + ':' + str(id) + ":" + str(group_lesson_id))
    )