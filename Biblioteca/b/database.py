# database.py
import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '1234',
            'host': 'localhost',
            'database': 'biblioteca_escolar'
        }

    def connect(self):
        return mysql.connector.connect(**self.config)

    def execute_query(self, query, params=None):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor
        except mysql.connector.Error as error:
            print(f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def call_procedure(self, proc_name, params):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            cursor.callproc(proc_name, params)
            connection.commit()
            return cursor
        except mysql.connector.Error as error:
            print(f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()