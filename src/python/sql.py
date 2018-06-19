import pypyodbc
import logging

CONNECTION_STRING = ''

class Database:

    def __init__(self, connection_string=CONNECTION_STRING):
        self.connection = pypyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self.cursor.close()
        self.connection.close()

    def validate(self, json):
        """Ensure new data is valid for the database."""
        pass

    def insert_into(self, table_name, values, columns=""):
        """Method to insert data into a given table."""
        col_string = ""
        if columns != "":
            columns = ", ".join(columns)
            col_string = f"({columns})"
        values = ", ".join([str(value) for value in values])
        val_string = f"({values})"
        self.cursor.execute(f"INSERT INTO {table_name} {col_string} VALUES {val_string}")

