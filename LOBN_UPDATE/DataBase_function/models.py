# ORM表模型
# 注意！一个表只能被实例化一次。

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
    一对多中的多: str = Field(default=None, foreign_key="表名.字段")  # 外键：一对多  （多对多使用关联表）  问题：如果外键关联的表，取决于关联表里的另一个字段（通过类型字段判断这个id是哪张表里的id），这个就有点复杂了
    jsonb: dict = Field(default=None, sa_type=JSON)  # jsonb格式的数据 {'name':'姓名str(加盐密码A)', 'id_card':'身份证号str(加盐密码B)'}
    phone_number: str = Field(unique=True)  # 唯一约束，使得此字段数据不能有重复（允许多个null值）
    示例表2属性名: list["示例表2"] = Relationship(back_populates="示例表1属性名")  # 关系：# 单向关系则不需要back_populates    # List["对方表"] 【注意引号】 对方表是“多”， 对方有多个对应结果， 用    List["对方表名"]


class 示例表2(SQLModel, table=True):
    __table_args__ = {"schema": "数据库里的架构名"}  # 必须
    __table_name__ = "数据库里的表名2"  # 必须
    # 下面是需要的列   必须
    id: int | None = Field(default=None, primary_key=True)
    外键_表1id: int | None = Field(default=None, foreign_key="数据库里的架构名.示例表1.id")  # 注意！有关系字段的情况下，外键要用完整路径（宽泛到架构名）（foreign_key="架构名.表名.字段名"），因为关系需要参考定义的外键，关系会在ORM程序内分析，这里收到python上下文的约束（join不用，因为一ing定义的__table_args__ = {"schema": "public"}直接给数据库处理，数据库没有python这里的上下文限制）
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


