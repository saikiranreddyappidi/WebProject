create table temp_cookie
(
    slno        int auto_increment
        primary key,
    reg         varchar(45) not null,
    cookievalue varchar(80) not null,
    ip          varchar(45) not null,
    datetime    datetime    not null
);

