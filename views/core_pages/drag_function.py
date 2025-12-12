"""拖拽,功能按钮区域"""

from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style

# 回调
import callbacks.core_pages_c.drag_function_c as drag_function_c


def layout():
    return html.Div(
        fac.AntdSpace(
            [
                *[
                    fuc.FefferyStyle(
                        rawStyle="""
                        .check-card-group-custom-style-demo .ant-pro-checkcard-content {
                            padding: 1px 8px;
                        }
                        """
                    ),
                    fac.AntdCheckCardGroup(
                        [
                            fac.AntdCheckCard(
                                fac.AntdIcon(icon=icon, style={"fontSize": 20}),
                                value=i,
                                style={
                                    "width": "auto",
                                    "marginRight": 3,
                                    "marginBottom": 1,
                                    "borderRadius": 1,
                                },
                            )
                            for icon, i in zip(
                                ["antd-cluster", "pi-database", "md-dashboard"],
                                [
                                    "picture-list",
                                    "picture-data",
                                    "property-attributes",
                                ],
                            )
                        ],
                        id="element_property_attributes",
                        className="check-card-group-custom-style-demo",
                        defaultValue=[
                            "picture-list",
                            "picture-data",
                            "property-attributes",
                        ],
                        multiple=True,
                    ),
                ],
                fuc.FefferyDiv(
                    [
                        fac.AntdCenter(
                            fac.AntdIcon(
                                icon="antd-file",
                                style=style(
                                    fontSize=20,
                                    color="#ffffff",
                                ),
                            ),
                        ),
                        fac.AntdCenter(
                            "模版",
                            style=style(
                                fontSize=12,
                                color="#ffffff",
                            ),
                        ),
                    ],
                    style=style(
                        width=40,
                        height="100%",
                    ),
                    id="print-template",
                    className="hover-div",
                ),
                fuc.FefferyDiv(
                    [
                        fac.AntdCenter(
                            fac.AntdIcon(
                                icon="pi-floppy-disk",
                                style=style(
                                    fontSize=20,
                                    color="#ffffff",
                                ),
                            ),
                        ),
                        fac.AntdCenter(
                            "保存",
                            style=style(
                                fontSize=12,
                                color="#ffffff",
                            ),
                        ),
                    ],
                    style=style(
                        width=40,
                        height="100%",
                    ),
                    id="save-template",
                    className="hover-div",
                ),
                fac.AntdDivider(
                    direction="vertical",
                    lineColor="red",
                    className={"height": "35px"},
                ),
                fuc.FefferyDiv(
                    [
                        fac.AntdCenter(
                            fac.AntdIcon(
                                icon="antd-container",
                                style=style(
                                    fontSize=20,
                                    color="#ffffff",
                                ),
                            ),
                        ),
                        fac.AntdCenter(
                            "预览",
                            style=style(
                                fontSize=12,
                                color="#ffffff",
                            ),
                        ),
                    ],
                    style=style(
                        width=40,
                        height="100%",
                    ),
                    id="preview-template",
                    className="hover-div",
                ),
                fac.AntdDivider(
                    direction="vertical",
                    lineColor="red",
                    className={"height": "35px"},
                ),
                fuc.FefferyDiv(
                    [
                        fac.AntdCenter(
                            fac.AntdIcon(
                                icon="md-help-outline",
                                style=style(
                                    fontSize=20,
                                    color="#ffffff",
                                ),
                            ),
                        ),
                        fac.AntdCenter(
                            "帮助",
                            style=style(
                                fontSize=12,
                                color="#ffffff",
                            ),
                        ),
                    ],
                    style=style(
                        width=40,
                        height="100%",
                    ),
                    id="help-template",
                    className="hover-div",
                ),
            ],
            size=10,
        ),
        style=style(
            width="25%",
            height="100%",
            # div 里面内容右对齐
            display="flex",
            justifyContent="right",
            alignItems="center",
            # 设置边距
            paddingRight=20,
            boxSizing="border-box",
        ),
    )


# 组件元素编辑属性
def element_property_attributes_layout(element_list):
    list_ = []
    for element in element_list:
        pass
    return list_
