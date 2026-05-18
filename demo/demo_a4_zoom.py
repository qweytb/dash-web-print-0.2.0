import dash
from dash import html, dcc, Input, Output, State
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style

# 实例化Dash应用对象
app = dash.Dash(__name__)

# A4纸标准尺寸 (210mm x 297mm) 对应的像素 (按96dpi计算)
A4_WIDTH_PX = 794  # 210mm ≈ 794px
A4_HEIGHT_PX = 1123  # 297mm ≈ 1123px

app.layout = fac.AntdCenter(
    [
        # 控制面板
        fac.AntdCard(
            [
                fac.AntdSpace(
                    [
                        fac.AntdText("缩放比例:", strong=True),
                        fac.AntdSlider(
                            id="zoom-slider",
                            min=0.5,
                            max=2.0,
                            step=0.1,
                            value=1.0,
                            marks={0.5: "50%", 1.0: "100%", 1.5: "150%", 2.0: "200%"},
                            style={"width": 300},
                        ),
                        fac.AntdText(id="zoom-value", style={"minWidth": 50}),
                    ],
                    align="center",
                ),
                fac.AntdDivider(),
                fac.AntdSpace(
                    [
                        fac.AntdButton(
                            "缩小",
                            id="zoom-out-btn",
                            type="primary",
                            icon=fac.AntdIcon(icon="antd-minus"),
                        ),
                        fac.AntdButton(
                            "重置",
                            id="zoom-reset-btn",
                            icon=fac.AntdIcon(icon="antd-reload"),
                        ),
                        fac.AntdButton(
                            "放大",
                            id="zoom-in-btn",
                            type="primary",
                            icon=fac.AntdIcon(icon="antd-plus"),
                        ),
                    ]
                ),
            ],
            title="缩放控制",
            style={"marginBottom": 24, "width": 500},
        ),
        # A4容器外框（用于显示边界和滚动）
        html.Div(
            [
                # A4页面容器
                html.Div(
                    [
                        # 模拟A4纸上的内容元素
                        # 标题
                        html.Div(
                            "A4文档标题",
                            style={
                                "fontSize": 24,
                                "fontWeight": "bold",
                                "textAlign": "center",
                                "marginBottom": 20,
                                "borderBottom": "2px solid #333",
                                "paddingBottom": 10,
                            },
                        ),
                        # 段落文本
                        html.P(
                            "这是一段示例文本，用于演示A4页面缩放功能。当你调整缩放比例时，A4页面内的所有元素都会按比例缩放。",
                            style={
                                "fontSize": 14,
                                "lineHeight": 1.8,
                                "marginBottom": 15,
                            },
                        ),
                        # 表格示例
                        html.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th("项目", style={"border": "1px solid #333", "padding": "8px", "backgroundColor": "#f0f0f0"}),
                                            html.Th("数量", style={"border": "1px solid #333", "padding": "8px", "backgroundColor": "#f0f0f0"}),
                                            html.Th("单价", style={"border": "1px solid #333", "padding": "8px", "backgroundColor": "#f0f0f0"}),
                                            html.Th("金额", style={"border": "1px solid #333", "padding": "8px", "backgroundColor": "#f0f0f0"}),
                                        ]
                                    )
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td("商品A", style={"border": "1px solid #333", "padding": "8px"}),
                                                html.Td("2", style={"border": "1px solid #333", "padding": "8px", "textAlign": "center"}),
                                                html.Td("¥100.00", style={"border": "1px solid #333", "padding": "8px", "textAlign": "right"}),
                                                html.Td("¥200.00", style={"border": "1px solid #333", "padding": "8px", "textAlign": "right"}),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("商品B", style={"border": "1px solid #333", "padding": "8px"}),
                                                html.Td("1", style={"border": "1px solid #333", "padding": "8px", "textAlign": "center"}),
                                                html.Td("¥150.00", style={"border": "1px solid #333", "padding": "8px", "textAlign": "right"}),
                                                html.Td("¥150.00", style={"border": "1px solid #333", "padding": "8px", "textAlign": "right"}),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("商品C", style={"border": "1px solid #333", "padding": "8px"}),
                                                html.Td("3", style={"border": "1px solid #333", "padding": "8px", "textAlign": "center"}),
                                                html.Td("¥50.00", style={"border": "1px solid #333", "padding": "8px", "textAlign": "right"}),
                                                html.Td("¥150.00", style={"border": "1px solid #333", "padding": "8px", "textAlign": "right"}),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            style={
                                "width": "100%",
                                "borderCollapse": "collapse",
                                "marginBottom": 20,
                                "fontSize": 12,
                            },
                        ),
                        # 图片区域
                        html.Div(
                            [
                                html.Div(
                                    "图片占位区域",
                                    style={
                                        "width": 200,
                                        "height": 150,
                                        "backgroundColor": "#e6f7ff",
                                        "border": "2px dashed #1890ff",
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "marginBottom": 10,
                                        "color": "#1890ff",
                                    },
                                ),
                                html.Div(
                                    "签名区域: _________________",
                                    style={
                                        "textAlign": "right",
                                        "marginTop": 30,
                                        "fontSize": 14,
                                    },
                                ),
                            ]
                        ),
                        # 多个装饰性元素
                        html.Div(
                            [
                                html.Div(
                                    "",
                                    style={
                                        "width": 50,
                                        "height": 50,
                                        "backgroundColor": "#ff4d4f",
                                        "borderRadius": "50%",
                                        "display": "inline-block",
                                        "margin": 5,
                                    },
                                ),
                                html.Div(
                                    "",
                                    style={
                                        "width": 50,
                                        "height": 50,
                                        "backgroundColor": "#52c41a",
                                        "borderRadius": "50%",
                                        "display": "inline-block",
                                        "margin": 5,
                                    },
                                ),
                                html.Div(
                                    "",
                                    style={
                                        "width": 50,
                                        "height": 50,
                                        "backgroundColor": "#1890ff",
                                        "borderRadius": "50%",
                                        "display": "inline-block",
                                        "margin": 5,
                                    },
                                ),
                            ],
                            style={"textAlign": "center", "marginTop": 20},
                        ),
                    ],
                    id="a4-container",
                    style={
                        "width": A4_WIDTH_PX,
                        "height": A4_HEIGHT_PX,
                        "backgroundColor": "white",
                        "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
                        "padding": 40,
                        "boxSizing": "border-box",
                        "transformOrigin": "top center",
                        "transition": "transform 0.2s ease",
                    },
                ),
            ],
            style={
                "overflow": "auto",
                "padding": 40,
                "backgroundColor": "#f5f5f5",
                "minHeight": "calc(100vh - 200px)",
                "width": "100%",
            },
        ),
    ],
    style=style(
        width="100vw",
        minHeight="100vh",
        backgroundColor="#fafafa",
        padding="20px 0",
        display="flex",
        flexDirection="column",
    ),
)


