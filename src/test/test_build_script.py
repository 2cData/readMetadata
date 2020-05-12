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
            obj('VALID_XLS_PATH').extract_table_metadata()

    def test_extract_column_metadata(self):
        res = obj(VALID_METADATA_PATH).extract_column_metadata()
        self.assertEqual(res[constant.COLUMN_NAME_NM].iloc[0], 'id')
        self.assertEqual(res[constant.COLUMN_DESCRIPTION_NM].iloc[0], 'unique id')
        self.assertEqual(res[constant.COLUMN_TYPE_NM].iloc[0], 'INT')
        self.assertEqual(res[constant.COLUMN_POSITION_NM].iloc[0], 1)
        self.assertEqual(res[constant.COLUMN_SIZE_NM].iloc[0], 255)
        self.assertEqual(res[constant.COLUMN_REQUIRED_NM].iloc[0], 'Yes')
