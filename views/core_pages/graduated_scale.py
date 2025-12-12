"""刻度"""

from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style

# 导入刻度线布局
import callbacks.core_pages_c.graduated_scale_c as graduated_scale


def top_layout(extent=None, ratio=1.0):
    base_space = 4
    space_w = base_space * ratio
    # 计算刻度线根数：0 刻度也算一根
    n_ticks = int((extent - 25) / base_space) + 1

    ticks = []
    for i in range(n_ticks):
        # 刻度线
        ticks.append(
            html.Div(
                fac.AntdText(
                    str(i) if i % 10 == 0 else "",
                    type="secondary",
                    style=style(
                        # 绝对定位
                        position="absolute",
                        # left="1px",
                        top="-5px",
                        # 字体大小
                        fontSize="10px",
                        # 强制不换行
                        whiteSpace="nowrap",
                    ),
                ),
                style=style(
                    borderLeft="1px solid #000",
                    height="15px" if i % 10 == 0 else "7px",
                    position="relative",
                ),
            )
        )
        # 空白：最后一条刻度之后不加
        if i != n_ticks - 1:
            ticks.append(html.Div(style=style(width=f"{space_w}px", height="1px")))

    return fac.AntdFlex(
        [html.Div(style=style(width="25px", height="20px"))]
        + [fac.AntdSpace(ticks, size=0, align="end", style=style(width="100%", height="20px"))],
        gap=0,
        style=style(
            width=25 + n_ticks * 1 + (n_ticks - 1) * space_w,  # ← 公式写对
            height="25px",
            background="#FFF",
        ),
    )


def left_layout(extent=None, ratio=1.0):
    base_gap = 4  # 原来 AntdSpace size=4
    gap = base_gap * ratio  # 只放大间距
    n_ticks = int((extent - 20) / base_gap)  # 根数（含 0）

    ticks = []
    for i in range(n_ticks):
        ticks.append(
            html.Div(
                fac.AntdText(
                    str(i) if i % 10 == 0 else "",
                    type="secondary",
                    style=style(
                        position="absolute",
                        fontSize="10px",
                        whiteSpace="nowrap",
                        transform="rotate(90deg)",
                        transformOrigin="left bottom",
                        marginLeft="-5px",
                        marginTop="-13px",
                    ),
                ),
                style=style(
                    borderBottom="1px solid #000",
                    width="15px" if i % 10 == 0 else "7px",
                    position="relative",
                ),
            )
        )

    return fac.AntdSpace(
        ticks,
        size=gap,
        align="end",
        direction="vertical",
        style=style(
            width="20px",
            display="flex",
            justifyContent="flex-start",
            alignItems="flex-end",
        ),
    )