# 滑块缩放回调
@app.callback(
    Output("a4-container", "style"),
    Output("zoom-value", "children"),
    Input("zoom-slider", "value"),
    prevent_initial_call=False,
)
def update_zoom(slider_value):
    """根据滑块值更新缩放"""
    scale = slider_value or 1.0
    new_style = {
        "width": A4_WIDTH_PX,
        "height": A4_HEIGHT_PX,
        "backgroundColor": "white",
        "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
        "padding": 40,
        "boxSizing": "border-box",
        "transformOrigin": "top center",
        "transition": "transform 0.2s ease",
        "transform": f"scale({scale})",
    }
    return new_style, f"{int(scale * 100)}%"


# 按钮缩放回调
@app.callback(
    Output("zoom-slider", "value"),
    Input("zoom-in-btn", "nClicks"),
    Input("zoom-out-btn", "nClicks"),
    Input("zoom-reset-btn", "nClicks"),
    State("zoom-slider", "value"),
    prevent_initial_call=True,
)
def button_zoom(in_clicks, out_clicks, reset_clicks, current_value):
    """处理按钮缩放"""
    current = current_value or 1.0
    ctx = dash.callback_context
    if not ctx.triggered:
        return current

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "zoom-in-btn":
        return min(2.0, round(current + 0.1, 1))
    elif triggered_id == "zoom-out-btn":
        return max(0.5, round(current - 0.1, 1))
    elif triggered_id == "zoom-reset-btn":
        return 1.0

    return current


if __name__ == "__main__":
    app.run(debug=True, port=8051)
