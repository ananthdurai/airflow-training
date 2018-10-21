import logging
from datetime import timedelta

import airflow
from airflow import DAG, AirflowException
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow_sla_and_alerting.alerts import AlertManager

args = {
    'owner': 'ananth',
    'start_date': airflow.utils.dates.days_ago(7),
    'on_failure_callback': AlertManager.on_failure_callback,
    'on_retry_callback': AlertManager.on_retry_callback,
    'on_success_callback': AlertManager.on_success_callback,
    'retries': 10,
    'retry_delay': timedelta(minutes=1),
    'depends_on_past': True,
    'email': ['dummy@example.com'],

}

dag = DAG(
    dag_id='alerts_dag',
    default_args=args,
    schedule_interval='@daily',
    sla_miss_callback=AlertManager.sla_miss_callback,
)


def task_fail():
    raise AirflowException("Task failed")


def task_success():
    logging.info("i'm good")


tf = PythonOperator(
    task_id='task_fail',
    python_callable=task_fail,
    dag=dag)

ts = PythonOperator(
    task_id='task_success',
    python_callable=task_success,
    dag=dag)

all_done = DummyOperator(task_id='all_done', sla=timedelta(hours=1), dag=dag)

tf.set_upstream(all_done)
ts.set_upstream(all_done)
