create table active_otps
(
    sl_no    int auto_increment
        primary key,
    reg      varchar(45)   not null,
    otp      varchar(45)   not null,
    ip       varchar(45)   not null,
    datetime varchar(45)   not null,
    cookie   varchar(100)  not null,
    `limit`  int default 0 not null
);

