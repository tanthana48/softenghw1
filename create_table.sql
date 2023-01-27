create table softeng.vendingmachine
(
    id           int auto_increment
        primary key,
    machine_name varchar(255) null,
    location     varchar(255) null
);

create table softeng.product
(

    product_id           int auto_increment
        primary key,
        constraint product___fk
        foreign key (machine_id) references vendingmachine (id)
            on update cascade on delete cascade,
    machine_id           int,
    product_name         varchar(255) null,
    amount               int default 0
);

