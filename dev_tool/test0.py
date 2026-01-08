import rxconfig
import uuid, itertools, time, datetime, random, ast, calendar, #redis, asyncio, queue
from typing import List, Union, Tuple, Callable, AsyncGenerator, Dict, Any
from sqlmodel import Session, select, update, func, or_, outerjoin, and_, exists, not_
from LOBN_UPDATE.DataBase_function.database import engine
from LOBN_UPDATE.DataBase_function.models import user, org, org_map_org2identity, identity
from concurrent.futures import ThreadPoolExecutor
#from LOBN_UPDATE.public_function import trim_datetime_range, yield_on_datetime_index, search_org_O2I_identity_by_user_groupby_org, search_org_by_user, replace_dictA_value_through_dictB, replace_privilege_null_according_to_privilege_level
from uuid_extensions import uuid7, uuid7str
#from collections import defaultdict
#from dataclasses import dataclass, astuple
#import pandas as pd


def print_info():
    print('UUID7:', uuid7str())
    print('DateTimeNow:', datetime.datetime.now())






def join_test():
    with Session(engine) as session:
        # 1. 找出中间表所有拥有的基地
        command = select(org_map_user2org_base, org_base.name).join(org_base).where(
            org_map_user2org_base.user_uuid == uuid.UUID('0676d2d6-acc8-7abd-8000-114f9774296b'))
        info_list = session.exec(command).all()
        print('DDD', len(info_list), info_list)
        # 3. 构造信息（为了foreach）
        foreach_list = []
        for info in info_list:
            print('BBB', info)
            # print('CCC', info[1])
            # foreach_list.append({
            #    "identity_uuid": str(info.map_user2identity.identity_uuid),
            #    "post": str(info.map_user2identity.post),
            #    "name": str(info.org_base.name),
            # })

        # print('AAA', foreach_list)


def test_change_jsonb():
    '''
  {
    "head_notice": [
      "第一条公告",
      "第二条公告"
    ],
    "test_change":"abc"
  }
    '''
    # 测试sqlmodel可不可以直接更改JSON B的某参数的值？
    with Session(engine) as session:
        # 1. 找出中间表所有拥有的基地
        command = select(main_web_page_set).where(main_web_page_set.page == '/index')
        info_list = session.exec(command).first()
        # print('AAAAA', info_list)
        # 1. 将json转为字典
        x = dict(info_list.value)
        # print('BBBBB', x)
        # 2. 更改字典
        # x["head_notice"].append('第三条公告')
        # x['test_change'] = 'yuioyuio'
        # print('CCCCCC', x)
        # 3. 将字典赋值给json
        info_list.value = x
        # print('DDDDD', info_list)
        session.commit()


def test_change_org_base_index_head_notice():
    # 测试修改基地组织的首页公告内容
    # 结论： 不指定的情况下是表对象修改；指定具体字段的情况下，是对值的直接修改。只有对表对象的修改是有效的【select多列也不行，必须是整个表】。   sqlarchemy可能可以，但还没式成
    '''
    当前json备份：
    {
  "说明": [
    "head_image:首图轮播图路径",
    "head_notice:首条轮播公告内容"
  ],
  "head_image": [
    "/image/logo_DaNa.jpg",
    "/image/police_record.png"
  ],
  "head_notice": [
    "第一条公告",
    "第二条公告"
  ]
}
    '''
    with Session(engine) as session:
        command = select(org_base).where(org_base.name == 'name_base2')
        info_data = session.exec(command).first()
        x = dict(info_data.WebPageSet_index)
        print('AAAAA', type(x), x)
        x['test'] = 'cvbn'
        print('BBBBB', type(x), x)
        info_data.WebPageSet_index = x
        session.add(info_data)
        session.commit()
    # 这样可以
    # with Session(engine) as session:
    #    command = select(table)
    #    info_data = session.exec(command).first()
    #    info_data.item = {'test': 'abcd'}
    #    session.commit()
    # 这样不行
    # with Session(engine) as session:
    #    command = select(table.item)
    #    info_data = session.exec(command).first()
    #    info_data = {'test': 'abcd'}
    #    session.commit()
    # 下面是还没试成功的sqlarchemy方法   可能可以
    # with Session(engine) as session:
    #    command = (
    #        update(org_base)
    #        .where(org_base.name == 'name_base2')
    #        .values(WebPageSet_index={'test': 'tyui', '说明': ['head_image:首图轮播图路径', 'head_notice:首条轮播公告内容'], 'head_image': ['/image/logo_DaNa.jpg', '/image/police_record.png'], 'head_notice': ['第一条公告', '第二条公告']})
    #    )
    #    session.exec(command).first()
    #    session.commit()


def test_switch_list2str():
    x = "['第一条公告', '第二条公告', '3333333']"
    x = input('输入列表：')
    y = ast.literal_eval(x)
    print(type(y), y)


