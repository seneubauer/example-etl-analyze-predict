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

