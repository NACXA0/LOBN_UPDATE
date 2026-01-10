# 配置的缓存变量
    # 这里存储系统的全局配置数据、网站运行逻辑等。
        #比如开关开发者模式、底层条件频率限制、与网站的运行逻辑有关，使得可以在后台配置网站的运行方式。
        #- 实现在不停机的情况下对网站运行进行控制
    # 结构说明：
        # 1. 不可变变量-由于过于敏感与重要，修改必须重启服务并修改代码进行修改的变量
        # 2. 可变变量-可以通过后台配置进行修改的变量
        # 3. 在文件global_config.py里 -> 更新变量的生命周期函数-定期从数据库获取最新配置信息
    # 用这里的 变量 缓存配置， 还是 redis缓存配置？—— 现在是用这里的 变量 缓存配置
        # redis缓存的优缺点：
            # 优点：支持多进程
            # 缺点：1. redis的数据类型支持多一道门槛，这里的变量缓存就是原生的类型
                # 2. 文件结构不好设计，配置文件的结构比较复杂，转到redis里的话还得附加一张表“键名&配置内容对应表”，而 这里的变量 直接就可以用类形成结构
            # 变量 缓存的其他优点：
                # 可以有默认值、完整的注释
                # 速度最快：无需网络通信


# region 不可变变量-由于过于敏感与重要，修改必须通过修改代码进行修改的变量

is_prod: bool = False  # 生产环境替换为True,如果正在开发中，使用False

class DataBase:
    #说明: 数据库连接参数,
    host: str = "localhost"   #host数据库地址
    port: int = 2345  #port数据库端口(str)
    dbname: str = "txcloudserverdb"  #dbname数据库名称
    user: str = "nacxa"    #user数据库用户名
    password: str= "QAZWSX"   #password数据库用户的密码

# endregion






# region 可变变量-可以通过后台配置进行修改的变量
    # 要遵循pydantic2的语法规范。以后升级迁移的redis-om也是这个规范。（仅动态数据必须遵守，本地不可变变量可不用）
from pydantic2 import BaseModel, Field

class test(BaseModel):  # 测试用的配置类
    test_config_var: str = Field(default='初始值')  # 测试用的变量，后台配置修改后会更新此变量的值
config_test = test()  # 实例化测试配置类



class system(BaseModel):
    # region 系统级参数
freq_of_get_config_system: int = Field(default=15)  # 获取系统配置的频率（秒）  定时查询配置文件数据库->写入python程序变量
freq_of_get_ui_config: int = Field(default=15 ) # 获取ui配置的频率（秒）  定时查询配置文件数据库->写入python程序变量
    # endregion
config_system = system()  # 实例化系统配置类


class page(BaseModel):  # 页面配置的公共变量
    config_page_index: dict = {}   # 首页的配置
    config_page_login: dict = {}   # 登录页的配置
config_page = page()  # 实例化页面配置类

class sms_login_verify_code(BaseModel):
    # region 短信基础信息
    sign_name: str = Field(default="个人网站验证码") # 短信签名名称
    template_code: str = Field(default="SMS_468735089")  # 短信模板Code
    send_sms_freq : int = Field(default=3)  #验证码短信发送频率（秒/个）【代转移】
    verify_code_effective_time: int = Field(default=300)  # 验证码有效期（秒）【代转移】
    # endregion

    # region 短信应用设置
    send_sms_freq = 3  # 验证码短信发送频率（秒/个）
    verify_code_effective_time = 300  # 验证码有效期（秒）
    check_verify_code_mistake = 3  # 一般性的验证码验证错误次数  超额则锁定？
    # endregion
config_sms_login_verify_code = sms_login_verify_code()  # 实例化短信配置类

class user(BaseModel):
    default_user_signin_privilege_select: dict = Field(default={})  # 用户注册的默认权限配置
config_user = user()  # 实例化用户配置类

class money(BaseModel):
    round_num: int = Field(default=2)  # 用于展示的金钱的小数位数
    refresh_user_money_can_show_button_freq: int = Field(default=3000)  # 主动刷新余额按钮的频率     使用.throttle(500) （毫秒）
    # 支付宝在支付方面的
    # 微信在支付方面的
config_money = money()  # 实例化金钱配置类

class ui(BaseModel):
    '''
    案例：default_button_throttle：某按钮已有后端独立判断，那么此时按钮throttle属于默认的仅state以及后端程序判断类
    '''
    default_button_throttle: int = Field(default=1000) #默认的按钮的防抖值（毫秒）       仅state以及后端程序判断类
    default_button_throttle_db: int = Field(default=3000) #默认的按钮的防抖值（毫秒）    数据库查询类
    default_button_throttle_sms: int = Field(default=10000) #默认的按钮的防抖值（毫秒）  发送短信类
