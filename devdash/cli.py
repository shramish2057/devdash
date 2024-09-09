import click
from tabulate import tabulate
import yaml
from devdash.utils.config_loader import get_config, set_config
from devdash.github.pr import GitHubPR
from devdash.github.issues import GitHubIssues
from devdash.github.stats import GitHubStats
from devdash.github.commits import GitHubCommits
from devdash.github.commits import GitHubPushEvents
from devdash.ci.jenkins import JenkinsCI
from devdash.ci.gitlab import GitLabCI
from devdash.ci.circleci import CircleCI
from devdash.docker.docker import DockerManager
from devdash.docker.docker import DockerVolumeManager
from devdash.docker.docker import DockerNetworkManager
from devdash.docker.docker import DockerImageManager
from devdash.k8s.kubernetes import KubernetesManager
from devdash.k8s.kubernetes import HelmManager
from devdash.system.system_metrics import SystemMetrics
import matplotlib.pyplot as plt

@click.group()
def cli():
    """DevDash - Developer Dashboard CLI."""
    pass

# TO DO: Fix detailed report 
# @click.command(name="detailed-report")
# @click.option('--config-file', required=True, help="Path to the YAML configuration file")
# def detailed_report(config_file):
#     """Run detailed report based on the provided YAML configuration file."""
#     with open(config_file, 'r') as file:
#         config = yaml.safe_load(file)

#     results = []
#     metrics_summary = {'CPU Usage': [], 'Memory Usage': [], 'Docker Stats': []}
    
#     # Set of all possible keys for consistency
#     all_keys = set()

#     # Iterate through the YAML configuration
#     for command in config['commands']:
#         for integration, tasks in command.items():
#             if integration == 'github':
#                 run_github_command(tasks, results)
#             elif integration == 'ci':
#                 run_ci_command(tasks, results)
#             elif integration == 'docker':
#                 run_docker_command(tasks, results, metrics_summary)
#             elif integration == 'system':
#                 run_system_command(tasks, results, metrics_summary)
#             elif integration == 'kubernetes':
#                 run_kubernetes_command(tasks, results)
    
#     # Ensure all dictionaries in `results` have the same keys
#     for result in results:
#         all_keys.update(result.keys())  # Collect all possible keys

#     # Add missing keys to ensure consistency
#     for result in results:
#         for key in all_keys:
#             if key not in result:
#                 result[key] = ''  # Fill missing keys with empty values

#     if results:
#         headers = list(all_keys)
#         print(tabulate(results, headers=headers, tablefmt="pretty"))
#     else:
#         print("No results to display.")

#     generate_resource_chart(metrics_summary)

# cli.add_command(detailed_report)  # Registering the command to CLI

