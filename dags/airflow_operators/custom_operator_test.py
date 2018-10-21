import os
import tempfile
from datetime import datetime

import unittest
from airflow.models import DAG
from airflow_operators.custom_operator import SqrtOperator, ZipOperator


# mock the custom operator
class MockSumBy2Operator(SqrtOperator):

    # here we mock the business logic or any external things by overriding.
    def my_business_log(self, value):
        return 200


class TestSumBy2Operator(unittest.TestCase):

    def test_custom_operator(self):
        dag = DAG(dag_id='some_dag_id', start_date=datetime(2018, 8, 24, 0))
        task = SqrtOperator(dag=dag, task_id='some_task_id', sqrt_value=9)
        result = task.execute(None)
        self.assertEquals(result, 3)

    def test_mock_custom_operator(self):
        dag = DAG(dag_id='some_dag_id', start_date=datetime(2018, 8, 24, 0))
        task = MockSumBy2Operator(dag=dag, task_id='some_task_id', sqrt_value=9)
        result = task.execute(None)
        self.assertNotEqual(result, 3)
        self.assertEquals(result, 200)


class TestZipOperator(unittest.TestCase):

    def setUp(self):
        self.output_base_path = str(tempfile.mkdtemp())
        self.output_zip = '%s/zip_test.zip' % self.output_base_path
        self.input_path = '/tmp/zip_test'
        self.op = tempfile.mkdtemp()

    def testZipOperator(self):
        dag = DAG(dag_id='some_dag_id', start_date=datetime(2018, 8, 24, 0))
        task = ZipOperator(dag=dag, task_id='some_task_id', path_to_file_to_zip=self.input_path,
                           path_to_save_zip=self.output_zip)
        task.execute(None)
        self.assertTrue(os.path.exists(self.output_zip))
