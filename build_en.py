#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 /en/ 英文版站点

原理：把中文页里藏在 data-en 属性中的英文文案，直接渲染成可见正文。
这样即使不执行 JS，搜索引擎抓到的 DOM 也已经是英文（原站英文只在属性里，爬虫看不见）。

同时完成：
  - html lang -> en
  - 强制语言为 en（window.LX_FORCE_LANG）
  - hreflang 互指（zh-CN / en / x-default）
  - canonical / og:url 指向 /en/
  - og:locale -> en_US
  - 根级静态资源路径修正为 ../
  - 语言切换按钮改为「中文」链接（链回中文站）
"""
import os, re, io, glob
from bs4 import BeautifulSoup, NavigableString

HERE = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(HERE, "en")
SITE = "https://www.lxshengda.com"

# 需要跳过的非页面文件
SKIP = {"404.html", "baidu_verify_codeva-cIOc4y6zQh.html", "google7fb949e9a0e3fcea.html"}

# 需要加 ../ 前缀的根级资源
ASSET_EXT = (".webp", ".png", ".jpg", ".jpeg", ".gif", ".css", ".js", ".ico", ".svg", ".txt")


def is_page_link(v):
    """判断是否指向站内页面（保持原样，不加 ../）"""
    if not v:
        return False
    if v.startswith(("#", "http", "mailto:", "tel:", "//", "data:")):
        return False
    return v.endswith(".html") or v in ("/", "./")


def needs_up(v):
    """根级静态资源需要加 ../"""
    if not v or v.startswith(("#", "http", "mailto:", "tel:", "//", "data:")):
        return False
    if v.startswith("assets/"):
        return True
    return v.lower().endswith(ASSET_EXT)


def build(page):
    src = io.open(os.path.join(HERE, page), encoding="utf-8").read()
    soup = BeautifulSoup(src, "html.parser")

    # ---------- 1. html lang ----------
    if soup.html:
        soup.html["lang"] = "en"

    # ---------- 2. 正文替换：data-en -> 可见内容 ----------
    n_text = 0
    for el in soup.find_all(attrs={"data-zh": True}):
        en = el.get("data-en")
        if en is None:
            continue
        frag = BeautifulSoup(en, "html.parser")
        el.clear()
        for c in list(frag.contents):
            el.append(c.extract())
        n_text += 1

    # placeholder
    n_ph = 0
    for el in soup.find_all(attrs={"data-zh-ph": True}):
        en = el.get("data-en-ph")
        if en is not None:
            el["placeholder"] = en
            n_ph += 1

    # ---------- 3. title ----------
    t = soup.find("title")
    if t and t.get("data-en"):
        t.string = t["data-en"]

    # ---------- 4. meta description ----------
    d = soup.find("meta", attrs={"name": "description"})
    if d and d.get("data-en"):
        d["content"] = d["data-en"]

    # ---------- 5. og:locale 互换 ----------
    for m in soup.find_all("meta", attrs={"property": "og:locale"}):
        m["content"] = "en_US"
    for m in soup.find_all("meta", attrs={"property": "og:locale:alternate"}):
        m["content"] = "zh_CN"

    # ---------- 6. canonical / og:url ----------
    en_url = f"{SITE}/en/{page}"
    zh_url = f"{SITE}/{page}"
    c = soup.find("link", attrs={"rel": "canonical"})
    if c:
        c["href"] = en_url
    for m in soup.find_all("meta", attrs={"property": "og:url"}):
        m["content"] = en_url

    # ---------- 7. hreflang ----------
    head = soup.head
    # 先清除从中文页带来的 hreflang（否则会重复一套指向中文的标签）
    if head:
        for old in head.find_all("link", attrs={"hreflang": True}):
            old.decompose()
    if head:
        for rel in [("alternate", "zh-CN", zh_url), ("alternate", "en", en_url),
                    ("alternate", "x-default", zh_url)]:
            tag = soup.new_tag("link")
            tag["rel"] = rel[0]
            tag["hreflang"] = rel[1]
            tag["href"] = rel[2]
            head.append(tag)

    # ---------- 8. 资源路径上提一级 ----------
    n_up = 0
    for el in soup.find_all(["img", "script", "link", "source", "a"]):
        for attr in ("src", "href"):
            v = el.get(attr)
            if v and needs_up(v) and not is_page_link(v):
                el[attr] = "../" + v
                n_up += 1

    # ---------- 9. 语言切换按钮 -> 回中文站 ----------
    btn = soup.find(id="langToggle")
    if btn:
        a = soup.new_tag("a")
        a["class"] = btn.get("class", ["lang-switch"])
        a["id"] = "langToggle"
        a["href"] = "../index.html"
        a.string = "中文"
        btn.replace_with(a)

    # ---------- 10. JSON-LD 内的 URL 指向英文版 ----------
    n_ld = 0
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if s.string:
            new = s.string.replace(f'"{SITE}/"', f'"{SITE}/en/"')
            if new != s.string:
                s.string = new
                n_ld += 1

    # ---------- 10.5 页脚「English Version」改为回中文站 ----------
    for a in soup.find_all("a", href=re.compile(r"^en/")):
        a["href"] = "../" + a["href"][3:]
        a.string = "中文版"

    # ---------- 11. 强制英文（放在 main.js 之前） ----------
    mjs = soup.find("script", attrs={"src": re.compile(r"assets/main\.js$")})
    if mjs:
        force = soup.new_tag("script")
        force.string = "window.LX_FORCE_LANG='en';"
        mjs.insert_before(force)

    # ---------- 11.5 海外阅读习惯：电话加 +86 国际区号，地址补 China ----------
    # tel: 链接补国际区号
    for a in soup.find_all("a", href=re.compile(r"^tel:")):
        digits = re.sub(r"\D", "", a["href"])
        if len(digits) == 11 and digits.startswith("1") and not digits.startswith("86"):
            a["href"] = "tel:+86" + digits
    # 正文里的手机号补 +86
    PHONE = r"\b(1[3-9]\d \d{4} \d{4})\b"   # 1XX XXXX XXXX（前3位 + 后8位）
    for node in list(soup.find_all(string=re.compile(PHONE))):
        node.replace_with(re.sub(PHONE, r"+86 \1", str(node)))
    # 地址补国家
    for node in list(soup.find_all(string=re.compile(r"Xuancheng, Anhui"))):
        node.replace_with(str(node).replace("Xuancheng, Anhui", "Xuancheng, Anhui, China"))
    # 地址补国家（JSON-LD 内）
    for s_ in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if s_.string and "Xuancheng" in s_.string and "China" not in s_.string:
            s_.string = s_.string.replace('"安徽省"', '"Anhui, China"')

    html = str(soup)

    # ---------- 12. onclick 里的图片路径 ----------
    html = re.sub(r"openLightbox\('(?!\.\./|http)([^']+\.(?:webp|jpg|jpeg|png|gif))'",
                  r"openLightbox('../\1'", html)

    return html, dict(text=n_text, ph=n_ph, up=n_up, ld=n_ld)


def main():
    os.makedirs(EN_DIR, exist_ok=True)
    pages = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(HERE, "*.html")))
             if os.path.basename(p) not in SKIP]
    print(f"待生成 {len(pages)} 个英文页\n")
    total = 0
    for page in pages:
        html, st = build(page)
        out = os.path.join(EN_DIR, page)
        io.open(out, "w", encoding="utf-8", newline="").write(html)
        total += 1
        print(f"  {page:26s} 正文{st['text']:3d}  占位{st['ph']:2d}  路径{st['up']:3d}  LD{st['ld']}")
    print(f"\n完成：{total} 个英文页 -> {EN_DIR}")


if __name__ == "__main__":
    main()
