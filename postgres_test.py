import psycopg2
import uuid
import time
import threading

pg_name = '<postgre server name>'
pg_password = '<postgre password>'

def connect():
    return psycopg2.connect(
        host=pg_name + '.postgres.database.azure.com',
        database='postgres',
        user='myadmin@' + pg_name + '.postgres.database.azure.com',
        password=pg_password)

cur = None

def createtable(drop=False):
    try:
        conn = connect()
        cur = conn.cursor()
        if (drop):
            cur.execute('drop table if exists events_jsonb;')
        cur.execute('''
        create table events_jsonb (
            id serial primary key,
            orderid UUID,
            data jsonb
        );
        ''')
        cur.execute('CREATE INDEX idxgin ON events_jsonb((data->>\'uuid\'));')
        conn.commit()
    except Exception as e:
        print('could not not create table maybe already exists: ' + str(e))
        pass
    finally:
        if (conn):
            cur.close()
            conn.close()

def row_count():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('select count(id) as max from events_jsonb;')
        rows = cur.fetchall()
        return rows[0][0]
    finally:
        if(conn):
            cur.close()
            conn.close()

def fetch_random_uuids(number, row_count):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute('''
            select orderid from events_jsonb
            where id in (
                select floor(random() * {})
                from (
                    select s.i as i
                    from generate_series(1, {}) s(i)
                ) as t
            );'''.format(row_count, number))
        return cur.fetchall()
    finally:
        if(conn):
            cur.close()
            conn.close()

def insert_jsonb(cur, orderid, data):
    cur.execute('insert into events_jsonb (orderid, data) values (\'{}\', \'{}\');'.format(uuid.uuid4(), data))

def select(cur):
    cur.execute('select id, orderid, data from events_jsonb order by id desc limit 1;')
    rows = cur.fetchall()
    for row in rows:
        pass

json = '''
{
    "id": 1234,
    "uuid": "some-uuid",
    "number": 12345.111,
    "text": "this is a bit longer text this is a bit longer text this is a bit longer text this is a bit longer text",
    "subobjects": [
        {
            "type": "event_type_0",
            "uuid": "1515176d-5067-44d7-b5a4-9d07b9d54e82",
            "text": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        },
        
        {
            "type": "event_type_1",
            "uuid": "f0249bdf-6d60-42af-ba06-e5e7a5cc7922",
            "text": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
        },
        
        {
            "type": "event_type_2",
            "uuid": "6b3467dd-27b4-49cc-a076-7b66c90cdc87",
            "text": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
        },
        
        {
            "type": "event_type_3",
            "uuid": "614e3285-fd57-4823-9bf5-911ccee43d48",
            "text": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
        },
        
        {
            "type": "event_type_4",
            "uuid": "c82dbe4d-114f-4931-8dfe-f6741c4b9e2c",
            "text": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        },
        
        {
            "type": "event_type_5",
            "uuid": "140467f1-3ad8-45ad-81f9-b721537e38b7",
            "text": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
        },
        
        {
            "type": "event_type_6",
            "uuid": "0361027a-2980-4df2-a9fc-624a77a808d3",
            "text": "gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg"
        },
        
        {
            "type": "event_type_7",
            "uuid": "bea0b257-a6f3-4b5b-8b65-c010d7d08676",
            "text": "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
        },
        
        {
            "type": "event_type_8",
            "uuid": "674dfd56-97d5-4036-9320-5443d3a98a66",
            "text": "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
        },
        
        {
            "type": "event_type_9",
            "uuid": "a02ba694-6799-404c-b3fc-407e00d16672",
            "text": "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
        },
        
        {
            "type": "event_type_10",
            "uuid": "6407a012-9b1a-49c4-abfb-721c4041d908",
            "text": "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"
        },
        
        {
            "type": "event_type_11",
            "uuid": "710de568-d8d6-462d-b456-3e20cd9d7bfd",
            "text": "llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll"
        },
        
        {
            "type": "event_type_12",
            "uuid": "d056c286-0190-4203-b696-c4d99d0ea020",
            "text": "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
        },
        
        {
            "type": "event_type_13",
            "uuid": "ff1458f6-bc7c-4d68-b622-a2a467fcd9c0",
            "text": "nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
        },
        
        {
            "type": "event_type_14",
            "uuid": "a03ce1d3-8659-49b7-b8a1-aa73c52db82d",
            "text": "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
        },
        
        {
            "type": "event_type_15",
            "uuid": "1a160684-c7b3-4435-9e45-a737e6c926e0",
            "text": "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp"
        },
        
        {
            "type": "event_type_16",
            "uuid": "ccea6725-703f-4e7b-a45d-7bd0d812fd2d",
            "text": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
        },
        
        {
            "type": "event_type_17",
            "uuid": "b436dc18-feb5-46a0-b210-a519fcaca371",
            "text": "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"
        },
        
        {
            "type": "event_type_18",
            "uuid": "11b457a3-d3e5-4d5c-adc2-c4d0a157bc9f",
            "text": "ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"
        },
        
        {
            "type": "event_type_19",
            "uuid": "b4960914-a356-489f-ab0e-e83aff527444",
            "text": "tttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"
        }
    ]
}
'''
json_len = len(json)

