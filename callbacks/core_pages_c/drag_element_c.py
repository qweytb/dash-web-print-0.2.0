"""拖拽元素的回调模块"""

import time
import dash
from dash import set_props, Patch, html, clientside_callback
from dash import Input, Output, State, ClientsideFunction, ALL
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style
import random
from loguru import logger
import json

from server import app
from views.status_pages import _404
from views.core_pages import drag_element

# 导入工具模块
import utils.pages_utils_def as pages_utils


# 配置模块
from configs.base_config import BaseConfig


# 拖拽元素的设置和布局
@app.callback(
    [
        Output("drag-container-inner-layout", "children"),
        Output("layout-helper-config", "data", allow_duplicate=True),
        Output("drag-element-property-attributes-group", "children", allow_duplicate=True),  # 生成卡片选择器
        Output("cache-element", "data", allow_duplicate=True),  # 缓存操作元素
    ],
    [
        Input("listen-drop-element", "dropEvent"),  # 拖拽组件的信息
        Input("drag-container-inner", "position"),  # 拖拽布局区域的坐标
        Input("listen-scroll-container-inner", "position"),  # 滚动布局区域的坐标
        Input("drag-element-transverse-click", "nClicks"),  # 横线点击
        Input("drag-element-vertical-click", "nClicks"),  # 竖线点击
        Input("drag-element-rectangle-click", "nClicks"),  # 矩形点击
        Input("drag-element-text-click", "nClicks"),  # 文本点击
        Input("drag-element-picture-click", "nClicks"),  # 图片点击
        Input("drag-element-qrcode-click", "nClicks"),  # 二维码点击
        Input("drag-element-barcode-click", "nClicks"),  # 条形码点击
        Input("drag-element-table-click", "nClicks"),  # 表格点击
    ],
    [
        State("drag-container-inner-layout", "children"),  # 拖拽布局区域的子组件
        State("drag-gridding-adsorb", "checked"),  # 是否开启网格吸附
        State("layout-helper-config", "data"),  # 布局配置数据
    ],
    prevent_initial_call=True,
)
def listen_drop_element(
    dropEvent,  # 拖拽数据
    div_position,  # 拖拽布局区域的坐标
    scroll_position,  # 滚动布局区域的坐标
    transverse,  # 横线
    vertical,  # 竖线
    rectangle,  # 矩形
    text,  #  文本
    picture,  # 图片
    qrcode,  # 二维码
    barcode,  # 条形码
    table,  # 表格
    layout_children,  # 拖拽布局
    checked,  # 是否开启网格吸附
    data,  # 配置数据
):
    """
    监听画布 drop 事件，生成并追加新元素
    """
    # ① 匹配元素
    element_types = ["transverse", "vertical", "rectangle", "text", "picture", "qrcode", "barcode", "table"]
    triggered = dash.ctx.triggered_id
    if not (transverse or vertical or rectangle or text or picture or qrcode or barcode or table) and not dropEvent:
        # return dash.no_update
        raise dash.exceptions.PreventUpdate  # 阻止回调执行

    # 匹配元素 标识符 确定其类型或类别
    element_type = next((ele for ele in element_types if ele in triggered), None)
    if not element_type:
        if dropEvent:
            element_type = dropEvent.get("data").get("info")

    logger.debug(f"【listen_drop_element】生成的元素：{element_type}")
    x, y = 0, 0
    # ③ 计算绝对坐标
    if "click" in triggered:
        x = random.randint(0, 100)
        y = random.randint(0, 100)
    if "listen-drop-element" in triggered:
        raw_x = dropEvent["pageX"] - div_position["x"]
        raw_y = dropEvent["pageY"] - div_position["y"] + scroll_position["top"]
        x, y = int(raw_x), int(raw_y)
        logger.debug(f"【listen_drop_element】原始坐标：({x},{y})")

    # ④ 开启网格吸附
    if checked:
        # x = (x // 20) * 20
        # y = (y // 20) * 20
        x = x - x % 20 if x % 20 < 10 else x + (20 - x % 20)
        y = y - y % 20 if y % 20 < 10 else y + (20 - y % 20)
        logger.debug(f"【listen_drop_element】网格吸附后坐标 -> ({x},{y})")

    # ⑥ 生成元素布局
    deag_layout = drag_element.drag_element_layout(
        element_type=element_type,
        element_x_y={"x": x, "y": y},
    )
    # 获取返回的元素和对应的属性
    element_data = deag_layout["element"]
    deag_layout = deag_layout["rnd"]

    logger.debug(f"【listen_drop_element】缓存的布局元素数据：{element_data}")
    data["drag_layout_list"][element_data["element_id"]] = element_data

    logger.info(f"【listen_drop_element】成功创建元素：{element_type} @({x}, {y})")

    # ⑦ 追加到画布
    new_children = [deag_layout] if layout_children is None else [*layout_children, deag_layout]

    logger.debug("【listen_drop_element】返回新 children 长度：{}", len(new_children))

    # 获取该元素的表单
    # element_form = drag_element.element_property_attributes_layout(
    #     element_config=element_data,
    # )
    # 初始化元素ID 卡片选择
    drag_rnd_id = element_data["element_id"]

    drag_layout_list = data.get("drag_layout_list")
    # 获取布局元素卡片
    element_children = drag_element.drag_element_list(drag_layout_list)

    return (
        new_children,
        data,
        element_children,
        drag_rnd_id,
    )


