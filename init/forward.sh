kubectl port-forward service/keycloak 3200:8080 &
kubectl port-forward service/adminer 3300:8080 &
kubectl port-forward service/grafana 3000:3000 &
kubectl port-forward service/prometheus 9090:9090 &
kubectl port-forward service/postgres-exporter 9187:9187 &
kubectl port-forward service/promtail 9080:9080