config_ui = ui()  # 实例化UI配置类

class aouth(BaseModel):    #网站本身相关     密钥、域名信息之类的
    commander_phone_number: str = Field(default='13051163820' )    #超管手机号，所有敏感操作都会向此手机号发送确认短信   纯数字   仅限国内
    domain: str = Field(default='nacxa.top')    #主域名
    cdn_domain: str = Field(default='https://cdn.dana.lobn.com.cn/')    #CDN域名     要用CDN访问oss文件，则后面直接加上文件路径
    DNICP: str = Field(default='京ICP备09068351号-2') #网站备案号
    police_record: str = Field(default='京公网安备 11010802034771号') #网站公安备案号
    service_phone_number: str = Field(default='400-610-8299') #客服电话  仅供展示
    service_email: str = Field(default='dana_service@lobn.com.cn') #客服邮箱
    path_user_data: str = Field(default='/user_data')   #存放用户文件的路径     /是assets里面  以后要转到oss
config_aouth = aouth()  # 实例化网站本身配置类


class REDIS(BaseModel):  # 用大写防止与redis包重名
    local_redis_url: str = Field(default='redis://localhost:6379') # 本地redis地址
    renewal_redis_connect_time: int = Field(default=300)   # redis实例的续约时间（秒）到时间主动请求一次延时，否则被否则被后台关闭频道、断开连接
config_redis = REDIS()  # 实例化REDIS配置类
    

