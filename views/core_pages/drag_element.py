"""拖拽元素的设置和布局"""

from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
import uuid
from typing import Any

# 导入回调模块
import callbacks.core_pages_c.drag_element_c as drag_element_c


# 配置模块
from configs.base_config import BaseConfig


# 转成纯字典
def _to_dict(obj: Any) -> Any:
    """递归把 Dash 组件对象→字典"""
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_dict(i) for i in obj]
    # 真正的组件对象
    if hasattr(obj, "to_plotly_json"):
        return obj.to_plotly_json()
    if hasattr(obj, "props") and hasattr(obj, "type"):
        return {
            "type": obj.type,
            "namespace": getattr(obj, "namespace", None),
            "props": _to_dict(obj.props),
        }
    return obj


# 拖拽元素页首布局
def layout():
    return fac.AntdSpace(
        [
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素横线
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-transverse",
                            data={"info": "transverse"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    html.Div(
                                        style=style(
                                            width=40,
                                            borderBottom="4px solid #FFF",
                                            borderRadius=10,
                                        ),
                                    ),
                                    fac.AntdCenter(
                                        "横线",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                        ),
                                    ),
                                ],
                                size=3,
                                direction="vertical",
                            ),
                            id="drag-element-transverse",
                            style=style(
                                height=45,
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-transverse-click",
                    className="hover-div",
                ),
                content="元素：横线",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素竖线
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-vertical",
                            data={"info": "vertical"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    html.Div(
                                        style=style(
                                            height=30,
                                            borderLeft="4px solid #FFF",
                                            borderRadius=5,
                                        ),
                                    ),
                                    fac.AntdCenter(
                                        "竖线",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                            width=10,
                                        ),
                                    ),
                                ],
                                size=3,
                            ),
                            id="drag-element-vertical",
                            style=style(
                                height=45,
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-vertical-click",
                    className="hover-div",
                ),
                content="元素：竖线",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素矩形
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-rectangle",
                            data={"info": "rectangle"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdCenter(
                                        fac.AntdIcon(
                                            icon="antd-border",
                                            style=style(
                                                fontSize=20,
                                                color="#ffffff",
                                            ),
                                        )
                                    ),
                                    fac.AntdCenter(
                                        "矩形",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                            # width=10,
                                        ),
                                    ),
                                ],
                                size=0,
                                direction="vertical",
                            ),
                            id="drag-element-rectangle",
                            style=style(
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-rectangle-click",
                    className="hover-div",
                ),
                content="元素：矩形",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdDivider(
                direction="vertical",
                lineColor="red",
                className={"height": "35px"},
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素文字
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-text",
                            data={"info": "text"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdIcon(
                                        icon="antd-file-text",
                                        style=style(
                                            fontSize=20,
                                            color="#ffffff",
                                        ),
                                    ),
                                    fac.AntdCenter(
                                        "文字",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                        ),
                                    ),
                                ],
                                size=0,
                                direction="vertical",
                            ),
                            id="drag-element-text",
                            style=style(
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-text-click",
                    className="hover-div",
                ),
                content="元素：文字",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素图片
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-picture",
                            data={"info": "picture"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdIcon(
                                        icon="antd-picture",
                                        style=style(
                                            fontSize=20,
                                            color="#ffffff",
                                        ),
                                    ),
                                    fac.AntdCenter(
                                        "图片",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                        ),
                                    ),
                                ],
                                size=0,
                                direction="vertical",
                            ),
                            id="drag-element-picture",
                            style=style(
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-picture-click",
                    className="hover-div",
                ),
                content="元素：图片",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素二维码
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-qrcode",
                            data={"info": "qrcode"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdCenter(
                                        fac.AntdIcon(
                                            icon="antd-qrcode",
                                            style=style(
                                                fontSize=20,
                                                color="#ffffff",
                                            ),
                                        )
                                    ),
                                    fac.AntdCenter(
                                        "二维码",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                        ),
                                    ),
                                ],
                                size=0,
                                direction="vertical",
                            ),
                            id="drag-element-qrcode",
                            style=style(
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-qrcode-click",
                    className="hover-div",
                ),
                content="元素：二维码",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素条形码
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-barcode",
                            data={"info": "barcode"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdCenter(
                                        fac.AntdIcon(
                                            icon="antd-bar-code",
                                            style=style(
                                                fontSize=20,
                                                color="#ffffff",
                                            ),
                                        )
                                    ),
                                    fac.AntdCenter(
                                        "条形码",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                        ),
                                    ),
                                ],
                                size=0,
                                direction="vertical",
                            ),
                            id="drag-element-barcode",
                            style=style(
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-barcode-click",
                    className="hover-div",
                ),
                content="元素：条形码",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            fac.AntdDivider(
                direction="vertical",
                lineColor="red",
                className={"height": "35px"},
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    [
                        # 绑定需要拖拽的元素表格
                        fuc.FefferyListenDrag(
                            targetSelector="#drag-element-table",
                            data={"info": "table"},
                        ),
                        fac.AntdCenter(
                            fac.AntdSpace(
                                [
                                    fac.AntdCenter(
                                        fac.AntdIcon(
                                            icon="bi-table",
                                            style=style(
                                                fontSize=20,
                                                color="#ffffff",
                                            ),
                                        )
                                    ),
                                    fac.AntdCenter(
                                        "表格",
                                        style=style(
                                            fontSize=12,
                                            color="#ffffff",
                                        ),
                                    ),
                                ],
                                size=0,
                                direction="vertical",
                            ),
                            id="drag-element-table",
                            style=style(
                                cursor="grab",  # 鼠标手势
                            ),
                        ),
                    ],
                    id="drag-element-table-click",
                    className="hover-div",
                ),
                content="元素：表格",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
        ],
        size=20,
        style=style(
            width="35%",
            height="100%",
        ),
    )


