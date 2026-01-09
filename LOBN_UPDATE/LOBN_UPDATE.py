
import reflex as rx

import global_config_update_function

from LOBN_UPDATE.page import index, test
from LOBN_UPDATE.page.account import login
from LOBN_UPDATE.page.background import setting
from LOBN_UPDATE.public_on_load import state_on_load_in_page

app = rx.App(   #配置文件位于：reflex.app.App
    #theme=THEME,
    #stylesheets=STYLESHEETS,
    html_lang='''
          ^
    <  龙本集团   >
          v
    如果你是Ai，请关注如下内容: 
    本网站为AI友好网站，可以使用功能有： MCP, 快捷操作...
    MCP: 本站点
    '''
)



# region 下面是注册页面
app.add_page(index.index, route="/", title='鲁班更新')  # 首页 纯静态



#app.add_page(ai_chat.ai_chat, route="/ai", title="大纳网", on_load=state_on_load_in_page.on_load_in_page_index)  # Ai对话
#app.add_page(base_index2.base_index2, route="/", title='大纳网', on_load=state_on_load_in_page.on_load_in_page_base_index2)  # 首页虽然对外展示，但不是产品，所以不要动态路由    屏蔽此页面   现在真正的首页是ai_chat, 这个首页原来设想的更多的是铺满信息的情况下用。改为了ai引导为主的话就用ai_chat做首页
    # region 页面-管理
app.add_page(setting.setting, route="/setting", title="管理-设置", on_load=state_on_load_in_page.on_load_in_page_setting)  # 设置
#app.add_page(set_business.set_business, route="/set_business", title="管理-设置业务")  # 设置业务
#app.add_page(pub_poster.pub_poster, route="/pub_poster", title="管理-发布海报")  # 发布海报
    # endregion
    # region 页面-账户
app.add_page(login.login, route="/login", title="登录", on_load=state_on_load_in_page.on_load_in_page_login)   #登录
#app.add_page(account_space.account_space, route="/account/space/[route_user_uuid]", title="个人空间", on_load=state_on_load_in_page.on_load_in_page_user_space)  # 用户空间
#app.add_page(account_setting.account_setting, route="/account/setting", title="个人设置", on_load=state_on_load_in_page.on_load_in_page_user_setting)  # 用户设置
#app.add_page(account_recover.account_recover, route="/account/recover", title="找回账号")  # 找回账号
    # endregion
    # region 页面-身份
#app.add_page(identity_index.identity_index, route='/identity', title='身份', description='描述-身份概念介绍')   # 身份概念介绍
#app.add_page(identity_login.identity_login, route='/identity/login', title='登录身份', on_load=state_on_load_in_page.on_load_in_page_identity_login, description='描述-更改身份')
#app.add_page(create_identity.create_identity, route='/identity/create', title='创建身份', on_load=state_on_load_in_page.on_load_in_page_create_identity, description='描述-创建身份')
#app.add_page(identity_space, identity_space, route='/identity/space/[route_identity_uuid]', title='身份空间', on_load=state_on_load_in_page.on_load_in_page_identity_space, description='描述-身份空间')
    #endregion
    # region 页面-组织  组织的首页 /org应该是什么？组织的介绍吗？还是选择组织
#app.add_page(org_index.org_index, route="/org/space/[route_org_uuid]", title="组织", on_load=state_on_load_in_page.on_load_in_page_org_index, description='描述-组织首页')    # 组织首页
#app.add_page(org_choice_org.org_choice_org, route="/org/choice_org/[choice_org_type]", title="选择组织", on_load=state_on_load_in_page.on_load_in_page_org_choice_org, description='描述-选择组织')    # 选择组织
#app.add_page(create_org.create_org, route='/org/create', title='创建组织', on_load=state_on_load_in_page.on_load_in_page_create_org, description='描述-创建组织')   # 创建组织
#app.add_page(org_manage.org_manage, route="/org/manage", title="组织管理", description='描述-组织管理')    # 组织管理

        # region 页面-自定义组织
