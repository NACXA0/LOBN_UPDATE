# 登录页
# 0695f53f-f111-7929-8000-9aed7c6bc284
'''
可学习内容：检测按钮事件
登录+注册
因为是无密码机制，所以只要有手机号、邮箱等与一个实体绑定即可，而个性化设置则可以通过检测是不是新账号来根据规则自动跳转到设置。没注册则自动注册
【待改进】增加功能：request_url    在url传入，登陆后跳转到那个url（因为点击了需要登录的应用，所以在来到登录，登陆后再回去），不填则转到主页。
'''

import rxconfig
import reflex as rx
import asyncio, datetime, time, uuid
from WEB_DaNa.public_state import state_login, BaseState, state_redis_pubsub, public_background, state_for_identity
from WEB_DaNa.public_function import logic_scend_sms, random_user_name
from sqlmodel import Session, select, desc
from WEB_DaNa.DataBase_function.database import engine
from WEB_DaNa.DataBase_function.models import user, user_login_history, identity
from uuid_extensions import uuid7, uuid7str


'''
添加登陆渠道需要注意的：
    1.添加跳转到各个前端组件的**按钮**们的!逻辑!
    2.添加组件（注意官网教程（自动建立的看不见的方法）：set_函数名）
    3.添加cond的唯一选择。
'''
'''
代码结构变更1：
    函数：
        1. async def function_login_by_code(self)
        2. def component_login_form() -> rx.Component:
    原因：为了复用发送验证码的逻辑，将独立的发送验证阿门转为使用ComponentState来共用state
    迁移目标：public_component的use_on_login_form（登录界面用的表单）这个preset_component_use（选择组件使用方法）
    新调用方法：state_verify_code.create(preset_component_use='use_on_login_form')
代码结构变更2：
    函数：
        1. async def function_login_by_code(self)
        2. def component_login_form() -> rx.Component:
    原因：代码结构变更1虽然复用了state，但是component却强制都迁移到了一个地方，这太乱了。
        对于代码结构变更1，现在有了优化方案->见下面的新结构说明
    新结构说明：component还迁移回来，知识state使用ComponentState中的State
    新调用方法：pass
代码结构变更3：
    又改回代码结构变更1了，componentstate问题太大了！！
    这个发送验证码这一块暂时先乱着吧，耦合性强一点，其他的不这么做，等以后reflex有了共享state再分出来。
    还没解决的问题：ComponentState内部的事件处理程序如何调用内部的其他是事件处理程序？
代码结构变更4：
    受不了了，ComponentState就连返回都只能指定具体的实例，可我是要self呀，这还怎么复用？
    全改回来了，改为验证码表单有很多分，每个页面都有独特的一份
    再共享state出来之气那尽量避免ComponentState！！
'''

#region 下面是为具体页面而实例化的ComponentState
#【弃用，等以后又共享state了再改】instance_verify_code_form_for_login = verify_code_form()   #实例化的ComponentState验证码表单_为了登陆页面的表单
#endregion


