-- create members table
create sequence member_id_seq;

create table if not exists member (
    id integer primary key default nextval('member_id_seq'),
    firstname varchar(128) not null,
    lastname varchar(128) not null,
    scoutname varchar(128) not null,
    email varchar(128) unique,
    phone varchar(64) unique,
    notes text default '',
    img varchar(64)
);

alter sequence member_id_seq owned by member.id;

-- create admin users table
create sequence user_id_seq;

create table if not exists app_user (
    id integer primary key default nextval('user_id_seq'),
    username varchar(128) unique not null,
    password text not null,
    email varchar(128) unique not null,
    admin boolean default FALSE
);

alter sequence user_id_seq owned by app_user.id;
