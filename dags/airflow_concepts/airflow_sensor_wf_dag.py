# Task wait for a file and compute the word count
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('HelloWorld', default_args=args)

wf_task_4 = ExternalTaskSensor(
    external_task_id='task_4',
    external_dag_id='HelloWorld',
    task_id='wf_task_4',
    dag=dag,
)

t4 = BashOperator(
    task_id='task_1',
    bash_command='echo "Task 4 completed successfully"',
    dag=dag)

t4.set_upstream(wf_task_4)
