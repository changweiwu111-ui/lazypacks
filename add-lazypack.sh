#!/bin/bash
# 一行把一篇懶人包加進庫並上線。
# 用法：./add-lazypack.sh <懶人包HTML路徑> <slug> <顯示標題> <一句副標>
# 例： ./add-lazypack.sh ~/.../某懶人包.html tax-2026 "報稅省錢攻略" "5 個多數人漏掉的扣除額"
set -e
SRC="$1"; SLUG="$2"; TITLE="$3"; SUB="$4"
[ -z "$SRC" ] || [ -z "$SLUG" ] || [ -z "$TITLE" ] && { echo "用法：$0 <HTML> <slug> <標題> <副標>"; exit 1; }
[ -f "$SRC" ] || { echo "✗ 找不到 HTML：$SRC"; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

# 1) 放檔
mkdir -p "$SLUG"; cp "$SRC" "$SLUG/index.html"

# 2) 更新 packs.json（同 slug 去重後 append）
python3 - "$SLUG" "$TITLE" "$SUB" <<'PY'
import json,sys,os
slug,title,sub=sys.argv[1],sys.argv[2],sys.argv[3]
p="packs.json"; data=json.load(open(p,encoding="utf-8"))
data=[x for x in data if x.get("slug")!=slug]
data.append({"slug":slug,"title":title,"sub":sub})
json.dump(data,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"✓ packs.json 現有 {len(data)} 篇")
PY

# 3) 重建首頁
python3 build_index.py

# 4) commit + push
git add -A
git -c user.name="changweiwu111-ui" -c user.email="changweiwu111@gmail.com" \
  commit -q -m "新增懶人包：$TITLE（$SLUG）"
git push -q origin main
echo "✓ 已上線：https://changweiwu111-ui.github.io/lazypacks/$SLUG/"
echo "  首頁：https://changweiwu111-ui.github.io/lazypacks/"
