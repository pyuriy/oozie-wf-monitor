# oozie-wf-monitor
Web UI to monitor oozie workflows

This script providess a web page to help monitoring certain oozie workflows. 
The script will get the workflow list from an text file (workflows.txt).

## Install Required Dependencies

Run the following command in your terminal:

```bash
pip install -r requirements.txt
```
if you use proxy the following command:

```bash
C:\tmp\oozie-wf-monitor-main>pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --proxy=http://you.proxy.com:80 -r requirements.txt
```

## Set Up Environment Variables in a .env File
- Create a .env file in your root folder and add the following variables:
on .env file set the folloing variables

```
OOZIE_URL = "https://oozie.site.com:11443/oozie/v2/jobs"
WORKFLOW_FILE = workflows.txt
```
## Start the scipt

You'll see the following message:

```
Bottle v0.13.2 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.
```

Open in your browser http://127.0.0.1:8080/
