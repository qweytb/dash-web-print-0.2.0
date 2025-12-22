import re
import dash
from dash import html, set_props, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from feffery_dash_utils.version_utils import (
    check_python_version,
    check_dependencies_version,
)

from server import app
from views import core_pages  # 核心页面
from configs.router_config import RouterConfig  # 路由配置参数
from views.status_pages import _404, _500  # 各状态页面

# 导入配置参数
from configs.base_config import BaseConfig


# 检查Python版本
check_python_version(min_version="3.8", max_version="3.13")
# 检查关键依赖库版本
check_dependencies_version(
    rules=[
        {"name": "dash", "specifier": ">=3.1.1,<4.0.0"},
        {"name": "feffery_antd_components", "specifier": ">=0.4.0,<0.5.0"},
        {"name": "feffery_utils_components", "specifier": ">=0.3.2,<0.4.0"},
        {"name": "feffery_dash_utils", "specifier": ">=0.2.6"},
    ]
)

app.layout = lambda: fuc.FefferyTopProgress(
    [
        # 全局消息提示
        fac.Fragment(id="global-message"),
        # 全局页面刷新
        fuc.FefferyReload(id="global-reload"),
        # 根节点url监听
        fuc.FefferyLocation(id="root-url"),
        # 布局助手参数设置
        dcc.Store(
            id="layout-helper-config",
            storage_type="local",
            data=BaseConfig.layout_helper_config,
        ),
        # 缓存操作的元素
        dcc.Store(id="cache-element", storage_type="session"),
        # 缓存浏览器指纹
        dcc.Store(
            id="element-browser-fingerprint",
            storage_type="local",
        ),
        # 添加防止调试 ，开发模式不添加
        fuc.FefferyDebugGuardian(strategy="infinite-debugger") if not BaseConfig.deploy_env == "dev" else None,
        # 应用根容器
        html.Div(
            id="root-container",
        ),
    ],
    id="layout-top-progress",
    minimum=0.33,
    color="#1677ff",
    manual=True,
)


app.clientside_callback(
    # 基于https://github.com/thumbmarkjs/thumbmarkjs
    "() => ThumbmarkJS.getFingerprint().then(fp => fp)",
    Output("element-browser-fingerprint", "data"),
    Input("element-browser-fingerprint", "id"),
)


def handle_root_router_error(e):
    """处理根节点路由错误"""

    set_props(
        "root-container",
        {
            "children": _500.render(e),
        },
    )


# 路由认证回调
@app.callback(
    Output("root-container", "children"),
    Input("root-url", "pathname"),
    State("root-url", "trigger"),
    prevent_initial_call=True,
    on_error=handle_root_router_error,  # 错误处理
    running=[[Output("layout-top-progress", "spinning"), True, False]],  # 显示进度条
)
def root_router(pathname, trigger):
    """根节点路由控制"""

    # 在动态路由切换时阻止根节点路由更新
    if trigger != "load":
        return dash.no_update

    # 演示专用页面展示
    if pathname == "/404-demo":
        return _404.render()
    if pathname == "/500-demo":
        return _500.render()

    # 检查当前访问目标pathname是否为有效页面
    if pathname in RouterConfig.valid_pathnames.keys():
        return core_pages.layout()
    else:
        # 返回404状态页面
        return _404.render()


if __name__ == "__main__":
    # 非正式环境下开发调试预览用
    # 生产环境推荐使用gunicorn启动
    app.run(host="0.0.0.0", port=8050, debug=True)
