#!/usr/bin/env python3
"""
render.py — Render content.md to output/output.html

Sleek & Modern redesign featuring:
  - Inter + JetBrains Mono (Google Fonts)
  - CSS custom-property design tokens (indigo / violet / cyan palette)
  - Sticky reading-progress bar
  - Scroll-triggered fade-in-up via Intersection Observer API
  - Hover lift & glow on code blocks, blockquotes, images, and diagrams
  - Animated gradient underline on links
  - macOS-style window chrome on code blocks
  - One Dark syntax highlighting (Pygments, falls back to Monokai)
  - Mermaid.js diagrams + MathJax LaTeX
  - Mobile-first responsive layout (clamp typography, fluid grid)
"""

import os
import re

import markdown
from pygments.formatters import HtmlFormatter

# ── 1. Read source Markdown ───────────────────────────────────────────────────
with open("content.md", "r", encoding="utf-8") as f:
    source = f.read()

# ── 2. Pre-process: protect Mermaid fences from Pygments ─────────────────────
mermaid_blocks: list[str] = []


def _save_mermaid(match: re.Match) -> str:
    mermaid_blocks.append(match.group(1).strip())
    return f"\n\nMERMAID_PLACEHOLDER_{len(mermaid_blocks) - 1}\n\n"


source = re.sub(r"```mermaid\r?\n(.*?)```", _save_mermaid, source, flags=re.DOTALL)

# ── 3. Convert Markdown → HTML ────────────────────────────────────────────────
md = markdown.Markdown(
    extensions=["extra", "codehilite", "toc", "sane_lists"],
    extension_configs={
        "codehilite": {"css_class": "highlight", "guess_lang": False, "use_pygments": True},
        "toc": {"title": "目錄", "toc_depth": 3},
    },
)
body_html = md.convert(source)

# ── 3b. Post-process: render task-list checkboxes ────────────────────────────
# 處理緊密清單：<li>[x] 文字
body_html = re.sub(r"<li>\[x\]", '<li><input type="checkbox" checked disabled>', body_html)
body_html = re.sub(r"<li>\[ \]", '<li><input type="checkbox" disabled>', body_html)
# 處理寬鬆清單（項目間有空行）：<li><p>[x] 文字</p></li>
body_html = re.sub(r"<li>\s*<p>\[x\]", '<li><p><input type="checkbox" checked disabled>', body_html)
body_html = re.sub(r"<li>\s*<p>\[ \]", '<li><p><input type="checkbox" disabled>', body_html)

# ── 4. Restore Mermaid blocks ─────────────────────────────────────────────────
for i, diagram in enumerate(mermaid_blocks):
    body_html = body_html.replace(
        f"<p>MERMAID_PLACEHOLDER_{i}</p>",
        f'<div class="mermaid-wrap"><div class="mermaid">{diagram}</div></div>',
    )

# ── 5. Pygments CSS — One Dark (Monokai fallback) ─────────────────────────────
try:
    pygments_css = HtmlFormatter(style="one-dark").get_style_defs(".highlight")
except Exception:
    pygments_css = HtmlFormatter(style="monokai").get_style_defs(".highlight")

