# LOBN_UPDATE
鲁班更新服务复刻

- 设计：
    - RBAC+RPAC
        用户->身份(不同的固定范围的可配置权限组)->【暂停】组织

    - 后台修改全局页面配置的方式：以大量动态var为基础，每次加载页面都查询一次配置文件。（经过论证，虽然不如全静态搞笑，但稳定、可发展）
        1.加载配置文件的方式：
            1.  【更好】后台修改配置文件数据库，本地文件数据库sqlite -> 等待用户主动刷新（或者增加刷新提示）
            每次打开页面都从数据库中查询一次配置。
                - 具体实施方式-防止用户恶意刷新造成数据库压力的方法：
                    python全局进程缓存：
                        python程序级别加一个定时器，定时轮训数据库配置保存为变量 -> 用户的刷新查询都是查询这个python变量
             
            2. 后台修改配置文件（文件名包含时间戳），用户主动刷新（根据时间戳与当前使用的时间戳是否一致判断是否是最新的配置），从文件中读取配置-> 加载到state.var

            - 1更好的原因：
                - ```
                你的逻辑非常清晰，这两种方式在理论上都是完全可行的。
                但在 **Reflex (SSR/长进程)** 的实际工程落地中，**方案 1（数据库）完胜方案 2（配置文件）**。
                为什么看似“轻量级”的配置文件方案反而不如数据库？让我们深入对比一下你提出的这两个流程，看看“坑”在哪里。
                ---
                ### 1. 数据库存储方案（你的方案 1）
                > **流程**：用户刷新 -> 查库 -> 返回数据。
                > **后台**：更新 DB 记录。
                *   **分析**：
                    *   **优点**：这是最标准的 Web 开发范式。SQLite/Postgres 专门为了“多读多写”设计，自带行级锁、事务隔离。
                    *   **你担心的“恶意刷新压力”**：
                        *   正如我们之前讨论的，利用 **Buffer Pool (内存缓存)** 和 **连接池复用**，实际上 1000 次刷新可能只有 1 次真正触碰到磁盘 IO。
                        *   数据库引擎对 SQL 解析和内存查找的优化程度，远超你用 Python 手写文件读取逻辑。
                *   **结论**：**可行且推荐。**
                ---
                ### 2. 配置文件存储方案（你的方案 2）
                > **流程**：用户刷新 -> 读取文件 (判断时间戳) -> 解析 JSON。
                > **后台**：覆盖写入新的 JSON 文件。
                这个方案在**单体脚本**（比如每天跑一次的爬虫）里很完美，但在 **SSR Web 服务**里有三个致命隐患：
                #### 隐患一：并发读写冲突（最危险）
                *   **场景**：
                    1.  用户 A 刷新页面 -> Python 进程打开 `config.json` 准备读取。
                    2.  恰好此时，管理员后台点击保存 -> Python 进程准备**写入** `config.json`。
                    3.  **结果**：在 Linux 系统中，正在写入的文件如果被读取，可能会读到**空数据**或者**写了一半的乱码 JSON**。
                    4.  **后果**：前端拿到损坏的 JSON，解析报错，页面直接白屏。
                *   **数据库的优势**：数据库会自动处理这种锁。写的时候，读操作会排队或者读旧的快照，绝不会读到“写了一半”的数据。
                #### 隐患二：JSON 解析的 CPU 成本
                *   **数据库方式**：`SELECT value FROM config`。数据库把字符串吐出来，直接赋值。
                *   **文件方式**：`json.load(open('config.json'))`。
                    *   每次刷新都要执行一次反序列化。如果配置很复杂，CPU 消耗会比简单的 DB 查询更高。
                    *   虽然你可以判断“时间戳”，但 `os.path.getmtime()` 也是一次系统调用（IO），并没有省多少事。
                #### 隐患三：容器化部署的噩梦
                *   Reflex 部署通常在 **Docker 容器**里。
                *   容器的文件系统通常是**只读**或**临时的**。
                *   如果你上传了新配置文件，重启容器后，文件可能会变回原来的镜像版本（除非你挂载了 Volume，但这增加了运维复杂度）。
                *   数据库是外部持久化存储，不存在这个问题。
                ---
                ### 修正后的“最佳实践”逻辑
                如果你想兼顾“文件的便捷”和“数据库的安全”，可以采用**“文件作为源头，数据库作为缓存”**的架构，这通常是大型系统的做法：
                1.  **开发阶段**：
                    *   你在本地维护一个 `config.json` 文件（方便 Git 管理）。
                2.  **部署/初始化阶段**：
                    *   服务启动时，Python 检查数据库里是否有配置。
                    *   如果没有，读取 `config.json` -> **写入数据库**。
                    *   之后的所有读写，**完全基于数据库**。
                3.  **后台修改阶段**：
                    *   管理员在网页改配置 -> **直接更新数据库**（不碰文件）。
                    *   （可选）如果要持久化到文件，可以提供一个“导出配置”按钮，手动触发把 DB 数据写回 `config.json`。
                ### 总结
                *   **不要**在 Web 服务运行期间频繁覆盖读取本地文件。这会引入并发锁风险和部署复杂性。
                *   **请使用数据库**。它就是专门为了解决“高并发读写一致性”而生的工具。你担心的性能问题，在现代数据库架构下几乎不存在。

                ```
        2. 不要主动通知前端刷新！会导致前端突变，用户体验差。
        3. ！！对于确定的不变配置还是用静态配置文件的方式，比如数据库、证书、超管账户！！




    - 后台修改网站运行逻辑配置的方式：原理同上。-> global_config.py
      - 不直接查数据库，利用数据库缓存的原因：查数据库需要很多的网络开销，而变量或着redis的开销很低（redis缓存的方案以后需要多进程优化再考虑）
      - 配置数据数据库-[低频同步]->全局python变量-[用户主动刷新（以后做主动同步）]->state.var   同一个变量有python变量和state.var两种
      - 这里存储系统的全局配置数据、网站运行逻辑等。比如开关开发者模式、底层条件频率限制、与网站的运行逻辑有关，使得可以在后台配置网站的运行方式。
      - 实现在不停机的情况下对网站运行进行控制
      - 更新方式：
        1. 当前：on_load 用户主动刷新则改变。
        2. 以后：高频同步。**尚且未知怎么做。**
            reflex如何实现一个事件处理器在用户处于某页面（聚焦于此页面更好）的时候才运行（或者周期性运行），否则不运行或者能触发什么中断条件？
            比如当用户处在页面时才使用不断获取某某数据的函数。 
      - 造成的影响：
        1. 原来的一些rxconfig里的参数（与网站运行相关）要转移进来。
        2. 现在rxconfig里只有更加必要的配置数据，如数据库、认证信息等（网站属性相关定义）
    - 



