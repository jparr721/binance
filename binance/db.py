import os
import sqlite3
from typing import Final

import pandas as pd

from binance import BINANCE_CODE_DIR, BINANCE_COMBINED_DATA_DIR

DATABASE_PATH: Final[str] = os.path.join(BINANCE_CODE_DIR, "..", "binance.sqlite")


def csv_to_sqlite(csv_file: str, table_name: str, db_file: str):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_file)

    # Convert the open_time to a valid timestamp
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

    # All tables have the same schema, so just make them uniformly
    schema = f"""CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            open_time DATETIME,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            close_time INTEGER,
            quote_asset_volume REAL,
            number_of_trades INTEGER,
            taker_buy_base_asset_volume REAL,
            taker_buy_quote_asset_volume REAL,
            ignore REAL)"""

    # Write the DataFrame to the SQLite database by iterating the rows and inserting
    # them one by one
    df.to_sql(table_name, conn, if_exists="replace", index=False, schema=schema)

    # Commit the changes and close the database connection
    conn.commit()

    # Close the database connection
    conn.close()


def create_database():
    for csv_file in os.listdir(BINANCE_COMBINED_DATA_DIR):
        csv_to_sqlite(
            os.path.join(BINANCE_COMBINED_DATA_DIR, csv_file),
            # Remove the extension and just keep the ticker symbol
            csv_file.replace("-1m-all.csv", ""),
            DATABASE_PATH,
        )


def query_sqlite(query: str):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)

    # Query the database
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    return df
