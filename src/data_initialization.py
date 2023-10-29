import models
import database
import authentication
from prettytable import PrettyTable
def add_student():
    student_info = models.Student.collect_student_input()
    new_student = models.Student(*student_info)
    
    query = "INSERT INTO Students (sr_code, last_name, given_name, middle_name, birth_date, email, program, block, address, contact_number, eContact_number, eContact_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (new_student.sr_code, new_student.last_name, new_student.given_name, new_student.middle_name, new_student.birth_date, new_student.email, new_student.program, new_student.block, new_student.address, new_student.contact_number, new_student.eContact_number, new_student.eContact_name)

    return query, values

def add_instrcutor():
    instructor_info = models.Instructor.collect_instructor_input()
    new_instructor = models.Instructor(*instructor_info)
    
    query = "INSERT INTO Instructor (emp_code, last_name, given_name, middle_name, birth_date, email, hdl_course, hdl_block, address, contact_number, eContact_number, eContact_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (new_instructor.emp_code, new_instructor.last_name, new_instructor.given_name, new_instructor.middle_name, new_instructor.birth_date, new_instructor.email, new_instructor.hdl_course, new_instructor.hdl_block, new_instructor.address, new_instructor.contact_number, new_instructor.eContact_number, new_instructor.eContact_name)
    
    return query, values

def search_user_id(user_id):
    with database.Database() as db:
        role_query = "SELECT Role FROM users WHERE user_id = %s"
        role_result = db.fetch_all(role_query, (user_id,))
        return role_result
            
def input_data(role):
    # Establish a connection to the database, initialization of user
    with database.Database() as db:
        if role == "student":
            new_user = add_student()
            
        else:
            new_user = add_instrutor()
        
        query, values = new_user
        
        user_id = values[0]
        email = values[5]
        password = values[0]
            
        success = db.execute_query(query,values)

        # Add the user information to the 'users' table
        query = "INSERT INTO users (user_id, email, Password, Role) VALUES (%s, %s, %s, %s)"
        values = (user_id, email, password, role)
        success = db.execute_query(query, values)

        if success:
            print(f"User {user_id} with role {role} added successfully.")
        else:
            print(f"Failed to add the user with role {role}.")   
             
def delete_data(user_id):
    with database.Database() as db:
        # Determine the role of the user
        role_result = search_user_id(user_id)
        
        if not role_result:
            print(f"User {user_id} not found.")
            return
        else:
            role = role_result[0][0]
            
            # Delete the user from the respective table based on their role
            if role == "student":
                # Delete the student
                db.execute_query("DELETE FROM Students WHERE sr_code = %s", (user_id,))
            elif role == "teacher":
                # Delete the instructor
                db.execute_query("DELETE FROM Instructor WHERE emp_code = %s", (user_id,))

            # Delete the user from the 'users' table
            db.execute_query("DELETE FROM users WHERE user_id = %s", (user_id,))
            print(f"User {user_id} deleted successfully.")

def update_user_id():
    with database.Database() as db:
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = authentication.authenticate_user(email, password)

        if user is None:
            print("Invalid credentials. Please try again.\n")
            return

        # Update the user's ID in the 'users' table and their role's table
        new_user_id = input("Enter the new ID: ")
        update_user_id_query = "UPDATE users SET user_id = %s WHERE email = %s AND password = %s"
        db.execute_query(update_user_id_query, (new_user_id, email, password))

        role = user[1]

        if role == "student":
            # Update student ID
            update_student_id_query = "UPDATE Students SET sr_code = %s WHERE email = %s"
            db.execute_query(update_student_id_query, (new_user_id, email))
        elif role == "teacher":
            # Update instructor ID
            update_instructor_id_query = "UPDATE Instructor SET emp_code = %s WHERE email = %s"
            db.execute_query(update_instructor_id_query, (new_user_id, email))

        print(f"User ID for user {email} updated successfully.")
        
