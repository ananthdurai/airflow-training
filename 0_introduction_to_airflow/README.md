# Introduction to Airflow

Airflow was started in October 2014 by Maxime Beauchemin at Airbnb. It was open source from the very first commit and officially brought under the Airbnb Github and announced in June 2015.

The project joined the Apache Software Foundation’s incubation program in March 2016.

### what is Airflow?

Airflow is a platform to programmatically author, schedule and monitor workflows.

### Airflow Principles:

- **Dynamic**: Airflow pipelines are the configuration as a code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.
- **Extensible**: Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
- **Elegant**: Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful Jinja templating engine.
- **Scalable**: Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. Airflow is ready to scale to infinity.

### Airflow v/s Cron:

| Cron                                                                                                       | Airflow                                                                                                                                               |
|:---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cron build into Linux, so requires no installation.                                                        | Airflow requires setup and installation of the web server and the scheduler. In most cases, it requires external executors like Celery or Kubernetes. |
| The job performance was not transparent. Cron keeps a log of job outputs on the server where the jobs run. | Airflow can aggregate logs from the job outputs and show in the UI.                                                                                   |
| Versioning and tracking changes/ rollback is hard.                                                         | Airflow programmatically authored so that we can use version, unit test/ integration test before the production rollout.                              |
| Rerunning, backfilling the failed tasks are hard.                                                          | Airflow designed to support rerunning and backfilling the tasks.                                                                                      |
| No task dependency management.                                                                             | Airflow Dags with Sensors and Operators support complex data pipeline dependency management.                                                          |

In nutshell, Airflow support much richer functionalities like

- Retries
- Dependencies between tasks
- SLAs/error notifications
- Metrics about time to complete, number of failures etc
- Logs
- Visibility

### When not to use Airflow?

Airflow is not a cron. If your task requires to run precisely the scheduled time, Airflow is not the appropriate choice. Airflow scheduler gives no guarantee that it schedule the task at the precisely scheduled time. Airflow is the best effort scheduler to schedule a task as soon as all the upstream dependency of the task is a success.
