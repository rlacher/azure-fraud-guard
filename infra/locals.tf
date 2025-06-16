# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher

# Common tags for all provisioned resources
locals {
  common_tags = {
    Project     = "Azure Fraud Guard"
    Environment = "mvp"
    ManagedBy   = "Terraform"
  }
}
