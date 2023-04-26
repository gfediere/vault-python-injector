# What is it ?
Vault python injector is a small python code that connect to a Vault server and change the secret for a determined path in a k8s env. Deployed on a Kubernetes environment it relies on the Kubernetes auth method of Vault to authenticate and make write commands for a static secret path.
Goal for this was to generate "traffic" on secrets and see how [Hashicorp Vault Secret Operator](https://developer.hashicorp.com/vault/docs/platform/k8s/vso) react with a significant amount of password changes

# Usage

Project has been containerized and could be deployed directly in a K8s environement:

    kubectl run vault-injector --image=gfediere/vaultsecretinjector --restart=Never --env="vault_server=YOUR_VAULT_CLUSTER" --env="vault_role=VAULT_ROLE" --env="mount_point=KV_MOUNT_POINT" --env="path=SECRET_PATH"  -n vault-injector

Example:

    kubectl run vault-injector --image=gfediere/vaultsecretinjector --restart=Never --env="vault_server=http://vault.vault.svc.cluster.local:8200" --env="vault_role=role_injector" --env="mount_point=kvv2" --env="path=webapp/config"  -n vault-injector