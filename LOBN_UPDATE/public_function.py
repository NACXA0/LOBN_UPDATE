# 公共函数 和 公共变量
import reflex as rx
import time

from typing import Tuple, Literal
import rxconfig
#import os, random, time, datetime, asyncio, logging, traceback, uuid
#import pandas as pd
from sqlmodel import Session, select, or_
from .DataBase_function.database import engine
#from .DataBase_function.models import user, product_make_an_appointment_time, org, identity, org_map_org2identity, approve_event, approve_history, approve_team

# 下面是短信用的
#from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
#from alibabacloud_tea_openapi import models as open_api_models
#from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
#from alibabacloud_tea_util import models as util_models
#from alibabacloud_tea_util.client import Client as UtilClient
#
#from concurrent.futures import ThreadPoolExecutor



# region 公共变量

# 下面是页面配置的公共变量
page_config_index = {}   # 首页的配置
page_config_login = {}   # 登录页的配置

# endregion




# 下面是公共函数

# 生命周期任务-定时查询配置文件数据库->写入python程序变量
def load_config_from_db(db_connection):
    while True:
        # 查询配置文件数据库
        print('占位-查询一次数据库')
        # 写入python变量
        print('占位-一条数据是一个页面配置的json-将所有的配置数据行写入到对应页面的python变量中')
        time.sleep(rxconfig.freq_of_get_ui_config)  # 每几秒查询一次








# 【随机起名】 用于新注册用户
def random_user_name() -> str:
    #输入：无   输出：形容词+的+名词 96x84种组合 用于新注册用户
    #import random
    adj = ("俏皮", "迷糊", "灵动", "憨态", "精灵", "萌动", "绮丽", "璀璨", "暖阳", "微笑", "星眸", "月牙", "翠绿", "鲜嫩", "亮泽", "梦幻", "甜蜜", "轻快", "悠扬", "悠闲", "翩翩", "轻盈", "活泼", "烂漫", "纯真", "天真", "妩媚", "优雅", "端庄", "俏丽", "伶俐", "机灵", "明媚", "温柔", "柔和", "悦耳", "悦目", "珍贵", "珍珠", "珊瑚", "碧绿", "美艳", "艳丽", "清新", "恬静", "宁静", "安静", "恬淡", "清澈", "纯净", "闪耀", "光彩", "妖娆", "魅力", "风情", "热情", "火辣", "冷艳", "高贵", "甜美", "清秀", "精致", "细腻", "柔滑", "顺滑", "柔韧", "坚韧", "弹性", "紧致", "丰满", "丰腴", "玲珑", "精巧", "匀称", "秀气", "短小", "精悍", "强壮", "健硕", "结实", "纤细", "苗条", "修长", "高挑", "婀娜", "俊俏", "英俊", "帅气", "阳刚", "阳光", "温文尔雅", "风度翩翩", "英姿焕发")
    verb = ('小猫', '甜心', '绵羊', '毛绒', '珍珠', '萌娃', '花蕾', '棉花', '眯眼', '笑脸', '呆萌', '粉嫩', '乖乖', '柔软', '爱抚', '温柔', '小鹿', '蜜蜂', '暖阳', '碎花', '甜品', '童话', '悠闲', '憨态', '星眸', '舒适', '柔毛', '小嘴', '乐园', '悦耳', '纯真', '梦境', '甜蜜', '轻盈', '珍惜', '温馨', '小兔', '悦目', '萌萌', '美好', '亲亲', '柔光', '小溪', '翅膀', '纯洁', '悦心', '萌货', '美食', '暖心', '小鱼', '悠扬', '萌哒', '美丽', '亲爱', '柔情', '小猪', '悠闲', '萌态', '美梦', '暖意', '小猴', '悠哉', '萌动', '美景', '暖色', '小鸡', '悠然', '萌发', '美酒', '小熊', '娃娃', '天使', '彩虹', '蝴蝶', '花朵', '爱心', '棉花糖', '小鸟', '星星', '宝宝', '微笑', '云朵', '小草', '稚气')
    return adj[random.randint(0, 92)] + '的' + verb[random.randint(0, 83)]

# 列表批处理——多线程
def multiprocessing_change_list(input_list: list, function) -> list:
    '''
    对列表的所有元素进行某同一操作
    输入：一个列表+对列表进行某操作的函数
    输出：处理后的列表

    需要的包：from concurrent.futures import ThreadPoolExecutor

    function示例：
    def process_element(x):
        # 对元素执行操作
        return x * x  # 示例操作：求平方
    '''
    # 创建一个线程池执行器
    with ThreadPoolExecutor() as executor:
        # 使用执行器的 map 方法来并行处理列表中的元素
        results = executor.map(function, input_list)
    # 将结果转换为列表
    return list(results)


# 循环遍历列表的生成器
'''
已有语法糖
import itertools

my_list = [1, 2, 3, 4, 5]
cycled_iterator = itertools.cycle(my_list)

for _ in range(10):     这个优先循环，或者是一直循环while True
    print(next(cycled_iterator))
'''


