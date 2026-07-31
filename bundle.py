#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 FBA 货件物流同步管理系统打包为单文件 HTML。
- 内联 css/style.css 到 <style>
- 内联所有 js/*.js（含 xlsx / jszip 库）到 <script>
- 移除 manifest / sw.js 引用（单文件部署不需要，且会静默失败）
这样部署到任何免费静态托管平台时只需上传这 1 个文件，彻底避免目录结构和 MIME 问题。
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE, "index.html")
OUT_PATH = os.path.join(BASE, "standalone.html")

def read(p):
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def escape_script(s):
    # ★ 全面清理内联 JS 中可能破坏 HTML 解析的内容
    # 1. 删除所有 <!-- ... --> HTML 注释（xlsx 库中存在，会导致浏览器把后续内容当注释）
    s = re.sub(r'<!--.*?-->', '', s, flags=re.DOTALL)
    # 2. </script → 防止提前闭合 script 标签
    s = s.replace("</script", "<\\/script")
    # 3. ]]> → 防止打破 CDATA / XHTML 解析
    s = s.replace("]]>", "]\\]>")
    return s

html = read(HTML_PATH)

# 1. 内联 CSS：替换 <link rel="stylesheet" href="css/style.css">
css = read(os.path.join(BASE, "css", "style.css"))
html = html.replace(
    '<link rel="stylesheet" href="css/style.css">',
    "<style>\n" + css + "\n</style>"
)

# 2. 移除 manifest 引用（单文件部署无意义，且会产生 404）
html = html.replace('<link rel="manifest" href="manifest.json">\n', "")

# 3. 内联所有 <script src="..."> 标签
script_files = [
    "js/xlsx.full.min.js",
    "js/jszip.min.js",
    "js/db.js",
    "js/app.js",
    "js/shipping-plan.js",
]
for sf in script_files:
    tag = f'<script src="{sf}"></script>'
    content = read(os.path.join(BASE, sf))
    inline = "<script>\n" + escape_script(content) + "\n</script>"
    if tag in html:
        html = html.replace(tag, inline)
    else:
        print(f"WARNING: 未找到标签 {tag}")

# 4. 移除 service worker 注册（sw.js 不存在，注册会失败；已在 try/catch 中，但单文件部署更干净）
html = re.sub(
    r"\s*if \('serviceWorker' in navigator\) \{[^}]*\}",
    "",
    html
)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize(OUT_PATH)
print(f"OK 生成单文件: {OUT_PATH}")
print(f"文件大小: {size/1024:.1f} KB ({size} bytes)")

# 5. 基本校验：确认关键内容已内联
checks = {
    "xlsx 库内联": "XLSX" in html or "SheetJS" in html,
    "JSZip 库内联": "JSZip" in html or "jszip" in html.lower(),
    "DB 对象内联": "const DB" in html or "class DB" in html or "DB =" in html,
    "App 对象内联": "const App" in html,
    "ShippingPlan 内联": "ShippingPlan" in html,
    "style 标签存在": "<style>" in html,
    "无残留 link css": 'href="css/style.css"' not in html,
    "无残留 script src": "<script src=" not in html,
}
print("--- 校验 ---")
for k, v in checks.items():
    print(f"  [{'OK' if v else 'FAIL'}] {k}")
