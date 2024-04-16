# Infrastructure configMaps
kubectl delete configmap relation-sql-configmap --ignore-not-found
kubectl create configmap relation-sql-configmap --from-file=infrastructure/relation.sql

kubectl delete configmap keycloak-realm-configmap --ignore-not-found
kubectl create configmap keycloak-realm-configmap --from-file=infrastructure/realm.json

# Monitoring configMaps
kubectl delete configmap grafana-datasources-config --ignore-not-found
kubectl create configmap grafana-datasources-config --from-file=monitoring/grafana-datasources.yml

kubectl delete configmap grafana --ignore-not-found
kubectl create configmap grafana --from-env-file=monitoring/grafana.env

kubectl delete configmap -l app=grafana-dashboard --ignore-not-found

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