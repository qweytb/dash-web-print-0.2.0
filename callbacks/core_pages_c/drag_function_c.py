"""功能区回调模块"""

import time
import dash
from dash import set_props, Patch, html
from dash import Input, Output, State, ClientsideFunction
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from loguru import logger
import time

from server import app

# 导入布局
import views.core_pages.drag_function as drag_function
from views.core_pages import drag_element


# 拖拽元素的属性编辑
@app.callback(
    Output("drag-element-picture", "style"),
    Output("drag-element-data", "style"),
    Output("drag-element-property-attributes", "style"),
    Input("element_property_attributes", "value"),
    prevent_initial_call=True,
)
def drag_element_property_attributes(value):

    # print(value)
    list_ = [style(display="block"), style(display="block"), style(display="block")]
    if not value:
        return [style(display="none"), style(display="none"), style(display="none")]
    if "picture-list" not in value:
        list_[0] = style(display="none")
    if "picture-data" not in value:
        list_[1] = style(display="none")
    if "property-attributes" not in value:
        list_[2] = style(display="none")

    return list_


# 点开打印模版菜单
@app.callback(
    Output("global-message", "children", allow_duplicate=True),
    Input("print-template", "nClicks"),
    prevent_initial_call=True,
)
def print_template_menu(nClicks):
    if not nClicks:
        return dash.no_update
    return fac.AntdModal("开发中......", title="模版管理", visible=True)