较之前项目的修改内容：
    1. 弃用privilege_level权限等级：
       1.  这个的设计哲学是便于权限配置。然而，权限应该是具体的，各种权限总体大小难以判断，然对于这里的简单配置这个需求而言，应该是**不同的默认权限配置，这是应该是全局的预设配置方式才对，而非属于个体的**。
       2.  原始设计哲学2:在权限变化时，依照权限等级自动更改权限配置。**新的权限也应该是由具体的权限组成的，在应用新的权限配置时应该使用一套是否可以具有新权限的判断流程**，而非简单地根据权限等级这个指标判断是否该应用新的权限配置。从这个角度来说，也应该弃用权限等级。
    2. 组织所有者用户（owner_user_uuid）和组织超级管理员用户（super_admin_user_uuid）改为组织所有者身份（owner_identity_uuid）和组织超级管理员身份（super_admin_identity_uuid）:
        - 组织不直接与用户沟通，必须通过身份。（审计及历史责任问题，可以通过身份用户修改记录溯源。）
    3. sqlmodel的模型字段定义参数：“nullable=False” ：非空(如果定义了外键则不用显示写nullable=False，因为外键默认非空) 
    4. org表去除：extra_data_uuid: str  # 附加字段表的数据的uuid
    附加字段依靠于org，的外键是org.uuid,而不是反过来。
    5. SQLModel对数据类型的支持进化了，以前很多需要用str，现在都原生支持了。比如：datetime、uuid、
    6. 将rxconfig中不属于reflex本身的部分分离，出来是一个global_config全局python变量缓存，有结构地存储等待赋值的python变量，内部的生命周期程序（这里时私有的函数）定期从数据库获取最新配置。
    7. 


业务内容：
    订单
    城市
    员工
    财务
    业务分类
    售后
    客户
    前台展示
    活动
    通知




### 设计方案
- 检测登录用户/用户单点登录（含多进程）： 现在单进程版直接用本地变量。
    每一个进程运行一开始都声称一个id->每个用户登录时都写入公共redis（用户id+进程id）—-》
    1. 用户退出redis收不到用户实例发来的心跳，则redis根据用户id删除数据 
    2. 进程结束redis心跳收不到进程回应，则redis根据进程删除数据




