import logging

from airflow import DAG
from airflow.utils import timezone
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

#ชื่อฟังก์ชั่นต้องไม่เหมือนชื่อtask เลยใส่ _ นำหน้า
#สามารถเขียนเพื่อเอาข้อมูลจาก context ออกมาได้

def _say_hello( name="", **context ):
    print(context)
    datestamp = context["ds"]
    #ใช้ได้แทน "name": "Kan {{ ds_nodash }}"
    #ds_nodash = context["ds_nodash"]
    print(f"Hello! {name} on {datestamp}")

#logging มีระดับการlog => info, debug แล้วแต่การทำงาน
def _print_log_messages():
    logging.info("Hello from Log")

with DAG(
    "my_dag_w9",
    start_date = timezone.datetime(2022,11,21),
    schedule = "*/30 * * * *",
    tags = ["workshop"],
    catchup = False,
) as dag:

    start = EmptyOperator(task_id = "start")

    echo_hello = BashOperator(
        task_id = "echo_hello",
        bash_command = "echo 'hello' on {{ ds }}",
    )
#    op_kwargs รับข้อมูลเป็น dict
    say_hello = PythonOperator(
        task_id = "say_hello",
        python_callable = _say_hello,
        op_kwargs = {
            "name": "Kan {{ ds_nodash }}",
        }
    )

    print_log_messages = PythonOperator(
        task_id = "print_log_messages",
        python_callable = _print_log_messages,

    )

    end =  EmptyOperator(task_id = "end")

    start >> echo_hello >> say_hello >> print_log_messages >> end
#    start >> echo_hello >> [ say_hello , print_log_messages ] >> end

