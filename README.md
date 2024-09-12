<h1 align="center">
DevDash: Developer Dashboard CLI </> 🐳 ☸ 🛠️
</h1>
<div align="center">

<img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg" alt="Awesome Badge"/>
<a href="https://arbeitnow.com/?utm_source=devdash"><img src="https://img.shields.io/static/v1?label=&labelColor=505050&message=arbeitnow&color=%230076D6&style=flat&logo=google-chrome&logoColor=%230076D6" alt="website"/></a>
<!-- <img src="http://hits.dwyl.com/shramish2057/devdash.svg" alt="Hits Badge"/> -->
<img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
<a href="https://discord.gg"><img src="https://img.shields.io/discord/733027681184251937.svg?style=flat&label=Join%20Community&color=7289DA" alt="Join Community Badge"/></a>
<a href="https://twitter.com/shramish2057" ><img src="https://img.shields.io/twitter/follow/shramish2057.svg?style=social" /> </a>
<br>

<i>Developer Dashboard CLI</i>

<a href="https://github.com/shramish2057/devdash/stargazers"><img src="https://img.shields.io/github/stars/shramish2057/devdash" alt="Stars Badge"/></a>
<a href="https://github.com/shramish2057/devdash/network/members"><img src="https://img.shields.io/github/forks/shramish2057/devdash" alt="Forks Badge"/></a>
<a href="https://github.com/shramish2057/devdash/pulls"><img src="https://img.shields.io/github/issues-pr/shramish2057/devdash" alt="Pull Requests Badge"/></a>
<a href="https://github.com/shramish2057/devdash/issues"><img src="https://img.shields.io/github/issues/shramish2057/devdash" alt="Issues Badge"/></a>
<a href="https://github.com/shramish2057/devdash/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/shramish2057/devdash?color=2b9348"></a>
<a href="https://github.com/shramish2057/devdash/blob/master/LICENSE"><img src="https://img.shields.io/github/license/shramish2057/devdash?color=2b9348" alt="License Badge"/></a>

<img alt="DevDash Readme" src="assets/agpr.gif"> </img>

<i>Liked the project? We'd love your contributions! Help us make it even better!</i>

</div>

# DevDash: Developer Dashboard CLI

**DevDash** is a command-line interface (CLI) tool designed to streamline and simplify the monitoring of repositories, CI/CD pipelines, system metrics, and other essential tools for developers. It provides integrations with popular platforms such as GitHub, Jenkins, GitLab, CircleCI, Docker, Kubernetes, and system-level monitoring.

## Features Overview

