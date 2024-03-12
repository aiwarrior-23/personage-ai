from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import uuid
import requests
from resume_generator import fetch_files_from_upload_folder
from flask import Flask, request, jsonify
import zipfile
import json
import os
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

app = Flask(__name__)
CORS(app)

file_path = 'response_data.json'

# Initialize an empty dictionary
data_dict = {}

# Open the file and load its content into a dictionary
try:
    with open(file_path, 'r') as file:
        data_dict = json.load(file)
except FileNotFoundError:
    print(f"The file {file_path} was not found.")
except json.JSONDecodeError:
    print("Error decoding JSON from the file.")

llm_langchain = AzureChatOpenAI(
    api_key="018970e835a643ccbeaec56c8220db14",
    api_version="2023-05-15",
    azure_endpoint="https://canfour.openai.azure.com/",
    azure_deployment="canfour",
)

embeddings = AzureOpenAIEmbeddings(
        api_key="be40bf82a06e4c958cee025b20ffb836",
        api_version="2023-05-15",
        azure_endpoint="https://rookie.openai.azure.com/",
        azure_deployment="rookie_embedding",
    )

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL configurations
app.config['MYSQL_HOST'] = '98.70.90.20'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'mgmt'

# Email configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'himanshuit3036@gmail.com'
app.config['MAIL_PASSWORD'] = 'jypq xtfi ruuj sqqy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail = Mail(app)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO company_table(username, first_name, last_name, email, company, user_type, location, department, reporting_manager) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (data.get('username'), data.get('first_name'), data.get('last_name'), data.get('email'), data.get('company'), data.get('user_type'), data.get('location'), data.get('department'), data.get('reporting_manager')))

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


def check_user_credentials(cursor, username, password):
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

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_type, is_valid = check_user_credentials(mysql.connection.cursor(),username, password)

    if is_valid:
        return jsonify({"message": "Success", "user_data": user_type}), 200
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

