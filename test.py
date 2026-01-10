import global_config
import uuid, itertools, time, datetime, random, ast, calendar
from sqlmodel import Session, select, update, func, or_, outerjoin, and_, exists, not_
from LOBN_UPDATE.DataBase_function.database import engine
from LOBN_UPDATE.DataBase_function.models import config_page, config_system, user, org, org_map_org2identity, identity
from uuid_extensions import uuid7, uuid7str

def print_info():
    print('UUID7:', uuid7str())
    print('当前时间Datetime:', datetime.datetime.now())
    print(uuid7(0))


def test_db():
    with Session(engine) as session:
        command = select(config_system)
        info_data = session.exec(command).first()
        print('WWWWWWWWW', type(info_data), info_data)


def test_redis():
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    value = r.get('foo')
    print('Redis value for key "foo":', value.decode('utf-8'))

def test_redis_om():
    # region 构建模型
    import datetime
    from typing import Optional
    from pydantic import EmailStr
    from redis_om import HashModel, Migrator


    class Customer(HashModel):
        first_name: str
        last_name: str
        email: EmailStr
        join_date: datetime.date
        age: int
        bio: Optional[str] = None
    # endregion

    # region 增加
    andrew = Customer(
        first_name="Andrew",
        last_name="Brookins",
        email="andrew.brookins@example.com",
        join_date=datetime.date.today(),
        age=38,
        bio="Python developer, works at Redis, Inc."
    )

    # 模型会自动生成全局唯一主键, 无需与 Redis 进行交互。
    print(andrew.pk)
    # > "01FJM6PH661HCNNRC884H6K30C"

    # 我们可以通过调用`save()`将模型保存到Redis中:
    andrew.save()

    # 2分钟（120秒）后使模型过期
    andrew.expire(120)

    # T为了用主键检索这个客户，我们使用`customer.get（）`：
    assert Customer.get(andrew.pk) == andrew
    # endregion


    # region 查询
    # 现在，如果我们将此模型与Redis部署一起使用
    # 安装了RediSearch模块后，我们可以运行以下查询。

    #在运行查询之前，我们需要运行迁移来设置
    #Redis OM将使用的索引。您还可以使用“migrate”`
    #CLI工具！
    Migrator().run()

    # 查找姓氏为“Brookins”的所有客户
    Customer.find(Customer.last_name == "Brookins").all()

    # F查找所有没有姓氏“Brookins”的客户
    Customer.find(Customer.last_name != "Brookins").all()

    # 查找姓氏为“Brookins”或年龄为
    #100，姓“史密斯”
    Customer.find((Customer.last_name == "Brookins") | (
            Customer.age == 100
    ) & (Customer.last_name == "Smith")).all()
    # endregion

1. 测试一下新增的pydantic方式获取配置。
2. 不要学习redis-om了，以后再说吧。
3. 将现在的 变量存储（pydantic范式）应用起来。


if __name__ == '__main__':
    print_info()
    #test_db()
    test_redis_om()
