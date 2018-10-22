# Introduction to data pipeline management with Airflow

The modern Data Warehouse increase in complexity it is necessary to have a dependable, scalable, intuitive, and simple scheduling and management program to monitor the flow of data and watch how transformations are completed.

Apache Airflow, help manage the complexities of their Enterprise Data Warehouse, is being adopted by tech companies everywhere for its ease of management, scalability, and elegant design. Airflow is rapidly becoming the go-to technology for companies scaling out large data warehouses.

The Introduction to the data pipeline management with Airflow training course is designed to familiarize participants with the use of Airflow schedule and maintain numerous ETL processes running on a large scale Enterprise Data Warehouse. 

Table of contents:

1. [Introduction to Airflow](https://github.com/ananthdurai/airflow-training/tree/master/1_introduction_to_airflow)
2. [Introduction to Airflow core concepts (DAGs, tasks, operators, sensors)](https://github.com/ananthdurai/airflow-training/tree/master/2_airflow_concepts)
3. [Airflow UI](https://github.com/ananthdurai/airflow-training/tree/master/3_airflow_ui)
4. [Airflow Scheduler](https://github.com/ananthdurai/airflow-training/tree/master/4_airflow_scheduler)
5. [Airflow Operators & Sensors](https://github.com/ananthdurai/airflow-training/tree/master/5_airflow_operators)
6. [Advance Airflow Concepts (Hooks, Connections, Variables, Templates, Macros, XCom) ](https://github.com/ananthdurai/airflow-training/tree/master/6_advance_airflow_concepts)
7. [SLA, Monitoring & Alerting](https://github.com/ananthdurai/airflow-training/tree/master/7_airflow_sla_and_alerting)
8. [Code examples](https://github.com/ananthdurai/airflow-training/tree/master/dags)

## Prerequisites

Participants should have a technology background, basic programming skills in Python and be open to sharing their thoughts and questions.

Participants need to bring their laptops. The examples tested on mac & ununtu machines. Participants can use any hosted airflow solutions such as [Google cloud composer](https://cloud.google.com/composer/) or [Astronomer](https://www.astronomer.io/blog/airflow-at-astronomer/)

## Installation

1. install sqllite3

2. run `./airflow scheduler` to start the airflow scheduler. The installation script will install all the dependencies 

3. run in another terminal `./airflow webserver`

4. on your browser visit `http://localhost:8080` to access airflow UI

## Contributing
Interested in contributing? Improving documentation? Adding more example? Check out [Contributing.md](https://github.com/ananthdurai/airflow-training/blob/master/contributing.md)

## License
As stated in the [License file](https://github.com/ananthdurai/airflow-training/blob/master/LICENSE) all lecture slides are provided under Creative Commons BY-NC 4.0. The exercise code is released under an MIT license.

Author:
 - [Ananth Packkildurai](https://github.com/ananthdurai/airflow-training/blob/master/author.md)

## Credit
- [Airflow documentation](https://airflow.apache.org/)
- [@dustinstansbury](https://medium.com/@dustinstansbury/understanding-apache-airflows-key-concepts-a96efed52b1a)
- [Airflow Plugins](https://github.com/airflow-plugins)
- [Astronomer Airflow blog](https://www.astronomer.io/blog/topic/airflow/)

