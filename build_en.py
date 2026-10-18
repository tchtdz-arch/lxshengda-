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
import os, re, io, glob, json
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


# JSON-LD 专用中英对照（页面 data-zh/data-en 覆盖不到的名称、地名等）
LD_MANUAL = {
    "郎溪胜达锻造有限公司": "Langxi Shengda Forging Co., Ltd.",
    "郎溪胜达锻造": "Langxi Shengda Forging",
    "郎溪胜达锻造 / 上海禹鸿": "Langxi Shengda Forging / Shanghai Yuhong",
    "上海禹鸿模具材料有限公司": "Shanghai Yuhong Die Material Co., Ltd.",
    "郎溪胜达锻造产品系列": "Langxi Shengda Forging Product Range",
    "经济开发区索埂路 10 号": "No. 10 Suogeng Road, Langxi Economic Development Zone",
    "宣城市郎溪县": "Langxi County, Xuancheng",
    "安徽省": "Anhui, China",
    "模具钢 / 工模具钢": "Die Steel / Tool & Die Steel",
    "锻件 / 飞轮储能转子": "Forgings / Flywheel Energy Storage Rotors",
    "模具钢 H13（宝钢）": "H13 Die Steel (Baosteel)",
    "H13 模具钢（宝钢）": "H13 Die Steel (Baosteel)",
    "油缸筒体（液压缸筒）": "Hydraulic Cylinder Barrels",
    "不锈钢锻件": "Stainless Steel Forgings",
    "各类锻件（定制）": "Custom Forgings",
    "热作模具锻件（热锻模 / 挤压模块 / 内衬 / 型材挤压模 / 挤压杆）":
        "Hot-Work Die Forgings (Hot Forging Dies / Extrusion Blocks / Liners / Profile Extrusion Dies / Extrusion Stems)",
    "石油锻件（转接头 / 方三通 / 方四通）":
        "Oil & Gas Forgings (Adapters / Square Tees / Square Crosses)",
    # 以下 6 条只存在于结构化数据中，页面正文无对应 data-en，需单独翻译
    "飞轮储能转子锻件、模具钢 H13、各类锻件专业厂家，锻造、热处理、精密加工一体化供应。":
        "Specialized manufacturer of flywheel energy storage rotor forgings, H13 die steel and various "
        "forgings, providing integrated forging, heat treatment and precision machining.",
    "大口径液压油缸筒体锻件，锻造成型 + 调质热处理，组织致密、壁厚均匀，配套化学成分、力学性能与 UT 探伤检测，可按图定制。":
        "Large-diameter hydraulic cylinder barrel forgings, forged and quench-and-tempered for dense "
        "structure and uniform wall thickness, supplied with chemical composition, mechanical property "
        "and UT inspection reports; custom-made to drawings.",
    "轴类、环形、饼类、模块等定制锻件，按客户图纸锻造、热处理与精加工，支持合金钢、不锈钢多牌号。":
        "Custom forgings including shafts, rings, discs and blocks, forged, heat-treated and precision "
        "machined to customer drawings, available in a wide range of alloy and stainless steel grades.",
    "宝钢 H13 热作模具钢（对应国标 4Cr5MoSiV1、日标 SKD61、德标 1.2344），供应退火态圆钢、锻件及热处理态产品，配套 NADCA #207 / SEP 1614 / VDG ASA 金相检验与 GB/T 228.1-2021 力学性能检测，UT 探伤、报告随货。":
        "Baosteel H13 hot-work die steel (4Cr5MoSiV1 in GB, SKD61 in JIS, 1.2344 in DIN), supplied as "
        "annealed round bars, forgings and heat-treated products, with metallographic examination to "
        "NADCA #207 / SEP 1614 / VDG ASA and mechanical testing to GB/T 228.1-2021, UT inspection and "
        "reports supplied with each shipment.",
    "4130（30CrMo）合金结构钢石油管汇锻件，主营转接头、方三通、方四通等高压承压锻件，锻造 + 调质热处理，配套化学成分、力学性能与 UT 探伤检测，可按图定制。":
        "4130 (30CrMo) alloy steel oil & gas manifold forgings, specializing in adapters, square tees and "
        "square crosses for high-pressure service, forged and quench-and-tempered, with chemical "
        "composition, mechanical property and UT inspection reports; custom-made to drawings.",
    "耐腐蚀高强度不锈钢锻件，覆盖 2Cr13 等马氏体及奥氏体不锈钢，按图定制锻造、热处理与精加工。":
        "Corrosion-resistant high-strength stainless steel forgings covering 2Cr13 and other martensitic "
        "and austenitic grades, custom forged, heat-treated and precision machined to drawings.",
}


