
# Vault Secret (Kubernetes)

This project is created to pull the secret from Vault Secret (beta) by HCP to Kubernetes. 
- https://developer.hashicorp.com/vault/tutorials/hcp-vault-secrets-get-started

To use this script, prepare the env for hcp credentials:
- Refer to this: https://developer.hashicorp.com/hcp/docs/vault-secrets/integrations/docker

1. Create a kustomize.yaml, refer to `kustomize.example.yaml`
```
HCP_CLIENT_ID=
HCP_CLIENT_SECRET=
VLT_ORGANIZATION_ID=
VLT_PROJECT_ID=
VLT_APPLICATION_NAME=
```

2. Create a config.yaml, refer to `config.example.yaml`
```
name: <name of the secret>
namespace: <which namespace is the secret located>
secrets: <List>
  - key: <what is the name of the secret from vault secret>
    value: <what is the name of the secret you want to patch to>
```

3. Create a manifest.yaml, refer to `manifest.example.yaml`

4. Deploy as an init container to patch the relevant secret mention. 