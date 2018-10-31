# Task wait for a file and compute the word count
from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.sensors import ExternalTaskSensor

args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 10, 20),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('HelloWorldSensors', default_args=args, schedule_interval='@daily')

wf_task_4 = ExternalTaskSensor(
    external_task_id='task_4',
    external_dag_id='HelloWorldAirflowDag',
    task_id='wf_task_4',
    dag=dag,
)

t4 = BashOperator(
    task_id='task_1',
    bash_command='echo "Task 4 completed successfully"',
    dag=dag)

t4.set_upstream(wf_task_4)
