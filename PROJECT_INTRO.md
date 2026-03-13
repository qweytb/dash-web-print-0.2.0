# 🎨 打印布局设计器

一个基于 Python 的高性能、拖拽式打印模板设计工具，使用 Dash + Feffery Antd Components 构建。

## ✨ 核心特性

- **直观的拖拽设计** - 无需编程，拖拽即可设计复杂打印模板
- **丰富的元素库** - 支持线条、矩形、文本、图片、表格、二维码、条形码等20+元素类型
- **智能吸附系统** - 网格吸附、对齐辅助线、缩放控制
- **精确样式控制** - 颜色、阴影、渐变、混合模式等高级样式
- **多页面支持** - 同时设计和管理多个页面模板
- **数据绑定** - 支持静态数据和动态数据源绑定
- **PDF导出** - 一键生成专业PDF文档
- **纯Python栈** - 从前端到后端完全使用Python实现

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python server.py
```

## 🛠️ 技术栈

- **前端框架**: Dash 3.x (基于 Flask + React)
- **UI组件**: Feffery Antd Components
- **工具库**: Feffery Utils Components
- **图像处理**: Pillow
- **条码生成**: python-barcode, qrcode
- **PDF生成**: ReportLab

## 📦 主要功能

### 设计功能
- 🎯 20+ 种拖拽元素（线条、形状、文本、图片、表格等）
- 📏 网格吸附、辅助线、标尺、缩放
- 🎨 高级样式系统（颜色、渐变、阴影、混合模式）
- 🔧 层级管理、锁定、透明度控制
- 📄 多页面支持、模板保存/加载

### 数据功能
- 💾 静态内容编辑
- 🔗 JSON/API 数据源绑定
- 📊 条件显示逻辑
- 📤 PDF导出

### 行业应用
- 🏢 企业文档设计
- 📦 物流标签设计
- 🏥 医疗证卡制作
- 🎓 教育证件设计
- 🏭 工业标签设计

## 📋 系统要求

- Python 3.8 - 3.13
- 4GB+ RAM
- 现代浏览器（Chrome/Firefox/Safari/Edge）

## 🗺️ 项目结构

```
web-拖拽-打印票据0.2.0/
├── app.py                      # 主应用入口
├── server.py                   # 服务器配置
├── configs/                    # 配置文件
│   ├── base_config.py
│   └── router_config.py
├── callbacks/                  # 回调函数
│   └── core_pages_c/          # 核心页面回调
│       ├── drag_element_c.py  # 拖拽元素逻辑
│       └── drag_help_c.py     # 辅助工具逻辑
├── views/                      # 视图
│   ├── core_pages/            # 核心页面
│   │   ├── drag_element.py    # 拖拽元素页面
│   │   └── drag_help.py       # 辅助工具页面
│   └── status_pages/          # 状态页面
├── utils/                      # 工具函数
│   ├── pages_utils.py         # 页面工具
│   └── image_utils.py         # 图像工具
├── requirements.txt            # Python依赖
└── PROJECT_INTRO.md           # 项目简介（本文件）

```

## 🎯 使用场景

- 🏢 **企业文档设计** - 合同、协议、通知等模板设计
- 📦 **物流标签** - 运输标签、包裹标签、仓储标签
- 🏥 **医疗证卡** - 患者腕带、处方单、设备标签
- 🎓 **教育证件** - 学生证、成绩单、证书设计
- 🏭 **工业标签** - 产品标签、设备标识、说明书

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- **项目预览**: http://bjzs.yangtianbao.cn
- **Dash官网**: https://dash.plotly.com/
- **Feffery组件**: https://github.com/CNFeffery

---

**让专业打印设计变得简单！**
