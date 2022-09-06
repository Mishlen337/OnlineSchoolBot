

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY key,
    tg_id BIGINT unique,
    name varchar(50) not null,
    patronymic varchar(50),
    surname varchar(50) not null,
    telephone varchar(50) not null unique,
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
insert into employee_roles values ('assistant');

create table IF not EXISTS employee_subject (
    employee_id integer not null CONSTRAINT fk_employee REFERENCES employees(id) on delete RESTRICT,
    subject_name varchar (50) not null CONSTRAINT fk_subject REFERENCES subjects(name) on delete RESTRICT,
    role varchar (50) not null CONSTRAINT fk_role REFERENCES employee_roles(role) on delete RESTRICT,
    available boolean,
    individual_price integer,
    description text,
    primary key (employee_id, subject_name, role),
    CONSTRAINT check_individual_price
    CHECK((role = 'personal_teacher' and available is not null and individual_price is not null) or
          role != 'personal_teacher' and available is null and individual_price is null)
);


create table if not EXISTS students (
    id serial PRIMARY key,
    telephone varchar(50) unique,
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
    homework_deadline_time timestamp,
    CONSTRAINT fk_employee_subject FOREIGN KEY (teacher_id, subject_name, role) REFERENCES employee_subject(employee_id, subject_name, role),
    CONSTRAINT date_check check (begin_at < end_at)
);

create or replace function check_personal_lesson_intersection() returns trigger AS $$
DECLARE
    count_personal_lesson_intersects integer;
    count_group_lesson_intersects integer;
    count_webinar_intersects integer;
BEGIN
    SELECT count(*) FROM personal_lessons WHERE teacher_id = new.teacher_id AND
                                             (begin_at <= new.begin_at AND end_at >= new.begin_at
                                              or 
                                              begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_personal_lesson_intersects;

    SELECT count(*) FROM group_lessons as gl
            join groups as g on gl.group_id = g.id
            join courses as c on g.course_id = c.id
        where c.teacher_id = new.teacher_id and
                                              (gl.begin_at <= new.begin_at AND gl.end_at >= new.begin_at
                                              or 
                                              gl.begin_at >= new.begin_at and gl.begin_at <= new.end_at)
        into count_group_lesson_intersects;

   SELECT count(*) FROM webinars AS w JOIN courses as c ON w.course_id = c.id 
                                where c.teacher_id = new.teacher_id and 
                                      (w.begin_at <= new.begin_at AND w.end_at >= new.begin_at
                                       or
                                       w.begin_at >= new.begin_at and w.begin_at <= new.end_at)
        into count_webinar_intersects;
    
    if count_personal_lesson_intersects > 1 THEN
        RAISE EXCEPTION 'Personal lesson intersects with other personal lessons. teacher id: %', new.teacher_id
            USING ERRCODE = '09001';
        return null;
    end if;

    if count_group_lesson_intersects > 0 THEN
        RAISE EXCEPTION 'Personal lesson intersects with group lessons. teacher id: %', new.teacher_id
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
after INSERT OR UPDATE ON personal_lessons FOR EACH ROW
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
    CONSTRAINT fk_employee_subject FOREIGN KEY (teacher_id, subject_name, role) REFERENCES employee_subject(employee_id, subject_name, role) on delete restrict,
    CONSTRAINT id_subject_name_unique UNIQUE(id, subject_name)
);

create table if not exists packages (
    name varchar(50) primary key,
    description text
);

insert into packages values ('Based');
insert into packages values ('Групповой');
insert into packages values ('Индивидуальный')

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
    message_id numeric(31),
    CONSTRAINT fk_order foreign key (order_id, student_id) REFERENCES orders(id, student_id) on delete CASCADE,
    CONSTRAINT fk_course_package FOREIGN key (course_id, package_name) REFERENCES course_package(course_id, package_name),
    CONSTRAINT student_id_course_id_unique UNIQUE (student_id, course_id)
);

create or replace function add_course_package_price() returns trigger AS $$
BEGIN
    select price from course_package
        where course_id = new.course_id and package_name = new.package_name
    limit 1
    into new.old_price;
    if new.old_price is null then
        new.old_price = 0;
    end if;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_add_course_package_price before
INSERT
  ON order_course_package FOR EACH ROW
