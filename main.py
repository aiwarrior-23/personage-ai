from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import uuid
import requests

app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_HOST'] = '98.70.90.20'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'mgmt'

# Email configurations
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO company_table(username, first_name, last_name, email, company, user_type, location, department, reporting_manager) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (data.get('username'), data.get('First Name'), data.get('Last NAme'), data.get('email'), data.get('company'), data.get('userType'), data.get('location'), data.get('department'), data.get('reporting manager')))

    mysql.connection.commit()
    cur.close()
    return jsonify({"message": f"User {data.get('username')} created successfully"}), 201

@app.route('/check_and_update_users', methods=['GET'])
def check_and_update_users():
    cur = mysql.connection.cursor()

    # Query to get all users from company_table
    cur.execute("SELECT username FROM company_table")
    user_list = cur.fetchall()

    # Check each user in the company_passwords table
    for user in user_list:
        username = user[0]
        cur.execute("SELECT * FROM company_passwords WHERE username = %s", (username,))
        result = cur.fetchone()

        # If user not in company_passwords table, add them
        if not result:
            response, status_code = validate_password(username, '')
            if status_code == 200:
                print(f"User {username} added to company_passwords table.")
            else:
                print(f"Failed to add user {username} to company_passwords table.")

    cur.close()
    return jsonify({"message": "Checked and updated users successfully"})

def validate_password(username, password):
    cur = mysql.connection.cursor()

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

def check_user_credentials(username, password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT password, username FROM company_passwords WHERE username = %s", (username,))
    user_record = cur.fetchone()
    cur.close()

    if user_record and user_record[0] == password:
        return user_record[1], True
    else:
        return None, False

@app.route('/validate_credentials', methods=['POST'])
def validate_credentials():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_type, is_valid = check_user_credentials(username, password)

    if is_valid:
        return jsonify({"user_type": user_type, "valid": True}), 200
    else:
        return jsonify({"message": "Invalid credentials", "valid": False}), 401

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_type, is_valid = check_user_credentials(username, password)

    if is_valid:
        return jsonify({"message": "Success", "user_type": user_type}), 200
    else:
        return jsonify({"message": "Failure"}), 401

@app.route('/change_password', methods=['POST'])
def change_password():
    """
    Endpoint to initiate password change process.

    Returns:
    str: Status message.
    """
    user_id = request.json.get('user_id')
    if not user_id:
        return "User ID is required", 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email FROM company_table WHERE username = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        email = user[0]
        try:
            # msg = Message("Change Your Password", sender="your_email", recipients=[email])
            # msg.body = "Here is your password reset link: <link>"
            # mail.send(msg)
            return "Link successfully sent"
        except Exception as e:
            return str(e)
    else:
        return "User not found"

@app.route('/send_mail/<int:user_id>')
def send_mail(user_id):
    """
    Endpoint to send an email to a user.

    Args:
    user_id (int): The user's ID.

    Returns:
    JSON: Email sending status.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'status': 'failure', 'message': 'User not found'}), 404

    email = user[0]

    try:
        msg = Message("Your Subject Here", sender='your-email@example.com', recipients=[email])
        msg.html = "<h1>Welcome</h1><p>Your HTML content here.</p>"
        mail.send(msg)
        return jsonify({'status': 'success', 'message': 'Email sent successfully'})
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)})

@app.route('/update_password', methods=['POST'])
def update_password():
    """
    Endpoint to update user's password.

    Returns:
    JSON: Update status.
    """
    user_id = request.json.get('user_id')
    new_password = request.json.get('new_password')

    if not user_id or not new_password:
        return jsonify({'error': 'Missing user_id or new_password'}), 400

    try:
        conn = mysql.connection
        cursor = conn.cursor()
        query = "UPDATE company_passwords SET password = %s WHERE username = %s"
        cursor.execute(query, (new_password, user_id))
        conn.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@app.route('/get_users', methods=['POST'])
def get_users():
    """
    Endpoint to retrieve users. If the username is 'admin', all users are retrieved.
    Otherwise, retrieves users by manager ID.

    Returns:
    JSON: List of users.
    """
    data = request.json
    username = data.get('username')
    manager_id = data.get('manager_id')

    conn = mysql.connection
    cursor = conn.cursor()

    if username == 'admin':
        query = 'SELECT * FROM company_table'
        cursor.execute(query)
    else:
        query = 'SELECT * FROM company_table WHERE reporting_manager = %s'
        cursor.execute(query, (manager_id,))

    try:
        rows = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        users = [{column_names[index]: value for index, value in enumerate(row)} for row in rows]

        return jsonify({'message': 'Success', 'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)