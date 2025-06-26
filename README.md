# oozie-wf-monitor
Web UI to monitor oozie workflows

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

def convert_gmt_to_est(gmt_time):
    gmt = pytz.timezone('GMT')
    est = pytz.timezone('US/Eastern')
    gmt_time = datetime.strptime(gmt_time, '%a, %d %b %Y %H:%M:%S GMT')
    gmt_time = gmt.localize(gmt_time)
    est_time = gmt_time.astimezone(est)
    return est_time.strftime('%Y-%m-%d %H:%M:%S')

def get_job_status(job_name):
    params = {
        "filter": f"name={job_name}",
        "len": 3
    }

    try:
        response = requests.get(url, params=params, auth=auth, verify=False)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            workflows = data.get("workflows", [])

            job_status = []
            for workflow in workflows:
                app_name = workflow.get("appName")
                status = workflow.get("status")
                start_time = workflow.get("startTime")
                start_time_est = convert_gmt_to_est(start_time)

                if status == "KILLED":
                    color = "red"
                elif status == "SUCCEEDED":
                    color = "green"
                elif status == "RUNNING":
                    color = "white"

                job_status.append((app_name, status, start_time_est, color))

            return job_status
        else:
            return [("Error", f"Failed to retrieve data: {response.status_code}", "", "red")]
    except requests.exceptions.RequestException as e:
        return [("Error", str(e), "", "red")]

def read_workflows_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            workflows = [line.strip() for line in file.readlines()]
            print(f"Workflows: {workflows}")
            return workflows
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

@route('/')
def index():
    workflows = read_workflows_from_file(workflow_file)
    job_status_list = []

    for workflow in workflows:
        job_status = get_job_status(workflow)
        job_status_list.append((workflow, job_status))

    return template('index', job_status_list=job_status_list)

run(reloader=True, debug=True)
