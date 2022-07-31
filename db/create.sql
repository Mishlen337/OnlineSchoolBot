

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY key,
    email varchar(255) not null unique,
    tg_id BIGINT unique,
    name varchar(50) not null,
    patronymic varchar(50),
    surname varchar(50) not null,
    telephone char(11) not null,
    description varchar(1000)
);

create table if not exists subjects (
    name varchar(50) PRIMARY key
);

create table if not exists employee_roles (
    role varchar(50) PRIMARY key
);

insert into employee_roles values ('course_teacher');
insert into employee_roles values ('personal_teacher');

create table IF not EXISTS employee_subject (
    employee_id integer not null CONSTRAINT fk_employee REFERENCES employees(id) on delete RESTRICT,
    subject_name varchar (50) not null CONSTRAINT fk_subject REFERENCES subjects(name) on delete RESTRICT,
    role varchar (50) not null CONSTRAINT fk_role REFERENCES employee_roles(role) on delete RESTRICT,
    available boolean,
    individual_price integer,
    primary key (employee_id, subject_name, role),
    CONSTRAINT check_individual_price((role = personal_teacher and available is not null and individual_price is not null) or
                                       role !=  personal_teacher and available is null and individual_price is null)
);


create table if not EXISTS students (
    id serial PRIMARY key,
    email varchar(255) unique,
    tg_id BIGINT not null unique,
    name varchar(50),
    patronymic varchar(50),
    surname varchar(50),
    class_num SMALLINT constraint class_num_check check(class_num >= 1 and (class_num <= 11))
);

create TABLE if not exists personal_lessons (
    id serial primary key,
    teacher_id integer not null,
    subject_name varchar(50) not null,
    role VARCHAR(50) not null constraint role_check check(role = 'personal_teacher'),
    student_id integer not null CONSTRAINT fk_student REFERENCES students(id) ON delete restrict,
    begin_at timestamp not null,
    end_at timestamp not null,
    price integer not null,
    status varchar(11) constraint status_check check (status in ('согласовано', 'оплачено')) DEFAULT 'согласовано',
    broadcast_link text,
    material_link text,
    record_link text,
    homework_link text,
    done_homework_file_id bigint,
    assistant_id integer constraint fk_employee REFERENCES employees(id) on delete set null,
    hometask_status varchar(9) CONSTRAINT hometask_status_check check(hometask_status in ('cдано', 'назначено', 'проверено')),
    CONSTRAINT fk_employee_subject FOREIGN KEY (teacher_id, subject_name, role) REFERENCES employee_subject(employee_id, subject_name, role),
    CONSTRAINT date_check check (begin_at < end_at);
);

create or replace function check_personal_lesson_intersection() returns trigger AS $$
DECLARE
    count_personal_lesson_intersects integer;
    count_webinar_intersects integer;
