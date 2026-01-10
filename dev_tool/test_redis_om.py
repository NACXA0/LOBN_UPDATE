"""
Redis OM Python 综合测试用例
涵盖：数据建模、验证、保存、查询、嵌入模型、直接Redis命令
"""

import datetime
from typing import Optional
from pydantic import EmailStr, ValidationError
from redis_om import (
    HashModel,
    JsonModel,
    EmbeddedJsonModel,
    Field,
    Migrator,
    get_redis_connection
)


def test_redis_om_comprehensive():
    """
    Redis OM Python 综合测试用例
    包含以下测试场景：
    1. 基本模型定义和保存
    2. 数据验证（email格式）
    3. 主键生成和获取
    4. 过期时间设置
    5. 嵌入模型（Address嵌入到Customer）
    6. 查询功能（等值、不等值、AND/OR组合）
    7. 索引创建和迁移
    8. 直接执行Redis命令
    9. 全文搜索功能
    """
    
    # ========== 1. 定义模型 ==========
    
    class Customer(HashModel, index=True):
        """客户模型 - HashModel存储"""
        first_name: str = Field(index=True)
        last_name: str = Field(index=True)
        email: EmailStr
        join_date: datetime.date = Field(index=True)
        age: int = Field(index=True)
        bio: Optional[str] = Field(full_text_search=True, default="")
    
    class Address(EmbeddedJsonModel):
        """地址模型 - 可嵌入到其他模型"""
        address_line_1: str
        address_line_2: Optional[str] = None
        city: str = Field(index=True)
        state: str = Field(index=True)
        country: str
        postal_code: str = Field(index=True)
    
    class CustomerWithAddress(JsonModel, index=True):
        """包含嵌入地址的客户模型 - JsonModel存储"""
        first_name: str
        last_name: str
        email: str
        join_date: datetime.date
        age: int
        bio: Optional[str] = Field(full_text_search=True, default="")
        address: Address  # 嵌入模型
    
    class Demo(HashModel):
        """演示模型 - 用于Redis命令测试"""
        some_field: str
    
    # ========== 2. 创建索引（迁移） ==========
    print("创建索引...")
    Migrator().run()
    
    # ========== 3. 测试数据验证 ==========
    print("\n=== 测试数据验证 ===")
    try:
        Customer(
            first_name="Andrew",
            last_name="Brookins",
            email="Not an email address!",  # 无效邮箱
            join_date=datetime.date.today(),
            age=38,
            bio="Python developer"
        )
        assert False, "应该抛出验证错误"
    except ValidationError as e:
        print(f"✓ 邮箱验证正确触发: {e}")
        assert "email" in str(e)
    
    # ========== 4. 测试基本CRUD操作 ==========
    print("\n=== 测试基本CRUD ===")
    
    # 创建客户
    andrew = Customer(
        first_name="Andrew",
        last_name="Brookins",
        email="andrew.brookins@example.com",
        join_date=datetime.date.today(),
        age=38,
        bio="Python developer, works at Redis, Inc."
    )
    
    # 保存到Redis
    andrew.save()
    print(f"✓ 客户保存成功，主键: {andrew.pk}")
    
    # 设置过期时间（2分钟）
    andrew.expire(120)
    print("✓ 设置过期时间120秒")
    
    # 通过主键获取
    retrieved_customer = Customer.get(andrew.pk)
    assert retrieved_customer == andrew
    print("✓ 通过主键获取客户成功")
    
    # ========== 5. 测试嵌入模型 ==========
    print("\n=== 测试嵌入模型 ===")
    
    address = Address(
        address_line_1="123 Main St",
        city="San Antonio",
        state="TX",
        country="USA",
        postal_code="78201"
    )
    
    customer_with_addr = CustomerWithAddress(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        join_date=datetime.date.today(),
        age=30,
        bio="Redis enthusiast",
        address=address
    )
    
    customer_with_addr.save()
    print(f"✓ 包含地址的客户保存成功，主键: {customer_with_addr.pk}")
    
    # ========== 6. 测试查询功能 ==========
    print("\n=== 测试查询功能 ===")
    
    # 创建更多测试数据
    customers = [
        Customer(
            first_name="Jane",
            last_name="Brookins",
            email="jane.brookins@example.com",
            join_date=datetime.date.today(),
            age=35,
            bio="Data scientist"
        ),
        Customer(
            first_name="Bob",
            last_name="Smith",
            email="bob.smith@example.com",
            join_date=datetime.date.today(),
            age=100,
            bio="Senior engineer"
        ),
        Customer(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            join_date=datetime.date.today(),
            age=100,
            bio="Project manager"
        ),
    ]
    
    for customer in customers:
        customer.save()
    
    print(f"✓ 创建了 {len(customers)} 个额外客户")
    
    # 查询：姓氏等于"Brookins"
    brookins_customers = Customer.find(Customer.last_name == "Brookins").all()
    print(f"✓ 找到姓氏为Brookins的客户: {len(brookins_customers)}个")
    assert len(brookins_customers) >= 2
    
    # 查询：姓氏不等于"Brookins"
    non_brookins = Customer.find(Customer.last_name != "Brookins").all()
    print(f"✓ 找到姓氏不为Brookins的客户: {len(non_brookins)}个")
    
    # 查询：复杂条件 (last_name="Brookins" OR (age=100 AND last_name="Smith"))
    complex_query = Customer.find(
        (Customer.last_name == "Brookins") | 
        ((Customer.age == 100) & (Customer.last_name == "Smith"))
    ).all()
    print(f"✓ 复杂查询结果: {len(complex_query)}个客户")
    
    # 查询：按城市和州查询（嵌入模型）
    sa_customers = CustomerWithAddress.find(
        CustomerWithAddress.address.city == "San Antonio",
        CustomerWithAddress.address.state == "TX"
    ).all()
    print(f"✓ 找到在San Antonio, TX的客户: {len(sa_customers)}个")
    
    # 查询：全文搜索
    bio_results = Customer.find(Customer.bio % "developer").all()
    print(f"✓ 全文搜索'developer'找到: {len(bio_results)}个客户")
    
    # ========== 7. 测试直接Redis命令 ==========
    print("\n=== 测试直接Redis命令 ===")
    
    redis_conn = Demo.db()
    redis_conn.sadd("myset", "a", "b", "c", "d")
    print("✓ 添加元素到集合")
    
    is_member_e = redis_conn.sismember("myset", "e")
    assert is_member_e is False
    print("✓ 检查'e'不在集合中")
    
    is_member_b = redis_conn.sismember("myset", "b")
    assert is_member_b is True
    print("✓ 检查'b'在集合中")
    
    # 使用 get_redis_connection
    redis_conn2 = get_redis_connection()
    redis_conn2.set("hello", "world")
    result = redis_conn2.get("hello")
    assert result.decode("utf-8") == "world"
    print("✓ 使用get_redis_connection读写数据")
    
    # ========== 8. 测试更新和删除 ==========
    print("\n=== 测试更新和删除 ===")
    
    # 更新客户信息
    andrew.age = 39
    andrew.bio = "Updated bio"
    andrew.save()
    print("✓ 更新客户信息")
    
    # 验证更新
    updated_customer = Customer.get(andrew.pk)
    assert updated_customer.age == 39
    assert updated_customer.bio == "Updated bio"
    print("✓ 更新验证成功")
    
    # 删除客户
    andrew.delete()
    assert Customer.get(andrew.pk) is None
    print("✓ 删除客户成功")
    
    # ========== 9. 测试批量操作 ==========
    print("\n=== 测试批量操作 ===")
    
    # 批量保存
    new_customers = [
        Customer(
            first_name=f"User{i}",
            last_name=f"Test{i}",
            email=f"user{i}@test.com",
            join_date=datetime.date.today(),
            age=20 + i,
            bio=f"Test user {i}"
        )
        for i in range(5)
    ]
    
    for customer in new_customers:
        customer.save()
    print("✓ 批量保存5个客户")
    
    # 批量查询 - 年龄范围
    young_customers = Customer.find(Customer.age < 25).all()
    print(f"✓ 查找年龄<25的客户: {len(young_customers)}个")
    
    # 批量删除
    for customer in new_customers:
        customer.delete()
    print("✓ 批量删除客户")
    
    # ========== 总结 ==========
    print("\n" + "="*50)
    print("✅ 所有测试通过！")
    print("="*50)
    print("\n功能覆盖:")
    print("  ✓ 数据建模（HashModel/JsonModel/EmbeddedJsonModel）")
    print("  ✓ 数据验证（Pydantic验证）")
    print("  ✓ CRUD操作（创建/读取/更新/删除）")
    print("  ✓ 索引和迁移")
    print("  ✓ 查询（等值/不等值/AND/OR/全文搜索）")
    print("  ✓ 嵌入模型")
    print("  ✓ 直接Redis命令")
    print("  ✓ 批量操作")
    print("  ✓ 过期时间设置")


