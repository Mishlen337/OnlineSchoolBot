--name: get_personal_lessons_homeworks
select 
    dplh.id, pl.subject_name, pl.begin_at, pl.end_at,
    s.name as student_name, s.patronymic as student_patronymic, s.surname as student_surname,
    s.tg_id as student_tg_id, pl.homework_link, dplh.done_homework_file_id
    from done_personal_lessons_homework as dplh
    join personal_lessons as pl on dplh.personal_lesson_id = pl.id
    join students as s on pl.student_id = s.id
where dplh.personal_assisting_id in 
        (select pa.id from employees as e join personal_assistings as pa on e.id = pa.assistant_id where e.tg_id = :tg_id) and
    pl.homework_deadline_time is not null -- and now() > pl.homework_deadline_time
        and dplh.checked_homework_file_id is null
order by pl.subject_name, pl.begin_at, s.surname, s.name, s.patronymic;

--name: get_webinars_homeworks
select 
    dwh.id, s.name as student_name, s.patronymic as student_patronymic, s.surname as student_surname,
    s.tg_id as student_tg_id,
    c.name as course_name, w.theme, w.format, w.begin_at, w.end_at, w.homework_link, dwh.done_homework_file_id
        from done_webinars_homework as dwh
            join webinars as w on dwh.webinar_id = w.id
            join students as s on dwh.student_id = s.id
            join courses as c on w.course_id = c.id
    where dwh.assistant_id = (select id from employees where tg_id = :tg_id) and
        w.homework_deadline_time is not null -- and now() > w.homework_deadline_time
            and dwh.checked_homework_file_id is null
    order by c.name, w.format, w.begin_at, s.surname, s.name, s.patronymic;

--name: get_group_lessons_homeworks
select
    dgh.id, s.name as student_name, s.patronymic as student_patronymic, s.surname as student_surname,
    s.tg_id as student_tg_id,
    c.name as course_name, g.type as group_type, gl.theme, gl.begin_at, gl.end_at, gl.homework_link, dgh.done_homework_file_id
    from done_group_homework as dgh
     join group_lessons as gl on dgh.group_lesson_id = gl.id
     join groups as g on gl.group_id = g.id
     join courses as c on g.course_id = c.id
     join students as s on dgh.student_id = s.id
where dgh.assistant_id = (select id from employees where tg_id = :tg_id) and
    gl.homework_deadline_time is not null -- and now() > gl.homework_deadline_time
        and dgh.checked_homework_file_id is null
order by c.name, g.type, gl.begin_at, s.surname, s.name, s.patronymic;

--name: get_personal_homework^
select checked_homework_file_id from done_personal_lessons_homework
    where id = :lesson_id and personal_assisting_id in 
        (select pa.id from employees as e join personal_assistings as pa on e.id = pa.assistant_id where e.tg_id = :tg_id)

--name: check_personal_homework
update done_personal_lessons_homework set checked_homework_file_id = :file_id
    where personal_assisting_id in 
        (select pa.id from employees as e join personal_assistings as pa on e.id = pa.assistant_id where e.tg_id = :tg_id)
        and id = :lesson_id

--name: get_webinar_homework^
select checked_homework_file_id from done_webinars_homework
    where id = :lesson_id and assistant_id = (select id from employees where tg_id = :tg_id)

--name: check_webinar_homework
update done_webinars_homework set checked_homework_file_id = :file_id
    where assistant_id = (select id from employees where tg_id = :tg_id) and id = :lesson_id

--name: get_group_lesson_homework^
select checked_homework_file_id from done_group_homework
    where id = :lesson_id and assistant_id = (select id from employees where tg_id = :tg_id)

--name: check_group_lesson_homework
update done_group_homework set checked_homework_file_id = :file_id
    where assistant_id = (select id from employees where tg_id = :tg_id) and id = :lesson_id