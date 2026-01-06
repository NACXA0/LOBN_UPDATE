# ORM表模型
# 注意！一个表只能被实例化一次。
'''
缩写对应表：
缩写：biz  全称：business     含义：业务
缩写：org  全称：organization 含义：组织
缩写：2    全程：to           含义：与……对应

例外：
identity不可简写为id，因为id通常代表编号(此外还是内置变量)，这里身份统一用identity。


- 完全等效：level = privilege_level    命名有区别只是为了命名便于理解，实质都是不同的权限组合。
    - level与level的区别：
        1. level是业务层面的，level(更易于理解,更加灵活)与实际权限之间隔着一层 ‘vip等级与权限配置的对应表’ 这个表是随业务变化的，可由超级管理员设置。
        2. level、privilege_level(更加复杂,但更精细)直接代表实际权限(辅佐以privilege_select加以说明)，除非修改底层代码否则不可更改.
    - privilege_level的权限表：    禁用：不可登录、不可见、不可使用
      0. 0禁用但保留
      1. 1注册成功但未通过必要审核，禁用——与0的区别在于这里在审核处要检索。
      2. 2注册成功但未通过必要审核，仅基本使用
      10. 10正常基本使用
'''
from typing import List, Optional
import rxconfig, uuid, datetime
from sqlmodel import Field, Relationship, SQLModel, Column, ARRAY, TEXT, UUID, String, JSON, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from decimal import Decimal
from uuid_extensions import uuid7, uuid7str

'''示例：
模块作用：
调用文件：
'''


class 这个实例化的模块的命名(SQLModel, table=True):
    __table_args__ = {"schema": "数据库里的架构名"}  # 必须
    __table_name__ = "数据库里的表名"  # 必须
    # 下面是需要的列   必须
    id: int | None = Field(default=None, primary_key=True)
    uuid: uuid.UUID  # UUID的数据类型是 uuid.UUID 需要导入库：uuid
    name: str
    money: Decimal = Field(decimal_places=6)  # max_digits最多可以有数字位数(6位)  decimal_places最多小数位数   注意：mon
    change_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    org_base: List[str] = Field(default=None, sa_column=Column(ARRAY(String())))  # 数组内含字符串的映射方法
    一对多中的多: str = Field(default=None,
                              foreign_key="表名.字段")  # 外键：一对多  （多对多使用关联表）  问题：如果外键关联的表，取决于关联表里的另一个字段（通过类型字段判断这个id是哪张表里的id），这个就有点复杂了
    jsonb: dict = Field(default=None, sa_type=JSON)  # jsonb格式的数据 {'name':'姓名str(加盐密码A)', 'id_card':'身份证号str(加盐密码B)'}
    phone_number: str = Field(unique=True)  # 唯一约束，使得此字段数据不能有重复（允许多个null值）
    示例表2属性名: list["示例表2"] = Relationship(
        back_populates="示例表1属性名")  # 关系：# 单向关系则不需要back_populates    # List["对方表"] 【注意引号】 对方表是“多”， 对方有多个对应结果， 用    List["对方表名"]


