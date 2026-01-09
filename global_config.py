# 配置的缓存变量
    # 这里存储系统的全局配置数据、网站运行逻辑等。
        #比如开关开发者模式、底层条件频率限制、与网站的运行逻辑有关，使得可以在后台配置网站的运行方式。
        #- 实现在不停机的情况下对网站运行进行控制
# 结构说明：
    # 1. 不可变变量-由于过于敏感与重要，修改必须重启服务并修改代码进行修改的变量
    # 2. 可变变量-可以通过后台配置进行修改的变量
    # 3. 在文件global_config.py里 -> 更新变量的生命周期函数-定期从数据库获取最新配置信息






# region 不可变变量-由于过于敏感与重要，修改必须通过修改代码进行修改的变量

is_prod: bool = False  # 生产环境替换为True,如果正在开发中，使用False

class DataBase:
    #说明: 数据库连接参数,
    host="localhost"   #host数据库地址
    port=2345  #port数据库端口(str)
    dbname="txcloudserverdb"  #dbname数据库名称
    user="nacxa"    #user数据库用户名
    password="QAZWSX"   #password数据库用户的密码

# endregion


# region 可变变量-可以通过后台配置进行修改的变量
test_config_var: str = '初始值'  # 测试用的变量，后台配置修改后会更新此变量的值
    # region 下面是页面配置的公共变量
config_page_index: dict = {}   # 首页的配置
config_page_login: dict = {}   # 登录页的配置
    # endregion


# 支付宝用的
#from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
#from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

    # region 系统级参数
freq_of_get_config_system: int = 15  # 获取系统配置的频率（秒）  定时查询配置文件数据库->写入python程序变量
freq_of_get_ui_config: int = 15  # 获取ui配置的频率（秒）  定时查询配置文件数据库->写入python程序变量
    # endregion




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