@app.route('/send_mail/<string:user_id>')
def send_mail(user_id):
    """
    Endpoint to send an email to a user.

    Args:
    user_id (int): The user's ID.

    Returns:
    JSON: Email sending status.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT email FROM company_table WHERE username = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'status': 'failure', 'message': 'User not found'}), 404

    email = user[0]

    try:
        msg = Message("Your Subject Here", sender='your-email@example.com', recipients=["diveshkumar930@gmail.com"])
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
        
@app.route('/upload', methods=['POST'])
async def upload_file():
    response_data = {
            'jd': "",
            'jobTitle': "",
            'jobID': "",
            'file_location':  f"",
            'backup_location': f"",
            'count' : "",
            'owner' : "",
            'manager' : "",
            'department' : "",
            'uploadSuccess': 'false'
        }

    try:
        requisition_id = request.form.get('jobID')
        job_title = request.form.get('jobTitle')
        job_description = request.form.get('jd')
        count = request.form.get('count')
        owner = request.form.get('owner')
        manager = request.form.get('manager')
        department = request.form.get('department')
        
        with open("overall_jobs.json", 'r') as file:
            overall_jobs = json.load(file)
        
        overall_jobs[requisition_id]="loading"
        with open(f'overall_jobs.json', 'w') as file:
            json.dump(overall_jobs, file)
        
        if not os.path.exists(f"{UPLOAD_FOLDER}/{requisition_id}/new"):
            os.makedirs(f"{UPLOAD_FOLDER}/{requisition_id}/new")
        

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        f = request.files['file']

        if f.filename == '':
            return jsonify({'error': 'No selected file'})

        filename = os.path.join(f"{UPLOAD_FOLDER}/{requisition_id}/new", f.filename)
        f.save(filename)

        if f.filename.endswith('.zip'):
            # Extract zip file
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(f"{UPLOAD_FOLDER}/{requisition_id}/new")

            os.remove(filename)
        # Construct JSON response
        response_data = {
            'jd': job_description,
            'jobTitle': job_title,
            'jobID': requisition_id,
            'file_location':  f"{UPLOAD_FOLDER}/{requisition_id}/new",
            'backup_location': f"{UPLOAD_FOLDER}/{requisition_id}/backup",
            'count' : count,
            'owner' : owner,
            'manager' : manager,
            'department' : department,
            'uploadSuccess': 'true'
        }
        overall_jobs[requisition_id]="uploaded"
        with open(f'overall_jobs.json', 'w') as file:
            json.dump(overall_jobs, file)
       #Save this Response Data Dictionary
        with open(f'{requisition_id}.json', 'w') as file:
            json.dump(response_data, file)
        # response = await fetch_files(response_data, requisition_id)
        return jsonify("Success")
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/get-upload-status', methods=['GET'])
def get_upload_status():
    # Retrieve the parameter from the query string
    filename_prefix = request.args.get('jobID')
    if not filename_prefix:
        return jsonify({"error": "Missing filename parameter"}), 400
    
    try:
        # Open and read the JSON file, then parse it to get the uploadStatus
        with open("overall_jobs.json", 'r') as file:
            data = json.load(file)  # Parse the JSON content into a Python dictionary
            
            # Check if 'uploadStatus' key exists in the dictionary
            if data[filename_prefix] == "loading":
                return jsonify({"status": "uploading"}), 200
            elif data[filename_prefix] == "uploaded":
                return jsonify({"status": "uploaded"}), 200
            else:
                return jsonify({"error": "uploadSuccess key not found in the file"}), 404
    except Exception as e:
        return jsonify({"error": f"Error reading or parsing file: {str(e)}"}), 500

import glob
import shutil
async def fetch_files(response_data, requisition_id):
    with open(f'{requisition_id}.json', 'r') as file:
        response_data = json.load(file)
    file_location = response_data['file_location']
    backup_location = response_data['backup_location']
    response_data["jobTitle"] = response_data['jobTitle']
    response_data["department"] = response_data['department']
    response_data["jobID"] = response_data['jobID']
    response_data["manager"] = response_data['manager']
    response_data["owner"] = response_data['owner']
    response_data["count"] = response_data['count']
    response_data["jd"] = response_data['jd']
    resume_json = fetch_files_from_upload_folder(file_location)
    pattern = os.path.join(file_location, '*.pdf')
    pdf_files = glob.glob(pattern)
    if not os.path.exists(backup_location):
        os.makedirs(backup_location)
        print(f"Created target directory: {backup_location}")
        
    for file_path in pdf_files:
        try:
            target_path = os.path.join(backup_location, os.path.basename(file_path))
            shutil.move(file_path, target_path)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    response_data["resumes"] = json.loads(resume_json)
    #Save this Response Data Dictionary
    with open(f'{requisition_id}.json', 'w') as file:
        json.dump(response_data, file)
    screening_status = await screen_resume(requisition_id)
    return "Success"


async def screen_resume(requisition_id):
    with open(f'{requisition_id}.json', 'r') as file:
        data_dict = json.load(file)
    prompt = ChatPromptTemplate.from_template("""
    Given below is the Job Description of a particular job requirement
    Job Description - {jd}
    Given below is the resume of a candidate for the above job role
    Resume - {resume}
    Can you please screen the candidate and decide whether he/she should be shortlisted or not.
    Make sure to extract all the important points mentioned in JD. Don't miss a single point.
    Extract all the skills or tools mentioned in JD and match accordingly
    Below are the mandatory skills where 100% match should be there
    Mandatory Skills - [python]
    For all the others 70% minimum match should be there. Give response in below JSON format -
    {{
        "Mandatory Skills": {{
            "skill1": "name the skill",
            "match": "what's the match in percentage with the skill. Follow this for all mandatory skills,
            "reason": "how did you conclude its a match or not a match?"
        }},
        "Other Skills" : {{
            "skill1": "name the skill",
            "match": "what's the match in percentage with the skill. Follow this for all other skills,
            "reason": "how did you conclude its a match or not a match?"
        }},
        "Overall Match":"in percentage",
        "Decision":"Selected or Rejected",
        "Reason":"Reason for the decision. Is the decision final or can a phone call be made to candidate to confirm few skills which are implied in resume but not explicitly mentioned",
        "Frequent Switcher": "Findout if the candidate has switched multiple companies in limited amount of time. Show the company and tenure to support your judgement",
        "Career Gap": "Can you notice any missing years where person was not working in a company? For example a person working in a company from 2012 to 2014 and then in next company 2016 to present, then there is two years gap. Mention all these gaps"
    }}
    """)
    chain = prompt | llm_langchain
    jd_text = "Roles & Responsibilities: Work on implementation of real-time and batch data pipelines for disparate data sources. Build the infrastructure required for optimal extraction, transformation, and loading of data from a wide variety of data sources using SQL and AWS technologies. Build and maintain an analytics layer that utilizes the underlying data to generate dashboards and provide actionable insights. Identify improvement areas in the current data system and implement optimizations. Work on specific areas of data governance including metadata management and data quality management. Participate in discussions with Product Management and Business stakeholders to understand functional requirements and interact with other cross-functional teams as needed to develop, test, and release features. Develop Proof-of-Concepts to validate new technology solutions or advancements. Work in an Agile Scrum team and help with planning, scoping and creation of technical solutions for the new product capabilities, through to continuous delivery to production. Work on building intelligent systems using various AI/ML algorithms. Desired Experience/Skill: Must have worked on Analytics Applications involving Data Lakes, Data Warehouses and Reporting Implementations. Experience with private and public cloud architectures with pros/cons. Ability to write robust code in Python and SQL for data processing. Experience in libraries such as Pandas is a must; knowledge of one of the frameworks such as Django or Flask is a plus. Experience in implementing data processing pipelines using AWS services: Kinesis, Lambda, Redshift/Snowflake, RDS. Knowledge of Kafka, Redis is preferred Experience on design and implementation of real-time and batch pipelines. Knowledge of Airflow is preferred. Familiarity with machine learning frameworks (like Keras or PyTorch) and libraries (like scikit-learn)"
    for key in data_dict.keys():
        print(key)
        if key == 'resumes':
            for res in data_dict[key].keys():
                print(res, type(res))
                resume_text = data_dict[key][res]["text"]
                print("-----------",resume_text)
                output = chain.invoke({"jd": jd_text, "resume":resume_text})
                output_content = output.content
                try:
                    # Find the JSON start and end, and parse it
                    json_start = output_content.find("{")
                    json_end = output_content.rfind("}") + 1
                    json_str = output_content[json_start:json_end]
                    json_data = json.loads(json_str)
                    data_dict[key][res]["ai_response"] = json_data 
                    #Save this Response Data Dictionary
                    with open('response_data.json', 'w') as file:
                        json.dump(data_dict, file)
                except json.JSONDecodeError:
                    print("Error decoding JSON")
            break;
    return("suceess")
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")