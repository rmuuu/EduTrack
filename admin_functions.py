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
        # Establish a connection to the database, initialization of user
        with database.Database() as db:
            if role == "student":
                new_user = data_initialization.add_student()
                
            else:
                new_user = data_initialization.add_instrcutor()
            
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
    else:
        print("Invalid role. Please enter 'teacher' or 'student'.")

def delete_user():
    user_id = input("Enter the ID of the user to delete:")
    
    # Establish a connection to the database
    with database.Database() as db:
        # Determine the role of the user
        role_query = "SELECT Role FROM users WHERE user_id = %s"
        role_result = db.fetch_data(role_query, (user_id,))
        
        if not role_result:
            print(f"User {user_id} not found.")
        else:
            role = role_result[0]
            user_role = role[0]
            
            # Delete the user from the respective table based on their role
            if user_role == "student":
                # Delete the student
                db.execute_query("DELETE FROM Students WHERE sr_code = %s", (user_id,))
            elif user_role == "teacher":
                # Delete the instructor
                db.execute_query("DELETE FROM Instructor WHERE emp_code = %s", (user_id,))
        
            # Delete the user from the 'users' table
            db.execute_query("DELETE FROM users WHERE user_id = %s", (user_id,))
            print(f"User {user_id} deleted successfully.")

def modify_user():
    user_id = input("Enter the ID of the user to modify: ")

    # Establish a connection to the database
    with database.Database() as db:
        # Determine the current role of the user
        current_role_query = "SELECT Role FROM users WHERE user_id = %s"
        current_role_result = db.fetch_data(current_role_query, (user_id))

        if not current_role_result:
            print(f"User {user_id} not found.")
            return

        current_role = current_role_result[0][0]

        if current_role == "student":
            # Update the student's role in the 'Students' table
            update_role_query = "UPDATE Students SET role = %s WHERE sr_code = %s"
            db.execute_query(update_role_query, ("teacher", user_id))
        elif current_role == "teacher":
            # Update the instructor's role in the 'Instructor' table
            update_role_query = "UPDATE Instructor SET role = %s WHERE emp_code = %s"
            db.execute_query(update_role_query, ("student", user_id))
        
        # Update the user's role in the 'users' table
        update_role_query = "UPDATE users SET Role = %s WHERE user_id = %s"
        db.execute_query(update_role_query, ("teacher" if current_role == "student" else "student", user_id))
        print(f"User {user_id} role updated successfully.")

def list_users():
    user_id = input("Enter the ID of the user to list: ")

    # Establish a connection to the database
    with database.Database() as db:
        # Determine the role of the user
        role_query = "SELECT Role FROM users WHERE user_id = %s"
        role_result = db.fetch_data(role_query, (user_id))

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

        user_list = db.fetch_data(user_list_query)

        if user_list:
            print(f"List of {role.capitalize()}s:")
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
