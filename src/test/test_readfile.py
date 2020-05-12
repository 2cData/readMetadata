import unittest
from main.read_file import ReadFile
import main.constant as constant

VALID_CSV_PATH = r'../../dropzone/test.csv'
VALID_XLS_PATH = r'/Users/david.callaghan/PycharmProjects/readMetadata/dropzone/MetadataWorkbook_sample.xlsx'

class Test_ReadFile(unittest.TestCase):

    def test_extract_metadata(self):
        res = ReadFile(VALID_XLS_PATH).extract_table_metadata()
        self.assertEqual(res.get(constant.DATABASE_NAMES_COLUMN_NM), 'sales')
        self.assertEqual(res.get(constant.TABLE_NAME_COLUMN_NM), 'test')

    def test_extract_metadata_invalid_database(self):
        res = ReadFile(VALID_XLS_PATH).extract_table_metadata()
        self.assertNotEqual(res.get(constant.DATABASE_NAMES_COLUMN_NM), '')
        self.assertEqual(res.get(constant.TABLE_NAME_COLUMN_NM), 'test')

    def test_extract_metadata_invalid_table(self):
        res = ReadFile(VALID_XLS_PATH).extract_table_metadata()
        self.assertEqual(res.get(constant.DATABASE_NAMES_COLUMN_NM), 'sales')
        self.assertNotEqual(res.get(constant.TABLE_NAME_COLUMN_NM), '')

    def test_extract_metadata_missing_file(self):
        with self.assertRaises(Exception):
            ReadFile('VALID_XLS_PATH').extract_table_metadata()
