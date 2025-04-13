data "azurerm_client_config" "current" {}

locals {
  subscription_ids_to_clean        = coalescelist(var.subscription_ids_to_clean, [data.azurerm_client_config.current.tenant_id])
  subscription_ids_to_clean_string = join(",", local.subscription_ids_to_clean)
}

module "terraform_azurerm_python_function" {
  # source = "../../terraform-azurerm-python-function"
  source  = "thecomalley/python-function/azurerm"
  version = "1.2.0"

  location = "Australia East"

  # { organization }-{ workload }-{ environment }-{ region }-{ component }-{ ResourceType }
  resource_group_name       = "oma-nuke-prd-aue-rg"
  function_app_name         = "oma-nuke-prd-aue-func"
  storage_account_name      = "omanukeprdauestorage"
  log_analytics_name        = "oma-nuke-prd-aue-law"
  app_service_plan_name     = "oma-nuke-prd-aue-asp"
  application_insights_name = "oma-nuke-prd-aue-ai"
  key_vault_name            = "oma-nuke-prd-aue-kv"

  python_version = "3.11"

  # must be a relative path to ${path.module}
  python_source_code_path = "../src"

  environment_variables = {
    TAG_KEY                   = "WorkloadName"
    SUBSCRIPTION_IDS_TO_CLEAN = local.subscription_ids_to_clean_string
  }

  secret_environment_variables = [
    "PUSHOVER_API_TOKEN",
    "PUSHOVER_USER_KEY"
  ]

  tags = {
    WorkloadName = "Azure Sandbox Nuke"
    Environment  = "Production"
  }
}

resource "azurerm_role_assignment" "example" {
  for_each             = toset(local.subscription_ids_to_clean)
  scope                = "/subscriptions/${each.value}"
  role_definition_name = "Contributor"
  principal_id         = module.terraform_azurerm_python_function.principal_id
}
