# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher
# Download script for dataset from OpenML

import os
import openml


def get_output_filename() -> str:
    filename = os.getenv("DATA_FILENAME")
    if not filename:
        raise RuntimeError(
            "Environment variable 'DATA_FILENAME' is not defined."
        )
    return filename


def download_openml_dataset(dataset_id: int, output_file: str) -> None:
    """
    Downloads an OpenML dataset by ID and saves it as a CSV file.

    Args:
        dataset_id: OpenML dataset ID.
        output_file: Filename for the saved CSV.
    """
    # Retrieve dataset metadata and data
    dataset = openml.datasets.get_dataset(dataset_id)
    df, _, _, _ = dataset.get_data(dataset_format="dataframe")

    # Ensure the label column exists
    if 'fraud' not in df.columns:
        raise ValueError("Expected label column 'fraud' not found in dataset.")

    # Save dataset to CSV using standard encoding and separator
    df.to_csv(output_file, sep=",", index=False, encoding="utf-8")

    print(f"Dataset saved to: {output_file}")


if __name__ == "__main__":
    DATASET_ID = 45955
    OUTPUT_CSV = get_output_filename()
    download_openml_dataset(DATASET_ID, OUTPUT_CSV)
