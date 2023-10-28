import user_interface
import database
import models
import data_initialization

def admin_menu(user):
    while True:
        choice = user_interface.admin_menu_prompt()
        
        if choice == 1:
            manage_users()
        elif choice == 2:
            manage_classes()
        elif choice == 3:
            manage_attendance()
        elif choice == 4:
            manage_grades()
        elif choice == 5:
            manage_schedule()
        elif choice == 6:
            break

def manage_users():
    while True:
        choice = user_interface.admin_manage_users_menu_prompt()
        
        if choice == 1:
            add_user()
        elif choice == 2:
            delete_user()
        elif choice == 3:
            modify_user()
        elif choice == 4:
            list_users()
        elif choice == 5:
            break

def add_user():
    role = input("Enter the user's role (teacher/student): ")
    if role in ["teacher", "student"]:
        data_initialization.input_data(role)
    else:
        print("Invalid role. Please enter 'teacher' or 'student'.")

def delete_user():
    user_id = input("Enter the ID of the user to delete:")
    data_initialization.delete_data(user_id)

def modify_user():
    user_id = input("Enter the ID of the user to modify: ")
    
    # Establish a connection to the database
    with database.Database() as db:
        # Determine the role of the user
        role_result = data_initialization.search_user_id(user_id)

        if not role_result:
            print(f"User {user_id} not found.")
            return

        role = role_result[0][0]

        if role == "student":
            # Update student information
            updated_info = data_initialization.add_student()
            query = "UPDATE Students SET last_name = %s, given_name = %s, middle_name = %s, birth_date = %s, email = %s, program = %s, block = %s, address = %s, contact_number = %s, eContact_number = %s, eContact_name = %s WHERE sr_code = %s"
            update_values = (*updated_info, user_id)
            db.execute_query(query, update_values)
        elif role == "teacher":
            # Update instructor information
            updated_info = data_initialization.add_instrcutor()
            query = "UPDATE Instructor SET last_name = %s, given_name = %s, middle_name = %s, birth_date = %s, email = %s, hdl_course = %s, hdl_block = %s, address = %s, contact_number = %s, eContact_number = %s, eContact_name = %s WHERE emp_code = %s"
            update_values = (*updated_info, user_id)
            db.execute_query(query, update_values)
        
        print(f"User {user_id} information updated successfully.")
        
        # Update the user's role in the 'users' table (if necessary)
        if role == "student":
            # Update student password
            new_password = input("Enter the new password for the student: ")
            update_password_query = "UPDATE Students SET Password = %s WHERE sr_code = %s"
            db.execute_query(update_password_query, (new_password, user_id))
        elif role == "teacher":
            # Update instructor password
            new_password = input("Enter the new password for the instructor: ")
            update_password_query = "UPDATE Instructor SET Password = %s WHERE emp_code = %s"
            db.execute_query(update_password_query, (new_password, user_id))
        
        # Print a confirmation message
        print(f"Password for user {user_id} updated successfully.")

        # Print the updated information
        if role == "student":
            updated_student_info = data_initialization.search_student(user_id)
            print("Updated Student Information:")
            data_initialization.display_student_info(updated_student_info)
        elif role == "teacher":
            updated_instructor_info = data_initialization.search_instructor(user_id)
            print("Updated Instructor Information:")
            data_initialization.display_instructor_info(updated_instructor_info)


def list_users():
    user_id = input("Enter the ID of the user to list: ")

    # Establish a connection to the database
    with database.Database() as db:
        # Determine the role of the user
        role_query = "SELECT Role FROM users WHERE user_id = %s"
        role_result = db.fetch_all(role_query, (user_id))

        if not role_result:
            print(f"User {user_id} not found.")
            return

        role = role_result[0][0]

        if role == "student":
            # Fetch and display the list of students
            user_list_query = "SELECT sr_code FROM Students"
        elif role == "teacher":
            # Fetch and display the list of instructors
            user_list_query = "SELECT emp_code FROM Instructor"

        user_list = db.fetch_all(user_list_query)

        if user_list:
            print(f"List of {role.capitalize()}/s:")
            for user_id in user_list:
                print(f"User ID: {user_id[0]}")
        else:
            print(f"No {role}s found.")

def manage_classes():
    while True:
        class_choice = user_interface.manage_classes_menu()
        
        if class_choice == 1:
            create_class()
        elif class_choice == 2:
            edit_class()
        elif class_choice == 3:
            delete_class()
        elif class_choice == 4:
            list_classes()
        elif class_choice == 5:
            break

def create_class():
    class_name = input("Enter the name of the new class: ")
    teacher_name = input("Enter the name of the teacher for this class: ")
    
    # Create a new class in the database using the database module
    if database.add_class(class_name, teacher_name):
        print(f"Class {class_name} with teacher {teacher_name} created successfully.")
    else:
        print(f"Class {class_name} already exists.")

