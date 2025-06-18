# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher

variable "location" {
  description = "Azure region for resource deployment"
  type        = string
  default     = "West Europe"
}

variable "subscription_id" {
  description = "Azure subscription under which resources will be created"
  type        = string
  sensitive   = true
}

variable "admin_username" {
  description = "Admin username for VM"
  type        = string
}

variable "admin_password" {
  description = "Admin password for VM"
  type        = string
  sensitive   = true
}

variable "ssh_public_key" {
  description = "SSH public key for VM; set via TF_VAR_SSH_PUBLIC_KEY locally or GitHub Secrets in CI."
  type        = string
}
