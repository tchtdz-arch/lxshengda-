#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给中文站页面补 hreflang，与 /en/ 英文站互指"""
import os, io, glob
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.lxshengda.com"
SKIP = {"404.html", "baidu_verify_codeva-cIOc4y6zQh.html", "google7fb949e9a0e3fcea.html"}

for path in sorted(glob.glob(os.path.join(HERE, "*.html"))):
    page = os.path.basename(path)
    if page in SKIP:
        continue
    s = io.open(path, encoding="utf-8").read()
    if "hreflang" in s:
        print("已存在，跳过:", page)
        continue
    soup = BeautifulSoup(s, "html.parser")
    head = soup.head
    if not head:
        print("无 head，跳过:", page)
        continue
    for hreflang, url in [("zh-CN", f"{SITE}/{page}"),
                          ("en", f"{SITE}/en/{page}"),
                          ("x-default", f"{SITE}/{page}")]:
        tag = soup.new_tag("link")
        tag["rel"] = "alternate"
        tag["hreflang"] = hreflang
        tag["href"] = url
        head.append(tag)
    io.open(path, "w", encoding="utf-8", newline="").write(str(soup))
    print("已加 hreflang:", page)