def edit_class():
    class_name = input("Enter the name of the class to edit: ")
    
    # Check if the class exists
    if database.class_exists(class_name):
        new_teacher_name = input("Enter the name of the new teacher for this class: ")
        
        # Modify the class's teacher in the database using the database module
        database.modify_class_teacher(class_name, new_teacher_name)
        print(f"Teacher of class {class_name} updated to {new_teacher_name}.")
    else:
        print(f"Class {class_name} not found.")

def delete_class():
    class_name = input("Enter the name of the class to delete: ")
    
    # Delete the class from the database using the database module
    if database.delete_class(class_name):
        print(f"Class {class_name} deleted successfully.")
    else:
        print(f"Class {class_name} not found.")

def list_classes():
    # List all classes from the database using the database module
    classes = database.get_all_classes()
    print("List of classes:")
    for class_info in classes:
        print(f"Class Name: {class_info.class_name}, Teacher: {class_info.teacher_name}")

def manage_attendance():
    while True:
        attendance_choice = user_interface.manage_attendance_menu()
        
        if attendance_choice == 1:
            mark_attendance()
        elif attendance_choice == 2:
            view_attendance()
        elif attendance_choice == 3:
            break

def mark_attendance():
    class_name = input("Enter the name of the class for which you want to mark attendance: ")
    date = input("Enter the date for which you want to mark attendance (YYYY-MM-DD): ")
    
    # Check if the class exists
    if database.class_exists(class_name):
        students = database.get_students_in_class(class_name)
        
        # Initialize an empty attendance list
        attendance_list = []
        
        # Mark attendance for each student
        for student in students:
            attendance_status = input(f"Is {student.username} present? (yes/no): ")
            attendance_list.append((student.username, date, attendance_status))
        
        # Save the attendance data in the database using the database module
        database.mark_attendance(class_name, date, attendance_list)
        print("Attendance marked successfully.")
    else:
        print(f"Class {class_name} not found.")

def view_attendance():
    class_name = input("Enter the name of the class for which you want to view attendance: ")
    
    # Check if the class exists
    if database.class_exists(class_name):
        date = input("Enter the date for which you want to view attendance (YYYY-MM-DD): ")
        
        # Retrieve the attendance data from the database using the database module
        attendance_data = database.get_attendance(class_name, date)
        
        if attendance_data:
            print("Attendance for class:", class_name, "on date:", date)
            for student, status in attendance_data:
                print(f"{student}: {status}")
        else:
            print("No attendance data found for the specified date.")
    else:
        print(f"Class {class_name} not found.")

def manage_grades():
    while True:
        grades_choice = user_interface.manage_grades_menu()
        
        if grades_choice == 1:
            input_grades()
        elif grades_choice == 2:
            view_grades()
        elif grades_choice == 3:
            break

def input_grades():
    class_name = input("Enter the name of the class for which you want to input grades: ")
    
    # Check if the class exists
    if database.class_exists(class_name):
        students = database.get_students_in_class(class_name)
        
        # Initialize an empty grades list
        grades_list = []
        
        # Input grades for each student
        for student in students:
            grade = input(f"Enter the grade for {student.username}: ")
            grades_list.append((student.username, class_name, grade))
        
        # Save the grades data in the database using the database module
        database.input_grades(grades_list)
        print("Grades inputted successfully.")
    else:
        print(f"Class {class_name} not found.")

def view_grades():
    class_name = input("Enter the name of the class for which you want to view grades: ")
    
    # Check if the class exists
    if database.class_exists(class_name):
        student_name = input("Enter the username of the student: ")
        
        # Retrieve the student's grades from the database using the database module
        student_grades = database.get_student_grades(student_name, class_name)
        
        if student_grades:
            print(f"Grades for {student_name} in class {class_name}:")
            for grade in student_grades:
                print(f"{grade[0]}: {grade[1]}")
        else:
            print("No grades found for the specified student.")
    else:
        print(f"Class {class_name} not found.")

def manage_schedule():
    while True:
        schedule_choice = user_interface.manage_schedule_menu()
        
        if schedule_choice == 1:
            view_class_schedule()
        elif schedule_choice == 2:
            break

def view_class_schedule():
    class_name = input("Enter the name of the class for which you want to view the schedule: ")
    
    # Check if the class exists
    if database.class_exists(class_name):
        class_schedule = database.get_class_schedule(class_name)
        
        if class_schedule:
            print(f"Class schedule for {class_name}:")
            for schedule in class_schedule:
                print(f"Day: {schedule[0]}, Time: {schedule[1]}, Subject: {schedule[2]}")
        else:
            print("No schedule found for the specified class.")
    else:
        print(f"Class {class_name} not found.")
