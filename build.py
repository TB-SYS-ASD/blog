#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键把 posts/*.md → posts/*.html
暗黑新中式风格 + 可选 Pygments 代码高亮
用法: python build.py
"""
import os
import re
import html
import datetime
from pathlib import Path

POST_DIR   = Path('posts')
TMPL_FILE  = Path('template.html')
# 如果希望用 Pygments，请 pip install pygments，然后置为 True
USE_PYGMENTS = False

try:
    if USE_PYGMENTS:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, guess_lexer
        from pygments.formatters import html as pygments_html
        from pygments.util import ClassNotFound
except ImportError:
    USE_PYGMENTS = False

def highlight_code(match):
    """把 ```lang...``` 转成高亮 HTML"""
    lang, code = match.group(1) or '', match.group(2)
    if USE_PYGMENTS:
        try:
            lexer = get_lexer_by_name(lang) if lang else guess_lexer(code)
            formatter = pygments_html.HtmlFormatter(style='atom-one-dark')
            return highlight(code, lexer, formatter)
        except ClassNotFound:
            pass
    # fallback
    code_esc = html.escape(code.strip())
    return f'<pre><code>{code_esc}</code></pre>'

def md2html(text: str) -> str:
    """极简 markdown → html（仅常用语法）"""
    # 1. 代码块
    text = re.sub(r'```(\w+)?\n(.*?)```', highlight_code, text, flags=re.S)
    # 2. 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 3. 图片
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    # 4. 链接
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # 5. 标题
    for i in range(6, 0, -1):
        text = re.sub(r'^' + '#' * i + r'\s+(.+)$', rf'<h{i}>\1</h{i}>', text, flags=re.M)
    # 6. 粗体 & 斜体
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    # 7. 引用
    text = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', text, flags=re.M)
    # 8. 列表
    text = re.sub(r'^\* (.+)$', r'<li>\1</li>', text, flags=re.M)
    text = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\n\g<0>\n</ul>', text, flags=re.S)
    # 9. 段落
    text = re.sub(r'\n{2,}', '</p><p>', text)
    text = f'<p>{text}</p>'
    # 10. 换行
    text = text.replace('\n', '<br>')
    return text

def build():
    tmpl = TMPL_FILE.read_text(encoding='utf-8')
    highlight_css = ''
    if USE_PYGMENTS:
        from pygments.formatters import HtmlFormatter
        highlight_css = '<style>' + HtmlFormatter(style='atom-one-dark').get_style_defs('.highlight') + '</style>'

    for md_file in POST_DIR.glob('*.md'):
        html_file = md_file.with_suffix('.html')
        md_text = md_file.read_text(encoding='utf-8')
        # 第一行如果是 # 标题，提取当 title
        title_match = re.match(r'^#\s+(.+)$', md_text, re.M)
        title = title_match.group(1).strip() if title_match else md_file.stem
        content = md2html(md_text)
        html_out = (tmpl
                    .replace('{{title}}', html.escape(title))
                    .replace('{{content}}', content)
                    .replace('{{highlight_css}}', highlight_css))
        html_file.write_text(html_out, encoding='utf-8')
        print(f'✔  {md_file}  →  {html_file}')

if __name__ == '__main__':
    build()   import subprocess
subprocess.run(['python','build_index.py'])