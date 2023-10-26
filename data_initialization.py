import models
def add_student():
    student_info = models.Student.collect_student_input()
    new_student = models.Student(*student_info)
    
    query = "INSERT INTO Students (sr_code, last_name, given_name, middle_name, birth_date, email, program, block, address, contact_number, eContact_number, eContact_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (new_student.sr_code, new_student.last_name, new_student.given_name, new_student.middle_name, new_student.birth_date, new_student.email, new_student.program, new_student.block, new_student.address, new_student.contact_number, new_student.eContact_number, new_student.eContact_name)

    return query, values

def add_instrcutor():
    instructor_info = models.Instructor.collect_instructor_input()
    new_instructor = models.Instructor(*instructor_info)
    
    query = "INSERT INTO Instructor (emp_code, last_name, given_name, middle_name, birth_date, email, hdl_course, hdl_block, address, contact_number, eContact_number, eContact_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (new_instructor.emp_code, new_instructor.last_name, new_instructor.given_name, new_instructor.middle_name, new_instructor.birth_date, new_instructor.email, new_instructor.hdl_course, new_instructor.hdl_block, new_instructor.address, new_instructor.contact_number, new_instructor.eContact_number, new_instructor.eContact_name)
    
    return query, values










































""" import database

def collect_user_input(field_names):
    user_data = {}
    for field in field_names:
        value = input(f"Enter {field}: ")
        user_data[field] = value
    print("User data collected:", user_data)  # Debugging print
    return user_data

def collect_data_and_insert_to_db(table_name, field_names):
    user_data = collect_user_input(field_names)
    with database.Database() as db:
        try:
            columns = ", ".join(user_data.keys())
            placeholders = ", ".join(["%s"] * len(user_data))
            values = tuple(user_data.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            success = db.execute_query(query, values)

            if success:
                print(f"Data added to the {table_name} table successfully.")
                return user_data  # Return the user data
            else:
                print(f"Failed to add data to the {table_name} table.")
                return None
        except Exception as e:
            db.connection.rollback()
            print(f"An error occurred: {e}")

def initialize_students_interactively():
    student_fields = ["sr_code", "last_name", "given_name", "middle_name", "birth_date", "email", "program", "block", "address", "contact_number", "eContact_number", "eContact_name"]
    user_data = collect_data_and_insert_to_db("Students", student_fields)

    if user_data:
        user_id = user_data.get("sr_code")
        password = user_data.get("sr_code")  # Set the password to sr_code

def initialize_instructors_interactively():
    instructor_fields = ["emp_code", "last_name", "given_name", "middle_name", "birth_date", "email", "hdl_course", "hdl_block", "address", "contact_number", "eContact_number", "eContact_name"]
    user_data = collect_data_and_insert_to_db("Instructors", instructor_fields)

    if user_data:
        user_id = user_data.get("emp_code")
        password = user_data.get("emp_code")  # Set the password to emp_code """
