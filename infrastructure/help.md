### Setup development environment with minikube:


1. Install minikube: https://minikube.sigs.k8s.io/docs/start/
2. Start minikube:
```
Minikube start
```
#### Deploy infrastructur:
Run the following command in `/infrastructur`:
```
kubectl apply -f . 
```

#### Deploy Monitoring:
Run the following command in `/monitoring`:
```
kubectl apply -f . 
```