
--name: get_webinar_materials

select w.theme, w.format, w.begin_at, w.end_at, w.record_link, w.material_link, w.homework_link
    from purchased_webinars as pw
        join webinars as w on pw.webinar_id = w.id
        join students as s on pw.student_id = s.id
    where w.course_id = :course_id and s.tg_id = :tg_id
order by w.format, w.begin_at;

--name: get_personal_lessons_materials
select pl.id as personal_lesson_id, e.name as teacher_name, e.patronymic as teacher_patronymic,
    e.surname as teacher_surname, pl.subject_name, pl.begin_at, pl.end_at, pl.record_link, pl.material_link, pl.homework_link
    from personal_lessons as pl join students as s on pl.student_id = s.id
                                join employees as e on pl.teacher_id = e.id
    where s.tg_id = :tg_id
order by pl.begin_at;