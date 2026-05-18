import dash
from dash import html, Input, Output, State
import feffery_antd_components as fac
from feffery_dash_utils.style_utils import style

# 实例化Dash应用对象
app = dash.Dash(__name__)

# A4纸标准尺寸基准值 (210mm x 297mm) @ 96dpi
BASE_WIDTH = 794  # px
BASE_HEIGHT = 1123  # px


def scale_value(value, scale):
    """按比例缩放数值"""
    return int(value * scale)


def scale_style(base_styles, scale):
    """批量缩放样式中的尺寸属性"""
    scaled = {}
    for key, val in base_styles.items():
        if key in [
            "width",
            "height",
            "minWidth",
            "minHeight",
            "maxWidth",
            "maxHeight",
            "fontSize",
            "lineHeight",
            "margin",
            "marginTop",
            "marginBottom",
            "marginLeft",
            "marginRight",
            "padding",
            "paddingTop",
            "paddingBottom",
            "paddingLeft",
            "paddingRight",
            "borderWidth",
            "borderRadius",
            "top",
            "bottom",
            "left",
            "right",
        ]:
            if isinstance(val, (int, float)):
                # 数值型直接缩放
                scaled[key] = scale_value(val, scale)
            elif isinstance(val, str) and val.replace("px", "").isdigit():
                # px单位字符串
                num = int(val.replace("px", ""))
                scaled[key] = scale_value(num, scale)
            else:
                scaled[key] = val
        elif key == "border":
            # 处理 border: "1px solid #333" 这种格式
            if isinstance(val, str) and "px" in val:
                parts = val.split("px")
                if parts[0].strip().isdigit():
                    num = int(parts[0].strip())
                    scaled[key] = f"{scale_value(num, scale)}px" + "px".join(parts[1:])
                else:
                    scaled[key] = val
            else:
                scaled[key] = val
        else:
            scaled[key] = val
    return scaled


