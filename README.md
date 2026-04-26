# User Role Management

[![CI Pipeline](https://github.com/xothmani/user-role-management/actions/workflows/ci.yml/badge.svg)](https://github.com/xothmani/user-role-management/actions/workflows/ci.yml)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-raybob2001-blue?logo=docker)](https://hub.docker.com/u/raybob2001)
[![Java](https://img.shields.io/badge/Java-21-orange?logo=openjdk)](https://openjdk.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.0-green?logo=springboot)](https://spring.io/projects/spring-boot)
[![Angular](https://img.shields.io/badge/Angular-17-red?logo=angular)](https://angular.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

A full-stack **User Role Management** system with JWT-based authentication, role-based access control, and a complete end-to-end DevOps pipeline — from source code to production on Kubernetes.

---

## Architecture

### Application Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                           │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP / REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FRONTEND  (Angular 17)                         │
│         SPA served via NGINX · NodePort 30080                   │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API  :8080
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND  (Spring Boot 3.2 / Java 21)             │
│   JWT Auth · RBAC · Spring Security · Actuator · Prometheus     │
└───────────────┬─────────────────────────┬───────────────────────┘
                │ JDBC (port 5432)         │ /actuator/prometheus
                ▼                         ▼
┌───────────────────────┐    ┌────────────────────────────────────┐
│  PostgreSQL 16-alpine │    │   Prometheus  →  Grafana           │
│  PVC  1 Gi            │    │   Metrics scraping & dashboards     │
└───────────────────────┘    └────────────────────────────────────┘
```

### CI/CD & GitOps Pipeline

```
┌──────────┐   push / PR    ┌──────────────────────────────────────┐
│  GitHub  │ ─────────────► │        GitHub Actions CI              │
│  (main,  │                │  ┌────────────┐  ┌────────────────┐  │
│   dev)   │                │  │ backend-ci │  │  frontend-ci   │  │
└──────────┘                │  │ Checkstyle │  │  ESLint        │  │
                            │  │ JUnit      │  │  Karma/Jasmine │  │
                            │  │ SonarQube  │  │  Trivy scan    │  │
                            │  │ Trivy scan │  │  Docker build  │  │
                            │  │ Docker push│  │  Docker push   │  │
                            │  └────────────┘  └────────────────┘  │
                            └──────────────────────┬───────────────┘
                                                   │  image:<sha> + latest
                                                   ▼
                                        ┌──────────────────┐
                                        │    Docker Hub    │
                                        │  raybob2001/...  │
                                        └────────┬─────────┘
                                                 │  GitOps sync
                                                 ▼
                                        ┌──────────────────┐
                                        │     ArgoCD       │
                                        │  auto-sync  k8s/ │
                                        │  self-heal       │
                                        │  prune           │
                                        └────────┬─────────┘
                                                 │
                                                 ▼
                                        ┌──────────────────┐
                                        │   Kubernetes     │
                                        │  (Minikube/prod) │
                                        │  NS: user-role-  │
                                        │      management  │
                                        └──────────────────┘
```

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Frontend | Angular | 17.3.0 |
| Frontend runtime | NGINX | alpine |
| Backend framework | Spring Boot | 3.2.0 |
| Backend language | Java | 21 |
| Authentication | JWT (jjwt) | 0.12.3 |
| Database | PostgreSQL | 16-alpine |
| ORM | Spring Data JPA / Hibernate | — |
| Metrics | Micrometer + Prometheus | — |
| Containerization | Docker / Docker Compose | — |
| Orchestration | Kubernetes | — |
| Local cluster | Minikube | — |
| GitOps | ArgoCD | — |
| Monitoring | Prometheus + Grafana | — |
| CI/CD | GitHub Actions | — |
| Code quality | SonarQube (SonarCloud) | — |
| Security scan | Trivy | — |
| Style checks | Checkstyle (Google) | 3.3.1 |

---

## Prerequisites

Make sure the following tools are installed before proceeding:

| Tool | Minimum version | Install guide |
|---|---|---|
| Docker & Docker Compose | 24+ | https://docs.docker.com/get-docker/ |
| Minikube | 1.32+ | https://minikube.sigs.k8s.io/docs/start/ |
| kubectl | 1.28+ | https://kubernetes.io/docs/tasks/tools/ |
| Java (JDK) | 21 | https://adoptium.net/ |
| Node.js | 20 LTS | https://nodejs.org/ |

---

## Quick Start (Docker Compose)

The fastest way to run the full stack locally.

**1. Clone the repository**

```bash
git clone https://github.com/xothmani/user-role-management.git
cd user-role-management
```

**2. Configure environment variables**

```bash
cp .env.example .env
# Edit .env and fill in DB_PASSWORD and JWT_SECRET
```

**3. Start all services**

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3001 |
| Backend API | http://localhost:8080 |
| Actuator health | http://localhost:8080/actuator/health |
| Prometheus metrics | http://localhost:8080/actuator/prometheus |

**4. Stop the stack**

```bash
docker compose down -v
```

---

## Kubernetes Deployment

### 1. Start Minikube

```bash
minikube start --cpus=4 --memory=4096
```

### 2. Enable the ingress add-on (optional)

```bash
minikube addons enable ingress
```

### 3. Apply all manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

### 4. Verify pods are running

```bash
kubectl get pods -n user-role-management
```

### 5. Access the frontend

```bash
minikube service frontend-service -n user-role-management
# or directly via NodePort:
# http://$(minikube ip):30080
```

### 6. Deploy ArgoCD application (GitOps)

```bash
# Install ArgoCD into the cluster (first time only)
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Apply the application manifest
kubectl apply -f k8s/argocd-app.yaml
```

ArgoCD will watch the `k8s/` directory on the `main` branch and automatically sync any changes with **self-heal** and **prune** enabled.

---

## Monitoring

The backend exposes Prometheus-compatible metrics at `/actuator/prometheus`.

### Prometheus

Configure Prometheus to scrape the backend by adding a scrape job:

```yaml
scrape_configs:
  - job_name: user-role-management
    metrics_path: /actuator/prometheus
    static_configs:
      - targets:
          - backend-service.user-role-management.svc.cluster.local:8080
```

### Grafana

1. Add the Prometheus instance as a data source in Grafana.
2. Import the **Spring Boot Statistics** dashboard (ID `6756`) from Grafana Labs, or build a custom dashboard using the `user-role-management` application tag added by Micrometer.

Key metrics available:

| Metric | Description |
|---|---|
| `http_server_requests_seconds` | HTTP request latency and throughput |
| `jvm_memory_used_bytes` | JVM heap and non-heap usage |
| `hikaricp_connections_active` | Active DB connection pool connections |
| `process_cpu_usage` | Process CPU utilisation |

---

## CI/CD Pipeline

The pipeline is defined in `.github/workflows/ci.yml` and triggers on every push or pull request to `main` and `dev`.

```
push / PR
    │
    ├── backend-ci
    │     ├── Checkstyle (Google Java Style)
    │     ├── JUnit tests  (mvnw test)
    │     ├── Package JAR  (mvnw package -DskipTests)
    │     ├── SonarQube analysis  (SonarCloud)
    │     ├── Docker build  (tagged with git SHA)
    │     ├── Trivy scan    (CRITICAL severity)
    │     └── Docker push   (SHA tag + latest) → Docker Hub
    │
    └── frontend-ci  (needs: backend-ci)
          ├── ESLint
          ├── Karma / Jasmine unit tests (ChromeHeadless)
          ├── Docker build  (tagged with git SHA)
          ├── Trivy scan    (CRITICAL severity)
          └── Docker push   (SHA tag + latest) → Docker Hub
```

Images are published to Docker Hub under `raybob2001/user-role-management-backend` and `raybob2001/user-role-management-frontend`. ArgoCD detects the updated `latest` tag and reconciles the cluster automatically.

---

## Project Structure

```
user-role-management/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions pipeline
├── backend/
│   ├── src/main/java/com/app/
│   │   ├── config/             # Security & app configuration
│   │   ├── controller/         # REST controllers
│   │   ├── dto/                # Request / response DTOs
│   │   ├── entity/             # JPA entities
│   │   ├── repository/         # Spring Data repositories
│   │   ├── security/           # JWT filter & utilities
│   │   └── service/            # Business logic
│   ├── Dockerfile
│   └── pom.xml
├── frontend/
│   ├── src/app/
│   │   ├── core/               # Guards & interceptors
│   │   ├── modules/            # Feature modules
│   │   ├── services/           # HTTP services
│   │   └── shared/             # Shared components
│   ├── nginx.conf
│   └── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── postgres-{deployment,service}.yaml
│   ├── backend-{deployment,service}.yaml
│   ├── frontend-{deployment,service}.yaml
│   └── argocd-app.yaml
├── docker-compose.yml
└── README.md
```

---

## Author

**Rayen Othmani**
ITBS Tunisia — Class of 2026

---

*Built with Spring Boot, Angular, and a fully automated DevOps pipeline.*