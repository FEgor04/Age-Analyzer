create table if not exists analyzed
(
    id            integer,
    domain        varchar(250),
    first_name    varchar(250),
    last_name     varchar(250),
    estimated_age real,
    real_age      real,
    mean          real,
    mode          real,
    harmonic_mean real,
    median        real,
    std           real,
    friends_cnt   integer,
    verified      boolean,
    last_check    date,
    vk_age        integer
);