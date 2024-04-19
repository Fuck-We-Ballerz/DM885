#!/bin/bash

kubectl delete configmap --all

# Infrastructure configMaps
kubectl create configmap relation-sql --from-file=infrastructure/relation.sql
kubectl create configmap keycloak-realm --from-file=infrastructure/realm.json
kubectl create configmap postgres-application --from-env-file=infrastructure/postgres-application.env
kubectl create configmap postgres-keycloak --from-env-file=infrastructure/postgres-keycloak.env
kubectl create configmap keycloak --from-env-file=infrastructure/keycloak.env

# Monitoring configMaps
kubectl create configmap grafana-datasources-config --from-file=monitoring/grafana-datasources.yaml
kubectl create configmap grafana --from-env-file=monitoring/grafana.env

DASHBOARDS_DIR="monitoring/dashboards"

# Loop through each file in the dashboards directory
for file in "$DASHBOARDS_DIR"/*
do
  # Get the filename without extension
  filename=$(basename -- "$file")
  name="${filename%.*}"

  # Create a ConfigMap for each dashboard file
  kubectl delete configmap "grafana-dashboard-$name" --ignore-not-found
  kubectl create configmap "grafana-dashboard-$name" --from-file="$file"
done

kubectl create configmap prometheus --from-file=monitoring/prometheus.yaml
kubectl create configmap promtail --from-file=monitoring/promtail.yaml