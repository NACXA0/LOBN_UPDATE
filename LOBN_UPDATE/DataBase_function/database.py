'''
!!!!!根据教程，具体的函数是写在应用程序内容的，也就是下面with……as……的程序app内的，
而这里应该是写一些可以通用的，比如创建引擎和创建表。
所以像是查询、增加/修改/删除等等这样对表有具体操作的，不写在这里，而是与具体需要他的函数结合。
'''
import rxconfig
from sqlmodel import Field, Session, SQLModel, create_engine, select
global engine
# 连接数据库
CONFIG = rxconfig.DataBase
db_url = str("postgresql+psycopg2://" + str(CONFIG.user) + ":" + str(CONFIG.password) + "@" + str(CONFIG.host) + ":" + str(CONFIG.port) + "/" + str(CONFIG.dbname))
#创建引擎
engine = create_engine(db_url, echo=not rxconfig.is_prod)   #【仅测试环境需要】打印运行内容echo=True

# 创建表——sqlmodel根据model里的定义自动创建表，无需手动创建数据库。
def create_db_and_tables():     #【待完善】
    SQLModel.metadata.create_all(engine)