class alipay:   # 支付宝相关
    disable_start_verify_button_time: int = 15   # 延时出启用开始认证按钮，防止用户频繁提交身份信息表单
    delay_show_check_verify_button_time: int = 5    # 延时出现核验完毕按钮的时间(S)(int)    大于点击跳转，进行扫码的时间；小于于实人验证所需的时间
    #alipay_notify_path = '/background/post_alipay_async_notify'  # 用户支付成功时异步通知的地址  POST    异步通知    支付宝服务器主动通知商户服务器里指定的页面http / https路径
    #alipay_notify_in_redis_publish_ttl = 86400  # 支付宝异步通知在redis发布订阅中的留存时间（秒）   超市就等待每天核对账目，或者主动查询
    #redis_async_alipay_notify_url = "redis://localhost:6379"  # 用于支付宝异步通知缓存redis数据库的URL  功能函数在self_define_function里
    #with open('应用私钥RSA2048-PCKS1格式-十慧科技.txt', 'r', encoding='utf-8') as file:  # 这个private_key是PCKS1格式的应用私钥，需要现在工具里转换格式。
    #    app_private_key = file.read()
    #with open('APPID十慧科技.txt', 'r', encoding='utf-8') as file:
    #    app_id = file.read()
    #with open('alipayPublicKey_RSA2-十慧科技.txt', 'r', encoding='utf-8') as file:
    #    alipay_public_key = file.read()
    #with open('AES_Key_十慧科技.txt', 'r', encoding='utf-8') as file:
    #    encrypt_key = file.read()
    #with open('应用公钥RSA2048-十慧科技.txt', 'r', encoding='utf-8') as file:
    #    app_cert_sn = file.read()
    #with open('支付宝账号ID-十慧科技.txt', 'r', encoding='utf-8') as file:
    #    seller_id = file.read()  # 这里连接卖家支付宝账号 ID。以 2088 开头的纯 16 位数字
    app_private_key = app_id = alipay_public_key = encrypt_key = app_cert_sn = seller_id = ''  # 先赋值空，防止报错


    def alipay_client(self):  # 支付宝通用的初始化内容
        '''调用方式：rxconfig.alipay().alipay_client()'''
        # 日志配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            filemode='a')
        logger = logging.getLogger('')
        # 配置
        alipay_client_config = AlipayClientConfig()
        # 支付宝网关（固定）
        alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
        # APPID 即创建应用后生成
        alipay_client_config.app_id = self.app_id
        # AES秘钥,开放平台接口内容加密方式中获取
        alipay_client_config.encrypt_key = self.encrypt_key
        # 接口加密方式,目前支持AES
        alipay_client_config.encrypt_type = 'AES'
        # 生成签名字符串所使用的签名算法类型，目前支持 RSA2 算法。
        alipay_client_config._sign_type = 'RSA2'
        # 编码集，支持 GBK/UTF-8
        alipay_client_config.charset = 'utf-8'
        # 参数返回格式，只支持 JSON（固定）
        alipay_client_config.format = 'json'
        # 支付宝公钥
        alipay_client_config.alipay_public_key = self.alipay_public_key
        # 开发者私钥，由开发者自己生成。格式:PKCS1
        alipay_client_config.app_private_key = self.app_private_key
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
        return client

    def alipay_client_sandbox(self):  # 支付宝通用的初始化内容   这里的括号就是空的 # 【仅供测试】沙箱版客户端
        # 日志配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filemode='a', )
        logger = logging.getLogger('')
        # 配置
        alipay_client_config = AlipayClientConfig()
        # 支付宝网关（固定）
        alipay_client_config.server_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do'
        # APPID 即创建应用后生成
        alipay_client_config.app_id = '9021000140651982'
        # AES秘钥,开放平台接口内容加密方式中获取
        alipay_client_config.encrypt_key = 'SEkZSzgsgIiLj0OllsdSsw=='
        # 接口加密方式,目前支持AES
        alipay_client_config.encrypt_type = 'AES'
        # 生成签名字符串所使用的签名算法类型，目前支持 RSA2 算法。
        alipay_client_config.sign_type = 'RSA2'
        # 编码集，支持 GBK/UTF-8
        alipay_client_config.charset = 'utf-8'
        # 参数返回格式，只支持 JSON（固定）
        alipay_client_config.format = 'json'
        # 支付宝公钥
        alipay_client_config.alipay_public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhWxoFTJoKaLMgsp1BWv0kavc8Sj2v+5CQR9sOdv1qzsm+Ff4nbRVwgK091/VVA+3BzVLsWVltDSmexE9Fs7q6weql2e6nOlPeKcHpNmE15T/K1KNQimyNx7YeV4Kh+dPTNXwk70FEIRzzt66i4EfAsbhTlZy7eXoNtkHBYixBD+InPg98pCgyDWn1+uxuyVD3Nk8XeK1LjBcGatmaytna89Bi1R+fnRLFAbitGWxtOI7qD368FTBZ5ZH1YprpXR5alf0+RHz2hje0x+XpwG9TYVIbfeiilTENoMkGVkUiEHQ7n8mz1Zhln623frBg/01YSw5WOAKPS9an9snv7ETSQIDAQAB'
        # 开发者私钥，由开发者自己生成。格式:PKCS1
        alipay_client_config.app_private_key = 'MIIEowIBAAKCAQEAhkELyMbKA9rwdxgKc8d57POTLQj1hlMPKDwZJMrF6SAxsJ6tSlmwheQ5+4IPcR9qkkjy/vck6nNaUXJ+wS88HbdTCRB6vsOebrNLspeSAx83LFiPHfjUQSxWzjIuCIGc6k4nvbO+19tNF+q1BplGVVZ6QZVnYf4r10h1O2++qBYCj9iBFqEIhtsPWQa6eSjcIRbB8UG1dTr/KzIffUvJObuG5Lh/azEa8f/E+S9kpp9zvkaJ4xivQLqkUDug6IR3F7/4xXrNsP40FSNYbczf+uvutLA1i0p4ojapX5xOlCQ2k9dtPmv1v2i1wNxvC1h9jxnm3oRpBvoPiV6DzKeSeQIDAQABAoIBAGRmcpyk5WC6tAgsZ2ysaeclRRRx1cOti/FH+HnGVvl/xQlTsT6gEl4fDqmjW0768qURfv/j7ayTtaChYl+wpmGGvsdRlqng+zPITDz0ExLYnldAp07/ziQrN4OejUR5QdMLvbalnHwrGd1f/h9AMxQQxv8S7yyee0TVgC6B4/Ao5jZDpsXarmX8f0NHSVlpKy9Gdghpc5v9ZxvXmfgD3GyJlRLUIkCvvlvsJFVRegySN8crlAX+mEFEye6nH1G6D5VN//j7KVbaLmSA4M58ONR4w3pRy+tYeFit+BhfhwJbljyO490zj2qZL5jjSBr0EWf+yI5zKl9mQfMzCIQqTLECgYEA0eemBR/mkzCwtDsGQT5pKTc/zJ4ktZrZ/Bi06oiqzGhRc/MWTsKeA54Brz0MoWap5ZzkzrEncqDx4fZLeEe2BdmXUdCipO4+aiiUoMBND11tHUfSdbPatXjzeE49/Rx490VhaF2at0iiLK93FJUVl7WWC5cpCzznqQKb4utOPVUCgYEAo7x9kbiy93+HieH6U+EOeU2bXSYyCJriXe+Om1GlhjshCH1oj4/XmZQXJ84gOjtFweWL+0xBEZWxSi5uzauLJ2oe017RzlWoUFuz+qDZJyLGki+lwmfL7JYmvHiepYg5RtEdzNzkdmuoO+NI/E4iiES0/Uqw2iNNwaZnOMymYJUCgYEAjCGCDFnHrOwMi8X73wKzYfiodwn8p+DBNjOoVAr5O41JE4dtlRcINpH9veebzwSi189uUS6jjzszQA8VQy9crXseMlh+vGzw7h45WzgGOgO9HJceQcXYdN5SbDaP27Jub2W6KdqTt1ieLAbYEL2WtLldek9n70Cxx3seZteAXCECgYBTcshokUKdAyEX89T6FPSkfBoXolTTr+R4zZPXswfyXoZaZlf4+u1990zJ27LvGrBVvuDV5aowBSPDU+Di72/PWbV2MpgpWdybf/E9ZebmnEGp1aDccLwsyuXZHnx0jvXqEr/mXhoOBJZMV20mMchFvQalJQD3XBDQBjgLabnN9QKBgDpBzNPMs5i+gOr3C2vWLDkUv9G0deem/BwcnmECWBUp7A6iSbQDRVqLxQCg0esJ6kL6P7Y3nlc4Zt8RdE4Un4M2UyZOA8OnTWnT0O4Or/8/0O/JazUEZqpwlbAezJ6QSGmDABbHs9huYpsYH7AGnbVNkPoMSdXoLdEfNzF8Vmdr'

        # 【可选，否则自己查询】return_url 用户确认支付时通知的地址    GET     同步通知 支付宝服务器主动通知商户服务器里指定的页面http/https路径
        alipay_client_config.return_url = ''
        # 【可选，否则自己查询】notify_url 用户支付成功时通知的地址    POST    异步通知 支付宝服务器主动通知商户服务器里指定的页面http/https路径
        alipay_client_config.notify_url = ''

        return DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
        # 实例化客户端



# endregion
















