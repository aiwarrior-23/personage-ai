from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def validate_credentials(username, password):
    # Dummy user credentials
    user_credentials = {
        "admin": {"password": "admin123", "user_type": "Admin"},
        "techhead": {"password": "techhead123", "user_type": "Tech Head"},
        "rechead": {"password": "rechead123", "user_type": "Recruitment Head"},
        "techuser": {"password": "techuser123", "user_type": "Tech User"},
        "hruser": {"password": "hruser123", "user_type": "HR User"}
    }

    # Validate credentials
    user = user_credentials.get(username.lower())
    if user and user["password"] == password:
        return user["user_type"], True
    else:
        return None, False


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate credentials and get user type
    user_type, is_valid = validate_credentials(username, password)

    if is_valid:
        return jsonify({"message": "Success", "user_type": user_type})
    else:
        return jsonify({"message": "Failure"}), 401

if __name__ == '__main__':
    app.run(debug=True)
