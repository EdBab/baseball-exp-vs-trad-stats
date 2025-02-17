terraform {
  backend "azurerm" {
    resource_group_name  = "my-aks-rg"
    storage_account_name = "myterraformstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}