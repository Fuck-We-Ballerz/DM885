kubectl create configmap relation-sql-configmap --from-file=infrastructure/relation.sql

kubectl create configmap keycloak-realm-configmap --from-file=infrastructure/realm.json