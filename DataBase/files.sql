create table files
(
    `sl.no`   int auto_increment
        primary key,
    file_name varchar(45)  not null,
    document  longblob     null,
    link      varchar(200) null
);

