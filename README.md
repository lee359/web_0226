# 📝 Markdown創作與渲染實作 <br>

## 1. 專案簡介
### content.md 主題

`content.md` 的主題為**個人技術履歷與作品集（Personal CV & Portfolio）**，涵蓋以下內容：

- 個人基本資料與自我介紹
- 程式語言與框架的技術技能表
- 學術背景（學歷、修習課程）
- 實際專案作品（RAG 問答系統、部落格平台、系統架構圖）
- 機器學習相關數學公式（損失函數、梯度下降、Softmax、Attention）
- 學習計畫任務清單與路線圖
- GitHub 統計圖片與相關連結

### Markdown 標籤使用範圍

文件中使用了以下所有要求的 Markdown 元素：

| 元素 | 說明 |
|------|------|
| 多層標題 | `#` ~ `####` 共四層 |
| 文字樣式 | **粗體**、*斜體*、~~刪除線~~、`行內程式碼` |
| 清單 | 有序清單、無序清單（含巢狀） |
| 任務清單 | `- [x]` / `- [ ]` |
| 表格 | 多個資料表 |
| 程式碼區塊 | Python、JavaScript、Mermaid |
| 引用區塊 | `>` blockquote |
| 水平線 | `---` |
| 超連結 | `[text](url)` |
| 圖片 | `![alt](url)` (GitHub Stats) |
| 數學公式 | `$inline$`、`$$display$$` (MathJax) |
| 流程圖 | Mermaid `graph` 語法（兩張） |

### 選用渲染工具 & 設計系統

使用 **Python `markdown` 套件**（搭配 `Pygments`）將 `content.md` 渲染為 `output/output.html`，並搭載完整設計系統：

| 層面 | 技術 | 說明 |
|------|------|------|
| 渲染核心 | `markdown` + `Pygments` | Markdown → HTML；One Dark 語法高亮 |
| 字型 | Inter + JetBrains Mono | Google Fonts CDN，現代 UI 標準字型 |
| 動畫 | CSS Keyframes + Intersection Observer API | 頁面進場動畫；滾動觸發逐元素淡入 |
| 互動 | CSS Transitions | Hover lift/glow 效果 |
| 排版 | CSS `clamp()` + CSS 自訂屬性 | 動態響應式字級，design-token 設計系統 |
| 圖表 | Mermaid.js CDN | 流程圖瀏覽器端渲染 |
| 數學 | MathJax CDN | LaTeX 公式向量渲染 |

選用理由：
- 純 Python 產生 HTML，**無需安裝 Node.js、Pandoc 或 LaTeX**
- CSS 自訂屬性（設計 token）使整體風格高度一致、易於維護
- Intersection Observer 在零依賴（無 GSAP / Framer Motion）的情況下實現流暢滾動動畫
- 跨平台（Windows / macOS / Linux）皆可執行

---

## 2. 環境需求

| 項目 | 版本需求 |
|------|---------|
| 作業系統 | Windows 10+ / macOS 12+ / Ubuntu 20.04+ |
| Python | 3.9 以上 |
| pip | 隨 Python 安裝 |
| 瀏覽器 | Chrome 90+ / Firefox 90+ / Edge 90+（支援 Intersection Observer API） |
| 網路連線 | 首次預覽需連線（載入 Google Fonts、Mermaid.js、MathJax CDN） |

> **Python 端無額外系統依賴**（無需 Pandoc、LaTeX、Node.js）。設計系統使用的 Inter 字型與 Mermaid.js / MathJax 所有動畫效果皆由瀏覽器端 CSS/JS 原生執行。

---

## 3. 安裝步驟

```bash
# 1. Clone repo（已在 GitHub Classroom 環境中完成）
git clone <your-repo-url>
cd hw1-markdown-creation-and-rendering-practice-lee359

# 2. （建議）建立虛擬環境
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. 安裝 Python 套件
pip install -r requirements.txt
```

---

## 4. 執行渲染

```bash
# 在 repo 根目錄執行
python render.py
```

執行後輸出結果存於 `output/output.html`：

```
✅  Successfully rendered → output/output.html
```

---

## 5. 預期輸出

| 檔案路徑 | 格式 | 說明 |
|----------|------|------|
| `output/output.html` | HTML | Sleek & Modern 互動式履歷頁面 |

### 視覺設計
- **網站部分截圖**：
    ![alt text](image-2.png)<br>
    ![alt text](image-1.png)

- **配色**：Indigo (#6366f1) / Violet (#8b5cf6) / Cyan (#06b6d4) 三色系，帶有輕度紫色光感背景
- **字型**：Inter（正文）+ JetBrains Mono（程式碼），Google Fonts CDN 載入
- **容器**：白色卡片圓角（16px），indigo 色調陰影，最大寬 880px

### 互動行為

| 功能 | 行為 |
|------|------|
| **閱讀進度條** | 頂端固定 3px 漸層進度條，隨頁面捲動即時更新 |
| **頁面進場動畫** | 容器整體以 `fadeInUp` keyframe 載入淡入 |
| **滾動觸發揭露** | 每個 `h2`、`h3`、段落、清單、引用、表格、程式碼區塊在進入視埠時逐一以 `fade-in-up` 呈現（錯開 55ms 延遲） |
| **連結 hover** | 漸層底線從左向右滑入（CSS `background-size` 動畫） |
| **程式碼區塊 hover** | 上移 3px + 陰影加深；頂部顯示 macOS 三點視窗 chrome |
| **引用區塊 hover** | 向右位移 5px + 輕微陰影 |
| **Mermaid 圖表 hover** | 上移 2px |
| **圖片 hover** | 放大 scale(1.02) + 陰影 |

### 特殊渲染

- One Dark 語法高亮（Pygments，Monokai fallback）
- Mermaid 流程圖（架構圖、學習路線圖）瀏覽器端自動渲染
- MathJax LaTeX 數學公式（損失函數、Softmax、Attention 等）

以任何現代瀏覽器開啟 `output/output.html` 即可預覽，**無需 server**。

---

## 6. 參考資料

**渲染核心**
- [Python-Markdown 官方文件](https://python-markdown.github.io/)
- [Pygments — Python 語法高亮套件](https://pygments.org/)

**前端設計系統**
- [Inter — Rasmus Andersson 設計的現代 UI 字型](https://rsms.me/inter/)
- [JetBrains Mono — 工程師專用等寬字型](https://www.jetbrains.com/lp/mono/)
- [Google Fonts CDN](https://fonts.google.com/)
- [CSS `clamp()` — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/clamp)

**動畫 & 互動**
- [Intersection Observer API — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [CSS Transitions — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions)
- [CSS Custom Properties（設計 token） — MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)

**圖表 & 公式**
- [Mermaid.js 官方文件](https://mermaid.js.org/)
- [MathJax 官方文件](https://www.mathjax.org/)

**其他**
- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats)
- [Markdown Guide](https://www.markdownguide.org/)


## 🤖 AI 輔助聲明

> 本文件部分內容（包含段落措辭、程式碼範例格式、排版結構）由 **GitHub Copilot（Claude Sonnet）** 輔助生成。創意發想與內容決策來自本人。<br>


