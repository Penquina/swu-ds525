import logging
from airflow import DAG
from airflow.utils import timezone
#step 2 ใช้ EmptyOperator เลย import EmptyOperator เข้ามา
from airflow.operators.empty import EmptyOperator
#step 5 import BashOperator
from airflow.operators.bash import BashOperator
#step 8
from airflow.operators.python import PythonOperator

def _push