import models
import database
import authentication
import user_interface
from prettytable import PrettyTable

def add_user(role, user_info):
    table_name = "Students" if role == "student" else "Instructors"
    fields = ["sr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "program", "year_lvl", "address", "contact_number", "eContact_number", "eContact_name"] if role == "student" else ["itr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "teaching", "address", "contact_number", "eContact_number", "eContact_name"]

    query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))})"
    values = tuple(user_info[fields.index(field)] for field in fields)

    return query, values

def input_data(role):
    user_info = models.Student.collect_student_input() if role == "student" else models.Instructor.collect_instructor_input()

    with database.Database() as db:
        new_user = add_user(role, user_info)
        query, values = new_user

        user_id = values[0]
        email = values[5]
        password = values[0]
        program = values[6]

        success = db.execute_query(query, values)
        
        if role == "student":
            # Set the query and values for the Courses table
            course_query = "INSERT INTO Program (program, sr_code) VALUES (%s,%s)"
            course_values = (program,user_id)
            # Execute the query for the Courses table
            success_course = db.execute_query(course_query, course_values)
        
        
        # Set the query and values for the users table
        user_query = "INSERT INTO users (user_id, email, Password, Role) VALUES (%s, %s, %s, %s)"
        user_values = (user_id, email, password, role)
        # Execute the query for the users table
        success_user = db.execute_query(user_query, user_values)

        if success and success_user:
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
            table_name = "Students" if role == "student" else "Instructors"

            # Delete the user from the respective table based on their role
            db.execute_query("DELETE FROM {table_name} WHERE {column_name} = %s".format(table_name=table_name, column_name='sr_code' if role == 'student' else 'itr_code'), (user_id,))


            # Delete the user from the 'users' table
            db.execute_query("DELETE FROM users WHERE user_id = %s", (user_id,))
            print(f"User {user_id} deleted successfully.")

def search_user_id(user_id):
    with database.Database() as db:
        role_query = "SELECT Role FROM users WHERE user_id = %s"
        role_result = db.fetch_all(role_query, (user_id,))
        return role_result

def update_id(user_id, email, role):
    new_user_id = input(f"Enter the {role}'s new ID: ")
    with database.Database() as db:
        table_name = "Students" if role == "student" else "Instructor"

        # Update user's ID in the 'users' table
        update_user_id_query = "UPDATE users SET user_id = %s WHERE email = %s"
        db.execute_query(update_user_id_query, (new_user_id, email))

        # Update the ID in the role's table
        query = "UPDATE {table_name} SET {column_name} = %s WHERE email = %s".format(table_name=table_name,column_name='sr_code' if role == 'student' else 'itr_code')
        
        db.execute_query(query, (new_user_id, email))
        print(f"User ID for user {email} updated successfully.")

def update_user_id():
    with database.Database() as db:
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = authentication.authenticate_user(email, password)

        if user is None:
            print("Invalid credentials. Please try again.\n")
            return

        update_id(user[0], email, user[1])

def update_field(user_id, role, field_name, choice):
    new_value = input(f"Enter the new {field_name}: ")
    table_name = "Students" if role == "student" else "Instructors"

    with database.Database() as db:
        # Check that the field_name corresponds to a valid field in the table
        valid_fields = {
            "last_name", "given_name", "middle_name", "birth_date", "email",
            "program", "year_lvl", "address", "contact_number", "eContact_name", "eContact_number",
            "teaching"
        }
        if field_name in valid_fields:
            query = "UPDATE {table_name} SET {field_name} = %s WHERE {column_name} = %s".format(table_name=table_name,field_name = field_name, column_name = 'sr_code' if role == 'student' else 'itr_code')
            
            db.execute_query(query, (new_value, user_id))
            if choice == 5:
                update_user_email_query = "UPDATE users SET email = %s WHERE user_id = %s"
                db.execute_query(update_user_email_query, (new_value, user_id))
            print(f"{field_name.capitalize()} updated successfully.")
        else:
            print(f"{field_name} is not a valid field for {table_name}.")

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
            fields = ["last_name", "given_name", "middle_name", "birth_date", "email", "program", "year_lvl", "address", "contact_number", "eContact_name", "eContact_number"]
        elif role == "instructor":
            fields = ["last_name", "given_name", "middle_name", "birth_date", "email", "teaching", "address", "contact_number", "eContact_name", "eContact_number"]

        while True:
            choice = user_interface.admin_manage_users_modify_update_info_menu_prompt(role)
            if choice == 0:
                break
            elif 1 <= choice <= len(fields):
                update_field(user_id, role, fields[choice - 1], choice)

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

def display_as_table(data, role):
    fields = ["sr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "program", "year_lvl", "address", "contact_number", "eContact_number", "eContact_name"] if role == "student" else ["itr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "teaching", "address", "contact_number", "eContact_number", "eContact_name"]
    
    table = PrettyTable()
    table.field_names = [f"{role.capitalize()} ID"] + fields

    for item in data:
        # Ensure that the number of fields matches the number of elements in the item
        if len(fields) == len(item) - 1:  # Subtract 1 for the role ID
            table.add_row([item[0]] + list(item[1:]))
        else:
            print(f"Error: Incorrect number of fields for {role} ID {item[0]}. Skipping row.")
    
    print(f"List of {role.capitalize()}s:")
    print(table)


def display_as_key_value(data, role):
    fields = ["sr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "program", "year_lvl", "address", "contact_number", "eContact_name", "eContact_number"] if role == "student" else ["itr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "teaching", "address", "contact_number", "eContact_name", "eContact_number"]

    if not data or not fields:
        print(f"No {role}s found.")
        return

    for i, item in enumerate(data):
        print(f"\n{role.capitalize()} {i + 1}:")
        for j, field in enumerate(item):
            # Check if the index is within the range of fields
            if 0 <= j < len(fields):
                print(f"  {fields[j]}: {field}")

def list_students(display_format):
    with database.Database() as db:
        query = "SELECT * FROM Students"
        students = db.fetch_all(query)

        if students:
            if display_format == "table":
                display_as_table(students, "student")
            elif display_format == "key-value":
                display_as_key_value(students, "student")
        else:
            print("No students found.")

def list_instructors(display_format):
    with database.Database() as db:
        query = "SELECT * FROM Instructors"
        instructors = db.fetch_all(query)

        if instructors:
            if display_format == "table":
                display_as_table(instructors, "instructor")
            elif display_format == "key-value":
                display_as_key_value(instructors, "instructor")
        else:
            print("No instructors found.")
