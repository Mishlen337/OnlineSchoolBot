
--name: get_available_teachers
select e.id as teacher_id, e.name as teacher_name, e.patronymic as teacher_patronymic,
    e.surname as teacher_surname, es.subject_name, es.individual_price as price
    from employee_subject as es
        join employees as e on es.employee_id = e.id
where es.role = 'personal_teacher' and es.available = True;

--name: get_personal_teacher_description^
select description from employee_subject
where subject_name = :subject_name and employee_id = :employee_id and role = 'personal_teacher'
limit 1;

--name: get_selected_personal_teachers
select e.id as teacher_id, e.name as teacher_name, e.patronymic as teacher_patronymic,
    e.surname as teacher_surname, pl.subject_name
    from personal_lessons as pl
    join employees as e on pl.teacher_id = e.id
    join students as s on pl.student_id = s.id
where s.tg_id = :tg_id
group by e.id, e.name, e.patronymic, e.surname, pl.subject_name