# ── 6. Compose full HTML document ─────────────────────────────────────────────
html_output = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Personal CV &amp; Portfolio · Lee</title>

  <!-- Google Fonts: Inter (UI) + JetBrains Mono (code) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet" />

  <!-- Mermaid.js -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

  <!-- MathJax -->
  <script>
    MathJax = {{
      tex: {{ inlineMath: [['$','$']], displayMath: [['$$','$$']] }}
    }};
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>

  <style>
    /* ── Design tokens ─────────────────────────────────────────────────────── */
    :root {{
      --bg:       #f0f4ff;
      --surface:  #ffffff;
      --border:   #e2e8f7;
      --text:     #0d1326;
      --muted:    #5a6482;
      --a1:       #6366f1;
      --a2:       #8b5cf6;
      --a3:       #06b6d4;
      --grad:     linear-gradient(135deg, var(--a1), var(--a2));
      --sh-sm:    0 2px 12px rgba(99,102,241,.10);
      --sh-md:    0 8px 36px rgba(99,102,241,.15);
      --sh-lg:    0 20px 64px rgba(99,102,241,.20);
      --r:        16px;
      --r-sm:     8px;
      --t:        .3s cubic-bezier(.4,0,.2,1);
    }}

    /* ── Reset ─────────────────────────────────────────────────────────────── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}

    /* ── Body ──────────────────────────────────────────────────────────────── */
    body {{
      font-family: 'Inter', 'Microsoft JhengHei', 'Noto Sans TC', sans-serif;
      font-size: 16px;
      line-height: 1.85;
      color: var(--text);
      background: var(--bg);
      background-image:
        radial-gradient(ellipse at 15% 10%, rgba(99,102,241,.15) 0, transparent 55%),
        radial-gradient(ellipse at 85% 90%, rgba(139,92,246,.12) 0, transparent 55%);
      background-attachment: fixed;
      padding: 36px 16px 96px;
    }}

    /* ── Reading progress bar ──────────────────────────────────────────────── */
    #progress-bar {{
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 3px;
      background: var(--grad);
      transform: scaleX(0);
      transform-origin: left center;
      z-index: 1000;
      transition: transform .12s linear;
      border-radius: 0 2px 2px 0;
    }}

    /* ── Page container ────────────────────────────────────────────────────── */
    .container {{
      max-width: 880px;
      margin: 0 auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--r);
      box-shadow: var(--sh-md);
      padding: 60px 76px;
      animation: pageEnter .65s cubic-bezier(.22,1,.36,1) both;
    }}
    @keyframes pageEnter {{
      from {{ opacity: 0; transform: translateY(20px); }}
      to   {{ opacity: 1; transform: none; }}
    }}

    /* ── Scroll-reveal ─────────────────────────────────────────────────────── */
    .reveal {{
      opacity: 0;
      transform: translateY(22px);
      transition: opacity .6s ease, transform .6s ease;
    }}
    .reveal.visible {{
      opacity: 1;
      transform: none;
    }}

    /* ── h1 — hero headline ────────────────────────────────────────────────── */
    h1 {{
      font-size: clamp(1.9em, 4.5vw, 2.6em);
      font-weight: 800;
      letter-spacing: -.03em;
      line-height: 1.2;
      background: linear-gradient(100deg, var(--a1) 0%, var(--a2) 50%, var(--a3) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 8px;
    }}

    /* ── h2 ────────────────────────────────────────────────────────────────── */
    h2 {{
      font-size: clamp(1.25em, 2.8vw, 1.55em);
      font-weight: 700;
      color: var(--text);
      margin: 56px 0 18px;
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    h2::before {{
      content: '';
      display: inline-block;
      width: 4px;
      height: 1.25em;
      background: var(--grad);
      border-radius: 3px;
      flex-shrink: 0;
    }}

    /* ── h3 / h4 ───────────────────────────────────────────────────────────── */
    h3 {{
      font-size: 1.12em;
      font-weight: 600;
      color: var(--a1);
      margin: 30px 0 10px;
    }}
    h4 {{
      font-size: .8em;
      font-weight: 700;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .09em;
      margin: 22px 0 8px;
    }}

    /* ── Paragraph & inline ────────────────────────────────────────────────── */
    p {{ margin: 12px 0; }}

    a {{
      color: var(--a1);
      text-decoration: none;
      background-image: linear-gradient(var(--a1), var(--a2));
      background-size: 0 2px;
      background-position: 0 100%;
      background-repeat: no-repeat;
      transition: background-size var(--t), color var(--t);
    }}
    a:hover {{
      background-size: 100% 2px;
      color: var(--a2);
    }}

    strong {{ font-weight: 700; color: var(--text); }}
    em     {{ color: var(--a1); font-style: italic; }}
    del    {{ color: #a0aec0; text-decoration: line-through; }}

    /* ── Blockquote ────────────────────────────────────────────────────────── */
    blockquote {{
      margin: 24px 0;
      padding: 18px 24px 18px 30px;
      background: linear-gradient(135deg, rgba(99,102,241,.06), rgba(139,92,246,.03));
      border-left: 4px solid var(--a1);
      border-radius: 0 var(--r-sm) var(--r-sm) 0;
      color: #374151;
      transition: transform var(--t), box-shadow var(--t);
    }}
    blockquote:hover {{
      transform: translateX(5px);
      box-shadow: var(--sh-sm);
    }}
    blockquote p {{ margin: 5px 0; }}

    /* ── Tables ────────────────────────────────────────────────────────────── */
    .table-wrap {{
      overflow-x: auto;
      margin: 24px 0;
      border-radius: var(--r-sm);
      box-shadow: var(--sh-sm);
      border: 1px solid var(--border);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: .93em;
    }}
    thead tr {{ background: var(--grad); }}
    th {{
      color: #fff;
      padding: 13px 18px;
      text-align: left;
      font-weight: 600;
      letter-spacing: .02em;
    }}
    td {{ padding: 11px 18px; border-bottom: 1px solid var(--border); }}
    tr:last-child td {{ border-bottom: none; }}
    tbody tr:nth-child(even) td {{ background: rgba(99,102,241,.03); }}
    tbody tr {{ transition: background var(--t); }}
    tbody tr:hover td {{ background: rgba(99,102,241,.08); }}

    /* ── Lists ─────────────────────────────────────────────────────────────── */
    ul, ol {{ padding-left: 28px; margin: 12px 0; }}
    li {{ margin: 6px 0; }}
    ul li::marker {{ color: var(--a1); }}
    ol li::marker {{ color: var(--a1); font-weight: 700; }}
    input[type="checkbox"] {{
      accent-color: var(--a1);
      margin-right: 8px;
      width: 15px; height: 15px;
      vertical-align: middle;
    }}

    /* ── Inline code ───────────────────────────────────────────────────────── */
    code {{
      font-family: 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace;
      font-size: .82em;
      background: rgba(99,102,241,.09);
      color: var(--a2);
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid rgba(99,102,241,.18);
    }}

    /* ── Code blocks ───────────────────────────────────────────────────────── */
    .highlight {{
      position: relative;
      border-radius: var(--r-sm);
      margin: 24px 0;
      overflow: hidden;
      box-shadow: var(--sh-sm);
      transition: box-shadow var(--t), transform var(--t);
    }}
    .highlight:hover {{
      box-shadow: var(--sh-md);
      transform: translateY(-3px);
    }}
    /* macOS window chrome */
    .highlight::before {{
      content: '';
      display: block;
      height: 34px;
      background: #21252b;
      border-bottom: 1px solid #2d3139;
      background-image:
        radial-gradient(circle 5.5px at 18px 50%, #ff5f57, #ff5f57),
        radial-gradient(circle 5.5px at 37px 50%, #febc2e, #febc2e),
        radial-gradient(circle 5.5px at 56px 50%, #28c840, #28c840);
      background-repeat: no-repeat;
    }}
    .highlight pre {{
      margin: 0;
      padding: 20px 24px;
      overflow-x: auto;
      font-family: 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace;
      font-size: .84em;
      line-height: 1.78;
    }}
    .highlight code {{
      background: none;
      padding: 0;
      border: none;
      color: inherit;
      font-size: inherit;
    }}

    /* ── Pygments One Dark token colours (injected below) ──────────────────── */
    {pygments_css}

    /* ── Horizontal rule ───────────────────────────────────────────────────── */
    hr {{
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--border) 30%, var(--border) 70%, transparent);
      margin: 48px 0;
    }}

    /* ── Images ────────────────────────────────────────────────────────────── */
    img {{
      max-width: 100%;
      border-radius: var(--r-sm);
      margin: 14px 0;
      display: block;
      transition: transform var(--t), box-shadow var(--t);
    }}
    img:hover {{
      transform: scale(1.02);
      box-shadow: var(--sh-md);
    }}

    /* ── Mermaid diagrams ──────────────────────────────────────────────────── */
    .mermaid-wrap {{
      background: linear-gradient(135deg, rgba(99,102,241,.04), rgba(139,92,246,.04));
      border: 1px solid var(--border);
      border-radius: var(--r);
      padding: 28px;
      margin: 26px 0;
      text-align: center;
      overflow-x: auto;
      transition: box-shadow var(--t), transform var(--t);
      position: relative;
    }}
    .mermaid-wrap:hover {{
      box-shadow: var(--sh-sm);
      transform: translateY(-2px);
    }}
    /* 放大提示按鈕 */
    .mermaid-zoom-btn {{
      position: absolute;
      top: 10px; right: 12px;
      background: rgba(99,102,241,.12);
      border: 1px solid rgba(99,102,241,.25);
      border-radius: 6px;
      padding: 4px 9px;
      font-size: .75em;
      color: var(--a1);
      cursor: pointer;
      opacity: 0;
      transition: opacity var(--t), background var(--t);
      user-select: none;
    }}
    .mermaid-wrap:hover .mermaid-zoom-btn {{
      opacity: 1;
    }}
    .mermaid-zoom-btn:hover {{
      background: rgba(99,102,241,.25);
    }}
    /* Lightbox overlay */
    #mermaid-lightbox {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(13,19,38,.82);
      backdrop-filter: blur(6px);
      z-index: 2000;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }}
    #mermaid-lightbox.open {{
      display: flex;
    }}
    #mermaid-lightbox-content {{
      background: var(--surface);
      border-radius: var(--r);
      padding: 36px 40px;
      max-width: 92vw;
      max-height: 88vh;
      overflow: auto;
      box-shadow: var(--sh-lg);
      position: relative;
      text-align: center;
    }}
    #mermaid-lightbox-close {{
      position: absolute;
      top: 12px; right: 16px;
      background: none;
      border: none;
      font-size: 1.4em;
      color: var(--muted);
      cursor: pointer;
      line-height: 1;
      transition: color var(--t);
    }}
    #mermaid-lightbox-close:hover {{ color: var(--text); }}

    /* ── Math ──────────────────────────────────────────────────────────────── */
    .MathJax {{ overflow-x: auto; }}

    /* ── Responsive breakpoints ────────────────────────────────────────────── */
    @media (max-width: 1050px) {{
      .container {{ max-width: 96vw; padding: 52px 56px; }}
    }}
    @media (max-width: 900px) {{
      .container {{ padding: 44px 40px; }}
      h1 {{ font-size: clamp(1.6em, 5vw, 2em); }}
    }}
    @media (max-width: 680px) {{
      .container {{ padding: 36px 24px; }}
      h2 {{ margin-top: 44px; font-size: 1.2em; }}
      .highlight pre {{ font-size: .8em; padding: 16px 16px; }}
      .mermaid-wrap {{ padding: 18px 12px; }}
      th, td {{ padding: 9px 12px; font-size: .88em; }}
    }}
    @media (max-width: 480px) {{
      .container {{ padding: 28px 16px; border-radius: 10px; }}
      h2 {{ margin-top: 36px; }}
      code {{ font-size: .78em; }}
    }}
  </style>
