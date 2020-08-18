import os.path
import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self):
        self.db_name = "database.db"

    def check_file(self):
        return os.path.isfile(self.db_name)

    # Checks if db exists, creates it if not
    def setup_db(self):
        if not self.check_file():
            self.connect_db()
            self.create_table()

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    # Create table
    def create_table(self):
        sql_command = """
            CREATE TABLE files (
            file_number INTEGER PRIMARY KEY,
            title VARCHAR(50),
            description VARCHAR(200),
            email VARCHAR(100),
            filename VARCHAR(100),
            time VARCHAR(8));"""
        self.write_db(sql_command)

    # Run write command with command from write
    def write_db(self, command: str, *value):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command, *value)
        connection.commit()

    # Make full write command to
    def write(self, title: str, description: str, email: str, filename: str):
        time = datetime.now().strftime("%H:%M:%S")
        sql_command = """INSERT INTO files
        (file_number, title, description, email, filename, time)
        VALUES (NULL, ?, ?, ?, ?, ?);"""
        self.write_db(sql_command, (title, description, email, filename, time))

    # Run read command
    def read_db(self, command: str, *value):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command, *value)
        result = cursor.fetchall()
        return result

    # Read all files
    def read_all(self):
        data = "SELECT * FROM files"
        return self.read_db(data)
