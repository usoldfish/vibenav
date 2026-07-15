#!/usr/bin/env python3
"""VibeNav 构建脚本: data/links.yaml -> dist/index.html (Craigslist 极简风)。
用法: python scripts/build.py   依赖: pip install pyyaml
"""
import html
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__SITE__ — __TAGLINE__</title>
<meta name="description" content="__TAGLINE__:AI 编程 IDE、命令行 Agent、应用生成器、MCP、提示词、发布增长等 __COUNT__ 个精选工具,极简纯链接导航。">
<style>
body{font-family:"Helvetica Neue",Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;font-size:14px;background:#fff;color:#222;margin:0;padding:0 12px 40px}
a{color:#00e;text-decoration:none}
a:visited{color:#551a8b}
a:hover{text-decoration:underline}
.top{max-width:1100px;margin:14px auto 6px;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.top h1{font-size:20px;margin:0;color:#551a8b}
.top .tag{color:#666;font-size:12px}
.top .spacer{flex:1}
.top input{border:1px solid #999;padding:3px 8px;font-size:13px;width:200px}
.meta{max-width:1100px;margin:0 auto 14px;color:#888;font-size:11px;border-bottom:1px solid #ddd;padding-bottom:8px}
.cols{max-width:1100px;margin:0 auto;column-width:250px;column-gap:28px}
.cat{break-inside:avoid;margin-bottom:18px}
.cat h2{font-size:14px;margin:0 0 4px;color:#222}
.cat ul{list-style:none;margin:0;padding:0}
.cat li{line-height:1.75}
.hide{display:none}
footer{max-width:1100px;margin:26px auto 0;border-top:1px solid #ddd;padding-top:10px;color:#888;font-size:11px}
footer a{color:#551a8b}
</style>
</head>
<body>
<div class="top">
  <h1>__SITE__</h1><span class="tag">__TAGLINE__ · 共 __COUNT__ 个工具</span>
  <span class="spacer"></span>
  <input id="q" type="search" placeholder="搜索…">
</div>
<div class="meta">纯链接 · 鼠标悬停看说明 · 更新于 __DATE__</div>
<div class="cols" id="cols">
__CONTENT__
</div>
<footer>
🆓 托管 / 数据库 / 支付 / 邮件等免费基础设施 → <a href="__FFD__">FreeDev 中文版(130 个免费服务)</a><br>
<a href="__REPO__">GitHub</a> · MIT · 数据人工精选,提 PR 改 <code>data/links.yaml</code> 即可
</footer>
<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{
  const v=q.value.trim().toLowerCase();
  document.querySelectorAll('.cat').forEach(cat=>{
    let n=0;
    cat.querySelectorAll('li').forEach(li=>{
      const hit=!v||li.textContent.toLowerCase().includes(v)||(li.querySelector('a').title||'').toLowerCase().includes(v);
      li.classList.toggle('hide',!hit);if(hit)n++;
    });
    cat.classList.toggle('hide',n===0);
  });
});
</script>
</body>
</html>
"""


def main():
    data = yaml.safe_load((ROOT / "data" / "links.yaml").read_text(encoding="utf-8"))
    blocks, count = [], 0
    for cat in data["categories"]:
        items = []
        for raw in cat["links"]:
            parts = [p.strip() for p in raw.split("|")]
            if len(parts) != 3:
                sys.exit(f"❌ 格式错误(应为 名称 | 网址 | 提示): {raw}")
            name, url, tip = parts
            items.append(
                f'<li><a href="{html.escape(url)}" title="{html.escape(tip)}" '
                f'target="_blank" rel="noopener">{html.escape(name)}</a></li>'
            )
            count += 1
        blocks.append(
            f'<div class="cat"><h2>{html.escape(cat["name"])}</h2>'
            f'<ul>{"".join(items)}</ul></div>'
        )
    out = (
        TPL.replace("__SITE__", data["site"])
        .replace("__TAGLINE__", data["tagline"])
        .replace("__COUNT__", str(count))
        .replace("__DATE__", date.today().isoformat())
        .replace("__CONTENT__", "\n".join(blocks))
        .replace("__FFD__", data["freefordev"])
        .replace("__REPO__", data["repo"])
    )
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "index.html").write_text(out, encoding="utf-8")
    print(f"✅ 构建完成: {len(data['categories'])} 个分类 / {count} 个链接 -> dist/index.html")


if __name__ == "__main__":
    main()
