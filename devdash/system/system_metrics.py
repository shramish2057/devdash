import psutil
import platform
from datetime import datetime
import time
import csv

class SystemMetrics:
    @staticmethod
    def get_cpu_usage():
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    @staticmethod
    def get_memory_usage():
        """Get current memory usage statistics."""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent
        }

    @staticmethod
    def get_disk_usage():
        """Get current disk usage statistics."""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }

    @staticmethod
    def get_network_stats():
        """Get current network statistics."""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }

    @staticmethod
    def get_system_info():
        """Get basic system information."""
        uname = platform.uname()
        return {
            'system': uname.system,
            'node_name': uname.node,
            'release': uname.release,
            'version': uname.version,
            'machine': uname.machine,
            'processor': uname.processor
        }

    @staticmethod
    def get_boot_time():
        """Get the system boot time."""
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        return bt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def display_system_metrics():
        """Display all system metrics."""
        print("=== System Metrics ===")
        print(f"System Info: {SystemMetrics.get_system_info()}")
        print(f"Boot Time: {SystemMetrics.get_boot_time()}")
        print(f"CPU Usage: {SystemMetrics.get_cpu_usage()}%")
        mem = SystemMetrics.get_memory_usage()
        print(f"Memory Usage: {mem['percent']}% (Used: {mem['used'] / (1024**3):.2f} GB / Total: {mem['total'] / (1024**3):.2f} GB)")
        disk = SystemMetrics.get_disk_usage()
        print(f"Disk Usage: {disk['percent']}% (Used: {disk['used'] / (1024**3):.2f} GB / Total: {disk['total'] / (1024**3):.2f} GB)")
        net = SystemMetrics.get_network_stats()
        print(f"Network Stats: Sent {net['bytes_sent'] / (1024**2):.2f} MB, Received {net['bytes_recv'] / (1024**2):.2f} MB")

    @staticmethod
    def live_system_metrics(refresh_interval=1):
        """Continuously refresh and display system metrics."""
        try:
            while True:
                SystemMetrics.clear_screen()
                print("=== Live System Metrics ===")
                print(f"CPU Usage: {SystemMetrics.get_cpu_usage()}%")
                memory = SystemMetrics.get_memory_usage()
                print(f"Memory Usage: {memory['percent']}% (Used: {memory['used'] / (1024**3):.2f} GB / Total: {memory['total'] / (1024**3):.2f} GB)")
                disk = SystemMetrics.get_disk_usage()
                print(f"Disk Usage: {disk['percent']}% (Used: {disk['used'] / (1024**3):.2f} GB / Total: {disk['total'] / (1024**3):.2f} GB)")
                net = SystemMetrics.get_network_stats()
                print(f"Network: Sent {net['bytes_sent'] / (1024**2):.2f} MB, Received {net['bytes_recv'] / (1024**2):.2f} MB")
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\nLive metrics monitoring stopped.")


    @staticmethod
    def alert_on_thresholds(cpu_threshold=90, memory_threshold=90):
        """Alert if CPU or memory usage exceeds a specified threshold."""
        cpu_usage = SystemMetrics.get_cpu_usage()
        memory = SystemMetrics.get_memory_usage()
        alerts = []

        if cpu_usage > cpu_threshold:
            alerts.append(f"High CPU Usage Alert: {cpu_usage}% (Threshold: {cpu_threshold}%)")

        if memory['percent'] > memory_threshold:
            alerts.append(f"High Memory Usage Alert: {memory['percent']}% (Threshold: {memory_threshold}%)")

        if alerts:
            for alert in alerts:
                print(f"ALERT: {alert}")
        else:
            print(f"CPU Usage: {cpu_usage}% (Threshold: {cpu_threshold}%)")
            print(f"Memory Usage: {memory['percent']}% (Threshold: {memory_threshold}%)")


    @staticmethod
    def record_metrics_to_csv(filename="system_metrics_history.csv"):
        """Record system metrics to a CSV file for historical data analysis."""
        try:
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['timestamp', 'cpu_usage', 'memory_usage', 'disk_usage', 'network_sent', 'network_recv']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()  # Write headers if the file is empty

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cpu_usage = SystemMetrics.get_cpu_usage()
                memory = SystemMetrics.get_memory_usage()
                disk = SystemMetrics.get_disk_usage()
                net = SystemMetrics.get_network_stats()

                writer.writerow({
                    'timestamp': timestamp,
                    'cpu_usage': cpu_usage,
                    'memory_usage': memory['percent'],
                    'disk_usage': disk['percent'],
                    'network_sent': net['bytes_sent'],
                    'network_recv': net['bytes_recv']
                })

                print(f"Metrics recorded at {timestamp}")
        except Exception as e:
            print(f"Failed to record metrics: {str(e)}")


            

