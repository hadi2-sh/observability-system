# Observability System



A containerized observability platform for monitoring a FastAPI application using metrics, logs, and distributed tracing.



## Overview



This project demonstrates how to build an end-to-end observability system using open-source tools.



It collects application metrics, aggregates container logs, captures distributed traces, and visualizes operational data through Grafana dashboards.



## Architecture



```mermaid

flowchart TB

&#x20;   A\[Client / Browser] --> B\[FastAPI Application]

&#x20;   B -->|Metrics| C\[Prometheus]

&#x20;   B -->|OTLP Traces| D\[Tempo]

&#x20;   B -->|Container Logs| E\[Alloy]

&#x20;   E -->|Log Forwarding| F\[Loki]

&#x20;   C --> G\[Grafana]

&#x20;   D --> G

&#x20;   F --> G

```



## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Application development |

| FastAPI | REST API framework |

| Uvicorn | ASGI application server |

| Docker | Containerization |

| Docker Compose | Multi-container orchestration |

| Prometheus | Metrics collection |

| Grafana | Monitoring dashboards |

| Loki | Log aggregation |

| Grafana Alloy | Log collection and forwarding |

| Tempo | Distributed tracing |

| OpenTelemetry | Instrumentation and trace export |



## Project Structure



```text

observability-system/

├── alloy/

│   └── config.alloy

├── loki/

│   └── loki-config.yaml

├── prometheus/

│   └── prometheus.yml

├── tempo/

│   └── tempo.yaml

├── app.py

├── Dockerfile

├── compose.yaml

├── requirements.txt

├── .dockerignore

└── .gitignore

```



## Services and Ports



| Service | Port | Purpose |

|---|---:|---|

| FastAPI | 8000 | Application API |

| Prometheus | 9090 | Metrics collection |

| Grafana | 3000 | Dashboards |

| Loki | 3100 | Log aggregation |

| Alloy | 12345 | Alloy interface |

| Tempo | 3200 | Trace querying |

| Tempo OTLP gRPC | 4317 | Trace ingestion |

| Tempo OTLP HTTP | 4318 | Trace ingestion |



## Getting Started



### Prerequisites



\- Docker Desktop

\- Git

\- Docker Compose



### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd observability-system

```



### 2. Start the system



```bash

docker compose up -d --build

```



This builds the FastAPI image and starts all six services.



### 3. Verify containers



```bash

docker compose ps

```



All six services should show a running status.



### 4. Access the interfaces



\- FastAPI: http://localhost:8000

\- Health check: http://localhost:8000/health

\- Prometheus metrics: http://localhost:8000/metrics

\- Prometheus UI: http://localhost:9090

\- Grafana: http://localhost:3000

\- Loki: http://localhost:3100

\- Alloy: http://localhost:12345

\- Tempo: http://localhost:3200



## Observability Features



### Metrics — Prometheus



The FastAPI application exposes Prometheus metrics through `/metrics`.



Implemented metrics include:



\- `http\_requests\_total` — total HTTP requests.

\- `http\_request\_duration\_seconds` — HTTP request duration histogram.



Prometheus scrapes the application every 15 seconds.



### Logs — Loki and Alloy



Grafana Alloy discovers Docker containers, collects their logs, and forwards them to Loki.



Logs can be explored in Grafana using LogQL.



Example query:



```logql

{container=\~".+"}

```



### Distributed Tracing — OpenTelemetry and Tempo



The FastAPI application is instrumented using OpenTelemetry.



Traces are exported to Tempo through OTLP.



Example TraceQL query:



```traceql

{ resource.service.name = "observability-app" }

```



### Log-to-Trace Correlation



Grafana Loki is configured with a derived field that extracts trace IDs from structured application logs.



This allows users to navigate from a log entry directly to its corresponding trace in Tempo.



## Grafana Dashboard



The project includes a dashboard with five monitoring panels:



1\. HTTP Request Rate

2\. Total HTTP Requests

3\. Average HTTP Response Time

4\. 95th Percentile Response Time (P95)

5\. Application Availability



These visualizations help monitor application traffic, latency, and availability.



## Reliability Testing



The system was tested with the following scenarios:



\- Normal HTTP requests.

\- Application error generation.

\- Error log collection through Loki.

\- Trace collection through Tempo.

\- Application container shutdown.

\- Prometheus outage detection.

\- Application restart and recovery.

\- Verification that all six containers are running.



## Persistent Storage



Docker named volumes are configured for:



\- Prometheus

\- Grafana

\- Loki

\- Alloy

\- Tempo



These volumes preserve service data across container restarts and recreation.



\*\*Important:\*\* Avoid running `docker compose down -v` unless you intentionally want to delete the persistent volumes and their data.



## Useful Docker Commands



Check running services:



```bash

docker compose ps

```



View all service logs:



```bash

docker compose logs

```



View application logs:



```bash

docker compose logs app

```



Restart all services:



```bash

docker compose restart

```



Stop all services:



```bash

docker compose down

```



Start all services again:



```bash

docker compose up -d

```



## Learning Outcomes



Through this project, I gained practical experience with:



- Building and containerizing a Python application.

- Managing multi-container applications with Docker Compose.

- Instrumenting applications with Prometheus metrics.

- Implementing structured application logging.

- Collecting and querying logs using Loki.

- Configuring Grafana Alloy for Docker log collection.

- Implementing distributed tracing using OpenTelemetry.

- Storing and querying traces using Tempo.

- Building monitoring dashboards in Grafana.

- Testing application availability and recovery.

- Configuring persistent Docker volumes.



## Future Improvements



\- Add HTTP error counters and error-rate monitoring.

\- Add alerting using Prometheus Alertmanager.

\- Improve dashboard visualizations and alert thresholds.

\- Pin dependency and container image versions.

\- Add automated tests and CI/CD integration.

\- Deploy the system to a cloud environment.



\---



\*\*Project:\*\* Observability System  

\*\*Status:\*\* Local implementation and reliability testing completed; documentation and publishing in progress.

