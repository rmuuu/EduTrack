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
    def collect_person_input():
        last_name = input("Enter last name: ")
        given_name = input("Enter given name: ")
        middle_name = input("Enter middle name: ")
        birth_date = input("Enter birth date (YYYY-MM-DD): ")
        email = input("Enter email address: ")
        address = input("Enter address: ")
        contact_number = input("Enter contact number: ")
        eContact_number = input("Enter emergency contact number: ")
        eContact_name = input("Enter emergency contact name: ")

        return last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name

class Student(Person):
    def __init__(self, sr_code, last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name, program, block):
        super().__init__(last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name)
        self.sr_code = sr_code
        self.program = program
        self.block = block

    @staticmethod
    def collect_student_input():
        sr_code = input("Enter SR Code: ")
        program = input("Enter Program: ")
        block = input("Enter Block: ")
        last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name = Person.collect_person_input()

        return sr_code, last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name, program, block

class Instructor(Person):
    def __init__(self, emp_code, last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name, hdl_course, hdl_block):
        super().__init__(last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name)
        self.emp_code = emp_code
        self.hdl_course = hdl_course
        self.hdl_block = hdl_block

    @staticmethod
    def collect_instructor_input():
        emp_code = input("Enter Employee Code: ")
        hdl_course = input("Enter Handled Course: ")
        hdl_block = input("Enter Handled Block: ")
        last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name = Person.collect_person_input()

        return emp_code, last_name, given_name, middle_name, birth_date, email, address, contact_number, eContact_number, eContact_name, hdl_course, hdl_block
        
class User:
    def __init__(self, user_id, email, password, role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role

class Class:
    def __init__(self, class_id, class_name, teacher_id):
        self.class_id = class_id
        self.class_name = class_name
        self.teacher_id = teacher_id

    @staticmethod
    def collect_class_input():
        class_name = input("Enter class name: ")
        teacher_id = input("Enter teacher ID: ")

        return class_name, teacher_id

class Attendance:
    def __init__(self, attendance_id, student_id, class_id, date, status):
        self.attendance_id = attendance_id
        self.student_id = student_id
        self.class_id = class_id
        self.date = date
        self.status = status

    @staticmethod
    def collect_attendance_input():
        student_id = input("Enter student ID: ")
        class_id = input("Enter class ID: ")
        date = input("Enter date: ")
        status = input("Enter status: ")

        return student_id, class_id, date, status

class Grade:
    def __init__(self, grade_id, student_id, class_id, grade):
        self.grade_id = grade_id
        self.student_id = student_id
        self.class_id = class_id
        self.grade = grade

    @staticmethod
    def collect_grade_input():
        student_id = input("Enter student ID: ")
        class_id = input("Enter class ID: ")
        grade = input("Enter grade: ")

        return student_id, class_id, grade

