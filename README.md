# 韋總裁 ・ 懶人包庫（lazypacks）

短影音導流用的懶人包總集。每篇一個資料夾，網址 `https://changweiwu111-ui.github.io/lazypacks/<slug>/`。

首頁列表：https://changweiwu111-ui.github.io/lazypacks/

## 新增一篇
把懶人包 HTML 複製成 `<slug>/index.html`，在首頁 `index.html` 的清單加一張卡片，commit + push 即可。

## 自動加入（推薦）
```
./add-lazypack.sh <懶人包HTML> <slug> "<標題>" "<副標>"
```
會自動：放檔 → 更新 packs.json → 重建首頁 index.html → commit + push。
首頁清單由 `packs.json` 單一來源產生，改清單後跑 `python3 build_index.py` 即可重建。
