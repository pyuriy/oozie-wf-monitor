# oozie-wf-monitor
Web UI to monitor oozie workflows

This script providess a web page to help monitoring certain oozie workflows. 
The script will get the workflow list from an text file (workflows.txt).

Clone this repository into your local machine.

## Install Required Dependencies

Run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Set Up Environment Variables in a .env File
- Create a .env file in your root folder and add the following variables:
on .env file set the folloing variables

```
OOZIE_URL = "https://oozie.site.com:11443/oozie/v2/jobs"
WORKFLOW_FILE = workflows.txt
```
