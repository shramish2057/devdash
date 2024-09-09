import requests

class CircleCI:
    def __init__(self, circle_token):
        self.circle_token = circle_token
        self.api_url = "https://circleci.com/api/v2"

    def get_projects(self):
        headers = {'Circle-Token': self.circle_token}
        response = requests.get(f"{self.api_url}/project", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch CircleCI projects: {response.status_code}")

    def get_pipeline_status(self, project_slug):
        headers = {'Circle-Token': self.circle_token}
        response = requests.get(f"{self.api_url}/project/{project_slug}/pipeline", headers=headers)

        if response.status_code == 200:
            pipelines = response.json()
            if pipelines['items']:
                latest_pipeline = pipelines['items'][0]
                return latest_pipeline['state']
            else:
                print("No pipelines found.")
        else:
            raise Exception(f"Failed to fetch CircleCI pipelines: {response.status_code}")

    def display_projects(self):
        try:
            projects = self.get_projects()
            for project in projects:
                print(f"Project: {project['slug']}")
        except Exception as e:
            print(str(e))

    def get_pipeline_job_logs(self, job_id):
        headers = {'Circle-Token': self.circle_token}
        response = requests.get(f"{self.api_url}/job/{job_id}/output", headers=headers)

        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            raise Exception(f"Job {job_id} not found.")
        else:
            raise Exception(f"Failed to fetch job logs: {response.status_code}")

    def display_pipeline_job_logs(self, job_id):
        try:
            logs = self.get_pipeline_job_logs(job_id)
            print(f"Logs for Job: {job_id}\n")
            print(logs)
        except Exception as e:
            print(f"Error fetching logs: {e}")

    def trigger_pipeline(self, project_slug, branch="main"):
        headers = {'Circle-Token': self.circle_token}
        data = {"branch": branch}
        response = requests.post(f"{self.api_url}/project/{project_slug}/pipeline", headers=headers, json=data)

        if response.status_code == 201:
            print(f"Pipeline triggered for project {project_slug} on branch {branch}")
        else:
            raise Exception(f"Failed to trigger pipeline: {response.status_code}")
