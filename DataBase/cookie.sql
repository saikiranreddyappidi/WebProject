create table cookie
(
    slno        int auto_increment
        primary key,
    regno       varchar(45)                    not null,
    cookievalue varchar(100) default '1729'    not null,
    ip          varchar(45)  default '0.0.0.0' not null,
    datetime    datetime                       null
)
    comment 'To store cookies ';