'''
通用界面配置表
这里存储页面的公共配置数据，前端每次加载和后台修改配置都触发查询。
极高频读，极低频写。
'''
class page_config(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "page_config"  # 必须
    # 下面是需要的列   必须
    uuid: str = Field(default_factory=uuid7, primary_key=True)  # 页面的uuid
    data: dict = Field(default=None, sa_type=JSON)  # 页面配置，jsonb格式存储    
    page_name: str = Field(unique=True)  # 页面名称，唯一约束. 不强制，更多是为了方便查询，每个页面都要有唯一的uuid
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")) # 此配置的创建时间
    create_user: str = # 创建词条数据的人



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
    privilege_select: dict = Field(default=rxconfig.user.default_user_signin_privilege_select, sa_type=JSON)  # 权限详细配置，用于权限管理，覆盖权限等级预设的权限。  None为无特殊权限覆盖，完全遵从权限等级预设。
    real_man_verify_info: dict = Field(default=None, sa_type=JSON)  # 实人认证信息 {'name':'姓名str(加盐密码A)', 'id_card_number':'身份证号str(加盐密码B)'}


'''
用户登录历史记录
只做存档，没有功能 ！只写入，不修改
action行为：登录为True；注销为False
'''
class user_login_history(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "user_login_history"  # 必须
    # 下面是需要的列   必须
    uuid: str = Field(default_factory=uuid7, primary_key=True)
    user_uuid: str  #用户uuid
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    action: bool    #用户行为：登录为True；注销为False
    ip: str    #IP地址




# region 组织表
'''
组织表——如：基地、企业、院校的统称。

config:
    身份加入组织时是否需要申请:
    # 【被org2identity_type_name的第一个参数等效代替】 default_signup_org2identity_type_name   默认身份注册到组织时，身份在组织中的岗位的名称。【应为org2identity_type_name已存在的名称】
'''
class org(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "org"  # 必须
    # 下面是需要的列   必须
    uuid: str = Field(default_factory=uuid7, primary_key=True)
    org_type: str  # 组织类型  基本类型: 基地(base)、企业(company)、院校(school)  附属类型:班级(class)
    url_name: str = Field(default=None, unique=True) #【唯一】【可选】 url别名，如果设置了，可以通过别名访问。含义与uuid相同，是更简单的方法，去别的别名可以更改，面向啊你给外部，而uuid不可更改，面向内部。
    extra_data_uuid: str  # 附加字段表的数据的uuid
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    change_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    last_login_date: str    # 最后管理员登录时间
    owner_user_uuid: str  # 拥有此组织的用户的uuid（确定且唯一）
    super_admin_user_uuid: str  # 超管用户的uuid（确定且唯一）
    name: str
    level: int = Field(default=0)   # 组织的vip等级   0为无vip
    privilege_select: dict = Field(default={}, sa_type=JSON)  # 同一职位内部的权限详细配置，用于权限管理，覆盖权限等级预设的权限。  None为无特殊权限覆盖，完全遵从权限等级预设。
    new_message_uuid: List[str] = Field(sa_column=Column(ARRAY(Text)))  # 未读的私信
    plug_component_foreach: list = Field(sa_type=JSON, default=[])  # 插件名称及其排版——用于foreach  这里的 default=[] foreach需要数组
    WebPageSet_index: dict = Field(sa_type=JSONB)   # 【需要改动】组织首页页面设置
    tip: str  # 说明（详细简介）——展示在详细信息
    slogan: str  # 标语——简要简介（一句话）——展示在组织卡片中
    affiliated_org_tag: dict = Field(default=None, sa_type=JSON)    # 附属组织的标签分类结构 {'一级分类1': {uuid:'', 'description': '描述', 'children': ['二级分类1':'']}， '一级分类2':{uuid:'', 'description': '描述', 'children': }}     1. 为什么仍需要uuid: 全局唯一性，使得上下级组织关系表可以遍历索引。2。为什么不用后面将uuid放到前面的方式: 名称作为键，利用字典键唯一的属性防止标签名重复  {uuid: {'description': '描述-一级分类1', 'children': [uuid:{'description': '描述-二级分类1', 'children': {}}]}， uuid:{'description': '描述-一级分类2', 'children': {}}}
    config: dict = Field(default={}, sa_type=JSON) # 设置。组织的设置信息。   与privilege_select不同，这里更由组织自己控制。
    config_org2identity_type_name: List[str] = Field(default=rxconfig.config_org_identity.org2identity_type_list, sa_column=Column(ARRAY(Text)))  # 配置的身份在组织中的岗位名称，这个太常用所以单独一个字段。


'''
组织与身份的关联表——身份在组织中的注册信息
'''
class org_map_org2identity(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "org_map_org2identity"  # 必须
    # 下面是需要的列   必须
    org_uuid: str = Field(default=None, foreign_key="public.org.uuid", primary_key=True)    # 组织的uuid
    identity_uuid: str = Field(default=None, foreign_key="public.identity.uuid", primary_key=True)  # 身份uuid
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    change_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    last_login_date: str  # 最后登录时间
    level: int = Field(default=0)  # 【正整数】当前此组织的身份的vip等级   0为无vip
    type: str = Field(default='')   # 身份在组织内的的特殊职位列表,  是组织对身份的定义。
    privilege_level: int = Field(default=10)    # 用户等级   直接代表实际权限    10为正常  0为禁用但保留 其他见readme.md
    privilege_select: dict = Field(default={}, sa_type=JSON)  # 同一职位内部的权限详细配置，用于权限管理，覆盖权限等级预设的权限。  None为无特殊权限覆盖，完全遵从权限等级预设。
    name: str   # 名称(主要用于展示)
    tip: str = Field(default='')    # 说明 一般是等于身份的名称
    WebPageSet_space: dict = Field(sa_type=JSON)   # 个人主页设置
    tag_in_org: List[str] = Field(sa_column=Column(ARRAY(Text))) # 身份在组织中的标签 用于组织对组织内的人员管理   如：班级A、小组B
    money: Decimal = Field(default=0, decimal_places=0) # 积分——仅限此身份注册信息在此组织中使用

'''
中间表: 组织之间的上下级关系
'''
class org_map_relation(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "org_map_relation"  # 必须
    # 下面是需要的列   必须
    master_org_uuid: str = Field(default=None, foreign_key="public.org.uuid", primary_key=True)    # 上级组织的uuid
    slave_org_uuid: str = Field(default=None, foreign_key="public.org.uuid", primary_key=True)  # 下级组织的uuid
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    change_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    privilege_select: dict = Field(default={}, sa_type=JSON)  # 权限详细配置，用于权限管理，覆盖权限等级预设的权限。  None为无特殊权限覆盖，完全遵从权限等级预设。
    #【停用，可能与tag_for_slave_org冲突】type: str   # 下级的职位类型，对于上级而言的
    tag_for_slave_org: List[str] = Field(sa_column=Column(ARRAY(Text)))  # 上级对下级的标签  存储org标签分类中的uuid， 如果找不到对应的分类(数据一致性错误)说明上级组织已经删除了此标签，则不显示标签。
    tag_for_master_org: List[str] = Field(sa_column=Column(ARRAY(Text)))  # 下级对上级的标签 这个是比较独立的，与上级组织无关。存储标签字符串列表['标签1', '标签2']
    tip: str  # 说明（详细简介）
    slogan: str  # 标语——简要简介（一句话）



# region 身份表——合师与会员、运维(管理)、助教等等各种身份，包含身份附加字段，如果需要。
'''
身份表：用户与身份 的关系映射表  一对多
对于不同身份的特异话：用外键join进来
更改：身份属于自然人，与用户一样样是自然人，身份与用户是一对多的关系，一个用户可以具有很多身份，但一个身份只能对应一个用户（如果要转移用户资产则需要转移数据（不常用））。
如果用户注销了此身份，但仍有资产：资产所有者变更为系统暂存。
如果用户建立了新账号：用什么方法将资产转移过去。
多账号共有一个身份的资产：不支持。只可以有一个资产所有者和多个资产管理员（防止资产纠纷）
- privilege_select解释
    'web_privilege': None  网站系统权限类型，默认是没有网站系统管理权

'''
class identity(SQLModel, table=True):
    __table_args__ = {"schema": "public"}  # 必须
    __table_name__ = "identity"  # 必须
    # 下面是需要的列   必须
    uuid: str = Field(default_factory=uuid7, primary_key=True)  # 此关系本身的uuid
    type: str  # 身份类型     管理(admin),运维(service)教师(teacher),学生(vip)       对于网站系统而言
    create_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    change_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
    last_login_date: str  # 最后登录时间
    user_uuid: str = Field(default=None, foreign_key="public.user.uuid")    # 用户的uuid
    name: str
    level: int = Field(default=0)   # vip等级   0为无vip
    privilege_select: dict = Field(default={}, sa_type=JSON)  # 此身份的基础权限配置，用于权限管理，覆盖权限等级预设的权限。  None为无特殊权限覆盖，完全遵从权限等级预设。
    tip: str = Field(default='')    # 说明 一般是等于name
    slogan: str  # 标语——简要简介（一句话）——展示在身份卡片中





