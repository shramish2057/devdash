import docker
from docker.errors import NotFound, APIError

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()

    def list_containers(self, all=False):
        """List all running/stopped containers."""
        try:
            containers = self.client.containers.list(all=all)
            return containers
        except APIError as e:
            raise Exception(f"Failed to list containers: {str(e)}")

    def display_containers(self, all=False):
        """Display all containers."""
        try:
            containers = self.list_containers(all=all)
            if containers:
                for container in containers:
                    print(f"Container ID: {container.short_id}, Name: {container.name}, Status: {container.status}")
            else:
                print("No containers found.")
        except Exception as e:
            print(f"Error: {e}")

    def view_logs(self, container_id):
        """Fetch and display logs of a specific container."""
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs().decode('utf-8')
            return logs
        except NotFound:
            raise Exception(f"Container {container_id} not found.")
        except APIError as e:
            raise Exception(f"Failed to fetch logs for container {container_id}: {str(e)}")

    def display_logs(self, container_id):
        """Display logs of a specific container."""
        try:
            logs = self.view_logs(container_id)
            print(f"Logs for container {container_id}:\n{logs}")
        except Exception as e:
            print(f"Error: {e}")

    def start_container(self, container_id):
        """Start a stopped container."""
        try:
            container = self.client.containers.get(container_id)
            container.start()
            print(f"Container {container_id} started.")
        except NotFound:
            raise Exception(f"Container {container_id} not found.")
        except APIError as e:
            raise Exception(f"Failed to start container {container_id}: {str(e)}")

    def stop_container(self, container_id):
        """Stop a running container."""
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            print(f"Container {container_id} stopped.")
        except NotFound:
            raise Exception(f"Container {container_id} not found.")
        except APIError as e:
            raise Exception(f"Failed to stop container {container_id}: {str(e)}")

    def get_container_stats(self, container_id):
        """Fetch and display real-time container stats (CPU, memory, I/O, network, etc.)."""
        try:
            container = self.client.containers.get(container_id)
            stats = container.stats(stream=False)
            return stats
        except NotFound:
            raise Exception(f"Container {container_id} not found.")
        except APIError as e:
            raise Exception(f"Failed to fetch stats for container {container_id}: {str(e)}")

    def display_stats(self, container_id):
        """Display real-time container stats (CPU, memory, I/O, network, etc.)."""
        try:
            stats = self.get_container_stats(container_id)
            print(f"Stats for container {container_id}:")
            print(f"CPU Usage: {stats['cpu_stats']['cpu_usage']['total_usage']}")
            print(f"Memory Usage: {stats['memory_stats']['usage']} bytes")
            print(f"Memory Limit: {stats['memory_stats']['limit']} bytes")
            print(f"Block I/O: {stats['blkio_stats']['io_service_bytes_recursive']}")
            print(f"Network Traffic: {stats['networks']}")
        except Exception as e:
            print(f"Error: {e}")

    def exec_command_in_container(self, container_id, command):
        """Execute a command inside a running container."""
        try:
            container = self.client.containers.get(container_id)
            exec_log = container.exec_run(command)
            print(f"Executed command '{command}' in container {container_id}:\n{exec_log.output.decode('utf-8')}")
        except NotFound:
            raise Exception(f"Container {container_id} not found.")
        except APIError as e:
            raise Exception(f"Failed to execute command in container {container_id}: {str(e)}")


class DockerVolumeManager:
    def __init__(self):
        self.client = docker.from_env()

    def list_volumes(self):
        """List all Docker volumes."""
        try:
            volumes = self.client.volumes.list()
            return volumes
        except APIError as e:
            raise Exception(f"Failed to list volumes: {str(e)}")

    def create_volume(self, name):
        """Create a Docker volume."""
        try:
            volume = self.client.volumes.create(name=name)
            print(f"Volume {name} created.")
        except APIError as e:
            raise Exception(f"Failed to create volume {name}: {str(e)}")

    def remove_volume(self, name):
        """Remove a Docker volume."""
        try:
            volume = self.client.volumes.get(name)
            volume.remove()
            print(f"Volume {name} removed.")
        except NotFound:
            raise Exception(f"Volume {name} not found.")
        except APIError as e:
            raise Exception(f"Failed to remove volume {name}: {str(e)}")

    def inspect_volume(self, name):
        """Inspect a Docker volume."""
        try:
            volume = self.client.volumes.get(name)
            return volume.attrs
        except NotFound:
            raise Exception(f"Volume {name} not found.")
        except APIError as e:
            raise Exception(f"Failed to inspect volume {name}: {str(e)}")

    def display_volumes(self):
        """Display all Docker volumes."""
        try:
            volumes = self.list_volumes()
            for volume in volumes:
                print(f"Volume Name: {volume.name}, Driver: {volume.attrs['Driver']}")
        except Exception as e:
            print(f"Error: {e}")

    def display_volume_info(self, name):
        """Display information about a Docker volume."""
        try:
            info = self.inspect_volume(name)
            print(f"Volume {name} Info: {info}")
        except Exception as e:
            print(f"Error: {e}")

class DockerNetworkManager:
    def __init__(self):
        self.client = docker.from_env()

    def list_networks(self):
        """List all Docker networks."""
        try:
            networks = self.client.networks.list()
            return networks
        except APIError as e:
            raise Exception(f"Failed to list networks: {str(e)}")

    def create_network(self, name):
        """Create a Docker network."""
        try:
            network = self.client.networks.create(name=name)
            print(f"Network {name} created.")
        except APIError as e:
            raise Exception(f"Failed to create network {name}: {str(e)}")

    def remove_network(self, name):
        """Remove a Docker network."""
        try:
            network = self.client.networks.get(name)
            network.remove()
            print(f"Network {name} removed.")
        except NotFound:
            raise Exception(f"Network {name} not found.")
        except APIError as e:
            raise Exception(f"Failed to remove network {name}: {str(e)}")

    def inspect_network(self, name):
        """Inspect a Docker network."""
        try:
            network = self.client.networks.get(name)
            return network.attrs
        except NotFound:
            raise Exception(f"Network {name} not found.")
        except APIError as e:
            raise Exception(f"Failed to inspect network {name}: {str(e)}")

    def display_networks(self):
        """Display all Docker networks."""
        try:
            networks = self.list_networks()
            for network in networks:
                print(f"Network Name: {network.name}, ID: {network.id}")
        except Exception as e:
            print(f"Error: {e}")

    def display_network_info(self, name):
        """Display information about a Docker network."""
        try:
            info = self.inspect_network(name)
            print(f"Network {name} Info: {info}")
        except Exception as e:
            print(f"Error: {e}")

class DockerImageManager:
    def __init__(self):
        self.client = docker.from_env()

    def build_image(self, path, tag):
        """Build a Docker image from a Dockerfile."""
        try:
            image, logs = self.client.images.build(path=path, tag=tag)
            print(f"Image {tag} built successfully.")
            for log in logs:
                print(log.get('stream', ''))
        except APIError as e:
            raise Exception(f"Failed to build image: {str(e)}")

    def list_images(self):
        """List all Docker images."""
        try:
            images = self.client.images.list()
            return images
        except APIError as e:
            raise Exception(f"Failed to list images: {str(e)}")

    def display_images(self):
        """Display all Docker images."""
        try:
            images = self.list_images()
            for image in images:
                print(f"Image ID: {image.id}, Tags: {image.tags}")
        except Exception as e:
            print(f"Error: {e}")

