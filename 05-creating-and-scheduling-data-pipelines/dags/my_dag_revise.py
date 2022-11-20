#import DAG เป็น pipeline
from airflow import DAG
#import Timezone
from airflow.utils import timezone
#step 2 ใช้ EmptyOperator เลย import EmptyOperator เข้ามา
from airflow.operators.empty import EmptyOperator
#step 5 import BashOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

#context manager เป็นการประกาศหัว
#"my_dag" ชื่อเดียวกับชื่อ file
#start date 2022, 10, 8
# schedule = None ยังไม่schedule
# step10
# schedule 
# schedule เที่ยงคืน คือ 0
# tags =['workshop'] จะทำให้เป็นชัดเจน
#v1  schedule = None ยังไม่set schedule
# with DAG(
#     "my_dag_revise",
#     start_date = timezone.datetime(2022, 10, 8),
#     schedule = None,
#     tags =["workshop"],
# ):
#     t1 = EmptyOperator( task_id = "t1")
#     t2 = EmptyOperator( task_id = "t2")

# #t1 รันก่อน t2
#     t1 >> t2

#v2
# with DAG(
#     "my_dag_revise",
#     start_date = timezone.datetime(2022, 10, 8),
#     schedule = None,
#     tags =["workshop"],
# ):
#     t1 = EmptyOperator( task_id = "t1")

#     echo_hello = BashOperator(
#         task_id = "echo_hello",
#         bash_command= "echo 'hello'",
#     )

#     t2 = EmptyOperator( task_id = "t2")

#t1 รันก่อน t2
#    t1 >> echo_hello >> t2

# #v3
# with DAG(
#     "my_dag_revise",
#     start_date = timezone.datetime(2022, 10, 8),
#     schedule = None,
#     tags =["workshop"],
# ):
#     t1 = EmptyOperator( task_id = "t1")

#     echo_hello = BashOperator(
#         task_id = "echo_hello",
#         bash_command= "echo 'hello'",
#     )
#     def _print_hey():
#         print("Hey!")

#     print_hey = PythonOperator(
#         task_id = "print_hey",
#         python_callable = _print_hey,
#     )

#     t2 = EmptyOperator( task_id = "t2")

# #t1 รันก่อน t2
#     t1 >> echo_hello >> print_hey >> t2

#v4 Schedule ใช้ ครอน เอกเพลสชั่น เดี๋ยวนี้ไม่ค่อยใช้ เพราะจะไม่รู้ว่าพังตอนไหน
#crontab.guru
#schedule = "* * * * *" รันตลอดเวลา

with DAG(
    "my_dag_revise",
    start_date = timezone.datetime(2022, 10, 8),
    schedule = " 30 8 * * *",
    tags =["workshop"],
):
    t1 = EmptyOperator( task_id = "t1")

    echo_hello = BashOperator(
        task_id = "echo_hello",
        bash_command= "echo 'hello'",
    )
    def _print_hey():
        print("Hey!")

    print_hey = PythonOperator(
        task_id = "print_hey",
        python_callable = _print_hey,
    )

    t2 = EmptyOperator( task_id = "t2")

#t1 รันก่อน t2
    #t1 >> echo_hello >> print_hey >> t2
    t1 >> [ echo_hello, print_hey] >> t2