ALT_MAP = {
    "郎溪胜达锻造": "Langxi Shengda Forging",
    "证书大图": "Certificate (full size)",
    "大图": "Full size image",
    "ISO 9001 证书": "ISO 9001 Certificate",
    "ISO 14001 证书": "ISO 14001 Certificate",
    "ISO 45001 证书": "ISO 45001 Certificate",
    "专精特新中小企业证书": "Specialized and Innovative SME Certificate",
    "高新技术企业证书": "High-Tech Enterprise Certificate",
    "宝武特冶授权证书": "Baowu Special Metallurgy authorized dealer certificate",
    "宝武特冶授权证明 - 上海禹鸿为宝武特种冶金有限公司圆棒协议用户":
        "Baowu Special Metallurgy authorization — Shanghai Yuhong is a contracted round bar user of Baowu Special Metallurgy Co., Ltd.",
    "宝武特冶授权证明 · 上海禹鸿为宝武特种冶金有限公司圆棒协议用户":
        "Baowu Special Metallurgy authorization — Shanghai Yuhong is a contracted round bar user of Baowu Special Metallurgy Co., Ltd.",
    "H13 及相关锻件产品图鉴": "H13 and related forging product gallery",
    "不锈钢锻件及多牌号锻件图鉴": "Stainless steel and multi-grade forging gallery",
    "公司部分产品图鉴：轧辊、H13 异形锻件、Cr12MoV 环形锻件、不锈钢锻件、筒形锻件、D2 锻件、刀体、三通、轴类、曲轴等":
        "Selected product gallery: rolls, H13 profile forgings, Cr12MoV ring forgings, stainless steel forgings, barrel forgings, D2 forgings, cutter bodies, tees, shafts, crankshafts, etc.",
    "各类锻件产品图鉴：轴类、环形、饼类、模块等":
        "Forging product gallery: shafts, rings, discs, blocks, etc.",
    "力学检测室": "Mechanical testing laboratory",
    "电子万能试验机": "Electronic universal testing machine",
    "电子万能试验机力学性能检测":
        "Mechanical property testing on electronic universal testing machine",
    "电子万能试验机拉伸试验 · H13 力学性能检测":
        "Tensile test on electronic universal testing machine — H13 mechanical properties",
    "金属摆锤冲击试验机": "Metal pendulum impact testing machine",
    "直读光谱仪": "Optical emission spectrometer",
    "直读光谱仪化学成分检测 · 宝钢 H13":
        "Chemical composition analysis by OES — Baosteel H13",
    "直读光谱仪成分检测": "Chemical composition analysis by OES",
    "疲劳测试报告 · 试样 10⁷ 周次通过": "Fatigue test report — specimen passed 10⁷ cycles",
    "疲劳试验报告 · 应力控制疲劳试验结果（GB/T 3075-2021）":
        "Fatigue test report — stress-controlled results (GB/T 3075-2021)",
    "大口径液压油缸筒体成品": "Large-diameter hydraulic cylinder barrel (finished)",
    "大口径液压油缸筒体锻件 - 锻造调质后粗加工态":
        "Large-diameter hydraulic cylinder barrel forging — rough machined after forging and Q&T",
    "挤压筒内衬锻件": "Extrusion container liner forging",
    "热作模具模块锻件": "Hot-work die block forging",
    "热作模具钢锻件 - 热锻模挤压模块坯料":
        "Hot-work die steel forging — blank for hot forging die / extrusion block",
    "石油管汇锻件 - 方三通方四通": "Oil & gas manifold forgings — square tees and crosses",
    "石油管汇锻件 - 方三通方四通方块锻件": "Oil & gas manifold forgings — square tee/cross blocks",
    "石油管汇锻件 - 转接头": "Oil & gas manifold forging — adapter",
    "石油管汇锻件 - 转接头锻件": "Oil & gas manifold forging — adapter forging",
    "精密加工锻件": "Precision machined forging",
    "锻件粗加工态": "Forging in rough machined condition",
    "飞轮储能转子体": "Flywheel energy storage rotor body",
    "飞轮储能转子整机 - 含阶梯轴": "Flywheel energy storage rotor assembly — with stepped shaft",
    "飞轮储能转子整机（含阶梯轴）": "Flywheel energy storage rotor assembly (with stepped shaft)",
}