</head>
<body>

  <!-- Reading progress -->
  <div id="progress-bar" role="progressbar" aria-label="Reading progress"></div>

  <!-- Mermaid Lightbox -->
  <div id="mermaid-lightbox" role="dialog" aria-modal="true" aria-label="圖表放大檢視">
    <div id="mermaid-lightbox-content">
      <button id="mermaid-lightbox-close" aria-label="關閉">&#x2715;</button>
      <div id="lb-svg-wrap"></div>
    </div>
  </div>

  <div class="container">
{body_html}
  </div>

  <script>
    /* ── 1. Reading-progress bar ────────────────────────────────────────────── */
    const bar = document.getElementById('progress-bar');
    window.addEventListener('scroll', function () {{
      var h = document.documentElement;
      var prog = h.scrollTop / (h.scrollHeight - h.clientHeight) || 0;
      bar.style.transform = 'scaleX(' + prog + ')';
    }}, {{ passive: true }});

    /* ── 2. Scroll-reveal via Intersection Observer ─────────────────────────── */
    var observer = new IntersectionObserver(function (entries) {{
      entries.forEach(function (entry) {{
        if (entry.isIntersecting) {{
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }}
      }});
    }}, {{ threshold: 0.07, rootMargin: '0px 0px -36px 0px' }});

    var targets = document.querySelectorAll(
      '.container h2, .container h3, .container h4, ' +
      '.container > p, .container > ul, .container > ol, ' +
      '.container > blockquote, .container .highlight, ' +
      '.container .mermaid-wrap, .container > img, .container > hr'
    );
    targets.forEach(function (el, i) {{
      el.classList.add('reveal');
      el.style.transitionDelay = (Math.min(i % 6, 5) * 55) + 'ms';
      observer.observe(el);
    }});

    /* ── 3. Wrap tables in scrollable container ─────────────────────────────── */
    document.querySelectorAll('.container table').forEach(function (tbl) {{
      if (!tbl.parentElement.classList.contains('table-wrap')) {{
        var wrap = document.createElement('div');
        wrap.className = 'table-wrap reveal';
        tbl.parentNode.insertBefore(wrap, tbl);
        wrap.appendChild(tbl);
        observer.observe(wrap);
      }}
    }});

    /* ── 4. Mermaid — 初始化（strict 模式防 XSS）───────────────────────────── */
    mermaid.initialize({{ startOnLoad: true, theme: 'neutral', securityLevel: 'strict' }});

    /* ── 5. Mermaid 點擊放大 Lightbox ──────────────────────────────────────── */
    var lightbox = document.getElementById('mermaid-lightbox');
    var lightboxContent = document.getElementById('mermaid-lightbox-content');
    var lightboxClose = document.getElementById('mermaid-lightbox-close');

    function openLightbox(svgHTML) {{
      document.getElementById('lb-svg-wrap').innerHTML = svgHTML;
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    }}
    function closeLightbox() {{
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    }}

    lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e) {{
      if (e.target === lightbox) closeLightbox();
    }});
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeLightbox();
    }});

    // 等 Mermaid 渲染完成後才掛按鈕（稍作延遲）
    setTimeout(function() {{
      document.querySelectorAll('.mermaid-wrap').forEach(function(wrap) {{
        var btn = document.createElement('button');
        btn.className = 'mermaid-zoom-btn';
        btn.setAttribute('aria-label', '放大圖表');
        btn.textContent = '⤢ 放大';
        wrap.appendChild(btn);
        btn.addEventListener('click', function() {{
          var svg = wrap.querySelector('svg');
          if (svg) openLightbox(svg.outerHTML);
        }});
      }});
    }}, 900);
  </script>
</body>
</html>
"""

# ── 7. Write output ───────────────────────────────────────────────────────────
output_path = "index.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅  Successfully rendered → {output_path}")
