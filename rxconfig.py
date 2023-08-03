import reflex as rx


class BinanceuiConfig(rx.Config):
    pass


config = BinanceuiConfig(
    app_name="binance_ui",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)

