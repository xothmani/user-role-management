#!/bin/bash
set -euo pipefail

# =============================================================================
#  User Role Management — GCP Deployment Script
#  Author : Rayen Othmani — ITBS Tunisia 2026
#  Usage  : chmod +x deploy-gcp.sh && ./deploy-gcp.sh
# =============================================================================

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }
step()    { echo -e "\n${BOLD}${CYAN}==> $*${NC}"; }

# ── Configuration — edit these values ────────────────────────────────────────
GCP_REGION="europe-west1"          # Belgium — closest to Tunisia
CLUSTER_NAME="user-role-cluster"
NAMESPACE="user-role-management"
BACKEND_IMAGE="raybob2001/user-role-management-backend:latest"
FRONTEND_IMAGE="raybob2001/user-role-management-frontend:latest"
DB_PASSWORD="ChangeMe2026!"        # Change before running in production
JWT_SECRET="mySecretKey2026TunisiaITBS"

# ── Banner ────────────────────────────────────────────────────────────────────
echo -e "${BOLD}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║     User Role Management — GCP Deployment       ║"
echo "  ║     ITBS Tunisia 2026 — Rayen Othmani           ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 0 — Check prerequisites
# ─────────────────────────────────────────────────────────────────────────────
step "Checking prerequisites"

command -v gcloud  >/dev/null 2>&1 || error "gcloud CLI not found. Install: https://cloud.google.com/sdk/docs/install"
command -v kubectl >/dev/null 2>&1 || error "kubectl not found. Install: https://kubernetes.io/docs/tasks/tools/"

success "gcloud  : $(gcloud version --format='value(Google Cloud SDK)' 2>/dev/null | head -1)"
success "kubectl : $(kubectl version --client --short 2>/dev/null | head -1)"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — GCP Authentication & Project
# ─────────────────────────────────────────────────────────────────────────────
step "GCP Authentication"

# Check if already logged in
if ! gcloud auth print-access-token >/dev/null 2>&1; then
  info "Opening browser for GCP login..."
  gcloud auth login
fi

# List projects and let user pick
echo ""
info "Available GCP projects:"
gcloud projects list --format="table(projectId,name)" 2>/dev/null || true
echo ""

read -rp "$(echo -e ${YELLOW}Enter your GCP Project ID: ${NC})" GCP_PROJECT

gcloud config set project "$GCP_PROJECT" --quiet
success "Project set to: $GCP_PROJECT"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Enable required GCP APIs
# ─────────────────────────────────────────────────────────────────────────────
step "Enabling GCP APIs"

APIS=(
  "container.googleapis.com"
  "compute.googleapis.com"
  "cloudresourcemanager.googleapis.com"
)

for api in "${APIS[@]}"; do
  info "Enabling $api ..."
  gcloud services enable "$api" --project="$GCP_PROJECT" --quiet
  success "$api enabled"
done

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Create GKE Autopilot Cluster
# ─────────────────────────────────────────────────────────────────────────────
step "Creating GKE Autopilot cluster: $CLUSTER_NAME"

if gcloud container clusters describe "$CLUSTER_NAME" \
     --region="$GCP_REGION" \
     --project="$GCP_PROJECT" >/dev/null 2>&1; then
  warn "Cluster '$CLUSTER_NAME' already exists — skipping creation"
else
  info "This takes 3–5 minutes..."
  gcloud container clusters create-auto "$CLUSTER_NAME" \
    --region="$GCP_REGION" \
    --project="$GCP_PROJECT"
  success "Cluster created"
fi

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Configure kubectl
# ─────────────────────────────────────────────────────────────────────────────
step "Configuring kubectl"

gcloud container clusters get-credentials "$CLUSTER_NAME" \
  --region="$GCP_REGION" \
  --project="$GCP_PROJECT"

success "kubectl context set to: $(kubectl config current-context)"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Create Namespace
# ─────────────────────────────────────────────────────────────────────────────
step "Creating namespace: $NAMESPACE"

kubectl apply -f k8s/namespace.yaml
success "Namespace ready"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — Apply ConfigMap
# ─────────────────────────────────────────────────────────────────────────────
step "Applying ConfigMap"

kubectl apply -f k8s/configmap.yaml
success "ConfigMap applied"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — Create Secret with real credentials
# ─────────────────────────────────────────────────────────────────────────────
step "Creating Kubernetes Secret"

DB_PASSWORD_B64=$(echo -n "$DB_PASSWORD" | base64)
JWT_SECRET_B64=$(echo -n "$JWT_SECRET"   | base64)

kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: $NAMESPACE
type: Opaque
data:
  DB_PASSWORD: $DB_PASSWORD_B64
  JWT_SECRET:  $JWT_SECRET_B64
EOF

