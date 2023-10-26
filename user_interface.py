def show_main_menu():
    print("\nMain Menu:")
    print("1. View Schedule")
    print("2. View Grades")
    print("3. View Attendance")
    print("4. Exit")

def show_admin_menu():
    print("\nAdmin Menu:")
    print("1. User Management")
    print("2. Class Management")
    print("3. Attendance Monitoring")
    print("4. Grade Management")
    print("5. Schedule Management")
    print("6. Exit")

def show_admin_manage_users_menu():
    print("\nAdmin Manage Users Menu:")
    print("1. Add User ")
    print("2. Delete User ")
    print("3. Modify User ")
    print("4. List Users ")
    print("5. Exit")

def show_teacher_menu():
    print("\nTeacher Menu:")
    print("1. Mark Attendance")
    print("2. Input Grades")
    print("3. View Class Schedule")
    print("4. Exit")

def show_student_menu():
    print("\nStudent Menu:")
    print("1. View Grades")
    print("2. View Attendance")
    print("3. View Class Schedule")
    print("4. Exit")

def get_user_choice():
    try:
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        return None

def main_menu_prompt():
    show_main_menu()
    return get_user_choice()

def admin_menu_prompt():
    show_admin_menu()
    return get_user_choice()

def admin_manage_users_menu_prompt():
    show_admin_manage_users_menu()
    return get_user_choice()

def teacher_menu_prompt():
    show_teacher_menu()
    return get_user_choice()

def student_menu_prompt():
    show_student_menu()
    return get_user_choice()
