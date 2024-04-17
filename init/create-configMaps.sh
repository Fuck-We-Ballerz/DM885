#!/bin/bash

kubectl delete configmap --all

# Infrastructure configMaps
kubectl create configmap relation-sql-configmap --from-file=infrastructure/relation.sql
kubectl create configmap keycloak-realm-configmap --from-file=infrastructure/realm.json

# Monitoring configMaps
kubectl create configmap grafana-datasources-config --from-file=monitoring/grafana-datasources.yml
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