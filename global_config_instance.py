# 专门存储连接实例，如数据库连接、redis连接、云服务连接。   这些实例是非静态的，与其他数据类缓存不一样。
import global_config



class REDIS:  # 用大写防止与redis包重名
    # 在服务器启动时创建实例【rxconfig里】
    redis_client_pubsub_user = redis.asyncio.Redis.from_url(global_config.REDIS.local_redis_url)  # redis实例，发布订阅，用户用的实例
    redis_client_pubsub_server = redis.asyncio.Redis.from_url(global_config.REDIS.local_redis_url)  # redis实例，发布订阅，服务器用滚动实例
    
    # 激活并创建实例， 被生命周期触发）
    @staticmethod
    async def activate_redis_pubsub():
        # 激活连接（通过 ping 方法 -> bool）
        if await REDIS.redis_client_pubsub_user.ping() and await REDIS.redis_client_pubsub_server.ping():
            print("redis连接成功, 并创建了redis实例: 'redis_client_pubsub_user'和'redis_client_pubsub_server'")
        else:
            print("redis连接失败, 关闭连接。")
            await REDIS.redis_client_pubsub_user.close()
            await REDIS.redis_client_pubsub_server.close()


class alipay:   # 支付宝相关
    
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
        alipay_client_config.app_id = global_config.alipay.app_id
        # AES秘钥,开放平台接口内容加密方式中获取
        alipay_client_config.encrypt_key = global_config.alipay.encrypt_key
        # 接口加密方式,目前支持AES
        alipay_client_config.encrypt_type = 'AES'
        # 生成签名字符串所使用的签名算法类型，目前支持 RSA2 算法。
        alipay_client_config._sign_type = 'RSA2'
        # 编码集，支持 GBK/UTF-8
        alipay_client_config.charset = 'utf-8'
        # 参数返回格式，只支持 JSON（固定）
        alipay_client_config.format = 'json'
        # 支付宝公钥
        alipay_client_config.alipay_public_key = global_config.alipay.alipay_public_key
        # 开发者私钥，由开发者自己生成。格式:PKCS1
        alipay_client_config.app_private_key = global_config.alipay.app_private_key
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
        return client

    # 沙盒版支付宝
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
        alipay_client_config.app_id = global_config.alipay.sandbox_app_id
        # AES秘钥,开放平台接口内容加密方式中获取
        alipay_client_config.encrypt_key = global_config.alipay.sandbox_encrypt_key
        # 接口加密方式,目前支持AES
        alipay_client_config.encrypt_type = 'AES'
        # 生成签名字符串所使用的签名算法类型，目前支持 RSA2 算法。
        alipay_client_config.sign_type = 'RSA2'
        # 编码集，支持 GBK/UTF-8
        alipay_client_config.charset = 'utf-8'
        # 参数返回格式，只支持 JSON（固定）
        alipay_client_config.format = 'json'
        # 支付宝公钥
        alipay_client_config.alipay_public_key = global_config.alipay.sandbox_alipay_public_key
        # 开发者私钥，由开发者自己生成。格式:PKCS1
        alipay_client_config.app_private_key = global_config.alipay.sandbox_app_private_key

        # 【可选，否则自己查询】return_url 用户确认支付时通知的地址    GET     同步通知 支付宝服务器主动通知商户服务器里指定的页面http/https路径
        alipay_client_config.return_url = global_config.alipay.sandbox_return_url
        # 【可选，否则自己查询】notify_url 用户支付成功时通知的地址    POST    异步通知 支付宝服务器主动通知商户服务器里指定的页面http/https路径
        alipay_client_config.notify_url = global_config.alipay.sandbox_notify_url

        return DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
        # 实例化客户端




