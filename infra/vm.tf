# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher

resource "azurerm_linux_virtual_machine" "vm" {
  name                            = "fraud-guard-vm"
  location                        = azurerm_resource_group.rg.location
  resource_group_name             = azurerm_resource_group.rg.name
  network_interface_ids           = [azurerm_network_interface.nic.id]
  size                            = "Standard_B1ms"
  admin_username                  = var.admin_username
  admin_password                  = var.admin_password
  disable_password_authentication = false
  computer_name                   = "fraudguard"
  depends_on                      = [azurerm_network_interface.nic]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }

  provisioner "file" {
    source      = "../azure-fraud-guard.tar.gz"
    destination = "/tmp/azure-fraud-guard.tar.gz"

    connection {
      type        = "ssh"
      host        = azurerm_public_ip.vm_public_ip.ip_address
      user        = var.admin_username
      private_key = file("~/.ssh/azure_vm_key")
      timeout     = "1m"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p /home/${var.admin_username}/azure-fraud-guard",
      "tar -xzf /tmp/azure-fraud-guard.tar.gz -C /home/${var.admin_username}/azure-fraud-guard",
      "rm /tmp/azure-fraud-guard.tar.gz"
    ]

    connection {
      type        = "ssh"
      host        = azurerm_public_ip.vm_public_ip.ip_address
      user        = var.admin_username
      private_key = file("~/.ssh/azure_vm_key")
      timeout     = "1m"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y ca-certificates curl",

      # Create keyring dir for Docker
      "sudo install -m 0755 -d /etc/apt/keyrings",

      # Add Docker GPG key
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc",
      "sudo chmod a+r /etc/apt/keyrings/docker.asc",

      # Add Docker repo
      "echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable' | sudo tee /etc/apt/sources.list.d/docker.list",
      "sudo apt-get update",

      # Install Docker and Compose plugin
      "sudo apt-get install -y docker-ce docker-ce-cli docker-compose-plugin",

      # Add user to Docker group
      "sudo usermod -aG docker ${var.admin_username}",
    ]

    connection {
      type        = "ssh"
      host        = azurerm_public_ip.vm_public_ip.ip_address
      user        = var.admin_username
      private_key = file("~/.ssh/azure_vm_key")
      timeout     = "1m"
    }
  }

  provisioner "remote-exec" {
    inline = [
      # Wait for docker to be ready before running compose
      "until docker info >/dev/null 2>&1; do echo 'Waiting for Docker...'; sleep 5; done",
      "sudo docker compose -f /home/${var.admin_username}/azure-fraud-guard/kafka/docker-compose.yaml up -d"
    ]

    connection {
      type        = "ssh"
      host        = azurerm_public_ip.vm_public_ip.ip_address
      user        = var.admin_username
      private_key = file("~/.ssh/azure_vm_key")
      timeout     = "1m"
    }
  }

  tags = local.common_tags
}
