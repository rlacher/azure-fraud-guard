# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher

import logging
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

import producer


@pytest.fixture
def sample_dataframe():
    """Provides a sample DataFrame resembling transaction data."""
    return pd.DataFrame({
        'distance_from_home': [57.88, 10.83, 5.09],
        'distance_from_last_transaction': [0.31, 0.18, 0.81],
        'ratio_to_median_purchase_price': [1.95, 1.29, 0.43],
        'repeat_retailer': [1, 1, 1],
        'used_chip': [1, 0, 0],
        'used_pin_number': [0, 0, 0],
        'online_order': [0, 0, 1],
        'fraud': [0, 0, 1],
    })


def test_load_data_success(tmp_path, sample_dataframe):
    """Ensure CSV loading returns a DataFrame with expected columns/data."""
    sample_csv = tmp_path / "sample.csv"
    sample_dataframe.to_csv(sample_csv, index=False)

    df = producer.load_data(str(sample_csv))

    assert not df.empty
    assert list(df.columns) == list(sample_dataframe.columns)
    pd.testing.assert_frame_equal(
        df.reset_index(drop=True), sample_dataframe.reset_index(drop=True)
    )


def test_load_data_file_not_found():
    """Ensure load_data raises exception for missing file."""
    with pytest.raises(Exception):
        producer.load_data("non_existent_file.csv")


def test_drop_fraud_column_present(sample_dataframe):
    """Drop 'fraud' column if present."""
    df_with_fraud = sample_dataframe.copy()
    result_df = producer.drop_fraud_column(df_with_fraud)

    # 'fraud' column should be removed
    assert 'fraud' not in result_df.columns

    expected_cols = [col for col in sample_dataframe.columns if col != 'fraud']
    assert list(result_df.columns) == expected_cols

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        df_with_fraud.drop(columns=['fraud']).reset_index(drop=True)
    )


def test_drop_fraud_column_not_present(sample_dataframe):
    """Return unchanged DataFrame if 'fraud' column missing."""
    df_without_fraud = sample_dataframe.drop(columns=['fraud'])
    result_df = producer.drop_fraud_column(df_without_fraud)

    assert list(result_df.columns) == list(df_without_fraud.columns)

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        df_without_fraud.reset_index(drop=True)
    )


@patch('producer.KafkaProducer')
def test_init_kafka_producer_success(mock_producer_class):
    """Ensure KafkaProducer is initialized with correct parameters."""
    mock_instance = mock_producer_class.return_value

    kafka_producer = producer.init_kafka_producer("kafka-kraft", 9092)

    mock_producer_class.assert_called_once()
    _, kwargs = mock_producer_class.call_args
    assert kwargs['bootstrap_servers'] == 'kafka-kraft:9092'
    assert kafka_producer is mock_instance


@patch('producer.time.sleep', return_value=None)
def test_stream_transactions_success(mock_sleep, sample_dataframe):
    """Ensure stream_random_transactions sends correct number of messages."""
    mock_producer = MagicMock()

    producer.stream_random_transactions(
        df=sample_dataframe,
        producer=mock_producer,
        topic="transactions",
        wait_time=0,
        num_transactions=2
    )

    assert mock_producer.send.call_count == 2
    assert mock_producer.flush.called, "Producer.flush() should be called"

    # Check that the correct topic was used in all send calls
    for call in mock_producer.send.call_args_list:
        args, _ = call
        assert args[0] == "transactions"


@patch('producer.time.sleep', return_value=None)
def test_stream_transactions_handles_send_exceptions(
    mock_sleep, sample_dataframe, caplog
):
    """Ensure send exceptions are caught, logged, and all attempts made."""
    mock_producer = MagicMock()
    mock_producer.send.side_effect = Exception("Send error")

    with caplog.at_level(logging.ERROR):
        producer.stream_random_transactions(
            df=sample_dataframe,
            producer=mock_producer,
            topic="transactions",
            wait_time=0,
            num_transactions=2
        )

    # All send attempts are made, despite internal exceptions
    assert mock_producer.send.call_count == 2
    assert mock_producer.flush.called

    # Check that error logs were emitted for send failures
    error_logs = [
        record for record in caplog.records if record.levelno == logging.ERROR
    ]
    assert any("Error sending transaction" in record.message
               for record in error_logs)
