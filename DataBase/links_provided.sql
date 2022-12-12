create table links_provided
(
    sl_no       int auto_increment
        primary key,
    faculty_id  varchar(45)                     not null,
    file_name   varchar(45)                     not null,
    drive_links varchar(100)                    not null,
    branch      varchar(45)                     not null,
    file_type   varchar(45)                     not null,
    datetime    datetime                        null,
    facultyname varchar(45) default 'Jhon' null
);