def create_a4_content(scale=1.0):
    """创建A4页面内容，所有尺寸按scale缩放"""

    # A4容器尺寸
    container_style = scale_style(
        {
            "width": BASE_WIDTH,
            "height": BASE_HEIGHT,
            "backgroundColor": "white",
            "boxShadow": "0 0 10px rgba(0,0,0,0.1)",
            "padding": 40,
            "boxSizing": "border-box",
            "position": "relative",
        },
        scale,
    )

    # 标题
    title = html.Div(
        "A4文档标题",
        style=scale_style(
            {
                "fontSize": 24,
                "fontWeight": "bold",
                "textAlign": "center",
                "marginBottom": 20,
                "borderBottom": "2px solid #333",
                "paddingBottom": 10,
            },
            scale,
        ),
    )

    # 段落文本
    paragraph = html.P(
        "这是一段示例文本，用于演示A4页面缩放功能。使用width/height方式缩放，文字和元素都保持清晰。",
        style=scale_style(
            {
                "fontSize": 14,
                "lineHeight": 1.8,
                "marginBottom": 15,
            },
            scale,
        ),
    )

    # 表格
    table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("项目", style=scale_style({"border": "1px solid #333", "padding": 8, "backgroundColor": "#f0f0f0", "fontSize": 12}, scale)),
                        html.Th("数量", style=scale_style({"border": "1px solid #333", "padding": 8, "backgroundColor": "#f0f0f0", "fontSize": 12}, scale)),
                        html.Th("单价", style=scale_style({"border": "1px solid #333", "padding": 8, "backgroundColor": "#f0f0f0", "fontSize": 12}, scale)),
                        html.Th("金额", style=scale_style({"border": "1px solid #333", "padding": 8, "backgroundColor": "#f0f0f0", "fontSize": 12}, scale)),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td("商品A", style=scale_style({"border": "1px solid #333", "padding": 8, "fontSize": 12}, scale)),
                            html.Td("2", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "center", "fontSize": 12}, scale)),
                            html.Td("¥100.00", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "right", "fontSize": 12}, scale)),
                            html.Td("¥200.00", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "right", "fontSize": 12}, scale)),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("商品B", style=scale_style({"border": "1px solid #333", "padding": 8, "fontSize": 12}, scale)),
                            html.Td("1", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "center", "fontSize": 12}, scale)),
                            html.Td("¥150.00", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "right", "fontSize": 12}, scale)),
                            html.Td("¥150.00", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "right", "fontSize": 12}, scale)),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("商品C", style=scale_style({"border": "1px solid #333", "padding": 8, "fontSize": 12}, scale)),
                            html.Td("3", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "center", "fontSize": 12}, scale)),
                            html.Td("¥50.00", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "right", "fontSize": 12}, scale)),
                            html.Td("¥150.00", style=scale_style({"border": "1px solid #333", "padding": 8, "textAlign": "right", "fontSize": 12}, scale)),
                        ]
                    ),
                ]
            ),
        ],
        style=scale_style(
            {
                "width": BASE_WIDTH - 80,  # 减去padding
                "borderCollapse": "collapse",
                "marginBottom": 20,
            },
            scale,
        ),
    )

    # 图片占位区
    image_area = html.Div(
        "图片占位区域",
        style=scale_style(
            {
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
            scale,
        ),
    )

    # 签名区
    signature = html.Div(
        "签名区域: _________________",
        style=scale_style(
            {
                "textAlign": "right",
                "marginTop": 30,
                "fontSize": 14,
            },
            scale,
        ),
    )

    # 装饰圆形
    circles = html.Div(
        [
            html.Div("", style=scale_style({"width": 50, "height": 50, "backgroundColor": "#ff4d4f", "borderRadius": 25, "display": "inline-block", "margin": 5}, scale)),
            html.Div("", style=scale_style({"width": 50, "height": 50, "backgroundColor": "#52c41a", "borderRadius": 25, "display": "inline-block", "margin": 5}, scale)),
            html.Div("", style=scale_style({"width": 50, "height": 50, "backgroundColor": "#1890ff", "borderRadius": 25, "display": "inline-block", "margin": 5}, scale)),
        ],
        style={"textAlign": "center", "marginTop": scale_value(20, scale)},
    )

    return html.Div(
        [title, paragraph, table, image_area, signature, circles],
        id="a4-container",
        style=container_style,
    )


# 布局
app.layout = fac.AntdCenter(
    [
        # 控制面板
        fac.AntdCard(
            [
                fac.AntdSpace(
                    [
                        fac.AntdText("缩放比例 (width/height方式):", strong=True),
                        fac.AntdSlider(
                            id="zoom-slider",
                            min=0.5,
                            max=1.5,
                            step=0.1,
                            value=1.0,
                            marks={0.5: "50%", 0.75: "75%", 1.0: "100%", 1.25: "125%", 1.5: "150%"},
                            style={"width": 350},
                        ),
                        fac.AntdText(id="zoom-value", style={"minWidth": 50}),
                    ],
                    align="center",
                ),
                fac.AntdDivider(),
                fac.AntdSpace(
                    [
                        fac.AntdButton("缩小", id="zoom-out-btn", type="primary", icon=fac.AntdIcon(icon="antd-minus")),
                        fac.AntdButton("75%", id="zoom-75-btn"),
                        fac.AntdButton("100%", id="zoom-100-btn"),
                        fac.AntdButton("125%", id="zoom-125-btn"),
                        fac.AntdButton("放大", id="zoom-in-btn", type="primary", icon=fac.AntdIcon(icon="antd-plus")),
                    ]
                ),
            ],
            title="缩放控制 (width/height方式 - 打印更清晰)",
            style={"marginBottom": 24, "width": 600},
        ),
        # A4容器外框
        html.Div(
            id="a4-wrapper",
            children=create_a4_content(1.0),
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


# 滑块缩放回调 - 重新渲染整个A4内容
@app.callback(
    Output("a4-wrapper", "children"),
    Output("zoom-value", "children"),
    Input("zoom-slider", "value"),
    prevent_initial_call=False,
)
def update_zoom(slider_value):
    """根据滑块值重新创建A4内容"""
    scale = slider_value or 1.0
    return create_a4_content(scale), f"{int(scale * 100)}%"


# 按钮缩放回调
@app.callback(
    Output("zoom-slider", "value"),
    Input("zoom-in-btn", "nClicks"),
    Input("zoom-out-btn", "nClicks"),
    Input("zoom-75-btn", "nClicks"),
    Input("zoom-100-btn", "nClicks"),
    Input("zoom-125-btn", "nClicks"),
    State("zoom-slider", "value"),
    prevent_initial_call=True,
)
def button_zoom(in_clicks, out_clicks, _75, _100, _125, current_value):
    """处理按钮缩放"""
    current = current_value or 1.0
    ctx = dash.callback_context
    if not ctx.triggered:
        return current

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "zoom-in-btn":
        return min(1.5, round(current + 0.1, 1))
    elif triggered_id == "zoom-out-btn":
        return max(0.5, round(current - 0.1, 1))
    elif triggered_id == "zoom-75-btn":
        return 0.75
    elif triggered_id == "zoom-100-btn":
        return 1.0
    elif triggered_id == "zoom-125-btn":
        return 1.25

    return current


if __name__ == "__main__":
    app.run(debug=True, port=8052)