- 文件结构的调用等级：越小越底层，只有高层可以调用底层，底层不能调用高层
    1. global_config、DataBase_funcfion/models    # 全局python变量缓存，如系统设置、全局页面设置等 # 以后改为redis-om的模型文件 如果改了：基础数据、模版类、静态末端配置文件，没有引用关系
    2. DataBase_funcfion/database、global_config_instace    # 长连接实例，有些依赖数据与模版
    3. global_config_get    获取全局python变量的生命周期函数
    4. public_state、public_function
    5. public_component
    6. public_template 模板高于组件，因为组件组成模板
    7. public_web_tool.video_player、 
    8. page 【这里是私有内容，可以调用前面的公有内容】
    9.  public_on_load on_load可能使用任意页面内部的state的function，所以必须高于所有页面 【此处使用到了公有与专有的内容，需要提权】
    10. LOBN_UPDATE、rxconfig 【这里有app的实例化，也有基础设置、激活此处的实例的程序(为了不传参地激活)】仅reflex的config




## 缓存与前后台配置专栏
- 三种缓存的讲解（简略）：
  1. global_config  数据缓存-以后改为redis-om的模版，
  2. global_config_update_function  更新数据缓存的函数，通常是从数据糊获取数据，然后加入缓存
  3. global_config_instance  实例化的缓存，有长连接等非静态数据的“变量”。
- 缓存变量基本代码架构示例——用户主动刷新。    高频同步以后再说，还不知道怎么做。    redis缓存的方案以后需要多进程优化再考虑
    配置信息数据库->python全局变量->state.var
    - ``` python 前端设置+显示： 
        import reflex as rx
        import global_config
        from sqlmodel import Session, select
        from LOBN_UPDATE.DataBase_function.database import engine
        from LOBN_UPDATE.DataBase_function.models import config_system
        from LOBN_UPDATE.public_function import random_user_name
        class state(rx.State):
            config_page: dict = {}
            config_system: dict = {}
            config_test_var: str  # 测试用的变量，后台配置修改后会更新此变量的值
            
            @rx.event
            def test_update_config_var(self, new_value: dict):
                # 模拟更新配置变量的操作
                
                # 写入数据库
                with Session(engine) as session:
                    session.add(config_system(
                        value=new_value['new_value'], 
                        value_type='str', 
                        name=f'测试后台设置值({random_user_name()})',
                        tip='这是一个用于测试的后台设置值',
                        create_user_uuid='06960ab6-bd3d-739d-8000-ec86da6176d5'
                    ))
                    session.commit()

                return rx.toast.success('配置已更新！')

            # 加载-主动刷新以更新
            def load_config_system_from_var_test(self):
                self.config_test_var = global_config.test_config_var
                print('state.var主动刷新加载配置：', self.config_test_var)
                
        @rx.page(on_load=state.load_config_system_from_var_test)
        def setting() -> rx.Component:
            return rx.box(
                rx.card(
                    rx.text('测试后台设置值：', state.config_test_var),
                    rx.form(
                        rx.input(placeholder='新值', name='new_value'),
                        rx.button('提交', type='submit'),
                        on_submit=state.test_update_config_var
                    )

                )
            )
    ```
    - ``` python 全局python变量
        test_config_var: str = '初始值'  # 测试用的变量，后台配置修改后会更新此变量的值
    ```
    - ``` python 从数据库获取配置数据
        # 生命周期任务-定时查询系统配置数据库->写入python程序变量
        async def load_config_system_from_db_test_config_var():
            try:
                while True:
                    # 查询系统配置数据库
                    # '占位-查询一次系统配置数据库'
                    with Session(engine) as session:
                        # 1. 在数据库里查询对uuid的用户
                        response = session.exec(select(config_system)).all()  # 找到的数据行
                        # '占位-将系统配置数据行写入到对应的python变量中'
                        out = response[random.randint(0, len(response)-1)]
                        if response:
                            global_config.test_config_var = out.value

                    await asyncio.sleep(5)  # 每几秒查询一次
            except asyncio.CancelledError:
                print("程序因错误而关闭: async def load_config_page_from_db():")
    ```
    - ``` python 将函数“从数据库获取配置数据”注册为生命周期任务在后台运行
        app.register_lifespan_task(global_config_update_function.load_config_system_from_db_test_config_var)
    ```







