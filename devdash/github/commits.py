import requests

class GitHubCommits:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{repo}/commits"

    def get_commits(self, branch=None, author=None, since=None, until=None, message=None):
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        params = {}
        if branch:
            params['sha'] = branch
        if author:
            params['author'] = author
        if since:
            params['since'] = since
        if until:
            params['until'] = until

        response = requests.get(self.api_url, headers=headers, params=params)

        if response.status_code == 200:
            commits = response.json()
            if message:
                # Filter commits by commit message
                commits = [commit for commit in commits if message.lower() in commit['commit']['message'].lower()]
            return commits
        else:
            raise Exception(f"Failed to fetch commits: {response.status_code}")

    def display_commits(self, branch=None, author=None, since=None, until=None, message=None):
        try:
            commits = self.get_commits(branch, author, since, until, message)
            if commits:
                for commit in commits:
                    sha = commit['sha']
                    commit_message = commit['commit']['message']
                    author_name = commit['commit']['author']['name']
                    commit_date = commit['commit']['author']['date']
                    print(f"Commit {sha[:7]} by {author_name} on {commit_date}: {commit_message}")
            else:
                print(f"No commits found for the specified filters.")
        except Exception as e:
            print(str(e))

    def group_commits_by_user(self):
        try:
            commits = self.get_commits()
            grouped = {}
            for commit in commits:
                author_name = commit['commit']['author']['name']
                if author_name not in grouped:
                    grouped[author_name] = []
                grouped[author_name].append(commit)
            
            for author, author_commits in grouped.items():
                print(f"\nCommits by {author}:")
                for commit in author_commits:
                    sha = commit['sha']
                    message = commit['commit']['message']
                    print(f"  Commit {sha[:7]}: {message}")
        except Exception as e:
            print(str(e))

    def group_commits_by_branch(self, branch):
        self.display_commits(branch=branch)

class GitHubPushEvents:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.api_url = f"https://api.github.com/repos/{repo}/events"

    def get_push_events(self):
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(self.api_url, headers=headers)

        if response.status_code == 200:
            events = response.json()
            push_events = [event for event in events if event['type'] == 'PushEvent']
            return push_events
        else:
            raise Exception(f"Failed to fetch push events: {response.status_code}")

    def display_push_events(self):
        try:
            push_events = self.get_push_events()
            if push_events:
                for event in push_events:
                    pusher = event['actor']['login']
                    commit_count = event['payload']['size']
                    branch = event['payload']['ref'].replace('refs/heads/', '')
                    print(f"Pusher: {pusher} pushed {commit_count} commit(s) to branch {branch}")
            else:
                print("No push events found.")
        except Exception as e:
            print(str(e))
