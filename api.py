from main import fetch_files_from_upload_folder
from flask import Flask, request, jsonify
import zipfile
import json
import os



app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    try:
        requisition_id = request.form.get('requisition_id')
        print(requisition_id)
        job_title = request.form.get('job_title')
        print(job_title)
        job_description = request.form.get('job_description')
        print(job_description)
        

        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        f = request.files['file']

        if f.filename == '':
            return jsonify({'error': 'No selected file'})

        filename = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filename)

        if f.filename.endswith('.zip'):
            # Extract zip file
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(app.config['UPLOAD_FOLDER'])

            os.remove(filename)
        # Construct JSON response
        response_data = {
            'job_description': job_description,
            'job_title': job_title,
            'requisition_id': requisition_id,
            'file_location':  os.path.abspath(UPLOAD_FOLDER)
        }
       #Save this Response Data Dictionary
        with open('response_data.json', 'w') as file:
            json.dump(response_data, file)
            return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/fetch-files', methods=['GET'])
def fetch_files():
    with open('response_data.json', 'r') as file:
        response_data = json.load(file)
    file_location = response_data['file_location']
    resume_json = fetch_files_from_upload_folder(file_location)
    
    response_data["resumes"] = json.loads(resume_json)

    #Save this Response Data Dictionary
    with open('response_data.json', 'w') as file:
        json.dump(response_data, file)

    return jsonify(response_data,"Sucees, all files parsed")


if __name__ == '__main__':
    app.run(debug=True)
