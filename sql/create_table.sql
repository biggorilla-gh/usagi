create table documents (
  id serial,
  universal_id varchar(255),
  title varchar(255),
  keywords text,
  path varchar(255)
);

create table filters (
  id serial,
  parent_id int,
  name varchar(255)
);
