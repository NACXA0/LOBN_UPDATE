#共用state
import reflex as rx
import global_config, time, random, asyncio, datetime, uuid
from decimal import Decimal
from sqlmodel import Session, select
from .DataBase_function.database import engine
from .DataBase_function.models import user, user_login_history
#from .public_function import logic_scend_sms, random_user_name, yield_on_datetime_index, yield_on_datetime_index_real_time, make_an_appointment_template_check_is_time_now



class BaseState(rx.State):
    user_uuid: str
    user_money_can_only_be_show: str    #显示的余额（余额用Decimal存储，str显示）
    user_name: str
    user_phone_number: str
    user_vip_level: int #个人vip等级
    identity: str   #当前的身份
    identity_vip_level: int #此身份的vip等级





# 登录逻辑 （所有函数都对basestate依赖，所以直接继承）

class state_login(BaseState):
    text_login_state: str = '登录'    #登录状态展示
    color_login_state: str = 'green'    #登录状态展示

    # 登录-根据uuid，写入必要数据到state里
    @rx.event
    def write_user_info_to_state(self, user_uuid: uuid.UUID):
        '''
        根据uuid，查找数据库，提取用户信息。
        :param user_uuid: 用户uuid
        '''
        with Session(engine) as session:
            # 1. 在数据库里查询对uuid的用户
            info_line = session.exec(select(user).where(user.uuid == user_uuid)).first()  # 找到的数据行
            # 2. 提取用户信息,并写入到state
            self.user_uuid = str(user_uuid)
            self.user_money_can_only_be_show = str(round(info_line.money, global_config.config_money.round_num))  # 展示用户金钱
            self.user_name = str(info_line.name)  # 展示用户昵称
            self.user_phone_number = str(info_line.phone_number)  # 展示用户手机号

    # 重新登陆-清除state信息
    @rx.event
    def relogin(self):
        # 1. 记录注销历史记录-如果登录的话
        if self.user_uuid:
            with Session(engine) as session:
                session.add(user_login_history(user_uuid=str(self.user_uuid), action=False, ip=self.router.session.client_ip))
                session.commit()
        # 2. 修改状态
        self.text_login_state, self.color_login_state = '登录', 'green'    #登陆状态转为为未登录
        print('用户', str(self.user_uuid), '重新登录。')
        self.user_uuid = ""
        self.user_money_can_only_be_show = '0.00'  #清除余额显示
        self.user_name = ""
        self.user_phone_number = ""
        return [rx.clear_local_storage(), rx.redirect("/login")]  # clear_local_strange就是一次清除所有缓存

    # 检查是否登录，决定是否跳转到登录页
    @rx.event
    async def check_login_or_not(self, need_login: bool = True, on_page_login: bool = False):  # 这是通用的检测是否登录  关于这个有时会执行很多次:每次焦点切换都会执行一次，而不是页面加载时执行一次
        '''
        检查是否已经登录   一般：需要登录的页面则可以无参数,  不需要登录的页面则need_login=False  登录页面特殊
        :param need_login:  是否需要登录。 True且未登录则转到登陆界面    默认用need_login=True而不是need_login  是为了防止on_load在编程时忘记添加而导致报错，在登录（可见私有内容）与不登录（不可见私有内容）的架构下，登录比不登录更保险。
        :param on_page_login:  是否在登录页面。在的话且已经登录，则去主页。  默认用False是因为一般都不是在登录页面，编程更方便。
        :return:

        合并了以前的：state_login.change_login_state_show,  # 根据登陆状态，决定登录/注销按钮显示那个
        '''
        if self.user_uuid == "":
            self.text_login_state, self.color_login_state = '登录', 'green'
            if need_login:
                #print('跳转到登陆页面。未登录')  # 【临时测试】
                return rx.redirect("/login")  # 是因为redirect执行不成功（跳转到本页面）就会触发多次执行此函数吗？
        else:
            self.text_login_state, self.color_login_state = '注销', 'red'
            if on_page_login:
                return rx.redirect("/")  # 已经登录了还来登陆页面。是来捣乱的。回主页去吧。