class 示例表2(SQLModel, table=True):
    __table_args__ = {"schema": "数据库里的架构名"}  # 必须
    __table_name__ = "数据库里的表名2"  # 必须
    # 下面是需要的列   必须
    id: int | None = Field(default=None, primary_key=True)
    外键_表1id: int | None = Field(default=None,
                                   foreign_key="数据库里的架构名.示例表1.id")  # 注意！有关系字段的情况下，外键要用完整路径（宽泛到架构名）（foreign_key="架构名.表名.字段名"），因为关系需要参考定义的外键，关系会在ORM程序内分析，这里收到python上下文的约束（join不用，因为一ing定义的__table_args__ = {"schema": "public"}直接给数据库处理，数据库没有python这里的上下文限制）
    示例表1属性名: 这个实例化的模块的命名 | None = Relationship(back_populates="示例表2属性名")  # 关系：通常名称加前缀 teble_
    # 关系的使用方式
    # 对方的名字  | None
    # 对方表是“一”， 对方只有一个对应结果， 用    对方表名 | None
    # 对方表是“多”， 对方有多个对应结果， 用    List[对方表名]
    # back_populates="我的反向关系在另一个模型里的属性名"
    #  单向关系则不需要back_populates
    # 何时对方的表名需要加引号：上下文再前面的加，在后面的不加。
    # 前文："Team" | None  后文：list[Hero]
    # 前文：list[Hero] 后文："Team" | None
    # 外键与关系：
    # 关系依赖外键工作：关系建立在外键的基础之上。
    # 外键：需要在数据库层面强制保证引用完整性（没有自动同步）【数据库层】
    # 优点：方便地在两个实体之间导航和访问【应用层】
    # 自动填充：ORM层面自动同步外键的修改
    # 使用原外键的功能更方便，不用再join了：关系表字段.字段
    # 一对多、多对多应该用关系
    # 可以单向，但通常双向。
    # 双向加back_populates="对方的属性名"， 单项不加。
    # 延迟加载：
    # 优点：节省初始查询的资源，只加载你需要的数据。
    # 缺点：在循环中访问关系属性时，会触发臭名昭著的 N+1 查询问题。
    # 这就是为什么 .options(selectinload(...)) 如此重要的原因。
    # 查询多结果直接用遍历：
    # 从一个表的结果获取另一个表的结果：直接遍历，不会导致数据库多次查询。
    # A、B有关系 -> A结果列表 -> 直接遍历A获取 A.B关系字段 -> 本地内存，与数据库无关
    # 基于外键的join仍然有用：
    # 1. 关系底层也是join，join是直接面向数据库的
    # 2. 过滤/聚合数据：可以基于两个表的任何字段进行 WHERE, ORDER BY, GROUP BY 等操作
    # 关系的用法：
    # 创建和更新：
    # 读：session.exec(select(本表名).options(selectinload(本表名.关系字段))).first().关系字段  # 最后的 .关系字段 是关键，不加不在结果显示，加了的时候会进行检索
    # 加这个的作用 .options(selectinload(本表名.关系字段))
    # 立即加载相关数据，而不是延迟加载。这可以减少查询次数，提高性能。
    # 需要导入：from sqlalchemy.orm import selectinload


'''
通用字段示例：

权限: 优先遵从权限配置，而后遵从权限等级

privilege_level     (权限等级)
含义：不同等级代表着不同的权限配置模板【以后再做】【权限配置模板还没做】

privilege_select    (权限配置)【可改进】以后可以改为子表，做一个联查来加速查询
权限配置的结构：
    1. 键为权限内容
    2. 值的数据类型是bool，只有三种形式True(具有此权限)、False(无此权限)、None(交由权限等级判断)
    {
        'approve_creat_org': true,  # 审核创建组织的权限：有           python类型：True
        'approve_creat_identity': false,    # 审核创建组织的权限：无   python类型：False
        'X': null  # 权限X：交由权限等级判断       python类型：None
    }

'''

# ----------------------------------------------------------------------------------------
# region 用户表
'''
用户表
'''


class user(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "user"  # 必须
    # 下面是需要的列   必须
    uuid: str = Field(default_factory=uuid7, primary_key=True)  # 【不用uuid.UUID是因为state的var不支持uuid】【创建新行时，这里生成uuid】主键由数据库管理，为确保唯一性一般不由代码设置. 这里除外，因为代码生程uuid更快。主键生成时会检测唯一性。
    name: str
    phone_number: str = Field(unique=True, index=True)  # 唯一约束
    money: Decimal = Field(default=0, decimal_places=6)  # max_digits最多可以有数字位数(6位)  decimal_places最多小数位数   注意：mon
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    last_login_date: str  # 最后登录时间
    level: int = Field(default=0)  # 个人VIP等级   0为无vip
    privilege_level: int = Field(default=10)  # 用户等级   直接代表实际权限    10为正常  0为禁用但保留  其他见readme.md
    privilege_select: dict = Field(default=rxconfig.user.default_user_signin_privilege_select, sa_type=JSON)  # 权限详细配置，用于权限管理，覆盖权限等级预设的权限。  None为无特殊权限覆盖，完全遵从权限等级预设。
    real_man_verify_info: dict = Field(default=None, sa_type=JSON)  # 实人认证信息 {'name':'姓名str(加盐密码A)', 'id_card_number':'身份证号str(加盐密码B)'}
