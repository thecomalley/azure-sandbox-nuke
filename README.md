# Azure Sandbox Nuke 💥

Function app to Nuke RGs from one or more Azure subscriptions keeping costs down!

- Scans for RGs that are missing a specific tag `KEY` & deletes them
- Supports multiple subscriptions
- Notifies the user via Pushover

This function app is deployed using the [terraform-azurerm-python-function](https://github.com/thecomalley/terraform-azurerm-python-function) module.

## Deployment instructions

1. `export ARM_SUBSCRIPTION_ID=<your-subscription-id>`
2. `terraform init`
3. `terraform apply`