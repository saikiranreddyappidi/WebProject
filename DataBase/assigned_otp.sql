create table assigned_otp
(
    sl_no    int auto_increment
        primary key,
    reg      varchar(45)  not null,
    otp      varchar(45)  not null,
    ip       varchar(45)  not null,
    datetime datetime     not null,
    cookie   varchar(100) not null
);

