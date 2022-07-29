
--name get_available_teachers
select es.subject_name, from employee_subject as es
    join employee as e on es.teacher_id = e.id
where es.role = 'personal_teacher'
