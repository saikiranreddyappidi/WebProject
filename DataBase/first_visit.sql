create table first_visit
(
    slno     int auto_increment
        primary key,
    reg      varchar(45) default '0' not null,
    cookie   varchar(80)             not null,
    ip       varchar(45)             not null,
    datetime datetime                not null
);

