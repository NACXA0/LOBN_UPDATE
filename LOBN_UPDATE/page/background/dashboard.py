# 控制台

import reflex as rx




class state(rx.State):
    activate_users: list[dict] = [] # 当前活跃用户  {'uuid': '用户uuid', 'login_date': '登录时间'}


def dashboard() -> rx.Component:
    return rx.center(
        rx.heading("控制台", font_size="2rem"),

        # 原理：redis定期向用户发送redis心跳包。
        rx.heading('当前活跃用户'),
        # 从redis获取数据-》转换写入state.activate_users



        height="100vh",
    )

