# 测试页面

from reflex as rx


class state(rx.State):
    pass


def test() -> rx.Component:
    return rx.text("测试页面")


