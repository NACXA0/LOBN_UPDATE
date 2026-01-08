# 信息检索地图
import uuid



# region 需要注册的地图

page_map = {    # 页面映射
        ("index", "0695f538-b4e4-7521-8000-479e0f78d3fb"),
        ("test", "0695f53a-73e4-77de-8000-28a10c0c1833"),
        ("login", "0695f53f-f111-7929-8000-9aed7c6bc284"),
        ("setting", "0695f540-03b9-7d73-8000-7cd5a31822d2"),
        # 在这里添加更多的页面映射
    }

# endregion

# region 下面是检索逻辑

'''
根据uuid查找页面
需要注册新页面到这里
'''
def get_page_by_uuid(uuid: str | uuid.UUID, by_uuid: bool = True) -> str | bool:
    '''
    根据uuid查找页面
    :param uuid: 页面uuid
    :param by_uuid: 是否按uuid查找，默认按uuid查找
    :return: 对应的uuid字符串或者页面名称
    '''
    # 如果是UUID对象转为字符串
    if isinstance(key, uuid.UUID):
        key = str(key)

    

    for name, page_uuid in page_map:
        if search_by_uuid:
            # 正向：输入是UUID，匹配元组第2个元素，返回第1个
            if key == page_uuid:
                return name
        else:
            # 反向：输入是Name，匹配元组第1个元素，返回第2个
            if key == name:
                return page_uuid
                
    return False


# endregion



if __name__ == "__main__":
    print(get_page_by_uuid("0695f540-03b9-7d73-8000-7cd5a31822d2", by_uuid=True))



