--name: get_webinar_materials
select w.id as webinar_id, w.theme, w.format, w.begin_at, w.end_at, w.record_link, w.material_link, w.homework_link, w.homework_deadline_time
    from purchased_webinars as pw
        join webinars as w on pw.webinar_id = w.id
        join students as s on pw.student_id = s.id
    where w.course_id = :course_id and s.tg_id = :tg_id
order by w.format, w.begin_at;

--name: get_personal_lessons_materials
select pl.id as personal_lesson_id, pl.begin_at, pl.end_at, pl.record_link, pl.material_link, pl.homework_link, pl.homework_deadline_time
    from personal_lessons as pl join students as s on pl.student_id = s.id
                                join employees as e on pl.teacher_id = e.id
    where s.tg_id = :tg_id and pl.teacher_id = :teacher_id and pl.subject_name = :subject_name
order by pl.begin_at;

--name: get_group_lessons_materials
select gl.id as group_lesson_id, g.id as group_id, gl.theme, gl.begin_at, gl.end_at, gl.record_link, gl.material_link, gl.homework_link, gl.homework_deadline_time
     from group_lessons as gl
        join groups as g on gl.group_id = g.id
        join group_student as gs on g.id = gs.group_id
        join students as s on gs.student_id = s.id
    where g.course_id = :course_id and s.tg_id = :tg_id
order by gl.begin_at;
