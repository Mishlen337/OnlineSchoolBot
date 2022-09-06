--name: get_user_tg_id^
select tg_id from employees where id = :employee_id;
