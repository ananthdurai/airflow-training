from datetime import datetime,timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

"""
### Hello world dag
"""
args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 10, 20),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),

}


dag = DAG('HelloWorldAirflowDag', default_args=args, schedule_interval='@daily')

dag.doc_md = __doc__

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello World from Task 1"',
    dag=dag)
t1.doc_md = """#Task 1
            print Hello world from task 1 
            """

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Hello World from Task 2"',
    dag=dag)

t2.doc_md = """#Task 2
            print Hello world from task 2 
            """

t3 = BashOperator(
    task_id='task_3',
    bash_command='echo "Hello World from Task 3"',
    dag=dag)

t3.doc_md = """#Task 3
            print Hello world from task 3 
            """

t4 = BashOperator(
    task_id='task_4',
    bash_command='sleep 300;echo "Hello World from Task 4"',
    dag=dag)

t4.doc_md = """#Task 4
            print Hello world from task 4 
            """

t2.set_upstream(t1)
t3.set_upstream(t1)
t4.set_upstream(t2)
t4.set_upstream(t3)



