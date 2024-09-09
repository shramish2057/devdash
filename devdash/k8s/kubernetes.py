from kubernetes import client, config
from kubernetes.client.rest import ApiException
import subprocess

class KubernetesManager:
    def __init__(self):
        # Load the kube config (from ~/.kube/config or the environment)
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

    def list_pods(self, namespace='default'):
        """List all pods in a namespace."""
        try:
            pods = self.v1.list_namespaced_pod(namespace)
            return pods.items
        except ApiException as e:
            raise Exception(f"Failed to list pods: {str(e)}")

    def display_pods(self, namespace='default'):
        """Display all pods in a namespace."""
        try:
            pods = self.list_pods(namespace)
            if pods:
                for pod in pods:
                    print(f"Pod Name: {pod.metadata.name}, Status: {pod.status.phase}")
            else:
                print(f"No pods found in namespace {namespace}.")
        except Exception as e:
            print(f"Error: {e}")

    def get_pod_logs(self, namespace, pod_name):
        """Fetch logs of a specific pod."""
        try:
            logs = self.v1.read_namespaced_pod_log(pod_name, namespace)
            return logs
        except ApiException as e:
            raise Exception(f"Failed to fetch logs for pod {pod_name}: {str(e)}")

    def display_pod_logs(self, namespace, pod_name):
        """Display logs of a specific pod."""
        try:
            logs = self.get_pod_logs(namespace, pod_name)
            print(f"Logs for pod {pod_name}:\n{logs}")
        except Exception as e:
            print(f"Error: {e}")

    def scale_deployment(self, namespace, deployment_name, replicas):
        """Scale a deployment to a specific number of replicas."""
        try:
            body = {"spec": {"replicas": replicas}}
            self.apps_v1.patch_namespaced_deployment_scale(
                name=deployment_name, namespace=namespace, body=body
            )
            print(f"Deployment {deployment_name} scaled to {replicas} replicas.")
        except ApiException as e:
            raise Exception(f"Failed to scale deployment {deployment_name}: {str(e)}")

    def list_services(self, namespace='default'):
        """List all services in a namespace."""
        try:
            services = self.v1.list_namespaced_service(namespace)
            return services.items
        except ApiException as e:
            raise Exception(f"Failed to list services: {str(e)}")

    def display_services(self, namespace='default'):
        """Display all services in a namespace."""
        try:
            services = self.list_services(namespace)
            if services:
                for svc in services:
                    print(f"Service Name: {svc.metadata.name}, Type: {svc.spec.type}")
            else:
                print(f"No services found in namespace {namespace}.")
        except Exception as e:
            print(f"Error: {e}")

    def create_namespace(self, name):
        """Create a new namespace."""
        try:
            body = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
            self.v1.create_namespace(body=body)
            print(f"Namespace {name} created.")
        except ApiException as e:
            raise Exception(f"Failed to create namespace {name}: {str(e)}")

    def delete_namespace(self, name):
        """Delete an existing namespace."""
        try:
            self.v1.delete_namespace(name=name)
            print(f"Namespace {name} deleted.")
        except ApiException as e:
            raise Exception(f"Failed to delete namespace {name}: {str(e)}")
        
    def get_pod_stats(self, namespace, pod_name):
        """Fetch real-time CPU and memory usage for a pod using the Kubernetes Metrics API."""
        try:
            # Metrics API URL (requires metrics-server to be running in the cluster)
            metrics_url = f"/apis/metrics.k8s.io/v1beta1/namespaces/{namespace}/pods/{pod_name}"
            api_client = client.ApiClient()
            response = api_client.call_api(
                metrics_url, "GET", response_type="json", _preload_content=False
            )

            if response[1] == 200:
                metrics = api_client.deserialize(response[0], object)
                return metrics
            else:
                raise Exception(f"Failed to fetch metrics: {response[1]}")
        except ApiException as e:
            raise Exception(f"Failed to get pod stats: {str(e)}")

    def display_pod_stats(self, namespace, pod_name):
        """Display real-time CPU and memory usage for a specific pod."""
        try:
            stats = self.get_pod_stats(namespace, pod_name)
            print(f"Real-Time Stats for Pod: {pod_name}")
            for container in stats['containers']:
                name = container['name']
                cpu = container['usage']['cpu']
                memory = container['usage']['memory']
                print(f"Container: {name}, CPU Usage: {cpu}, Memory Usage: {memory}")
        except Exception as e:
            print(f"Error fetching pod stats: {e}")


class HelmManager:
    def install_chart(self, release_name, chart_name, namespace, values_file=None):
        """Install a Helm chart."""
        try:
            command = ["helm", "install", release_name, chart_name, "--namespace", namespace]
            if values_file:
                command.extend(["-f", values_file])

            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Helm Chart {chart_name} installed successfully with release name {release_name}:\n{result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to install Helm chart: {e.stderr.decode('utf-8')}")

    def upgrade_chart(self, release_name, chart_name, namespace, values_file=None):
        """Upgrade a Helm chart."""
        try:
            command = ["helm", "upgrade", release_name, chart_name, "--namespace", namespace]
            if values_file:
                command.extend(["-f", values_file])

            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Helm Chart {chart_name} upgraded successfully with release name {release_name}:\n{result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to upgrade Helm chart: {e.stderr.decode('utf-8')}")

    def uninstall_chart(self, release_name, namespace):
        """Uninstall a Helm chart."""
        try:
            command = ["helm", "uninstall", release_name, "--namespace", namespace]
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Helm Chart with release name {release_name} uninstalled successfully:\n{result.stdout.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to uninstall Helm chart: {e.stderr.decode('utf-8')}")

