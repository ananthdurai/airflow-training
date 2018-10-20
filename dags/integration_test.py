import unittest

from airflow.models import DagBag


class TestDagPipeline(unittest.TestCase):
    LOAD_SECOND_THRESHOLD = 2

    def setUp(self):
        self.dagbag = DagBag(dag_folder='/Users/adurai/workspace/airflow-training/dags')

    def test_import_dags(self):
        self.assertFalse(
            len(self.dagbag.import_errors),
            'DAG import failures. Errors: {}'.format(
                self.dagbag.import_errors
            )
        )

    def test_task_count(self):
        dag_id = 'alerts_dag'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 3)
