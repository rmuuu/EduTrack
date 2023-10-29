import mysql.connector as mysql
import logging

class Database:
    def __init__(self, db_config=None):
        if db_config is None:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "EduTrack"
            }
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connect(**self.db_config, buffered=True)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except mysql.Error as e:
            logging.error(f"Database query error: {e}")
            self.connection.rollback()
        finally:
            self.disconnect()
            return

    def fetch_all(self, query, params=None):
        self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.Error as e:
            logging.error(f"Database query error: {e}")
        finally:
            self.disconnect()

    def fetch_one(self, query, params=None):
        self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except mysql.Error as e:
            logging.error(f"Database query error: {e}")
        finally:
            self.disconnect()
            
    def setup_database(self):
        # Check if the database and tables exist, and create them if not
        try:
            self.connect()
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS EduTrack")
            self.cursor.execute("USE EduTrack")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    user_id VARCHAR(10) PRIMARY KEY,
                    email VARCHAR(100),
                    password VARCHAR(25),
                    role VARCHAR(10)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Students (
                    sr_code VARCHAR(10) PRIMARY KEY,
                    last_name VARCHAR(50),
                    given_name VARCHAR(50),
                    middle_name VARCHAR(50),
                    birth_date VARCHAR(50),
                    email VARCHAR(100),
                    program VARCHAR(50),
                    block VARCHAR(20), 
                    address VARCHAR(255),
                    contact_number VARCHAR(20),
                    eContact_name VARCHAR(50),
                    eContact_number VARCHAR(20)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Instructor (
                    emp_code VARCHAR(10) PRIMARY KEY,
                    last_name VARCHAR(50),
                    given_name VARCHAR(50),
                    middle_name VARCHAR(50),
                    birth_date VARCHAR(50),
                    email VARCHAR(100),
                    hdl_course VARCHAR(50),
                    hdl_block VARCHAR(20),
                    address VARCHAR(255),
                    contact_number VARCHAR(20),
                    eContact_name VARCHAR(50),
                    eContact_number VARCHAR(20)
                )
            """)
            # Add more table creation statements for other tables as needed
        except mysql.Error as e:
            # Log the error and raise a custom exception
            logging.error(f"Database setup error: {e}")
            raise DatabaseError("Error setting up the database.")
        finally:
            self.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
