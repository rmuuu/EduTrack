import authentication
from admin_functions import AdminManager
# import student_functions
# import instructor_functions

class EduTrack:
    def __init__(self):
        self.user = None

    def login(self):
        while self.user is None:
            print("Welcome to EduTrack!")
            email = input("Email: ")
            password = input("Password: ")

            self.user = authentication.authenticate_user(email, password)

            if email == "" and password == "":
                admin_manager = AdminManager()
                admin_manager.admin_menu()
                print("Logged out.\n")
            elif self.user is None:
                print("Invalid credentials. Please try again.\n")

    def execute_user_functionality(self):
        if self.user[1] == "student":
            print("Student Menu:")
            student_functions.student_menu(self.user[1])
        elif self.user[1] == "instructor":
            print("Instructor Menu:")
            instructor_functions.instructor_menu(self.user[1])

def main():
    edutrack = EduTrack()
    edutrack.login()
    edutrack.execute_user_functionality()

if __name__ == "__main__":
    main()
