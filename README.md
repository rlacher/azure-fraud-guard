# Azure Fraud Guard

<!-- Badges -->
[![terraform-format](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/terraform-fmt.yaml?label=terraform-format&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/terraform-fmt.yaml)
[![terraform-validate](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/terraform-validate.yaml?label=terraform-validate&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/terraform-validate.yaml)
[![license](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://spdx.org/licenses/MIT.html)

Foundation for an end-to-end cloud-native fraud detection pipeline on Azure.

## Prerequisites

- Terraform v1.12 or later
- Azure CLI configured with access to your subscription

## Getting Started

1. Clone the repository and navigate to the infra directory:

   ```bash
   git clone https://github.com/rlacher/azure-fraud-guard.git
   cd azure-fraud-guard/infra
   ```

2. Initialise Terraform:
   ```bash
   terraform init
   ```

3. Provide required variables by creating a `terraform.tfvars` file or exporting environment variables:

    - `subscription_id` (Azure subscription ID)
    - `admin_username` (VM admin username)
    - `admin_password` (VM admin password)

4. Apply the Terraform configuration:

    ```bash
    terraform apply
    ```

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Developed by [René Lacher](https://github.com/rlacher).