class alipay(BaseModel):   # 支付宝相关
    disable_start_verify_button_time: int = Field(default=15)   # 延时出启用开始认证按钮，防止用户频繁提交身份信息表单
    delay_show_check_verify_button_time: int = Field(default=5)    # 延时出现核验完毕按钮的时间(S)(int)    大于点击跳转，进行扫码的时间；小于于实人验证所需的时间
    #alipay_notify_path = '/background/post_alipay_async_notify'  # 用户支付成功时异步通知的地址  POST    异步通知    支付宝服务器主动通知商户服务器里指定的页面http / https路径
    #alipay_notify_in_redis_publish_ttl = 86400  # 支付宝异步通知在redis发布订阅中的留存时间（秒）   超市就等待每天核对账目，或者主动查询
    #redis_async_alipay_notify_url = "redis://localhost:6379"  # 用于支付宝异步通知缓存redis数据库的URL  功能函数在self_define_function里
    
    # 开发者私钥，由开发者自己生成。格式:PKCS1
    #with open('应用私钥RSA2048-PCKS1格式-十慧科技.txt', 'r', encoding='utf-8') as file:  # 这个private_key是PCKS1格式的应用私钥，需要现在工具里转换格式。
    #    app_private_key = file.read()
    app_private_key: str = Field(default='')
    # APPID 即创建应用后生成
    #with open('APPID十慧科技.txt', 'r', encoding='utf-8') as file:
    #    app_id = file.read()
    app_id: str = Field(default='')
    # 支付宝公钥
    #with open('alipayPublicKey_RSA2-十慧科技.txt', 'r', encoding='utf-8') as file:
    #    alipay_public_key = file.read()
    alipay_public_key: str = Field(default='')
    # AES秘钥,开放平台接口内容加密方式中获取
    #with open('AES_Key_十慧科技.txt', 'r', encoding='utf-8') as file:
    #    encrypt_key = file.read()
    encrypt_key: str = Field(default='')
    #with open('应用公钥RSA2048-十慧科技.txt', 'r', encoding='utf-8') as file:
    #    app_cert_sn = file.read()
    app_cert_sn: str = Field(default='')
    #with open('支付宝账号ID-十慧科技.txt', 'r', encoding='utf-8') as file:
    #    seller_id = file.read()  # 这里连接卖家支付宝账号 ID。以 2088 开头的纯 16 位数字
    seller_id: str = Field(default='')


    
    # APPID 即创建应用后生成
    sandbox_app_id: str = Field(default='9021000140651982')
    # AES秘钥,开放平台接口内容加密方式中获取
    sandbox_encrypt_key: str = Field(default='SEkZSzgsgIiLj0OllsdSsw==')
    # 支付宝公钥
    sandbox_alipay_public_key: str = Field(default='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhWxoFTJoKaLMgsp1BWv0kavc8Sj2v+5CQR9sOdv1qzsm+Ff4nbRVwgK091/VVA+3BzVLsWVltDSmexE9Fs7q6weql2e6nOlPeKcHpNmE15T/K1KNQimyNx7YeV4Kh+dPTNXwk70FEIRzzt66i4EfAsbhTlZy7eXoNtkHBYixBD+InPg98pCgyDWn1+uxuyVD3Nk8XeK1LjBcGatmaytna89Bi1R+fnRLFAbitGWxtOI7qD368FTBZ5ZH1YprpXR5alf0+RHz2hje0x+XpwG9TYVIbfeiilTENoMkGVkUiEHQ7n8mz1Zhln623frBg/01YSw5WOAKPS9an9snv7ETSQIDAQAB')
    # 开发者私钥，由开发者自己生成。格式:PKCS1
    sandbox_app_private_key: str = Field(default='MIIEowIBAAKCAQEAhkELyMbKA9rwdxgKc8d57POTLQj1hlMPKDwZJMrF6SAxsJ6tSlmwheQ5+4IPcR9qkkjy/vck6nNaUXJ+wS88HbdTCRB6vsOebrNLspeSAx83LFiPHfjUQSxWzjIuCIGc6k4nvbO+19tNF+q1BplGVVZ6QZVnYf4r10h1O2++qBYCj9iBFqEIhtsPWQa6eSjcIRbB8UG1dTr/KzIffUvJObuG5Lh/azEa8f/E+S9kpp9zvkaJ4xivQLqkUDug6IR3F7/4xXrNsP40FSNYbczf+uvutLA1i0p4ojapX5xOlCQ2k9dtPmv1v2i1wNxvC1h9jxnm3oRpBvoPiV6DzKeSeQIDAQABAoIBAGRmcpyk5WC6tAgsZ2ysaeclRRRx1cOti/FH+HnGVvl/xQlTsT6gEl4fDqmjW0768qURfv/j7ayTtaChYl+wpmGGvsdRlqng+zPITDz0ExLYnldAp07/ziQrN4OejUR5QdMLvbalnHwrGd1f/h9AMxQQxv8S7yyee0TVgC6B4/Ao5jZDpsXarmX8f0NHSVlpKy9Gdghpc5v9ZxvXmfgD3GyJlRLUIkCvvlvsJFVRegySN8crlAX+mEFEye6nH1G6D5VN//j7KVbaLmSA4M58ONR4w3pRy+tYeFit+BhfhwJbljyO490zj2qZL5jjSBr0EWf+yI5zKl9mQfMzCIQqTLECgYEA0eemBR/mkzCwtDsGQT5pKTc/zJ4ktZrZ/Bi06oiqzGhRc/MWTsKeA54Brz0MoWap5ZzkzrEncqDx4fZLeEe2BdmXUdCipO4+aiiUoMBND11tHUfSdbPatXjzeE49/Rx490VhaF2at0iiLK93FJUVl7WWC5cpCzznqQKb4utOPVUCgYEAo7x9kbiy93+HieH6U+EOeU2bXSYyCJriXe+Om1GlhjshCH1oj4/XmZQXJ84gOjtFweWL+0xBEZWxSi5uzauLJ2oe017RzlWoUFuz+qDZJyLGki+lwmfL7JYmvHiepYg5RtEdzNzkdmuoO+NI/E4iiES0/Uqw2iNNwaZnOMymYJUCgYEAjCGCDFnHrOwMi8X73wKzYfiodwn8p+DBNjOoVAr5O41JE4dtlRcINpH9veebzwSi189uUS6jjzszQA8VQy9crXseMlh+vGzw7h45WzgGOgO9HJceQcXYdN5SbDaP27Jub2W6KdqTt1ieLAbYEL2WtLldek9n70Cxx3seZteAXCECgYBTcshokUKdAyEX89T6FPSkfBoXolTTr+R4zZPXswfyXoZaZlf4+u1990zJ27LvGrBVvuDV5aowBSPDU+Di72/PWbV2MpgpWdybf/E9ZebmnEGp1aDccLwsyuXZHnx0jvXqEr/mXhoOBJZMV20mMchFvQalJQD3XBDQBjgLabnN9QKBgDpBzNPMs5i+gOr3C2vWLDkUv9G0deem/BwcnmECWBUp7A6iSbQDRVqLxQCg0esJ6kL6P7Y3nlc4Zt8RdE4Un4M2UyZOA8OnTWnT0O4Or/8/0O/JazUEZqpwlbAezJ6QSGmDABbHs9huYpsYH7AGnbVNkPoMSdXoLdEfNzF8Vmdr')
    # 【可选，否则自己查询】return_url 用户确认支付时通知的地址    GET     同步通知 支付宝服务器主动通知商户服务器里指定的页面http/https路径
    sandbox_return_url: str = Field(default='')
    # 【可选，否则自己查询】notify_url 用户支付成功时通知的地址    POST    异步通知 支付宝服务器主动通知商户服务器里指定的页面http/https路径
    sandbox_notify_url: str = Field(default='')
config_alipay = alipay()  # 实例化支付宝配置类



# endregion
















