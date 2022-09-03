--name: auth_employee
update employees set tg_id = :tg_id where telephone = :telephone RETURNING *;
