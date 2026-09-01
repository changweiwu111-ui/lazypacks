#!/usr/bin/env python3
"""單位中性版生成器（2026-09-01 Iris 定稿規格）。

原版一字不動；輸出到 unit/<slug>/index.html。規則：
A 標題去「｜韋總裁」 B about 卡整移、章名「關 於 我」→「開 始 之 前」
C/D LINE・IG・forms.gle 按鈕與 cta-sign 署名移除 E footer 只刪 © 行
F 內文導流句換 Iris 三句標準句（表列逐句替換，不自由發揮）
頁面不標「單位版」，只加 <!-- unit-neutral --> 註解。
"""
import os, re, sys

L = os.path.dirname(os.path.abspath(__file__))
SLUGS = ("retire-300 cashflow-calc dividend-design first-invest principal-boost "
         "say-no-fund money-roles etf-nolook money-3stages money-mindset coach-guide "
         "money-at-work car-plan etf-fees money-mission gump-guide retire-cashflow "
         "money-guard family-order payday-order medical-reserve mortgage-order "
         "cashflow-gap retire-base money-roll").split()

S1 = "算出來的數字，直接回給傳這份給你的人，請他幫你看一眼。"
S2 = "想整個聊一次，就回頭找傳這份給你的人，跟他說「想聊聊」就好。"

# F：逐句替換表（key=檔內原句片段需唯一；value=標準句成品，保留原元素外殼）
SENT = {
  "cashflow-calc": [
    ("算出來的三個數字（目標／入場價／還差），<b>截圖傳到 LINE（@228ceqzw）給我</b>——我幫你看，照你的狀況，累積階段可以怎麼排。",
     "算出來的三個數字（目標／入場價／還差），直接回給傳這份給你的人，請他幫你看一眼，照你的狀況，累積階段可以怎麼排。"),
    ("如果你想要這種換法：到 LINE（@228ceqzw）打「<b>諮詢</b>」，我照你的金額算給你看，一個月差多少、怎麼換最順。先看數字再說。",
     "如果你想要這種換法：" + S2 + "照你的金額算一次，一個月差多少、怎麼換最順。先看數字再說。"),
    ("<h3>算完之後，<br>把你的三個數字傳給我。</h3>",
     "<h3>算完之後，<br>把你的三個數字傳回去。</h3>"),
    ("<p>試算器按出來的結果，<br>照這個格式傳到我的 LINE 就好：</p>",
     "<p>試算器按出來的結果，<br>照這個格式回給傳這份給你的人：</p>"),
    ("<p>換成你的數字，三十秒。<br>不管差多遠，傳過來我看一眼，<br>跟你聊聊累積階段可以怎麼排。</p>",
     "<p>換成你的數字，三十秒。<br>不管差多遠，請他幫你看一眼，<br>聊聊累積階段可以怎麼排。</p>"),
  ],
  "first-invest": [
    ("算出來的數字，<b>截圖傳到 LINE（@228ceqzw）給我</b>——我幫你看看這個金額對你的收支會不會太緊、跑不跑得完。",
     S1 + "這個金額對你的收支會不會太緊、跑不跑得完。"),
  ],
  "gump-guide": [
    ("把你的假設和數字傳給我——<b>LINE @228ceqzw 打「諮詢」</b>，我幫你把這三題一題一題過一遍。",
     "把你的假設和數字，回給傳這份給你的人，請他幫你把這三題一題一題過一遍。"),
  ],
  "cashflow-gap": [
    ("算出來的數字，<b>照下面的格式傳到 LINE（@228ceqzw）給我</b>——我幫你看這個差額，該用哪一層的錢去接。",
     "算出來的數字，照下面的格式回給傳這份給你的人，請他幫你看這個差額，該用哪一層的錢去接。"),
  ],
  "money-roles": [
    ("📱 算完了？把這個數字連同你的狀況，到 LINE 打「<b>諮詢</b>」＋你的數字傳給我，我幫你看看分工合不合理。",
     "📱 算完了？把這個數字連同你的狀況，回給傳這份給你的人，請他幫你看看分工合不合理。"),
    ("<p>想整個聊一次的話，打「<b>諮詢</b>」就好。</p>", "<p>" + S2 + "</p>"),
  ],
  "dividend-design": [
    ("——這就是我在諮詢裡做的事。", "——這部分，找傳這份給你的人一起挑就好。"),
    ("或在 LINE 直接回覆「諮詢」＋你的缺口數字。<br>先線上聊聊，不推銷、不施壓，<br>我幫你看你的固定層接不接得住。",
     "或把你的缺口數字，回給傳這份給你的人。<br>先線上聊聊，不推銷、不施壓，<br>請他看你的固定層接不接得住。"),
  ],
  "medical-reserve": [
    ("<span class=\"g\">直接在這個 LINE 對話傳給我</span>——我幫你算 65 歲那年的帳單長怎樣。",
     "<span class=\"g\">直接回給傳這份給你的人</span>——請他幫你算 65 歲那年的帳單長怎樣。"),
  ],
}

# 加回 gump/cashflow-calc 補充句（exact 對齊實檔）
SENT["gump-guide"] = [
  ("把你的假設和數字傳給我——<b>LINE @228ceqzw 打「諮詢」＋你的數字</b>——我幫你看這個假設站不站得住，",
   "把你的假設和數字，回給傳這份給你的人——請他幫你看這個假設站不站得住，"),
  ("把它傳給我，我幫你看兩件事：", "把它回給傳這份給你的人，請他幫你看兩件事："),
]
SENT["cashflow-calc"] += [
  ("想知道你的版本，把試算器的數字傳給我，我幫你看一次。",
   "想知道你的版本，把試算器的數字回給傳這份給你的人，請他幫你看一次。"),
  ("<p><b>韋總裁。</b>我幫靠時間和體力賺錢的人，把錢的順序排對，讓錢開始替你工作。從學生到六十幾歲的長輩都服務過。每個人的問題不一樣，我只找適合你的方法。</p>",
   ""),
]

