

--name: get_personal_lessons_schedule
select pl.subject_name,
    e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname,
    pl.begin_at, pl.end_at, pl.broadcast_link
    from personal_lessons as pl
        join students as s on pl.student_id = s.id
        join employees as e on pl.teacher_id = e.id
where s.tg_id = :tg_id and now() < pl.end_at
order by pl.subject_name, pl.begin_at;

--name: get_purchased_webinars_schedule
select c.name as course_name, c.subject_name, w.theme,
    e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname,
    w.begin_at, w.end_at, w.broadcast_link
    from purchased_webinars as pw
        join students as s on pw.student_id = s.id
        join webinars as w on pw.webinar_id = w.id
        join courses as c on w.course_id = c.id
        join employees as e on c.teacher_id = e.id
where s.tg_id = :tg_id and now() < w.end_at
order by c.name, w.begin_at;

--name: get_group_lessons_schedule
select c.name as course_name, c.subject_name, g.type as group_type, gl.theme,
    e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname,
    gl.begin_at, gl.end_at, gl.broadcast_link
    from group_lessons as gl
        join groups as g on gl.group_id = g.id
        join courses as c on g.course_id = c.id
        join employees as e on c.teacher_id = e.id
        join group_student as gs on g.id = gs.group_id
        join students as s on gs.student_id = s.id
where s.tg_id = :tg_id and now() < gl.end_at
order by c.name, gl.begin_at;
