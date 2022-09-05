
--name: tg_auth
insert into students(tg_id) values (:tg_id);

-- Inserting extra information about student
--name: telephone_init
update students set telephone = :telephone
where tg_id = :tg_id;

--name: fio_init
update students set name = :name,
                    patronymic = :patronymic, surname = :surname
                where tg_id = :tg_id;

--name: class_num_init
update students set class_num = :class_num
                where tg_id = :tg_id;


--name: get_id^
select id from students
where tg_id = :tg_id
limit 1;

--name: get_user_info^
select * from students where tg_id = :tg_id;
