create table alreadylogin
(
    slno     int auto_increment
        primary key,
    reg      varchar(45)   not null,
    cookie   varchar(80)   not null,
    ip       varchar(20)   not null,
    datetime datetime      not null,
    enable   int default 0 not null
);

