#!/bin/bash
# 一行把一篇懶人包加進庫並上線。
# 用法：./add-lazypack.sh <懶人包HTML路徑> <slug> <顯示標題> <一句副標> [LINE關鍵字,逗號分隔]
# 例： ./add-lazypack.sh ~/.../某懶人包.html tax-2026 "報稅省錢攻略" "5 個多數人漏掉的扣除額" "報稅,扣除額"
# 第5參數＝LINE 關鍵字（worker 靠 packs.json 的 kw 比對才會自動回懶人包；不給則沿用舊 kw 不洗掉）
set -e
SRC="$1"; SLUG="$2"; TITLE="$3"; SUB="$4"; KW="$5"
[ -z "$SRC" ] || [ -z "$SLUG" ] || [ -z "$TITLE" ] && { echo "用法：$0 <HTML> <slug> <標題> <副標>"; exit 1; }
[ -f "$SRC" ] || { echo "✗ 找不到 HTML：$SRC"; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

# 1) 放檔
mkdir -p "$SLUG"; cp "$SRC" "$SLUG/index.html"

# 2) 更新 packs.json（同 slug 去重後 append）
python3 - "$SLUG" "$TITLE" "$SUB" "$KW" <<'PY'
import json,sys
slug,title,sub,kw=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
p="packs.json"; data=json.load(open(p,encoding="utf-8"))
old=[x for x in data if x.get("slug")==slug]
data=[x for x in data if x.get("slug")!=slug]
rec={"slug":slug,"title":title,"sub":sub}
if kw:                                   # 新給的關鍵字（逗號分隔→多關鍵字）
    ks=[w.strip() for w in kw.split(",") if w.strip()]
    rec["kw"]=ks if len(ks)>1 else ks[0]
elif old and old[0].get("kw"):           # 沒給就沿用舊 kw，不洗掉
    rec["kw"]=old[0]["kw"]
data.append(rec)
json.dump(data,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"✓ packs.json 現有 {len(data)} 篇" + (f"，kw={rec.get('kw')}" if rec.get('kw') else "（無kw，worker不會自動回）"))
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
