import airflow
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
import random


args = {
    'owner': 'ananth',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='example_branch_operator',
    default_args=args,
    schedule_interval="@daily")

cmd = 'ls -l'
run_this_first = DummyOperator(task_id='run_this_first', dag=dag)

# randomly pick a branch for demo
options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

branching = BranchPythonOperator(
    task_id='branching',
    python_callable=lambda: random.choice(options),
    dag=dag)
branching.set_upstream(run_this_first)

join = DummyOperator(
    task_id='join',
    trigger_rule='one_success',
    dag=dag
)

for option in options:
    t = DummyOperator(task_id=option, dag=dag)
    t.set_upstream(branching)
    dummy_follow = DummyOperator(task_id='follow_' + option, dag=dag)
    t.set_downstream(dummy_follow)
    dummy_follow.set_downstream(join)
