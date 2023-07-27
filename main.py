import os

import typer
from loguru import logger

from binance.binance_data_dl import download_binance_data
from binance.db import DATABASE_PATH, create_database
from binance.webui import app as webui_app

app = typer.Typer(add_completion=False)


@app.command(help="Download the monthly data from Binance.")
def download(
    refresh: bool = typer.Option(False, help="Specifies whether to attempt to download the latest binance data.")
):
    download_binance_data(refresh)


@app.command(help="Start the web UI.")
def webui(port: int = typer.Option(8080, help="The port to run the web UI on.")):
    # Create the sqlite database from the data.nosync/combined folder
    if not os.path.exists(DATABASE_PATH):
        try:
            logger.info("Database not found, creating.")
            create_database()
        except Exception as e:
            logger.error(f"Failed to create database with error: {e}")
            raise e

    webui_app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    app()
