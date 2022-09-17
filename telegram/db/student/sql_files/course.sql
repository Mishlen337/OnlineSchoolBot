--name: get_courses
select
  c.id as course_id, c.name as course_name,
  c.subject_name,
  e.name as teacher_name,
  e.patronymic as teacher_patronymic,
  e.surname as teacher_surname,
  c.begin_at,
  c.end_at,
  c.description,
  filt_o.status
from
  courses as c
  join employees as e on c.teacher_id = e.id
  left join (select o.status, ocp.course_id from order_course_package as ocp
            join orders as o on ocp.order_id = o.id
            join students as s on o.student_id = s.id
            where s.tg_id = :tg_id) as filt_o
  on c.id = filt_o.course_id
order by c.name;

--name: get_course_packages
select
  package_name
from
  course_package
where
  course_id = :course_id
order by price;

--name: get_purchased_courses
select c.id, c.name from
  orders as o join order_course_package as ocp on o.id = ocp.order_id
              join courses as c on ocp.course_id = c.id
              join students as s on o.student_id = s.id
  where o.status = 'оплачено' and s.tg_id = :tg_id

--name: get_full_and_partly_purchased_courses
select c.id as course_id, c.tg_group_link, c.name as course_name, c.begin_at,
  e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname
  from
  orders as o join order_course_package as ocp on o.id = ocp.order_id
              join courses as c on ocp.course_id = c.id
              join students as s on o.student_id = s.id
              join employees as e on c.teacher_id = e.id
  where o.status = 'оплачено' and s.tg_id = :tg_id
union
select c.id as course_id, c.tg_group_link, c.name as course_name, c.begin_at,
  e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname
  from
  purchased_webinars as pw join webinars as w on pw.webinar_id = w.id
                           join courses as c on w.course_id = c.id
                           join students as s on pw.student_id = s.id
                           join employees as e on c.teacher_id = e.id
  where s.tg_id = :tg_id;

--name: get_pro_purchased_courses
select c.id as course_id, g.tg_group_link, c.name as course_name, c.begin_at,
  e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname
  from
  orders as o join order_course_package as ocp on o.id = ocp.order_id
              join courses as c on ocp.course_id = c.id
              join students as s on o.student_id = s.id
              join employees as e on c.teacher_id = e.id
              join groups as g on c.id = g.course_id
  where o.status = 'оплачено' and s.tg_id = :tg_id and package_name = 'Групповой';

--name: get_course_groups
select id, type from groups where course_id = :course_id;

--name: group_sign_up
insert into group_student values ((select id from students where tg_id = :tg_id), :group_id);