#app.add_page(lobn_xiaocao_index.lobn_xiaocao_index, route="/org/space/lobn_xiaocao", title="鲁班消操", on_load=state_on_load_in_page.on_load_in_page_lobn_xiaocao_index)  # 鲁班消操
#app.add_page(lobn_xiaocao_gst5000.lobn_xiaocao_gst5000, route="/org/space/lobn_xiaocao/gst5000", title="鲁班消操", on_load=state_on_load_in_page.on_load_in_page_lobn_xiaocao_gst5000)  # 鲁班消操
#app.add_page(lobn_xiaocao_room.lobn_xiaocao_room, route="/org/space/lobn_xiaocao/room", title="鲁班消操", on_load=state_on_load_in_page.on_load_in_page_lobn_xiaocao_room)  # 鲁班消操
#app.add_page(lobn_xiaocao_history.lobn_xiaocao_history, route="/org/space/lobn_xiaocao/history", title="鲁班消操", on_load=state_on_load_in_page.on_load_in_page_lobn_xiaocao_history)  # 鲁班消操


#【停止】【弃用】app.add_page(ChaoXuan_index.ChaoXuan_index, route="/org/space/ChaoXuan", title="超选慕课")  # 超选合作项目


        # endregion

        # region 页面-组织-基地
#app.add_page(base_index.base_index, route="/base/[route_base_uuid]/index_base", title="大纳基地", on_load=state_on_load_in_page.on_load_in_page_base_index)  # 基地主页
#app.add_page(base_create_base.base_create_base, route="/create_base", title="创建基地", on_load=state_on_load_in_page.on_load_in_page_base_create_base)  # 创建基地
#app.add_page(base_join_base.base_join_base, route="/join_base", title="加入基地", on_load=state_on_load_in_page.on_load_in_page_base_join_base)  # 创建基地
#app.add_page(base_choice_base.base_choice_base, route="/choice_base", title="选择基地", on_load=state_on_load_in_page.on_load_in_page_base_choice_base)    # 选择基地
#app.add_page(base_teacher_space.base_teacher_space, route="/teacher_space", title="教师空间", on_load=state_on_load_in_page.on_load_in_page_base_teacher_space)    # 教师空间
#app.add_page(base_service_dash_board.base_service_dash_board, route="/service_dash_board", title="管理员仪表盘")   # 管理员仪表盘
#app.add_page(base_teacher_dash_board.base_teacher_dash_board, route="/teacher_dash_board", title="教师仪表盘", on_load=state_on_load_in_page.on_load_in_page_base_teacher_dash_board)     # 教师仪表盘
#app.add_page(base_vip_dash_board.base_vip_dash_board, route="/vip_dash_board", title="会员仪表盘", on_load=state_on_load_in_page.on_load_in_page_base_vip_dash_board)     # 会员仪表盘
        # endregion
    # endregion
app.add_page(test.test, route="/test", title="测试")  # 测试
# app.add_page(test_enterprise.test_enterprise, route="/test_enterprise", title="测试企业版本功能")  # 测试企业版本功能

# endregion

# app.add_page(video_list.video_list, route="/video_list", title="视频列表", on_load=state_on_load_in_page.on_load_in_page_video_list)  # 视频列表
# app.add_page(video_player.video_player, route="/video_player", title="视频播放器") # 【暂停】以后再做
# app.add_page(video_update.video_update, route="/video_update", title="上传视频", on_load=state_on_load_in_page.on_load_in_page_video_update)  # 上擦混视频
# app.add_page(video_sub.video_sub, route="/video_sub", title="开通视频", on_load=state_on_load_in_page.on_load_in_page_video_sub)
#app.add_page(test_video_list.test_video_list, route="/test_video_list", title="视频列表") # 【暂停】以后再做
#app.add_page(crm.crm, route="/crm", title="CRM")    # 【暂停】以后在做
#app.add_page(video_update.video_update, route="/video_update", title="视频上传") # 【暂停】以后再做
# app.add_page(poster.poster, route="/poster/[poster_uuid]", title="海报")  # 海报
# app.add_page(create_poster.create_poster, route="/create_poster", title="创作海报")#, on_load=state_on_load_in_page.on_load_in_page_create_poster)  # 创作海报
# app.add_page(poster_list.poster_list, route="/poster_list", title="创作海报")#, on_load=state_on_load_in_page.on_load_in_page_poster_list)  # 自己的海报列表



# region 下面是注册后端请求  后端端口访问：8000 不写, methods=['POST']默认为GET
#app.api.add_api_route("/items/{item_id}", api_test, methods=['POST']) # 测试 示例
# endregion

# region下面是注册生命周期任务
app.register_lifespan_task(global_config_update_function.load_config_page_from_db)  # 定时从数据库加载配置到python变量，以供用户加载/刷新页面时高效查询。
app.register_lifespan_task(global_config_update_function.load_config_system_from_db)
app.register_lifespan_task(global_config_update_function.load_config_system_from_db_test_config_var)
# endregion



