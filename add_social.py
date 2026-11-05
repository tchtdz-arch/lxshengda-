# -*- coding: utf-8 -*-
"""在全部页面页脚插入 Facebook / LinkedIn 社交图标（幂等）。
插入位置：页脚「网站地图」行之前（电话/邮箱行之后）。
"""
import os, re, glob, sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

FB = "https://www.facebook.com/profile.php?id=61596347517612"
LI = "https://www.linkedin.com/in/%E6%96%8C-%E5%90%B4-307315445/"

SVG_FB = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5.02 '
          '3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26'
          'c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.45 2.91h-2.33V22c4.78-.76 8.44-4.92 8.44-9.94z"/></svg>')

SVG_LI = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04'
          '-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46'
          'v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.14 2.07 2.07 0 0 1 0 4.14zM7.12 20.45H3.55V9h3.57v11.45z"/></svg>')

BLOCK = ('<div class="f-line f-social">'
         f'<a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook">{SVG_FB}</a>'
         f'<a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn">{SVG_LI}</a>'
         '</div>')

# 插入锚点：页脚里的「网站地图」行
ANCHOR = re.compile(r'(<div class="f-line"><a data-en="Sitemap")')

files = []
for pat in ('*.html', 'en/*.html', 'en/insights/*.html', 'insights/*.html', 'en/products/*.html', 'products/*.html'):
    files += glob.glob(pat)

changed = skipped = nofooter = 0
for f in sorted(set(files)):
    s = open(f, encoding='utf-8').read()
    if 'site-footer' not in s:
        nofooter += 1
        continue
    if 'f-line f-social' in s:
        skipped += 1
        continue
    m = ANCHOR.search(s)
    if not m:
        print('  [WARN] 无锚点:', f)
        continue
    s2 = s[:m.start()] + BLOCK + '\n' + s[m.start():]
    open(f, 'w', encoding='utf-8', newline='').write(s2)
    changed += 1

print(f'完成：修改 {changed} 页，已存在跳过 {skipped} 页，无页脚 {nofooter} 页')
