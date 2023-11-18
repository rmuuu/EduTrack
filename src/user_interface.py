def show_main_menu():
    print("\nMain Menu:")
    print("1. View Schedule")
    print("2. View Grades")
    print("3. View Attendance")
    print("0. Exit")

def show_admin_menu():
    print("\nAdmin Menu:")
    print("1. Register Student")
    print("2. Employ Instructor")
    print("3. Attendance Monitoring")
    print("4. Grade Management")
    print("0. Exit")

def show_manage_attendance_menu():
    print("\nAttendance Menu:")
    print("1. View attendance")
    print("2. Mark attendance")
    print("0. Exit")

def show_manage_grades_menu():
    print("\nGrades Menu:")
    print("1. View grades")
    print("2. Input grades")
    print("0. Exit")

def show_admin_manage_students_menu():
    print("\nAdmin Manage Students Menu:")
    print("1. Add Students ")
    print("2. Delete Students ")
    print("3. Modify Students ")
    print("4. List Students ")
    print("0. Exit")

def show_admin_manage_instructor_menu():
    print("\nAdmin Manage Instructor Menu:")
    print("1. Add Instructor ")
    print("2. Delete Instructor ")
    print("3. Modify Instructor ")
    print("4. List Instructor ")
    print("0. Exit")

def show_admin_manage_users_display_list_menu():
    print("\nAdmin Manage Users Display List Menu:")
    print("1. Table form ")
    print("2. Key-value form ")
    print("0. Exit")

def show_admin_manage_users_list_menu_():
    print("\nAdmin Manage Users List Menu:")
    print("1. List Students")
    print("2. List Instructors")
    print("0. Exit")

def show_admin_manage_users_modify_menu():
    print("\nAdmin Manage Users Modify Menu:")
    print("1. Change ID")
    print("2. Change Password")
    print("3. Update Info")
    print("0. Exit")

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
        print("  7. Update Year Level")
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
        print("  6. Update Teaching")
        print("  7. Update Address")
        print("  8. Update Contact Number")
        print("  9. Update Emergency Contact Name")
        print(" 10. Update Emergency Contact Number")
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
    print("3. View Personal Info")
    print("0. Exit")

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

def manage_attendance_menu_prompt():
    show_manage_attendance_menu()
    return get_user_choice()

def manage_grades_menu_prompt():
    show_manage_grades_menu()
    return get_user_choice()

def admin_manage_users_students_prompt():
    show_admin_manage_students_menu()
    return get_user_choice()

def admin_manage_users_instructor_prompt():
    show_admin_manage_instructor_menu()
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