# 已经布局到画布的拖拽元素器
@app.callback(
    [
        Output("drag-container-inner-layout", "children", allow_duplicate=True),  # 拖拽布局
        Output("layout-helper-config", "data", allow_duplicate=True),  # 布局助手配置
        # Output("drag-element-property-attributes-form", "children", allow_duplicate=True),  # 属性配置表单
        Output("cache-element", "data"),  # 缓存操作元素
    ],
    [
        Input({"type": "RND", "id": ALL}, "key"),  # 拖拽元素器key
        Input({"type": "RND", "id": ALL}, "position"),  # 坐标
        Input({"type": "RND", "id": ALL}, "size"),  # 坐标
    ],
    [
        # State("drag-element-property-attributes-group", "value"),  # 获取选中的卡片值
        State("drag-container-inner-layout", "children"),  # 拖拽布局区域的子组件
        State("drag-gridding-adsorb", "checked"),  # 是否开启网格吸附
        State("layout-helper-config", "data"),  # 布局配置数据
    ],
    prevent_initial_call=True,
)
def drag_element_rnd_layout(
    rnd_key,
    rnd_position,
    rnd_size,
    # value,
    layout_children,
    checked,
    data,
):
    """拖拽元素"""

    if not len(layout_children):  # 拖拽元素不存在
        logger.warning("【拖动随机元素】未找到拖拽元素，返回 no_update")
        return dash.no_update

    triggered = dash.ctx.triggered

    if not triggered:
        logger.warning("【拖动随机元素】未找到触发源，返回 no_update")
        return dash.no_update

    # 调试：打印所有参数
    logger.debug(f"【拖动随机元素】检查网格吸附状态：{checked}")
    logger.debug(f"【拖动随机元素】layout_children数量：{len(layout_children)}")
    logger.debug(f"【拖动随机元素】data keys：{list(data.keys())}")

    # 如果 checked 是字符串（从某个状态获取），尝试转换
    if isinstance(checked, str):
        checked = checked.lower() == "true"
        logger.debug(f"【拖动随机元素】转换后的checked值：{checked}")

    # 获取触发源信息
    prop_id_str = triggered[0]["prop_id"] if triggered else ""
    logger.debug(f"【拖动随机元素】触发源原始字符串：{prop_id_str}")

    # 解析 prop_id 字符串，支持多种格式
    trigger_id = None
    import re

    if "#" in prop_id_str:
        # 格式: "type#id.property"
        parts = prop_id_str.split("#")
        trigger_id = parts[1].split(".")[0]  # 获取 id 部分
    else:
        # 可能是 JSON 字符串，如 {"id":"3c0a9980-2f2b-4354-94a0-e5005df1850d","type":"RND"}.position
        # 使用正则提取 id
        id_match = re.search(r'"id"\s*:\s*"([^"]+)"', prop_id_str)
        if id_match:
            trigger_id = id_match.group(1)
        else:
            # 尝试其他格式
            id_match = re.search(r'\{["\']id["\']:\s*["\']([^"\']+)["\']', prop_id_str)
            if id_match:
                trigger_id = id_match.group(1)
            else:
                logger.warning(f"【拖动随机元素】无法从prop_id中提取元素ID：{prop_id_str}")
                trigger_id = None

    # 1. 定位索引
    drag_rnd_id = trigger_id
    if not drag_rnd_id:
        logger.warning("【拖动随机元素】未找到触发元素ID，返回 no_update")
        return dash.no_update

    try:
        idx = next(i for i, full_id in enumerate(rnd_key) if full_id.startswith(drag_rnd_id))
    except StopIteration:
        logger.warning("【拖动随机元素】未找到对应索引，返回 no_update")
        return dash.no_update

    # 判断元素坐标是否有变动
    element_data = data["drag_layout_list"][drag_rnd_id]

    # 读取坐标（只读取一次）
    x, y = rnd_position[idx]["x"], rnd_position[idx]["y"]
    logger.debug(f"【拖动随机元素】触发元素：{drag_rnd_id} 坐标：({x},{y})")

    # 读取坐标与尺寸
    size = rnd_size[idx] or {}
    w = size.get("width", element_data["element_config"].get("width", 0))
    h = size.get("height", element_data["element_config"].get("height", 0))
    # 处理宽高去掉单位
    w = w if w is None else int(w[:-2]) if isinstance(w, str) and w.endswith(("px", "pt", "em", "rem")) else w if isinstance(w, int) else 0
    h = h if h is None else int(h[:-2]) if isinstance(h, str) and h.endswith(("px", "pt", "em", "rem")) else h if isinstance(h, int) else 0
    logger.debug(f"【拖动随机元素】元素尺寸：({w},{h})")

    # 解析元素类型
    element_type = rnd_key[idx].split("+")[1]
    logger.debug(f"【拖动随机元素】元素类型：{element_type}")

    # 🔒 忽略 ≤2px 的抖动（含坐标 & 宽高），防止快速拖动时频繁更新
    old = element_data["element_config"]
    old_x, old_y = int(old.get("x", 0)), int(old.get("y", 0))

    logger.debug(f"【拖动随机元素】检测到移动：({old_x},{old_y}) -> ({x},{y})")

    if abs(x - old_x) <= 2 and abs(y - old_y) <= 2:
        logger.debug(f"【拖动随机元素】忽略微变动({x},{y}), 返回 no_update")
        raise dash.exceptions.PreventUpdate

    # 4. 网格吸附（只在有效移动时才执行吸附）
    if checked:
        logger.debug(f"【拖动随机元素】网格吸附已开启，进行吸附计算")
        # 计算当前网格位置
        current_x = x - x % 20 if x % 20 < 10 else x + (20 - x % 20)
        current_y = y - y % 20 if y % 20 < 10 else y + (20 - y % 20)

        # 只有当坐标变化超过 5px 时才执行吸附，避免微小移动时吸附导致跳回
        if abs(current_x - old_x) > 5 or abs(current_y - old_y) > 5:
            x = current_x
            y = current_y
            logger.debug(f"【拖动随机元素】吸附后坐标：({x},{y})")
        else:
            # 坐标变化很小，保持原坐标不变，避免跳回
            x = old_x
            y = old_y
            logger.debug(f"【拖动随机元素】坐标变化小于阈值，保持原坐标：({x},{y})")
    else:
        logger.debug(f"【拖动随机元素】网格吸附已关闭，保持原坐标：({x},{y})")

    # 5. 删除旧布局
    logger.debug(f"【拖动随机元素】删除前元素数量：{len(layout_children)}")
    layout_children = pages_utils.remove_rnd_by_uuid(rnd_list=layout_children, target_uuid=drag_rnd_id)
    logger.debug(f"【拖动随机元素】删除后元素数量：{len(layout_children)}")

    # 删除元素缓存
    logger.debug(f"【拖动随机元素】从缓存中移除：{drag_rnd_id}")
    logger.debug(f"【拖动随机元素】缓存中所有元素：{list(data['drag_layout_list'].keys())}")
    element_data = data["drag_layout_list"].pop(drag_rnd_id)
    logger.debug(f"【拖动随机元素】元素原始坐标：({element_data['element_config']['x']}, {element_data['element_config']['y']})")
    element_data["element_config"]["x"] = x
    element_data["element_config"]["y"] = y
    logger.debug(f"【拖动随机元素】更新后坐标：({x}, {y})")
    if rnd_size[idx]:
        # 获取组件的宽高
        element_w = rnd_size[idx].get("width")
        element_h = rnd_size[idx].get("height")
        # 获取组件的高度宽度
        element_data["element_config"]["width"] = (
            element_w if element_w is None else int(element_w[:-2]) if isinstance(element_w, str) and element_w.endswith(("px", "pt", "em", "rem")) else element_w if isinstance(element_w, int) else 0
        )
        element_data["element_config"]["height"] = (
            element_h if element_h is None else int(element_h[:-2]) if isinstance(element_h, str) and element_h.endswith(("px", "pt", "em", "rem")) else element_h if isinstance(element_h, int) else 0
        )

    # 获取新元素布局
    logger.debug("【拖动随机元素】获取重新创建新元素布局")
    deag_layout = drag_element.drag_element_layout(element_config=element_data)
    element_data = deag_layout["element"]
    deag_layout = deag_layout["rnd"]

    logger.debug(f"【listen_drop_element】缓存的布局元素数据：{element_data}")
    data["drag_layout_list"][element_data["element_id"]] = element_data

    logger.info(f"【拖动随机元素】新建组件：{element_type} 坐标({x},{y})")

    new_children = [deag_layout] if layout_children is None else [*layout_children, deag_layout]
    logger.debug("【拖动随机元素】返回新 children 长度：{}", len(new_children))

    logger.debug(f"【拖动随机元素】返回操作的元素：{drag_rnd_id}")

    # 去掉所有元素的选中样式，防止和卡片选中样式渲染重复照常闪烁错误
    new_children = pages_utils.select_only_uuid(new_children, None)

    return new_children, data, drag_rnd_id


