import authentication
import admin_functions

def main():
    user = None

    while user is None:
        print("Welcome to the EduTrack!")
        email = input("Email: ")
        password = input("Password: ")
        
        user = authentication.authenticate_user(email, password)
        
        # Admin Privilege
        if email == "":
            if password == "":
                admin = admin_functions.admin_menu()
                print("Logged out.\n")
        elif user is None:
            print("Invalid credentials. Please try again.\n")
    
    if user[1] == "student":
        print("this executed, student")
        student_functions.student_menu(user[1])
    elif user[1] == "instructor":
        print("this executed, instructor")
        instructor_functions.instructor_menu(user[1])

if __name__ == "__main__":
    main() 