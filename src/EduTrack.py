import authentication
import admin_functions

def main():
    user = None

    while user is None:
        print("Welcome to the EduTrack!")
        username = input("Username: ")
        password = input("Password: ")

    # Admin Privilege
        if username == "admin":
            if password == "password":
                admin_functions.admin_menu(user)

        user = authentication.authenticate_user(username, password)

        if user is None:
            print("Invalid credentials. Please try again.\n")
    
    if user.role == authentication.TEACHER:
        print("this executed, teahcer")
        teacher_functions.teacher_menu(user)
    elif user.role == authentication.STUDENT:
        print("this executed, student")
        student_functions.student_menu(user)

if __name__ == "__main__":
    main()