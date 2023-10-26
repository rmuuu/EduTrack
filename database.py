import mysql.connector as mysql
import logging

# Custom exception for database errors
class DatabaseError(Exception):
    pass

# Custom Database class with additional features
class Database:
    def __init__(self, db_config=None):
        if db_config is None:
            # Use default configuration if not provided
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "EduTrack"
            }
        self.db_config = db_config
        self.connection = None
        self.cursor = None

        # Set up logging
        logging.basicConfig(filename='database.log', level=logging.INFO)

        # Automatically create the database and tables if they don't exist
        self.setup_database()

    def connect(self):
        try:
            self.connection = mysql.connect(**self.db_config, buffered=True)
            self.cursor = self.connection.cursor()
        except mysql.Error as e:
            # Log the error and raise a custom exception
            logging.error(f"Database connection error: {e}")
            raise DatabaseError("Unable to connect to the database.")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except mysql.Error as e:
            # Log the error and raise a custom exception
            logging.error(f"Database query error: {e}")
            self.connection.rollback()
            raise DatabaseError("Error executing the database query.")

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.Error as e:
            # Log the error and raise a custom exception
            logging.error(f"Database query error: {e}")
            raise DatabaseError("Error fetching data from the database.")

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
