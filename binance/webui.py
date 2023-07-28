import os

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
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
    q = request.args.get("q")
    if q is None:
        q = ""

    return render_template("index.html", error_msg=error_msg, q=q)


@app.route("/submit_query", methods=["GET"])
def submit_query():
    q = request.args.get("q")

    if q is None:
        return redirect(url_for("index", error_msg="No query provided"))
    else:
        # Submit the raw query to the sqlite instance
        # and return the result
        try:
            dataframe: pd.DataFrame = query_sqlite(q)

            # Convert the dataframe to a JSON string
            query_json = dataframe.to_json(orient="records")
            query_html = dataframe.to_html(table_id="query_table")

            return render_template("index.html", error_msg="", query_json=query_json, query_html=query_html, q=q)

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return redirect(url_for("index", error_msg=f"Error executing query: {e}"))
