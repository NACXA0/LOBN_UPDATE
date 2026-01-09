# 测试页面
# 0695f53a-73e4-77de-8000-28a10c0c1833

import reflex as rx
from LOBN_UPDATE.public_state import BaseState, state_login

class state(rx.State):
    pass


def test() -> rx.Component:
    return rx.vstack(
        rx.text("测试页面"),
        rx.text('用户uuid:', BaseState.user_uuid),
        rx.text('用户名称:', BaseState.user_name),
        rx.text('用户手机号:', BaseState.user_phone_number),
        rx.text('身份:', BaseState.identity),
        rx.button('重新登录', on_click=state_login.relogin)
    )


