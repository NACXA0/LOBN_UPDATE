# 测试页面
# 0695f53a-73e4-77de-8000-28a10c0c1833

from reflex as rx


class state(rx.State):
    pass


def test() -> rx.Component:
    return rx.text("测试页面")