1. **CI/CD Pipeline Monitoring**: Monitor jobs, pipelines, and statuses across Jenkins, GitLab CI, CircleCI.
2. **GitHub Integrations**: Fetch and display GitHub pull requests, issues, commits, statistics, and more.
3. **Docker and Kubernetes Management**: Manage Docker containers, networks, and volumes, and monitor Kubernetes pods and deployments.
4. **System Monitoring**: Monitor CPU, memory, disk usage, network stats, and more, with threshold alerts and live monitoring.
5. **Configuration Management**: Set and manage configurations for GitHub and other integrations.

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
  - [CI/CD Commands](#cicd-commands)
  - [GitHub Commands](#github-commands)
  - [Docker Commands](#docker-commands)
  - [Kubernetes Commands](#kubernetes-commands)
  - [System Monitoring Commands](#system-monitoring-commands)
  - [Configuration Commands](#configuration-commands)
- [Examples](#examples)
- [Contributions](#contributions)
- [License](#license)

---

## Installation

### 1. Clone the DevDash repository:
   ```bash
   git clone https://github.com/shramish2057/devdash
   ```

### 2. Navigate into the project directory:

```bash
cd devdash
```

### 3. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install the required dependencies:

```bash
pip install -r requirements.txt
```
### 5. Install DevDash CLI:

```bash
python setup.py install
```

## Usage
You can invoke the devdash command from your terminal to access different developer tools.

### To view help for DevDash, run:

```bash
devdash --help
```
Each command group (e.g., ci, github, docker) has its own set of subcommands. You can view the available subcommands by using the --help option:

```bash
devdash ci --help
```

## Commands

### CI/CD Commands
The ci command allows you to interact with Jenkins, GitLab, CircleCI, and Docker environments.

##### Available CI/CD Subcommands:

#### Jenkins

- jenkins-jobs: Fetch and display Jenkins jobs.
- jenkins-job-status: Get the status of a specific Jenkins job.
- jenkins-build-logs: Fetch build logs for a Jenkins job.
- jenkins-trigger-build: Trigger a new Jenkins job build.

#### GitLab

- gitlab-projects: List all projects in GitLab.
- gitlab-pipeline-status: Check the pipeline status for a GitLab project.
- gitlab-job-logs: Fetch job logs for a GitLab pipeline.
- gitlab-trigger-pipeline: Trigger a GitLab pipeline.

#### CircleCI

- circleci-projects: List all CircleCI projects.
- circleci-pipeline-status: Get the pipeline status of a CircleCI project.
- circleci-job-logs: Fetch CircleCI job logs.
- circleci-trigger-pipeline: Trigger a new CircleCI pipeline.


### GitHub Commands
The github command provides integration with GitHub for managing repositories.

Available GitHub Subcommands:
#### Pull Requests

- pr: Fetch and display pull requests from a GitHub repository.

#### Commits

- commits: Display commits from a GitHub repository.
- group-commits-by-user: Group and display commits by user.
- group-commits-by-branch: Group and display commits by branch.

#### Issues

- issues: Fetch and display issues from a GitHub repository.

#### Statistics

- stats: Display repository statistics such as stars, forks, etc.

#### Push Events

- pushes: Fetch and display push events from a GitHub repository.

### Docker Commands
The docker command group allows you to interact with Docker containers, volumes, and networks.

##### Available Docker Subcommands:
#### Containers

- list-containers: List all Docker containers.
- start-container: Start a Docker container.
- stop-container: Stop a Docker container.
- view-logs: View logs of a Docker container.

#### Volumes

- list-volumes: List all Docker volumes.
- create-volume: Create a new Docker volume.
- remove-volume: Remove a Docker volume.

#### Networks

- list-networks: List all Docker networks.
- create-network: Create a new Docker network.
- remove-network: Remove a Docker network.

### Kubernetes Commands
The kubernetes command group allows you to manage Kubernetes resources.

##### Available Kubernetes Subcommands:
#### Pods
- list-pods: List all Kubernetes pods in a namespace.
- pod-logs: View logs of a specific pod.
- pod-stats: View real-time CPU/Memory stats for a pod.

#### Deployments
- scale-deployment: Scale a Kubernetes deployment to a specific number of replicas.

#### Helm
- helm-install: Install a Helm chart.
- helm-upgrade: Upgrade an existing Helm chart.
- helm-uninstall: Uninstall a Helm chart.

#### System Monitoring Commands
The system command allows you to monitor system-level metrics like CPU, memory, disk usage, and more.

### Available System Monitoring Subcommands:

#### CPU

- cpu-usage: Show the current CPU usage.

#### Memory

- memory-usage: Show the current memory usage.

#### Disk

- disk-usage: Show the current disk usage.

#### Network

- network-stats: Show current network traffic statistics.

#### System Info

- system-info: Display basic system information such as OS, architecture, etc.

#### Live Monitoring

- live-metrics: Continuously monitor system metrics with a refresh interval.

#### Alerts

- threshold-alerts: Set alerts if system metrics exceed specific thresholds.

#### Recording Metrics

- record-metrics: Record system metrics to a file for historical analysis.

### Configuration Commands
The config command allows you to manage DevDash configurations, such as setting tokens for integrations (e.g., GitHub).

##### Available Configuration Subcommands:

#### Set Configuration
- set: Set configuration values like GitHub personal access tokens.

## Examples
### Fetching GitHub Pull Requests:

```bash
devdash github pr --repo=owner/repo --state=open
```

### Fetching Jenkins Jobs:

```bash
devdash ci jenkins-jobs --jenkins-url=http://localhost:8080 --username=admin --token=your_token
```
### Listing Docker Containers:

```bash
devdash ci docker list-containers
```
### Monitoring CPU Usage:

```bash
devdash system cpu-usage
```
### Triggering a GitLab Pipeline:

```bash
devdash ci gitlab-trigger-pipeline --gitlab-url=https://gitlab.com --token=your_token --project-id=12345 --ref=master
```

## Contributions
We welcome contributions from the community! Feel free to submit pull requests, open issues, and suggest new features.

## How to Contribute:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with a detailed explanation of your changes.

## License
This project is licensed under the MIT License.