# ========== 使用示例 ==========

if __name__ == "__main__":
    """
    运行测试的说明：
    
    1. 启动Redis（需要RediSearch和RedisJSON模块）:
       docker run -p 6379:6379 -p 8001:8001 redis/redis-stack
    
    2. 安装依赖:
       pip install redis-om pydantic
    
    3. 运行测试:
       python test_redis_om.py
    
    或使用pytest:
       pytest test_redis_om.py -v
    """
    test_redis_om_comprehensive()


# ========== 简化版快速测试 ==========

def test_redis_om_quick():
    """简化版快速测试 - 基本功能验证"""
    
    class SimpleCustomer(HashModel, index=True):
        name: str
        email: EmailStr
        age: int
    
    # 创建索引
    Migrator().run()
    
    # 保存数据
    customer = SimpleCustomer(
        name="Test User",
        email="test@example.com",
        age=25
    )
    customer.save()
    print(f"✓ 保存客户: {customer.pk}")
    
    # 查询数据
    found = SimpleCustomer.find(SimpleCustomer.name == "Test User").first()
    assert found.name == "Test User"
    print("✓ 查询成功")
    
    # 删除数据
    customer.delete()
    print("✓ 删除成功")


# ========== 测试特定功能 ==========

def test_validation_only():
    """仅测试数据验证功能"""
    
    class ValidatedModel(HashModel):
        email: EmailStr
        age: int = Field(gt=0, lt=150)  # 年龄必须>0且<150
        name: str = Field(min_length=2, max_length=50)
    
    # 有效数据
    valid = ValidatedModel(
        email="valid@example.com",
        age=25,
        name="Valid Name"
    )
    valid.save()
    print("✓ 有效数据保存成功")
    
    # 无效邮箱
    try:
        ValidatedModel(
            email="invalid",
            age=25,
            name="Valid Name"
        )
        assert False
    except ValidationError:
        print("✓ 邮箱验证生效")
    
    # 无效年龄
    try:
        ValidatedModel(
            email="valid@example.com",
            age=200,
            name="Valid Name"
        )
        assert False
    except ValidationError:
        print("✓ 年龄验证生效")
    
    # 无效名字长度
    try:
        ValidatedModel(
            email="valid@example.com",
            age=25,
            name="A"
        )
        assert False
    except ValidationError:
        print("✓ 名字长度验证生效")


