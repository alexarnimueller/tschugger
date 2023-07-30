-- create members table
create sequence member_id_seq;

create table if not exists member (
    id integer primary key default nextval('member_id_seq'),
    name varchar(128) not null,
    category varchar(64) not null default 'Tschugger',
    email varchar(128) unique,
    phone varchar(64) unique,
    notes text default '',
    joined date default CURRENT_DATE,
    token varchar(16) default ''
);

alter sequence member_id_seq owned by member.id;

-- create admin users table
create sequence user_id_seq;

create table if not exists app_user (
    id integer primary key default nextval('user_id_seq'),
    username varchar(80) unique not null,
    password text not null,
    email varchar(120) unique not null
);

alter sequence user_id_seq owned by app_user.id;

-- insert dummy admin for testing
insert into app_user(username, password, email)
  values ('admin',
          'pbkdf2:sha256:260000$pMhHQ0zDCRnkVAJ7$8efafb0ad1e04adefa5b9eb5e9c9f3623ed172bbdade2449c719d50d2c932854',
          'admin@example.com');
