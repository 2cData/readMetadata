import logging
import pathlib

import pandas as pd
import yaml

import main.constant as constant
from main.log import CustomLogger

logging.setLoggerClass(CustomLogger)

'''
create or replace table emp_basic (
first_name string ,
last_name string ,
email string ,
streetaddress string ,
city string ,
start_date date
);
'''


class Build_Script():
    path = ''

    def __init__(self, path):
        self.path = path
        self._file_exists()

    def build_admin_script(self):
        admin = self.extract_admin_commands()

        return ''

    def build_sql_script(self):
        table = self.extract_table_metadata()
        column = self.extract_column_metadata()

        return ''

    def extract_table_metadata(self):
        try:
            df = pd.read_excel(self.path,
                               skiprows=constant.SKIP_DATABASE_ROWS,
                               nrows=constant.NUM_DATABASE_ROWS,
                               usecols={0, 1},
                               keep_default_na=False,
                               na_values='NaN',
                               na_filter=True,
                               sheet_name=constant.SHEET_NAME)

            header = df.values

            res = {constant.DATABASE_NAMES_COLUMN_NM: header[constant.DATABASE_NAMES_COLUMN_ID, 1],
                   constant.TABLE_NAME_COLUMN_NM: header[constant.TABLE_NAME_COLUMN_ID, 1]}

            return res
        except Exception:
            msg = "Error occurred in extract_table_metadata for: {}".format(self.path)
            logging.exception(msg)
            raise Exception(msg)

    def extract_column_metadata(self):
        try:
            df = pd.read_excel(self.path,
                               skiprows=constant.SKIP_COLUMN_ROWS,
                               header=0,
                               usecols=list(range(6)),
                               sheet_name=constant.SHEET_NAME)

            return df.to_dict(orient='index')
        except Exception:
            msg = "Error occurred in extract_table_metadata for: {}".format(self.path)
            logging.exception(msg)
            raise Exception(msg)

    def extract_admin_commands(self):
        try:
            with open(self.path) as file:
                df = pd.io.json_normalize(yaml.load(file))

            return df.to_dict(orient='index')
        except Exception:
            msg = "Error occurred in extract_admin_commands for: {}".format(self.path)
            logging.exception(msg)
            raise Exception(msg)

    def _file_exists(self):
        file = pathlib.Path(self.path)

        if not file.exists():
            msg = "File does not exist : {}".format(self.path)
            logging.exception(msg)
            raise Exception(msg)
