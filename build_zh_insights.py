#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成中文技术文章（insights/）

背景：中文站此前 0 篇技术内容，是 AI 搜索与百度长尾收录的最大缺口。
英文站已有 8 篇（build_insights.py），本脚本补齐中文侧。

产出：
  insights.html                 中文文章列表页
  insights/*.html               中文技术文章
并在 tech.html / products.html 注入「延伸阅读」内链区块。

用法：C:/Users/tcht/.workbuddy/binaries/python/envs/default/Scripts/python.exe build_zh_insights.py
"""
import os, io, re, json
from zh_articles import ARTICLES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "insights")
SITE = "https://www.lxshengda.com"
TODAY = "2026-11-05"
SITE_NAME = "郎溪胜达锻造有限公司"

KEYWORDS = {
    "h13-1-2344-skd61-difference":
        "H13,1.2344,SKD61,4Cr5MoSiV1,热作模具钢,模具钢牌号对照,H13成分,1.2344成分,"
        "H13和1.2344区别,模具钢选材,宝钢H13",
    "flywheel-rotor-forged-vs-cast":
        "飞轮储能转子,飞轮转子锻件,转子锻件,锻件和铸件区别,飞轮储能,"
        "转子锻造,高速转子,25Cr2Ni4MoV,飞轮转子材料",
    "forging-ratio-and-internal-quality":
        "锻造比,锻造比计算,锻件内部质量,锻造工艺,锻件疏松,锻造流线,"
        "锻件探伤,锻件晶粒度,锻造变形量",
    "ut-acceptance-criteria":
        "超声波探伤,UT探伤,锻件探伤标准,GB/T 6402,ASTM A388,EN 10228-3,"
        "探伤验收等级,无损检测,锻件检测",
}


def up(frag):
    """把根目录相对链接上提一级（供 insights/ 子目录使用）"""
    frag = frag.replace('href="./"', 'href="../"')
    frag = re.sub(r'src="\.\./(?!/)', 'src="../../', frag)
    frag = re.sub(r'href="(?!#|https?:|mailto:|tel:|\.\./)([^"]+)"', r'href="../\1"', frag)
    frag = re.sub(r'src="(?!#|https?:|\.\./)([^"]+)"', r'src="../\1"', frag)
    return frag


def load_shell(deeper=True):
    """从中文本地页 tech.html 提取 header / footer / lightbox / scripts"""
    src = io.open(os.path.join(HERE, "tech.html"), encoding="utf-8").read()
    header = re.search(r'<header class="site-header">.*?</header>', src, re.S).group(0)
    footer = re.search(r'<footer class="site-footer">.*?</footer>', src, re.S).group(0)
    tail = src[src.find("</footer>"):]
    lightbox = re.search(r'<!-- 证书灯箱 -->\s*(<div class="lightbox".*?</div>)', tail, re.S).group(1)
    scripts = re.search(r'<script src="assets/main\.js[^"]*"></script>.*?(?=</body>)', tail, re.S).group(0)

    if deeper:
        header, footer, lightbox = up(header), up(footer), up(lightbox)
        scripts = scripts.replace('src="assets/', 'src="../assets/')
    return header, footer, lightbox, scripts


def lang_link(header, href, label="EN"):
    """把 header 里的语言切换 button 换成跳转链接（避免中文文章页原地切换后正文不变）"""
    return re.sub(
        r'<button[^>]*id="langToggle"[^>]*>[^<]*</button>',
        f'<a class="lang-switch" href="{href}" id="langToggle">{label}</a>',
        header)


def faq_json(faqs):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": "zh-CN",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    }, ensure_ascii=False, indent=2)


def article_json(a):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": a["h1"],
        "description": a["desc"],
        "datePublished": TODAY,
        "dateModified": TODAY,
        "inLanguage": "zh-CN",
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME,
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/logo.png"}},
        "mainEntityOfPage": f"{SITE}/insights/{a['slug']}.html",
    }, ensure_ascii=False, indent=2)


def breadcrumb_json(a):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "技术文章", "item": f"{SITE}/insights.html"},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": f"{SITE}/insights/{a['slug']}.html"},
        ]
    }, ensure_ascii=False, indent=2)


def build_article(a, header, footer, lightbox, scripts):
    slug, url = a["slug"], f"{SITE}/insights/{a['slug']}.html"
    # 英文站对应文章 slug 与中文不同，切换链接与 hreflang 必须用映射后的英文 slug
    en_url = f"{SITE}/en/insights/{EN_SLUG[slug]}.html"
    faq_html = "".join(
        f'<div class="faq-item"><div class="q">{q}</div><div class="a-body"><p>{ans}</p></div></div>'
        for q, ans in a["faq"])
    h = lang_link(header, f"../../en/insights/{EN_SLUG[slug]}.html")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<link href="../../favicon.png" rel="icon" type="image/png"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{a['seo_title']}</title>
<meta content="{a['desc']}" name="description"/>
<meta content="{KEYWORDS[slug]}" name="keywords"/>
<meta content="index, follow" name="robots"/>
<meta content="{SITE_NAME}" name="author"/>
<link href="{url}" rel="canonical"/>
<meta content="pc,mobile" name="applicable-device"/>
<meta content="webkit" name="renderer"/>
<meta content="IE=edge" http-equiv="X-UA-Compatible"/>
<meta content="telephone=no" name="format-detection"/>
<link href="../../assets/style.css" rel="stylesheet"/>
<meta content="article" property="og:type"/>
<meta content="{SITE_NAME}" property="og:site_name"/>
<meta content="{a['seo_title']}" property="og:title"/>
<meta content="{a['desc']}" property="og:description"/>
<meta content="{url}" property="og:url"/>
<meta content="{SITE}/logo.png" property="og:image"/>
<meta content="zh_CN" property="og:locale"/>
<meta content="en_US" property="og:locale:alternate"/>
<link href="{url}" hreflang="zh-CN" rel="alternate"/>
<link href="{en_url}" hreflang="en" rel="alternate"/>
<link href="{en_url}" hreflang="x-default" rel="alternate"/>
<script type="application/ld+json">
{article_json(a)}
</script>
<script type="application/ld+json">
{breadcrumb_json(a)}
</script>
<script type="application/ld+json">
{faq_json(a['faq'])}
</script>
</head>
<body>
{h}
<section class="art-band">
<div class="container art-body">
<div class="art-meta"><a href="../insights.html">技术文章</a> · 技术说明 · {TODAY}</div>
<h1>{a['h1']}</h1>
<p class="art-lead">{a['lead']}</p>
{a['body']}
<h2>常见问题</h2>
<div class="faq-list">
{faq_html}
</div>
<div class="art-cta">
<h3>需要报价或文件核对？</h3>
<p>把图纸、材质牌号与检测要求发给我们，我们来确认可制造性、检验方案与交期。</p>
<p><a class="btn btn-primary" href="../contact.html">联系我们</a> <a class="btn btn-ghost" href="../products.html">查看产品</a></p>
</div>
</div>
</section>
{footer}
{lightbox}
<script>window.LX_FORCE_LANG='zh';</script>
{scripts}
</body>
</html>
"""


def hub_json():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "锻件技术文章",
        "description": "面向锻件采购与工艺工程师的技术说明：牌号对照、锻件与铸件对比、锻造比、超声波探伤验收标准。",
        "inLanguage": "zh-CN",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": a["title"],
             "url": f"{SITE}/insights/{a['slug']}.html"}
            for i, a in enumerate(ARTICLES)
        ],
    }, ensure_ascii=False, indent=2)


def build_hub(header, footer, lightbox, scripts):
    cards = ""
    for a in ARTICLES:
        cards += f"""<a class="ins-card" href="insights/{a['slug']}.html">
<h3>{a['title']}</h3>
<p>{a['desc']}</p>
<span>阅读全文 →</span>
</a>
"""
    h = lang_link(header, "en/insights.html")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<link href="favicon.png" rel="icon" type="image/png"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>技术文章 | 锻件选材、标准与检测知识 | 郎溪胜达锻造</title>
<meta content="面向锻件采购与工艺工程师的技术文章：H13 / 1.2344 / SKD61 牌号对照、飞轮储能转子锻件与铸件对比、锻造比与内部质量、锻件超声波探伤验收标准（GB/T 6402、ASTM A388、EN 10228-3）。" name="description"/>
<meta content="锻件技术文章,模具钢牌号对照,H13,1.2344,SKD61,飞轮转子锻件,锻造比,锻件超声波探伤,GB/T 6402,ASTM A388,EN 10228-3,锻件选材" name="keywords"/>
<meta content="index, follow" name="robots"/>
<meta content="{SITE_NAME}" name="author"/>
<link href="{SITE}/insights.html" rel="canonical"/>
<meta content="pc,mobile" name="applicable-device"/>
<meta content="webkit" name="renderer"/>
<meta content="IE=edge" http-equiv="X-UA-Compatible"/>
<meta content="telephone=no" name="format-detection"/>
<link href="assets/style.css" rel="stylesheet"/>
<meta content="website" property="og:type"/>
<meta content="{SITE_NAME}" property="og:site_name"/>
<meta content="技术文章 | 锻件选材、标准与检测知识" property="og:title"/>
<meta content="面向锻件采购与工艺工程师的技术文章：牌号对照、锻件与铸件对比、锻造比、探伤验收标准。" property="og:description"/>
<meta content="{SITE}/insights.html" property="og:url"/>
<meta content="{SITE}/logo.png" property="og:image"/>
<meta content="zh_CN" property="og:locale"/>
<link href="{SITE}/insights.html" hreflang="zh-CN" rel="alternate"/>
<link href="{SITE}/en/insights.html" hreflang="en" rel="alternate"/>
<link href="{SITE}/en/insights.html" hreflang="x-default" rel="alternate"/>
<script type="application/ld+json">
{hub_json()}
</script>
</head>
<body>
{h}
<section class="art-band">
<div class="container">
<div class="sec-head">
<div class="en">技术文章</div>
<h1>锻件选材、标准与检测技术说明</h1>
<p>把询价时最常被问到的问题写成短文：牌号到底能不能等效、锻件和铸件差在哪、锻造比怎么定、探伤要求怎么写才可考核。都是能直接用在图纸和采购单上的内容。</p>
</div>
<div class="ins-grid">
{cards}</div>
</div>
</section>
{footer}
{lightbox}
<script>window.LX_FORCE_LANG='zh';</script>
{scripts}
</body>
</html>
"""


# 中文 slug → 英文 slug（英文站对应文章，供 data-en-href 使用）
EN_SLUG = {
    "h13-1-2344-skd61-difference": "h13-vs-1-2344-vs-skd61",
    "flywheel-rotor-forged-vs-cast": "forged-vs-cast-flywheel-rotor",
    "forging-ratio-and-internal-quality": "forging-ratio-and-internal-quality",
    "ut-acceptance-criteria": "ut-acceptance-criteria-forgings",
}
EN_TITLE = {
    "h13-1-2344-skd61-difference": "H13 vs 1.2344 vs SKD61: One Steel, Three Names",
    "flywheel-rotor-forged-vs-cast": "Forged vs Cast Flywheel Rotor",
    "forging-ratio-and-internal-quality": "Forging Ratio and Internal Quality",
    "ut-acceptance-criteria": "UT Acceptance Criteria for Forgings",
}


def inject_further_reading():
    """在 tech.html / products.html 注入「延伸阅读」内链（幂等）

    区块带 data-zh / data-en 与 data-en-href：
    build_en.py 会据此生成英文版区块，链接指向英文站同名文章，避免中文 slug 在 /en/ 下变成死链。
    """
    items = ""
    for a in ARTICLES:
        zh_slug = a["slug"]
        items += (f'<li><a data-en="{EN_TITLE[zh_slug]}" data-en-href="insights/{EN_SLUG[zh_slug]}.html" '
                  f'data-zh="{a["title"]}" href="insights/{zh_slug}.html">{a["title"]}</a></li>\n')
    items += ('<li><a data-en="All technical notes →" data-en-href="insights.html" '
              'data-zh="查看全部技术文章 →" href="insights.html">查看全部技术文章 →</a></li>\n')
    block = f"""<section class="fr-band"><div class="container">
<div class="further-reading">
<h3 data-en="Further reading" data-zh="延伸阅读">延伸阅读</h3>
<ul>
{items}</ul>
</div>
</div></section>
"""
    for page in ("tech.html", "products.html"):
        p = os.path.join(HERE, page)
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        # 幂等：先清掉旧区块（新版包在 section 里，兼容清理旧版裸 div）
        if "fr-band" in s:
            s = re.sub(r'<section class="fr-band">.*?</section>\s*', "", s, flags=re.S)
        if "further-reading" in s:
            s = re.sub(r'<div class="further-reading">.*?</div>\s*', "", s, flags=re.S)
        if '<footer class="site-footer">' in s:
            s = s.replace('<footer class="site-footer">', block + '<footer class="site-footer">', 1)
            io.open(p, "w", encoding="utf-8", newline="").write(s)
            print(f"  注入延伸阅读: {page}")


def update_sitemap():
    p = os.path.join(HERE, "sitemap.xml")
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r"\s*<url>\s*<loc>[^<]*/insights[^<]*</loc>.*?</url>", "", s, flags=re.S)
    entries = [f"{SITE}/insights.html"] + [f"{SITE}/insights/{a['slug']}.html" for a in ARTICLES]
    add = ""
    for loc in entries:
        add += f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n"
    s = s.replace("</urlset>", add + "</urlset>")
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print(f"  sitemap.xml 更新: +{len(entries)} 条")


def main():
    os.makedirs(OUT, exist_ok=True)
    h, f, lb, sc = load_shell(deeper=True)
    for a in ARTICLES:
        html = build_article(a, h, f, lb, sc)
        io.open(os.path.join(OUT, a["slug"] + ".html"), "w", encoding="utf-8", newline="").write(html)
        print(f"  文章: insights/{a['slug']}.html  ({len(html)} 字节)")
    h2, f2, lb2, sc2 = load_shell(deeper=False)
    hub = build_hub(h2, f2, lb2, sc2)
    io.open(os.path.join(HERE, "insights.html"), "w", encoding="utf-8", newline="").write(hub)
    print(f"  列表页: insights.html ({len(hub)} 字节)")
    inject_further_reading()
    update_sitemap()
    try:
        import bump_assets
        bump_assets.bump(verbose=False)
        print("  资源版本号: 已刷新")
    except Exception as e:
        print(f"[!] 版本号刷新跳过：{e}")


if __name__ == "__main__":
    main()
