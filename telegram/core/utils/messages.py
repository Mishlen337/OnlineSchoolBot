"""Module to declare message templates."""
PERSONAL_LESSON_MESSAGE = '''<b>Преподаватель: {teacher_name}</b>
Название занятия: {lesson_title}
Место проведения: {place}
'''
<<<<<<< Updated upstream
=======
SELECT_INFO_COURSE = '''<b>Название курса: {name}</b>
Название предмета: {course_subject_name}
Преподаватель: {teacher_subject_name}
Тариф Стандарт: {price_course_standard}
Тариф ПРО: {price_course_pro}
Дата начала курса: {begin_at}
Дата конца курса: {end_at}
'''
BASKET_INFO_COURSE = '''<b>Название курса: {name}</b>
Название предмета: {course_subject_name}
Преподаватель: {teacher_subject_name}
Выбранный тариф: {tariff}
Стоимость выбранного тарифа: {selected_tariff}
Дата начала курса: {begin_at}
Дата конца курса: {end_at}

'''
SCHEDULE_INFO_COURSE = '''<b>Название курса: {name}</b>
Название предмета: {course_subject_name}
Преподаватель: {teacher_subject_name}
Дата начала занятия: {begin_at}
Ссылка на занятие: {broadcast_link}
'''