# 点击拖拽的元素显示属性配置
@app.callback(
    Output("cache-element", "data", allow_duplicate=True),  # 缓存操作元素
    Input({"type": "RND", "id": ALL}, "selected"),  # 选中
    State({"type": "RND", "id": ALL}, "key"),  # 拖拽元素器key
    prevent_initial_call=True,
)
def nClicks_element_property_attributes(
    rnd_selected,  # 选中
    rnd_key,  # 拖拽元素器key
):
    triggered = dash.ctx.triggered_id
    if not triggered:
        return dash.no_update
    drag_rnd_id = triggered["id"]
    dx = next(i for i, full_id in enumerate(rnd_key) if full_id.startswith(drag_rnd_id))

    if not rnd_selected[dx]:
        # logger.debug("【点击拖拽的元素】取消选中元素")
        # return "0"
        raise dash.exceptions.PreventUpdate  # 拦截
    logger.info(f"点击拖拽的元素,选中的元素是: {drag_rnd_id}")
    return drag_rnd_id


# 初始化加载布局
@app.callback(
    Output("drag-container-inner-layout", "children", allow_duplicate=True),  # 拖拽布局
    Output("drag-element-property-attributes-group", "children"),  # 卡片元素列表
    Output("drag-element-property-attributes-form", "children", allow_duplicate=True),  # 属性配置表单
    Output("drag-container-inner-layout", "style", allow_duplicate=True),
    Input("help-refresh-layout", "nClicks"),
    Input("layout-helper-config", "data"),  # 布局配置数据,
    State("drag-container-inner-layout", "children"),  # 拖拽布局区域的子组件
    prevent_initial_call=True,
)
def init_load_layout(nClicks, data, layout_children):
    """初始化加载布局"""

    triggered = dash.ctx.triggered_id
    if "layout-helper-config" in triggered and not layout_children:
        logger.debug("【init_load_layout】初始化加载布局")
        # 获取布局元素
        drag_layout_list = data.get("drag_layout_list")
        # 显示纸张编辑的属性
        drag_canvas = data["drag_canvas"]
        w = drag_canvas.get("m_mm_w")
        h = drag_canvas.get("m_mm_h")
        m_Bkgrd_color = drag_canvas.get("m_Bkgrd_color")
        if not drag_layout_list:
            element_form = drag_element.element_property_attributes_layout(element_config=drag_canvas)
            return (
                dash.no_update,
                dash.no_update,
                element_form,
                style(
                    width=f"{w}mm",
                    height=f"{h}mm",
                    # backgroundColor=m_Bkgrd_color,
                ),
            )
        # 获取布局元素卡片
        element_children = drag_element.drag_element_list(drag_layout_list)

        # # 显示纸张编辑的属性
        # drag_canvas = data["drag_canvas"]
        element_form = drag_element.element_property_attributes_layout(element_config=drag_canvas)

        new_children = []
        for k, v in drag_layout_list.items():
            deag_layout = drag_element.drag_element_layout(element_config=v)
            deag_layout = deag_layout["rnd"]
            new_children.append(deag_layout)

        return new_children, element_children, element_form, style(width=f"{w}mm", height=f"{h}mm")

    return dash.no_update


