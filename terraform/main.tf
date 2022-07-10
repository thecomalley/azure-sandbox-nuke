data "azurerm_client_config" "current" {
}

resource "azurerm_resource_group" "main" {
  name     = "oma-azcleaner-rg"
  location = "Australia East"
}

resource "azurerm_storage_account" "main" {
  name                     = "omaazcleanerst"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "main" {
  name                = "oma-azcleaner-asp"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = "oma-azcleaner-log"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}


resource "azurerm_application_insights" "main" {
  name                = "oma-azcleaner-appi"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "other"
}

resource "azurerm_key_vault" "main" {
  name                       = "oma-azcleaner-kv"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  sku_name                   = "standard"
  enable_rbac_authorization  = true
}

resource "azurerm_role_assignment" "admin" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_linux_function_app" "main" {
  name                = "oma-azcleaner-func"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  service_plan_id               = azurerm_service_plan.main.id

  storage_account_name          = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key

  functions_extension_version = "~4"

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    ENABLE_ORYX_BUILD              = true # Required to enable remote build on Linux
    SCM_DO_BUILD_DURING_DEPLOYMENT = true # Required to enable remote build on Linux
    AZURE_SUBSCRIPTION_ID          = data.azurerm_client_config.current.subscription_id
    MODE                           = "desctructive"
    DISCORD_WEBHOOK_URL            = "@Microsoft.KeyVault(VaultName=${azurerm_key_vault.main.name};SecretName=discord-webhook-url)"
  }

  site_config {
    application_insights_connection_string = azurerm_application_insights.main.connection_string
    application_stack {
      python_version = 3.8
    }
  }
}

resource "azurerm_role_assignment" "main" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_function_app.main.identity[0].principal_id
}

resource "azurerm_role_assignment" "contributor" {
  scope                = "/subscriptions/${data.azurerm_client_config.current.subscription_id}"
  role_definition_name = "Contributor"
  principal_id         = azurerm_linux_function_app.main.identity[0].principal_id
}