

--name get_personal_lessons_schedule
select pl.subject_name, e.name, e.patronymic, e.surname, pl.bedin_at, pl.end_at, pl.broadcast_link
    from personal_lessons as pl
        join students as s on pl.student_id = s.id
        join employees as e on pl.teacher_id = e.id
where s.tg_id = :tg_id and now() < pl.end_at

--name get_purchased_webinars_schedule
select c.name, c.course_subject_name, w.theme, e.name, e.patronymic, e.surname, w.begin_at, w.end_at,
       pl.broadcast_link
    from purchased_webinars as pw
        join students as s on pw.student_id = s.id
        join webinars as w on pw.webinar_id = w.id
        join courses as c on w.course_id = c.id
        join employees as e on c.teacher_id = e.id
where s.tg_id = :tg_id and now() < w.end_at

