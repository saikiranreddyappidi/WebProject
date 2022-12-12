create table active_users
(
    Slno       int auto_increment
        primary key,
    faculty_id varchar(45)                   not null,
    cookie     varchar(100)                  not null,
    login_ip   varchar(45) default '0.0.0.0' not null
);

