from logger import get_logger

def check_user_credentials(cursor, username, password):
    logger = get_logger("my_logger")
    try:
        cur = cursor
        cur.execute("SELECT company_passwords.password, company_passwords.username, company_table.* FROM company_passwords LEFT JOIN company_table ON company_table.username = company_passwords.username WHERE company_passwords.username = %s AND company_passwords.password = %s", (username, password))
        columns = [col[0] for col in cur.description]
        user_record = cur.fetchone()
        cur.close()
        if user_record and user_record[0] == password:  # Access password using index
            user_dict = dict(zip(columns, user_record))
            return user_dict, True
        else:
            return None, False

    except Exception as e:
        # Handle the exception, you might want to log it or return a specific error
        print(f"Error: {e}")
        logger.error(str(e))
        return None, False

    

def validate_password(cursor,username, password):
    cur = cursor

    # Insert username and password into company_passwords table
    try:
        cur.execute("INSERT INTO company_passwords(username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        response = {"message": f"User {username} added to company_passwords table."}
        status_code = 200
    except Exception as e:
        mysql.connection.rollback()
        response = {"message": str(e)}
        status_code = 400
    finally:
        cur.close()

    return response, status_code