# 缓存的拖拽元素操作id
@app.callback(
    Output("drag-element-property-attributes-group", "value", allow_duplicate=True),  # 设定选中的元素
    Input("cache-element", "data"),  # 获取拖拽元素操作的元素ID
    prevent_initial_call=True,
)
def drag_element_cache_id(drag_element):
    if not drag_element:
        return dash.no_update
    logger.info(f"缓存的拖拽元素操作id，设定卡片选项: {drag_element}")
    return drag_element


# 选择卡片元素编辑属性
@app.callback(
    [
        Output("drag-element-property-attributes-form", "children", allow_duplicate=True),  # 属性配置表单
        Output("drag-element-data-source-scrollbar", "children"),  # 数据源
        Output("drag-container-inner-layout", "children", allow_duplicate=True),  # 拖拽布局
    ],
    [
        Input("drag-element-property-attributes-group", "value"),  # 获取选中的元素
    ],
    [
        State("layout-helper-config", "data"),  # 布局配置数据,
        State("drag-container-inner-layout", "children"),  # 拖拽布局区域的子组件
    ],
    prevent_initial_call=True,
)
def select_card_element_property_attributes(rnd_element, data, layout_children):
    """选择卡片元素编辑属性"""
    if not rnd_element:  # 未选择元素
        logger.debug(f"【选择卡片元素编辑属性】未选择元素，返回纸张元素属性")
        drag_canvas = data["drag_canvas"]
        element_form = drag_element.element_property_attributes_layout(element_config=drag_canvas)
        # 获取元素的动态字段配置
        element_dynamic_field = drag_element.data_source_layout()

        # 去掉所有元素的选中样式，防止和卡片选中样式渲染重复照常闪烁错误
        new_children = pages_utils.select_only_uuid(layout_children, None)
        return element_form, element_dynamic_field, new_children

    logger.debug(f"【选择卡片元素编辑属性】已选择元素，返回元素属性{rnd_element}")
    element_data = data["drag_layout_list"].get(rnd_element, None)
    if not element_data:
        # # 显示纸张编辑的属性
        # drag_canvas = data["drag_canvas"]
        # element_form = drag_element.element_property_attributes_layout(element_config=drag_canvas)
        # logger.debug(f"【选择卡片元素编辑属性】未获取元素属性表单{rnd_element}")
        # # 只更新表单，不改动数据源和布局
        # return element_form, dash.no_update, dash.no_update
        raise dash.exceptions.PreventUpdate  # 阻止更新
    else:
        # 获取该元素的表单
        element_form = drag_element.element_property_attributes_layout(
            element_config=element_data,
        )
        logger.debug(f"【选择卡片元素编辑属性】已获取元素属性表单{rnd_element}")

        # 获取元素的动态字段配置
        element_dynamic_field = drag_element.data_source_layout(
            element_type=element_data["element_type"],
        )

        # 操作的元素设置成选中
        new_children = pages_utils.select_only_uuid(layout_children, rnd_element)
        logger.debug(f"【选择卡片元素编辑属性】已操作元素, 给布局的属性加上选中样式{rnd_element}")

        return element_form, element_dynamic_field, new_children


