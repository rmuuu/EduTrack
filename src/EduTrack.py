import authentication
import admin_functions

def main():
    user = None

    while user is None:
        print("Welcome to the EduTrack!")
        email = input("Email: ")
        password = input("Password: ")

    # Admin Privilege
        if email == "":
            if password == "":
                admin_functions.admin_menu(user)

        user = authentication.authenticate_user(email, password)

        if user is None:
            print("Invalid credentials. Please try again.\n")
    
    if user.role == "teacher":
        print("this executed, teahcer")
        teacher_functions.teacher_menu(user)
    elif user.role == "student":
        print("this executed, student")
        student_functions.student_menu(user)

if __name__ == "__main__":
    main()  