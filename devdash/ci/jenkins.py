import requests
from requests.auth import HTTPBasicAuth

class JenkinsCI:
    def __init__(self, jenkins_url, username, token):
        self.jenkins_url = jenkins_url
        self.username = username
        self.token = token
        self.api_url = f"{jenkins_url}/api/json"

    def get_jobs(self):
        response = requests.get(self.api_url, auth=HTTPBasicAuth(self.username, self.token))

        if response.status_code == 200:
            jobs = response.json().get('jobs', [])
            return jobs
        else:
            raise Exception(f"Failed to fetch Jenkins jobs: {response.status_code}")

    def display_jobs(self):
        try:
            jobs = self.get_jobs()
            if jobs:
                for job in jobs:
                    name = job['name']
                    color = job['color']  # "color" represents job status (e.g., "blue" = success)
                    print(f"Job: {name}, Status: {color}")
            else:
                print("No jobs found.")
        except Exception as e:
            print(str(e))

    def get_job_status(self, job_name):
        job_url = f"{self.jenkins_url}/job/{job_name}/api/json"
        response = requests.get(job_url, auth=HTTPBasicAuth(self.username, self.token))

        if response.status_code == 200:
            job_info = response.json()
            last_build = job_info['lastBuild']
            build_status = last_build.get('result', 'IN PROGRESS')
            return build_status
        else:
            raise Exception(f"Failed to fetch job status for {job_name}: {response.status_code}")
        
    def get_build_logs(self, job_name, build_number):
        build_url = f"{self.jenkins_url}/job/{job_name}/{build_number}/consoleText"
        response = requests.get(build_url, auth=HTTPBasicAuth(self.username, self.token))

        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            raise Exception(f"Build {build_number} not found for job {job_name}.")
        else:
            raise Exception(f"Failed to fetch build logs: {response.status_code}")

    def display_build_logs(self, job_name, build_number):
        try:
            logs = self.get_build_logs(job_name, build_number)
            print(f"Logs for Job: {job_name}, Build: {build_number}\n")
            print(logs)
        except Exception as e:
            print(f"Error fetching logs: {e}")

    def trigger_build(self, job_name):
        build_url = f"{self.jenkins_url}/job/{job_name}/build"
        response = requests.post(build_url, auth=HTTPBasicAuth(self.username, self.token))

        if response.status_code == 201:
            print(f"Build triggered for job: {job_name}")
        else:
            raise Exception(f"Failed to trigger build: {response.status_code}")