BEGIN
    SELECT count(*) FROM personal_lessons WHERE teacher_id = new.teacher_id AND
                                             (begin_at <= new.begin_at AND end_at >= new.begin_at
                                              or 
                                              begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_personal_lesson_intersects;

   SELECT count(*) FROM webinars AS w JOIN courses as c ON w.course_id = c.id 
                                where c.teacher_id = new.teacher_id and 
                                      (w.begin_at <= new.begin_at AND w.end_at >= new.begin_at
                                       or
                                       w.begin_at >= new.begin_at and w.begin_at <= new.end_at)
        into count_webinar_intersects;
    
    if count_personal_lesson_intersects > 0 THEN
        RAISE EXCEPTION 'Personal lesson intersects with other personal lessons. teacher id: %', new.teacher_id
            USING ERRCODE = '09001';
        return null;
    end if;
    if count_webinar_intersects > 0 then
        RAISE EXCEPTION 'Personal lesson intersects with webinars. teacher id: %', new.teacher_id
            USING ERRCODE = '09002';
        return null;
    end if;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tr_check_personal_lesson_intersection
before INSERT OR UPDATE ON personal_lessons FOR EACH ROW
EXECUTE PROCEDURE check_personal_lesson_intersection();

create or replace function add_personal_lesson_price() returns trigger AS $$
BEGIN
    select individual_price from employee_subject where employee_id = new.teacher_id 
                                                        and subject_name = new.subject_name
                                                        and role = new.role
        limit 1
        into new.price;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tr_add_personal_lesson_price
before INSERT ON personal_lessons FOR EACH ROW
EXECUTE PROCEDURE add_personal_lesson_price();

create table if not exists courses (
    id serial PRIMARY key,
    name VARCHAR(255) not null,
    begin_at date not null,
    end_at date not null,
    description text,
    tg_group_link text,
    teacher_id integer not null,
    subject_name varchar(50) not null,
    role VARCHAR(50) not null constraint role_check check(role = 'course_teacher'),
    CONSTRAINT fk_employee_subject FOREIGN KEY (teacher_id, subject_name, role) REFERENCES employee_subject(employee_id, subject_name, role) on delete restrict
);

create table if not exists packages (
    name varchar(50) primary key,
    description text
);

insert into packages values ('про');
insert into packages values ('стандарт');

create table if not exists course_package (
    course_id integer not null CONSTRAINT fk_course references courses(id) on delete restrict,
    package_name varchar(50) not null CONSTRAINT fk_package REFERENCES packages(name) on delete restrict,
    price integer not null,
    PRIMARY key (course_id, package_name)
);



create table if not exists orders (
    id serial primary key,
    order_time TIMESTAMP not null,
    status varchar(10) not null constraint status_check check (status in ('неоплачено', 'оплачено'))
                        default 'неоплачено',
    student_id integer not null CONSTRAINT fk_student REFERENCES students(id) on delete restrict,
    constraint id_student_id_unique UNIQUE (id, student_id)
);

create unique index if not exists unique_not_purchased_status on orders(status, student_id) where status = 'неоплачено';

create or replace function fill_purchased_webinars() returns trigger AS $$
DECLARE
    w_id integer;
BEGIN
    IF new.status = 'оплачено' then
        FOR w_id in select w.id from order_course_package as ocp
                        join courses as c on ocp.course_id = c.id
                        join webinars as w on w.course_id = c.id
                where ocp.order_id = new.id and ocp.student_id = new.student_id
        LOOP
            BEGIN
                INSERT INTO purchased_webinars(webinar_id, student_id) VALUES (w_id, new.student_id);
                EXCEPTION
                WHEN unique_violation THEN RAISE NOTICE 'webinar: % has been already purchased by student_id: %', w_id, new.id;
            END;
        END LOOP;
    END IF;
    return null;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_fill_purchased_webinars after
INSERT OR UPDATE
  ON orders FOR EACH ROW
EXECUTE
  PROCEDURE fill_purchased_webinars();


create table if not exists order_course_package (
    id serial primary key,
    order_id integer not null,
    student_id integer not null,
    course_id integer not null,
    package_name varchar(50) not null,
    old_price integer not null,
    CONSTRAINT fk_order foreign key (order_id, student_id) REFERENCES orders(id, student_id) on delete CASCADE,
    CONSTRAINT fk_course_package FOREIGN key (course_id, package_name) REFERENCES course_package(course_id, package_name),
    CONSTRAINT student_id_course_id_unique UNIQUE (student_id, course_id)
);

create table if not exists webinars (
    id serial primary key,
    theme varchar(256) not null,
    course_id integer constraint fk_course REFERENCES courses (id),
    begin_at timestamp,
    end_at timestamp,
    format varchar(6) not null constraint format_check check (format in ('запись', 'онлайн')),
    broadcast_link text,
    material_link text,
    record_link text,
    homework_link text,
    CONSTRAINT format_restrictions_check CHECK (
        format = 'онлайн' and begin_at is not null and end_at is not null or format = 'запись' and record_link is not null),
    CONSTRAINT date_check check (begin_at is not null and end_at is not null and begin_at < end_at)
);

create or replace function check_webinar_intersection() returns trigger AS $$
DECLARE
    st integer;
    webinar_teacher_id integer;
    count_personal_lesson_intersects integer;
    count_webinar_intersects integer;
BEGIN
    SELECT teacher_id from courses where id = new.course_id into webinar_teacher_id;
    SELECT count(*) FROM personal_lessons WHERE teacher_id = webinar_teacher_id AND
                                             (begin_at <= new.begin_at AND end_at >= new.begin_at
                                              or 
                                              begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_personal_lesson_intersects;
    SELECT count(*) FROM webinars where course_id = new.course_id and 
                                      (begin_at <= begin_at AND end_at >= new.begin_at
                                       or
                                       begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_webinar_intersects;
    if count_personal_lesson_intersects > 0 then
        RAISE exception 'Webinar intersects with personal lessons. teacher id: %', webinar_teacher_id
            USING ERRCODE = '09003';
        return null;
    end IF;
    if count_webinar_intersects > 1 then
        RAISE exception 'Webinar intersects with other webinars. teacher id: %', webinar_teacher_id
            USING ERRCODE = '09004';
        return null;
    end if;
    FOR st in select ocp.student_id from order_course_package as ocp join orders as o on ocp.order_id = o.id
               where o.status = 'оплачено' and course_id = new.course_id
    LOOP
        BEGIN
            INSERT INTO purchased_webinars(webinar_id, student_id) VALUES (new.id, st);
        EXCEPTION
            WHEN unique_violation
                THEN RAISE NOTICE 'webinar has been already purchased by student_id: %', st;
        end;
    END LOOP;
    return null;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_check_webinar_intersection after
INSERT or UPDATE
  ON webinars FOR EACH ROW
EXECUTE
  PROCEDURE check_webinar_intersection();

