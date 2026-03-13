import math
import re
import dash
from dash import html, dcc, Input, Output


def calculate_font_size_v3(
    text,
    container_width,
    container_height,
    max_font_size=24,
    min_font_size=12,
    step=1,
    padding_x=20,
    padding_y=10,
    line_height_ratio=1.2,
    width_safety_ratio=0.95,  # 稍微保守一点
    height_safety_ratio=0.90,
):
    """
    修复版：确保算法算出的换行和浏览器实际一致

    关键修复：
    1. 每行字数估算更保守（考虑浏览器实际渲染）
    2. 强制换行样式和算法逻辑匹配
    """

    if not text:
        return max_font_size

    # 可用空间
    effective_padding_y = min(padding_y * 2, container_height * 0.3)
    effective_padding_x = min(padding_x * 2, container_width * 0.2)
    available_width = (container_width - effective_padding_x) * width_safety_ratio
    available_height = (container_height - effective_padding_y) * height_safety_ratio

    if available_width <= 0 or available_height <= 0:
        return min_font_size

    total_chars = len(text)

    current_size = max_font_size

    while current_size >= min_font_size:
        line_height = current_size * line_height_ratio

        # 单行高度检查
        if line_height > available_height:
            current_size -= step
            continue

        # === 关键修复：每行字数估算要考虑实际字符宽度 ===
        # 中文字符实际宽度略大于字号，英文略小，平均按 1.0 算，但留余量
        # 实际测试发现，浏览器渲染时每个字会稍微宽一点，所以保守估计
        effective_char_width = current_size * 1.02  # 稍微高估字符宽度

        chars_per_line = math.floor(available_width / effective_char_width)

        if chars_per_line <= 0:
            current_size -= step
            continue

        # 计算需要的行数
        if total_chars <= chars_per_line:
            lines_needed = 1
        else:
            lines_needed = math.ceil(total_chars / chars_per_line)

        total_height = lines_needed * line_height

        if total_height <= available_height:
            return current_size

        current_size -= step

    return min_font_size


# === 备选方案：基于实际像素测量的思路 ===


def calculate_font_size_conservative(
    text,
    container_width,
    container_height,
    max_font_size=24,
    min_font_size=12,
    padding_x=20,
    padding_y=10,
    line_height_ratio=1.2,
):
    """
    更保守的方案：假设每个字符宽度 = font-size，但每行留 2-3 个字的余量
    确保第一行绝对不会溢出
    """

    if not text:
        return max_font_size

    effective_padding_y = min(padding_y * 2, container_height * 0.3)
    available_width = (container_width - min(padding_x * 2, container_width * 0.2)) * 0.95
    available_height = (container_height - effective_padding_y) * 0.90

    if available_width <= 0 or available_height <= 0:
        return min_font_size

    total_chars = len(text)

    for size in range(max_font_size, min_font_size - 1, -1):
        line_height = size * line_height_ratio

        if line_height > available_height:
            continue

        # 保守：每行留 3 个字的余量，确保不会溢出
        chars_per_line = max(math.floor(available_width / size) - 2, 1)

        if total_chars <= chars_per_line:
            return size

        lines = math.ceil(total_chars / chars_per_line)

        if lines * line_height <= available_height:
            return size

    return min_font_size


# === Dash 应用 ===

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H3("修复版：确保第一行满了就换行"),
        html.Div(
            [
                html.Label("测试文本（多复制一些测试）："),
                dcc.Input(
                    id="input-text",
                    value="你好世界这是一段测试文本请观察第一行填满后才换行你好世界这是一段测试文本请观察第一行填满后才换行",
                    style={"width": "100%", "fontSize": "16px"},
                    type="text",
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        html.Div(
            [
                html.Label("容器高度(px):"),
                dcc.Slider(id="height", min=40, max=200, step=5, value=80, marks={40: "40", 60: "60", 80: "80", 100: "100", 150: "150", 200: "200"}),
            ],
            style={"marginBottom": "10px"},
        ),
        html.Div(
            [
                html.Label("算法版本:"),
                dcc.RadioItems(
                    id="algorithm",
                    options=[
                        {"label": "V3-标准版", "value": "v3"},
                        {"label": "V4-保守版（每行留余量）", "value": "conservative"},
                    ],
                    value="conservative",  # 默认用保守版
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        # 显示区域
        html.Div(
            id="display-box",
            children=[html.Span(id="display-text")],
            style={
                "width": "600px",
                "height": "80px",
                "border": "2px solid #007bff",
                "borderRadius": "8px",
                "backgroundColor": "#f8f9fa",
                "padding": "10px 20px",
                "overflow": "hidden",
                "display": "flex",
                "alignItems": "flex-start",
                "justifyContent": "flex-start",
                "boxSizing": "border-box",
                "transition": "all 0.3s ease",
            },
        ),
        html.Div(id="debug", style={"marginTop": "10px", "fontFamily": "monospace", "whiteSpace": "pre-line"}),
    ]
)


@app.callback(
    [Output("display-text", "children"), Output("display-text", "style"), Output("display-box", "style"), Output("debug", "children")],
    [Input("input-text", "value"), Input("height", "value"), Input("algorithm", "value")],
)
def update(text, height, algo):
    width = 600

    if algo == "v3":
        size = calculate_font_size_v3(
            text,
            width,
            height,
            padding_y=10,
            line_height_ratio=1.2,
            max_font_size=24,
        )
    else:
        size = calculate_font_size_conservative(
            text,
            width,
            height,
            padding_y=10,
            line_height_ratio=1.2,
            max_font_size=24,
        )

    # 计算诊断信息
    avail_width = (width - 40) * 0.95
    avail_height = (height - 20) * 0.90

    # 用实际算法逻辑反推行数
    if algo == "v3":
        char_width = size * 1.02
        chars_per_line = math.floor(avail_width / char_width)
    else:
        chars_per_line = max(math.floor(avail_width / size) - 2, 1)

    total_chars = len(text)
    lines = 1 if total_chars <= chars_per_line else math.ceil(total_chars / chars_per_line)

    actual_height = lines * size * 1.2

    debug_info = f"""字号: {size}px
每行字数(算法): {chars_per_line}
总字数: {total_chars}
预估行数: {lines}
实际需高度: {actual_height:.1f}px
可用高度: {avail_height:.1f}px"""

    return (
        text,
        {
            "fontSize": f"{size}px",
            "lineHeight": "1.2",
            "wordBreak": "break-all",  # 强制任意位置换行
            "overflowWrap": "break-word",  # 额外保险
            "width": "100%",
            "margin": "0",
        },
        {
            "width": "600px",
            "height": f"{height}px",
            "border": "2px solid #007bff",
            "borderRadius": "12px",
            "backgroundColor": "#f8f9fa",
            # "padding": "10px 20px",
            # "overflow": "hidden",
            "display": "flex",
            "alignItems": "flex-start",
            "justifyContent": "flex-start",
            "boxSizing": "border-box",
            "transition": "all 0.3s ease",
        },
        html.Pre(debug_info, style={"background": "#f0f0f0", "padding": "10px", "borderRadius": "4px"}),
    )


if __name__ == "__main__":
    app.run(debug=True)