#下面是state
class state(rx.State):
    '''
    验证码验证系统
    关于使用rx.ComponentState将此复用为子状态的实现方法：
        一个rx.ComponentState仅可创建一个组件，对于有多个复用组件的情况，需要在其组件部分使用match来选择性return。
    '''
    # region 1. 变量
    _verify_code_create_date = "0.0"  # 验证码创建时间
    _verify_code: str = ''  # 生成的验证码
    verify_phone_number_input: str = ''  # 客户端提交的手机号
    _verify_phone_number: str = ''  # 发送验证码的手机号
    verify_code_input: str = ''  # 客户端提交的验证码
    lock_send_verify_code_button: bool = False  # 禁用发送验证码按钮
    send_verify_code_button_show: str = '程序错误！请用rx.cond主动设置按钮默认文字'  # 发送验证码按钮显示的内容
    # endregion

    # region 2. 事件处理程序
    # 发送验证码按钮用
    @rx.event
    async def function_submit_verify_code(self):
        '''
        发送验证码流程：
            2. 前置条件判断：输入的电话号码是否合规
            3. 前置条件判断：发送不过于频繁
            通过了前置条件 -》
            4. 记录发送验证码的手机号【防止发送后变更手机号】
            5. 生成并发送验证码
            6. 更新验证码发送时间
            7. 临时禁用发送验证码按钮
        '''
        # 2. 前置条件判断：输入的电话号码是否合规  电话号码的格式不合规不会报错，但发不出去)
        if not self.verify_phone_number_input.isdigit():
            return rx.toast.error('请输入正确的手机号')
        # 3. 前置条件判断：发送不过于频繁
        if time.time() - float(self._verify_code_create_date) < rxconfig.verify_code.send_sms_freq:
            return rx.window_alert("请稍后再试，验证码请求过于频繁。")  # 这里用aleart，强制选择确认框后再继续
        # 通过了前置条件 -》
        # 4. 记录发送验证码的手机号
        self._verify_phone_number = self.verify_phone_number_input
        # 5. 生成并发送验证码
        self._verify_code = logic_scend_sms.generate_verify_code()  # 创建验证码
        try:
            await logic_scend_sms.main_async(int(self._verify_phone_number), self._verify_code)  # 发送验证码
        except:
            return rx.toast.error('验证码发送失败')
        # 6. 更新验证码发送时间
        self._verify_code_create_date = str(time.time())
        return [state.change_send_verify_code_button_show(),  # 7. 临时禁用发送验证码按钮,
                rx.toast.success('验证码已发送')]


    # 检查验证码
    @rx.event
    def function_check_verify_code(self):  # 登陆按钮用   检查BaseState里的验证码，并返回通过与否。
        '''
        检查验证码：
            1. 前置条件判断：是否已经发送验证码
            2. 前置条件判断：现有的验证码是否已经过期
            3. 前置条件判断：验证码是否输入正确
            4. 到此验证码认证通过

            需要 1. 临时存储验证码，2. 验证码有效期
            隐含问题：发送验证码后，用另一个账户登录（需要将发送验证码的手机号与验证码绑定），否则就是：先发送验证码的发错了，要用另一个手机号登录。         一个登陆限制：验证码输入错误或与发送验证码的id不匹配
        '''
        # 1. 前置条件判断：是否已经发送验证码
        if not self._verify_code:
            return False, rx.toast.warning("请先发送验证码")
        # 2. 前置条件判断：现有的验证码是否已经过期
        if time.time() - float(self._verify_code_create_date) >= rxconfig.verify_code.verify_code_effective_time:  # 验证码过期
            return False, rx.toast.error("验证码已过期，请重新发送。")
        # 3. 前置条件判断：验证码是否输入正确
        if (self.verify_phone_number_input != self._verify_phone_number) or (self.verify_code_input != self._verify_code):  # 手机号或验证码任一不相等。   用不等而不是等于，不等更简单-》任何不符，直接拒绝。
            return False, rx.toast.error("请重新输入，验证码输入错误，")
        # 4. 到此验证码认证通过，返回通过验证码的手机号
        return True, self._verify_phone_number

    # 点击发送验证码后按钮延迟 只管如何禁用send_verify_code_button_show，需要设置默认文字   禁用按钮->开始倒计时->解锁
    @rx.event(background=True)
    async def change_send_verify_code_button_show(self, count_down: int = rxconfig.verify_code.send_sms_freq):
        '''
        调用方法：
        rx.button(
            rx.cond(instance_verify_code_form_for_login.State.lock_send_verify_code_button,
                instance_verify_code_form_for_login.State.send_verify_code_button_show,
                "这里是未锁定时按钮显示的文字",
            ),
            disabled=instance_verify_code_form_for_login.State.lock_send_verify_code_button,
            on_click=instance_verify_code_form_for_login.State.function_submit_verify_code()  # 提交按钮【新提交方法】
        ),

        将此注册为background的原因：锁定按钮UI有时是与其他事件同时发生的（如rx.toast）,改为background可以相当于并发事件，否则得等另一个事件结束才可以触发。
        '''
        if not self.lock_send_verify_code_button:
            async with self:
                self.lock_send_verify_code_button = True
            while count_down > 0:
                async with self:
                    self.send_verify_code_button_show = str(count_down) + '秒后重发'  # 1.显示倒计时
                await asyncio.sleep(1)  # 2.等待
                count_down -= 1  # 3.更新记时
                yield
            async with self:
                self.lock_send_verify_code_button = False

    # 清除用于验证的state
    @rx.event
    def clear_verify_state(self):
        self._verify_code = self.verify_phone_number_input = self.verify_code_input = ""

    @rx.event
    async def function_login_by_code(self):
        '''
        写入登录信息到state
            1.在数据库里查询对应手机号的用户的uuid
                1.1注册：数据库找不到用户信息
                1.2注册后再找一边，确认信息成功写入用户数据库。
            2.写入从数据库找到的用户信息到state
            3.记录最新登陆时间
            4. 修改展示的登陆状态
            5.清除登陆验证信息，防止退出后还能再短时间内使用同样的验证码登录。(注意！不能重置验证码时间，因为登录时间也包含验证码发送倒计时内)（必须要重新获取一次验证码，走一遍流程）
            6.登陆成功，跳转。
            7.启动账户相关的后台任务
        '''
        # 1. 验证验证码
        is_pass, user_phone_number = self.function_check_verify_code()
        if not is_pass:
            return user_phone_number
        get_state_login = await self.get_state(state_login)
        # 2. 在数据库里查询对应手机号的用户的uuid
        with Session(engine) as session:
            # 1.1 查找用户信息
            user_select_command = select(user).where(user.phone_number == user_phone_number)
            user_info_line = session.exec(user_select_command).first()
            # 1.2找不到返回None -> 进行注册 （第一次找有没有注册）
            if not user_info_line:
                # 1.2.1.1.1 构造用户数据
                user_uuid = uuid7
                user_name = random_user_name
                user_money = '0'
                user_level = 0
                user_privilege_level = 10
                user_privilege_select = rxconfig.user.default_user_signin_privilege_select
                # 1.2.1.1.2 构造会员身份数据
                identity_uuid = uuid7
                identity_name = user_name
                identity_level = 0
                identity_privilege_level = 10
                identity_privilege_select = None
                identity_tip = '账号注册第一会员身份'
                identity_slogan = '账号注册第一会员身份'

                # 1.2.1.2.1 创建数据行——用户数据
                session.add(user(uuid=user_uuid, name=user_name, phone_number=user_phone_number, last_login_date=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")))
                # 1.2.1.2.2 创建数据行——会员身份
                session.add(identity(uuid=identity_uuid, type='vip', user_uuid=user_uuid, name=user_name, tip=identity_tip, slogan=identity_slogan, last_login_date=datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")))
                # 1.2.1.3 提交
                try:
                    session.commit()  # 提交
                except:
                    return rx.toast.error('注册失败！')
            else:
                # 1.2.2.1 构造用户数据
                user_uuid = user_info_line.uuid
                user_name = user_info_line.name
                user_money = user_info_line.money
                user_level = user_info_line.level
                user_privilege_level = user_info_line.privilege_level
                user_privilege_select = user_info_line.privilege_select

                # 1.2.2.2 查找最近登录的会员身份   （只有注册过才需要查找）
                command_identity_recent = select(identity).where(identity.user_uuid == user_uuid).order_by(desc(identity.last_login_date)).limit(1)
                identity_recent_info_line = session.exec(command_identity_recent).first()
                if not identity_recent_info_line:   # 注册身份失败，单注册用户成功
                    return rx.window_alert('程序错误！注册用户的时候没有注册会员身份')
                # 1.2.2.3 构造会员身份数据
                identity_uuid = identity_recent_info_line.uuid
                identity_name = identity_recent_info_line.name
                identity_level = identity_recent_info_line.level
                identity_privilege_level = identity_recent_info_line.privilege_level
                identity_privilege_select = identity_recent_info_line.privilege_select
                identity_tip = identity_recent_info_line.tip
                identity_slogan = identity_recent_info_line.slogan

            # 2.1 写入用户信息到state
            base_state = await self.get_state(BaseState)
            base_state.user_uuid = str(user_uuid)
            base_state.user_money_can_only_be_show = str(round(user_money, rxconfig.config_money.round_num))  # 展示用户金钱
            base_state.user_name = user_name  # 展示用户昵称
            base_state.user_phone_number = user_phone_number  # 展示用户手机号
            base_state.user_level = user_level  # 用户等级
            base_state.user_privilege_level = user_privilege_level  # 用户权限等级
            base_state.user_privilege_select = user_privilege_select    # 用户权限配置
            # 2.2 写入会员身份信息到state
            get_identity_state = await self.get_state(state_for_identity)
            get_identity_state.identity_uuid = identity_uuid
            get_identity_state.identity_type = 'vip'
            get_identity_state.identity_name = identity_name
            get_identity_state.level = identity_level
            get_identity_state.privilege_level = identity_privilege_level
            get_identity_state.privilege_select = identity_privilege_select
            get_identity_state.tip = identity_tip
            get_identity_state.slogan = identity_slogan
            # 3. 记录最新登陆时间
            user_info_line.last_login_date = str(datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S"))
            # 记录登录历史记录
            session.add(user_login_history(user_uuid=str(user_uuid), action=True, ip=self.router.session.client_ip))
            session.commit()
        # 4. 修改展示的登陆状态
        get_state_login.text_login_state, get_state_login.color_login_state = '注销', 'red'
        # 5. 清除登陆验证信息。  防止退出后还能再短时间内使用同样的验证码登录。(注意！不能重置验证码时间，因为登录时间也包含验证码发送倒计时内)（必须要重新获取一次验证码，走一遍流程）
        self.clear_verify_state()
        return [
            rx.redirect(self.router.url.query_parameters.get('redirect_to', '/')),  # 6. 登陆成功，跳转到传参来的页面
            rx.toast.success("登陆成功！")
            #【暂停约时间系统】public_background.make_an_appointment_time_is_up  # 7. 启动到时间提示的后台任务
        ]

    # endregion

# region 3. 用于组成主组件的组件模块
def login_form() -> rx.Component:
    return rx.vstack(
        rx.text(
            "手机号",
            size="3",
            weight="medium",
            text_align="left",
            width="100%",
        ),
        rx.input(  # 手机号/邮箱输入框
            rx.input.slot(rx.icon("user")),
            placeholder="手机号",
            type="number",
            size="3",
            width="100%",
            on_blur=state.set_verify_phone_number_input,  # 检测事件【新提交方法】
        ),

        rx.hstack(
            rx.text("验证码", size="3", weight="medium", ),
            justify="between",
            width="100%",
        ),
        rx.flex(
            rx.input(  # 验证码输入框
                rx.input.slot(rx.icon("lock")),
                placeholder="验证码",
                type="number",
                size="3",
                width="100%",
                on_blur=state.set_verify_code_input,  # 检测事件【新提交方法】
                #这里增加键盘回车检测，回车提交
            ),
            rx.button(
                rx.cond(state.lock_send_verify_code_button,
                    state.send_verify_code_button_show,
                    "发送验证码",
                ),
                disabled=state.lock_send_verify_code_button,
                on_click=state.function_submit_verify_code  # 提交按钮【新提交方法】
            ),  # 验证码提交按钮【这里需要添加阿里云的实人认证】
            direction="row",
            spacing="2",
            width="100%",
        ),

        rx.button("登录",
            size="3",
            width="100%",
            on_click=state.function_login_by_code  # 提交按钮【新提交方法】
            # 这里不加lock_login_button,因为有可能在验证码所应期间就登陆，没有提交验证码是无法登录的，所以不用再加一个判断。
        ),

        # rx.text("新提交方法：为按钮绑定事件", f"{instance_verify_code_form_for_login.State.verify_phone_number_input},{instance_verify_code_form_for_login.State.verify_code_input}"),
    )
# endregion




#下面是主函数
def login() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.image(
                        src="/image_web_info/logo_DaNa.jpg",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("登录",
                       size="6",
                       as_="h2",
                       text_align="center",
                       width="100%",
                    ),
                    justify="start",
                    spacing="4",
                    width="100%",
                ),

                login_form(),

                rx.link("手机号不可用了?", href="/find_account", size="3"),  # 忘记账号需要跳转到帮助中心，申诉找回。
                spacing="6",
                width="100%",
            ),

            size="4",
            max_width="28em",
            width="100%",
        ),

    )

    
