import user_interface
import data_initialization
import database
import models

class AdminManager:
    def admin_menu(self):
        while True:
            choice = user_interface.admin_menu_prompt()
            
            if choice == 1:
                self.manage_student()
            elif choice == 2:
                self.manage_instructor()
            elif choice == 3:
                self.manage_attendance()
            elif choice == 4:
                self.manage_grades()
            elif choice == 0:
                break

    def manage_student(self):
        while True:
            choice = user_interface.admin_manage_users_students_prompt()
            
            if choice == 1:
                self.add_student()
            elif choice == 2:
                self.delete_student()
            elif choice == 3:
                self.modify_user()
            elif choice == 4:
                self.dis_student()
            elif choice == 0:
                break

    def manage_instructor(self):
        while True:
            choice = user_interface.admin_manage_users_instructor_prompt()
            
            if choice == 1:
                self.add_instructor()
            elif choice == 2:
                self.delete_instructor()
            elif choice == 3:
                self.modify_user()
            elif choice == 4:
                self.dis_instructor()
            elif choice == 0:
                break

    def add_student(self):
        data_initialization.input_data("student")

    def add_instructor(self):
        data_initialization.input_data("instructor")

    def delete_student(self):
        user_id = input("Enter the ID of the student to delete:")
        data_initialization.delete_data(user_id)

    def delete_instructor(self):
        user_id = input("Enter the ID of the instructor to delete:")
        data_initialization.delete_data(user_id)

    def modify_user(self):
        while True:
            choice = user_interface.admin_manage_users_modify_menu_prompt()
            
            if choice == 1:
                data_initialization.update_user_id()
            elif choice == 2:
                data_initialization.update_password()
            elif choice == 3:
                data_initialization.update_info()
            elif choice == 0:
                break

    def dis_student(self):
        choice = user_interface.admin_manage_users_display_list_menu_prompt()
        display_format = self.get_display_format(choice)
        data_initialization.list_students(display_format)

    def dis_instructor(self):
        choice = user_interface.admin_manage_users_display_list_menu_prompt()
        display_format = self.get_display_format(choice)
        data_initialization.list_instructors(display_format)

    def get_display_format(self, choice):
        if choice == 1:
            return "table"
        elif choice == 2:
            return "key-value"

    def manage_attendance(self):
        while True:
            attendance_choice = user_interface.manage_attendance_menu_prompt()
            
            if attendance_choice == 1:
                self.view_attendance()
            elif attendance_choice == 2:
                self.mark_attendance()
            elif attendance_choice == 0:
                break

    def mark_attendance(self):
        try:
            with database.Database() as db:
                program = input("Enter the name of the program: ")
                date = input("Enter the date (YYYY-MM-DD): ")
                if db.class_exists(program):
                    students = db.get_students_in_class(program)
                    attendance_list = []
                    for student in students:
                        status = input(f"Is {student[0]} P-resent/L-Late/A-Absent?: ")
                        attendance_list.append((student[0], student[1], date, status))
                    db.mark_attendance(program, date, attendance_list)
                else:
                    print(f"Program {program} not found.")
        except database.DatabaseError as e:
            print(f"Database error: {e}")

    def view_attendance(self):
        try:
            with database.Database() as db:
                program = input("Enter the name of the program: ")
                date = input("Enter the date (YYYY-MM-DD): ")

                if db.class_exists(program):
                    attendance_data = db.get_attendance(program, date)

                    if attendance_data:
                        print(f"Attendance for {program} on {date}:")
                        for student, status in attendance_data:
                            print(f"{student}: {status}")
                    else:
                        print("No attendance data found.")
                else:
                    print(f"Program {program} not found.")
        except database.DatabaseError as e:
            print(f"Database error: {e}")

    def manage_grades(self):
        while True:
            grades_choice = user_interface.manage_grades_menu_prompt()
            
            if grades_choice == 1:
                self.view_grades()
            elif grades_choice == 2:
                self.input_grades()
            elif grades_choice == 0:
                break

    def input_grades(self):
        try:
            with database.Database() as db:
                program = input("Enter the name of the program: ")
                course = input("Enter course code: ")
                if db.class_exists(program):
                    students = db.get_students_in_class(program)

                    grades_list = []
                    for student in students:
                        grade = input(f"Enter the grade for {student[0]}: ")
                        grades_list.append((student[0], student[1], course, grade))

                    db.input_grades(grades_list)
                else:
                    print(f"Program {program} not found.")
        except database.DatabaseError as e:
            print(f"Database error: {e}")

    def view_grades(self):
        try:
            with database.Database() as db:
                program = input("Enter the name of the program: ")
                course = input("Enter course code: ")
                sr_code = input("Enter the sr_code of the student: ")

                students = db.get_students_in_class(program)
                
                student_grades = db.get_student_grades(sr_code, course)

                if student_grades:
                    for username in students:
                        print(f"Grades for {username[0]} in {course}:")
                        for grade in student_grades:
                            print(f"{grade[0]}: {grade[1]}")
                else:
                    print("No grades found.")
        except database.DatabaseError as e:
            print(f"Database error: {e}")
            