resource "azurerm_resource_group" "main" {
  name     = "oma-azCleaner-rg"
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
  name                = "oma-azCleaner-asp"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "main" {
  name                = "oma-azCleaner-func"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  storage_account_name = azurerm_storage_account.main.name
  service_plan_id      = azurerm_service_plan.main.id

  identity {
    type = "SystemAssigned"
  }

  sticky_settings {

  }

  site_config {
    application_stack {
        python_version = 3.8
    }
  }
}
