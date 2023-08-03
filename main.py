import os

import typer
from loguru import logger

from binance_data_dl import download_binance_data_klines
from binance_ui.db import DATABASE_PATH, create_database

app = typer.Typer(add_completion=False)


def init_db(refresh):
    # Create the sqlite database from the data.nosync/combined folder
    if not os.path.exists(DATABASE_PATH):
        try:
            logger.info("Creating database.")
            create_database()
        except Exception as e:
            logger.error(f"Failed to create database with error: {e}")
            raise e
    else:
        if refresh:
            logger.info("Deleting existing database.")
            os.remove(DATABASE_PATH)
            logger.info("Creating new database.")
            create_database()
        else:
            logger.info("Database already exists.")


@app.command(help="Download the monthly data from Binance.")
def download(
    refresh: bool = typer.Option(False, help="Whether or not to attempt to download the latest binance data.")
):
    download_binance_data_klines(refresh)


@app.command(help="Start Web UI")
def web():
    init_db(False)
    os.system("reflex run")


@app.command(help="Create the SQLite database.")
def make_db(refresh: bool = typer.Option(False, help="Whether or not to delete and re-make the sqlite database.")):
    init_db(refresh)


if __name__ == "__main__":
    app()
