"""刻度线长度设置"""

import time
import dash
from dash import set_props, Patch, html
from dash import Input, Output, State, ClientsideFunction
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from loguru import logger

from server import app

# 刻度线长度设置布局
import views.core_pages.graduated_scale as graduated_scale


# 刻度线长度设置回调
@app.callback(
    [
        Output("top-scale-label", "children"),
        Output("left-scale-label", "children"),
    ],
    [
        Input("listen-element-size-container", "width"),
        Input("listen-element-size-container", "height"),
        Input("drag-container-inner", "_height"),  # 拖拽布局区域大小
    ],
    [
        State("drag-module-size-container", "height"),
    ],
    prevent_initial_call=True,
)
def set_drag_help_line(width, height, _height, module_height):
    if not _height:
        return dash.no_update
    if not width or not height:
        return dash.no_update
    if int(height) > int(_height):
        height = height
    else:
        height = _height

    scale_height = module_height + 100 if module_height + 60 > height else height
    logger.info(f"刻度线长度设置回调: {width}, {height}, {module_height}")

    return [
        graduated_scale.top_layout(extent=width),
        graduated_scale.left_layout(extent=scale_height),
    ]
