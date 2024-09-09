import requests

class GitLabCI:
    def __init__(self, gitlab_url, token):
        self.gitlab_url = gitlab_url
        self.token = token
        self.api_url = f"{gitlab_url}/api/v4"

    def get_projects(self):
        headers = {'Private-Token': self.token}
        response = requests.get(f"{self.api_url}/projects", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch GitLab projects: {response.status_code}")

    def get_pipeline_status(self, project_id):
        headers = {'Private-Token': self.token}
        response = requests.get(f"{self.api_url}/projects/{project_id}/pipelines", headers=headers)

        if response.status_code == 200:
            pipelines = response.json()
            if pipelines:
                latest_pipeline = pipelines[0]
                return latest_pipeline['status']
            else:
                print("No pipelines found.")
        else:
            raise Exception(f"Failed to fetch GitLab pipelines: {response.status_code}")

    def display_projects(self):
        try:
            projects = self.get_projects()
            for project in projects:
                print(f"Project: {project['name']}, ID: {project['id']}")
        except Exception as e:
            print(str(e))

    def get_pipeline_job_logs(self, project_id, job_id):
        headers = {'Private-Token': self.token}
        response = requests.get(f"{self.api_url}/projects/{project_id}/jobs/{job_id}/trace", headers=headers)

        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            raise Exception(f"Job {job_id} not found for project {project_id}.")
        else:
            raise Exception(f"Failed to fetch job logs: {response.status_code}")

    def display_pipeline_job_logs(self, project_id, job_id):
        try:
            logs = self.get_pipeline_job_logs(project_id, job_id)
            print(f"Logs for Project: {project_id}, Job: {job_id}\n")
            print(logs)
        except Exception as e:
            print(f"Error fetching logs: {e}")

    def trigger_pipeline(self, project_id, ref="master"):
        headers = {'Private-Token': self.token}
        data = {'ref': ref}
        response = requests.post(f"{self.api_url}/projects/{project_id}/trigger/pipeline", headers=headers, json=data)

        if response.status_code == 201:
            print(f"Pipeline triggered for project {project_id} on branch {ref}")
        else:
            raise Exception(f"Failed to trigger pipeline: {response.status_code}")