def build(page):
    src = io.open(os.path.join(HERE, page), encoding="utf-8").read()
    soup = BeautifulSoup(src, "html.parser")

    # ---------- 0. 从 data-zh/data-en 配对建立「中→英」词典 ----------
    # 用于把 JSON-LD 里的中文文案自动换成页面上已有的英文，无需人工翻译
    zh2en = {}
    for el in soup.find_all(attrs={"data-zh": True}):
        zh, en = el.get("data-zh"), el.get("data-en")
        if not zh or not en:
            continue
        zh_txt = BeautifulSoup(zh, "html.parser").get_text(" ", strip=True)
        en_txt = BeautifulSoup(en, "html.parser").get_text(" ", strip=True)
        if zh_txt and en_txt and zh_txt != en_txt:
            zh2en[zh_txt] = en_txt

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

    # ---------- 11.8 图片 alt 英文化 ----------
    n_alt = 0
    for img in soup.find_all("img"):
        a = img.get("alt")
        if a and a.strip() in ALT_MAP:
            img["alt"] = ALT_MAP[a.strip()]
            n_alt += 1

    html = str(soup)

    # ---------- 11.6 海外习惯：英文站邮箱统一用 Gmail（送达率优于 163） ----------
    html = html.replace("tchtdz@163.com", "tchtdz@gmail.com")

    # ---------- 11.7 JSON-LD 英文化：用页面已有的 data-zh/data-en 配对自动翻译 ----------
    n_ld_fixed = [0]
    for s_ in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if not s_.string:
            continue
        try:
            data = json.loads(s_.string)
        except Exception:
            continue

        def walk(o):
            if isinstance(o, dict):
                return {k: walk(v) for k, v in o.items()}
            if isinstance(o, list):
                return [walk(v) for v in o]
            if isinstance(o, str):
                v = o.strip()
                if v in LD_MANUAL:
                    n_ld_fixed[0] += 1
                    return LD_MANUAL[v]
                if v in zh2en:
                    n_ld_fixed[0] += 1
                    return zh2en[v]
                # 长描述：与页面文案按前缀模糊匹配（JSON-LD 里常有截断或小改动）
                if len(v) >= 20 and re.search(r"[\u4e00-\u9fff]", v):
                    for k, val in zh2en.items():
                        if len(k) >= 20 and (k.startswith(v[:20]) or v.startswith(k[:20])):
                            n_ld_fixed[0] += 1
                            return val
                # 「中文 / English」双语写法 → 取英文半边
                m = re.match(r"^(.+?)\s*/\s*([A-Za-z0-9 ,.\-&()'/]+)$", v)
                if m and re.search(r"[\u4e00-\u9fff]", m.group(1)):
                    n_ld_fixed[0] += 1
                    return m.group(2)
                return o
            return o

        new_data = walk(data)
        s_.string = json.dumps(new_data, ensure_ascii=False, indent=2)

    html = str(soup)

    # ---------- 12. onclick 里的图片路径 ----------
    html = re.sub(r"openLightbox\('(?!\.\./|http)([^']+\.(?:webp|jpg|jpeg|png|gif))'",
                  r"openLightbox('../\1'", html)

    return html, dict(text=n_text, ph=n_ph, up=n_up, ld=n_ld, ldfix=n_ld_fixed[0])


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
        print(f"  {page:26s} 正文{st['text']:3d}  占位{st['ph']:2d}  路径{st['up']:3d}  LD{st['ld']} LD英化{st['ldfix']}")
    print(f"\n完成：{total} 个英文页 -> {EN_DIR}")


if __name__ == "__main__":
    main()
