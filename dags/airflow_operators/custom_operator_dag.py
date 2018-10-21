import airflow
from airflow import DAG

from airflow_operators.custom_operator import SqrtOperator, ZipOperator, UnzipOperator

args = {
    'owner': 'ananth',
    'start_date': airflow.utils.dates.days_ago(2)
}

FILE_TO_ZIP_PATH = "/tmp/input/test.txt"    # location to file or folder to zip
ZIP_FILE_PATH = "/tmp/output/test.txt.zip"  # location save the zip operation to and read the unzip operator from
UNZIP_PATH = "/tmp/output/"                 # location to unzip the contents of the file


dag = DAG(
    dag_id='custom_operator',
    default_args=args,
    schedule_interval="@daily")

sqrt = SqrtOperator(task_id='sqrt', sqrt_value=20, dag=dag)

zip_task = ZipOperator(
    task_id='zip_task',
    path_to_file_to_zip=FILE_TO_ZIP_PATH,
    path_to_save_zip=ZIP_FILE_PATH,
    dag=dag)

unzip_task = UnzipOperator(
    task_id='unzip_task',
    path_to_zip_file=ZIP_FILE_PATH,
    path_to_unzip_contents=UNZIP_PATH,
    dag=dag)


zip_task.set_downstream(unzip_task)

