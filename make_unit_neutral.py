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
SLUGS = ("allocation-tool retire-300 cashflow-calc dividend-design first-invest principal-boost "
         "say-no-fund money-roles etf-nolook money-3stages money-mindset coach-guide "
         "money-at-work car-plan etf-fees money-mission gump-guide retire-cashflow "
         "money-guard family-order payday-order medical-reserve mortgage-order "
         "cashflow-gap retire-base money-roll tax-check-3 dividend-check-3 first-million "
         # 2026-10-09 新增 11 份（新三段式／equity-loan 母版／v2 數字卡版）
         "invest-start afford-sustain tech-pairing retire-backward salary-split5 equity-loan "
         "house-cash maturity-money credit-line deposit-optimize dividend-3flaws "
         # 2026-10-15 新增 2 份（30萬配方／ETF 底牌，KH681 影片文案用）
         "thirty-recipe etf-roles "
         # 2026-10-29 新增 3 份（出國／J卡／領錢，KH681 影片文案用；J卡推薦碼走 ?ref=）
         "travel-fund jcard-guide monthly-20k").split()

S1 = "算出來的數字，直接回給傳這份給你的人，請他幫你看一眼。"
S2 = "想整個聊一次，就回頭找傳這份給你的人，跟他說「想聊聊」就好。"

