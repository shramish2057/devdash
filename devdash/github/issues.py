import requests

class GitHubIssues:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{repo}/issues"

    def get_issues(self, state="open"):
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        params = {'state': state}
        response = requests.get(self.api_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch issues: {response.status_code}")

    def display_issues(self, state="open"):
        try:
            issues = self.get_issues(state)
            if issues:
                for issue in issues:
                    print(f"Issue #{issue['number']}: {issue['title']} by {issue['user']['login']}")
            else:
                print(f"No {state} issues found.")
        except Exception as e:
            print(str(e))
