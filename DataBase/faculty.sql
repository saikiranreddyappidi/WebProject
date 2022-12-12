create table faculty
(
    sl_no        int auto_increment,
    Name         varchar(45) not null,
    faculty_id   varchar(45) not null,
    faculty_pswd varchar(45) not null,
    primary key (sl_no, faculty_id)
);

