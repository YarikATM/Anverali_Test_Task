CREATE TABLE IF NOT EXISTS tasks (
    id     serial
        primary key
        unique,
    title  varchar(55) not null,
    description   text,
    expire date
);