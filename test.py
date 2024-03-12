from flask import Flask, request, render_template, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
import json
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI

import json

# The path to your JSON file
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

# Now data_dict contains the JSON data as a Python dictionary
print(data_dict)

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

app = Flask(__name__)
@app.route('/screen-resume', methods=['GET'])
def screen_resume(resume, jd):
    resume_text = resume
    jd_text = jd
    
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
    output = chain.invoke({"jd": jd_text, "resume":resume_text})
    output_content = output.content
    try:
        # Find the JSON start and end, and parse it
        json_start = output_content.find("{")
        json_end = output_content.rfind("}") + 1
        json_str = output_content[json_start:json_end]
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON"}

jd = "Roles & Responsibilities: Work on implementation of real-time and batch data pipelines for disparate data sources. Build the infrastructure required for optimal extraction, transformation, and loading of data from a wide variety of data sources using SQL and AWS technologies. Build and maintain an analytics layer that utilizes the underlying data to generate dashboards and provide actionable insights. Identify improvement areas in the current data system and implement optimizations. Work on specific areas of data governance including metadata management and data quality management. Participate in discussions with Product Management and Business stakeholders to understand functional requirements and interact with other cross-functional teams as needed to develop, test, and release features. Develop Proof-of-Concepts to validate new technology solutions or advancements. Work in an Agile Scrum team and help with planning, scoping and creation of technical solutions for the new product capabilities, through to continuous delivery to production. Work on building intelligent systems using various AI/ML algorithms. Desired Experience/Skill: Must have worked on Analytics Applications involving Data Lakes, Data Warehouses and Reporting Implementations. Experience with private and public cloud architectures with pros/cons. Ability to write robust code in Python and SQL for data processing. Experience in libraries such as Pandas is a must; knowledge of one of the frameworks such as Django or Flask is a plus. Experience in implementing data processing pipelines using AWS services: Kinesis, Lambda, Redshift/Snowflake, RDS. Knowledge of Kafka, Redis is preferred Experience on design and implementation of real-time and batch pipelines. Knowledge of Airflow is preferred. Familiarity with machine learning frameworks (like Keras or PyTorch) and libraries (like scikit-learn)"
for key in data_dict.keys():
    if key == 'resumes':
        for res in key.keys():
            resume = data_dict[res]["text"]
    decision = screen_resume(resume, jd)
    print(decision)