# 布局元素列表
def drag_element_list(drag_layout_list):
    check_card_list = []
    for element in drag_layout_list.values():
        element_type = element.get("element_type")
        if element_type == "transverse":
            children = fac.AntdSpace(
                [
                    html.Div(
                        style=style(
                            width=20,
                            borderBottom="2px solid #000",
                            borderRadius=10,
                        ),
                    ),
                    fac.AntdCenter(
                        "横线",
                        style=style(
                            fontSize=14,
                            color="#000000",
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "vertical":
            children = fac.AntdSpace(
                [
                    html.Div(
                        style=style(
                            height=20,
                            borderLeft="2px solid #000",
                            borderRadius=5,
                        ),
                    ),
                    fac.AntdCenter(
                        "竖线",
                        style=style(
                            fontSize=14,
                            color="#000000",
                            # width=10,
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "rectangle":
            children = fac.AntdSpace(
                [
                    fac.AntdCenter(
                        fac.AntdIcon(
                            icon="antd-border",
                            style=style(
                                fontSize=20,
                                color="#000000",
                            ),
                        )
                    ),
                    fac.AntdCenter(
                        "矩形",
                        style=style(
                            fontSize=14,
                            color="#000000",
                            # width=10,
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "text":
            children = fac.AntdSpace(
                [
                    fac.AntdIcon(
                        icon="antd-file-text",
                        style=style(
                            fontSize=20,
                            color="#000000",
                        ),
                    ),
                    fac.AntdCenter(
                        "文字",
                        style=style(
                            fontSize=14,
                            color="#000000",
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "picture":
            children = fac.AntdSpace(
                [
                    fac.AntdIcon(
                        icon="antd-picture",
                        style=style(
                            fontSize=20,
                            color="#000000",
                        ),
                    ),
                    fac.AntdCenter(
                        "图片",
                        style=style(
                            fontSize=12,
                            color="#000000",
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "qrcode":
            children = fac.AntdSpace(
                [
                    fac.AntdCenter(
                        fac.AntdIcon(
                            icon="antd-qrcode",
                            style=style(
                                fontSize=20,
                                color="#000000",
                            ),
                        )
                    ),
                    fac.AntdCenter(
                        "二维码",
                        style=style(
                            fontSize=12,
                            color="#000000",
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "barcode":
            children = fac.AntdSpace(
                [
                    fac.AntdCenter(
                        fac.AntdIcon(
                            icon="antd-bar-code",
                            style=style(
                                fontSize=20,
                                color="#000000",
                            ),
                        )
                    ),
                    fac.AntdCenter(
                        "条形码",
                        style=style(
                            fontSize=12,
                            color="#000000",
                        ),
                    ),
                ],
                size=10,
            )
        elif element_type == "table":
            children = fac.AntdSpace(
                [
                    fac.AntdCenter(
                        fac.AntdIcon(
                            icon="bi-table",
                            style=style(
                                fontSize=20,
                                color="#000000",
                            ),
                        )
                    ),
                    fac.AntdCenter(
                        "表格",
                        style=style(
                            fontSize=12,
                            color="#000000",
                        ),
                    ),
                ],
                size=10,
            )

        check_card_list.append(
            fac.AntdCheckCard(
                children,
                value=element.get("element_id"),
                style=style(
                    width="97%",
                    marginRight=3,
                    marginBottom=3,
                    borderRadius=5,
                ),
            )
        )
    return check_card_list


# 拖拽元素在布局区域的各元素的布局
def drag_element_layout(
    element_type: str = None,  # 元素类型
    element_x_y: dict = {"x": 0, "y": 0},  # 元素坐标
    element_config: dict = {},  # 元素配置
    element_preview: bool = False,  # 元素预览,
    dynamic_field: dict = {},  # 动态字段
):
    """
    拖拽元素布局
    """
    # 随机生成id
    component_id = element_config.get("element_id", str(uuid.uuid4()))
    element_type = element_config.get("element_type", element_type)
    element_config_ = element_config.get("element_config", {})

    element = {
        "element_id": component_id,
        "element_type": element_type,
    }
    rnd_kwargs = dict()
    if element_type == "transverse":
        element_config = {
            "thick": element_config_.get("thick", 2),  # 线宽
            "color": element_config_.get("color", "#000000"),  # 线条颜色
            "style": element_config_.get("style", "solid"),  # 线条样式
            "length": element_config_.get("length", 100),  # 线段长度
            "lock": element_config_.get("lock", False),  # 是否锁定
            "x": element_config_.get("x", element_x_y["x"]),  # x坐标
            "y": element_config_.get("y", element_x_y["y"]),  # y坐标
        }

        border = f"{element_config['thick']}px {element_config['style']} {element_config['color']}"
        rnd_kwargs = dict(
            children=[html.Div(style=style(width="100%", borderTop=f"{border}"))],
            size={"width": element_config["length"], "height": 2},
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            direction=["right", "left"] if not element_preview else [],
            # disableDragging=False if not element_preview or not element_config["lock"] else True,
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "vertical":
        element_config = {
            "thick": element_config_.get("thick", 2),  # 线宽
            "color": element_config_.get("color", "#000000"),  # 颜色
            "style": element_config_.get("style", "solid"),  # 样式
            "length": element_config_.get("length", 100),  # 长度
            "lock": element_config_.get("lock", False),  # 锁定
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        border = f"{element_config['thick']}px {element_config['style']} {element_config['color']}"

        rnd_kwargs = dict(
            children=[html.Div(style=style(height="100%", borderLeft=f"{border}"))],
            size={"width": 2, "height": element_config["length"]},
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            direction=["top", "bottom"] if not element_preview else [],
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "rectangle":
        element_config = {
            "thick": element_config_.get("thick", 2),  # 线宽
            "color": element_config_.get("color", "#000000"),  # 颜色
            "style": element_config_.get("style", "solid"),  # 样式
            "width": element_config_.get("width", 80),  # 宽度
            "height": element_config_.get("height", 80),  # 高度
            "radius": element_config_.get("radius", 0),  # 圆角
            "lock": element_config_.get("lock", False),
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        border = f"{element_config['thick']}px {element_config['style']} {element_config['color']}"
        rnd_kwargs = dict(
            children=[
                html.Div(
                    style=style(
                        width="100%",
                        height="100%",
                        border=f"{border}",
                        boxSizing="border-box",
                        borderRadius=element_config.get("radius"),
                    )
                )
            ],
            size={"width": element_config["width"], "height": element_config["height"]},
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            minHeight=20,
            minWidth=20,
            direction=["right", "left", "top", "bottom"] if not element_preview else [],
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "text":
        element_config = {
            "text": element_config_.get("text", "示例文本"),  # 文本内容
            "fontSize": element_config_.get("fontSize", 14),  # 字体大小
            "color": element_config_.get("color", "#000000"),  # 颜色
            "width": element_config_.get("width", 80),  # 字体容器宽
            "height": element_config_.get("height", 26),  # 字体容器高
            "style": element_config_.get("style", "static"),  # 字体数据类型
            "size": element_config_.get("size", 0),  # 字体间隔
            "lock": element_config_.get("lock", False),  # 锁定
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        rnd_kwargs = dict(
            children=[
                fac.AntdText(
                    f"{element_config['text']}",
                    strong=True,
                    style=style(
                        fontSize=element_config["fontSize"],
                        color=element_config.get("color"),
                        # 设置字间距
                        letterSpacing=f"{element_config.get('size')}px",
                        marginRight=f"-{element_config.get('size')}px",
                        display="inline-block",
                    ),
                )
            ],
            size={"width": element_config["width"], "height": element_config["height"]},
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            style=style(border="1px dashed #000") if not element_preview else None,
            direction=["top", "right", "bottom", "left"] if not element_preview else [],
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "picture":
        element_config = {
            "src": element_config_.get("src", "123456"),  # 图片的显示内容
            "height": element_config_.get("height", 80),  # 图片的高度
            "width": element_config_.get("width", 80),  # 图片的宽度
            "style": element_config_.get("style", "static"),  # 图片的数据类型
            "radius": element_config_.get("radius", 0),  # 圆角
            "lock": element_config_.get("lock", False),  # 锁定
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        rnd_kwargs = dict(
            children=[
                html.Img(
                    src=f"{element_config['src']}",
                    height=element_config["height"],
                    style=style(
                        width="100%",
                        height="100%",
                        borderRadius=element_config.get("radius"),
                    ),
                ),
            ],
            size={"width": element_config["width"], "height": element_config["height"]},
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            style=style(border="1px dashed #000") if not element_preview else None,
            direction=["top", "right", "bottom", "left"] if not element_preview else [],
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "qrcode":
        element_config = {
            "value": element_config_.get("value", "123456789"),  # 二维码内容
            "size": element_config_.get("size", 70),  # 二维码大小
            "style": element_config_.get("style", "static"),  # 二维码数据类型
            "lock": element_config_.get("lock", False),  # 锁定
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        rnd_kwargs = dict(
            children=[fuc.FefferyQRCode(value=f"{element_config['value']}", size=element_config["size"])],
            size={
                "width": element_config["size"] + 2,
                "height": element_config["size"] + 2,
            },
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            minHeight=50,
            minWidth=50,
            style=style(border="1px dashed #000") if not element_preview else None,
            direction=[],
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "barcode":
        element_config = {
            "value": element_config_.get("value", "123456789"),  # 条形码内容
            "fontSize": element_config.get("fontSize", 10),  # 字体大小
            # "width": element_config_.get("width", 200),  # 条形码宽度
            "height": element_config_.get("height", 25),  # 条形码高度
            "lock": element_config_.get("lock", False),  # 锁定
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        rnd_kwargs = dict(
            children=[
                fuc.FefferyBarcode(
                    value=f"{element_config['value']}",
                    fontSize=element_config["fontSize"],
                    textAlign="left",
                    height=element_config["height"],
                    width=1,
                    margin=5,
                )
            ],
            size={
                # "width": element_config["width"],
                # "height": element_config["height"],
            },
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            style=style(border="1px dashed #000") if not element_preview else None,
            direction=[],  # ["top", "right", "bottom", "left"] if not element_preview else [],
            disableDragging=element_preview or element_config["lock"],
        )

    elif element_type == "table":
        element_config = {
            "thead": element_config_.get("thead", 1),  # 是否显示表头
            "row": element_config_.get("row", 5),  # 列数
            "row_h": element_config_.get("row_h", 20),  # 行高
            "row_w": element_config_.get("row_w", 30),  # 行宽
            "width": element_config_.get("width", 300),  # 表宽
            "lock": element_config_.get("lock", False),  # 锁定
            "x": element_config_.get("x", element_x_y["x"]),
            "y": element_config_.get("y", element_x_y["y"]),
        }
        rnd_kwargs = dict(
            children=[
                fuc.FefferyStyle(
                    rawStyle=f"""
                    /* 整个表格的样式 */
                    .table-container {{
                        width: 100%;
                        height: 100%;
                        border-collapse: collapse;
                        font-family: Arial, sans-serif;
                        border: 1px solid #ccc;   /* 实色边框 */
                        box-shadow: none;         /* 彻底去掉阴影 */
                    }}
                    /* 表格行的样式 */
                    .table-row {{
                        border-bottom: 1px solid #ddd;  /* 添加行hover样式 */
                    }}
                    .table-row:hover {{
                        # background-color: #f5f5f5;  /* 鼠标悬停时背景颜色 */
                    }}
                    /* 单元格通用样式 */
                    .table-cell {{
                        width: {element_config["row_w"]}px;
                        height: {element_config["row_h"]}px;
                        padding: 0px;
                        text-align: left;
                        border: 1px solid #ccc;
                        word-wrap: break-word;
                    }}

                    /* 表头单元格样式 */
                    .table-header {{
                        background-color: #4CAF50;
                        color: white;
                        font-weight: bold;
                        text-align: center;
                    }}
                    """
                ),
                html.Table(
                    [
                        html.Tr(
                            [html.Th("", className="table-cell table-header") for i in range(element_config["row"])],
                            className="table-row",
                        )
                        if element_config["thead"] == 1
                        else None,
                        *[
                            html.Tr(
                                [html.Td("", className="table-cell") for i in range(element_config["row"])],
                                className="table-row",
                            )
                            for i in range(2)
                        ],
                    ],
                    className="table-container",
                ),
            ],
            size={
                "width": element_config["width"],
                # "height": element_config["height"],
            },
            position={
                "x": element_config.get("x"),
                "y": element_config.get("y"),
            },
            style=style(border="1px dashed #000") if not element_preview else None,
            direction=["right", "left"] if not element_preview else [],
            disableDragging=element_preview or element_config["lock"],
        )

    # 只在非 preview 模式下才给 id
    if not element_preview:
        rnd_kwargs["id"] = {"type": "RND", "id": component_id}
        rnd_kwargs["key"] = f"{component_id}+{element_type}"
    # 创建拖拽元素
    element_end = fuc.FefferyRND(
        **rnd_kwargs,
        bounds="parent",
        selected=False,
    )
    # 添加元素数据
    element["element_config"] = element_config

    return {"rnd": _to_dict(element_end), "element": element}


# 拖拽元素属性编辑
def element_property_attributes_layout(
    element_config: dict = {},  # 元素配置
):
    component_id = element_config.get("element_id", "")
    element_type = element_config.get("element_type", "")
    element_config_ = element_config.get("element_config", {})

    if element_type == "transverse":
        values_ = {
            "component_id": component_id,
            "thick": element_config_.get("thick"),
            "color": element_config_.get("color"),
            "style": element_config_.get("style"),
            "length": element_config_.get("length"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "lock": element_config_.get("lock", True),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="length", size="small", min=0, style={"width": "100%"}),
                    label=f"组件长度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="x", size="small", min=0, style={"width": "100%"}),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="y", size="small", min=0, style={"width": "100%"}),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="thick", size="small", min=0, style={"width": "100%"}),
                    label=f"线条粗细",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "实线": "solid",
                                "点线": "dotted",
                                "虚线": "dashed",
                                "双线": "double",
                                "无边框": "none",
                            }.items()
                        ],
                        value="实线",
                        style={"width": "100%"},
                    ),
                    label=f"线条类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdColorPicker(
                        name="color",
                        showText=True,
                        size="small",
                        value="#000000",
                        style=style(
                            width="100%",
                        ),
                    ),
                    label=f"线条颜色",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "vertical":
        values_ = {
            "component_id": component_id,
            "thick": element_config_.get("thick"),
            "color": element_config_.get("color"),
            "style": element_config_.get("style"),
            "length": element_config_.get("length"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="length", size="small", min=0, style={"width": "100%"}),
                    label=f"组件长度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="x", size="small", min=0, style={"width": "100%"}),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="y", size="small", min=0, style={"width": "100%"}),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="thick", size="small", min=0, style={"width": "100%"}),
                    label=f"线条粗细",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "实线": "solid",
                                "点线": "dotted",
                                "虚线": "dashed",
                                "双线": "double",
                                "无边框": "none",
                            }.items()
                        ],
                        value="实线",
                        style={"width": "100%"},
                    ),
                    label=f"线条类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdColorPicker(
                        name="color",
                        showText=True,
                        size="small",
                        value="#000000",
                        style=style(
                            width="100%",
                        ),
                    ),
                    label=f"线条颜色",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "rectangle":
        values_ = {
            "component_id": component_id,
            "thick": element_config_.get("thick"),
            "color": element_config_.get("color"),
            "style": element_config_.get("style"),
            "width": element_config_.get("width"),
            "height": element_config_.get("height"),
            "radius": element_config_.get("radius"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="width",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"宽度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="height",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"高度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="x",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="y",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(
                        variant="solid",
                        lineColor="#595959",
                        className={"margin": "0px"},
                    ),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="thick", size="small", min=0, style={"width": "100%"}),
                    label=f"线条粗细",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "实线": "solid",
                                "点线": "dotted",
                                "虚线": "dashed",
                                "双线": "double",
                                "无边框": "none",
                            }.items()
                        ],
                        value="实线",
                        style={"width": "100%"},
                    ),
                    label=f"线条类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdColorPicker(
                        name="color",
                        showText=True,
                        size="small",
                        value="#000000",
                        style=style(
                            width="100%",
                        ),
                    ),
                    label=f"线条颜色",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="radius", size="small", min=0, style={"width": "100%"}),
                    label=f"矩形圆角",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "text":
        values_ = {
            "component_id": component_id,
            "text": element_config_.get("text"),
            "fontSize": element_config_.get("fontSize"),
            "width": element_config_.get("width"),
            "height": element_config_.get("height"),
            "style": element_config_.get("style", "static"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "size": element_config_.get("size"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="width",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"宽度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="height",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"高度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="x",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="y",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "静态内容": "static",
                                "动态内容": "variation",
                            }.items()
                        ],
                        value="静态内容",
                        style={"width": "100%"},
                    ),
                    label=f"字段类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(name="text", mode="text-area"),
                    label=f"字段内容",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    [
                        # 通过FefferyListenDrop绑定拖拽元素放置目标容器
                        fuc.FefferyListenDrop(
                            id="drop-element-data-source",
                            targetSelector="#drag-element-data-form-source",
                        ),
                        fac.AntdCenter(
                            "拖放数据源字段到这里",
                            id="drag-element-data-form-source",
                            style={
                                "width": 145,
                                "height": 50,
                                "font-size": 12,
                                "marginTop": "5px",
                                "color": "#909090",
                                "background": "#f0f0f0",
                                "border": "1px solid #909090",
                            },
                        ),
                    ],
                    label=f"绑定字段",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="fontSize", size="small", min=0, style={"width": "100%"}),
                    label=f"字体大小",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdColorPicker(
                        name="color",
                        showText=True,
                        size="small",
                        value="#000000",
                        style=style(
                            width="100%",
                        ),
                    ),
                    label=f"字体颜色",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="size", size="small", min=0, style={"width": "100%"}),
                    label=f"字体间隔",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "picture":
        values_ = {
            "component_id": component_id,
            "width": element_config_.get("width"),
            "height": element_config_.get("height"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "style": element_config_.get("style", "static"),
            "src": element_config_.get("src"),
            "radius": element_config_.get("radius"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="width",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"宽度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="height",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"高度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="x",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="y",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "静态内容": "static",
                                "动态内容": "variation",
                            }.items()
                        ],
                        value="静态内容",
                        style={"width": "100%"},
                    ),
                    label=f"数据类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(name="src", mode="text-area"),
                    label=f"图片",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    [
                        # 通过FefferyListenDrop绑定拖拽元素放置目标容器
                        fuc.FefferyListenDrop(
                            id="drop-element-data-source",
                            targetSelector="#drag-element-data-form-source",
                        ),
                        fac.AntdCenter(
                            "拖放数据源字段到这里",
                            id="drag-element-data-form-source",
                            style={
                                "width": 145,
                                "height": 50,
                                "font-size": 12,
                                "marginTop": "5px",
                                "color": "#909090",
                                "background": "#f0f0f0",
                                "border": "1px solid #909090",
                            },
                        ),
                    ],
                    label=f"绑定字段",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="radius", size="small", min=0, style={"width": "100%"}),
                    label=f"设置圆角",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "qrcode":
        values_ = {
            "component_id": component_id,
            "size": element_config_.get("size"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "style": element_config_.get("style", "static"),
            "value": element_config_.get("value"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="size",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"大小",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="x",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="y",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "静态内容": "static",
                                "动态内容": "variation",
                            }.items()
                        ],
                        value="静态内容",
                        style={"width": "100%"},
                    ),
                    label=f"数据类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(name="value", mode="text-area"),
                    label="内容",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    [
                        # 通过FefferyListenDrop绑定拖拽元素放置目标容器
                        fuc.FefferyListenDrop(
                            id="drop-element-data-source",
                            targetSelector="#drag-element-data-form-source",
                        ),
                        fac.AntdCenter(
                            "拖放数据源字段到这里",
                            id="drag-element-data-form-source",
                            style={
                                "width": 145,
                                "height": 50,
                                "font-size": 12,
                                "marginTop": "5px",
                                "color": "#909090",
                                "background": "#f0f0f0",
                                "border": "1px solid #909090",
                            },
                        ),
                    ],
                    label=f"绑定字段",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "barcode":
        values_ = {
            "component_id": component_id,
            "height": element_config_.get("height"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "fontSize": element_config_.get("fontSize"),
            "style": element_config_.get("style", "static"),
            "value": element_config_.get("value"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="height",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"高度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="x",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="y",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="fontSize",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"字体大小",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="style",
                        size="small",
                        # placeholder='size="small"',
                        options=[
                            {"label": f"{k}", "value": f"{v}"}
                            for k, v in {
                                "静态内容": "static",
                                "动态内容": "variation",
                            }.items()
                        ],
                        value="静态内容",
                        style={"width": "100%"},
                    ),
                    label=f"数据类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(name="value", mode="text-area"),
                    label=f"内容",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    [
                        # 通过FefferyListenDrop绑定拖拽元素放置目标容器
                        fuc.FefferyListenDrop(
                            id="drop-element-data-source",
                            targetSelector="#drag-element-data-form-source",
                        ),
                        fac.AntdCenter(
                            "拖放数据源字段到这里",
                            id="drag-element-data-form-source",
                            style={
                                "width": 145,
                                "height": 50,
                                "font-size": 12,
                                "marginTop": "5px",
                                "color": "#909090",
                                "background": "#f0f0f0",
                                "border": "1px solid #909090",
                            },
                        ),
                    ],
                    label=f"绑定字段",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    elif element_type == "table":
        values_ = {
            "component_id": component_id,
            "thead": element_config.get("thead", 1),  # 是否显示表头
            "row": element_config.get("row", 5),  # 行数
            "width": element_config_.get("width"),
            "row_h": element_config_.get("row_h"),
            "row_w": element_config_.get("row_w"),
            "x": element_config_.get("x"),
            "y": element_config_.get("y"),
            "lock": element_config_.get("lock"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="component_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label=f"组件ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdText(
                        BaseConfig.element[element_type],
                    ),
                    label=f"组件类型",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="x",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"X坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="y",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"Y坐标",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="width",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"宽度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="thead",
                        options=[{"label": f"{k}", "value": f"{v}"} for k, v in {"显示表头": 1, "影藏表头": 0}.items()],
                        style={"width": "100%"},
                    ),
                    label=f"显示表头",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="row",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label=f"显示行数",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="row_h",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label="单元高度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(
                        name="row_w",
                        size="small",
                        min=0,
                        style={"width": "100%"},
                    ),
                    label="单元宽度",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    # 直接传入字符串
                    fac.AntdSwitch(
                        name="lock",
                        checkedChildren="禁止",
                        unCheckedChildren="允许",
                    ),
                    label=f"锁定编辑",
                ),
                span=24,
            ),
        ]

    else:
        values_ = {
            "m_id": element_config.get("m_id"),
            "m_name": element_config.get("m_name"),
            "m_paper_type": element_config.get("m_paper_type"),
            "m_mm_w": element_config.get("m_mm_w"),
            "m_mm_h": element_config.get("m_mm_h"),
            "m_px_w": element_config.get("m_px_w"),
            "m_px_h": element_config.get("m_px_h"),
            "m_pages_num": element_config.get("m_pages_num"),
            "m_Bkgrdp": element_config.get("m_Bkgrdp"),
            "m_Bkgrd_color": element_config.get("m_Bkgrd_color"),
            "m_paper_data": element_config.get("m_paper_data", "静态JSON"),
        }
        form = [
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="m_id",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label="页面ID",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="m_name",
                        variant="borderless",
                        placeholder="请输入",
                        style={"width": "100%"},
                    ),
                    label="模版名称",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="m_paper_type",
                        size="small",
                        options=[{"label": k, "value": k} for k in BaseConfig.paper.keys()],
                        style={"width": "100%"},
                    ),
                    label="纸张尺寸",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="m_mm_w", min=0, size="small", style={"width": "100%"}),
                    label="宽",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="m_mm_h", min=0, size="small", style={"width": "100%"}),
                    label="高",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInputNumber(name="m_pages_num", min=0, size="small", style={"width": "100%"}),
                    label="页数",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdColorPicker(
                        name="m_Bkgrd_color",
                        showText=True,
                        size="small",
                        value="#000000",
                        style=style(
                            width="100%",
                        ),
                    ),
                    label="背景颜色",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdCenter(
                        "选择背景图片",
                        style={
                            "width": 145,
                            "height": 145,
                            "font-size": 12,
                            "marginTop": "5px",
                            "color": "#909090",
                            "background": "#f0f0f0",
                            "border": "1px solid #909090",
                        },
                    ),
                    label="背景图片",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdSelect(
                        name="m_paper_data",
                        size="small",
                        options=[{"label": k, "value": k} for k in ["静态JSON", "动态接口"]],
                        style={"width": "100%"},
                    ),
                    label="数据源",
                ),
                span=24,
            ),
            fac.AntdCol(
                fac.AntdFormItem(
                    fac.AntdInput(
                        name="m_paper_data_text",
                        placeholder="输入数据文本",
                        mode="text-area",
                        autoSize={"minRows": 10, "maxRows": 10},
                    ),
                    # label="数据文本",
                ),
                span=24,
            ),
        ]

    return fac.AntdForm(
        fac.AntdRow(
            [
                *form,
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdDivider(variant="solid", lineColor="#595959", className={"margin": "0px"}),
                    ),
                    span=24,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdButton(
                            "提交",
                            id="element-from-submit",
                            type="primary",
                            block=True,
                            # disabled=True if not element_type else False,
                        )
                    ),
                    span=8,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdButton(
                            "复制",
                            id="element-from-copy",
                            type="primary",
                            block=True,
                            disabled=True if not element_type else False,
                        )
                    ),
                    span=8,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdButton(
                            "删除",
                            id="element-from-del",
                            type="primary",
                            block=True,
                            disabled=True if not element_type else False,
                        )
                    ),
                    span=8,
                ),
                fac.AntdCol(
                    fuc.FefferyDebounceProp(id="element-property-attributes-form-debounce", debounceWait=500),
                    span=24,
                ),
            ],
            gutter=5,
        ),
        id="element-property-attributes-form",
        values=values_,
        enableBatchControl=True,
        labelCol={"span": 8},
        wrapperCol={"span": 24},
        labelAlign="right",
        # layout="vertical",
        className={
            ".ant-form-item": {
                "padding": "0px",
                "border-radius": "0px",
                "margin-bottom": "0px",
            },
        },
    )


# 数据源的显示和隐藏
def data_source_layout(element_type: str = None):
    type_map = ["text", "picture", "qrcode", "barcode"]

    if element_type in type_map:
        return fac.AntdAccordion(
            items=[
                {
                    "title": f"{data_type}",
                    "key": data_type,
                    "showArrow": False,
                    "children": fac.AntdRow(
                        [
                            fac.AntdCol(
                                [
                                    # 绑定需要拖拽的元素横线
                                    fuc.FefferyListenDrag(
                                        targetSelector=f"#drag-print-data-source-{v}",
                                        data={
                                            "info": f"{v}",
                                        },
                                    ),
                                    fac.AntdCenter(
                                        f"{k}",
                                        id=f"drag-print-data-source-{v}",
                                        # 关键：加一个自定义属性 data-type="text"
                                        **{"data-type": "text"},
                                        style={
                                            "backgroundColor": "#1677ff",
                                            "color": "white",
                                            "height": 45,
                                            "fontSize": 10,
                                        },
                                    ),
                                ],
                                span=6,
                            )
                            for k, v in BaseConfig.data_source[data_type].items()
                        ],
                        gutter=[5, 5],
                    ),
                }
                for data_type in BaseConfig.data_source.keys()
            ],
            expandIconPosition="right",
            size="small",
            ghost=False,
        )
    else:
        return fac.AntdAlert(message="当前组件，不支持，数据源配置", type="success")
