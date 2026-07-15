#!/usr/bin/env python3
"""VibeNav 构建脚本: data/links.yaml -> dist/index.html (Craigslist 极简风)。
特性: 中/英/日切换 · 底部 TAG 标签筛选 · 字号小中大 · 搜索
用法: python scripts/build.py   依赖: pip install pyyaml
"""
import html
import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["zh", "en", "ja"]

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VibeNav — Vibe Coding 工具导航</title>
<meta name="description" content="Vibe Coding 工具导航(中/EN/日):AI 编程 IDE、命令行 Agent、应用生成器、MCP、提示词、发布增长等 __COUNT__ 个精选工具,极简纯链接。">
<style>
:root{--fs:14px}
html.fs-s{--fs:12.5px}html.fs-l{--fs:16.5px}
body{font-family:"Helvetica Neue",Helvetica,Arial,"PingFang SC","Hiragino Sans","Microsoft YaHei",sans-serif;font-size:var(--fs);background:#fff;color:#222;margin:0;padding:0 12px 40px}
a{color:#00e;text-decoration:none}
a:visited{color:#551a8b}
a:hover{text-decoration:underline}
.top{max-width:1100px;margin:14px auto 6px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.top h1{font-size:1.45em;margin:0;color:#551a8b}
.top .tag{color:#666;font-size:.86em}
.top .spacer{flex:1}
.top input{border:1px solid #999;padding:3px 8px;font-size:.93em;width:170px}
.ctl{display:flex;gap:2px;align-items:center}
.ctl button{border:1px solid #ccc;background:#fff;color:#551a8b;font-size:.8em;padding:2px 7px;cursor:pointer}
.ctl button.on{background:#551a8b;color:#fff;border-color:#551a8b}
.ctl .sep{color:#ccc;margin:0 6px}
.meta{max-width:1100px;margin:0 auto 14px;color:#888;font-size:.8em;border-bottom:1px solid #ddd;padding-bottom:8px}
.cols{max-width:1100px;margin:0 auto;column-width:250px;column-gap:28px}
.cat{break-inside:avoid;margin-bottom:18px}
.cat h2{font-size:1em;margin:0 0 4px;color:#222}
.cat ul{list-style:none;margin:0;padding:0}
.cat li{line-height:1.75}
.hide{display:none}
.tagbox{max-width:1100px;margin:26px auto 0;border-top:1px solid #ddd;padding-top:10px}
.tagbox b{font-size:.93em}
.tagbox .chips{margin-top:6px;line-height:2.1}
.chip{border:1px solid #ccc;border-radius:3px;padding:1px 7px;margin-right:6px;font-size:.86em;color:#551a8b;cursor:pointer;white-space:nowrap;display:inline-block}
.chip .n{color:#999;font-size:.85em}
.chip.on{background:#551a8b;color:#fff;border-color:#551a8b}
.chip.on .n{color:#ddd}
footer{max-width:1100px;margin:20px auto 0;border-top:1px solid #ddd;padding-top:10px;color:#888;font-size:.8em}
footer a{color:#551a8b}
</style>
</head>
<body>
<div class="top">
  <h1>VibeNav</h1><span class="tag"><span id="tagline"></span> · <span id="count"></span></span>
  <span class="spacer"></span>
  <input id="q" type="search" placeholder="搜索…">
  <span class="ctl">
    <button data-lang="zh">中</button><button data-lang="en">EN</button><button data-lang="ja">日</button>
    <span class="sep">|</span>
    <button data-fs="s" id="fss"></button><button data-fs="m" id="fsm"></button><button data-fs="l" id="fsl"></button>
  </span>
</div>
<div class="meta"><span id="meta"></span> · <span id="updated"></span> __DATE__</div>
<div class="cols" id="cols">
__CONTENT__
</div>
<div class="tagbox"><b id="tagstitle"></b><div class="chips" id="chips">__TAGS__</div></div>
<footer>
<span id="f1"></span> <a href="__FFD__" id="f1link"></a><br>
<a href="__REPO__">GitHub</a> · MIT · <span id="f2"></span> <code>data/links.yaml</code>
</footer>
<script>
const I18N=__I18N__;
const TAGL=__TAGL__;
const HTML_LANG={zh:"zh-CN",en:"en",ja:"ja"};
let lang=localStorage.getItem("vn-lang")||(navigator.language||"zh").slice(0,2);
if(!I18N[lang])lang="zh";
let fs=localStorage.getItem("vn-fs")||"m";
let activeTag="",query="";
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];

function applyFs(){
  document.documentElement.classList.remove("fs-s","fs-l");
  if(fs!=="m")document.documentElement.classList.add("fs-"+fs);
  $$(".ctl button[data-fs]").forEach(b=>b.classList.toggle("on",b.dataset.fs===fs));
  localStorage.setItem("vn-fs",fs);
}
function applyLang(){
  const t=I18N[lang];
  document.documentElement.lang=HTML_LANG[lang];
  $("#tagline").textContent=t.tagline;
  $("#meta").textContent=t.meta;$("#updated").textContent=t.updated;
  $("#q").placeholder=t.search;
  $("#tagstitle").textContent=t.tags_title;
  $("#f1").textContent=t.footer1;$("#f1link").textContent=t.footer1_link;
  $("#f2").textContent=t.footer2;
  $("#fss").textContent=t.font_s;$("#fsm").textContent=t.font_m;$("#fsl").textContent=t.font_l;
  $$(".cat h2").forEach(h=>h.textContent=h.dataset[lang]);
  $$(".cat li a").forEach(a=>a.title=a.dataset[lang]);
  $$("#chips .chip").forEach(c=>{c.firstChild.textContent=TAGL[c.dataset.tag][lang]+" ";});
  $$(".ctl button[data-lang]").forEach(b=>b.classList.toggle("on",b.dataset.lang===lang));
  document.title="VibeNav — "+t.tagline;
  localStorage.setItem("vn-lang",lang);
  render();
}
function render(){
  let shown=0;
  $$(".cat").forEach(cat=>{
    let n=0;
    cat.querySelectorAll("li").forEach(li=>{
      const a=li.querySelector("a");
      const hay=(a.textContent+" "+(a.dataset[lang]||"")+" "+li.dataset.tags).toLowerCase();
      const hit=(!query||hay.includes(query))&&(!activeTag||li.dataset.tags.split(",").includes(activeTag));
      li.classList.toggle("hide",!hit);if(hit)n++;
    });
    cat.classList.toggle("hide",n===0);shown+=n;
  });
  const t=I18N[lang];
  $("#count").textContent=(t.total?t.total+" ":"")+shown+" "+t.tools;
}
$("#q").addEventListener("input",e=>{query=e.target.value.trim().toLowerCase();render();});
$$(".ctl button[data-lang]").forEach(b=>b.addEventListener("click",()=>{lang=b.dataset.lang;applyLang();}));
$$(".ctl button[data-fs]").forEach(b=>b.addEventListener("click",()=>{fs=b.dataset.fs;applyFs();}));
document.getElementById("chips").addEventListener("click",e=>{
  const c=e.target.closest(".chip");if(!c)return;
  activeTag=activeTag===c.dataset.tag?"":c.dataset.tag;
  $$("#chips .chip").forEach(x=>x.classList.toggle("on",x.dataset.tag===activeTag));
  render();
});
applyFs();applyLang();
</script>
</body>
</html>
"""


def split3(s, what):
    parts = [p.strip() for p in s.split("|")]
    if len(parts) != 3:
        sys.exit(f"❌ {what} 应为三段(中|英|日): {s}")
    return parts


def main():
    data = yaml.safe_load((ROOT / "data" / "links.yaml").read_text(encoding="utf-8"))
    tagl = {k: dict(zip(LANGS, split3(v, f"标签 {k}"))) for k, v in data["tags"].items()}

    blocks, count, tag_count = [], 0, {k: 0 for k in tagl}
    for cat in data["categories"]:
        names = split3(cat["name"], "分类名")
        items = []
        for raw in cat["links"]:
            parts = [p.strip() for p in raw.split("|")]
            if len(parts) != 6:
                sys.exit(f"❌ 链接应为 6 段(名称|网址|标签|中|英|日): {raw}")
            name, url, tags, zh, en, ja = parts
            taglist = [t.strip() for t in tags.split(",")]
            for t in taglist:
                if t not in tagl:
                    sys.exit(f"❌ 未定义的标签 {t}: {raw}")
                tag_count[t] += 1
            items.append(
                f'<li data-tags="{",".join(taglist)}">'
                f'<a href="{html.escape(url)}" title="{html.escape(zh)}" '
                f'data-zh="{html.escape(zh)}" data-en="{html.escape(en)}" data-ja="{html.escape(ja)}" '
                f'target="_blank" rel="noopener">{html.escape(name)}</a></li>'
            )
            count += 1
        blocks.append(
            f'<div class="cat"><h2 data-zh="{html.escape(names[0])}" '
            f'data-en="{html.escape(names[1])}" data-ja="{html.escape(names[2])}">'
            f'{html.escape(names[0])}</h2><ul>{"".join(items)}</ul></div>'
        )

    chips = "".join(
        f'<span class="chip" data-tag="{k}"><span>{html.escape(v["zh"])} </span>'
        f'<span class="n">({tag_count[k]})</span></span>'
        for k, v in tagl.items() if tag_count[k]
    )

    out = (
        TPL.replace("__COUNT__", str(count))
        .replace("__DATE__", date.today().isoformat())
        .replace("__CONTENT__", "\n".join(blocks))
        .replace("__TAGS__", chips)
        .replace("__FFD__", data["freefordev"])
        .replace("__REPO__", data["repo"])
        .replace("__I18N__", json.dumps(data["i18n"], ensure_ascii=False))
        .replace("__TAGL__", json.dumps(tagl, ensure_ascii=False))
    )
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    (dist / "index.html").write_text(out, encoding="utf-8")
    print(f"✅ 构建完成: {len(data['categories'])} 分类 / {count} 链接 / {sum(1 for k in tag_count if tag_count[k])} 标签 -> dist/index.html")


if __name__ == "__main__":
    main()
