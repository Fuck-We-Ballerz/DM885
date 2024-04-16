#!/bin/bash
is_minikube_running() {
    minikube status >/dev/null 2>&1
}

# Function to start Minikube if it's not already running
start_minikube() {
    if ! is_minikube_running; then
        echo "Starting Minikube..."
        minikube start
    else
        echo "Minikube is already running."
    fi
}

start_minikube

# To access the minikube docker daemon
eval $(minikube -p minikube docker-env)

docker build -t grafana -f monitoring/docker/Dockerfile.grafana .
docker build -t prometheus -f monitoring/docker/Dockerfile.prometheus .
docker build -t promtail -f monitoring/docker/Dockerfile.promtail .