insert_mutex = threading.Condition()
select_mutex = threading.Condition()
insert_count = 0
select_count = 0
insert_per_loop = 5

def insertrange(max):
    global insert_count
    try:
        conn = connect()
        cur = conn.cursor()
        for i in range(0, int(max/insert_per_loop)):
            for k in range(0, insert_per_loop):
                insert_jsonb(cur, '00000000000000000000', json)
                conn.commit()
            insert_mutex.acquire()
            insert_count += insert_per_loop
            insert_mutex.notifyAll()
            insert_mutex.release()
    finally:
        if (conn):
            cur.close()
            conn.close()

def selectrandom(orderids):
    global select_count
    try:
        conn = connect()
        cur = conn.cursor()
        n = 0
        while True:
            for i in orderids:
                cur.execute('select data->>\'subobjects\' from events_jsonb where data->>\'uuid\' = \'{}\'::text'.format(i[0]))
                for k in cur.fetchall():
                    len(k[0])
                    pass
                conn.commit()
                if n % insert_per_loop == 0:
                    select_mutex.acquire()
                    select_count += insert_per_loop
                    select_mutex.notifyAll()
                    select_mutex.release()
                n += 1
    finally:
        if (conn):
            cur.close()
            conn.close()

def selectrange(max):
    global select_count
    try:
        conn = connect()
        cur = conn.cursor()
        for i in range(0, int(max/insert_per_loop)):
            for k in range(0, insert_per_loop):
                select(cur)
                conn.commit()
            select_mutex.acquire()
            select_count += insert_per_loop
            select_mutex.notifyAll()
            select_mutex.release()
    finally:
        if (conn):
            cur.close()
            conn.close()

def progress():
    global select_count
    global insert_count
    prev_select_count = 0
    prev_insert_count = 0
    while True:
        current_time = time.monotonic()
        time.sleep(5)
        select_mutex.acquire()
        tmp_select_count = select_count
        select_mutex.notifyAll()
        select_mutex.release()

        insert_mutex.acquire()
        tmp_insert_count = insert_count
        insert_mutex.notifyAll()
        insert_mutex.release()
        time_elapsed = time.monotonic() - current_time

        print('-----------------------------')
        print('elapsed:       {:12.2f} sec'.format(time_elapsed))
        d_insert_count = tmp_insert_count - prev_insert_count
        prev_insert_count = tmp_insert_count
        print('inserts count: {:12.1f}'.format(tmp_insert_count))
        print('inserts:       {:12.2f} tps'.format(d_insert_count / time_elapsed))
        d_select_count = tmp_select_count - prev_select_count
        prev_select_count = tmp_select_count
        print('selects count: {:12.1f}'.format(tmp_select_count))
        print('selects:       {:12.1f} tps'.format(d_select_count / time_elapsed))
        print('all bytes out: {:12.1f} chars'.format(tmp_insert_count * json_len))
        print('message size:  {:12.1f} chars'.format(json_len))
        print('bytes/sec:     {:12.1f}'.format(d_insert_count * json_len / time_elapsed))


def main(insert_t_count, select_t_count, message_per_t):
    print('fetching current row count, may take a while (1-2 min)')
    all_rows_count = row_count()
    print('fetched current row count: {}'.format(all_rows_count))

    orderids_num = 1000000
    print('fetching random uuids: {}'.format(orderids_num))
    orderids = fetch_random_uuids(orderids_num, all_rows_count)
    print('fetched random uuids: {}'.format(orderids_num))

    print('starting insert threads: {}'.format(insert_t_count))
    for i in range(0, insert_t_count):
        t = threading.Thread(target=insertrange, args=(message_per_t,))
        t.start()

    print('starting select threads: {}'.format(select_t_count))
    for i in range(0, select_t_count):
        t = threading.Thread(target=selectrandom, args=(orderids,))
        t.start()

    t = threading.Thread(target=progress, args=())
    t.start()
    t.join()


#print('trying to create table (if not exists)')
#createtable()

# params:
# - insert thread count
# - select thread count
# - max message to insert per thread
main(100, 0, 100000)


