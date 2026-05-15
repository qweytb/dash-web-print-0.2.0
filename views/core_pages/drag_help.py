"""鼠标拖拽辅助线"""

from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
import random

# 回调
import callbacks.core_pages_c.drag_help_c as drag_help_c


def layout():
    return fac.AntdSpace(
        [
            fac.AntdCenter(
                fac.AntdText(
                    "辅助线",
                    style=style(
                        fontSize=10,
                        color="#ffffff",
                    ),
                ),
                style=style(width=10),
            ),
            fac.AntdDivider(
                direction="vertical",
                lineColor="red",
                className={"height": "35px"},
            ),
            fuc.FefferyDiv(
                fac.AntdCenter(
                    fac.AntdSpace(
                        [
                            fac.AntdCenter(
                                fac.AntdIcon(
                                    icon="antd-pause",
                                    style=style(
                                        fontSize=20,
                                        color="#ffffff",
                                        # 旋转90度
                                        # transform="rotate(90deg)",
                                    ),
                                )
                            ),
                            fac.AntdCenter(
                                "纵向",
                                style=style(
                                    fontSize=12,
                                    color="#ffffff",
                                ),
                            ),
                        ],
                        size=0,
                        direction="vertical",
                    )
                ),
                id="help-lengthways-top",
                className="hover-div",
            ),
            fuc.FefferyDiv(
                fac.AntdCenter(
                    fac.AntdSpace(
                        [
                            fac.AntdCenter(
                                fac.AntdIcon(
                                    icon="antd-pause",
                                    style=style(
                                        fontSize=20,
                                        color="#ffffff",
                                        # 旋转90度
                                        transform="rotate(90deg)",
                                    ),
                                )
                            ),
                            fac.AntdCenter(
                                "横向",
                                style=style(
                                    fontSize=12,
                                    color="#ffffff",
                                ),
                            ),
                        ],
                        size=0,
                        direction="vertical",
                    )
                ),
                id="help-crosswise-left",
                className="hover-div",
            ),
            fuc.FefferyDiv(
                fac.AntdCenter(
                    fac.AntdSpace(
                        [
                            fac.AntdCenter(
                                fac.AntdIcon(
                                    icon="antd-table",
                                    style=style(
                                        fontSize=20,
                                        color="#ffffff",
                                    ),
                                )
                            ),
                            fac.AntdCenter(
                                "网格",
                                style=style(
                                    fontSize=12,
                                    color="#ffffff",
                                ),
                            ),
                        ],
                        size=0,
                        direction="vertical",
                    )
                ),
                id="help-gridding-centre",
                className="hover-div",
            ),
            fac.AntdCheckCard(
                "网格吸附",
                id="drag-gridding-adsorb",
                className="my-checkcard",
            ),
            fuc.FefferyDiv(
                fac.AntdCenter(
                    fac.AntdIcon(
                        icon="antd-zoom-in",
                        style=style(
                            fontSize=24,
                            color="#ffffff",
                        ),
                    ),
                    style=style(
                        height=45,
                    ),
                ),
                id="help-zoom-in",
                className="hover-div",
            ),
            fuc.FefferyDiv(
                fac.AntdCenter(
                    fac.AntdText(
                        "100%",
                        id="help-zoom-in-text",
                        type="danger",
                        style=style(
                            fontSize=20,
                        ),
                    ),
                    style=style(height=45, width=50),
                ),
            ),
            fuc.FefferyDiv(
                fac.AntdCenter(
                    fac.AntdIcon(
                        icon="antd-zoom-out",
                        style=style(
                            fontSize=24,
                            color="#ffffff",
                        ),
                    ),
                    style=style(
                        height=45,
                    ),
                ),
                id="help-zoom-out",
                className="hover-div",
            ),
            fac.AntdPopover(
                fuc.FefferyDiv(
                    fac.AntdCenter(
                        fac.AntdIcon(
                            icon="antd-delete",
                            style=style(
                                fontSize=24,
                                color="#ffffff",
                            ),
                        ),
                        style=style(
                            height=45,
                        ),
                    ),
                    id="help-delete-data",
                    className="hover-div",
                ),
                content="清除布局",
                placement="left",
                arrow="hide",
                color="rgb(255,255,255,0.5)",
                styles={
                    "body": {
                        "padding": "2px",
                    }
                },
            ),
            # fuc.FefferyDiv(
            #     fac.AntdCenter(
            #         fac.AntdIcon(
            #             icon="antd-container",
            #             style=style(
            #                 fontSize=26,
            #                 color="#ffffff",
            #             ),
            #         ),
            #         style=style(
            #             height=45,
            #         ),
            #     ),
            #     id="help-refresh-layout",
            #     className="hover-div",
            # ),
        ],
        size=20,
        style=style(
            width="35%",
            height="100%",
        ),
    )


def help_layout(help_type, extent=None):
    if "lengthways" == help_type:
        return fuc.FefferyRND(
            [
                html.Div(
                    style=style(
                        width=5,
                        height=40,
                        background="#DB1C1C",
                        border="1px solid #000",
                    ),
                ),
            ],
            dragAxis="x",
            size={"height": extent - 20},
            dragGrid=[1, 1],
            position={"x": random.randint(300, 1000), "y": 65},
            direction=[],  # 关闭尺寸调整功能
            # lockAspectRatio=True,
            bounds="parent",
            style=style(
                borderLeft="1px solid #FF0000",
                paddingTop="10px",
            ),
        )
    elif "crosswise" == help_type:
        return fuc.FefferyRND(
            [
                html.Div(
                    style=style(
                        width=60,
                        height=5,
                        background="#DB1C1C",
                        border="1px solid #000",
                    ),
                ),
            ],
            dragAxis="y",
            size={"width": extent - 20},
            dragGrid=[1, 1],
            position={"x": 20, "y": random.randint(200, 800)},
            direction=[],  # 关闭尺寸调整功能
            bounds="parent",
            style=style(
                borderTop="1px solid #FF0000",
                paddingLeft="10px",
            ),
        )
    elif "gridding" == help_type:
        return fuc.FefferyStyle(
            rawStyle="""
                .grid-lines {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-image:
                        linear-gradient(to right, #e0e0e0 1px, transparent 1px),
                        linear-gradient(to bottom, #e0e0e0 1px, transparent 1px);
                    background-size: 20px 20px; /* 控制网格的大小 */
                    pointer-events: none; /* 添加这一行，使网格不响应鼠标事件 */
                    z-index: 0; /* 确保网格在内容下方 */
                }
                """
        )
