from typer import Typer

from binance.binance_data_dl import download_binance_data

app = Typer()


@app.command(help="Download the monthly data from Binance")
def download():
    download_binance_data()


if __name__ == "__main__":
    app()
