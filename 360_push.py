#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
360 搜索站长平台 · URL 主动推送（API 批量提交）

特点（对比百度）：
  - 360 配额大得多（约 500 条/天/站点），可一次批量 POST
  - site 参数用不带协议的域名：www.lxshengda.com
  - 接口：https://data.360.cn/api/submit?site=<域名>&token=<token>

准备工作：
  1. 在 https://zhanzhang.so.com/ 登录 → 添加站点 www.lxshengda.com → 验证（文件/HTML标签/CNAME 任选）
  2. 验证通过后进入「数据提交」页，拿到接口 token
  3. 把 token 写入同目录 360_token.txt（单行）

用法：
  python 360_push.py                 # 推送 sitemap 全部页面
  python 360_push.py <url> [<url>…]  # 只推指定 URL
"""
import os, re, sys, time, urllib.request, urllib.parse, datetime

SITE = "www.lxshengda.com"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, "360_token.txt")
SITEMAP = os.path.join(HERE, "sitemap.xml")
PENDING = os.path.join(HERE, "pending360.txt")
LOG = os.path.join(HERE, "push360.log")


def read_token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"[x] 未找到 {TOKEN_FILE}\n    请先创建该文件并写入 360 推送 token（单行）")
    tok = open(TOKEN_FILE, encoding="utf-8-sig").read().strip()
    if not tok:
        sys.exit("[x] 360_token.txt 为空")
    return tok


def sitemap_urls():
    if not os.path.exists(SITEMAP):
        return []
    xml = open(SITEMAP, encoding="utf-8").read()
    urls = re.findall(r"<loc>(https://www\.lxshengda\.com/[^<]*)</loc>", xml)
    return [u for u in urls if not u.lower().endswith((".webp", ".jpg", ".jpeg", ".png", ".gif"))]


def read_pending():
    if not os.path.exists(PENDING):
        return []
    return [l.strip() for l in open(PENDING, encoding="utf-8") if l.strip().startswith("http")]


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def submit(token, urls):
    ep = "https://data.360.cn/api/submit?" + urllib.parse.urlencode({"site": SITE, "token": token})
    body = "\n".join(urls).encode("utf-8")
    req = urllib.request.Request(
        ep, data=body, headers={"Content-Type": "text/plain; charset=utf-8"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def main():
    token = read_token()

    if len(sys.argv) > 1:
        targets = [a for a in sys.argv[1:] if a.startswith("http")]
    else:
        pend = read_pending()
        rest = [u for u in sitemap_urls() if u not in pend]
        targets = list(dict.fromkeys(pend + rest))

    if not targets:
        log("[x] 没有可推送的 URL")
        return

    log(f"[i] 360 提交 · 站点 {SITE} · 共 {len(targets)} 条")
    code, body = submit(token, targets)
    log(f"[i] HTTP {code} · {body[:300]}")

    # 成功则清空 pending，失败则全部记入 pending 待重试
    ok = code == 200 and ("success" in body.lower() or "ok" in body.lower() or body.strip().startswith("{"))
    if ok:
        open(PENDING, "w", encoding="utf-8").write("")
        log(f"[OK] 已提交 {len(targets)} 条，pending 清空")
    else:
        open(PENDING, "w", encoding="utf-8").write("\n".join(targets) + "\n")
        log(f"[!!] 提交未成功，已写入 {PENDING} 待重试（{len(targets)} 条）")


if __name__ == "__main__":
    main()
