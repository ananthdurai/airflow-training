# Airflow Operators:

While DAGs describe how to run a workflow, Operators determine what gets done.

An operator describes a single task in a workflow. Operators are usually (but not always) atomic, meaning they can stand on their own and don’t need to share resources with any other operators. The DAG will make sure that operators run in the certain correct order; other than those dependencies, operators generally run independently. They may run on two completely different machines.

There are over 100 operators shipped with Airflow. Airflow operators can be broadly categorized into three categories.

### Action Operators:

The action operators perform some action such as executing a Python function or submitting a Spark Job.

 (e.g.) BashOperator, PythonOperator, DockerOperator, OracleOperator

### Sensor Operators:

The Sensor operators trigger downstream tasks in the dependency graph when a specific criterion is met, for example checking for a particular file becoming available on S3 before using it downstream. Sensors are a dominant feature of Airflow allowing us to create complex workflows and efficiently manage their preconditions.

(e.g.) S3KeySensors, HivePartitionSensor, ExternalTaskSensor, TimeSensor

### Transfer Operators:

Transfer Operators move data between systems such as from Hive to Mysql or from S3 to Hive.

(e.g.) GenericTransfer,MsSqlToHiveTransfer, RedshiftToS3Transfer



### Operator Properties:

| Property                    | Desc                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Default                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| dag                         | a reference to the dag the task is attached to                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Mandatory param        |
| task_id                     | a unique, meaningful id for the task                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Mandatory param        |
| email                       | email to send notification if any                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | None                   |
| email_on_retry              | boolean flag to send email on the task retry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | True                   |
| email_on_failure            | boolean flag to send email on the task failure                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | True                   |
| retries                     | the number of retries that should be performed before failing the task                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 0                      |
| retry_delay                 | delay between retries                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | timedelta(seconds=300) |
| retry_exponential_backoff   | maximum delay interval between retries                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | False                  |
| depends_on_past             | when set to true, task instances will run sequentially while relying on the previous task's schedule to succeed. The task instance for the start_date is allowed to run.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | False                  |
| adhoc                       | Mark the task as `adhoc`. Adhoc tasks used for performing certain task-specific on demand                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | False                  |
| params                      | Parameters / variables pass to airflow task instances                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | None                   |
| priority_weight             | priority weight of this task against other task. This allows the executor to trigger higher priority tasks before others when things get backed up.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 1                      |
| pool                        | the slot pool this task should run in, slot pools are a way to limit concurrency for certain tasks                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | None                   |
| sla                         | time by which the job is expected to succeed. Note that this represents the \`\`timedelta\`\` after the period is closed. For example if you set an SLA of 1 hour, the scheduler would send dan email soon after `1:00AM` on the `2016-01-02` if the `2016-01-01` instance has not succeeded yet. The scheduler pays special attention for jobs with an SLA and sends alert emails for sla misses. SLA misses are also recorded in the database for future reference. All tasks that share the same SLA time get bundled in a single email, sent soon after that time. SLA notification are sent once and only once for each task instance.    | None                   |
| execution_timeout           | max time allowed for the execution of this task instance, if it goes beyond it will raise and fail.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | None                   |
| task_concurrency            | When set, a task will be able to limit the concurrent runs across execution_dates                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | None                   |



### Bash Operators:

Execute a Bash script, command or set of commands. (e.g.) Bash Operator to clean /tmp files periodically. 

```python
clean_tmp_dir = BashOperator(
    task_id='clean_tmp_dir',
    bash_command='find /tmp -mtime +2 -type f -exec rm -rf {} \;',
    dag='cleaner_dag'
)
```

### Python Operators:

Executes a Python callable method.

```python
def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)
    
for i in range(10): # loop in to create dynamic operators.
    task = PythonOperator(
        task_id='sleep_for_' + str(i), # task id should be unique
        python_callable=my_sleeping_function, # python callable method
        op_kwargs={'random_base': float(i) / 10}, # pass the method argument here
        dag=dag)
```

### Branch Operators:

Allows a workflow to "branch" or follow a single path following the execution of this task.

It derives the PythonOperator and expects a Python function that returns the task\_id to follow. The task\_id returned should point to a task directly downstream from {self}. All other `branches` or directly downstream tasks are marked with a state of `skipped` so that these paths can't move forward. The \`\`skipped\`\` states are propageted downstream to allow for the DAG state to fill up and the DAG run's state to be inferred. Note that using tasks with `depends_on_past=True` downstream from `BranchPythonOperator` is logically unsound as `skipped` status will invariably lead to block tasks that depend on their past successes.`skipped` states propagates where all directly upstream tasks are`skipped`.

```python
branching = BranchPythonOperator(
    task_id='branching',
    python_callable=lambda: random.choice(options),
    dag=dag)
