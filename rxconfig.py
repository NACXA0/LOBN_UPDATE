# 包含reflex基本参数

import reflex as rx


config = rx.Config(
    app_name="LOBN_UPDATE", # 应用的名称（应与应用目录匹配）
    state_auto_setters=True,    # 是否自动为状态基变量创建 setter,也就是启用 state.set_var
    show_built_with_reflex=False,  # 不显示reflex标签  需要订阅团队，否则修改底层 秘密
    #loglevel
    #frontend_port = 3000,   #前端端口
    #frontend_path
    #backend_port = 8000,    #后端端口
    #api_url
    #deploy_url
    #redis='redis://localhost:6379'  # 不用这个，使用内部的redis
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)

