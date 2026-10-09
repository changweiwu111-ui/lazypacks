#!/usr/bin/env python3
"""把 lp_counter.html 計數器補進懶人包 index.html（已有 wei-card-stats 的跳過）。
用法：python3 inject_counter.py            → 全部頂層懶人包
      python3 inject_counter.py <slug> ...  → 只補指定的
unit/（單位中性版，同仁流量）不裝。"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SNIP = open(os.path.join(HERE, 'lp_counter.html'), encoding='utf-8').read()
slugs = sys.argv[1:] or sorted(d for d in os.listdir(HERE)
                               if d != 'unit' and os.path.isfile(os.path.join(HERE, d, 'index.html')))
done = skip = 0
for s in slugs:
    p = os.path.join(HERE, s, 'index.html')
    t = open(p, encoding='utf-8').read()
    if 'wei-card-stats' in t or '</body>' not in t:
        skip += 1; continue
    i = t.rfind('</body>')
    open(p, 'w', encoding='utf-8').write(t[:i] + SNIP + t[i:])
    done += 1
print(f'✓ 計數器：新補 {done} 包，跳過 {skip} 包（已有或無 </body>）')
