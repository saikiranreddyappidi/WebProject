create table passwordlink
(
    slno     int auto_increment,
    regno    varchar(45) not null,
    link     varchar(80) not null,
    ip       varchar(20) null,
    datetime varchar(45) not null,
    primary key (slno, regno)
);

