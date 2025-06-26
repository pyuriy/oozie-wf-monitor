# works fine
from bottle import route, run, template, TEMPLATE_PATH
import requests
from requests_kerberos import HTTPKerberosAuth
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load environment variables from .env file
load_dotenv()

# Dynamically set the template path relative to the script
script_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(script_dir, 'views')
TEMPLATE_PATH.append(template_dir)

# Get URL and file name from environment variables
url = os.getenv("OOZIE_URL")
workflow_file = os.getenv("WORKFLOW_FILE")

auth = HTTPKerberosAuth(mutual_authentication=True, delegate=False)

def get_all_workflows():
    params = {
        "len": 200000
    }
    try:
        response = requests.get(url, params=params, auth=auth, verify=False)
        if response.status_code == 200:
            data = response.json()
            workflows = data.get("workflows", [])
            return workflows
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def read_workflows_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            workflows = {}
            group = None
            for line in lines:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    group = line[1:-1]
                    workflows[group] = []
                elif line:
                    workflows[group].append(line)
            return workflows
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}

@route('/')
def index():
    all_workflows = get_all_workflows()
    workflows = read_workflows_from_file(workflow_file)
    job_status_list = []
    for group, workflow_names in workflows.items():
        group_job_status = []
        for workflow_name in workflow_names:
            workflow_runs = [workflow for workflow in all_workflows if workflow.get("appName") == workflow_name]
            workflow_runs.sort(key=lambda x: x.get("startTime"), reverse=True)
            last_3_runs = workflow_runs[:3]
            run_statuses = []
            for run in last_3_runs:
                status = run.get("status")
                if status == "KILLED":
                    color = "red"
                elif status == "SUCCEEDED":
                    color = "green"
                elif status == "RUNNING":
                    color = "white"
                run_statuses.append((status, color))
            group_job_status.append((workflow_name, run_statuses))
        job_status_list.append((group, group_job_status))
    return template('index', job_status_list=job_status_list)

run(reloader=True, debug=True)
