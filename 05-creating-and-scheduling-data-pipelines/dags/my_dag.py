from airflow import DAG
from airflow.utils import timezone
#step 2 ใช้ EmptyOperator เลย import EmptyOperator เข้ามา
from airflow.operators.empty import EmptyOperator
#step 5 import BashOperator
from airflow.operators.bash import BashOperator
#step 8
from airflow.operators.python import PythonOperator

#context manager
#"my_dag" ชื่อเดียวกับชื่อ file
#start date 2022, 10, 8
# schedule = None ยังไม่schedule
# step10
# schedule 
# schedule เที่ยงคืน คือ 0
with DAG(
    "my_dag",
    start_date = timezone.datetime(2022, 10, 8),
    schedule = "0 0 * * *",
    tags = ["workshop"],
):
    # Task
    #1st task ยังไม่ทำอะไร
    # step 1
    t1 = EmptyOperator( task_id = "t1")

    #step 4
    echo_hello = BashOperator(
        task_id = "echo_hello",
        bash_command = "echo 'hello'",
    )
    #step 7
    def _print_hey():
        print("Hey!")

    print_hey = PythonOperator(
        task_id = "print_hey",
        python_callable = _print_hey,
    )

    # 2nd task
    t2 = EmptyOperator( task_id = "t2")
    #step 3  
    #t1 >> t2
    #step 6
    #t1 >> echo_hello >> t2

    #step 9
    #t1 >> echo_hello >> print_hey >> t2

    #step 11

    #t1 >> echo_hello 
    #t1 >> print_hey 
    #echo_hello >> t2
    #print_hey >> t2
 
    t1 >> [echo_hello, print_hey] >> t2
