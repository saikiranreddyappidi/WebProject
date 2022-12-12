create table assigned_sections
(
    slno    int auto_increment
        primary key,
    fac_id  varchar(45)               not null,
    sec     varchar(45) default '18'  not null,
    subject varchar(45) default 'pps' not null
);

