create table gauge_types (
    uid integer unique not null,
    name varchar(25) not null,
    primary key (uid)
);

create table characteristic_types (
    uid integer unique not null,
    name varchar(25) not null,
    is_gdt boolean not null,
    primary key (uid)
);

create table gauges (
    uid varchar(25) unique not null,
    location varchar(25) not null,
    type_uid integer not null,
    foreign key (type_uid) references gauge_types.uid,
    primary key (uid)
);

create table parts (
    drawing varchar(25) not null,
    revision varchar(5) not null,
    item varchar(25) not null,
    primary key (drawing, revision, item)
);

create table characteristics (
    uid integer unique not null,
    name varchar(25) not null,
    nominal decimal not null,
    usl decimal not null,
    lsl decimal not null,
    type_uid integer not null,
    gauge_uid integer not null,
    part_drawing varchar(25) not null,
    part_revision varchar(5) not null,
    part_item varchar(25) not null,
    foreign key (type_uid) references characteristic_types.uid,
    foreign key (gauge_uid) references gauges.uid,
    foreign key (part_drawing, part_revision, part_item) references (parts.drawing, parts.revision, parts.item),
    primary key (uid)
);