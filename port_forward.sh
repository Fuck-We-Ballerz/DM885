#!/bin/bash

# Function to check if minikube is running
check_minikube() {
    if ! minikube status &> /dev/null; then
        echo "Minikube is not running. Please start minikube first."
        exit 1
    fi
}

# Check if minikube is running
check_minikube

# Function to port forward a service
port_forward() {
    local service_name=$1
    local local_port=$2
    local remote_port=$3
    
    echo "Port forwarding $service_name to local port $local_port..."
    kubectl port-forward service/$service_name $local_port:$remote_port &
}

# Port forward Adminer
port_forward adminer 3300 8080

# Port forward Keycloak
port_forward keycloak 3200 8080

echo "Port forwarding completed. Press Ctrl+C to stop port forwarding."
