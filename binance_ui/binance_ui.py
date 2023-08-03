import reflex as rx
from binance_ui.db import query_sqlite
import plotly.express as px
import plotly.graph_objects as go


def every(seq, nth: int, do, else_):
    if not isinstance(seq, list) and not isinstance(seq, tuple):
        raise ValueError(f"Expected sequence of list or tuple, got '{type(seq)}'")

    out = []
    for i, entry in enumerate(seq):
        if i == 0:
            do(seq, entry, out)
            continue

        if i % nth == 0:
            do(seq, entry, out)
            continue

        else_(seq, entry, out)
    return out


class State(rx.State):
    pass


class Fig:
    def __init__(self, fig, title):
        self.fig = fig
        self.title = title

    def __call__(self):
        return rx.vstack(rx.heading(self.title, size="md"), rx.plotly(data=self.fig))


def make_candlestick_figs(symbol="ETHUSDC"):
    daily_data = query_sqlite(
        f"""SELECT strftime('%Y-%m-%d', open_time) AS x,
               MIN(open)                       AS open,
               MAX(high)                       AS high,
               MIN(low)                        AS low,
               MAX(close)                      AS close
           FROM {symbol}
           WHERE x >= DATE('now', '-5 years')
           GROUP BY x limit 1000"""
    ).to_dict(orient="list")
    daily_fig = go.Figure(data=[go.Candlestick(**daily_data)])

    monthly_data = query_sqlite(
        f"""
        SELECT strftime('%Y-%m', open_time) AS x,
           MIN(open)                    AS open,
           MAX(high)                    AS high,
           MIN(low)                     AS low,
           MAX(close)                   AS close
        FROM {symbol}
        WHERE x >= DATE('now', '-5 years')
        GROUP BY x"""
    ).to_dict(orient="list")
    monthly_fig = go.Figure(data=[go.Candlestick(**monthly_data)])

    yearly_data = query_sqlite(
        f"""
        SELECT strftime('%Y', open_time) AS x,
               MIN(open)                 AS open,
               MAX(high)                 AS high,
               MIN(low)                  AS low,
               MAX(close)                AS close
        FROM {symbol}
        WHERE x >= DATE('now', '-5 years')
        GROUP BY x
        """
    ).to_dict(orient="list")
    yearly_fig = go.Figure(data=[go.Candlestick(**yearly_data)])

    return (
        Fig(daily_fig, "ETHUSDC Price Change Per Day"),
        Fig(monthly_fig, "ETHUSDC Price Change Per Month"),
        Fig(yearly_fig, "ETHUSDC Price Change Per Year"),
    )


def index() -> rx.Component:
    """A view of the todo list.

    Returns:
        The index page of the todo app.
    """

    # for fig in make_candlestick_figs():
    #     rx.for

    return rx.container(
        rx.heading("Binance Viewer"),
        *[f() for f in make_candlestick_figs()],
        center_content=True,
    )


# Create the app and add the state.
app = rx.App(state=State)

# Add the index page and set the title.
app.add_page(index, title="Binance Viewer")

# Compile the app.
app.compile()
