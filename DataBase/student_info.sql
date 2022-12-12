create table student_info
(
    Sl_No      int auto_increment,
    Reg_No     varchar(45)              not null,
    Name       varchar(45)              not null,
    PassWord   varchar(45)              not null,
    email      varchar(45)              not null,
    photo_link varchar(300)             null,
    IP         varchar(45) default '0'  null,
    sec        varchar(10) default '18' null,
    primary key (Sl_No, Reg_No)
);

