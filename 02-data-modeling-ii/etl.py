import glob
import json
import os
from typing import List

from cassandra.cluster import Cluster

table_drop = "DROP TABLE events"
#1. เพิ่ม field : created_at text : เพราะจะเก็บข้อมูลfiled เพิ่ม

table_create = """
    CREATE TABLE IF NOT EXISTS events
    (
        id text,
        type text,
        public boolean,
        created_at text, 
        PRIMARY KEY (
            id,
            type
        )
    )
"""

create_table_queries = [
    table_create,
]
drop_table_queries = [
    table_drop,
]

def drop_tables(session):
    for query in drop_table_queries:
        try:
            rows = session.execute(query)
        except Exception as e:
            print(e)


def create_tables(session):
    for query in create_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            print(e)

def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files

#5. Read JSON แล้วprintout ข้อมูลที่เซตที่ 3มาดู
def process(session, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r") as f:
            #load file มาอ่าน
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                #5.จากเดิม print(each["id"], each["type"], each["actor"]["login"])
                #  ล้อตาม2.ที่ insert_sample_data เปลี่ยนเป็น
                # Print มาดู ยังไม่ได้ใส่ตาราง
                print(each["id"], each["type"], each["public"], each["created_at"])

                # Insert data into tables here
                #6. ใส่ข้อมูลในตาราง
                query = f"""
                INSERT INTO events (id, type, public, created_at) VALUES ('{each["id"]}', '{each["type"]}', {each["public"]}, '{each["created_at"]}' )
                """
                session.execute(query)


# 2. เพิ่ม ค่าใน created_at เข้ามา "2022-08-17T15:51:05Z"

def insert_sample_data(session):
    query = f"""
    INSERT INTO events (id, type, public, created_at) VALUES ('23487929661', 'PushEvent', true, '2022-08-17T15:51:05Z' )
    """
    session.execute(query)


def main():
    cluster = Cluster(['127.0.0.1'])    # Connect casada 
    session = cluster.connect()         # Create session

    # Create keyspace
    try:
        session.execute(               #Create dB
            """
            CREATE KEYSPACE IF NOT EXISTS github_events
            WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
            """
        )
    except Exception as e:
        print(e)

    # Set keyspace
    try:
        session.set_keyspace("github_events")    
    except Exception as e:
        print(e)

    drop_tables(session)    #drop table
    #Prepare for create new table ถ้าอยากเก็บข้อมูล field เพิ่มต้องสร้างfield ใหม่ ไปที่ table_create
    create_tables(session)  

    #4.Test แล้วใช้ได้ จะนำเข้าจริง เซตpath ไปที่ directory data ที่เก็บ json
    process(session, filepath="../data")
    # ใส่ข้อมูล hard code เข้าไปเพื่อทดสอบว่าสามารถใส่ข้อมูลในตารรางได้มั้ย เป็นขั้น 2 ขฬ เรียก function : insert_sample_data

    insert_sample_data(session)

    # Select data in Cassandra and print them to stdout
    #3. Select event เปลี่ยน id เป็น "id": "23487929661" , เปลี่ยน type เป็น "type": "PushEvent"
    # เดิมเป็น SELECT * from events WHERE id = '23487929637' AND type = 'IssueCommentEvent'
    query = """
    SELECT * from events WHERE id = '23487929661' AND type = 'PushEvent'
    """

    
    try:
        rows = session.execute(query)
    except Exception as e:
        print(e)

    for row in rows:
        print(row)

# Main 
if __name__ == "__main__":
    main()