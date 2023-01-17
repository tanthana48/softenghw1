create table softeng.vendingmachine
(
    id           int auto_increment
        primary key,
    machine_name varchar(255) null,
    location     varchar(255) null,
    product      json         null
);
