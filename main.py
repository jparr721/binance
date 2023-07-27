import typer

from binance.binance_data_dl import download_binance_data

app = typer.Typer(add_completion=False)


@app.command(help="Download the monthly data from Binance.")
def download(
    refresh: bool = typer.Option(False, help="Specifies whether to attempt to download the latest binance data.")
):
    download_binance_data(refresh)


if __name__ == "__main__":
    app()
