#database.py
import mysql.connector as mysql
import logging
from contextlib import ContextDecorator
import models

# Custom exception for database errors
class DatabaseError(Exception):
    pass

# Custom Database class with additional features
class Database(ContextDecorator):
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
        try:
            if self.connection:
                self.connection.close()
        except mysql.Error as e:
            logging.error(f"Error while disconnecting from the database: {e}")
            raise DatabaseError("Error disconnecting from the database.")

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
            pass

    def fetch_all(self, query, params=None):
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

    def fetch_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
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
            self.create_instructors_table()
            self.create_students_table()
            self.create_users_table()
            self.create_attendance_table()
            self.create_program_table()
            self.create_grades_table()
        except mysql.Error as e:
            # Log the error and raise a custom exception
            logging.error(f"Database setup error: {e}")
            raise DatabaseError("Error setting up the database.")
        finally:
            self.disconnect()

    def create_instructors_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS Instructors (
                itr_code VARCHAR(10) PRIMARY KEY,
                last_name VARCHAR(50) NOT NULL,
                given_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50) NOT NULL,
                birth_date DATE NOT NULL,
                email VARCHAR(100) NOT NULL,
                teaching VARCHAR(50) NOT NULL, 
                address VARCHAR(255) NOT NULL,
                contact_number VARCHAR(20) NOT NULL,
                eContact_name VARCHAR(50) NOT NULL,
                eContact_number VARCHAR(20) NOT NULL
            )
        """
        self.execute_query(query)

    def create_students_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS Students (
                sr_code VARCHAR(10) PRIMARY KEY,
                last_name VARCHAR(50) NOT NULL,
                given_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50) NOT NULL,
                birth_date DATE NOT NULL,
                email VARCHAR(100) NOT NULL,
                program VARCHAR(50) NOT NULL,
                year_lvl VARCHAR(20) NOT NULL, 
                semester VARCHAR(20) NOT NULL, 
                address VARCHAR(255) NOT NULL,
                contact_number VARCHAR(20) NOT NULL,
                eContact_name VARCHAR(50) NOT NULL,
                eContact_number VARCHAR(20) NOT NULL
            )
        """
        self.execute_query(query)

    def create_users_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS Users (
                user_id VARCHAR(10) PRIMARY KEY,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(25) NOT NULL,
                role VARCHAR(10) NOT NULL
            )
        """
        self.execute_query(query)

    def create_attendance_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS Attendance (
                att_id VARCHAR(20) PRIMARY KEY,
                sr_code VARCHAR(10), FOREIGN KEY (sr_code) REFERENCES Students(sr_code),
                username VARCHAR(255) NOT NULL,
                date DATE NOT NULL,
                status VARCHAR(10)
            )
        """
        self.execute_query(query)

    def create_program_table(self):
        try:
            self.execute_query("""
                CREATE TABLE IF NOT EXISTS Program (
                    class_id INT AUTO_INCREMENT PRIMARY KEY,
                    sr_code VARCHAR(10),
                    FOREIGN KEY (sr_code) REFERENCES Students(sr_code),
                    program VARCHAR(255) NOT NULL
                )
            """)
        except mysql.Error as e:
            logging.error(f"Error creating Program table: {e}")
            raise DatabaseError("Error creating Program table.")
        
    def create_grades_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Grades (
                    grade_id INT AUTO_INCREMENT PRIMARY KEY,
                    sr_code VARCHAR(10), FOREIGN KEY (sr_code) REFERENCES Students(sr_code),
                    username VARCHAR(255) NOT NULL,
                    course VARCHAR(255),
                    grade INT NOT NULL
                )
            """)
        except mysql.Error as e:
            logging.error(f"Error creating Grades table: {e}")
            raise DatabaseError("Error creating Grades table.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        
    def class_exists(self, program):
        query = "SELECT COUNT(*) FROM Program WHERE program = %s"
        params = (program,)
        result = self.fetch_one(query, params)
        return result[0] > 0

    def get_students_in_class(self, program):
        program = program
        query = "SELECT CONCAT(last_name, ', ', given_name) AS username, sr_code FROM Students WHERE program = %s"
        params = (program,)
        result = self.fetch_all(query, params)
        return result

    def mark_attendance(self, program, date, attendance_list):
        try:
            att_id = f"{program}_{date}"
            for student_info in attendance_list:
                username, sr_code, date, attendance_status = student_info
                query = """
                    INSERT INTO Attendance (att_id, username, sr_code, date, status)
                    VALUES (%s, %s, %s, %s, %s)
                """
                params = (att_id, username, sr_code, date, attendance_status)
                self.execute_query(query, params)
                print("Attendance marked successfully.")
        except Exception as e:
            print(f"Error marking attendance: {e}")

    def get_attendance(self, program, date):
        att_id = f"{program}_{date}"
        query = "SELECT username, status FROM Attendance WHERE att_id = %s"
        params = (att_id,)
        result = self.fetch_all(query, params)
        return result

    def input_grades(self, grades_list):
        try:
            for username, sr_code, course, grade in grades_list:
                query = """
                    INSERT INTO Grades (username, sr_code, course, grade)
                    VALUES (%s, %s, %s, %s)
                """
                params = (username, sr_code, course, grade)
                self.execute_query(query, params)
                print("Grade marked successfully.")
        except Exception as e:
            print(f"Error marking grade: {e}")

    def get_student_grades(self, sr_code, course):
        query = """
            SELECT course, grade
            FROM Grades
            WHERE sr_code = %s AND course = %s
        """
        params = (sr_code, course)
        return self.fetch_all(query, params)
