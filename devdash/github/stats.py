import requests

class GitHubStats:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{repo}"

    def get_stats(self):
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(self.api_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch repository stats: {response.status_code}")

    def display_stats(self):
        try:
            stats = self.get_stats()
            print(f"Repository: {stats['name']}")
            print(f"Stars: {stats['stargazers_count']}")
            print(f"Forks: {stats['forks_count']}")
            print(f"Watchers: {stats['watchers_count']}")
            print(f"Open Issues: {stats['open_issues_count']}")
        except Exception as e:
            print(str(e))
