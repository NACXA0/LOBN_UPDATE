# 后台设置页面
# 0695f540-03b9-7d73-8000-7cd5a31822d2
'''
后台设置的整体模版
面向PC端
'''


import reflex as rx
import global_config, uuid
from sqlmodel import Session, select
from LOBN_UPDATE.DataBase_function.database import engine
from LOBN_UPDATE.DataBase_function.models import config_system
from uuid_extensions import uuid7, uuid7str
from LOBN_UPDATE.public_function import random_user_name

class state(rx.State):
    config_page: dict = {}
    config_system: dict = {}
    config_test_var: str  # 测试用的变量，后台配置修改后会更新此变量的值
    
    @rx.event
    def test_update_config_var(self, new_value: dict):
        # 模拟更新配置变量的操作
        
        # 写入数据库
        with Session(engine) as session:
            session.add(config_system(
                value=new_value['new_value'], 
                value_type='str', 
                name=f'测试后台设置值({random_user_name()})',
                tip='这是一个用于测试的后台设置值',
                create_user_uuid='06960ab6-bd3d-739d-8000-ec86da6176d5'
            ))
            session.commit()

        return rx.toast.success('配置已更新！')

    # 加载-主动刷新以更新
    def load_config_system_from_var_test(self):
        # 方案1：变量缓存
        self.config_test_var = global_config.test_config_var

        # 方案2:redis-om缓存
        正在做

        print('state.var主动刷新加载配置：', self.config_test_var)
        
@rx.page(on_load=state.load_config_system_from_var_test)
def setting() -> rx.Component:
    return rx.box(
        rx.card(
            rx.text('测试后台设置值：', state.config_test_var),
            rx.form(
                rx.input(placeholder='新值', name='new_value'),
                rx.button('提交', type='submit'),
                on_submit=state.test_update_config_var
            )

        )
    )
