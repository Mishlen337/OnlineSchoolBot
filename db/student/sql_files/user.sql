
--name: tg_auth
insert into students(tg_id) values (:tg_id);

--name: info_init
-- Inserting extra information about student
with updated as (
update students set email = :email, name = :name,
                    patronymic = :patronymic, surname = :surname,
                    class_num = :class_num
                where tg_id = :tg_id
)

--name: get_id^
select id from students
where tg_id = :tg_id;
