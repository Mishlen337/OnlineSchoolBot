--name: get_personal_lessons_schedule
select pl.subject_name, pl.begin_at, pl.end_at, pl.broadcast_link,
    s.name as student_name, s.patronymic as student_patronymic, s.surname as student_surname,
    s.tg_id as student_tg_id
    from personal_lessons as pl join students as s on pl.student_id = s.id
where pl.teacher_id = (select id from employees where tg_id = :tg_id) and now() < pl.end_at
order by pl.subject_name, pl.begin_at;

--name: get_webinars_schedule
select c.name as course_name, c.subject_name, w.begin_at, w.end_at, w.broadcast_link, w.theme
    from webinars as w join courses as c on w.course_id = c.id
where c.teacher_id = (select id from employees where tg_id = :tg_id) and w.format = 'онлайн' and now() < w.end_at
order by c.name, w.begin_at;

--name: get_group_lessons_schedule
select c.name as course_name, g.type as group_type,
    c.subject_name, gl.theme, gl.begin_at, gl.end_at, gl.broadcast_link
    from group_lessons as gl join groups as g on gl.group_id = g.id
                             join courses as c on g.course_id = c.id
where c.teacher_id = (select id from employees where tg_id = :tg_id) and now() < gl.end_at
order by c.name, gl.begin_at;