# 删除元素
@app.callback(
    Output("drag-container-inner-layout", "children", allow_duplicate=True),  # 拖拽布局
    Output("drag-element-property-attributes-group", "children", allow_duplicate=True),
    Output("layout-helper-config", "data", allow_duplicate=True),  # 布局配置数据,
    Output("drag-element-property-attributes-group", "value", allow_duplicate=True),  # 卡片选择
    Input("element-from-del", "nClicks"),
    State("drag-container-inner-layout", "children"),  # 拖拽布局区域的子组件
    State("element-property-attributes-form", "values"),  # 元素属性表单
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def delete_element(nClicks, layout_children, values, data):
    if not (nClicks and len(layout_children)):
        return dash.no_update

    logger.info("【删除元素】点击了元素删除按钮")

    # 1. 获取布局元素id
    component_id = values.get("component_id", None)
    logger.info(f"【删除元素】删除的元素id为：{component_id}")

    drag_layout_list = data.get("drag_layout_list")

    # 删除旧布局配置
    del drag_layout_list[component_id]
    data["drag_layout_list"] = drag_layout_list

    # print(drag_layout_list)

    # if not drag_layout_list:
    #     return dash.no_update
    # 获取布局元素卡片
    element_children = drag_element.drag_element_list(drag_layout_list)

    # 5. 删除旧布局
    new_children = pages_utils.remove_rnd_by_uuid(rnd_list=layout_children, target_uuid=component_id)

    return new_children, element_children, data, None


# 获取拖拽的动态字段
@app.callback(
    Output("element-property-attributes-form", "values"),
    Input("drop-element-data-source", "dropEvent"),
    State("element-property-attributes-form", "values"),
    prevent_initial_call=True,
)
def get_drag_element_property_attributes(dropEvent, values):
    if not dropEvent:
        return dash.no_update
    drop = dropEvent.get("data").get("info")
    if values.get("text", None):  # 存在text字段，则更新
        values["text"] = drop
    if values.get("value", None):  # 存在value字段，则更新
        values["value"] = drop
    if values.get("src", None):  # 存在src字段，则更新
        values["src"] = drop
    values["style"] = "variation"
    return values


# 保存元素属性
@app.callback(
    [
        Output("drag-container-inner-layout", "children", allow_duplicate=True),  # 拖拽布局
        Output("layout-helper-config", "data", allow_duplicate=True),  # 布局配置数据,
        Output("drag-element-property-attributes-group", "value", allow_duplicate=True),  # 卡片选择
        Output("drag-container-inner-layout", "style"),
    ],
    [
        Input("element-from-submit", "nClicks"),
    ],
    [
        State("element-property-attributes-form", "values"),
        State("layout-helper-config", "data"),  # 布局配置数据,
        # State("drag-container-inner", "_width"),  # 拖拽布局区域大小
        # State("drag-container-inner", "_height"),  # 拖拽布局区域大小
    ],
    prevent_initial_call=True,
)
def drag_element_from_submit(nClicks, values, data):
    if not nClicks:
        return dash.no_update

    if "m_id" in values:
        logger.info("这是编辑纸张元素属性,更新")
        # raise dash.exceptions.PreventUpdate  # 阻止更新
        return (
            dash.no_update,
            dash.no_update,
            dash.no_update,
            style(width=f"{values['m_mm_w']}mm", height=f"{values['m_mm_h']}mm"),
        )
    else:
        drag_layout_list = {}
        component_id = values.get("component_id", "")
        if component_id:
            drag_layout_list = data.get("drag_layout_list")
            element_config = drag_layout_list.get(component_id).get("element_config")
            # 移除ID值
            del values["component_id"]

            drag_layout_list[component_id]["element_config"] = {**element_config, **values}

            data["drag_layout_list"] = drag_layout_list

        new_children = []
        for k, v in drag_layout_list.items():
            deag_layout = drag_element.drag_element_layout(element_config=v)
            deag_layout = deag_layout["rnd"]
            new_children.append(deag_layout)

        return new_children, data, component_id, dash.no_update


# 目标属性向防抖属性的同步建议使用浏览器端回调，一行js就搞定
app.clientside_callback(
    """values => values""",
    Output("element-property-attributes-form-debounce", "sourceProp"),
    Input("element-property-attributes-form", "values"),
    prevent_initial_call=True,
)


# 拖动元素的防抖回调
app.clientside_callback(
    """
    (x, y, old_x, old_y) => {
        // 如果坐标变化很小，返回 no_update
        if (Math.abs(x - old_x) < 2 && Math.abs(y - old_y) < 2) {
            return null;
        }
        return {x, y, old_x, old_y};
    }
    """,
    Output("drag-element-position-cache", "data"),
    [
        Input({"type": "RND", "id": ALL}, "position"),
    ],
    State("drag-element-position-cache", "data"),
    prevent_initial_call=True,
)


# 表单属性随着元素属性变化
@app.callback(
    Output("element-property-attributes-form", "values", allow_duplicate=True),
    Output("layout-helper-config", "data", allow_duplicate=True),  # 布局配置数据,
    Input("element-property-attributes-form-debounce", "debounceProp"),
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def element_property_attributes_form(values, data):
    if not values:
        raise dash.exceptions.PreventUpdate  # 阻止更新
    if not "m_id" in values:
        raise dash.exceptions.PreventUpdate  # 阻止更新

    drag_canvas = data["drag_canvas"]
    paper_type = values.get("m_paper_type")
    ele_w_h = BaseConfig.paper.get(paper_type)

    if drag_canvas["m_paper_type"] != paper_type:
        drag_canvas["m_paper_type"] = paper_type
        values["m_mm_w"] = ele_w_h.get("w_mm")
        values["m_mm_h"] = ele_w_h.get("h_mm")

    if drag_canvas["m_mm_w"] != values["m_mm_w"]:
        drag_canvas["m_mm_w"] = values["m_mm_w"]

    if drag_canvas["m_mm_h"] != values["m_mm_h"]:
        drag_canvas["m_mm_h"] = values["m_mm_h"]

    if drag_canvas["m_Bkgrd_color"] != values["m_Bkgrd_color"]:
        drag_canvas["m_Bkgrd_color"] = values["m_Bkgrd_color"]

    # {'m_id': '1234567', 'm_name': '测试模版', 'm_paper_type': 'A3', 'm_mm_w': '210', 'm_mm_h': '297', 'm_px_w': '210', 'm_px_h': '297', 'm_pages_num': '1', 'm_Bkgrdp': '1', 'm_Bkgrd_color': '#ffffff'}
    data["drag_canvas"] = drag_canvas
    logger.debug(f"设置纸张类型，{paper_type}")

    return values, data


# 保存画布的px属性
@app.callback(
    Output("layout-helper-config", "data", allow_duplicate=True),  # 布局配置数据,
    Input("drag-container-inner", "_width"),  # 拖拽布局区域大小
    Input("drag-container-inner", "_height"),  # 拖拽布局区域大小
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def drag_container_inner_px(width, height, data):
    if not width or not height:
        return dash.no_update

    drag_canvas = data["drag_canvas"]
    drag_canvas["m_px_w"] = width
    drag_canvas["m_px_h"] = height

    data["drag_canvas"] = drag_canvas

    return data
