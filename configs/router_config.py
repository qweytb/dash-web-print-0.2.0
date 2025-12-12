import re
from typing import List, Union


class RouterConfig:
    """路由配置参数"""

    # 与应用首页对应的pathname地址
    index_pathname: str = "/index"

    # 有效页面pathname地址 -> 页面标题映射字典
    valid_pathnames: dict = {
        "/": "票据打印设计器",
        "/designer": "票据打印设计器",
    }
