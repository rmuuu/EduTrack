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

def show_admin_manage_users_display_list_menu():
    print("\nAdmin Manage Users Display List Menu:")
    print("1. Table form ")
    print("2. Key-value form ")
    print("3. Exit")
    
def show_admin_manage_users_list_menu_():
    print("\nAdmin Manage Users List Menu:")
    print("1. List Students")
    print("2. List Instructors")
    print("3. Exit")
    
def show_admin_manage_users_modify_menu():
    print("\nAdmin Manage Users Modify Menu:")
    print("1. Change ID")
    print("2. Change Password")
    print("3. Update Info")
    print("4. Exit")
    
def show_admin_manage_users_modify_update_info_menu(role):
    if role == "student":
        print("\nAdmin Manage Users Modify Update Info Menu:")
        print(" Update Student's Information:")
        print("  1. Update Last Name")
        print("  2. Update Given Name")
        print("  3. Update Middle Name")
        print("  4. Update Birth Date")
        print("  5. Update Email")
        print("  6. Update Program")
        print("  7. Update Block")
        print("  8. Update Address")
        print("  9. Update Contact Number")
        print(" 10. Update Emergency Contact Name")
        print(" 11. Update Emergency Contact Number")
        print("  0. Exit")
        
    elif role == "instructor":
        print("\nAdmin Manage Users Modify Update Info Menu:")
        print(" Update Instructor's Information:")
        print("  1. Update Last Name")
        print("  2. Update Given Name")
        print("  3. Update Middle Name")
        print("  4. Update Birth Date")
        print("  5. Update Email")
        print("  6. Update Hdl Course")
        print("  7. Update Hdl Block")
        print("  8. Update Address")
        print("  9. Update Contact Number")
        print(" 10. Update Emergency Contact Name")
        print(" 11. Update Emergency Contact Number")
        print("  0. Exit")

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

def admin_manage_users_display_list_menu_prompt():
    show_admin_manage_users_display_list_menu()
    return get_user_choice()

def admin_manage_users_list_menu_prompt():
    show_admin_manage_users_list_menu_()
    return get_user_choice()

def admin_manage_users_modify_menu_prompt():
    show_admin_manage_users_modify_menu()
    return get_user_choice()

def admin_manage_users_modify_update_info_menu_prompt(role):
    show_admin_manage_users_modify_update_info_menu(role)
    return get_user_choice()

def teacher_menu_prompt():
    show_teacher_menu()
    return get_user_choice()

def student_menu_prompt():
    show_student_menu()
    return get_user_choice()
