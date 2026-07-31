# FBA货件物流同步管理系统 (Web版)

## 特性

- **零依赖、零编译**：纯 HTML + CSS + JavaScript，双击 `index.html` 即可使用
- **本地存储**：使用浏览器内置 IndexedDB，数据完全在设备本地，无需任何服务器
- **跨平台**：Windows、macOS、Linux、Android、iOS — 任何有浏览器的设备都能运行
- **PWA 支持**：可安装到桌面/主屏幕，离线可用
- **响应式设计**：PC 端左右分栏布局，手机端自动切换为单列卡片布局

## 快速开始

### 方式1: 直接打开 (最简单)

1. 双击 `FBAShipmentWeb/index.html`
2. 浏览器自动打开，立即可用

### 方式2: 本地服务器 (推荐，支持PWA安装)

```bash
cd FBAShipmentWeb
python -m http.server 8080
# 然后打开 http://localhost:8080
```

### 方式3: 安装到桌面 (PWA)

Chrome/Edge 浏览器打开后 → 地址栏右侧「安装」按钮 → 安装为桌面应用

Android Chrome 打开后 → 菜单 → 「添加到主屏幕」

## 功能模块

| 模块 | 功能 |
|------|------|
| 首页概览 | 仪表盘数据统计、快速操作入口、最近风险和日志 |
| 货件列表 | FBA货件 CRUD、搜索筛选、详情查看、截图关联 |
| 导入Excel | 上传货代物流Excel表，智能识别列头，批量入库 |
| OCR识别 | 上传货代截图，Tesseract.js 中英文混合OCR识别 |
| 匹配管理 | 未匹配物流清单、手动绑定、已匹配关系查看 |
| 风险视图 | 蓝/黄/红三色风险标记、过期预警弹窗 |
| 操作日志 | 完整操作记录，按时间倒序 |
| 数据管理 | 导出JSON备份、导入恢复、清空数据 |

## 项目结构

```
FBAShipmentWeb/
├── index.html          # 主页面 (所有UI布局 + 应用控制器)
├── manifest.json       # PWA 清单
├── sw.js               # Service Worker (离线缓存)
├── css/
│   └── style.css       # 全局样式 (响应式设计)
├── js/
│   ├── db.js           # IndexedDB 数据库层 (CRUD/统计/导入导出)
│   └── app.js          # 业务逻辑层 (模型/工具/同步/风险/OCR/Excel)
└── icons/
    └── icon-192.svg    # PWA 图标
```

## 技术实现对照

| 原需求 | Web版实现 |
|--------|-----------|
| 企微智能表格 | IndexedDB 本地数据库 (shipments/logistics/matches/logs 四个表) |
| Excel导入 | SheetJS (xlsx) CDN 动态加载 |
| OCR截图识别 | Tesseract.js CDN 动态加载，中英文混合识别 |
| 数据持久化 | IndexedDB，所有数据存储在浏览器本地 |
| 绿色标记 | syncMark='synced' → row-synced CSS类 |
| 蓝色标记 | syncMark='risk_delay' → row-risk-delay CSS类 |
| 黄色标记 | syncMark='risk_group' → row-risk-group CSS类 |
| 红色过期 | syncMark='risk_expired' → row-risk-expired CSS类 |
| PC分栏布局 | flexbox layout, sidebar + main-content |
| 手机单列 | @media(max-width:768px) 自适应 |
| OCR失败容错 | 自动弹窗 → 手动录入表单 |
| 编码无法匹配 | 未匹配清单 + 下拉选择手动绑定 |
| 过期预警弹窗 | 首页自动检测并弹出过期预警 |

## 日期格式兼容

支持以下所有日期格式的智能解析：
- `2026-08-15` (ISO)
- `2026/08/15`
- `2026.08.15`
- `08-15-2026` (US)
- `15/08/2026` (EU)
- `20260815` (紧凑)
- `2026年8月15日` (中文)

## 浏览器兼容性

- Chrome/Edge 90+
- Firefox 90+
- Safari 15+
- Android Chrome 90+
- iOS Safari 15+
