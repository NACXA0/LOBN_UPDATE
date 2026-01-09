# 首页
# 纯静态文件->为了首页加载速度
# 0695f538-b4e4-7521-8000-479e0f78d3fb
import reflex as rx



def index() -> rx.Component:
    return rx.center(
        rx.heading('欢迎来到首页'), 
        rx.link('登录', href='/login')
    )


