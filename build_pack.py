# -*- coding: utf-8 -*-
"""用 etf-nolook 母版套出新懶人包。用法：python3 build_pack.py spec.json out.html"""
import json, re, sys, html as H

MASTER = "/Users/changweiwu/Downloads/_網站與部署專案/lazypacks/etf-nolook/index.html"
src = open(MASTER, encoding="utf-8").read()
HEAD = src[:src.index("<body")]           # doctype + head + css
BODY_OPEN = re.search(r'(<body[^>]*>)', src).group(1)
TAIL = src[src.index("</body>"):]

def bold(t):
    """把【…】轉成 <strong>，並跳脫其餘 HTML"""
    parts = re.split(r'【(.+?)】', t)
    out = ""
    for i, p in enumerate(parts):
        out += (f"<strong>{H.escape(p)}</strong>" if i % 2 else H.escape(p))
    return out

def gold(t, cls="num"):
    """把【…】轉成金色 span（給 h1 / cta-h2 / pull 用）"""
    parts = re.split(r'【(.+?)】', t)
    out = ""
    for i, p in enumerate(parts):
        out += (f'<span class="{cls}">{H.escape(p)}</span>' if i % 2 else H.escape(p))
    return out

def build(s):
    P = []
    A = P.append
    A('<main class="wrap">\n')
    # hero
    A(f'''  <header class="hero">
    <div class="hero-meta">{H.escape(s["meta"])}<span class="dot"></span>閱讀時間 3 分鐘</div>
    <h1>{gold(s["h1"])}</h1>
    <p class="hero-sub">{bold(s["lead"])}</p>
    <div class="hero-rule"></div>
  </header>\n\n''')
    # about
    prev = "\n".join(f'        <li><span class="num">{n:02d}</span><span>{H.escape(t)}</span></li>'
                     for n, t in enumerate(s["preview"], 1))
    A(f'''  <section>
    <div class="chapter-mark">
      <span class="chapter-no">00</span>
      <span class="chapter-label">關於我</span>
    </div>
    <h2 class="h2">在你往下讀之前，先讓你知道我是誰</h2>
    <p class="h2-sub">{H.escape(s["about_sub"])}</p>

    <div class="about-card">
      <div class="about-avatar"></div>
      <div class="about-name">韋 總 裁</div>
      <div class="about-role">吳 昌 韋 ・ @ceo.wei</div>
      <div class="about-rule"></div>
      <p class="about-bio">我幫 22-45 歲的上班族看資產配置，工程師、護理師、老師、律師都有，<strong>一份一份看過</strong>。</p>
      <p class="about-bio">{bold(s["about_2nd"])}</p>
      <div class="about-tag">做 自 己 的 富 一 代</div>
    </div>

    <div class="preview">
      <div class="preview-head">你會讀到</div>
      <ul>
{prev}
      </ul>
    </div>
  </section>\n\n''')
    # sections
    for i, sec in enumerate(s["sections"], 1):
        steps = ""
        for j, st in enumerate(sec["steps"], 1):
            num = st.get("num") or f"{j:02d}"
            steps += f'''      <div class="step">
        <div class="step-num">{H.escape(num)}</div>
        <div class="step-body">
          <h4>{H.escape(st["h4"])}</h4>
          <p>{bold(st["body"])}</p>
        </div>
      </div>\n'''
        extra = ""
        if sec.get("pull"):
            extra += f'''
    <div class="pull-soft" style="margin-top:24px">
      <div class="ln">{gold(sec["pull"], "g")}</div>
      <span class="cite">{H.escape(sec["pull_cite"])}</span>
    </div>\n'''
        if sec.get("myths"):
            ms = "\n".join(f'        <p>{bold(m)}</p>' for m in sec["myths"])
            extra += f'''
    <div class="layer" style="margin-top:18px">
      <div class="layer-note">
        <div class="lbl">兩個常見誤會</div>
{ms}
      </div>
    </div>\n'''
        if sec.get("bridge"):
            extra += f'''
    <div class="bridge">
      <p>{bold(sec["bridge"])}</p>
    </div>\n'''
        A(f'''  <section>
    <div class="chapter-mark">
      <span class="chapter-no">{i:02d}</span>
      <span class="chapter-label">{H.escape(sec["label"])}</span>
    </div>
    <h2 class="h2">{H.escape(sec["h2"])}</h2>
    <p class="h2-sub">{H.escape(sec["kicker"])}</p>

    <div class="steps-card">
{steps}    </div>
{extra}  </section>\n\n''')
    # CTA
    ask = s["cta_ask"]
    A(f'''  <div class="cta-card">
    <h2 class="cta-h2">想知道自己<span class="g">{H.escape(ask)}</span></h2>
    <div class="cta-rule"></div>

    <p class="cta-body">{bold(s["cta_lead"])}</p>
    <p class="cta-body">看完，直接在這個聊天室回我一句「<strong>想知道{H.escape(ask)}</strong>」，IG 私訊我也可以。{bold(s["cta_hint"])}</p>
    <p class="cta-body">想整個攤開看一次，打「<strong>諮詢</strong>」就好。一對一，把收支、預備金、這筆錢的用途一起看。第一次只聊你的狀況，要不要繼續，你自己決定。</p>
    <p class="cta-body" style="font-size:13px;opacity:.75">{s["compliance"]}</p>

    <div class="cta-meta">
      <div>
        <div class="n">30 分鐘</div>
        <div class="l">面談時長</div>
      </div>
      <div>
        <div class="n">免費</div>
        <div class="l">首次諮詢</div>
      </div>
      <div>
        <div class="n">1 對 1</div>
        <div class="l">線上 / 實體</div>
      </div>
    </div>

    <div class="cta-actions">
      <a class="cta-btn cta-btn-primary" href="https://forms.gle/44gpc9N1KWcB7RWy6" target="_blank">填表預約諮詢</a>
    </div>

    <div class="cta-sign">
      <div class="cta-sign-name">韋 總 裁</div>
      <a class="cta-sign-link" href="https://ceo-wei.pages.dev" target="_blank">ceo-wei.pages.dev</a>
    </div>
  </div>

  <footer>
    <div class="foot-handle">@ ceo.<span class="g">wei</span></div>
    <div class="foot-disclaim">{s["disclaimer"]}</div>
  </footer>

</main>
''')
    return "".join(P)

spec = json.load(open(sys.argv[1], encoding="utf-8"))
head = HEAD
head = re.sub(r'<title>.*?</title>', f'<title>{H.escape(spec["title"])}</title>', head, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*(")',
              lambda m: m.group(1)+H.escape(spec["sub"])+m.group(2), head)
open(sys.argv[2], "w", encoding="utf-8").write(head + BODY_OPEN + "\n" + build(spec) + TAIL)
print(f'✅ {sys.argv[2]}  ({len(open(sys.argv[2],encoding="utf-8").read())//1024} KB)')