def make_an_appointment():
    # 约时间测试
    with Session(engine) as session:
        command = select(product_make_an_appointment_event)
        info_data = session.exec(command).first().periods
        print('AAAAAA', type(info_data), info_data)


def test_calendar():
    # import calendar
    print(calendar.prmonth(2024, 7))


# @numba.jit(nogil=False) numba可以加速计算，需要安装numba
def test_calculate_pi(start: int, end: int) -> float:
    '''
    计算圆周率 pi = 4(1 - 1/3 + 1/5 1/7 + 1/9 -1/11 + ...)
    '''
    result = 0.0
    positive = True
    n = 1
    for i in range(start, end):
        tmp = 1.0 / float(i * 2 + 1)
        if positive:
            result += tmp
        else:
            result -= tmp
        positive = not positive
        # print('轮：', n, '值：', result)
        # n += 1
    result = 4.0 * result
    print(result)
    return result


def test_calculate_week():
    num = calendar.monthrange(datetime.datetime.now().year, 3)[1]  # 获取本月天数
    print(num)
    week_num = 4 if (num / 7) == 4 else 5  # 得知本月共有几周
    print(week_num)
    # 获取当前是本月的第几周
    week_number = ((datetime.date.today().day + datetime.date(datetime.date.today().year, datetime.date.today().month,
                                                              1).weekday()) // 7) + 1  # 计算当前是本月的第几周
    print(f"当前是本月的第{week_number}周")


def test_datetime():
    '''
    生成某某时间（以当前时间为基础）
    replace制定某事件为某某，此外都是当前时间

    strptime 字符串转换为datetime
    精确到某某时，小时、分钟、秒、微秒自动为0
    不精确到某某时，最不精确为年。最不精确为1900-1-1 00：00:00
    '''
    # 下面是生成某某时间
    x = datetime.datetime.now().replace(year=2025, month=2, day=10, hour=15, minute=30, second=0, microsecond=0)
    print(str(x))
    xa = datetime.datetime.now().replace(year=2025, month=2, day=10)
    print(str(xa))
    xb = datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
    print(str(xb))
    # 下面是字符串转datetime
    y = datetime.datetime.strptime('2025-02-09-15:30:00', '%Y-%m-%d-%H:%M:%S')  # 普通
    print(type(y), y)
    ya = datetime.datetime.strptime('2025-02-09', '%Y-%m-%d')  # 精确到某某
    print(type(ya), ya)
    yb = datetime.datetime.strptime('15:30:00', '%H:%M:%S')  # 不精确到某某
    print(type(yb), yb)
    # 下面是rx.calendar接受的字符串
    print(datetime.date.today())
    print(datetime.date(year=2099, month=12, day=31).strftime("%a %b %d %Y"))
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    formatted_date = tomorrow.strftime("%a %b %d %Y")
    print(formatted_date)


def test_time_unit():
    '''
    通过函数match，来判断元组(time_unit)中满足条件的元素，然后将这些元素对应的变量的值设置为True，其他的都设置为False。使用map，不使用遍历
    '''
    detail_round: list[int | float] = [2, 6]  # 测试
    time_unit = ("年", "季", "月", "周", "日", "时", "分", "秒")

    will_open_time_unit: set[int] = set()  # 集合 类似于列表，但 1.无序 2. 每个元素只能有一个

    def match_unit(detail_round: int, switch_on: bool):
        match detail_round:  # 做到这里了，这里是控制下面精确选时间的输入方式是否存在，以及如果存在日历的话日历显示的最模糊的时间细节。 这里做完后要用此对下面选择的时间进行“修整”，然后就是存储了。
            case 0:  # 年 最模糊是否等于年就足够了
                self.open_self_define_event_day = switch_on
                will_open_time_unit.add(0)
                # self.self_define_event_calendar_max_detail = 'year'
            case 1:  # '季'   #不存在->异化为3月：实际修约间隔*3
                self.open_self_define_event_day = switch_on
                # self.self_define_event_calendar_max_detail = 'month'
                will_open_time_unit.add(1)
            case 2:  # '月'
                self.open_self_define_event_day = switch_on
                # self.self_define_event_calendar_max_detail = 'month'
                will_open_time_unit.add(2)
            case 3:  # '周'   #不存在->异化为7日：实际修约间隔*7
                self.open_self_define_event_day = switch_on
                # self.self_define_event_calendar_max_detail = 'day'
                will_open_time_unit.add(3)
            case 4:  # '日'
                self.open_self_define_event_day = switch_on
                will_open_time_unit.add(4)
            case 5:  # '时'
                self.open_self_define_event_hour = switch_on
                will_open_time_unit.add(5)
            case 6:  # '分'
                self.open_self_define_event_minute = switch_on
                will_open_time_unit.add(6)
            case 7:  # '秒' 最精确是否等于秒就足够了
                self.open_self_define_event_second = switch_on
                will_open_time_unit.add(7)
            case _:
                ValueError('程序错误！')

    map(match_unit, tuple(range(detail_round[0], detail_round[1] + 1)))  # 1. 替换为True操作 2. 收集已经替换为True的变量
    will_open_time_unit: set = {0, 1, 2, 3, 4, 5, 6, 7} - will_open_time_unit  # 计算出未出现的变量的索引，
    # 按照索引，将未出现过的变量设置为False


def redis_R_W():
    '''redis简单读写'''
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # 测试连接是否成功
    print(redis_client.ping())

    # 设置键值对
    redis_client.set('key', 'value')
    # 获取键对应的值
    value = redis_client.get('key')
    print(value)  # 输出 b'value'，b 前缀表示字节字符串


# redis发布订阅，约时间系统到时间提示的整体架构逻辑
async def redis_pub_sub():
    '''
    redis的发布订阅测试

    各个系统的redis实现（以后转为消息队列）：
    1. 生命周期任务创建redis实例。 每一个服务都有单独的频道（随事件创建实例需要一个时间间隔）
    2. 所有用户在登录时创建所有服务的redis监听(频道)，监听属于自己的消息。
    3. 当有消息时（对应服务的频道）发布消息给对应用户（频道名用用户uuid标识）
    4. 用户在对应服务的实例中收到消息并解析消息内容。  （需要解析以及会包含不需要的信息，这效率确实不高，以后转为消息队列实现）
    '''

    # 在服务器启动时创建实例【rxconfig里】
    pubsub_user = redis.asyncio.Redis.from_url("redis://localhost:6379")  # 用户用的实例
    pubsub_server = redis.asyncio.Redis.from_url("redis://localhost:6379")  # 服务器用滚动实例

    # 激活并创建实例（在function里， 被生命周期触发）
    async def activate_redis_pubsub():
        try:
            # 激活连接（通过 ping 方法）
            result_user = await pubsub_user.ping()
            result_server = await pubsub_server.ping()
            print(f"连接成功: {result_user}和{result_server}")
        except ConnectionError as e:
            print(f"连接失败: {e}")
        finally:
            # 关闭连接
            await result_user.close()
            await result_server.close()

    # 定义接收redis订阅的消息的逻辑（function里）
    async def redis_subscribe(redis_client, channel_name, func):
        """
        订阅频道并监听消息， 对接收到的消息进行某种处理
        :param redis_client redis实例
        :param channel_name 频道名称
        :param func 消息处理函数
        使用方法：
            await asyncio.create_task(subscribe(pubsub_user, 'my_channel', on_message))
            on_message是要对接收到的消息作出的处理。它接收一个参数，这个参数是订阅收到的消息
        """
        while True:  # 添加重试逻辑
            try:
                # 创建发布/订阅对象
                pubsub = redis_client.pubsub()
                await pubsub.subscribe(channel_name)

                print(f"订阅者已连接到频道: {channel_name}")

                # 监听频道消息
                async for message in pubsub.listen():
                    if message["type"] == "message":  # 只处理普通消息
                        func(message)
            except ConnectionError as e:
                print(f"连接中断: {e}，尝试重新连接...")
                await redis_client.close()  # 关闭旧连接
                await asyncio.sleep(1)  # 等待一段时间后重试

    # 定义要对接收到的消息作出的处理【被登录里的启动订阅者逻辑触发】（basestate中）
    def route_redis_channel_message(message):
        '''
        接收redis里属于自己的消息并路由
        :param message: redis频道订阅收到的消息
        '''
        print(f"收到消息: {message['data'].decode('utf-8')}")  # 临时测试
        match message:
            case 'service1':
                pass
            case 'service2':
                pass
            case _:
                ValueError('程序错误！redis订阅收到的消息都应该注册到这里。')

    # 【以后给消息队列做】启动心跳倒计时，到时间主动请求一次延时，否则被关闭频道、断开连接。【登陆后自动触发】（后台任务）    # await pubsub_user.close()

    # 启动订阅者：开始对接收到的消息作出处理（业务逻辑中）
    await asyncio.create_task(redis_subscribe(pubsub_user, 'my_channel', route_redis_channel_message))

    await asyncio.sleep(2)  # 测试用的延时

    # 发布消息（业务逻辑中）
    pubsub_server.publish('my_channel', "message")
    # 关闭，如果需要
    # await pubsub_server.close()


# redis 发布——用于测试系统内的订阅
async def redis_pub():
    message = 'test_pub'
    await rxconfig.REDIS.redis_client_pubsub_server.publish('0676d2d6-acc8-7abd-8000-114f9774296b',
                                                            message)  # 向redis发布消息


# 写入时间到数据库，然后读取接下来一个小时的时间，然后在到时间的时候输出
def test_write_db_time_then_yield_on_time_of_near_hour():
    # 辅助测试：存入一个即将到时间的数据
    with Session(engine) as session:
        # 合并datetime时间列表中连续的时间 然后 遍历解析合并连续时间后的datetime列表
        append_time_range_note = []  # append_time_range_note:添加了的时间——用于最后的提示
        l = [
            (datetime.datetime.now() + datetime.timedelta(seconds=10),
             datetime.datetime.now() + datetime.timedelta(seconds=30)),
            (datetime.datetime.now() + datetime.timedelta(seconds=15),
             datetime.datetime.now() + datetime.timedelta(seconds=55)),
            (datetime.datetime.now() + datetime.timedelta(seconds=30),
             datetime.datetime.now() + datetime.timedelta(seconds=90))
        ]
        for time_range in l:
            command = product_make_an_appointment_time(
                user_uuid='0676d2d6-acc8-7abd-8000-114f9774296b',
                event_uuid='067b5b21-eea9-7ae1-8000-bdd1ab7abbe3',
                start_date=time_range[0].strftime("%Y-%m-%d %H:%M:%S"),
                end_date=time_range[1].strftime("%Y-%m-%d %H:%M:%S"),
                tip='test'
            )
            session.add(command)
        session.commit()

    # 检索出接下来1个小时的可能发生的到时间事件， 暂时存入列表，以后改为用rabbitmq
    near_future_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    with Session(engine) as session:  # 1. 未来：结束时间大于现在 2. 一个小时内将开始：开始时间小于未来一个小时
        command = select(product_make_an_appointment_time).where(
            product_make_an_appointment_time.end_date > datetime.datetime.now()).where(
            product_make_an_appointment_time.start_date < near_future_time)
        near_future_data = session.exec(command).all()  # 找到的数据

    print('TIME:', near_future_time)
    print(type(near_future_data), near_future_data)

    # 运行

    async def main():
        async for index in yield_on_datetime_index(tuple((i.start_date, i.end_date) for i in near_future_data)):  # 后台任务
            print(index)
            print(
                f'时间：{str(near_future_data[index].uuid)}到时间了。注释：{near_future_data[index].tip}，开始时间：{str(near_future_data[index].start_date)}, 结束时间：{str(near_future_data[index].end_date)}')

    asyncio.run(main())


# 【暂停】以后再复盘——约时间系统的测试
class test_last_make_an_appointment:
    '''
    暂停前最后的约时间系统的测试
    测试按列表时间的元素输出，并可接受十时传入的数据，也按时输出
    这个还有问题，不能达到理想的情况：现在插入的时间不能按时输出
    '''
    import threading

    async def gen_get_list(l):
        '''
        接收一个列表l，会按照列表l按时输出元素。
        同时，当列表l新增元素（将会在外部向l添加l2），可以及时感知到，并同样按时间输出。
        :param l: 原始时间列表
        '''
        index = 0
        while True:
            # 检查索引是否超出当前列表长度
            while index < len(l):
                # 按列表元素的值休眠相应秒数
                await asyncio.sleep(l[index])
                # 生成当前元素
                yield l[index]
                index += 1
            # 如果没有新元素，短暂休眠后继续检查
            print('休眠1秒等待列表出现新元素')
            await asyncio.sleep(1)

    # 多线程向列表添加
    def append_threading(l, l2):
        '''
        多线程向列表添加（模拟reflex
        :param l: 原始列表
        :param l2: 要添加的元素的列表
        '''
        for i in l2:
            l.append(i)
            print(f'多线程向列表添加了元素:{i}')

    async def main(self, l, l2):
        iter_gen = self.gen_get_list(l)
        while True:
            next_var = await anext(iter_gen)
            print(next_var)
            # await asyncio.sleep(1)

    if __name__ == "__main__":
        pass

        # 理想输出： 11，2，3，4，5，66，然后等待30秒结束程序
    #    total_wait_time = 30  # 总等待时间，总时间内的元素都应该被检测到
    #    l = [1, 3, 5, 6]
    #    l2 = [1, 2, 4, 6]
    # 创建线程
    #    thread = threading.Thread(target=append_threading, args=(l, l2))
    # 启动线程
    #    thread.start()

    # 等待线程执行完毕
    # thread.join()

    #    asyncio.run(main(l, l2))

# 测试查询A_A2B_B_C的关系们
def test_search_A_A2B_B_C():
    '''
        class A(SQLModel, table=True):
            id: int = Field(default=None, primary_key=True)

        class A2B(SQLModel, table=True):
            id: int = Field(default=None, primary_key=True)
            aid: int = Field(default=None, foreign_key="a.id")
            bid: int = Field(default=None, foreign_key="b.id")

        class B(SQLModel, table=True):
            id: int = Field(default=None, primary_key=True)
            cid: int = Field(default=None, foreign_key="c.id")

        class C(SQLModel, table=True):
            id: int = Field(default=None, primary_key=True)
        '''
    ''' 完全版简明
        class A(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
    class AA(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)

    class A2B(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        aid: int = Field(default=None, foreign_key="a.id")
        bid: int = Field(default=None, foreign_key="b.id")
    class AA2B(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        aid: int = Field(default=None, foreign_key="aa.id")
        bid: int = Field(default=None, foreign_key="b.id")
    class A2BB(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        aid: int = Field(default=None, foreign_key="a.id")
        bid: int = Field(default=None, foreign_key="bb.id")
    class AA2BB(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        aid: int = Field(default=None, foreign_key="aa.id")
        bid: int = Field(default=None, foreign_key="bb.id")

    class B(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        cid: int = Field(default=None, foreign_key="c.id")
    class BB(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        cid: int = Field(default=None, foreign_key="c.id")

    class C(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
    '''
    pass

# 测试函数search_org_O2I_identity_by_user_groupby_org
def text_search_org_O2I_identity_by_user_groupby_org():
    x = search_org_O2I_identity_by_user_groupby_org(
        '0676d2d6-acc8-7abd-8000-114f9774296b',
        ['uuid', 'name', 'type', 'slogan'],
        ['level'],
        ['uuid', 'type'],
        'base'
    )

    print(type(x[0]['uuid']))
    print(x)




# region 实人认证——跳转支付宝认证
import uuid, logging, rxconfig, traceback
# h5人脸核身-第一步初始化用的
from alipay.aop.api.domain.OpenCertifyIdentifyInfo import OpenCertifyIdentifyInfo
from alipay.aop.api.domain.OpenCertifyMerchantConfigs import OpenCertifyMerchantConfigs
from alipay.aop.api.domain.DatadigitalFincloudGeneralsaasFaceCertifyInitializeModel import DatadigitalFincloudGeneralsaasFaceCertifyInitializeModel
from alipay.aop.api.request.DatadigitalFincloudGeneralsaasFaceCertifyInitializeRequest import DatadigitalFincloudGeneralsaasFaceCertifyInitializeRequest
from alipay.aop.api.response.DatadigitalFincloudGeneralsaasFaceCertifyInitializeResponse import DatadigitalFincloudGeneralsaasFaceCertifyInitializeResponse
# h5人脸核身-第二步进行认证用的
from alipay.aop.api.domain.DatadigitalFincloudGeneralsaasFaceCertifyVerifyModel import DatadigitalFincloudGeneralsaasFaceCertifyVerifyModel
from alipay.aop.api.request.DatadigitalFincloudGeneralsaasFaceCertifyVerifyRequest import DatadigitalFincloudGeneralsaasFaceCertifyVerifyRequest
from alipay.aop.api.response.DatadigitalFincloudGeneralsaasFaceCertifyVerifyResponse import DatadigitalFincloudGeneralsaasFaceCertifyVerifyResponse
# h5人脸核身-第三步查询结果用的
from alipay.aop.api.domain.DatadigitalFincloudGeneralsaasFaceCertifyQueryModel import DatadigitalFincloudGeneralsaasFaceCertifyQueryModel
from alipay.aop.api.request.DatadigitalFincloudGeneralsaasFaceCertifyQueryRequest import DatadigitalFincloudGeneralsaasFaceCertifyQueryRequest
from alipay.aop.api.response.DatadigitalFincloudGeneralsaasFaceCertifyQueryResponse import DatadigitalFincloudGeneralsaasFaceCertifyQueryResponse
class real_man_verify():
    # 注意，有时候手机浏览器直接访问url会报错missing method, 只有将URL转为二维码，然后手机支付宝扫码才行。
    '''H5人脸核身
    client是支付宝通用的初始化内容 在rxconfig里的alipay_client
    使用方法：
        #第一步：获取认证ID
        function_First_Initialize(cert_name: str, cert_no: str, return_url: str) -> certify_id   #cert_name姓名, cert_no身份证, return_url认证完后跳转到哪个url   url要加上http://
        #第二步：进行认证
        Middle_Verify(certify_id: str) -> 字符串的 认证url    浏览器打开跳转支付宝，或者支付宝扫码url的二维码
        #第三步：查询认证结果
        Finally_Query(certify_id: str) -> 字符串 "T" 或 "F"
    '''
    '''ps
    #使用产品： 支付宝的支付宝H5人脸核身--调用起支付宝APP或者扫码调用支付宝APP认证后返回认证结果
    #https://opendocs.alipay.com/open/02zlo5?pathHash=435386db
    #【反例，错误多】python示例： https://opendocs.alipay.com/open/0dozh3
    #注意： 1支付宝账号必须时公司的 2签名用普通接口，新的v3签名不支持python；3只能使用密钥方式，证书方式不支持python（https://opendocs.alipay.com/support/01ravf）

    关于报错： ERROR Error when executing request: Object type <class 'str'> cannot be passed to C code
    好像支付宝给的办法没什么用-因为官方示例都给错了：（ 应该是aes_encrypt_content里改，而不是decrypt
    1. 注意：若直接引用报如下错误，需要对 SDK提供的AES加密工具类代码(alipay/aop/api/util/EncryptUtils.py)中的 iv 做 .encode("utf8") 处理。
    2. 起因：支付宝alipay模块-实人认证
    3. 处理后示例代码：
    def aes_decrypt_content(encrypted_content, encrypt_key, charset):
        encrypted_content = base64.b64decode(encrypted_content)
        iv = '\0' * BLOCK_SIZE
        cryptor = AES.new(base64.b64decode(encrypt_key), AES.MODE_CBC, iv.encode("utf-8"))#对iv做encode("utf8")处理
        content = unpad(cryptor.decrypt(encrypted_content))
        if PYTHON_VERSION_3:
            content = content.decode(charset)
            return content

    def aes_encrypt_content(content, encrypt_key, charset):
        length = None
        if PYTHON_VERSION_3:
            length = len(bytes(content, encoding=charset))
        else:
            length = len(bytes(content))
        padded_content = pad(content, length)
        iv = '\0' * BLOCK_SIZE
        cryptor = AES.new(base64.b64decode(encrypt_key), AES.MODE_CBC, iv.encode('utf-8'))
        encrypted_content = cryptor.encrypt(padded_content.encode('utf-8'))
        encrypted_content = base64.b64encode(encrypted_content)
        if PYTHON_VERSION_3:
            encrypted_content = str(encrypted_content, encoding=charset)
        return encrypted_content
    '''
    '''【相关内容备份】#支付宝通用的初始化内容的备份
    def alipay_init():  #支付宝通用的初始化内容
        # 日志配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            filemode='a', )
        logger = logging.getLogger('')
        # 配置
        alipay_client_config = AlipayClientConfig()
        # 支付宝网关（固定）
        alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
        # APPID 即创建应用后生成
        alipay_client_config.app_id = rxconfig.pay.alipay.app_id
        # AES秘钥,开放平台接口内容加密方式中获取
        alipay_client_config.encrypt_key = rxconfig.pay.alipay.encrypt_key
        # 接口加密方式,目前支持AES
        alipay_client_config.encrypt_type = 'AES'
        # 生成签名字符串所使用的签名算法类型，目前支持 RSA2 算法。
        alipay_client_config._sign_type = 'RSA2'
        # 编码集，支持 GBK/UTF-8
        alipay_client_config.charset = 'utf-8'
        # 参数返回格式，只支持 JSON（固定）
        alipay_client_config.format = 'json'
        # 支付宝公钥
        alipay_client_config.alipay_public_key = rxconfig.pay.alipay.alipay_public_key
        # 开发者私钥，由开发者自己生成。格式:PKCS1
        alipay_client_config.app_private_key = rxconfig.pay.alipay.app_private_key
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
        return client
    '''

    # 下面是函数
    @staticmethod
    def First_Initialize(client, cert_name: str, cert_no: str, phone_no: str = None, return_url: str = 'https://baidu.com', outer_order_no=str(uuid.uuid4()).replace('-', '')):  # 第一步初始化
        '''
        跳转支付宝人脸核身初始化
        :param cert_name: 姓名
        :param cert_no: 身份证号码
        :param return_url:认证成功后需要跳转的地址，一般为商户业务页面；若无跳转地址可填空字符"" 示例：'https://baidu.com'
        :param outer_order_no: 【默认为已配置好的uuid】类似于订单号的32位字母数字组合
        :return:{
            "datadigital_fincloud_generalsaas_face_certify_initialize_response": {
                "code": "10000",
                "msg": "Success",
                "certify_id": "2109b5e671aa3ff2eb4851816c65828f"
            },
            "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
        }
        '''
        # 对照接口文档，构造请求对象
        model = DatadigitalFincloudGeneralsaasFaceCertifyInitializeModel()
        model.outer_order_no = outer_order_no  # 去除横杠的uuid，刚好32位数字字母组合。   官方示例里给的是错误的
        model.biz_code = "FUTURE_TECH_BIZ_FACE_SDK"
        model.identity_param = OpenCertifyIdentifyInfo()  # 这里是子集，需要额外导入包来涵盖他们 这里官方文档是错误的-这样为每一个子集创建sdk的方式的策略太糟糕了。
        model.identity_param.identity_type = "CERT_INFO"
        model.identity_param.cert_type = "IDENTITY_CARD"
        model.identity_param.cert_name = cert_name
        model.identity_param.cert_no = cert_no
        # 【可选-当前未选】（手机号）
        if phone_no:
            model.identity_param.phone_no = phone_no

        model.merchant_config = OpenCertifyMerchantConfigs()
        model.merchant_config.face_reserve_strategy = 'never'  # 是否保存用户照片 never不保存  reserve保存（有保存费）
        model.merchant_config.return_url = return_url

        request = DatadigitalFincloudGeneralsaasFaceCertifyInitializeRequest(biz_model=model)
        request.need_encrypt = True
        response_content = False
        try:
            response_content = client.execute(request)  # 支付宝的SDK大有问题！！！修改了两个错误再：aes_encrypt_content
        except Exception as e:
            logging.error(f"Error when executing request: {e}")
        if not response_content:
            print("failed execute")
        else:
            response = DatadigitalFincloudGeneralsaasFaceCertifyInitializeResponse()
            # 解析响应结果
            response.parse_response_content(response_content)
            if response.is_success():
                # print("请求成功,响应结果--certify_id: " + response.certify_id) #官方示例里的web_url其实是没有的
                return response.certify_id
            else:
                # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
                # print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
                return {"code": response.code, "msg": response.msg, "sub_code": response.sub_code, "sub_msg": response.sub_msg}

    @staticmethod
    def Middle_Verify(client, certify_id: str):  # 第二步开始认证
        '''
        跳转支付宝人脸核身开始认证      需要用支付宝扫码
        :param certify_id: 上一步传下来的certify_id
        :return:{
            "datadigital_fincloud_generalsaas_face_certify_verify_response": {
                "code": "10000",
                "msg": "Success",
                "certify_url": "https://openapi.alipay.com/gateway.do?alipay_sdk=alipay-sdk-java-dynamicVersionNo&app_id=2015111100758155&biz_content=%7B%22certify_id%22%3A%22ZM201611253000000121200404215172%22%7D&charset=GBK&format=json&method=datadigital.fincloud.generalsaas.face.certify.verify&sign=MhtfosO8AKbwctDgfGitzLvhbcvi%2FMv3iBES7fRnIXn%2BHcdwq9UWltTs6mEvjk2UoHdLoFrvcSJipiE3sL8kdJMd51t87vcwPCfk7BA5KPwa4%2B1IYzYaK6WwbqOoQB%2FqiJVfni602HiE%2BZAomW7WA3Tjhjy3D%2B9xrLFCipiroDQ%3D&sign_type=RSA2&timestamp=2016-11-25+15%3A00%3A59&version=1.0&sign=MhtfosO8AKbwctDgfGitzLvhbcvi%2FMv3iBES7fRnIXn%2BHcdwq9UWltTs6mEvjk2UoHdLoFrvcSJipiE3sL8kdJMd51t87vcwPCfk7BA5KPwa4%2B1IYzYaK6WwbqOoQB%2FqiJVfni602HiE%2BZAomW7WA3Tjhjy3D%2B9xrLFCipiroDQ%3D"
            },
            "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
        }
        '''
        # 对照接口文档，构造请求对象
        model = DatadigitalFincloudGeneralsaasFaceCertifyVerifyModel()
        # datadigital.fincloud.generalsaas.face.certify.initialize(H5人脸核身初始化)返回的certify_id
        model.certify_id = certify_id
        request = DatadigitalFincloudGeneralsaasFaceCertifyVerifyRequest(biz_model=model)
        request.need_encrypt = True
        response_content = False
        try:
            response_content = client.execute(request)
        except Exception as e:
            logging.error(f"Error when executing request: {e}")
        if not response_content:
            print("failed execute")
        else:
            response = DatadigitalFincloudGeneralsaasFaceCertifyVerifyResponse()
            # 解析响应结果
            response.parse_response_content(response_content)
            if response.is_success():
                # print("请求成功,响应结果certify_url:  " + response.certify_url)
                return response.certify_url
            else:
                # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
                logging.error(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    @staticmethod
    def Finally_Query(client, certify_id: str):  # 查询结果
        '''
        跳转支付宝人脸核身查询记录
        :param certify_id:第一步的certify_id
        :return:{
            "datadigital_fincloud_generalsaas_face_certify_query_response": {
                "code": "10000",
                "msg": "Success",
                "passed": "T"
            },
            "sign": "ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE"
        }
        '''
        # 对照接口文档，构造请求对象
        model = DatadigitalFincloudGeneralsaasFaceCertifyQueryModel()
        # datadigital.fincloud.generalsaas.face.certify.initialize(H5人脸核身初始化)返回的certify_id
        model.certify_id = certify_id
        request = DatadigitalFincloudGeneralsaasFaceCertifyQueryRequest(biz_model=model)
        response_content = False
        try:
            response_content = client.execute(request)
        except Exception as e:
            logging.error(f"Error when executing request: {e}")
            logging.error(traceback.format_exc())
        if not response_content:
            print("failed execute")
        else:
            response = DatadigitalFincloudGeneralsaasFaceCertifyQueryResponse()
            # 解析响应结果
            response.parse_response_content(response_content)
            if response.is_success():
                # print("请求成功,响应结果passed:  " + response.passed)
                return response.passed
            else:
                # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
                logging.error(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    # 测试用例
    #print(real_man_verify.First_Initialize(rxconfig.pay.alipay.alipay_client(),'姓名','身份证号'))
# endregion


# 找出连接表里存在于不存在数据的原始表
def test_search_identity_in_org_and_not_in_org():
    '''
    【有效】另一种方法：优点：减少了数据传输次数 缺点：加重了计算 适合少量数据
    #实测时间 0.0001s   0.00011s    0.00012s
    command = (select(
            identity,  # 选择完整的 Identity 对象
            func.count(org_map_org2identity.identity_uuid).label('link_count')  # 计算链接数并命名为 'link_count'
        )
        .select_from(   # 使用 LEFT OUTER JOIN    这确保了所有 type='A' 的 identity 都会被返回，即使它们在 map_org2identity 中没有匹配项
            outerjoin(identity, org_map_org2identity, and_(
                identity.uuid == org_map_org2identity.identity_uuid,
                org_map_org2identity.org_uuid == '1689320b-fe50-7b46-8000-8b2fc5dde217'
        )))
        .where(identity.user_uuid == '0676d2d6-acc8-7abd-8000-114f9774296b')
        .group_by(identity)# 按 Identity 对象进行分组)
    )
    # 5. 执行查询
    with Session(engine) as session:
        results = session.exec(command).all()

    # 分类结果
    identity_in_org = [id for id, count in results if count > 0]
    identity_not_in_org = [id for id, count in results if count == 0]
    '''

    #【有效】另一种方法：优点：减少了计算，只是简单地查询  缺点：加重了服务器请求次数   适合大量数据。    实测时间: 0.0001s 0.00008s
    stmt_with_link = (select(identity)
        .join(org_map_org2identity)
        .where(
            and_(
                identity.user_uuid == '0676d2d6-acc8-7abd-8000-114f9774296b',
                exists().where(
                    and_(
                        org_map_org2identity.identity_uuid == identity.uuid,
                        org_map_org2identity.org_uuid == '0689320b-fe50-7b46-8000-8b2fc5dde217'
                    )
                ).correlate(identity)  # 明确指定关联 Identity 表
            )
        )
    )

    # 查询没有链接的 Identity 对象(user_uuid=A 且存在 org_uuid=B 的映射)
    stmt_without_link = (select(identity)
        .where(
            and_(
                identity.user_uuid == '0676d2d6-acc8-7abd-8000-114f9774296b',
                not_(
                    exists().where(
                        and_(
                        org_map_org2identity.identity_uuid == identity.uuid,
                        org_map_org2identity.org_uuid == '0689320b-fe50-7b46-8000-8b2fc5dde217'
                    )
                ).correlate(identity)  # 明确关联 Identity 表
            )
        )
    ))



    # 执行查询
    with Session(engine) as session:
        identity_in_org = [row for row in session.exec(stmt_with_link).all()]
        identity_not_in_org = [row for row in session.exec(stmt_without_link).all()]

    print('IN:', identity_in_org)
    print('NOT IN:', identity_not_in_org)

# 限制长度，超出长度仍写入则，从前往后覆盖
def rewrite_str():
    input_var = ""
    for _ in range(10):
        x = str(random.randint(1, 9))
        if len(input_var) < 6:
            input_var += x
        else:
            input_var = (x + input_var)[:6]
        print(input_var)

if __name__ == '__main__':
    #print_info()
    # join_test()
    # test_change_jsonb()
    # test_change_org_base_index_head_notice()
    # test_switch_list2str()
    # make_an_appointment()
    # test_calendar()
    # test_calculate_pi(0, 1000)
    # test_datetime()
    # test_time_unit()
    # print(uuid7str())
    # redis_R_W()
    # asyncio.run(redis_pub_sub())
    # test_write_db_time_then_yield_on_time_of_near_hour()
    # asyncio.run(redis_pub())
    #test_search_identity_in_org_and_not_in_org()
    #command = (select(
    #        identity.uuid,
    #        identity.name,
    #        identity.type,
    #        identity.level,
    #        org_map_org2identity.type,
    #        org_map_org2identity.level,
    #        org_map_org2identity.tip,
    #        org_map_org2identity.money,
    #        user.phone_number,
    #        user.name,
    #        user.real_man_verify_info,
    #        user.level,
    #    )
    #    .join(identity, org_map_org2identity.identity_uuid == identity.uuid)
    #    .join(user, identity.user_uuid == user.uuid)
    #    .where(org_map_org2identity.org_uuid == '0689320b-fe50-7b46-8000-8b2fc5dde217')
    #)
    #with Session(engine) as session:
    #    result = session.exec(command).first()


    #print('RRRRRRR', result)

    #rewrite_str()
    L = [1,2,3]
    print(L[3])




