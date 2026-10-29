# System Monitoring

A small observability stack that runs locally with one command: a Python exporter collects host metrics, Prometheus scrapes them, and Grafana displays them on a dashboard that is provisioned from code, with no manual setup in the UI.

## Architecture

    monitor.py (exporter, :8000/metrics)  -->  Prometheus (:9090)  -->  Grafana (:3000)

| Service    | Image / build              | Port |
|------------|----------------------------|------|
| monitor    | built from `Dockerfile`    | 8000 |
| prometheus | `prom/prometheus:v2.51.0`  | 9090 |
| grafana    | `grafana/grafana:10.4.0`   | 3000 |

## Metrics

The exporter uses `psutil` and `prometheus_client` and refreshes every 5 seconds:

- `system_cpu_percent`
- `system_memory_percent`, `system_memory_used_bytes`, `system_memory_total_bytes`
- `system_disk_percent`, `system_disk_used_bytes`, `system_disk_total_bytes`

## Run it

```bash
git clone https://github.com/kaciczak0211/system_monitoring.git
cd system_monitoring
docker compose up -d --build
```

- Raw metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090 (Status > Targets should show `monitor` as UP)
- Grafana: http://localhost:3000 (local default login `admin` / `admin`)

The Prometheus datasource and the dashboard are loaded automatically from `grafana/provisioning/`.

Stop with `docker compose down` (add `-v` to remove stored data).

## What I practised

- Writing a custom Prometheus exporter in Python
- Configuring Prometheus scrape targets
- Provisioning Grafana datasources and dashboards as code
- Running a multi-container stack with Docker Compose (shared network, named volumes, restart policies)

## Next steps

- Add alerting rules (e.g. high disk usage)
- Add a GitHub Actions workflow that lints the code and builds the image
- Deploy the stack to a fresh Linux VM with an Ansible playbook
