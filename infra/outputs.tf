# SPDX-License-Identifier: MIT
# Outputs for provisioned resources

output "vm_public_ip_address" {
  description = "The public IP address of the Azure VM"
  value       = azurerm_public_ip.vm_public_ip.ip_address
}
