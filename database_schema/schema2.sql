-- ENUMERATION TABLES --

create table location_types (
    id varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_location_types primary key (id),
    constraint uc_location_types unique (id)
);
-- work station, machine pad, conference room, wfh, main entry

create table machine_types (
    id varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_machine_types primary key (id),
    constraint uc_machine_types unique (id)
);
-- cnc machine, drill press, filament winder, label laser...

create table gauge_types (
    id varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_gauge_types primary key (id),
    constraint uc_gauge_types unique (id)
);
-- caliper, bore micrometer, indicator, cmm, vision system...

create table characteristic_types (
    id varchar(25) not null,
    is_gdt boolean not null,

    -- primary key and unique constraint
    constraint pk_characteristic_types primary key (id),
    constraint uc_characteristic_types unique (id)
);
-- diameter, distance, circularity, position, surface profile...

create table specification_types (
    id varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_specification_types primary key (id),
    constraint uc_specification_types unique (id)
);


-- RECORD TABLES --

create table departments (
    id integer not null,
    name varchar(25) not null,
    description varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_departments primary key (id),
    constraint uc_departments unique (id)
);
-- manufacturing engineering, new product development, cnc, welding, fabrication, marketing, finance, data science

create table locations (
    id integer not null,
    name varchar(25) not null,
    description varchar(100) not null,

    -- primary key and unique constraint
    constraint pk_locations primary key (id),
    constraint uc_locations unique (id),

    -- one location relates to one location type
    location_type_id integer not null,
    constraint uc_location_type unique (location_type_id),
    constraint fk_location_type foreign key location_type_id references location_types.id
);
-- john doe's work station, machine pad for NKZ, conference room AB12...

create table employees (
    id integer not null,
    first_name varchar(25) not null,
    last_name varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_employees primary key (id),
    constraint uc_employees unique (id),

    -- one employee relates to one department
    department_id integer not null,
    constraint uc_department unique (department_id),
    constraint fk_department foreign key department_id references departments.id,

    -- one employee relates to one location
    location_id integer not null,
    constraint uc_location unique (location_id),
    constraint fk_location foreign key location_id references locations.id,

    -- enforce first/last name combination is always unique
    constraint uc_employee_name unique (first_name, last_name)
);
-- all the employees

create table machines (
    id integer not null,
    name varchar(25) not null,

    -- primary key and unique constraint
    constraint pk_machines primary key (id),
    constraint uc_machines unique (id),

    -- one machine relates to one machine type
    machine_type_id varchar(25) not null,
    constraint uc_machine_type unique (machine_type_id),
    constraint fk_machine_type foreign key machine_type_id references machine_types.id,

    -- one machine relates to one location
    location_id integer not null,
    constraint uc_location unique (location_id),
    constraint fk_location foreign key location_id references locations.id
);
-- all the machines for manufacturing and organization

create table parts (
    id integer not null,
    part_number varchar(25) not null,
    revision varchar(5) not null,

    -- primary key and unique constraint
    constraint pk_parts primary key (id),
    constraint uc_parts unique (id),

    -- enforce part/rev combination is always unique
    constraint uc_part unique (part_number, revision)
);

create table inspection_reports (
    id integer not null,
    day_started date not null,
    day_finished date,

    -- primary key and unique constraint
    constraint pk_inspection_reports primary key (id),
    constraint uc_inspection_reports unique (id),

    -- many inspection reports relate to one part
    part_id integer not null,
    constraint fk_part foreign key part_id references parts.id,
);

create table gauges (
    id integer not null,
    name varchar(25) not null,
    last_calibrated date not null,

    -- primary key and unique constraint
    constraint pk_gauges primary key (id),
    constraint uc_gauges unique (id),

    -- one gauge relates to one gauge type
    gauge_type_id varchar(25) not null,
    constraint uc_gauge_type unique (gauge_type_id),
    constraint fk_gauge_type foreign key gauge_type_id references gauge_types.id,

    -- one gauge can relate to one employee
    employee_id integer,
    constraint uc_employee unique (employee_id),
    constraint fk_employee foreign key employee_id references employees.id,

    -- one gauge can relate to one location
    location_id integer,
    constraint uc_location unique (location_id),
    constraint fk_location foreign key location_id references locations.id
);
-- all the gauges

create table characteristics (
    id integer not null,
    name varchar(25) not null,
    precision integer not null,
    nominal decimal not null,
    usl decimal,
    lsl decimal,
    measured decimal,

    -- primary key and unique constraint
    constraint pk_characteristics primary key (id),
    constraint uc_characteristics unique (id),

    -- many characteristics relate to one inspection report
    inspection_report_id integer not null,
    constraint fk_inspection_report foreign key inspection_report_id references inspection_reports.id,

    -- one characteristic relates to one characteristic type
    characteristic_type_id varchar(24) not null,
    constraint uc_characteristic_type unique (characteristic_type_id),
    constraint fk_characteristic_type foreign key characteristic_type_id references characteristic_types.id,

    -- one characteristic relates to one specification type
    specification_type_id varchar(25) not null,
    constraint uc_specification_type unique (specification_type_id),
    constraint fk_specification_type foreign key specification_type_id references specification_types.id
);
-- all the characteristic measurements