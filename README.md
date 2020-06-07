# setup db
- run commands in `postgres.sh` by hand step by step, because IPs and db name need to be set manually
- from a postgresql client (e.g. intellij idea)
    - run `create_table.sql` for creating table and installing uuid extension
    - run `generate.sql` to generate 2M records (will take some 10 minutes)
    
# run tests in VM
- in VM install python3 and psycopg2-binary e.g.
    - `sudo yum install python3 pip3`
    - `pip3 install psycopg2-binary`
- set the connection string in `postgres_test.sql` with db name, password
- copy the `postgres_test.py` to the VM
- edit last line parameters:
    - insert threads
    - select threads
    - max messages to insert
    
# some info:
- records used for insert in `generate.sql` and `postgres_test.py` is about `14 kBytes`
- `count(*)` of records are extremely slow, 1-2 minutes
- also fetching random uuids in the `generate.sql` is very slow
- **when running selects and inserts in parallel, for some reason selects starve out inserts very much, not sure if python implementation of postgresql issue**
- for best performance run the test from an Azure VM
- every thread is using it's own connection and there is commit after every statement

# example results used:
- 450GB of drive
- cores: v2 or v4 (see file name)
- no replicas
- \> 10M records already inserted