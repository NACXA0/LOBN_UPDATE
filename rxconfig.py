import reflex as rx

config = rx.Config(
    app_name="LOBN_UPDATE",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)