success "Secret created"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — Deploy PostgreSQL
# ─────────────────────────────────────────────────────────────────────────────
step "Deploying PostgreSQL"

kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml

info "Waiting for PostgreSQL to be ready..."
kubectl rollout status deployment/postgres \
  -n "$NAMESPACE" --timeout=120s
success "PostgreSQL ready"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 — Deploy Backend
# ─────────────────────────────────────────────────────────────────────────────
step "Deploying Backend (Spring Boot)"

kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml

info "Waiting for Backend to be ready (may take ~90s on first pull)..."
kubectl rollout status deployment/backend \
  -n "$NAMESPACE" --timeout=180s
success "Backend ready"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 10 — Deploy Frontend with LoadBalancer (GCP needs LoadBalancer not NodePort)
# ─────────────────────────────────────────────────────────────────────────────
step "Deploying Frontend (Angular / NGINX)"

kubectl apply -f k8s/frontend-deployment.yaml

# Apply frontend service as LoadBalancer (overrides NodePort from k8s/frontend-service.yaml)
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: $NAMESPACE
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
EOF

info "Waiting for Frontend to be ready..."
kubectl rollout status deployment/frontend \
  -n "$NAMESPACE" --timeout=180s
success "Frontend ready"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 11 — Wait for External IP
# ─────────────────────────────────────────────────────────────────────────────
step "Waiting for public IP (LoadBalancer provisioning ~60s)"

EXTERNAL_IP=""
ATTEMPTS=0
MAX_ATTEMPTS=30

while [[ -z "$EXTERNAL_IP" || "$EXTERNAL_IP" == "<pending>" ]]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  if [[ $ATTEMPTS -gt $MAX_ATTEMPTS ]]; then
    warn "IP not ready yet. Run manually: kubectl get svc frontend -n $NAMESPACE"
    break
  fi
  EXTERNAL_IP=$(kubectl get svc frontend \
    -n "$NAMESPACE" \
    -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
  if [[ -z "$EXTERNAL_IP" || "$EXTERNAL_IP" == "<pending>" ]]; then
    info "Still provisioning... ($ATTEMPTS/$MAX_ATTEMPTS)"
    sleep 10
  fi
done

# ─────────────────────────────────────────────────────────────────────────────
# STEP 12 — (Optional) Install ArgoCD
# ─────────────────────────────────────────────────────────────────────────────
step "ArgoCD installation (optional)"

read -rp "$(echo -e ${YELLOW}Install ArgoCD for GitOps? [y/N]: ${NC})" INSTALL_ARGOCD
if [[ "${INSTALL_ARGOCD,,}" == "y" ]]; then
  kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
  kubectl apply -n argocd \
    -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  kubectl apply -f k8s/argocd-app.yaml

  info "Waiting for ArgoCD server..."
  kubectl rollout status deployment/argocd-server \
    -n argocd --timeout=120s

  ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret \
    -o jsonpath="{.data.password}" | base64 -d)

  success "ArgoCD installed"
  info "ArgoCD admin password: ${BOLD}$ARGOCD_PASSWORD${NC}"
  info "Access: kubectl port-forward svc/argocd-server -n argocd 8080:443"
else
  info "ArgoCD skipped"
fi

# ─────────────────────────────────────────────────────────────────────────────
# STEP 13 — Final Summary
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║           Deployment Complete!                  ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BOLD}Cluster:${NC}     $CLUSTER_NAME  ($GCP_REGION)"
echo -e "${BOLD}Namespace:${NC}   $NAMESPACE"
echo -e "${BOLD}Project:${NC}     $GCP_PROJECT"
echo ""

if [[ -n "$EXTERNAL_IP" && "$EXTERNAL_IP" != "<pending>" ]]; then
  echo -e "${BOLD}${GREEN}Frontend URL:${NC}  http://$EXTERNAL_IP"
  echo -e "${BOLD}${GREEN}Backend API:${NC}   http://$EXTERNAL_IP:8080  (internal only)"
else
  echo -e "${YELLOW}Frontend IP pending. Run:${NC}"
  echo "  kubectl get svc frontend -n $NAMESPACE"
fi

echo ""
echo -e "${BOLD}Default login:${NC}"
echo "  Email    : admin@app.com"
echo "  Password : Admin@123"
echo ""
echo -e "${BOLD}Useful commands:${NC}"
echo "  kubectl get pods   -n $NAMESPACE"
echo "  kubectl get svc    -n $NAMESPACE"
echo "  kubectl logs -f deploy/backend  -n $NAMESPACE"
echo "  kubectl logs -f deploy/frontend -n $NAMESPACE"
echo ""
echo -e "${BOLD}To delete the cluster when done:${NC}"
echo "  gcloud container clusters delete $CLUSTER_NAME --region=$GCP_REGION --project=$GCP_PROJECT"
echo ""
