#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度站长平台 · 普通收录 API 主动推送
用法：
    1) 把 token 写进同目录 baidu_token.txt（单行，只有 token 字符串）
    2) python baidu_push.py            # 推送 sitemap.xml 中全部页面
       python baidu_push.py https://www.lxshengda.com/products.html   # 只推指定 URL
说明：
    - 每日配额见返回字段 remain，超额会返回 error 400
    - 推送成功不代表收录，仅代表百度已收到
"""
import os, re, sys, json, urllib.request, urllib.parse

# 注意：百度 API 的 site 参数必须是不带协议的域名，
# 带 https:// 会返回 {"error":400,"message":"site init fail"}
SITE = "www.lxshengda.com"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, "baidu_token.txt")
SITEMAP = os.path.join(HERE, "sitemap.xml")


def read_token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"[x] 未找到 {TOKEN_FILE}\n    请先创建该文件并写入百度推送 token（单行）")
    tok = open(TOKEN_FILE, encoding="utf-8-sig").read().strip()
    if not tok:
        sys.exit("[x] baidu_token.txt 为空")
    return tok


def collect_urls():
    if len(sys.argv) > 1:
        return [a for a in sys.argv[1:] if a.startswith("http")]
    if not os.path.exists(SITEMAP):
        sys.exit(f"[x] 未找到 {SITEMAP}")
    xml = open(SITEMAP, encoding="utf-8").read()
    urls = re.findall(r"<loc>(https://www\.lxshengda\.com/[^<]*)</loc>", xml)
    urls = [u for u in urls if not u.lower().endswith((".webp", ".jpg", ".jpeg", ".png", ".gif"))]
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def push(token, urls):
    endpoint = "http://data.zz.baidu.com/urls?" + urllib.parse.urlencode({"site": SITE, "token": token})
    body = "\n".join(urls).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "text/plain", "User-Agent": "curl/8.0"},
        method="POST",
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
    urls = collect_urls()
    if not urls:
        sys.exit("[x] 没有可推送的 URL")
    print(f"[i] 站点：{SITE}")
    print(f"[i] 待推送 {len(urls)} 条 URL")
    status, text = push(token, urls)
    print(f"[i] HTTP {status}")
    try:
        data = json.loads(text)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        if "success" in data:
            print(f"[✓] 成功推送 {data['success']} 条，今日剩余配额 {data.get('remain', '?')}")
            for k in ("not_same_site", "not_valid", "error"):
                if data.get(k):
                    print(f"[!] {k}: {data[k]}")
        else:
            print("[!] 推送未成功，检查 token / 站点归属 / 配额")
    except json.JSONDecodeError:
        print("[raw]", text[:500])


if __name__ == "__main__":
    main()
