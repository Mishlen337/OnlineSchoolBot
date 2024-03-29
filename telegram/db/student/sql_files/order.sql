

--name: get_basket_content
select c.id as course_id, c.name as course_name, c.subject_name,
       e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname,
       ocp.package_name, ocp.old_price as price
    from order_course_package as ocp
        join students as s on ocp.student_id = s.id
        join orders as o on ocp.order_id = o.id
        join courses as c on ocp.course_id = c.id
        join employees as e on c.teacher_id = e.id
where s.tg_id = :tg_id and o.status = 'неоплачено';

--name: purchase_basket
update orders set status = 'оплачено' where student_id = :student_id and status = 'неоплачено' 

--name: _create_basket^
insert into orders(order_time, student_id) values (:order_time, :student_id)
returning id;

--name: delete_basket
delete from orders where status = 'неоплачено' and student_id = :student_id

--name: add_course_package
insert into order_course_package(order_id, student_id, course_id, package_name)
    values (:order_id, :student_id, :course_id, :package_name)

--name: _get_order_id^
select id from orders
where student_id = :student_id and status = 'неоплачено'
limit 1;

--name: _get_order_course_status^
select ocp.package_name, o.status from order_course_package as ocp
    join orders as o on ocp.order_id = o.id
where o.id = :order_id and ocp.student_id = :student_id and ocp.course_id = :course_id;

--name: get_order_course_package_message_ids
select ocp.message_id from order_course_package as ocp
    join orders as o on ocp.order_id = o.id
    join students as s on o.student_id = s.id
    where s.tg_id = :tg_id and o.status = 'неоплачено';

--name: update_order_course_package_message_ids
update order_course_package set message_id = :message_id
where order_id = :order_id