def test_queries_only():
    """仅测试查询功能"""
    
    class QueryModel(HashModel, index=True):
        name: str
        value: int
        active: bool
    
    Migrator().run()
    
    # 创建测试数据
    items = [
        QueryModel(name="A", value=1, active=True),
        QueryModel(name="B", value=2, active=False),
        QueryModel(name="C", value=3, active=True),
    ]
    for item in items:
        item.save()
    
    # 等值查询
    results = QueryModel.find(QueryModel.name == "A").all()
    assert len(results) == 1
    print("✓ 等值查询")
    
    # 不等值查询
    results = QueryModel.find(QueryModel.name != "A").all()
    assert len(results) == 2
    print("✓ 不等值查询")
    
    # 布尔查询
    results = QueryModel.find(QueryModel.active == True).all()
    assert len(results) == 2
    print("✓ 布尔查询")
    
    # AND查询
    results = QueryModel.find(
        (QueryModel.value > 1) & (QueryModel.active == True)
    ).all()
    assert len(results) == 1
    print("✓ AND查询")
    
    # OR查询
    results = QueryModel.find(
        (QueryModel.name == "A") | (QueryModel.value == 3)
    ).all()
    assert len(results) == 2
    print("✓ OR查询")
    
    # 清理
    for item in items:
        item.delete()


