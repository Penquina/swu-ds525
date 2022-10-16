import logging
from airflow import DAG
from airflow.utils import timezone
#step 2 ใช้ EmptyOperator เลย import EmptyOperator เข้ามา
from airflow.operators.empty import EmptyOperator
#step 5 import BashOperator
from airflow.operators.bash import BashOperator
#step 8
from airflow.operators.python import PythonOperator

'''
def _say_hello():
    print("Hello")
'''
def _say_hello(**context):
    print(context)
    datestamp = context["ds"]
    print("Hello")


def _print_log_messages():
    logging.info = ("Hello from Log") 

#context manager
#"my_dag" ชื่อเดียวกับชื่อ file
#start date 2022, 10, 8
# schedule = None ยังไม่schedule
# step10
# schedule 
# schedule เที่ยงคืน คือ 0
with DAG(
    "my_dag2",
    start_date=timezone.datetime(2022, 10, 15),
    schedule="*/30 * * * *",
    tags=["workshop"],
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")

    echo_hello = BashOperator(
        task_id="echo_hello",
        bash_command="echo 'hello' on {{ ds }}",        
    )

    say_hello = PythonOperator(
        task_id="say_hello",
        python_callable=_say_hello,
    )

    print_log_messages = PythonOperator(
        task_id="print_log_messages",
        python_callable=_print_log_messages,
    )

    end = EmptyOperator(task_id="end")

    start >> echo_hello >> [say_hello, print_log_messages] >> end