def update_info():
    user_id = input("Enter the ID of the user to modify: ")
    with database.Database() as db:
        # Determine the role of the user
        role_result = search_user_id(user_id)

        if not role_result:
            print(f"User {user_id} not found.")
            return

        role = role_result[0][0]

        if role == "student":
            # Update student information
            program = input("Enter Program: ")
            block = input("Enter Block: ")
            updated_info = models.Person.collect_person_input()

            query = "UPDATE Students SET program = %s, block = %s, last_name = %s, given_name = %s, middle_name = %s, birth_date = %s, email = %s, address = %s, contact_number = %s, eContact_number = %s, eContact_name = %s WHERE sr_code = %s"
            update_values = (program, block, *updated_info, user_id)
            db.execute_query(query, update_values)

            print(f"User {user_id} information updated successfully.")

            # Print the updated information
            info_query = "SELECT * FROM Students WHERE sr_code = %s"
            print("Updated Student Information:")
            print(db.fetch_all(info_query, (user_id,)))

        elif role == "teacher":
            # Update instructor information
            hdl_course = input("Enter Handled Course: ")
            hdl_block = input("Enter Handled Block: ")
            updated_info = models.Person.collect_person_input()

            query = "UPDATE Instructor SET hdl_course = %s, hdl_block = %s, last_name = %s, given_name = %s, middle_name = %s, birth_date = %s, email = %s, address = %s, contact_number = %s, eContact_number = %s, eContact_name = %s WHERE emp_code = %s"
            update_values = (hdl_course, hdl_block, *updated_info, user_id)
            db.execute_query(query, update_values)

            print(f"User {user_id} information updated successfully.")

            # Print the updated information
            info_query = "SELECT * FROM Instructor WHERE emp_code = %s"
            print("Updated Instructor Information:")
            print(db.fetch_all(info_query, (user_id,)))


def update_password():
    user_id = input("Enter the ID of the user: ")
    with database.Database() as db:
        # Determine the role of the user
        role_result = search_user_id(user_id)

        if not role_result:
            print(f"User {user_id} not found.")
            return

        new_password = input("Enter the new password for the user: ")
        update_password_query = "UPDATE users SET Password = %s WHERE user_id = %s"
        db.execute_query(update_password_query, (new_password, user_id))
        
        # Print a confirmation message
        print(f"Password for user {user_id} updated successfully.")

def list_students():
    with database.Database() as db:
        # Fetch and display student information
        query = "SELECT * FROM Students"
        students = db.fetch_all(query)

        if students:
            table = PrettyTable()
            table.field_names = ["Student ID", "Last Name", "Given Name", "Middle Name", "Birth Date", "Email", "Program", "Block", "Address", "Contact Number", "Emergency Contact Name", "Emergency Contact Number"]

            for student in students:
                table.add_row([student[0], student[1], student[2], student[3], student[4], student[5], student[6], student[7], student[8], student[9], student[10], student[11]])

            print("List of Students:")
            print(table)
        else:
            print("No students found.")

def list_instructors():
    with database.Database() as db:
        # Fetch and display instructor information
        query = "SELECT * FROM Instructor"
        instructors = db.fetch_all(query)

        if instructors:
            table = PrettyTable()
            table.field_names = ["Instructor ID", "Last Name", "Given Name", "Middle Name", "Birth Date", "Email", "Handled Course", "Handled Block", "Address", "Contact Number", "Emergency Contact Name", "Emergency Contact Number"]

            for instructor in instructors:
                table.add_row([instructor[0], instructor[1], instructor[2], instructor[3], instructor[4], instructor[5], instructor[6], instructor[7], instructor[8], instructor[9], instructor[10], instructor[11]])

            print("List of Instructors:")
            print(table)
        else:
            print("No instructors found.")



































# """ import database

# def collect_user_input(field_names):
#     user_data = {}
#     for field in field_names:
#         value = input(f"Enter {field}: ")
#         user_data[field] = value
#     print("User data collected:", user_data)  # Debugging print
#     return user_data

# def collect_data_and_insert_to_db(table_name, field_names):
#     user_data = collect_user_input(field_names)
#     with database.Database() as db:
#         try:
#             columns = ", ".join(user_data.keys())
#             placeholders = ", ".join(["%s"] * len(user_data))
#             values = tuple(user_data.values())

#             query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#             success = db.execute_query(query, values)

#             if success:
#                 print(f"Data added to the {table_name} table successfully.")
#                 return user_data  # Return the user data
#             else:
#                 print(f"Failed to add data to the {table_name} table.")
#                 return None
#         except Exception as e:
#             db.connection.rollback()
#             print(f"An error occurred: {e}")

# def initialize_students_interactively():
#     student_fields = ["sr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "program", "block", "address", "contact_number", "eContact_number", "eContact_name"]
#     user_data = collect_data_and_insert_to_db("Students", student_fields)

#     if user_data:
#         user_id = user_data.get("sr_code")
#         password = user_data.get("sr_code")  # Set the password to sr_code

# def initialize_instructors_interactively():
#     instructor_fields = ["emp_code", "last_name", "given_name", "middle_name", "birth_date", "email", "hdl_course", "hdl_block", "address", "contact_number", "eContact_number", "eContact_name"]
#     user_data = collect_data_and_insert_to_db("Instructors", instructor_fields)

#     if user_data:
#         user_id = user_data.get("emp_code")
#         password = user_data.get("emp_code")  # Set the password to emp_code """
