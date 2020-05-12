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
        # This is not building a large string, so readability is more important to me than performance
        table = self.extract_table_metadata()
        database_name = table.get(constant.DATABASE_NAMES_COLUMN_NM)
        table_name = table.get(constant.TABLE_NAME_COLUMN_NM)

        sql = "CREATE OR REPLACE TABLE " + database_name + "." + table_name + "(\n"

        column = self.extract_column_metadata()
        for index in column.index:
            sql = sql + column[constant.COLUMN_NAME_NM][index]
            sql = sql + ' '
            sql = sql + column[constant.COLUMN_TYPE_NM][index]

            size = str(column[constant.COLUMN_SIZE_NM][index])
            if size != 'nan':
                sql = sql + '(' + size
                sql = sql[:-2]
                sql = sql + ')'

            required = column[constant.COLUMN_REQUIRED_NM][index]
            if len(required) > 0:
                sql = sql + ' NOT NULL'

            sql = sql + ',\n'

        sql = sql[:-2]
        sql = sql + ');'

        return sql

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
            return pd.read_excel(self.path,
                                 skiprows=constant.SKIP_COLUMN_ROWS,
                                 header=0,
                                 usecols=list(range(6)),
                                 sheet_name=constant.SHEET_NAME)
        except Exception:
            msg = "Error occurred in extract_table_metadata for: {}".format(self.path)
            logging.exception(msg)
            raise Exception(msg)

    def extract_admin_commands(self):
        try:
            with open(self.path) as file:
                file = yaml.load(file, Loader=yaml.FullLoader)

            return file.get('engine')
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