# Add the functions to handle different services (GitHub, CI/CD, Docker, System, Kubernetes)
def run_github_command(tasks, results):
    """Run GitHub-related commands."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    for task, params in tasks.items():
        if task == 'pr':
            repo = params['repo']
            state = params.get('state', 'open')
            github_pr = GitHubPR(repo, token)
            prs = github_pr.get_pull_requests(state)
            results.append({"Command": "GitHub PR", "Repo": repo, "State": state, "PRs": len(prs)})

def run_ci_command(tasks, results):
    """Run CI/CD-related commands (Jenkins, GitLab, CircleCI)."""
    for task, params in tasks.items():
        if task == 'jenkins_jobs':
            url = params['jenkins-url']
            username = params['username']
            token = params['token']
            jenkins_ci = JenkinsCI(url, username, token)
            jobs = jenkins_ci.get_jobs()
            results.append({"Command": "Jenkins Jobs", "Jobs": len(jobs)})

def run_docker_command(tasks, results, metrics_summary):
    """Run Docker-related commands."""
    docker_manager = DockerManager()
    for task, params in tasks.items():
        if task == 'container_stats':
            container_id = params['container-id']
            stats = docker_manager.get_container_stats(container_id)
            results.append({"Command": "Docker Stats", "Container": container_id, "CPU Usage": stats['cpu_stats']['cpu_usage']['total_usage']})
            metrics_summary['Docker Stats'].append(stats['cpu_stats']['cpu_usage']['total_usage'])

def run_system_command(tasks, results, metrics_summary):
    """Run system-related commands (CPU, Memory, etc.)."""
    for task, params in tasks.items():
        if task == 'cpu_usage':
            cpu_usage = SystemMetrics.get_cpu_usage()
            results.append({"Command": "CPU Usage", "Usage (%)": f"{cpu_usage}%"})
            metrics_summary['CPU Usage'].append(cpu_usage)

        if task == 'memory_usage':
            memory = SystemMetrics.get_memory_usage()
            memory_percent = memory['percent']
            results.append({"Command": "Memory Usage", "Usage (%)": f"{memory_percent}%"})
            metrics_summary['Memory Usage'].append(memory_percent)

def run_kubernetes_command(tasks, results):
    """Run Kubernetes-related commands."""
    k8s_manager = KubernetesManager()
    for task, params in tasks.items():
        if task == 'list_pods':
            namespace = params.get('namespace', 'default')
            pods = k8s_manager.list_pods(namespace)
            results.append({"Command": "Kubernetes Pods", "Namespace": namespace, "Pods": len(pods)})

def generate_resource_chart(metrics_summary):
    """Generate a resource chart based on collected metrics."""
    plt.figure(figsize=(10, 6))

    # Plot CPU Usage
    if metrics_summary['CPU Usage']:
        plt.plot(metrics_summary['CPU Usage'], label='CPU Usage')

    # Plot Memory Usage
    if metrics_summary['Memory Usage']:
        plt.plot(metrics_summary['Memory Usage'], label='Memory Usage')

    # Plot Docker CPU Stats
    if metrics_summary['Docker Stats']:
        plt.plot(metrics_summary['Docker Stats'], label='Docker CPU Usage')

    plt.title('Resource Metrics Overview')
    plt.xlabel('Time (or Command #)')
    plt.ylabel('Usage (%)')
    plt.legend()
    plt.grid(True)
    plt.show()


# Config related commands
@cli.group()
def config():
    """Configuration commands."""
    pass

@config.command()
@click.option('--github-token', help='GitHub personal access token')
def set(github_token):
    """Set configuration values."""
    if github_token:
        set_config('github_token', github_token)
        click.echo('GitHub token saved.')


# GitHub related commands
@cli.group()
def github():
    """GitHub related commands."""
    pass

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
@click.option('--state', default='open', help='State of pull requests to fetch (open, closed, all)')
def pr(repo, state):
    """Fetch and display pull requests from the GitHub repository."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    github_pr = GitHubPR(repo, token)
    github_pr.display_pull_requests(state)

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
@click.option('--state', default='open', help='State of issues to fetch (open, closed, all)')
def issues(repo, state):
    """Fetch and display issues from the GitHub repository."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    github_issues = GitHubIssues(repo, token)
    github_issues.display_issues(state)

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
def stats(repo):
    """Fetch and display repository statistics."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    github_stats = GitHubStats(repo, token)
    github_stats.display_stats()

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
@click.option('--branch', help='Branch to filter commits')
@click.option('--author', help='Author to filter commits')
@click.option('--since', help='Only commits after this date (YYYY-MM-DD)')
@click.option('--until', help='Only commits before this date (YYYY-MM-DD)')
@click.option('--message', help='Filter commits containing this message')
def commits(repo, branch, author, since, until, message):
    """Fetch and display commits from the GitHub repository."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    github_commits = GitHubCommits(repo, token)
    github_commits.display_commits(branch=branch, author=author, since=since, until=until, message=message)

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
def group_commits_by_user(repo):
    """Fetch and display commits grouped by user."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    github_commits = GitHubCommits(repo, token)
    github_commits.group_commits_by_user()

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
@click.option('--branch', required=True, help='Branch to filter commits')
def group_commits_by_branch(repo, branch):
    """Fetch and display commits grouped by branch."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')
    
    github_commits = GitHubCommits(repo, token)
    github_commits.group_commits_by_branch(branch)

@github.command()
@click.option('--repo', required=True, help='GitHub repository name (e.g., owner/repo)')
def pushes(repo):
    """Fetch and display push events from the GitHub repository."""
    token = get_config('github_token')
    if not token:
        raise click.UsageError('GitHub token not set. Use "devdash config set --github-token <token>" to set it.')

    github_push_events = GitHubPushEvents(repo, token)
    github_push_events.display_push_events()


# CI/CD related commands
@cli.group()
def ci():
    """CI/CD related commands."""
    pass

@ci.command()
@click.option('--jenkins-url', required=True, help='Jenkins server URL (e.g., http://localhost:8080)')
@click.option('--username', required=True, help='Jenkins username')
@click.option('--token', required=True, help='Jenkins API token or password')
def jenkins_jobs(jenkins_url, username, token):
    """Fetch and display Jenkins jobs."""
    jenkins_ci = JenkinsCI(jenkins_url, username, token)
    jenkins_ci.display_jobs()

@ci.command()
@click.option('--jenkins-url', required=True, help='Jenkins server URL (e.g., http://localhost:8080)')
@click.option('--username', required=True, help='Jenkins username')
@click.option('--token', required=True, help='Jenkins API token or password')
@click.option('--job', required=True, help='Jenkins job name')
def jenkins_job_status(jenkins_url, username, token, job):
    """Fetch and display Jenkins job status."""
    jenkins_ci = JenkinsCI(jenkins_url, username, token)
    status = jenkins_ci.get_job_status(job)
    print(f"Job {job} status: {status}")

@ci.command()
@click.option('--jenkins-url', required=True, help='Jenkins server URL (e.g., http://localhost:8080)')
@click.option('--username', required=True, help='Jenkins username')
@click.option('--token', required=True, help='Jenkins API token or password')
@click.option('--job', required=True, help='Jenkins job name')
@click.option('--build-number', required=True, help='Build number to fetch logs for')
def jenkins_build_logs(jenkins_url, username, token, job, build_number):
    """Fetch and display Jenkins build logs."""
    jenkins_ci = JenkinsCI(jenkins_url, username, token)
    jenkins_ci.display_build_logs(job, build_number)

@ci.command()
@click.option('--jenkins-url', required=True, help='Jenkins server URL (e.g., http://localhost:8080)')
@click.option('--username', required=True, help='Jenkins username')
@click.option('--token', required=True, help='Jenkins API token or password')
@click.option('--job', required=True, help='Jenkins job name')
def jenkins_trigger_build(jenkins_url, username, token, job):
    """Trigger a new Jenkins build."""
    jenkins_ci = JenkinsCI(jenkins_url, username, token)
    jenkins_ci.trigger_build(job)

@ci.command()
@click.option('--gitlab-url', required=True, help='GitLab server URL (e.g., https://gitlab.com)')
@click.option('--token', required=True, help='GitLab personal access token')
def gitlab_projects(gitlab_url, token):
    """Fetch and display GitLab projects."""
    gitlab_ci = GitLabCI(gitlab_url, token)
    gitlab_ci.display_projects()

@ci.command()
@click.option('--gitlab-url', required=True, help='GitLab server URL (e.g., https://gitlab.com)')
@click.option('--token', required=True, help='GitLab personal access token')
@click.option('--project-id', required=True, help='GitLab project ID')
def gitlab_pipeline_status(gitlab_url, token, project_id):
    """Fetch and display GitLab pipeline status for a specific project."""
    gitlab_ci = GitLabCI(gitlab_url, token)
    status = gitlab_ci.get_pipeline_status(project_id)
    print(f"Pipeline status for project {project_id}: {status}")

@ci.command()
@click.option('--gitlab-url', required=True, help='GitLab server URL (e.g., https://gitlab.com)')
@click.option('--token', required=True, help='GitLab personal access token')
@click.option('--project-id', required=True, help='GitLab project ID')
@click.option('--job-id', required=True, help='Job ID to fetch logs for')
def gitlab_job_logs(gitlab_url, token, project_id, job_id):
    """Fetch and display GitLab job logs."""
    gitlab_ci = GitLabCI(gitlab_url, token)
    gitlab_ci.display_pipeline_job_logs(project_id, job_id)

@ci.command()
@click.option('--gitlab-url', required=True, help='GitLab server URL (e.g., https://gitlab.com)')
@click.option('--token', required=True, help='GitLab personal access token')
@click.option('--project-id', required=True, help='GitLab project ID')
@click.option('--ref', default="master", help='Branch or tag to trigger the pipeline (default: master)')
def gitlab_trigger_pipeline(gitlab_url, token, project_id, ref):
    """Trigger a new GitLab pipeline."""
    gitlab_ci = GitLabCI(gitlab_url, token)
    gitlab_ci.trigger_pipeline(project_id, ref)

@ci.command()
@click.option('--circle-token', required=True, help='CircleCI personal access token')
def circleci_projects(circle_token):
    """Fetch and display CircleCI projects."""
    circle_ci = CircleCI(circle_token)
    circle_ci.display_projects()

@ci.command()
@click.option('--circle-token', required=True, help='CircleCI personal access token')
@click.option('--project-slug', required=True, help='CircleCI project slug (e.g., gh/owner/repo)')
def circleci_pipeline_status(circle_token, project_slug):
    """Fetch and display CircleCI pipeline status."""
    circle_ci = CircleCI(circle_token)
    status = circle_ci.get_pipeline_status(project_slug)
    print(f"Pipeline status for project {project_slug}: {status}")

@ci.command()
@click.option('--circle-token', required=True, help='CircleCI personal access token')
@click.option('--job-id', required=True, help='CircleCI Job ID to fetch logs for')
def circleci_job_logs(circle_token, job_id):
    """Fetch and display CircleCI job logs."""
    circle_ci = CircleCI(circle_token)
    circle_ci.display_pipeline_job_logs(job_id)

@ci.command()
@click.option('--circle-token', required=True, help='CircleCI personal access token')
@click.option('--project-slug', required=True, help='CircleCI project slug (e.g., gh/owner/repo)')
@click.option('--branch', default="main", help='Branch to trigger pipeline (default: main)')
def circleci_trigger_pipeline(circle_token, project_slug, branch):
    """Trigger a new CircleCI pipeline."""
    circle_ci = CircleCI(circle_token)
    circle_ci.trigger_pipeline(project_slug, branch)

# Docker-related commands
@ci.group()
def docker():
    """Docker related commands."""
    pass

@docker.command()
@click.option('--all', is_flag=True, help='Show all containers (default shows only running containers)')
def list_containers(all):
    """List all Docker containers."""
    docker_manager = DockerManager()
    docker_manager.display_containers(all=all)

@docker.command()
@click.option('--container-id', required=True, help='Docker container ID or name')
def view_logs(container_id):
    """Fetch and display logs of a Docker container."""
    docker_manager = DockerManager()
    docker_manager.display_logs(container_id)

@docker.command()
@click.option('--container-id', required=True, help='Docker container ID or name')
def start_container(container_id):
    """Start a Docker container."""
    docker_manager = DockerManager()
    docker_manager.start_container(container_id)

@docker.command()
@click.option('--container-id', required=True, help='Docker container ID or name')
def stop_container(container_id):
    """Stop a Docker container."""
    docker_manager = DockerManager()
    docker_manager.stop_container(container_id)

@docker.command()
@click.option('--container-id', required=True, help='Docker container ID or name')
def container_stats(container_id):
    """Fetch and display real-time Docker container stats."""
    docker_manager = DockerManager()
    docker_manager.display_stats(container_id)

@docker.command()
@click.option('--container-id', required=True, help='Docker container ID or name')
@click.option('--command', required=True, help='Command to execute inside the container')
def exec_command(container_id, command):
    """Execute a command inside a Docker container."""
    docker_manager = DockerManager()
    docker_manager.exec_command_in_container(container_id, command)

@docker.command()
def list_volumes():
    """List all Docker volumes."""
    volume_manager = DockerVolumeManager()
    volume_manager.display_volumes()

@docker.command()
@click.option('--name', required=True, help='Volume name')
def create_volume(name):
    """Create a Docker volume."""
    volume_manager = DockerVolumeManager()
    volume_manager.create_volume(name)

@docker.command()
@click.option('--name', required=True, help='Volume name')
def remove_volume(name):
    """Remove a Docker volume."""
    volume_manager = DockerVolumeManager()
    volume_manager.remove_volume(name)

@docker.command()
@click.option('--name', required=True, help='Volume name')
def inspect_volume(name):
    """Inspect a Docker volume."""
    volume_manager = DockerVolumeManager()
    volume_manager.display_volume_info(name)

@docker.command()
def list_networks():
    """List all Docker networks."""
    network_manager = DockerNetworkManager()
    network_manager.display_networks()

@docker.command()
@click.option('--name', required=True, help='Network name')
def create_network(name):
    """Create a Docker network."""
    network_manager = DockerNetworkManager()
    network_manager.create_network(name)

@docker.command()
@click.option('--name', required=True, help='Network name')
def remove_network(name):
    """Remove a Docker network."""
    network_manager = DockerNetworkManager()
    network_manager.remove_network(name)

@docker.command()
@click.option('--name', required=True, help='Network name')
def inspect_network(name):
    """Inspect a Docker network."""
    network_manager = DockerNetworkManager()
    network_manager.display_network_info(name)

@docker.command()
@click.option('--path', required=True, help='Path to the Dockerfile directory')
@click.option('--tag', required=True, help='Tag to assign to the image')
def build_image(path, tag):
    """Build a Docker image from a Dockerfile."""
    image_manager = DockerImageManager()
    image_manager.build_image(path, tag)

@docker.command()
def list_images():
    """List all Docker images."""
    image_manager = DockerImageManager()
    image_manager.display_images()

# Kubernetes-related commands
@ci.group()
def kubernetes():
    """Kubernetes related commands."""
    pass

@kubernetes.command()
@click.option('--namespace', default='default', help='Kubernetes namespace')
def list_pods(namespace):
    """List all Kubernetes pods in a namespace."""
    k8s_manager = KubernetesManager()
    k8s_manager.display_pods(namespace)

@kubernetes.command()
@click.option('--namespace', required=True, help='Kubernetes namespace')
@click.option('--pod-name', required=True, help='Pod name')
def pod_logs(namespace, pod_name):
    """Fetch and display logs of a specific Kubernetes pod."""
    k8s_manager = KubernetesManager()
    k8s_manager.display_pod_logs(namespace, pod_name)

@kubernetes.command()
@click.option('--namespace', required=True, help='Kubernetes namespace')
@click.option('--deployment-name', required=True, help='Deployment name')
@click.option('--replicas', required=True, type=int, help='Number of replicas to scale to')
def scale_deployment(namespace, deployment_name, replicas):
    """Scale a Kubernetes deployment."""
    k8s_manager = KubernetesManager()
    k8s_manager.scale_deployment(namespace, deployment_name, replicas)

@kubernetes.command()
@click.option('--namespace', default='default', help='Kubernetes namespace')
def list_services(namespace):
    """List all Kubernetes services in a namespace."""
    k8s_manager = KubernetesManager()
    k8s_manager.display_services(namespace)

@kubernetes.command()
@click.option('--name', required=True, help='Namespace name')
def create_namespace(name):
    """Create a new Kubernetes namespace."""
    k8s_manager = KubernetesManager()
    k8s_manager.create_namespace(name)

@kubernetes.command()
@click.option('--name', required=True, help='Namespace name')
def delete_namespace(name):
    """Delete an existing Kubernetes namespace."""
    k8s_manager = KubernetesManager()
    k8s_manager.delete_namespace(name)

@kubernetes.command()
@click.option('--namespace', required=True, help='Kubernetes namespace')
@click.option('--pod-name', required=True, help='Pod name')
def pod_stats(namespace, pod_name):
    """Fetch and display real-time stats (CPU/Memory usage) for a Kubernetes pod."""
    k8s_manager = KubernetesManager()
    k8s_manager.display_pod_stats(namespace, pod_name)

@kubernetes.command()
@click.option('--release-name', required=True, help='Release name for the Helm chart')
@click.option('--chart-name', required=True, help='Helm chart name (e.g., stable/nginx)')
@click.option('--namespace', required=True, help='Kubernetes namespace')
@click.option('--values-file', help='Optional values file for Helm chart')
def helm_install(release_name, chart_name, namespace, values_file):
    """Install a Helm chart."""
    helm_manager = HelmManager()
    helm_manager.install_chart(release_name, chart_name, namespace, values_file)

@kubernetes.command()
@click.option('--release-name', required=True, help='Release name for the Helm chart')
@click.option('--chart-name', required=True, help='Helm chart name (e.g., stable/nginx)')
@click.option('--namespace', required=True, help='Kubernetes namespace')
@click.option('--values-file', help='Optional values file for Helm chart')
def helm_upgrade(release_name, chart_name, namespace, values_file):
    """Upgrade an existing Helm chart."""
    helm_manager = HelmManager()
    helm_manager.upgrade_chart(release_name, chart_name, namespace, values_file)

@kubernetes.command()
@click.option('--release-name', required=True, help='Release name for the Helm chart')
@click.option('--namespace', required=True, help='Kubernetes namespace')
def helm_uninstall(release_name, namespace):
    """Uninstall a Helm chart."""
    helm_manager = HelmManager()
    helm_manager.uninstall_chart(release_name, namespace)


# System Monitoring
@cli.group()
def system():
    """System monitoring commands."""
    pass

@system.command()
def cpu_usage():
    """Show current CPU usage."""
    usage = SystemMetrics.get_cpu_usage()
    print(f"Current CPU usage: {usage}%")

@system.command()
def memory_usage():
    """Show current memory usage."""
    memory = SystemMetrics.get_memory_usage()
    print(f"Memory Usage: {memory['percent']}% (Used: {memory['used'] / (1024**3):.2f} GB / Total: {memory['total'] / (1024**3):.2f} GB)")

@system.command()
def disk_usage():
    """Show current disk usage."""
    disk = SystemMetrics.get_disk_usage()
    print(f"Disk Usage: {disk['percent']}% (Used: {disk['used'] / (1024**3):.2f} GB / Total: {disk['total'] / (1024**3):.2f} GB)")

@system.command()
def network_stats():
    """Show current network traffic stats."""
    network = SystemMetrics.get_network_stats()
    print(f"Network Stats: Sent {network['bytes_sent'] / (1024**2):.2f} MB, Received {network['bytes_recv'] / (1024**2):.2f} MB")

@system.command()
def system_info():
    """Show basic system information."""
    info = SystemMetrics.get_system_info()
    print(f"System Info: {info}")

@system.command()
def boot_time():
    """Show system boot time."""
    boot_time = SystemMetrics.get_boot_time()
    print(f"System Boot Time: {boot_time}")

@system.command()
def all_metrics():
    """Show all system metrics."""
    SystemMetrics.display_system_metrics()

@system.command()
@click.option('--interval', default=1, help='Refresh interval in seconds')
def live_metrics(interval):
    """Show continuously updated system metrics (e.g., every second)."""
    SystemMetrics.live_system_metrics(refresh_interval=interval)

@system.command()
@click.option('--cpu-threshold', default=90, help='CPU usage threshold for alerts')
@click.option('--memory-threshold', default=90, help='Memory usage threshold for alerts')
def threshold_alerts(cpu_threshold, memory_threshold):
    """Alert if system metrics exceed specified thresholds (e.g., CPU > 90%)."""
    SystemMetrics.alert_on_thresholds(cpu_threshold, memory_threshold)

@system.command()
@click.option('--filename', default='system_metrics_history.csv', help='File to record historical metrics')
def record_metrics(filename):
    """Record system metrics to a file for historical analysis."""
    SystemMetrics.record_metrics_to_csv(filename)

if __name__ == '__main__':
    cli()
