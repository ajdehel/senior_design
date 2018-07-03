import logging
import pypyodbc

LOGGER = logging.getLogger("PLUMBINTEL")

class Database:

    def __init__(self, driver=None, server=None, port=None,
                 database=None, username=None, password=None, **kwargs):
        connection_string = (f"DRIVER={{{driver}}};SERVER={server};PORT={port};"
                             f"DATABASE={database};UID={username};PWD={password}")
        LOGGER.debug(connection_string)
        self.connection = pypyodbc.connect(connection_string, **kwargs)
        LOGGER.info("Connection Succeeded.")

    def __enter__(self):
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        if e_type:
            LOGGER.error(str(e_type))
        self.connection.close()

    def validate(self, json):
        """Ensure new data is valid for the database."""
        pass

    def update(self, table_name, values, columns=""):
        """Method to update data in a given table.
            will also insert new data into the table if the first
            column item in values is not found in the database.
        """
        self._insert(table_name, values, columns)

    def _insert(self, table_name, values, columns=""):
        """Underlying method to insert new values into a given data."""
        col_string = ""
        if columns != "":
            columns = ", ".join(columns)
            col_string = f"({columns})"
        values = ", ".join([ "'"+str(value)+"'" if type(value) is str else str(value) for value in values ])
        val_string = f"({values})"
        insert_string = f"INSERT INTO {table_name} {col_string} VALUES {val_string};"
        LOGGER.debug(insert_string)
        try:
            with self.connection.cursor().execute(insert_string):
                LOGGER.info("Insert Succeeded.")
        except pypyodbc.DataError as error:
            LOGGER.error(error)

    def _update(self, table_name, values, clause, columns):
        """Underlying method to update an existing entry in a given table."""

    @property
    def connected(self):
        return self.connection.connected
