import mysql.connector as mysql
db = mysql.connect(host="localhost",user="root",password="",database="EduTrack")
command_handler = db.cursor(buffered=True)

STUDENT = 'student'
TEACHER = 'teacher'

def authenticate_user(username, password):
    # Define the query parameters
    query_vals = (username, password)

    # Execute the SQL query to check if the user with the provided credentials exists
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s", query_vals)

    # Fetch the user record
    user_record = command_handler.fetchone()

    if user_record:
        # Extract the user's username and role from the query result
        username, role = user_record[1], user_record[3]
        return User(username, role)

    return None

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
