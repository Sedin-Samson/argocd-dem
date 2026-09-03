# 🚀 Argo CD GitOps Complete Hands-On Learning Guide

Welcome to the **Practical Argo CD GitOps Tutorial**! This repository provides a complete, beginner-friendly setup for deploying a 2-tier application (Frontend + Backend) locally using **Docker**, **Kubernetes (Minikube)**, and **Argo CD**.

---

## 📁 Repository Structure

```text
argocd/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
└── kubernetes/
    ├── namespace.yaml
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── argocd-frontend-app.yaml
    ├── argocd-backend-app.yaml
    ├── backend/
    │   ├── backend-deployment.yaml
    │   └── backend-service.yaml
    └── frontend/
        ├── frontend-deployment.yaml
        └── frontend-service.yaml
```

---

## 🛠️ Quick Commands Cheat Sheet

### 1. Build and Load Images (Minikube)
```bash
# Build Backend image
docker build -t backend:v1 ./backend

# Build Frontend image
docker build -t frontend:v1 ./frontend

# Load images into Minikube container engine
minikube image load backend:v1
minikube image load frontend:v1
```

### 2. Manual kubectl Deployment (Without Argo CD)
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml

# Check running resources
kubectl get all -n dev
```

### 3. Install Argo CD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Retrieve Initial Admin Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# Port Forward Argo CD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Access UI at `https://localhost:8080` (Username: `admin`).

---

## 🌐 Architectural Comparison: Local vs AWS EKS

### Local Cluster (Minikube)
```text
Developer → Git Repo → Argo CD (in Cluster) → Local K8s Node → Frontend Service (NodePort) → Backend Service (ClusterIP)
```

### AWS EKS (Production)
```text
Developer → GitHub/GitLab → Argo CD (in EKS) → EKS Nodes → AWS ALB (Ingress) → Frontend → Backend → ECR Registry
```
