"""辅助布局的设置和回调"""

import time
import dash
from dash import set_props, Patch, html
from dash import Input, Output, State, ClientsideFunction
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from loguru import logger

from server import app

# 辅助线布局
import views.core_pages.drag_help as drag_help

# 导入配置
from configs.base_config import BaseConfig


# 添加布局辅助线
@app.callback(
    [
        Output("main-layout-container", "children"),
    ],
    [
        Input("help-lengthways-top", "nClicks"),
        Input("help-crosswise-left", "nClicks"),
    ],
    [
        State("main-layout-container", "children"),
        State("listen-element-size-container", "width"),
        State("listen-element-size-container", "height"),
    ],
    prevent_initial_call=True,
)
def add_drag_help_line(
    lengthways_click,  # 横线点击
    crosswise_click,  # 竖线点击
    layout_children,  # 拖拽布局
    container_width,  # 布局主容器宽度
    container_height,  # 布局主容器高度
):
    """添加纵向或横向辅助线"""
    # 1. 谁触发了回调
    triggered = dash.ctx.triggered_id or ""  # 防止 None 报错
    # 2. 决定类型 + 尺寸
    if "lengthways" in triggered:
        help_type, extent = "lengthways", container_height
    elif "crosswise" in triggered:
        help_type, extent = "crosswise", container_width
    else:
        return dash.no_update  # 无关触发 → 不更新

    # 3. 生成辅助线
    logger.info(f"添加布局辅助线，类型：{help_type}，尺寸：{extent}")
    new_line = drag_help.help_layout(help_type=help_type, extent=extent)

    # 4. 追加到孩子列表
    new_children = [new_line] if layout_children is None else [*layout_children, new_line]
    logger.info(f"更新：{help_type}，布局容器辅助线")
    return [new_children]


# 网格辅助线
@app.callback(
    [
        Output("layout-helper-config", "data"),
        Output("grid-lines-layout", "children"),
        Output("drag-gridding-adsorb", "checked"),  # 是否开启网格吸附
    ],
    Input("help-gridding-centre", "nClicks"),
    State("layout-helper-config", "data"),
    prevent_initial_call=True,
)
def grid_lines_layout(nClicks, data):
    """
    网格线开关控制
    返回 (data, 网格线元素)
    """
    triggered = dash.ctx.triggered_id

    show_grid = data["show_grid"]

    logger.info(f"【网格线】当前状态：{show_grid}")
    # ① 首次加载已开启网格 → 直接渲染
    if show_grid and not nClicks:
        logger.info("【网格线】初始状态为开启，直接渲染网格线")
        return data, drag_help.help_layout("gridding"), True

    # ② 未点击按钮 → 不处理
    if not nClicks or "gridding" not in triggered:
        return dash.no_update

    # ③ 切换显示状态
    show_grid = not show_grid
    data["show_grid"] = show_grid

    if show_grid:
        logger.info("【网格线】已开启，组件将自动吸附网格")
        return data, drag_help.help_layout("gridding"), True
    else:
        logger.info("【网格线】已关闭，取消吸附功能")
        return data, [], False


# 纸张的缩放
@app.callback(
    [
        Output("layout-helper-config", "data", allow_duplicate=True),
        Output("help-zoom-in-text", "children"),
        Output("drag-container-inner-style", "rawStyle"),
    ],
    [
        Input("help-zoom-in", "nClicks"),
        Input("help-zoom-out", "nClicks"),
    ],
    [
        State("layout-helper-config", "data"),
        State("drag-module-size-container", "width"),
        State("drag-module-size-container", "height"),
    ],
    prevent_initial_call=True,
)
def zoom_in(zoom_in, zoom_out, zoom_data, width, height):
    """缩放比例调整"""

    if not zoom_in and not zoom_out:  # 无触发
        logger.info(f"【缩放比例】无触发器，返回 no_update, 显示当前比例")
        zoom_data["zoom_scale"] = 1.0
        return (
            zoom_data,
            f"{zoom_data['zoom_scale'] * 100:.0f}%",
            dash.no_update,
        )

    if not BaseConfig.enable_zoom_canvas:
        set_props(
            "global-message",
            {
                "children": fac.AntdMessage(
                    content="【提示】当前缩放功能为测试阶段，请勿使用",
                    type="error",
                    maxCount=3,
                )
            },
        )
        return dash.no_update

    triggered = dash.ctx.triggered_id
    logger.info(f"【缩放比例】触发器：{triggered}")

    if "zoom-in" in triggered:
        zoom_data["zoom_scale"] = round(zoom_data["zoom_scale"] + 0.1, 1)
        logger.info(f"【缩放比例】已放大，当前比例：{zoom_data['zoom_scale']}")

    if "zoom-out" in triggered:
        zoom_data["zoom_scale"] = round(zoom_data["zoom_scale"] - 0.1, 1)
        logger.info(f"【缩放比例】已缩小，当前比例：{zoom_data['zoom_scale']}")

    rawStyle = f"""
            #drag-container-inner-layout {{
                position: relative; /* 确保容器是定位上下文 */
                z-index: 1; /* 确保内容在网格上方 */
                transform-origin: 0 0;     /* 左上角 */
                transform: scale({zoom_data["zoom_scale"]});
                transition: transform .2s;                                                   
                # background-color: rgba(0, 0, 0, 0.25);
            }}
            #drag-container-inner {{
                width: {width * zoom_data["zoom_scale"]}px;
                height: {height * zoom_data["zoom_scale"]}px;
            }}
            """

    return zoom_data, f"{zoom_data['zoom_scale'] * 100:.0f}%", rawStyle


# 清除缓存
@app.callback(
    Output("drag-container-inner-layout", "children", allow_duplicate=True),  # 拖拽元素容器
    Output("layout-helper-config", "data", allow_duplicate=True),  # 配置数据
    Output("drag-element-property-attributes-group", "children", allow_duplicate=True),  # 卡片元素列表
    Input("help-delete-data", "nClicks"),
    State("layout-helper-config", "data"),
    prevent_initial_call=True,
)
def clear_pycache(nClicks, data):
    """清除缓存"""
    if not nClicks or "help-delete-data" not in dash.ctx.triggered_id:
        return dash.no_update

    logger.info("【清除缓存】开始清理缓存")
    set_props(
        "global-message",
        {
            "children": [
                fac.AntdMessage(
                    content="【提示】清除当前缓存，删除布局，初始化设定",
                    type="error",
                    maxCount=3,
                ),
                fuc.FefferyReload(delay=2000, reload=True),
            ]
        },
    )
    # 清空布局
    # data["drag_layout_list"] = {}
    data = BaseConfig.layout_helper_config
    return [], data, []
