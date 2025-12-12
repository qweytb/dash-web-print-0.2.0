import dash
from dash import html, set_props
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style

from dash import Input, Output

# 实例化Dash应用对象
app = dash.Dash(__name__)

# 添加初始化页面内容
app.layout = fac.AntdCenter(
    [
        html.Div(
            [
                fuc.FefferyRND(
                    [i],
                    id={"type": "rnd-block", "index": i},
                    size={"width": 50, "height": 50},
                    position={"x": i * 53, "y": 50},
                    direction=[],  # 关闭尺寸调整功能
                    bounds="parent",
                    style=style(background="white", padding=24, boxShadow="0 0 8px #d9d9d9"),
                )
                for i in range(15)
            ],
            style=style(border="1px solid #8c8c8c", height=600, width=800, backgroundColor="#5e4646"),
        ),
    ],
    style=style(
        width="100vw",
        height="100vh",
        backgroundColor="#2161c0",
    ),
)


if __name__ == "__main__":
    app.run(debug=True)
