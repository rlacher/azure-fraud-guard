# Azure Fraud Guard

<!-- Badges -->
[![terraform-format](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/terraform-fmt.yaml?label=terraform-format&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/terraform-fmt.yaml)
[![terraform-validate](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/terraform-validate.yaml?label=terraform-validate&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/terraform-validate.yaml)
[![docker-build](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/docker.yaml?label=docker-build&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/docker.yaml)
[![flake8](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/lint.yaml?label=flake8&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/lint.yaml)
[![pytest](https://img.shields.io/github/actions/workflow/status/rlacher/azure-fraud-guard/test.yaml?label=pytest&style=flat)](https://github.com/rlacher/azure-fraud-guard/actions/workflows/test.yaml)
[![license](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://spdx.org/licenses/MIT.html)

Foundation for an end-to-end cloud-native fraud detection pipeline on Azure.

## Prerequisites

- Terraform v1.12 or later
- Azure CLI configured with access to your subscription
- SSH client installed (for key generation, VM provisioning and remote access)

## Getting Started

1. Generate an SSH key pair for VM setup and access:

   ```bash
   mkdir -p ~/.ssh
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/azure_vm_key -N ""
   ```

2. Clone the repository and navigate to the infra directory:

   ```bash
   git clone https://github.com/rlacher/azure-fraud-guard.git
   cd azure-fraud-guard/infra
   ```

3. Initialise Terraform:
   ```bash
   terraform init
   ```

4. Set the SSH public key as an environment variable for Terraform:

   ```bash
   export TF_VAR_SSH_PUBLIC_KEY="$(cat ~/.ssh/azure_vm_key.pub)"
   ```

5. Provide required variables either in a `.tfvars` file or as environment variables:

    - `subscription_id` (Azure subscription ID)
    - `admin_username` (VM admin username)
    - `admin_password` (VM admin password)

6. Apply the Terraform configuration to provision resources:

    ```bash
    infra/scripts/pre-apply.sh
    cd infra
    terraform apply -auto-approve
    ```

*Note:* Kafka is automatically installed and started on the Azure VM during provisioning, serving as an asynchronous event stream for fraud detection. No manual setup needed.

## Dataset

This project uses the [Credit Card Fraud dataset (ID: 45955)](https://www.openml.org/d/45955) available on OpenML under the CC0 Public Domain licence.

### Feature Description

- **Task**: Supervised binary classification
- **Target variable**: `fraud` (1 = fraud, 0 = legitimate)
- **Samples**: 1,000,000 transactions
- **Fraud cases**: 87,403 (8.7%) — imbalanced dataset
- **Features (8)**:
  - `distance_from_home`: Distance from cardholder’s home
  - `distance_from_last_transaction`: Distance from previous transaction
  - `ratio_to_median_purchase_price`: Transaction price relative to median spend
  - `repeat_retailer`: 1 if retailer previously used; else 0
  - `used_chip`: 1 if card chip used; else 0
  - `used_pin_number`: 1 if PIN entered; else 0
  - `online_order`: 1 if transaction online; else 0

The dataset is labelled and imbalanced, reflecting the nature of real-world fraud detection problems. No preprocessing or feature engineering was applied before model development.

### Download Instructions

To download the dataset automatically:

```bash
python3 data/download.py
```

<!-- Original Kaggle source: https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud -->

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Developed by [René Lacher](https://github.com/rlacher).
