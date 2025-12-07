#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 posts/*.md → 生成 posts/index.json
"""
import json
import re
from pathlib import Path
from datetime import datetime

POST_DIR = Path('posts')
INDEX_FILE = POST_DIR / 'index.json'

def extract_front_matter(md_text: str):
    fm_match = re.match(r'^---\n(.+?)\n---', md_text, re.S)
    data = {'title': None, 'date': None}
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if line.startswith('title:'):
                data['title'] = line.split(':', 1)[1].strip().strip('"\'')
            elif line.startswith('date:'):
                data['date'] = line.split(':', 1)[1].strip().strip('"\'')
    return data

def build():
    index = []
    for md in POST_DIR.glob('*.md'):
        text = md.read_text(encoding='utf-8')
        fm = extract_front_matter(text)
        title = fm['title'] or md.stem.replace('-', ' ')
        date  = fm['date'] or datetime.fromtimestamp(md.stat().st_mtime).strftime('%Y-%m-%d')
        html_file = md.with_suffix('.html').name
        index.append({'title': title, 'date': date, 'file': html_file})

    index.sort(key=lambda x: x['date'], reverse=True)
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✔ 已更新 {INDEX_FILE}  （共 {len(index)} 篇文章）')

if __name__ == '__main__':
    build()