#!/usr/bin/env python3
"""讀 packs.json → 重建首頁 index.html。新增懶人包只要改 packs.json 再跑這支。"""
import json, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
packs = json.load(open(os.path.join(HERE, "packs.json"), encoding="utf-8"))

cards = "\n".join(
    f'''      <a class="card" href="./{p["slug"]}/">
        <div class="card-title">{html.escape(p["title"])}</div>
        <div class="card-sub">{html.escape(p["sub"])}</div>
        <div class="card-go">開啟懶人包 →</div>
      </a>''' for p in packs)

page = f'''<!DOCTYPE html>
<html lang="zh-Hant"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>韋總裁 ｜ 懶人包庫</title>
<meta name="description" content="韋總裁的財務懶人包總集，看完短影音想深入的內容都在這。">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@700;900&family=Noto+Sans+TC:wght@400;500;600&display=swap" rel="stylesheet">
<style>
 :root{{--navy:#0F172A;--navy2:#1E293B;--gold:#CA8A04;--gold-l:#FCD34D;--text:#E5E7EB;--mute:#94A3B8;--bd:rgba(202,138,4,.25)}}
 *{{box-sizing:border-box;margin:0;padding:0}}
 body{{background:radial-gradient(circle at top,#1E293B,#0F172A 70%);color:var(--text);font-family:"Noto Sans TC",sans-serif;min-height:100vh;padding:56px 18px 80px;line-height:1.7}}
 .wrap{{max-width:680px;margin:0 auto}}
 header{{text-align:center;margin-bottom:40px}}
 .badge{{display:inline-block;padding:4px 12px;background:rgba(202,138,4,.15);border:1px solid var(--bd);border-radius:999px;color:var(--gold-l);font-size:12px;margin-bottom:16px}}
 h1{{font-family:"Noto Serif TC",serif;font-size:clamp(28px,6vw,40px);color:var(--gold);letter-spacing:1px;margin-bottom:10px}}
 .sub{{color:var(--mute);font-size:15px;max-width:440px;margin:0 auto}}
 .grid{{display:flex;flex-direction:column;gap:14px;margin-top:8px}}
 .card{{display:block;text-decoration:none;background:rgba(30,41,59,.55);border:1px solid var(--bd);border-radius:16px;padding:22px 24px;transition:transform .15s,border-color .2s,background .2s}}
 .card:hover{{transform:translateY(-2px);border-color:var(--gold);background:rgba(30,41,59,.8)}}
 .card-title{{font-family:"Noto Serif TC",serif;font-weight:900;font-size:19px;color:#fff;margin-bottom:6px}}
 .card-sub{{color:var(--mute);font-size:14px;margin-bottom:12px}}
 .card-go{{color:var(--gold-l);font-size:13px;font-weight:600;letter-spacing:.04em}}
 footer{{text-align:center;margin-top:48px;color:var(--mute);font-size:12.5px;line-height:1.9}}
 footer a{{color:var(--gold-l);text-decoration:none}}
</style></head><body>
 <div class="wrap">
  <header>
   <span class="badge">韋總裁 ・ 做自己的富一代</span>
   <h1>懶人包庫</h1>
   <p class="sub">看完短影音還想深入的，都整理在這。挑一個有感的點進去。</p>
  </header>
  <div class="grid">
{cards}
  </div>
  <footer>
   韋總裁 ｜ 富邦人壽　·　<a href="https://instagram.com/changw_0331" target="_blank" rel="noopener">@changw_0331</a><br>
   以上為財務規劃觀念與框架，不是任何個股、ETF 或商品的買賣建議。
  </footer>
 </div>
</body></html>'''

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print(f"✓ 首頁已重建，共 {len(packs)} 篇")
