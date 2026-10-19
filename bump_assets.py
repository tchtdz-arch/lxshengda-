# -*- coding: utf-8 -*-
"""给全站 HTML 里的 style.css / main.js 引用加「内容哈希」版本号（cache busting）。

用法（在网站根目录）：
    python bump_assets.py

特性：
- 版本号 = 资源文件内容 md5 前 8 位，内容不变则版本号不变，变了自动跟着变
- 幂等：重复运行不会叠加出 ?v=a?v=b
- 二进制读写，不改变文件原有换行符
- 被 build_en.py / build_pages.py / build_insights.py 反代调用（bump()），
  保证重新生成英文站后版本号不会丢
"""
import hashlib
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCES = ("style.css", "main.js")
SKIP_DIRS = {".git", ".vercel", "node_modules", ".playwright-cli"}


def _digest(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def _html_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def bump(verbose=True):
    """返回 (扫描数, 改动数)。"""
    vers = {}
    for name in RESOURCES:
        p = os.path.join(ROOT, "assets", name)
        if os.path.exists(p):
            vers[name] = _digest(p)
            if verbose:
                print(f"  {name} -> v={vers[name]}")
    if not vers:
        print("  [bump] assets 下没有可处理的资源，跳过")
        return 0, 0

    pats = {
        name: re.compile(r"(assets/" + re.escape(name) + r")(\?v=[0-9a-fA-F]+)?")
        for name in vers
    }

    files = _html_files()
    changed = 0
    for fp in files:
        with open(fp, "rb") as f:
            raw = f.read()
        try:
            src = raw.decode("utf-8")
        except UnicodeDecodeError:
            print(f"  [bump] 跳过非 UTF-8 文件：{os.path.relpath(fp, ROOT)}")
            continue
        out = src
        for name, v in vers.items():
            out = pats[name].sub(lambda m, _v=v: f"{m.group(1)}?v={_v}", out)
        if out != src:
            with open(fp, "wb") as f:
                f.write(out.encode("utf-8"))
            changed += 1
            if verbose:
                print(f"  更新 {os.path.relpath(fp, ROOT)}")

    if verbose:
        print(f"  [bump] 扫描 {len(files)} 个 HTML，改动 {changed} 个")
    return len(files), changed


if __name__ == "__main__":
    print("== cache busting ==")
    bump()