def test_embedded_only():
    """仅测试嵌入模型"""
    
    class Phone(EmbeddedJsonModel):
        number: str
        type: str = Field(index=True)  # mobile/home/work
    
    class Contact(JsonModel, index=True):
        name: str
        phones: list[Phone]  # 嵌入模型列表
    
    Migrator().run()
    
    contact = Contact(
        name="John Doe",
        phones=[
            Phone(number="555-1234", type="mobile"),
            Phone(number="555-5678", type="home"),
        ]
    )
    contact.save()
    print(f"✓ 保存联系人: {contact.pk}")
    print(f"  手机: {contact.phones[0].number}")
    
    # 查询
    found = Contact.get(contact.pk)
    assert len(found.phones) == 2
    print("✓ 获取嵌入数据成功")
    
    contact.delete()


def test_redis_commands_only():
    """仅测试直接Redis命令"""
    
    class TestModel(HashModel):
        field: str
    
    # 通过模型获取连接
    conn = TestModel.db()
    
    # 字符串操作
    conn.set("test:key", "value")
    assert conn.get("test:key").decode() == "value"
    print("✓ 字符串操作")
    
    # 列表操作
    conn.lpush("test:list", "a", "b", "c")
    assert conn.llen("test:list") == 3
    print("✓ 列表操作")
    
    # 集合操作
    conn.sadd("test:set", "x", "y", "z")
    assert conn.scard("test:set") == 3
    print("✓ 集合操作")
    
    # 哈希操作
    conn.hset("test:hash", "field1", "value1")
    assert conn.hget("test:hash", "field1").decode() == "value1"
    print("✓ 哈希操作")
    
    # 使用get_redis_connection
    conn2 = get_redis_connection()
    conn2.incr("test:counter")
    assert int(conn2.get("test:counter")) >= 1
    print("✓ get_redis_connection")


# ========== 测试辅助函数 ==========

def setup_test_data():
    """创建测试数据的辅助函数"""
    class TestCustomer(HashModel, index=True):
        name: str
        email: EmailStr
        age: int
    
    Migrator().run()
    
    # 清理旧数据
    old_data = TestCustomer.find().all()
    for item in old_data:
        item.delete()
    
    # 创建新数据
    data = [
        TestCustomer(name="Alice", email="alice@test.com", age=25),
        TestCustomer(name="Bob", email="bob@test.com", age=30),
        TestCustomer(name="Charlie", email="charlie@test.com", age=35),
    ]
    for item in data:
        item.save()
    
    return TestCustomer, data


def cleanup_test_data(ModelClass):
    """清理测试数据的辅助函数"""
    items = ModelClass.find().all()
    for item in items:
        item.delete()


# ========== 使用示例 ==========
"""
快速开始：

1. 基础测试:
   test_redis_om_quick()

2. 完整测试:
   test_redis_om_comprehensive()

3. 特定功能测试:
   test_validation_only()
   test_queries_only()
   test_embedded_only()
   test_redis_commands_only()

4. 自定义测试:
   from your_module import test_redis_om_comprehensive
   test_redis_om_comprehensive()
"""