EXECUTE
  PROCEDURE add_course_package_price();

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
    homework_deadline_time timestamp,
    CONSTRAINT format_restrictions_check CHECK (
        format = 'онлайн' and begin_at is not null and end_at is not null and begin_at < end_at
            or format = 'запись' and record_link is not null)
);

create or replace function check_webinar_intersection() returns trigger AS $$
DECLARE
    st integer;
    webinar_teacher_id integer;
    count_personal_lesson_intersects integer;
    count_group_lesson_intersects integer;
    count_webinar_intersects integer;
    w record;
BEGIN
    -- intersections
    SELECT teacher_id from courses where id = new.course_id into webinar_teacher_id;
    SELECT count(*) FROM personal_lessons WHERE teacher_id = webinar_teacher_id AND
                                             (begin_at <= new.begin_at AND end_at >= new.begin_at
                                              or 
                                              begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_personal_lesson_intersects;
    
    SELECT count(*) FROM group_lessons as gl
            join groups as g on gl.group_id = g.id
            join courses as c on g.course_id = c.id
        where c.teacher_id = webinar_teacher_id and
                                              (gl.begin_at <= new.begin_at AND gl.end_at >= new.begin_at
                                              or 
                                              gl.begin_at >= new.begin_at and gl.begin_at <= new.end_at)
        into count_group_lesson_intersects;
    

    SELECT count(*) FROM webinars where course_id in (select id from courses where teacher_id=webinar_teacher_id) and 
                                      (begin_at <= new.begin_at AND end_at >= new.begin_at
                                       or
                                       begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_webinar_intersects;

    if count_personal_lesson_intersects > 0 then
        RAISE exception 'Webinar intersects with personal lessons. teacher id: %', webinar_teacher_id
            USING ERRCODE = '09003';
        return null;
    end IF;

    if count_group_lesson_intersects > 0 then 
        RAISE exception 'Webinar intersects with gropup lessons. teacher id: %', webinar_teacher_id
            USING ERRCODE = '09003';
        return null;
    end IF;

    if count_webinar_intersects > 1 then
        RAISE exception 'Webinar intersects with other webinars. teacher id: %', webinar_teacher_id
            USING ERRCODE = '09004';
        return null;
    end if;
    -- adding to purchase webinars
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
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_check_webinar_intersection after
INSERT or UPDATE
  ON webinars FOR EACH ROW
EXECUTE
  PROCEDURE check_webinar_intersection();

create table if not exists purchased_webinars (
    webinar_id integer CONSTRAINT fk_webinar REFERENCES webinars(id),
    student_id integer CONSTRAINT fk_student REFERENCES students(id),
    primary key(webinar_id, student_id)
);

create table if not exists course_assistings (
    id serial primary key,
    assistant_id integer not null,
    assistant_subject_name varchar(50) not null,
    assistant_role VARCHAR(50) not null constraint role_check check(assistant_role = 'assistant'),
    course_id integer not null,
    course_subject_name varchar(50) not null,
    available boolean not null default true,
    CONSTRAINT fk_course FOREIGN KEY(course_id, course_subject_name)
        REFERENCES courses(id, subject_name) on delete restrict,
    CONSTRAINT fk_employee_subject FOREIGN KEY (assistant_id, assistant_subject_name, assistant_role)
        REFERENCES employee_subject(employee_id, subject_name, role) on delete restrict,
    CONSTRAINT subject_name_check CHECK(assistant_subject_name = course_subject_name),
    CONSTRAINT assistant_id_course_id_unique UNIQUE(assistant_id, course_id)
);

create table if not exists done_webinars_homework (
    id serial primary key,
    webinar_id integer not null,
    student_id integer not null,
    assistant_id integer not null,
    course_id integer not null,
    done_homework_file_id text not null,
    done_homework_time TIMESTAMP not null,
    checked_homework_file_id text,
    CONSTRAINT fk_purchased_webinars FOREIGN KEY (webinar_id, student_id) REFERENCES purchased_webinars(webinar_id, student_id),
    CONSTRAINT fk_course_assistings FOREIGN KEY (assistant_id, course_id) REFERENCES course_assistings(assistant_id, course_id),
    CONSTRAINT webinar_id_student_id_unique UNIQUE (webinar_id, student_id)
);

create or replace function preprocessing_done_webinars_homework() returns trigger AS $$
DECLARE
    min_assistant_homeworks integer;
    webinar_course_id integer;
BEGIN
    new.done_homework_time := NOW();

    IF new.assistant_id is NULL AND new.course_id is NULL THEN
        select course_id from webinars where id = new.webinar_id into webinar_course_id;
        new.course_id := webinar_course_id;
        select min(assistings_count.count) from
            (select count(*) as count from course_assistings as ca
                LEFT JOIN done_webinars_homework as dwh ON ca.assistant_id = dwh.assistant_id and ca.course_id = dwh.course_id
            where ca.course_id = webinar_course_id and ca.available = True GROUP BY ca.assistant_id)
                as assistings_count
        into min_assistant_homeworks;
        IF min_assistant_homeworks is NULL then
            RAISE exception 'No assistants can check the homework or no such webinar'
                USING ERRCODE = '09005';
            return null;
        END IF;
        select ca.assistant_id from course_assistings as ca
            LEFT JOIN done_webinars_homework as dwh ON ca.assistant_id = dwh.assistant_id and ca.course_id = dwh.course_id
        where ca.course_id = webinar_course_id and ca.available = True  GROUP BY ca.assistant_id HAVING count(*) = min_assistant_homeworks
        limit 1 into new.assistant_id;
    END IF;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_preprocessing_done_webinars_homework before
INSERT
  ON done_webinars_homework FOR EACH ROW
EXECUTE
  PROCEDURE preprocessing_done_webinars_homework();

create or replace function check_webinar_done_homework_time() returns trigger AS $$
DECLARE
    homework_deadline_time_var TIMESTAMP;
BEGIN
    select homework_deadline_time from webinars where id = new.webinar_id
        into homework_deadline_time_var;
    IF homework_deadline_time_var is not null and new.done_homework_time > homework_deadline_time_var then
        RAISE exception 'Done homework time more than webinars deadline time: %', homework_deadline_time_var
            USING ERRCODE = '09000';
        return null;
    end IF;
    return null;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_check_webinar_done_homework_time after
INSERT
  ON done_webinars_homework FOR EACH ROW
EXECUTE
  PROCEDURE check_webinar_done_homework_time();


create table if not exists personal_assistings (
    id serial PRIMARY KEY,
    teacher_id integer not null,
    teacher_subject_name varchar(50) not null,
    teacher_role varchar(50) not null constraint teacher_role_check check(teacher_role = 'personal_teacher'),
    assistant_id integer not null,
    assistant_subject_name varchar(50) not null,
    assistant_role varchar(50) not null constraint assistant_role_check check(assistant_role = 'assistant'),
    available boolean not null default true,
    
    CONSTRAINT fk_assistant_employee_subject FOREIGN KEY (assistant_id, assistant_subject_name, assistant_role)
        REFERENCES employee_subject(employee_id, subject_name, role) on delete restrict,
    CONSTRAINT fk_teacher_employee_subject FOREIGN KEY (teacher_id, teacher_subject_name, teacher_role)
        REFERENCES employee_subject(employee_id, subject_name, role) on delete restrict,
    CONSTRAINT subject_check CHECK (teacher_subject_name = assistant_subject_name),
    CONSTRAINT teacher_id_teacher_subject_name_assistant_id_unique
        UNIQUE (teacher_id, teacher_subject_name, assistant_id)
);


create table if not exists done_personal_lessons_homework (
    id serial primary key,
    personal_lesson_id integer not null CONSTRAINT fk_personal_lesson_id REFERENCES personal_lessons (id),
    done_homework_file_id text not null,
    done_homework_time timestamp not null,
    personal_assisting_id integer not null CONSTRAINT fk_personal_assisting_id REFERENCES personal_assistings (id),
    checked_homework_file_id text,
    CONSTRAINT personal_lesson_id_unique UNIQUE (personal_lesson_id)
);

create or replace function preprocessing_done_personal_lessons_homework() returns trigger AS $$
DECLARE
    min_assistant_homeworks integer;
    personal_lesson_info record;
BEGIN
    new.done_homework_time := NOW();
    select teacher_id, subject_name from personal_lessons
        where id = new.personal_lesson_id into personal_lesson_info;
    IF new.personal_assisting_id is NULL THEN
        select min(assistings_count.count) from
            (select count(*) as count from personal_assistings as pa
                LEFT JOIN
                    (select * from done_personal_lessons_homework as dplh
                        JOIN personal_lessons as pl ON dplh.personal_lesson_id = pl.id) as edplh ON 
                pa.id = edplh.personal_assisting_id
            where pa.teacher_id = personal_lesson_info.teacher_id 
                AND pa.teacher_subject_name = personal_lesson_info.subject_name and pa.available = True
                    GROUP BY pa.assistant_id)
            as assistings_count
        into min_assistant_homeworks;
        IF min_assistant_homeworks is NULL then
            RAISE exception 'No assistants can check the homework or no such personal lesson'
                USING ERRCODE = '09005';
            return null;
        END IF;
        select pa.id from personal_assistings as pa
                LEFT JOIN
                    (select * from done_personal_lessons_homework as dplh
                        JOIN personal_lessons as pl ON dplh.personal_lesson_id = pl.id) as edplh ON 
                pa.id = edplh.personal_assisting_id
            where pa.teacher_id = personal_lesson_info.teacher_id 
                AND pa.teacher_subject_name = personal_lesson_info.subject_name and pa.available = True
                    GROUP BY pa.assistant_id, pa.id
            HAVING count(*) = min_assistant_homeworks
        limit 1 into new.personal_assisting_id;
    END IF;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_preprocessing_done_personal_lessons_homework before
INSERT
  ON done_personal_lessons_homework FOR EACH ROW
EXECUTE
  PROCEDURE preprocessing_done_personal_lessons_homework();


create or replace function check_personal_lesson_done_homework_time() returns trigger AS $$
DECLARE
    homework_deadline_time_var TIMESTAMP;
BEGIN
    select homework_deadline_time from personal_lessons where id = new.personal_lesson_id
        into homework_deadline_time_var;
    IF homework_deadline_time_var is not null and new.done_homework_time > homework_deadline_time_var then
        RAISE exception 'Done homework time more than webinars deadline time: %', homework_deadline_time_var
            USING ERRCODE = '09000';
        return null;
    end IF;
    return null;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_check_personal_lesson_done_homework_time after
INSERT
  ON done_personal_lessons_homework FOR EACH ROW
EXECUTE
  PROCEDURE check_personal_lesson_done_homework_time();



create table if not exists group_types (
    type varchar(50) primary key
);

create table if not exists groups (
    id serial primary key,
    type varchar(50) not null constraint fk_groups REFERENCES group_types(type),
    course_id integer not null constraint fk_courses REFERENCES courses(id),
    tg_group_link text,
    CONSTRAINT course_id_type_unique UNIQUE(course_id, type)
);

create table if not exists group_student (
    student_id integer not null CONSTRAINT fk_students REFERENCES students(id),
    group_id integer not null CONSTRAINT fk_groups REFERENCES groups(id),
    PRIMARY KEY (student_id, group_id)
);

create or replace function group_membership_check() returns trigger AS $$
DECLARE
    course_pro_purchase integer;
BEGIN
    select count(*) from groups as g
        join courses as c on g.course_id = c.id
        join order_course_package as ocp on c.id = ocp.course_id
        join orders as o on ocp.order_id = o.id
    where o.status = 'оплачено' and o.student_id = new.student_id and
          g.id = new.group_id and ocp.package_name = 'Групповой' into course_pro_purchase;
    IF course_pro_purchase = 0 then
        RAISE exception 'student is not allowed to be in this group' USING ERRCODE = '09000';
        return null;
    END IF;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_group_membership_check before 
INSERT OR UPDATE
  ON group_student FOR EACH ROW
EXECUTE
  PROCEDURE group_membership_check();

create table if not exists group_lessons (
    id serial primary key,
    theme varchar(255) not null ,
    group_id integer not null constraint fk_groups REFERENCES groups(id),
    begin_at TIMESTAMP not null,
    end_at TIMESTAMP not null,
    broadcast_link text,
    material_link text,
    record_link text,
    homework_link text,
    homework_deadline_time timestamp,
    CONSTRAINT date_check CHECK (begin_at < end_at)
);


create or replace function check_group_lessons_intersection() returns trigger AS $$
DECLARE
    st integer;
    group_teacher_id integer;
    count_personal_lesson_intersects integer;
    count_webinar_intersects integer;
    w record;
BEGIN
    SELECT c.teacher_id from groups as g 
        join courses as c on g.course_id = c.id where g.id = new.group_id into group_teacher_id;

    SELECT count(*) FROM personal_lessons WHERE teacher_id = group_teacher_id AND
                                             (begin_at <= new.begin_at AND end_at >= new.begin_at
                                              or 
                                              begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_personal_lesson_intersects;

    SELECT count(*) FROM webinars where course_id in (select id from courses where teacher_id=group_teacher_id) and 
                                      (begin_at <= new.begin_at AND end_at >= new.begin_at
                                       or
                                       begin_at >= new.begin_at and begin_at <= new.end_at)
        into count_webinar_intersects;

    if count_personal_lesson_intersects > 0 then
        RAISE exception 'Webinar intersects with personal lessons. teacher id: %', group_teacher_id
            USING ERRCODE = '09003';
        return null;
    end IF;

    if count_webinar_intersects > 0 then
        RAISE exception 'Webinar intersects with other webinars. teacher id: %', group_teacher_id
            USING ERRCODE = '09004';
        return null;
    end if;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_check_group_lessons_intersection after
INSERT or UPDATE
  ON group_lessons FOR EACH ROW
EXECUTE
  PROCEDURE check_group_lessons_intersection();


create table if not exists done_group_homework(
    id serial primary key,
    group_id integer not null,
    student_id integer not null,
    group_lesson_id integer not null,
    assistant_id integer not null,
    course_id integer not null,
    done_homework_file_id text not null,
    done_homework_time TIMESTAMP not null,
    checked_homework_file_id text,
    constraint fk_group_student FOREIGN KEY (group_id, student_id)
        REFERENCES group_student(group_id, student_id),
    CONSTRAINT fk_course_assistings FOREIGN KEY (assistant_id, course_id) REFERENCES course_assistings(assistant_id, course_id),
    CONSTRAINT group_lesson_id_student_id_unique UNIQUE (group_lesson_id, student_id)
);


create or replace function preprocessing_done_group_homework() returns trigger AS $$
DECLARE
    min_assistant_homeworks integer;
    group_course_id integer;
BEGIN
    new.done_homework_time := NOW();

    IF new.assistant_id is NULL AND new.course_id is NULL THEN
        select g.course_id from group_lessons as gl
            join groups as g on gl.group_id = g.id
            where gl.id = new.group_lesson_id into group_course_id;

        new.course_id := group_course_id;
        select min(assistings_count.count) from
            (select count(*) as count from course_assistings as ca
                LEFT JOIN done_group_homework as dgh ON ca.assistant_id = dgh.assistant_id and ca.course_id = dgh.course_id
            where ca.course_id = group_course_id and ca.available = True GROUP BY ca.assistant_id)
                as assistings_count
        into min_assistant_homeworks;
        IF min_assistant_homeworks is NULL then
            RAISE exception 'No assistants can check the homework or no such group lesson'
                USING ERRCODE = '09005';
            return null;
        END IF;
        select ca.assistant_id from course_assistings as ca
            LEFT JOIN done_group_homework as dgh ON ca.assistant_id = dgh.assistant_id and ca.course_id = dgh.course_id
        where ca.course_id = group_course_id and ca.available = True  GROUP BY ca.assistant_id HAVING count(*) = min_assistant_homeworks
        limit 1 into new.assistant_id;
    END IF;
    return new;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_preprocessing_done_group_homework before
INSERT
  ON done_group_homework FOR EACH ROW
EXECUTE
  PROCEDURE preprocessing_done_group_homework();

create or replace function check_group_lesson_done_homework_time() returns trigger AS $$
DECLARE
    homework_deadline_time_var TIMESTAMP;
BEGIN
    select homework_deadline_time from group_lessons where id = new.group_lesson_id
        into homework_deadline_time_var;
    IF homework_deadline_time_var is not null and new.done_homework_time > homework_deadline_time_var then
        RAISE exception 'Done homework time more than webinars deadline time: %', homework_deadline_time_var
            USING ERRCODE = '09000';
        return null;
    end IF;
    return null;
END;
$$ LANGUAGE plpgsql;

CREATE
OR REPLACE TRIGGER tr_check_group_lesson_done_homework_time after
INSERT
  ON done_group_homework FOR EACH ROW
EXECUTE
  PROCEDURE check_group_lesson_done_homework_time();