# F：逐句替換表（key=檔內原句片段需唯一；value=標準句成品，保留原元素外殼）
SENT = {
  "first-million": [
    ("看完，直接在這個聊天室回我一句「<strong>想知道適不適合</strong>」，IG 私訊我也可以。回的時候順便跟我說：",
     "看完，直接回給傳這份給你的人一句「<strong>想知道適不適合</strong>」。回的時候順便跟他說："),
    ("三種我講的東西不一樣。", "三種要講的東西不一樣。"),
    ("想整個攤開看一次，打「<strong>諮詢</strong>」就好。一對一，", S2 + "一對一，"),
    ("韋總裁 ・ 資產配置", "資產配置"),
    ("韋總裁 ・ 第一個一百萬指南", "第一個一百萬指南"),
    ("<h4>所以這件事我當面跟你講</h4>", "<h4>所以這件事要當面講</h4>"),
    ("<strong>我寧願花三十分鐘", "<strong>寧願花三十分鐘"),
    ("<strong>我沒辦法隔著一份文件判斷你是哪一種</strong>。所以這段我寧願當面講，",
     "<strong>沒辦法隔著一份文件判斷你是哪一種</strong>。所以這段寧願當面講，找傳這份給你的人，"),
  ],
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

# 2026-09-12 補做（gap-fill 版型家族 A）
SENT["tax-check-3"] = [
  ("看完，直接在這個聊天室回我一句「<strong>想知道怎麼查</strong>」，IG 私訊我也可以。回的時候順便說一下你的收入來源有幾種，只有薪水就講薪水，我對著你的狀況跟你聊。",
   "看完，回給傳這份給你的人一句「<strong>想知道怎麼查</strong>」。回的時候順便說一下你的收入來源有幾種，只有薪水就講薪水，請他對著你的狀況跟你聊。"),
  ("想整個攤開看一次，打「<strong>諮詢</strong>」就好。一對一，把收支、預備金、這筆錢的用途一起看。第一次只聊你的狀況，要不要繼續，你自己決定。",
   S2 + "一對一，把收支、預備金、這筆錢的用途一起看。第一次只聊你的狀況，要不要繼續，你自己決定。"),
  ("要問國稅局或會計師，我不給個案稅務建議。", "要問國稅局或會計師，這份不給個案稅務建議。"),
  ('<div class="l">首次諮詢</div>', '<div class="l">第一次聊</div>'),
]
SENT["dividend-check-3"] = [
  ("看完，直接在這個聊天室回我一句「<strong>想知道怎麼算</strong>」，IG 私訊我也可以。回的時候順便說一下你現在是還在累積，還是已經要靠它過生活，我對著你的階段跟你聊。",
   "看完，回給傳這份給你的人一句「<strong>想知道怎麼算</strong>」。回的時候順便說一下你現在是還在累積，還是已經要靠它過生活，請他對著你的階段跟你聊。"),
  ("想整個攤開看一次，打「<strong>諮詢</strong>」就好。一對一，把收支、預備金、這筆錢的用途一起看。第一次只聊你的狀況，要不要繼續，你自己決定。",
   S2 + "一對一，把收支、預備金、這筆錢的用途一起看。第一次只聊你的狀況，要不要繼續，你自己決定。"),
  ("這個我不給也不能給，要問合法的證券投資顧問。", "這份不給也不能給，要問合法的證券投資顧問。"),
  ('<div class="l">首次諮詢</div>', '<div class="l">第一次聊</div>'),
]

# 2026-10-09 補做 11 份
# 新三段式（first-million 同家族）：諮詢卡第二句固定「想整個攤開看一次，打「諮詢」就好。」
_CONSULT_3SEG = ("想整個攤開看一次，打「<strong>諮詢</strong>」就好。", S2)
SENT["invest-start"] = [
  ("填下面的表約一次諮詢，我照你的狀況幫你排。還沒想到要不要約，就直接回我一句你現在卡在哪一步，我們先聊。",
   S2 + "還沒想到要不要約，就把你現在卡在哪一步，直接回給傳這份給你的人。"),
]
SENT["afford-sustain"] = [
  ("<span>把你的答案回給我，我跟你說先動哪一塊</span>",
   "<span>把你的答案回給傳這份給你的人，請他幫你看先動哪一塊</span>"),
  ("看完，直接在這個聊天室回我一句「<strong>想知道養不養得起</strong>」，IG 私訊我也可以。回的時候順便講一句就好：",
   "看完，直接回給傳這份給你的人一句「<strong>想知道養不養得起</strong>」。回的時候順便講一句就好："),
  ("這三種我講的東西不一樣。", "這三種要講的東西不一樣。"),
  _CONSULT_3SEG,
]
SENT["tech-pairing"] = [
  ("看完，直接在這個聊天室回我一句「<strong>想知道怎麼搭配</strong>」，IG 私訊我也可以。回的時候順便跟我說：",
   "看完，直接回給傳這份給你的人一句「<strong>想知道怎麼搭配</strong>」。回的時候順便跟他說："),
  ("三種我講的東西不一樣。", "三種要講的東西不一樣。"),
  _CONSULT_3SEG,
]
SENT["retire-backward"] = [
  ("<span>把你算出來的數字回給我，我跟你說先動哪一塊</span>",
   "<span>把你算出來的數字回給傳這份給你的人，請他幫你看先動哪一塊</span>"),
  ("看完，直接在這個聊天室回我一句「<strong>我的數字</strong>」，IG 私訊我也可以。回的時候順便講一句就好：你希望退休後一個月有多少可以花？還沒想過也直接說，我們一起抓。",
   "看完，直接回給傳這份給你的人一句「<strong>我的數字</strong>」。回的時候順便講一句就好：你希望退休後一個月有多少可以花？還沒想過也直接說，請他陪你一起抓。"),
  _CONSULT_3SEG,
]
SENT["dividend-3flaws"] = [
  ("看完，直接在這個聊天室回我一句「<strong>想知道怎麼放</strong>」，IG 私訊我也可以。回的時候順便講一句就好：",
   "看完，直接回給傳這份給你的人一句「<strong>想知道怎麼放</strong>」。回的時候順便講一句就好："),
  ("這兩種人我講的東西不一樣。", "這兩種人要講的東西不一樣。"),
  _CONSULT_3SEG,
]
# v2 數字卡版（about/sign/brand/母版註解走 GENERIC_RE；CTA 第二句逐句換）
SENT["salary-split5"] = [
  ("<p>把你預備金還差多少<b>回我</b>，我告訴你先動哪一塊。想知道自己怎麼配置，打「<b>諮詢</b>」。</p>",
   "<p>把你預備金還差多少，<b>回給傳這份給你的人</b>，請他幫你看先動哪一塊。" + S2 + "</p>"),
]
# equity-loan 母版家族（hero 留言句、「私訊我幫你看一次」走 GENERIC）
SENT["credit-line"] = [
  ("想知道的話，回 LINE 跟我說房子在哪一區、哪年買的就好。",
   "想知道的話，把房子在哪一區、哪年買的，回給傳這份給你的人，請他幫你看一眼。"),
]
SENT["deposit-optimize"] = [
  ("這份指南不寫。私訊我，我當面幫你算一次。", "這份指南不寫。" + S2),
]
SENT["thirty-recipe"] = [
  ("<h2 class=\"h2\">算你的 30 萬之前，先認識我</h2>", "<h2 class=\"h2\">算你的 30 萬之前，先看這份在講什麼</h2>"),
  ("要不要繼續聊，你自己決定。</p>", "要不要繼續聊，你自己決定。</p>\n  <p class=\"cta-body\">" + S2 + "</p>"),
]
SENT["etf-roles"] = [
  ("5 年第一線觀察", "第一線觀察"),
  ("<strong>我不報明牌，先看適不適合再談</strong>。</p>",
   "<strong>我不報明牌，先看適不適合再談</strong>。</p>\n  <p class=\"cta-body\">" + S2 + "</p>"),
]


# 2026-10-29：J卡推薦碼公版——預設連官網，同仁在網址後加 ?ref=<自己的推薦碼> 才換成他的推薦連結
JREF_NOTE = "<!-- 公版給同仁：辦卡按鈕預設連台北富邦官網。要放你自己的推薦連結，傳網址時在後面加 ?ref=你的推薦碼（你推薦連結 ebank.taipeifubon.com.tw/EXT/curl/ 後面那串），例：…/unit/jcard-guide/?ref=AbCd1234 -->"
SENT["jcard-guide"] = [
  ('<p class="disclose">這個連結有<b>我的專屬推薦碼</b>，<br>新戶用它辦卡，銀行會給我推薦禮；<br>你拿的都一樣，用不用都可以。</p>',
   JREF_NOTE + '\n    <p class="disclose" id="ref-disclose">按鈕連到台北富邦官網辦卡；<br>傳這份給你的人如果有推薦連結，用他的也可以，<br>你拿的權益都一樣。</p>'),
  ('<a class="btn" href="https://ebank.taipeifubon.com.tw/EXT/curl/WyQDMliO" target="_blank" rel="noopener">用我的專屬推薦碼辦 J 卡<small>點進去自動帶入推薦碼｜由銀行審核</small></a>',
   '<a class="btn" id="ref-btn" href="https://www.fubon.com/banking/Personal/credit_card/all_card/omiyage/omiyage.htm" target="_blank" rel="noopener">去辦 J 卡<small>由銀行審核</small></a>\n'
   '    <script>(function(){try{var r=new URLSearchParams(location.search).get("ref");if(r&&/^[A-Za-z0-9]{4,20}$/.test(r)){var b=document.getElementById("ref-btn");b.href="https://ebank.taipeifubon.com.tw/EXT/curl/"+r;b.innerHTML="用推薦碼辦 J 卡<small>點進去自動帶入推薦碼｜由銀行審核</small>";document.getElementById("ref-disclose").innerHTML="這個連結有<b>傳這份給你的人的推薦碼</b>，<br>新戶用它辦卡，銀行會給他推薦禮；<br>你拿的都一樣，用不用都可以。";}}catch(e){}})();</script>'),
  ("辦卡按鈕帶有韋總裁的專屬推薦碼（J 卡揪友推薦）：新戶透過它核卡並完成首刷，推薦人可獲得台北富邦銀行的即享券；",
   "辦卡按鈕若帶有推薦碼（J 卡揪友推薦）：新戶透過它核卡並完成首刷，推薦人可獲得台北富邦銀行的即享券；"),
]

SENT["jcard-guide"] += [
  ('<span>整理｜<b>韋總裁</b></span>', ''),
]
SENT["travel-fund"] = [
  ('<h2 class="h2">在算你的出國預算之前，<br>先讓你知道我是誰</h2>', '<h2 class="h2">在算你的出國預算之前，<br>先看這份在講什麼</h2>'),
  ('<li><span class="num">→</span><span>最後送你一個 3 分鐘的理財人格測驗</span></li>', '<li><span class="num">→</span><span>算完，找傳這份給你的人一起看</span></li>'),
  ('<h3>我們的做法：<br>每個月配多少，事先就定好</h3>', '<h3>一種做法：<br>每個月配多少，事先就定好</h3>'),
  ('<p>我們用的月配方式，', '<p>有一種月配方式，'),
]
SENT["monthly-20k"] = [
  ('<h2 class="h2">在算你的數字之前，<br>先讓你知道我是誰</h2>', '<h2 class="h2">在算你的數字之前，<br>先看這份在講什麼</h2>'),
]

# 2026-10-29：測驗卡／填表卡（連韋總 LINE、表單）整張換成中性諮詢卡
NEUTRAL_CTA = {
  "travel-fund": ("你的出國預算，<br><span class=\"g\">找人一起算一次</span>",
                  "三個地方怎麼分、本金怎麼累積，每個人的收入跟存款都不一樣。"),
  "monthly-20k": ("你的月領目標，<br><span class=\"g\">找人一起算一次</span>",
                  "每個月想多領多少、要先準備什麼，每個人的數字都不一樣。先把你的數字算清楚，再談後面的事。"),
}
def neutral_cta(s, t):
    if s not in NEUTRAL_CTA:
        return t
    i = t.find('<div class="cta-card">')
    if i == -1:
        return t
    h2, body = NEUTRAL_CTA[s]
    t = _remove_div_block(t, i)
    card = ('<div class="cta-card">\n  <h2 class="cta-h2">' + h2 + '</h2>\n  <div class="cta-rule"></div>\n'
            '  <p class="cta-body">' + body + '</p>\n  <p class="cta-body">' + S2 + '</p>\n</div>\n')
    return t[:i] + card + t[i:]

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
  # 2026-10-09 新三段式／equity-loan 母版／v2 數字卡版共用構件
  ("<div class=\"hero-meta\">韋總裁 ・ ", "<div class=\"hero-meta\">"),           # hero-meta「韋總裁 ・ 分類」
  ("本內容由韋總裁（吳昌韋）提供，", "本內容"),                                 # footer 首句署名
  ("，私訊我幫你看一次。", "，請傳這份給你的人幫你看一次。"),                    # equity-loan 母版 03 收尾句
]
GENERIC_RE = [
  re.compile(r'<a class="cta-sign-link"[^>]*>.*?</a>\s*', re.S),
  re.compile(r'<div class="foot-handle">.*?</div>\s*', re.S),
  re.compile(r'<h2 class="h2">[^<]*我是誰[^<]*</h2>\s*'),
  re.compile(r'<p class="h2-sub">[^<]*為什麼是我[^<]*</p>\s*'),
  # equity-loan 母版 hero：「留言「增值」來的，這份就是說好的指南。」→ 整句刪，留後面的「3 分鐘，看懂…」
  re.compile(r'留言「[^」<]{1,10}」來的，(?:這份就是說好的[^。<]{1,10}。|說好的)'),
  # v2 數字卡版：B 關於我(含頭像)、E 署名、footer 品牌句、母版說明註解
  re.compile(r'<section class="about">.*?</section>\s*', re.S),
  re.compile(r'\s*<div class="sign">韋總裁</div>'),
  re.compile(r'<span class="brand">做自己的富一代</span>'),
  re.compile(r'<!-- ═+\s*懶人包通用母版 v2.*?-->\s*', re.S),
  re.compile(r'<!-- [A-E] .*?-->\s*', re.S),
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
        t = neutral_cta(s, t)                                                          # 10/29 中性諮詢卡
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
