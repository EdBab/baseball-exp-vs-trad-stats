terraform {
  backend "azurerm" {
    resource_group_name  = "my-aks-rg"
    storage_account_name = "myterraformstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}


provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}