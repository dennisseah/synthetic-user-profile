locals {
  resource_location = "West US 2"
  openai_location   = "eastus"
}

variable "resource_prefix" {
  description = "Prefix for all resources"
  type        = string
}

variable "azure_subscription_id" {
  description = "Azure subscription id"
  type        = string
}


data "azurerm_subscription" "primary" {}
data "azurerm_client_config" "current" {}


resource "azurerm_resource_group" "synthnetic_user_profile" {
  name     = "${var.resource_prefix}_synthnetic_user_profile_rg"
  location = local.resource_location
}

resource "azurerm_cognitive_account" "openai" {
  name                  = "${var.resource_prefix}-synthnetic-user-profile-openai"
  kind                  = "OpenAI"
  location              = local.openai_location
  resource_group_name   = azurerm_resource_group.synthnetic_user_profile.name
  custom_subdomain_name = "${var.resource_prefix}-synthnetic-user-profile"
  sku_name              = "S0"
}


resource "azurerm_cognitive_deployment" "openai_model" {
  name                 = "gpt-4o"
  cognitive_account_id = azurerm_cognitive_account.openai.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o"
    version = "2024-05-13"
  }
  sku {
    name     = "Standard"
    capacity = 150 # 150k TPM
  }
}
