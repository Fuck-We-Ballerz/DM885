#!/bin/bash
echo "Creating secrets..."
kubectl delete secret postgres-application --ignore-not-found
kubectl create secret generic postgres-application --from-env-file=secrets/postgres-application-dev.env

kubectl delete secret keycloak --ignore-not-found
kubectl create secret generic keycloak --from-env-file=secrets/keycloak-dev.env

kubectl delete secret postgres-keycloak --ignore-not-found
kubectl create secret generic postgres-keycloak --from-env-file=secrets/postgres-keycloak-dev.env