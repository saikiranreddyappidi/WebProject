create table deletion_requests
(
    slno      int auto_increment
        primary key,
    reg       varchar(45) null,
    filename  varchar(45) not null,
    file_link varchar(45) null,
    subject   varchar(45) null,
    comments  longtext    null,
    datetime  varchar(45) not null
);

