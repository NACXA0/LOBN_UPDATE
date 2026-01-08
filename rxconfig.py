# 包含reflex基本参数、程序参数设置、程序实例、激活此处的实例的程序

import reflex as rx
# 支付宝用的
#from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
#from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

# region 系统级参数
is_prod: bool = False  # 生产环境替换为True,如果正在开发中，使用False
freq_of_get_ui_config: int = 5  # 获取ui配置的频率（秒）  定时查询配置文件数据库->写入python程序变量
# endregion

class DataBase:
    #说明: 数据库连接参数,
    host="localhost"   #host数据库地址
    port=2345  #port数据库端口(str)
    dbname="txcloudserverdb"  #dbname数据库名称
    user="nacxa"    #user数据库用户名
    password="QAZWSX"   #password数据库用户的密码


class login:
    class send_verify_code:
        sign_name = "个人网站验证码"  # 短信签名名称
        template_code = "SMS_468735089"  # 短信模板Code
        send_sms_freq = 3  #验证码短信发送频率（秒/个）【代转移】
        verify_code_effective_time = 300  # 验证码有效期（秒）【代转移】

class user:
    default_user_signin_privilege_select = {}  # 用户注册的默认权限配置

class verify_code:
    send_sms_freq = 3  # 验证码短信发送频率（秒/个）
    verify_code_effective_time = 300  # 验证码有效期（秒）
    check_verify_code_mistake = 3  # 一般性的验证码验证错误次数  超额则锁定？

class config_money:
    round_num: int = 2  # 用于展示的金钱的小数位数
    refresh_user_money_can_show_button_freq = 3000  # 主动刷新余额按钮的频率     使用.throttle(500) （毫秒）

    class alipay:   # 支付宝在支付方面的
        pass
    class wechat_pay:   # 微信在支付方面的
        pass

class ui:
    '''
    案例：default_button_throttle：某按钮已有后端独立判断，那么此时按钮throttle属于默认的仅state以及后端程序判断类
    '''
    default_button_throttle = 1000 #默认的按钮的防抖值（毫秒）       仅state以及后端程序判断类
    default_button_throttle_db = 3000 #默认的按钮的防抖值（毫秒）    数据库查询类
    default_button_throttle_sms = 10000 #默认的按钮的防抖值（毫秒）  发送短信类


class aouth:    #网站本身相关     密钥、域名信息之类的
    commander_phone_number: str = '13051163820'     #超管手机号，所有敏感操作都会向此手机号发送确认短信   纯数字   仅限国内
    domain: str = 'nacxa.top'    #主域名
    cdn_domain: str = 'https://cdn.dana.lobn.com.cn/'    #CDN域名     要用CDN访问oss文件，则后面直接加上文件路径
    DNICP: str = '京ICP备09068351号-2' #网站备案号
    police_record: str = '京公网安备 11010802034771号' #网站公安备案号
    service_phone_number: str = '400-610-8299' #客服电话  仅供展示
    service_email: str = 'dana_service@lobn.com.cn' #客服邮箱
    path_user_data: str = '/user_data'   #存放用户文件的路径     /是assets里面  以后要转到oss



class REDIS:  # 用大写防止与redis包重名
    # 在服务器启动时创建实例【rxconfig里】
    #redis_client_pubsub_user = redis.asyncio.Redis.from_url("redis://localhost:6379")  # redis实例，发布订阅，用户用的实例
    #redis_client_pubsub_server = redis.asyncio.Redis.from_url("redis://localhost:6379")  # redis实例，发布订阅，服务器用滚动实例

    renewal_redis_connect_time: int = 300   # redis实例的续约时间（秒）到时间主动请求一次延时，否则被否则被后台关闭频道、断开连接

    # 激活并创建实例（在rxconfig里）， 被生命周期触发）
    #@staticmethod
    #async def activate_redis_pubsub():
        # 激活连接（通过 ping 方法 -> bool）
    #    if await REDIS.redis_client_pubsub_user.ping() and await REDIS.redis_client_pubsub_server.ping():
    #        print("redis连接成功, 并创建了redis实例: 'redis_client_pubsub_user'和'redis_client_pubsub_server'")
    #    else:
    #        print("redis连接失败, 关闭连接。")
    #        await REDIS.redis_client_pubsub_user.close()
    #        await REDIS.redis_client_pubsub_server.close()

    




config = rx.Config(
    app_name="LOBN_UPDATE", # 应用的名称（应与应用目录匹配）
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
