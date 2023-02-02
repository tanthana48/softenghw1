drop database if exists vending_machine;

create database vending_machine;

create table vending_machine.machine
(
    id           int auto_increment
        primary key,
    machine_name varchar(255) null,
    location     varchar(255) null
);

create table vending_machine.product
(

    product_id           int auto_increment
        primary key,
        constraint product___fk
        foreign key (machine_id) references machine (id)
            on update cascade on delete cascade,
    machine_id           int,
    product_name         varchar(255) null,
    amount               int default 0
);
