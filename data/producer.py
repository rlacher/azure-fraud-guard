# SPDX-License-Identifier: MIT
# Copyright (c) 2025 René Lacher
# Data-generating producer for transactional data

import json
import logging
import os
import sys
import time

from kafka import KafkaProducer
import pandas as pd

DATA_FILENAME: str = os.getenv('DATA_FILENAME')
KAFKA_TOPIC: str = 'transactions'
KAFKA_BROKER_HOST: str = 'kafka-kraft'
KAFKA_BROKER_PORT: int = 9092
WAIT_TIME_S: float = 1.0
NUM_TRANSACTIONS: int = 100

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data(filename: str) -> pd.DataFrame:
    """Load fraud transaction data from a CSV file.

    Args:
        filename: Path to the CSV file containing transaction data.
    Returns:
        DataFrame containing the transaction data.
    Raises:
        Exception: If the file cannot be read or parsed.
    """
    try:
        df = pd.read_csv(filename)
        logger.info(f"Loaded dataframe with {len(df)} rows")

        return df
    except Exception as e:
        logger.error(
            f"Failed to load data from {filename}: {e}",
            exc_info=True
        )
        raise


def drop_fraud_column(df: pd.DataFrame) -> pd.DataFrame:
    """Drop the 'fraud' column from the DataFrame if it exists.

    Args:
        df: DataFrame containing transaction data.
    Returns:
        DataFrame without the 'fraud' column.
    """
    if 'fraud' in df.columns:
        df = df.drop(columns=['fraud'])
        logger.info("Dropped 'fraud' column from DataFrame.")
    return df


def init_kafka_producer(server: str, port: int) -> KafkaProducer:
    """Initialize a Kafka producer.

    Args:
        server: Kafka broker server name or address.
        port: Kafka broker port.
    Returns:
        KafkaProducer instance.
    """
    producer = KafkaProducer(
        bootstrap_servers=f'{server}:{port}',
        retries=5,
        retry_backoff_ms=2000,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )
    return producer


def stream_random_transactions(
        df: pd.DataFrame,
        producer: KafkaProducer,
        topic: str,
        wait_time: float,
        num_transactions: int = NUM_TRANSACTIONS
) -> None:
    """Stream transactions to Kafka topic.

    Selects a random sample of transactions and sends them to the Kafka topic.

    Args:
        df: DataFrame containing transaction data.
        producer: KafkaProducer instance to send messages.
    """
    df_sample = df.sample(n=min(num_transactions, len(df)), random_state=42)
    logger.info(
        f"Streaming {num_transactions} "
        f"random transactions to topic '{topic}'."
    )

    for _, row in df_sample.iterrows():
        transaction = row.to_dict()
        try:
            producer.send(topic, value=transaction)
            logger.debug(f"Produced transaction: {transaction}")
            time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Error sending transaction: {e}", exc_info=True)

    producer.flush()
    logger.info("Finished streaming transactions.")


if __name__ == "__main__":
    if DATA_FILENAME is None:
        logger.critical(
            "Required environment variable 'DATA_FILENAME' is not set."
        )
        sys.exit(1)
    else:
        logger.info(f"Using data file: {DATA_FILENAME}")

    df = load_data(DATA_FILENAME)
    df = drop_fraud_column(df)

    producer = init_kafka_producer(
        KAFKA_BROKER_HOST,
        KAFKA_BROKER_PORT
    )

    stream_random_transactions(
        df,
        producer,
        KAFKA_TOPIC,
        WAIT_TIME_S
    )
