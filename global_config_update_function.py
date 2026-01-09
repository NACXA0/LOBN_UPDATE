# 获取全局python变量的生命周期函数
import global_config, asyncio, random
from decimal import Decimal
from sqlmodel import Session, select
from LOBN_UPDATE.DataBase_function.database import engine
from LOBN_UPDATE.DataBase_function.models import config_system

# 生命周期任务-定时查询配置文件数据库->写入python程序变量
async def load_config_page_from_db():
    try:
        while True:
            # 查询配置文件数据库
            #print('占位-查询一次数据库')
            # 写入python变量
            #print('占位-一条数据是一个页面配置的json-将所有的配置数据行写入到对应页面的python变量中')
            await asyncio.sleep(global_config.freq_of_get_ui_config)  # 每几秒查询一次
    except asyncio.CancelledError:
        print("程序因错误而关闭: async def load_config_page_from_db():")

# 生命周期任务-定时查询系统配置数据库->写入python程序变量
async def load_config_system_from_db():
    try:
        while True:
            # 查询系统配置数据库
            #print('占位-查询一次系统配置数据库')
            # 写入python变量
            #print('占位-将系统配置数据行写入到对应的python变量中')
            await asyncio.sleep(global_config.freq_of_get_config_system)  # 每几秒查询一次
    except asyncio.CancelledError:
        print("程序因错误而关闭: async def load_config_page_from_db():")

# 生命周期任务-定时查询系统配置数据库->写入python程序变量
async def load_config_system_from_db_test_config_var():
    try:
        while True:
            # 查询系统配置数据库
            # '占位-查询一次系统配置数据库'
            with Session(engine) as session:
                # 1. 在数据库里查询对uuid的用户
                response = session.exec(select(config_system)).all()  # 找到的数据行
                # '占位-将系统配置数据行写入到对应的python变量中'
                out = response[random.randint(0, len(response)-1)]
                if response:

                    # 方案1: 变量缓存
                    global_config.test_config_var = out.value

                    # 方案2: redis缓存
                    正在做

            await asyncio.sleep(5)  # 每几秒查询一次
    except asyncio.CancelledError:
        print("程序因错误而关闭: async def load_config_page_from_db():")





