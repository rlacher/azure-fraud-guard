# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher
# Provision of cloud resources, VM setup and Docker install

resource "azurerm_resource_group" "rg" {
  name     = "fraud-guard-rg"
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_virtual_network" "vnet" {
  name                = "fraud-guard-vnet"
  address_space       = ["192.168.0.0/24"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.common_tags
}

resource "azurerm_subnet" "subnet" {
  name                 = "fraud-guard-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["192.168.0.128/25"]
}

# Public IP omitted intentionally for security; internal-only access; health monitored through logs.
resource "azurerm_network_interface" "nic" {
  name                = "fraud-guard-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    private_ip_address_version    = "IPv4"
  }

  tags = local.common_tags
}