# 全包通用替換（版型家族 A/B 的固定構件）
GENERIC = [
  (">韋總裁<span class=\"dot\"></span>", ">"),                                # hero-meta 前綴
  ("<span class=\"cite\">韋總裁 ・ ", "<span class=\"cite\">"),               # 引言署名
  ("已複製，回聊天室貼上、填好傳給我", "已複製，回聊天室貼上、填好傳回去"),      # 複製鈕文字
  ("數字傳給我。</h3>", "數字傳回去。</h3>"),                                  # CTA 標題
  ("<span class=\"kw\">回覆「諮詢」＋你的數字</span>", "<span class=\"kw\">把你的數字傳回去</span>"),
  ("<span class=\"kw\">回覆「諮詢」</span>", "<span class=\"kw\">說「想聊聊」就好</span>"),
  ("<p style=\"margin:16px 0 0\">我幫你", "<p style=\"margin:16px 0 0\">請傳這份給你的人幫你"),
  ("想整個聊一次的話，打「諮詢」就好。", S2),
  ("想整個聊一次的話，打「<strong>諮詢</strong>」就好。", S2),
  ("直接回在這個聊天室", "回給傳這份給你的人"),
  ("回在這個聊天室", "回給傳這份給你的人"),
  ("我對著你的", "請他對著你的"),
  ("。我陪你看的是", "。他會陪你看的是"),
  ("這題你也可以直接丟給我，我幫你看。", "這題你也可以直接丟給傳這份給你的人，請他幫你看。"),
  ("把數字傳過來，我幫你看一次。", "把數字回給傳這份給你的人，請他幫你看一次。"),
]
GENERIC_RE = [
  re.compile(r'<a class="cta-sign-link"[^>]*>.*?</a>\s*', re.S),
  re.compile(r'<div class="foot-handle">.*?</div>\s*', re.S),
  re.compile(r'<h2 class="h2">[^<]*我是誰[^<]*</h2>\s*'),
  re.compile(r'<p class="h2-sub">[^<]*為什麼是我[^<]*</p>\s*'),
]

BTN_PATTERNS = [
    re.compile(r'<a\b[^>]*href="https?://line\.me[^"]*"[^>]*>.*?</a>\s*', re.S),
    re.compile(r'<a\b[^>]*href="https?://(?:www\.)?instagram\.com[^"]*"[^>]*>.*?</a>\s*', re.S),
    re.compile(r'<a\b[^>]*href="https?://forms\.gle[^"]*"[^>]*>.*?</a>\s*', re.S),
    re.compile(r'<a\b[^>]*href="https?://hiwen\.pages\.dev[^"]*"[^>]*>.*?</a>\s*', re.S),
]

# 含巢狀 div 的區塊用深度走訪移除，不用 regex（cta-sign 裡有 cta-sign-name）
DIV_BLOCKS = ['<div class="cta-sign">']

def _remove_div_block(t, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', t[start:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            return t[:start] + t[start + m.end():]
    return t

def remove_about_card(t):
    """移除自介卡：家族 B 是含 class="about" 的 .card，家族 A 是 .about-card。"""
    ai = t.find('class="about"')  # 只配到 about（about-card/about-role 不算）
    while ai != -1 and t[ai + len('class="about'):ai + len('class="about') + 1] != '"':
        ai = t.find('class="about', ai + 1)
    if ai != -1:
        start = t.rfind('<div class="card">', 0, ai)
        if start != -1:
            t = _remove_div_block(t, start)
    start = t.find('<div class="about-card">')
    if start != -1:
        t = _remove_div_block(t, start)
    return t, True

def main():
    problems = []
    for s in SLUGS:
        src = os.path.join(L, s, "index.html")
        t = open(src, encoding="utf-8").read()

        t = t.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n<!-- unit-neutral -->", 1)
        t = re.sub(r'(<title>[^<]*?)\s*｜\s*韋總裁\s*(</title>)', r'\1\2', t)          # A
        t, _ = remove_about_card(t)                                                    # B
        t = t.replace("關 於 我", "開 始 之 前").replace(">關於我<", ">開始之前<")        # B
        for p in BTN_PATTERNS + GENERIC_RE:                                            # C/D
            t = p.sub("", t)
        for marker in DIV_BLOCKS:                                                      # C/D 巢狀區塊
            i = t.find(marker)
            while i != -1:
                t = _remove_div_block(t, i)
                i = t.find(marker)
        t = re.sub(r'(?:<br>\s*)?©\s*韋總裁[^<\n]*', '', t)                            # E
        for old, new in SENT.get(s, []):                                               # F 逐句（必須對上）
            if old not in t:
                problems.append(f"{s}: 替換句沒對上 -> {old[:40]}")
            t = t.replace(old, new)
        for old, new in GENERIC:                                                       # F 通用構件
            t = t.replace(old, new)

        out_dir = os.path.join(L, "unit", s)
        os.makedirs(out_dir, exist_ok=True)
        open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(t)

        leaks = []
        for pat in ["228ceqzw", "line.me", "forms.gle", "instagram.com", "ceo-wei",
                    "ceo.wei", "韋總裁", "吳昌韋", "做自己的富一代", "諮詢", "傳給我", "hiwen.pages"]:
            n = t.count(pat)
            if n:
                leaks.append(f"{pat}x{n}")
        print(f"{s:16s} {'; '.join(leaks) if leaks else 'CLEAN'}")
    for p in problems:
        print("⚠️", p, file=sys.stderr)

if __name__ == "__main__":
    main()
