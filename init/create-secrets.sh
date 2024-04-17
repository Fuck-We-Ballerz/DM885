#!/bin/bash

kubectl delete secrets --all

# Create secrets
echo "Creating secrets..."
kubectl create secret generic postgres-application --from-env-file=secrets/postgres-application-dev.env
kubectl create secret generic keycloak --from-env-file=secrets/keycloak-dev.env
kubectl create secret generic postgres-keycloak --from-env-file=secrets/postgres-keycloak-dev.env

# Monitoring secrets
kubectl create secret generic grafana --from-env-file=secrets/grafana-dev.env
kubectl create secret generic postgres-exporter --from-env-file=secrets/postgres-exporter-dev.env
