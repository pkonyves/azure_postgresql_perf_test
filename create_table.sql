-- install uuid extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- verify extension works
select uuid_generate_v4();

-- create table
create table events_jsonb (
    id serial primary key,
    orderid UUID,
    data jsonb
);

-- create index on json 'uuid' field
CREATE INDEX idxgin ON events_jsonb((data->>'uuid'));