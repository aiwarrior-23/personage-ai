from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import uuid

app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'your_host'
app.config['MYSQL_USER'] = 'your_user'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_db'

# Email configurations
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

def validate_credentials(username, password):
    """
    Validate user credentials.

    Args:
    username (str): The username.
    password (str): The password.

    Returns:
    tuple: User type and a boolean indicating if credentials are valid.
    """
    # Dummy user credentials
    user_credentials = {
        "admin": {"password": "admin123", "user_type": "Admin"},
        # ... add other credentials here
    }

    user = user_credentials.get(username.lower())
    if user and user["password"] == password:
        return user["user_type"], True
    else:
        return None, False

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.

    Returns:
    JSON: Login success or failure message.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_type, is_valid = validate_credentials(username, password)

    if is_valid:
        return jsonify({"message": "Success", "user_type": user_type})
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
    cursor.execute("SELECT email FROM user WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        email = user[0]
        try:
            msg = Message("Change Your Password", sender="your_email", recipients=[email])
            msg.body = "Here is your password reset link: <link>"
            mail.send(msg)
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
        query = "UPDATE users SET password = %s WHERE user_id = %s"
        cursor.execute(query, (new_password, user_id))
        conn.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Endpoint to add a new user.

    Returns:
    JSON: Addition status and user ID.
    """
    data = request.json
    user_id = str(uuid.uuid4())  # Generate a unique user ID

    name = data.get('name')
    department = data.get('department')
    reporting_manager = data.get('department')
    # ... other fields

    conn = mysql.connection
    cursor = conn.cursor()

    query = '''INSERT INTO users (user_id, name, department, reporting_manager, ...)
               VALUES (%s, %s, %s, %s, ...)'''
    values = (user_id, name, department, reporting_manager, ...)

    try:
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'User added successfully', 'user_id': user_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/get_users', methods=['GET'])
def get_users():
    """
    Endpoint to retrieve users by manager ID.

    Returns:
    JSON: List of users.
    """
    manager_id = request.args.get('manager_id')

    conn = mysql.connection
    cursor = conn.cursor()

    query = '''SELECT * FROM users WHERE managerid = %s'''
    values = (manager_id,)

    try:
        cursor.execute(query, values)
        rows = cursor.fetchall()

        users = [{'user_id': row[0], 'name': row[1], 'department': row[2], 'reporting_manager': row[3]} for row in rows]

        return jsonify({'message': 'Success', 'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(debug=True)