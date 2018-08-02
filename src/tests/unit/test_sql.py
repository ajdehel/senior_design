import logging
import unittest
from unittest import mock

from plumbintel import sql

logging.getLogger("PLUMBINTEL").setLevel(100)

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # mock pypyodbc.connect()
        self.patched_connect = mock.patch("pypyodbc.connect")
        self.mocked_connect = self.patched_connect.start()
        self.mocked_connection = mock.Mock()
        self.mocked_connect.return_value = self.mocked_connection
        # mock cursor
        self.mocked_cursor = mock.Mock()
        self.mocked_connection.cursor.return_value = self.mocked_cursor
        # mock execute
        self.mocked_execute = mock.Mock()
        self.mocked_cursor.execute = self.mocked_execute
        # config to reuse
        self.constructor_kwargs = ["driver", "server", "port", "database", "username", "password"]

    ### init tests
    def test_init__error_on_no_kwargs(self):
        with self.assertRaises(TypeError):
            test_db = sql.Database()

    def test_init__error_on_missing_kwargs(self):
        for key in self.constructor_kwargs:
            test_config = { key: f"TEST_{key}" for key in self.constructor_kwargs }
            test_config[key] = None
            with self.subTest(f"{key}=None"):
                with self.assertRaises(TypeError):
                    test_db = sql.Database()


    ### insert tests
    def test_insert_into__execute_called(self):
        test_config = { key: f"TEST_{key}" for key in self.constructor_kwargs }
        test_db = sql.Database(**test_config)
        values = ("TEST", "TEST", "TEST")
        test_db.insert("HelloTable", values)
        self.assertTrue(self.mocked_cursor.execute.called)

    def tearDown(self):
        self.patched_connect.stop()

if __name__ == "__main__":
    unittest.main()
