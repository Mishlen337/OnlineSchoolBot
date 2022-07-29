--name get_courses
select
  c.id as course_id as c.name as course_name,
  c.course_subject_name,
  e.name as teacher_name,
  e.patronymic as teacher_patronymic,
  e.surname as teacher_surname,
  c.begin_at,
  end_at,
  o.status
from
  courses as c
  join employees on c.teacher_id = e.id
  left join order_course_package as ocp on c.id = ocp.course_id
  join orders as on ocp.order_id = o.id
  join students as s on o.student_id = s.id
where
  s.tg_id =: tg_id --name get_course_packages
select
  package_name
from
  course_package
where
  course_id =: course_id