import fitz 
# import mysql.connector
from dotenv import load_dotenv
import os
# from db import *
# import requests
import json
import re

# def read_resume_pdf(resume_file_path):
#     resume_text = ""
#     with fitz.open(resume_file_path) as pdf_document:
#         num_pages = pdf_document.page_count
#         for page_num in range(num_pages):
#             page = pdf_document[page_num]
#             resume_text += page.get_text()

#     return resume_text

# def read_JD_pdf(jd_file_path):
#     JD_text = ""
#     with fitz.open(jd_file_path) as pdf_document:
#         num_pages = pdf_document.page_count
#         for page_num in range(num_pages):
#             page = pdf_document[page_num]
#             JD_text += page.get_text()

#     return JD_text

# file_save_path = os.getcwd()

def fetch_files_from_upload_folder(file_location):
    try:
        files_data = {}
        UPLOAD_FOLDER = file_location

        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            if os.path.isfile(file_path):
                print(file_path)
                resume_text = ""
                with fitz.open(file_path) as pdf_document:
                    num_pages = pdf_document.page_count
                    for page_num in range(num_pages):
                        page = pdf_document[page_num]
                        resume_text += page.get_text()
                        resume_text = re.sub(r'\n+', ' ', resume_text)
                files_data[len(files_data) + 1] = {'file_name': filename,
                    'text': resume_text
                }
                # files_data.append({
                #     'id': len(files_data) + 1,
                #     'file_name': filename,
                #     'text': resume_text
                # })

        json_data = json.dumps(files_data)

        return json_data

    except Exception as e:
        return {'error': str(e)}
# Example usage
# json_data = fetch_files_from_upload_folder()
# print(json_data)
# resume_file_path = 'Divesh_Kumar_Mitahee_Resume.pdf'
# jd_file_path = 'Byke-insurance-certificate.pdf'
# resume_pdf_text = read_resume_pdf(resume_file_path)
# jd_pdf_text = read_JD_pdf(jd_file_path)
# print(resume_pdf_text)
# print(jd_pdf_text)

# def download_file(url, save_path):
#     try:
#         if not url or not isinstance(url, str):
#             raise ValueError(f"Invalid URL: {url}")

#         print(f"Downloading file from URL: {url}")

#         response = requests.get(url, stream=True)
#         response.raise_for_status() 

#         with open(save_path, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)

#         print(f"File downloaded successfully to {save_path}")

#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading file: {e}")

# if __name__ == "__main__":
#     resume_urls = get_resume_url()
#     local_save_directory = file_save_path

#     for i in resume_urls:
#         file_name = os.path.basename(i)
#         local_save_path = os.path.join(local_save_directory, file_name)
#         download_file(i, local_save_path)

#     connection.close()


