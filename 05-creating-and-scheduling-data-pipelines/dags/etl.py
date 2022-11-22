import json
import glob
import os
from typing import List

from airflow import DAG
from airflow.utils import timezone
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

#hooks เรียกconnection เพื่อsecurity

#1 
def _get_files(filepath: str) -> List[str]:
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

#2 ได้file จาก task #1แล้ว ไม่ต้อง all_files = get_files(filepath)
# แต่ดึงจาก context

#3 PostgresHook
#hooks เรียกconnection เพื่อsecurity ต้อง

#    conn = psycopg2.connect(
#         "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
#     )


# version1 ไม่ดีเพราะ 1 task ทำงานหลายอย่าง ควรแยกเป็น1งาน 1 task

# def _process(**context):
#     hook = PostgresHook(postgres_conn_id ="my_postgres")
#     conn = hook.get_conn()
#     cur = conn.cursor()

#     #5 Create table
#     #Create table actors
#     table_create_actors = """
#         CREATE TABLE IF NOT EXISTS actors (
#             id int,
#             login text,
#             PRIMARY KEY(id)
#         )
#     """
#     #Create table events
#     table_create_events = """
#         CREATE TABLE IF NOT EXISTS events (
#             id text,
#             type text,
#             actor_id int,
#             actor_url text,
#             created_at text,
#             PRIMARY KEY(id),
#             CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id)
#         )
#     """
#     #Lis for table to create , order is importance, create main first
#     create_table_queries = [
#         table_create_actors,
#         table_create_events,
#     ]

#     for query in create_table_queries:
#         cur.execute(query)
#         conn.commit()

#     ti = context["ti"]
#     # Get list of files from filepath
#     all_files = ti.xcom_pull(task_ids = "get_files", key = "return_value")
#     #all_files = get_files(filepath)

#     for datafile in all_files:
#         print('for datafile in all_files:')
        
#         with open(datafile, "r") as f:
#             #If not json must change code for get input
#             data = json.loads(f.read())
#             for each in data:
#                 # Print some sample data
#                 print(each["id"], each["type"], each["actor"]["login"])
#                 if each["type"] == "IssueCommentEvent":
#                     print(
#                         each["id"], 
#                         each["type"],
#                         each["actor"]["id"],
#                         each["actor"]["login"],
#                         each["repo"]["id"],
#                         each["repo"]["name"],
#                         each["created_at"],
#                         each["payload"]["issue"]["url"],
#                     )
#                 else:
#                     print(
#                         each["id"], 
#                         each["type"],
#                         each["actor"]["id"],
#                         each["actor"]["login"],
#                         each["repo"]["id"],
#                         each["repo"]["name"],
#                         each["created_at"],
#                     )

#                 # Insert data into tables here
#                 insert_statement = f"""
#                     INSERT INTO actors (
#                         id,
#                         login
#                     ) VALUES ({each["actor"]["id"]}, 
#                     '{each["actor"]["login"]}')
#                     ON CONFLICT (id) DO NOTHING
#                 """
#                 #Importance in "ON CONFLICT (id) DO NOTHING "
#                 #If insert actor same id code is do nothing 

#                 # print(insert_statement)
#                 cur.execute(insert_statement)

#                 # Insert data into tables here 
#                 # 2. from create table in create_tables.py increase feature to have the same in that columns  
#                 # 3. increase '{each["actor"]["url"]}','{each["created_at"]}' in the command
#                 insert_statement = f"""
#                     INSERT INTO events (
#                         id,
#                         type,
#                         actor_id,
#                         actor_url,
#                         created_at
#                     ) VALUES ('{each["id"]}',
#                      '{each["type"]}',
#                      '{each["actor"]["id"]}',
#                      '{each["actor"]["url"]}',
#                      '{each["created_at"]}')
#                     ON CONFLICT (id) DO NOTHING
#                 """
#                 # print(insert_statement)
#                 cur.execute(insert_statement)

#                 conn.commit()

#version2 แยกงานเป็นแต่ละ task
# สร้าง task create table
def _create_tables():
    hook = PostgresHook(postgres_conn_id ="my_postgres")
    conn = hook.get_conn()
    cur = conn.cursor()

    #5 Create table
    #Create table actors
    table_create_actors = """
        CREATE TABLE IF NOT EXISTS actors (
            id int,
            login text,
            PRIMARY KEY(id)
        )
    """
    #Create table events
    table_create_events = """
        CREATE TABLE IF NOT EXISTS events (
            id text,
            type text,
            actor_id int,
            actor_url text,
            created_at text,
            PRIMARY KEY(id),
            CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id)
        )
    """
    #Lis for table to create , order is importance, create main first
    create_table_queries = [
        table_create_actors,
        table_create_events,
    ]

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def _process(**context):
    hook = PostgresHook(postgres_conn_id ="my_postgres")
    conn = hook.get_conn()
    cur = conn.cursor()

    ti = context["ti"]
    # Get list of files from filepath
    all_files = ti.xcom_pull(task_ids = "get_files", key = "return_value")
    #all_files = get_files(filepath)

    for datafile in all_files:
        print('for datafile in all_files:')
        
        with open(datafile, "r") as f:
            #If not json must change code for get input
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                print(each["id"], each["type"], each["actor"]["login"])
                if each["type"] == "IssueCommentEvent":
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                        each["payload"]["issue"]["url"],
                    )
                else:
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                    )

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO actors (
                        id,
                        login
                    ) VALUES ({each["actor"]["id"]}, 
                    '{each["actor"]["login"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                #Importance in "ON CONFLICT (id) DO NOTHING "
                #If insert actor same id code is do nothing 

                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into tables here 
                # 2. from create table in create_tables.py increase feature to have the same in that columns  
                # 3. increase '{each["actor"]["url"]}','{each["created_at"]}' in the command
                insert_statement = f"""
                    INSERT INTO events (
                        id,
                        type,
                        actor_id,
                        actor_url,
                        created_at
                    ) VALUES ('{each["id"]}',
                     '{each["type"]}',
                     '{each["actor"]["id"]}',
                     '{each["actor"]["url"]}',
                     '{each["created_at"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                conn.commit()

#อ่านข้อมูลจากfolder data

with DAG(
    "etl",
    start_date = timezone.datetime(2022, 11, 22),
    schedule = "@daily",
    tags = ["workshop"],
    catchup = False,
) as dag:

    get_files = PythonOperator(
        task_id = "get_files",
        python_callable = _get_files,
        op_kwargs={
            "filepath":"/opt/airflow/dags/data",
        }
    )

    create_tables = PythonOperator(
        task_id = "create_tables",
        python_callable = _create_tables,
    )

    process = PythonOperator(
        task_id = "process",
        python_callable = _process,
        op_kwargs={
            "filepath":"/opt/airflow/dags/data",
        }
    )
#4
   #get_files >> create_tables >> process

   #test รันแบบขนาน
    [get_files , create_tables] >> process
