create table apporved_files
(
    slno        int auto_increment
        primary key,
    regno       varchar(45)   not null,
    file_name   varchar(45)   not null,
    file_type   varchar(45)   not null,
    file_link   varchar(350)  not null,
    subject     varchar(45)   not null,
    stu_comment longtext      null,
    apporved_by varchar(45)   not null,
    fac_comment longtext      null,
    datetime    datetime      not null,
    enable      int default 1 not null
);

