# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher

# Configure the Microsoft Azure Cloud provider pinning major versions
terraform {
  required_version = "~> 1.12"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.33"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
