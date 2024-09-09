import requests

class GitHubPR:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{repo}/pulls"

    def get_pull_requests(self, state="open"):
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        params = {'state': state}
        response = requests.get(self.api_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch pull requests: {response.status_code}")

    def display_pull_requests(self, state="open"):
        try:
            pull_requests = self.get_pull_requests(state)
            if pull_requests:
                for pr in pull_requests:
                    print(f"PR #{pr['number']}: {pr['title']} by {pr['user']['login']}")
            else:
                print(f"No {state} pull requests found.")
        except Exception as e:
            print(str(e))
