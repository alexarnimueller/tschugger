-- create members table
create sequence member_id_seq;

create table if not exists member (
    id integer primary key default nextval('member_id_seq'),
    username varchar(80) unique not null,
    password text not null,
    category varchar(64) not null default 'Tschugger',
    firstname varchar(128) not null,
    lastname varchar(128) not null,
    scoutname varchar(128) not null,
    email varchar(128) unique,
    phone varchar(64) unique,
    notes text default '',
    img varchar(64),
    admin boolean default FALSE
);

alter sequence member_id_seq owned by member.id;
