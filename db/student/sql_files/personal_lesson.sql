
--name: get_available_teachers
select e.name, e.patronymic, e.surname, es.subject_name, es.individual_price
    from employee_subject as es
        join employees as e on es.employee_id = e.id
where es.role = 'personal_teacher' and es.available = True;
