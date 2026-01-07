import reflex as rx






class DataBase:
    # 【未启用】schema_name: str = "public"    # 架构名-默认 public
    pass
    





config = rx.Config(
    app_name="LOBN_UPDATE",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