# 保存打印模版
@app.callback(
    Output("global-message", "children", allow_duplicate=True),
    Input("save-template", "nClicks"),
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def save_print_template(nClicks, data):
    if not nClicks:
        return dash.no_update
    return fac.AntdModal(
        fuc.FefferyScrollbars(
            fuc.FefferyJsonViewer(
                id="json-viewer-demo1",
                data=data,
                theme="solarized",
                collapsed=2,
            ),
            style={
                "maxHeight": "70vh",
                "maxWidth": "600px",
                "border": "1px dashed #e1dfdd",
            },
        ),
        title="保存打印模版",
        visible=True,
        width=1000,
    )


# 预览打印模版
@app.callback(
    Output("global-message", "children", allow_duplicate=True),
    Input("preview-template", "nClicks"),
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def preview_print_template(nClicks, data):
    if not nClicks:
        return dash.no_update
    drag_canvas = data["drag_canvas"]
    m_px_w = drag_canvas["m_px_w"]
    m_mm_w = drag_canvas["m_mm_w"]
    m_mm_h = drag_canvas["m_mm_h"]
    logger.info(f"打印模版宽高：{m_px_w} * {drag_canvas['m_px_h']}")
    return fac.AntdModal(
        fac.AntdSpace(
            [
                # 执行JS
                fuc.FefferyExecuteJs(id="print-js-window"),
                # 元素转图片
                fuc.FefferyDom2Image(id="print-target-window"),
                fuc.FefferyInViewport(
                    html.Div(
                        [
                            html.Div(
                                # children=rendered_components,
                                id="preview-template-canvas-pages",
                                style=style(
                                    width=f"{m_mm_w}mm",
                                    height=f"{m_mm_h}mm",
                                    # 相对定位
                                    position="relative",
                                    margin="0",
                                    padding="0",
                                ),
                            ),
                        ],
                        style=style(border="1px solid #8c8c8c", background="white", boxSizing="border-box", margin=2),
                    ),
                    id="preview-template-canvas",
                    threshold=1,
                ),
                fac.AntdSpace(
                    [
                        fac.AntdButton("弹窗打印", id="print-popup-window", size="middle", variant="dashed", color="primary"),
                        fac.AntdButton("PDF打印", id="print-target-trigger-pdf", size="middle", variant="dashed", color="danger"),
                        fac.AntdButton("静默打印", size="middle", variant="dashed", color="gold"),
                    ],
                    direction="vertical",
                    size="small",
                ),
            ],
            size="small",
            align="start",
        ),
        id="preview-print-template-modal",
        title="预览打印模版",
        visible=True,
        width=int(m_px_w) + 200,
        className={".ant-modal-content": {"padding": "20px 24px"}},
    )


# 打开预览窗口之后渲染预览
@app.callback(
    Output("preview-template-canvas-pages", "children"),
    Input("preview-template-canvas", "inViewport"),
    State("preview-print-template-modal", "visible"),
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def in_viewport_demo1(inViewport, visible, data):
    if not inViewport and not visible:
        return []

    time.sleep(0.5)

    drag_layout_list = data.get("drag_layout_list")
    new_children = []
    for k, v in drag_layout_list.items():
        deag_layout = drag_element.drag_element_layout(
            element_config=v,  # 元素配置
            element_preview=True,  # 元素预览,
        )
        deag_layout = deag_layout["rnd"]
        new_children.append(deag_layout)
    return new_children


# 路由里面渲染的组件，打印指定元素ding
@app.callback(
    Output("print-target-window", "targetSelector"),
    Input("print-popup-window", "nClicks"),
    prevent_initial_call=True,  # 注释掉实现自动打印
)
def get_print_target_2(nClicks):
    return "#preview-template-canvas-pages"


# 弹窗打印
@app.callback(
    Output("print-js-window", "jsString"),
    Input("print-target-window", "screenshotResult"),
    prevent_initial_call=True,
)
def execute_js_demo_2(screenshotResult):
    data = screenshotResult.get("dataUrl")

    # 创建包含 base64 图像的 HTML 内容
    html_content = f"""
    <html>
        <body>
            <img src="{data}" style="width:100%;">
        </body>
    </html>
    """

    # 使用 iframe 打印
    js = f"""
    var iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    document.body.appendChild(iframe);
    iframe.contentDocument.write(`{html_content}`);
    iframe.contentDocument.close();
    iframe.onload = function() {{
        iframe.contentWindow.print();
        document.body.removeChild(iframe);
    }};
    """

    return js


# pdf 打印
@app.callback(
    Output("print-js-window", "jsString", allow_duplicate=True),
    Input("print-target-trigger-pdf", "nClicks"),
    State("layout-helper-config", "data"),  # 布局配置数据,
    prevent_initial_call=True,
)
def execute_js_demo_2_pdf(nClicks, data):
    if not nClicks:
        return dash.no_update
    import uuid

    drag_canvas = data["drag_canvas"]
    paper_type = drag_canvas.get("m_paper_type")
    m_mm_w = drag_canvas["m_mm_w"]
    m_mm_h = drag_canvas["m_mm_h"]

    type_name = paper_type  # "A4"

    zdy = f"""jsPDF: {{ unit: 'mm', format: [{m_mm_w},{m_mm_h}], orientation: 'p' }}"""
    a3 = """jsPDF: { unit: 'mm', format: 'a3', orientation: 'p' }"""
    a5 = """jsPDF: { unit: 'mm', format: 'a5', orientation: 'l' }"""
    a4 = """jsPDF: { unit: 'mm', format: 'a4', orientation: 'p' }"""  # 默认
    if type_name == "A5":
        jsPDF = a5
    if type_name == "A4":
        jsPDF = a4
    if type_name == "A3":
        jsPDF = a3
    if type_name in ["自定义", "A5/90", "A4/3"]:
        jsPDF = zdy

    js_code = f"""
    var a = "{uuid.uuid4()}"; // 保证jsString每次都有变动
    var element = document.getElementById("preview-template-canvas-pages");
    html2pdf()
        .set({{
            image: {{ type: 'jpeg', quality: 1 }},
            html2canvas: {{
                dpi: 192,
                scale: 1,
                logging: true,
                useCORS: true,
                y: 0,
                scrollX: 0,
                scrollY: 0,
                width: element.offsetWidth,
                pagebreak: {{ mode: ['avoid-all'] }},
                height: element.scrollHeight
            }},
            {jsPDF}
        }})
        .from(element)
        .toPdf()
        .get('pdf')
        .then(function(pdf) {{
            if (pdf.getNumberOfPages() > 1) {{
                pdf.deletePage(2); // 删除第二页
            }}
            return pdf.output('bloburl');
        }})
        .then(function(pdfUrl){{
            window.open(pdfUrl, '_blank');
        }});
    """

    return js_code


# 布局助手帮助画面
@app.callback(
    Output("global-message", "children", allow_duplicate=True),
    Input("help-template", "nClicks"),
    prevent_initial_call=True,
)
def help_layout_helper(nClicks):
    if not nClicks:
        return dash.no_update
    return fac.AntdModal("开发中......", title="布局助手帮助画面", visible=True)
