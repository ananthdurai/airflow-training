import math

from airflow.models import BaseOperator
from airflow.utils import apply_defaults
import logging

'''
Given a integer the SqrtOperator will sqrt of the input
'''
class SqrtOperator(BaseOperator):

    @apply_defaults
    def __init__(self, sqrt_value, *args, **kwargs):
        self.sqrt_value = sqrt_value
        super(SqrtOperator, self).__init__(*args, **kwargs)

    # override execute method
    def execute(self, context):
        logging.info("called")
        return self.my_business_log(self.sqrt_value)

    # here we separated the business logic or any external api call
    def my_business_log(self, value):
        return math.sqrt(value)


