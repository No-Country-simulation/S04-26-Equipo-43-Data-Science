import reflex as rx

config = rx.Config(
    app_name="dashboard",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                has_background=True,
                radius="medium",
                accent_color="cyan",
            )
        )
    ]
)