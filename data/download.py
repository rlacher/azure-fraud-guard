# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher
# Download script for dataset from OpenML

import openml


def download_openml_dataset(dataset_id: int, output_file: str) -> None:
    """
    Downloads an OpenML dataset by ID and saves it as a CSV file.

    Args:
        dataset_id: OpenML dataset ID.
        output_file: Filename for the saved CSV.
    """
    # Retrieve dataset from OpenML
    dataset = openml.datasets.get_dataset(dataset_id)

    # Load data as pandas DataFrame (features) and Series (target)
    X, y, _, _ = dataset.get_data(dataset_format="dataframe")

    # Combine features and target into a single DataFrame
    df = X.copy()
    df['fraud'] = y

    # Save DataFrame to CSV
    df.to_csv(output_file, sep=",", index=False, encoding="utf-8")

    print(f"Dataset saved to {output_file}")


if __name__ == "__main__":
    DATASET_ID = 45955
    OUTPUT_CSV = "card_transdata.csv"
    download_openml_dataset(DATASET_ID, OUTPUT_CSV)
