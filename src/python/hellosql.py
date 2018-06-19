import sql
import unittest
from unittest import mock

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.mocked_Connection = mock.Mock()
        self.mocked_Cursor = mock.Mock()
        self.patched_Connect = mock.patch("pypyodbc.connect")
        self.patched_Connect.start()
        self.mocked_Connect = self.patched_Connect.start()
        self.mocked_Connect.return_value = self.mocked_Connection
        self.mocked_Connection.cursor.return_value = self.mocked_Cursor

    def test__insert_into__with_columns(self):
        db = sql.Database()
        values = (1, 14.0, 0)
        columns = ("deviceID", "metricA", "metricB")
        db.insert_into("HelloTable", values, columns=columns)
        print(self.mocked_Cursor.execute.call_args)

    def test__insert_into__without_columns(self):
        db = sql.Database()
        values = (1, 14.0, 0)
        db.insert_into("HelloTable", values)
        print(self.mocked_Cursor.execute.call_args)

    def tearDown(self):
        self.patched_Connect.stop()

if __name__ == "__main__":
    unittest.main()
