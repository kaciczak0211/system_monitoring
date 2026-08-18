import psutil
from prometheus_client import start_http_server, Gauge
import time

cpu = Gauge("system_cpu_percent", "CPU usage percentage")
memory = Gauge("system_memory_percent", "Memory usage percentage")
memory_used = Gauge("system_memory_used_bytes", "Used memory in bytes")
memory_total = Gauge("system_memory_total_bytes", "Total memory in bytes")
disk = Gauge("system_disk_percent", "Disk usage percentage")
disk_used = Gauge("system_disk_used_bytes", "Used disk space in bytes")
disk_total = Gauge("system_disk_total_bytes", "Total disk space in bytes")


def collect_metrics():
    # CPU
    cpu.set(psutil.cpu_percent(interval=1))

    # Memory
    mem = psutil.virtual_memory()
    memory.set(mem.percent)
    memory_used.set(mem.used)
    memory_total.set(mem.total)

    # Disk
    d = psutil.disk_usage("/")
    disk.set(d.percent)
    disk_used.set(d.used)
    disk_total.set(d.total)


if __name__ == "__main__":
    # Prometheus will scrape http://localhost:8000/metrics
    start_http_server(8000)

    while True:
        collect_metrics()
        time.sleep(5)