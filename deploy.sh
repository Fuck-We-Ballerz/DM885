#!/bin/bash

# Function to apply a Kubernetes manifest file
apply_manifest() {
    local manifest_file=$1
    if ! kubectl apply -f "$manifest_file"; then
        echo "Error applying $manifest_file"
        exit 1
    fi
}

# Function to check if minikube is running
check_minikube() {
    if ! minikube status &> /dev/null; then
        echo "Minikube is not running. Please start minikube first."
        exit 1
    fi
}

# Check if minikube is running
check_minikube

# Apply Kubernetes manifests
for file in infrastructure/*.yaml; do
    apply_manifest "$file"
done

echo "Deployment completed successfully."
