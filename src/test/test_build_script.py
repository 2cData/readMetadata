import unittest

import main.constant as constant
from main.build_script import Build_Script as obj

VALID_METADATA_PATH = r'/Users/david.callaghan/PycharmProjects/readMetadata/dropzone/MetadataWorkbook_sample.xlsx'
VALID_ADMIN_PATH = r'/Users/david.callaghan/PycharmProjects/readMetadata/dropzone/permissions_dev.yaml'


class Test_Build_Script(unittest.TestCase):

    def test_extract_table_metadata(self):
        res = obj(VALID_METADATA_PATH).extract_table_metadata()
        self.assertEqual(res.get(constant.DATABASE_NAMES_COLUMN_NM), 'sales')
        self.assertEqual(res.get(constant.TABLE_NAME_COLUMN_NM), 'test')

    def test_extract_table_metadata_invalid_database(self):
        res = obj(VALID_METADATA_PATH).extract_table_metadata()
        self.assertNotEqual(res.get(constant.DATABASE_NAMES_COLUMN_NM), '')
        self.assertEqual(res.get(constant.TABLE_NAME_COLUMN_NM), 'test')

    def test_extract_table_metadata_invalid_table(self):
        res = obj(VALID_METADATA_PATH).extract_table_metadata()
        self.assertEqual(res.get(constant.DATABASE_NAMES_COLUMN_NM), 'sales')
        self.assertNotEqual(res.get(constant.TABLE_NAME_COLUMN_NM), '')

    def test_extract_table_metadata_missing_file(self):
        with self.assertRaises(Exception):
            obj('VALID_METADATA_PATH').extract_table_metadata()

    def test_extract_column_metadata(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')

    def test_extract_column_metadata_invalid_name(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertNotEqual(res[constant.COLUMN_NAME_NM].iloc[0], '')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')

    def test_extract_column_metadata_invalid_description(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertNotEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], '')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')

    def test_extract_column_metadata_invalid_type(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertNotEqual(res[constant.COLUMN_TYPE_NM].iloc[0], '')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')

    def test_extract_column_metadata_invalid_position(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertNotEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 0)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')

    def test_extract_column_metadata_invalid_size(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertNotEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 0)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')

    def test_extract_column_metadata_invalid_required(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()

        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertNotEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'No')

    def test_extract_column_metadata_missing_file(self):
        with self.assertRaises(Exception):
            obj('VALID_METADATA_PATH').extract_column_metadata()

    def test_extract_column_metadata_size(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res.shape[0], 4)
        self.assertEqual(res.shape[1], 6)

    def test_build_sql_script(self):
        target = """CREATE OR REPLACE TABLE sales.test(
id INT(255) NOT NULL,
product VARCHAR(125) NOT NULL,
price DECIMAL NOT NULL,
purchased TIMESTAMP NOT NULL);"""

        sql = obj(VALID_METADATA_PATH).build_sql_script()

        self.assertAlmostEquals(sql, target)

    def test_extract_table_metadata(self):
        res = obj(VALID_ADMIN_PATH).extract_admin_commands()
        role = res.get('role')[0]
        self.assertEqual(role, "CREATE ROLE dev_role COMMENT='This is the developer role'")
