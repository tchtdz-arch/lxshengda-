#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度站长平台 · 普通收录 API 主动推送（增强版）

特性：
  1. 从 sitemap.xml 提取全部页面 URL（过滤图片）
  2. 读取 pending.txt 中的待补推 URL，一并推送（优先级最高）
  3. 逐条推送而非批量 POST —— 百度每日配额极小（约 10 条/天）时，
     批量接口整批返回 over quota 会白跑，逐条推送能"用尽每一份额度"
  4. 推送失败（over quota）的 URL 自动写回 pending.txt，下次优先补推
  5. 成功记录写入 push.log，便于溯源

用法：
  python baidu_push.py              # 全量 + 补推 pending
  python baidu_push.py <url> [...]  # 只推指定 URL
说明：
  - 返回字段 remain 为当日剩余配额
  - 推送成功不代表收录，仅代表百度已收到
"""
import os, re, sys, json, time, urllib.request, urllib.parse, datetime

# 注意：百度 API 的 site 参数必须是不带协议的域名，
# 带 https:// 会返回 {"error":400,"message":"site init fail"}
SITE = "www.lxshengda.com"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, "baidu_token.txt")
SITEMAP = os.path.join(HERE, "sitemap.xml")
PENDING = os.path.join(HERE, "pending.txt")
LOG = os.path.join(HERE, "push.log")


def read_token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"[x] 未找到 {TOKEN_FILE}\n    请先创建该文件并写入百度推送 token（单行）")
    tok = open(TOKEN_FILE, encoding="utf-8-sig").read().strip()
    if not tok:
        sys.exit("[x] baidu_token.txt 为空")
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


def write_pending(urls):
    with open(PENDING, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(urls))
        if urls:
            f.write("\n")


def log(msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def push_one(token, url):
    ep = "http://data.zz.baidu.com/urls?" + urllib.parse.urlencode({"site": SITE, "token": token})
    req = urllib.request.Request(
        ep, data=url.encode(), headers={"Content-Type": "text/plain"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
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
        targets = pend + list(dict.fromkeys(rest))

    if not targets:
        log("[x] 没有可推送的 URL")
        return

    log(f"[i] 站点 {SITE} · 待推 {len(targets)} 条（pending {len(read_pending())} 条优先）")

    ok, over, other = [], [], []
    for u in targets:
        code, body = push_one(token, u)
        short = u.replace("https://www.lxshengda.com", "") or "/"
        try:
            data = json.loads(body)
            if code == 200 and "success" in data:
                log(f"  [OK] {short:28s} success={data['success']} remain={data.get('remain','?')}")
                ok.append(u)
            elif data.get("message") == "over quota":
                log(f"  [!!] {short:28s} over quota -> pending")
                over.append(u)
            else:
                log(f"  [xx] {short:28s} {code} {body[:100]}")
                other.append(u)
        except json.JSONDecodeError:
            log(f"  [xx] {short:28s} {code} {body[:100]}")
            other.append(u)
        time.sleep(0.4)

    write_pending(over + other)
    log(f"[i] 汇总：成功 {len(ok)} / 超额 {len(over)} / 其他失败 {len(other)}；pending 存 {len(over)+len(other)} 条")


if __name__ == "__main__":
    main()
