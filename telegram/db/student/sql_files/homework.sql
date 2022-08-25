--name: turn_in_personal_lesson_homework
with updated as (
update personal_lessons set done_homework_file_id = :file_id, homework_status = 'сдано'
    where id = :lesson_id and student_id = (select id from students where tg_id = :tg_id)
);
