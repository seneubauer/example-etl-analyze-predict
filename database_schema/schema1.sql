-- independent tables

-- table of vendors for purchased components
create table vendors (
    uid integer unique not null,
    name varchar(50) not null,
    reputation decimal,
    constraint uid_pk primary key (uid)
);

-- table of job orders for built components
create table job_orders (
    uid varchar(25) unique not null,
    parameter0 decimal,
    parameter1 integer,
    parameter2 varchar(100),
    primary key (uid)
);

create table purchase_orders (
    uid varchar(25) unique not null,
    primary key (uid)
);

create table unit_types (
    uid integer unique not null,
    name varchar(50) not null,
    constraint uid_pk primary key (uid)
)








-- table of parts
create table parts (
    uid integer unique not null,
    item_number varchar(25) not null,
    revision varchar(5) not null,
    drawing varchar(25),
    primary key (uid),
    constraint part_uid unique (item_number, drawing)
);

-- table of materials used to make parts
create table materials (
    uid integer unique not null,
    name varchar(50) not null,
    part_uid integer not null,
    primary key (uid),
    constraint foreign key (part_uid) references parts.uid
);

