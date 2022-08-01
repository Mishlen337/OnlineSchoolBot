--name: get_courses
select
  c.id as course_id, c.name as course_name,
  c.subject_name,
  e.name as teacher_name,
  e.patronymic as teacher_patronymic,
  e.surname as teacher_surname,
  c.begin_at,
  c.end_at,
  filt_o.status
from
  courses as c
  join employees as e on c.teacher_id = e.id
  left join (select o.status, ocp.course_id from order_course_package as ocp
            join orders as o on ocp.order_id = o.id
            join students as s on o.student_id = s.id
            where s.tg_id = :tg_id) as filt_o
  on c.id = filt_o.course_id;

--name: get_course_packages
select
  package_name
from
  course_package
where
  course_id = :course_id;