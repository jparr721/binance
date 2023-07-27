import os

import pandas as pd
from flask import Flask, make_response, redirect, render_template, request, url_for
from loguru import logger

from binance import BINANCE_CODE_DIR
from binance.db import query_sqlite

STATIC_ASSET_DIR = os.path.join(BINANCE_CODE_DIR, "..", "static")

app = Flask(__name__, template_folder=STATIC_ASSET_DIR)


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    error_msg = request.args.get("error_msg")
    if error_msg is None:
        error_msg = ""

    return render_template("index.html", error_msg=error_msg)


@app.route("/q", methods=["GET"])
def submit_query():
    q = request.args.get("query")

    if q is None:
        return {}
    else:
        # Submit the raw query to the sqlite instance
        # and return the result
        try:
            dataframe: pd.DataFrame = query_sqlite(q)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return {}

        # Convert the dataframe to a JSON string
        json_str = dataframe.to_json(orient="records")
        return json_str
