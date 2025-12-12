from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style

# 导入回调模块
import callbacks.core_pages_c as core_pages_c

from configs.base_config import BaseConfig

# 导入布局模块
from . import drag_element, drag_help, drag_function, graduated_scale


def layout():
    return fac.AntdFlex(
        [
            html.Div(
                fac.AntdFlex(
                    [
                        fac.AntdSpace(
                            [
                                html.Img(
                                    src="/assets/imgs/icon.ico",
                                    style=style(
                                        height=25,
                                    ),
                                ),
                                fac.AntdText(
                                    BaseConfig.app_title,
                                    style=style(fontSize=18, color="#ffffff"),
                                ),
                                fac.AntdText(
                                    f"版本号：{BaseConfig.app_version}",
                                    style=style(fontSize=10, color="#ffffff"),
                                ),
                            ],
                            size=10,
                            style=style(
                                width="20%",
                                height="100%",
                                padding=10,
                                boxSizing="border-box",
                            ),
                        ),
                        # 拖拽组件元素
                        drag_element.layout(),
                        # 拖拽辅助线
                        drag_help.layout(),
                        # 功能按钮布局
                        drag_function.layout(),
                    ],
                    style=style(
                        width="100%",
                        height="100%",
                    ),
                ),
                style=style(
                    width="100%",
                    height=45,
                    background="#666666",
                ),
            ),
            fuc.FefferyDiv(
                [
                    # 顶部渐变刻度
                    fac.AntdAffix(
                        id="top-scale-label",
                        offsetTop=0,
                        target="affix-container",
                        style=style(
                            height="25px",
                        ),
                    ),
                    # 监听内容区域元素尺寸,
                    fuc.FefferyListenElementSize(
                        id="listen-element-size-container",
                        target="affix-container",
                    ),
                    fac.AntdFlex(
                        [
                            # 左边渐变刻度
                            html.Div(
                                id="left-scale-label",
                                style=style(
                                    width="20px",
                                ),
                            ),
                            html.Div(
                                [
                                    fac.AntdAffix(
                                        [
                                            fac.AntdCollapse(
                                                fuc.FefferyScrollbars(
                                                    [
                                                        fuc.FefferyStyle(
                                                            rawStyle="""
                                                        .check-card-group-custom-style-demo .ant-pro-checkcard-content {
                                                            padding: 0px 5px;
                                                        }
                                                        """
                                                        ),
                                                        fac.AntdCheckCardGroup(
                                                            id="drag-element-property-attributes-group",
                                                            # defaultValue="7b8f99ec-1b0a-458c-af20-5b0b38533b8f",
                                                            className="check-card-group-custom-style-demo",
                                                            style=style(width="100%"),
                                                        ),
                                                    ],
                                                    style=style(
                                                        height="calc(100vh - 170px)",
                                                    ),
                                                ),
                                                bordered=False,
                                                title="布局的组件",
                                                size="small",
                                                # isOpen=False,
                                                styles={
                                                    "header": {"backgroundColor": "#666666"},
                                                    "body": {"padding": "10px 5px 5px 5px", "boxSizing": "border-box"},
                                                },
                                                style=style(
                                                    background="#ffffff",
                                                    width="240px",
                                                    # 绝对定位
                                                    position="absolute",
                                                    left="20px",
                                                    borderRadius="10px",
                                                    boxShadow="rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px",
                                                ),
                                            ),
                                        ],
                                        id="drag-element-picture",
                                        offsetTop=15,
                                        target="affix-container-inner",
                                        style=style(display="none"),
                                    ),
                                    fac.AntdAffix(
                                        [
                                            fac.AntdCollapse(
                                                fuc.FefferyScrollbars(
                                                    fac.AntdAlert(
                                                        message="当前组件，不支持，数据源配置", type="success"
                                                    ),
                                                    id="drag-element-data-source-scrollbar",
                                                    style=style(
                                                        height="calc(100vh - 170px)",
                                                    ),
                                                ),
                                                bordered=False,
                                                title="设定的数据源",
                                                size="small",
                                                # isOpen=False,
                                                styles={
                                                    "header": {"backgroundColor": "#666666"},
                                                    "body": {"padding": "10px 5px 5px 5px", "boxSizing": "border-box"},
                                                },
                                                style=style(
                                                    background="#ffffff",
                                                    width="240px",
                                                    # 绝对定位
                                                    position="absolute",
                                                    right="300px",
                                                    borderRadius="10px",
                                                    boxShadow="rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px",
                                                ),
                                            ),
                                        ],
                                        id="drag-element-data",
                                        offsetTop=15,
                                        target="affix-container-inner",
                                    ),
                                    fac.AntdAffix(
                                        [
                                            fac.AntdCollapse(
                                                fuc.FefferyScrollbars(
                                                    id="drag-element-property-attributes-form",
                                                    style=style(
                                                        height="calc(100vh - 170px)",
                                                        overflowX="hidden",
                                                    ),
                                                ),
                                                bordered=False,
                                                title="组件的属性设置",
                                                size="small",
                                                # isOpen=False,
                                                styles={
                                                    "header": {
                                                        "backgroundColor": "#666666",
                                                    },
                                                    "body": {"padding": "10px 5px 5px 5px", "boxSizing": "border-box"},
                                                },
                                                style=style(
                                                    background="#ffffff",
                                                    width="240px",
                                                    # 绝对定位
                                                    position="absolute",
                                                    right="30px",
                                                    borderRadius="10px",
                                                    boxShadow="rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px",
                                                ),
                                            ),
                                        ],
                                        id="drag-element-property-attributes",
                                        offsetTop=15,
                                        target="affix-container-inner",
                                    ),
                                    html.Div(
                                        id="grid-lines-layout",
                                    ),
                                    # 通过FefferyListenDrop绑定拖拽元素放置目标容器
                                    fuc.FefferyListenDrop(
                                        id="listen-drop-element",
                                        targetSelector="#drag-container-inner-layout",
                                    ),
                                    # 拖拽元素放置目标容器
                                    fuc.FefferyDiv(
                                        [
                                            html.Div(
                                                className="grid-lines",
                                            ),
                                            # 监听内容区域元素尺寸,
                                            fuc.FefferyListenElementSize(
                                                id="drag-module-size-container",
                                                target="drag-container-inner-layout",
                                            ),
                                            # 保证拖拽元素放置容器在最顶层
                                            fuc.FefferyStyle(
                                                id="drag-container-inner-style",
                                                rawStyle="""
                                                #drag-container-inner-layout {
                                                    position: relative; /* 确保容器是定位上下文 */
                                                    z-index: 1; /* 确保内容在网格上方 */
                                                    transform-origin: 0 0;     /* 左上角 */
                                                    transform: scale(1);
                                                    transition: transform .2s;               
                                                }
                                                """,
                                            ),
                                            # 这里设置纸张大小
                                            html.Div(
                                                id="drag-container-inner-layout",
                                                style=style(width="210mm", height="297mm"),
                                            ),
                                        ],
                                        # 拖阻布局页
                                        id="drag-container-inner",
                                        enableEvents=["position", "size"],
                                        style=style(
                                            # 绝对定位
                                            position="absolute",
                                            left=300,
                                            top=60,
                                            backgroundColor="#ffffff",
                                            boxShadow="rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px",
                                        ),
                                    ),
                                ],
                                id="affix-container-inner",
                                style=style(
                                    width="calc(100% - 20px)",
                                    backgroundColor="#EEEEEE",
                                    # 启动绝对单位
                                    position="relative",
                                ),
                            ),
                        ],
                        gap=5,
                        style=style(
                            width="100%",
                        ),
                    ),
                    # 滚动条监听
                    fuc.FefferyListenScroll(
                        id="listen-scroll-container-inner",
                        target="affix-container",
                    ),
                ],
                id="affix-container",
                scrollbar="simple",
                style=style(
                    overflowY="auto",
                    overflowX="hidden",
                    width="100%",
                    height="calc(100% - 60px)",
                    maxHeight="calc(100% - 60px)",
                    maxWidth="100%",
                ),
            ),
            html.Div(
                style=style(
                    width="100%",
                    height=15,
                    backgroundColor="#AAAAAA",
                    border="1px solid #000",
                ),
            ),
        ],
        id="main-layout-container",
        vertical=True,
        style=style(
            width="100vw",
            minWidth=1900,
            height="100vh",
            minHeight=900,
            overflowX="hidden",
        ),
    )
