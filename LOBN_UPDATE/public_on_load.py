# on_load  高于所有页面，所有页面在加载时进行的判断  如是否登录
'''
on_load的等级特别高，高于所有页面
是因为on_load可能使用任意页面内部的state的function，所以必须高于所有页面   （因此才从public_state中独立出来）
'''
import reflex as rx
from .public_state import state_login

#on_load每个页面加载时调用的函数
class state_on_load_in_page(rx.State): #各个页面的加载时要做的事情配置     页面加载很可能使用basestate，所以直接继承。
    # 用法：!!多件要做的事情，使用**列表**!!所有页面都需要这个函数，然后在app.py里的路由中使用on_load这个函数【使用@rx.app的on_load有些地方用不了】
    #注意！！不能使用append（会报错）！！试验发现最好的方法是现在这样：
        #给on_load的函数列表 = [
        #       函数1，
        #       函数2
        #   ]
        #   return 给on_load的函数列表


    #下面是注册页面加载时调用的函数

        
    # 下面是登录页面加载时调用的函数
    @rx.event
    def on_load_in_page_login(self):
        print('页面的on_load：login')
        return [  #第一个是need_on_load, 第二个是need_on_load_in_page
            #state_login.check_login_or_not(False, '/', True),  # 检查是否登录，决定是否跳转到登录页
        ]

    
    @rx.event
    def on_load_in_page_setting(self):
        print('页面的on_load：setting')
        return [  #第一个是need_on_load, 第二个是need_on_load_in_page
            #state_login.check_login_or_not(False, '/', True),  # 检查是否登录，决定是否跳转到登录页
        ]



