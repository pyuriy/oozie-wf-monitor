<!DOCTYPE html>
<html>
<head>
    <title>Job Status</title>
    <style>
        table {
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>Job Status</h1>
    % for group, group_job_status in job_status_list:
        <h2>{{ group }}</h2>
        <table>
            <tr>
                <th>Workflow Name</th>
                <th>Last 3 Runs</th>
            </tr>
            % for workflow_name, run_statuses in group_job_status:
                <tr>
                    <td>{{ workflow_name }}</td>
                    <td>
                        % for status, color in run_statuses:
                            <span style="background-color: {{ color }}">{{ status }}</span>&nbsp;
                        % end
                    </td>
                </tr>
            % end
        </table>
    % end
</body>
</html>
