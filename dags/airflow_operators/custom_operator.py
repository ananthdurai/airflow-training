import math

from airflow.models import BaseOperator
from airflow.utils import apply_defaults
import logging
from zipfile import ZipFile
import os


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
        super(ZipOperator, self).__init__(*args, **kwargs)

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

            # todo: print out contents and results of zip file creation (compression ratio, size, etc)

            logging.info("Closing Zip File Object")
            zip_file.close()

        logging.info("Moving '" + str(zip_file_name) + "' to '" + str(self.path_to_save_zip) + "'")
        os.rename(zip_file_name, self.path_to_save_zip)

        logging.info("Finished executing ZipOperator.execute(context)")


class UnzipOperator(BaseOperator):
    """
    An operator which takes in a path to a zip file and unzips the contents to a location you define.
    :param path_to_zip_file: Full path to the zip file you want to Unzip
    :type path_to_zip_file: string
    :param path_to_unzip_contents: Full path to where you want to save the contents of the Zip file you're Unzipping
    :type path_to_unzip_contents: string
    """

    template_fields = ('path_to_zip_file', 'path_to_unzip_contents')
    template_ext = []
    ui_color = '#ffffff'  # UnzipOperator's Main Color: white  # todo: find better color

    @apply_defaults
    def __init__(
            self,
            path_to_zip_file,
            path_to_unzip_contents,
            *args, **kwargs):
        self.path_to_zip_file = path_to_zip_file
        self.path_to_unzip_contents = path_to_unzip_contents
        super(UnzipOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        logging.info("Executing UnzipOperator.execute(context)")

        logging.info("path_to_zip_file: " + str(self.path_to_zip_file))
        logging.info("path_to_unzip_contents: " + str(self.path_to_unzip_contents))

        # No check is done if the zip file is valid so that the operator fails when expected so that airflow can properly mark the task as failed and schedule retries as needed
        with ZipFile(self.path_to_zip_file, 'r') as zip_file:
            logging.info("Created zip file object '" + str(zip_file) + "' from path '" + str(self.path_to_zip_file) + "'")
            logging.info("Extracting all the contents to '" + str(self.path_to_unzip_contents) + "'")
            zip_file.extractall(self.path_to_unzip_contents)
            logging.info("Closing Zip File Object")
            zip_file.close()

        logging.info("Finished executing UnzipOperator.execute(context)")

