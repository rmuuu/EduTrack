import database

def authenticate_user(email, password):
    with database.Database() as db:
        # Define the query parameters
        query_vals = (email, password)

        # Execute the SQL query to check if the user with the provided credentials exists
        query = "SELECT * FROM Users WHERE email = %s AND password = %s"
        user_record = db.fetch_one(query, query_vals)
        if user_record:
            # Extract the user's email and role from the query result
            email, role = user_record[1], user_record[3]
            return email, role

        return None
