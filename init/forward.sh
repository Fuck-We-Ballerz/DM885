kubectl port-forward service/keycloak 3200:8080 &
kubectl port-forward service/adminer 3300:8080 &
kubectl port-forward service/grafana 3000:3000
