# Results

- `450GB / v2`, inserts_thread: 100, selects_thread: 0    -> inserts: `1600 tps` | selects: `0 tps`
- `450GB / v2`, inserts_thread: 0  , selects_thread: 100  -> inserts: `0 tps` | selects: `2600 tps`
- `450GB / v2`, inserts_thread: 50 , selects_thread: 50   -> inserts: `300 tps` | selects: `1500 tps`
- `450GB / v4`, inserts_thread: 100, selects_thread: 0    -> inserts: `3000 tps` | selects: `0 tps`
- `450GB / v4`, inserts_thread: 0  , selects_thread: 100  -> inserts: `0 tps` | selects: `5000 tps`

## example results used:
- 450GB of drive
- cores: v2 or v4 (see file name)
- no replicas
- \> 10M records already inserted


# How to run
## setup db
- run commands in `postgres.sh` by hand step by step, because IPs and db name need to be set manually
- from a postgresql client (e.g. intellij idea)
    - run `create_table.sql` for creating table and installing uuid extension
    - run `generate.sql` to generate 2M records (will take some 10 minutes)
    
## run tests in VM
- in VM install python3 and psycopg2-binary e.g.
    - `sudo yum install python3 pip3`
    - `pip3 install psycopg2-binary`
- set the connection string in `postgres_test.sql` with db name, password
- copy the `postgres_test.py` to the VM
    - use scp
    - or simply `ssh` into the vm, use `vim postgres_test.py`, press `i` then copy-paste the code
- edit last line parameters with arguments:
    - 1) insert threads
    - 2) select threads
    - 3) max messages to insert
- run: `python3 postgres_test.py`
    
## some info:
- records used for insert/select in `generate.sql` and `postgres_test.py` is about `14 kBytes`
- `count(*)` of records are extremely slow, 1-2 minutes
- also fetching random uuids in the `generate.sql` is very slow
- **when running selects and inserts in parallel, for some reason selects starve out inserts very much, not sure if python implementation of postgresql issue**
- for best performance run the test from an Azure VM
- every thread is using it's own connection and there is commit after every statement

