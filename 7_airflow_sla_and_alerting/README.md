# Alerting, monitoring & SLA

Airflow has good support for basic monitoring of your jobs.

- SLA misses: airflow is able to send out an email bundling all SLA misses for a specific scheduling interval.
- EmailOperator: airflow can send out emails when a specific point in a DAG is reached such as task `failed`, `success`, `retry`etc
- Notification: Sending notifications to popular online services like Slack.
- Airflow UI: The airflow dashboard itself, which you can manually refresh to verify which jobs ran successfully or failed recently.
- Python callbacks: python function to call for a certain events like `SLA Miss`, `task failed`or `task_success`

An example DAG with all the monitoring:

```python
monitoring_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'sla': timedelta(hours=2),
}

def call_failue(context):
    send_slack_notification('task failed')

def call_success(context):
    send_slack_notification('task success')

def call_sla_miss(context):
    send_slack_notification('sla miss')
    send_pager_duty_notification()


monitor_dag = dag = DAG(
    dag_id='example_monitor_dag',
    default_args=monitoring_args,
    schedule_interval="@daily",
    on_failure_callback=call_failue,
    on_success_callback=call_success,
    sla_miss_callback=call_failue
)

```


