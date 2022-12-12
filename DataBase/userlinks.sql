create table userlinks
(
    slno      int auto_increment
        primary key,
    reg       varchar(45)    not null,
    sec       int default 18 null,
    filename  varchar(45)    not null,
    file_type varchar(45)    not null,
    link      varchar(350)   not null,
    datetime  datetime       not null,
    subject   varchar(45)    not null,
    comment   longtext       null
);

