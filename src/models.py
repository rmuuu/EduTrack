class Person:
    def __init__(self, last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name):
        self.last_name = last_name
        self.given_name = given_name
        self.middle_name = middle_name
        self.birth_date = birth_date
        self.email = email
        self.address = address
        self.contact_number = contact_number
        self.eContact_number = eContact_number
        self.eContact_name = eContact_name
 
    @staticmethod
    def collect_user_input():
        last_name =       input("      Last name : ")
        given_name =      input("     Given name : ")
        middle_name =     input("    Middle name : ")
        birth_date =      input(" Birth date\n   (YYYY-MM-DD) : ")
        email =           input("  Email address : ")
        address =         input("        Address : ")
        contact_number =  input(" Contact number : ")
        print("In case of emergency.")
        eContact_name =   input("   Contact name : ")
        eContact_number = input(" Contact number : ")
        
        return last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name    

class Student(Person):
    def __init__(self, sr_code, last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name, program, year_lvl):
        super().__init__(last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name)
        self.sr_code = sr_code
        self.program = program
        self.year_lvl = year_lvl

    @staticmethod
    def collect_student_input():
        print("Please Enter :")
        sr_code =  input("  Enter SR Code : ")
        program =  input("Program (IT/CS) : ")
        year_lvl = input("     Year Level : ")
        
        # Collecting user input from the parent class
        last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name = Person.collect_user_input()

        return sr_code, last_name, given_name, middle_name, birth_date, email, program, year_lvl, address, contact_number, eContact_number, eContact_name

class Instructor(Person):
    def __init__(self, itr_code, last_name, given_name, middle_name, birth_date, email, teaching, address, contact_number, eContact_number, eContact_name):
        super().__init__(last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name)
        self.itr_code = itr_code
        self.teaching = teaching

    @staticmethod
    def collect_instructor_input():
        print("Please Enter :")
        itr_code = input("  Instructor ID : ")
        teaching = input("       Teaching : ")

        # Collecting user input from the parent class
        last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name = Person.collect_user_input()

        return itr_code, last_name, given_name, middle_name, birth_date, email, teaching, address, contact_number, eContact_number, eContact_name
