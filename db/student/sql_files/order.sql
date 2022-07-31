

--name: get_basket_content
select c.name as course_name, c.subject_name as course_subject_name,
       e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname,
       ocp.package_name, ocp.old_price as price
    from order_course_package as ocp
        join students as s on ocp.student_id = s.id
        join orders as o on ocp.order_id = o.id
        join courses as c on ocp.course_id = c.id
        join employees as e on c.teacher_id = e.id
where s.tg_id = :tg_id and o.status = 'неоплачено';

--name: _create_basket
insert into orders(order_time, student_id) values (:order_time, :student_id)
returning id;

--name: delete_basket
delete from orders where status = 'неоплачено' and student_id = :student_id

--name: add_course_package
insert into order_course_package(order_id, student_id, course_id, package_name, old_price)
    values (:order_id, :student_id, :course_id, :package_name, :old_price)

--name _get_order_id^
select o.id from orders as o
    join students as s on o.student_id
where s.tg_id = :tg_id
