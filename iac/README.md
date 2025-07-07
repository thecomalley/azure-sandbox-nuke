# iac

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.0 |
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | ~> 4.23 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.25.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_terraform_azurerm_python_function"></a> [terraform\_azurerm\_python\_function](#module\_terraform\_azurerm\_python\_function) | thecomalley/python-function/azurerm | 1.2.0 |

## Resources

| Name | Type |
|------|------|
| [azurerm_role_assignment.contributor](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_subscription_ids_to_clean"></a> [subscription\_ids\_to\_clean](#input\_subscription\_ids\_to\_clean) | List of subscription IDs to clean | `list(string)` | `[]` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
