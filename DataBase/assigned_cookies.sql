create table assigned_cookies
(
    id       bigint auto_increment
        primary key,
    reg      varchar(45)  not null,
    cookies  varchar(100) not null,
    datetime datetime     null
);