```

### Short Circuit Operators:

Allows a workflow to continue only if a condition is met. Otherwise, the  
workflow `short-circuits` and downstream tasks are skipped.  

The ShortCircuitOperator is derived from the PythonOperator. It evaluates a  
condition and short-circuits the workflow if the condition is False. Any  
downstream tasks are marked with a state of `skipped`. If the condition is  
True, downstream tasks proceed as normal.  

The condition is determined by the result of `python_callable``.

```python
cond_true = ShortCircuitOperator(
    task_id='condition_is_True', python_callable=lambda: True, dag=dag)

cond_false = ShortCircuitOperator(
    task_id='condition_is_False', python_callable=lambda: False, dag=dag)
```

### Running individual tasks:

```powershell
airflow test <dag_id> <task_id> <execution date> (or)
airflow test -tp {'param1': 'my_param'} <dag_id> <task_id> <execution_date>
```

### Writing custom Operators:

It's very simple, extend the `BaseOperator` class and `override` the contructor and the `execute` method.

(e.g.) A custom Airflow operator to `zip` all the files in a given directory

```python
class ZipOperator(BaseOperator):
    """
    An operator which takes in a path to a file and zips the contents to a location you define.
    :param path_to_file_to_zip: Full path to the file you want to Zip
    :type path_to_file_to_zip: string
    :param path_to_save_zip: Full path to where you want to save the Zip file
    :type path_to_save_zip: string
    """

    template_fields = ('path_to_file_to_zip', 'path_to_save_zip')
    template_ext = []
    ui_color = '#ffffff'  # ZipOperator's Main Color: white  # todo: find better color

    @apply_defaults
    def __init__(
            self,
            path_to_file_to_zip,
            path_to_save_zip,
            *args, **kwargs):
        self.path_to_file_to_zip = path_to_file_to_zip
        self.path_to_save_zip = path_to_save_zip

    def execute(self, context):
        logging.info("Executing ZipOperator.execute(context)")

        logging.info("Path to the File to Zip provided by the User (path_to_file_to_zip): " + str(self.path_to_file_to_zip))
        logging.info("Path to save the Zip File provided by the User (path_to_save_zip) : " + str(self.path_to_save_zip))

        dir_path_to_file_to_zip = os.path.dirname(os.path.abspath(self.path_to_file_to_zip))
        logging.info("Absolute path to the File to Zip: " + str(dir_path_to_file_to_zip))

        zip_file_name = os.path.basename(self.path_to_save_zip)
        logging.info("Zip File Name: " + str(zip_file_name))

        file_to_zip_name = os.path.basename(self.path_to_file_to_zip)
        logging.info("Name of the File or Folder to be Zipped: " + str(file_to_zip_name))

        os.chdir(dir_path_to_file_to_zip)
        logging.info("Current Working Directory: " + str(os.getcwd()))

        with ZipFile(zip_file_name, 'w') as zip_file:
            logging.info("Created zip file object '" + str(zip_file) + "' with name '" + str(zip_file_name) + "'")
            is_file = os.path.isfile(self.path_to_file_to_zip)
            logging.info("Is the File to Zip a File (else its a folder): " + str(is_file))
            if is_file:
                logging.info("Writing '" + str(file_to_zip_name) + "to zip file")
                zip_file.write(file_to_zip_name)
            else:  # is folder
                for dirname, subdirs, files in os.walk(file_to_zip_name):
                    logging.info("Writing '" + str(dirname) + "to zip file")
                    zip_file.write(dirname)
                    for filename in files:
                        file_name_to_write = os.path.join(dirname, filename)
                        logging.info("Writing '" + str(file_name_to_write) + "to zip file")
                        zip_file.write(file_name_to_write)
            logging.info("Closing Zip File Object")
            zip_file.close()

        logging.info("Moving '" + str(zip_file_name) + "' to '" + str(self.path_to_save_zip) + "'")
        os.rename(zip_file_name, self.path_to_save_zip)

        logging.info("Finished executing ZipOperator.execute(context)")
```


