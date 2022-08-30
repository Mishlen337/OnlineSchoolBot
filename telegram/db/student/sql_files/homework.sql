--name: get_personal_lesson_access^
select id from personal_lessons
    where id = :lesson_id and student_id = (select id from students where tg_id = :tg_id);

--name: turn_in_personal_lesson_homework
insert into done_personal_lessons_homework (personal_lesson_id, done_homework_file_id)
    values (:lesson_id, :file_id);

--name: turn_in_webinar_homework
insert into done_webinars_homework (webinar_id, student_id, done_homework_file_id)
    values (:webinar_id, (select id from students where tg_id = :tg_id limit 1), :file_id);
