"""Global styles and reusable HTML building blocks.

Design language: warm sand neutrals, warm-ink text, Inter at weight 500 with
tight tracking, pill-shaped controls, 12px panels, ink-and-watercolour
illustrations. FlashEDA's amber bolt and navy tile provide the brand accents.
"""

from __future__ import annotations

import html
from datetime import date
from pathlib import Path

import streamlit as st

from docs_site import illustrations as il

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/sjapanjots/Flash-EDA"
DOCS_REPO_URL = "https://github.com/sjapanjots/Flasheda-Documentation-"
PYPI_URL = "https://pypi.org/project/flasheda/"

C = {
    "page": "#FCFDFD", "sand": "#F3F2EB", "sand2": "#E8E6D9", "sand3": "#DCD9C9",
    "ink": "#26251E", "ink2": "#3B392F", "body": "#545244", "muted": "#6F6C5B", "faint": "#A9A593",
    "orange": "#F97316", "amber": "#F59E0B", "gold": "#FDE047", "navy": "#0B1220", "navy2": "#16233D",
}


_CSS = f"""
<style>
:root {{ --ink:{C['ink']}; --body:{C['body']}; --muted:{C['muted']}; --sand:{C['sand']}; --sand2:{C['sand2']}; --sand3:{C['sand3']}; --orange:{C['orange']}; }}

/* ---------- page frame ---------- */
.stApp {{ background: linear-gradient(180deg, {C['sand3']} 0px, {C['sand2']} 140px, {C['page']} 620px, {C['page']} 100%); }}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stMainBlockContainer"] {{ max-width: 1200px; padding: 6.5rem 2rem 0; }}
[data-testid="stDecoration"] {{ display: none; }}
h1, h2, h3, h4 {{ color: var(--ink) !important; font-weight: 500 !important; }}
a {{ color: var(--ink); }}

/* ---------- top navigation: floating pill ---------- */
[data-testid="stHeader"] {{ height: 76px; }}
[data-testid="stToolbar"] {{ justify-content: center; }}
[data-testid="stToolbar"] > div:first-child {{
  width: min(900px, calc(100vw - 2rem)); height: 50px; margin-top: 14px; padding: 0 9.5rem 0 1.1rem;
  background: rgba(243,242,235,.86); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(220,217,201,.7); border-radius: 9999px; box-shadow: 0 6px 24px rgba(38,37,30,.06); }}
[data-testid="stTopNav"] {{ justify-content: center; }}
[data-testid="stHeaderLogo"] {{ height: 26px !important; width: auto !important; }}
.fe-navcta {{ position: fixed; top: 26px; right: max(1.5rem, calc(50vw - 450px + 7px)); z-index: 1000001; }}
.fe-navcta a {{ display:inline-flex; align-items:center; gap:.4rem; background:{C['ink']}; color:#FCFDFD !important; text-decoration:none;
  border-radius:9999px; padding:.42rem 1rem; font-size:.88rem; font-weight:500; }}
.fe-navcta a:hover {{ background:#000; }}
[data-testid="stTopNavLinkContainer"] {{ gap: .15rem; }}
[data-testid="stTopNavLink"], [data-testid="stTopNavSection"] {{ border-radius: 9999px !important; }}
[data-testid="stTopNavLink"] span, [data-testid="stTopNavSection"] span {{ color: var(--ink2, #3B392F); font-size: .92rem; }}
[data-testid="stTopNavLink"][aria-current="page"] {{ background: {C['ink']} !important; }}
[data-testid="stTopNavLink"][aria-current="page"] span {{ color: #FCFDFD !important; }}

/* ---------- typography helpers ---------- */
.fe-pill {{ display:inline-flex; align-items:center; gap:.45rem; padding:.28rem .8rem; border-radius:9999px;
  background:{C['sand']}; color:{C['ink2']}; font-size:.82rem; font-weight:500; border:1px solid {C['sand2']}; text-decoration:none; }}
.fe-pill .dot {{ width:.45rem; height:.45rem; border-radius:9999px; background:var(--orange); }}
.fe-h1 {{ font-size: clamp(2.6rem, 5.6vw, 4.2rem); font-weight:500; letter-spacing:-.035em; line-height:1.02; color:var(--ink); margin:1.1rem 0 .9rem; }}
.fe-h2 {{ font-size: clamp(1.9rem, 3.4vw, 2.6rem); font-weight:500; letter-spacing:-.025em; line-height:1.1; color:var(--ink); margin:0; }}
.fe-h3 {{ font-size: 1.5rem; font-weight:500; letter-spacing:-.01em; line-height:1.3; color:var(--ink); margin:.7rem 0 .6rem; }}
.fe-lead {{ font-size: 1.22rem; line-height:1.55; color:var(--body); margin:0; }}
.fe-muted {{ color: var(--muted); }}

/* ---------- buttons ---------- */
.fe-btns {{ display:flex; gap:.6rem; flex-wrap:wrap; }}
.fe-btn {{ display:inline-flex; align-items:center; gap:.4rem; padding:.62rem 1.25rem; border-radius:9999px; font-weight:500; font-size:.95rem;
  text-decoration:none !important; transition:transform .15s ease, background .15s ease; }}
.fe-btn:hover {{ transform: translateY(-1px); }}
.fe-btn.dark {{ background:{C['ink']}; color:#FCFDFD !important; }}
.fe-btn.dark:hover {{ background:#000; }}
.fe-btn.light {{ background:{C['sand']}; color:{C['ink']} !important; border:1px solid {C['sand3']}; }}
.fe-link {{ color:var(--ink) !important; font-weight:500; text-decoration:none; border-bottom:1px solid {C['sand3']}; padding-bottom:1px; }}
.fe-link:hover {{ border-color: var(--ink); }}
.fe-install {{ display:inline-flex; align-items:center; gap:.7rem; font-family:'JetBrains Mono', ui-monospace, monospace; font-size:.92rem;
  background:{C['navy']}; color:#E2E8F0; padding:.6rem 1.1rem; border-radius:9999px; }}
.fe-install b {{ color:{C['gold']}; font-weight:500; }}

/* ---------- hero ---------- */
.fe-hero {{ text-align:center; padding: 1.2rem 0 0; }}
.fe-hero .fe-lead {{ max-width: 40rem; margin: 0 auto 1.6rem; }}
.fe-hero .fe-btns {{ justify-content:center; margin-bottom: 1.1rem; }}
.fe-hero-art {{ margin: 2.4rem -2rem 0; }}
.fe-hero-art img {{ width:100%; display:block; }}

/* ---------- sections ---------- */
.fe-section {{ padding: 4.5rem 0 1rem; }}
.fe-rule {{ border:0; height:1px; background:{C['sand2']}; margin: 2.5rem 0 0; }}
.fe-statement {{ font-size: clamp(1.5rem, 2.6vw, 2.15rem); line-height:1.25; letter-spacing:-.02em; color:var(--ink); font-weight:500; margin:1rem 0 0; max-width: 62rem; }}
.fe-statement span {{ color: var(--faint, #A9A593); }}
.fe-head-row {{ display:flex; justify-content:space-between; align-items:flex-end; gap:1.5rem; flex-wrap:wrap; margin-bottom: 2.5rem; }}

/* feature rows (text + sand panel) */
.fe-row {{ display:grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items:center; margin: 0 0 4.5rem; }}
.fe-row.rev .fe-row-text {{ order: 2; }}
.fe-row-text p {{ font-size:1.05rem; line-height:1.6; color:var(--body); margin:0 0 1rem; max-width: 30rem; }}
.fe-panel {{ background:{C['sand']}; border-radius:12px; padding: 1.6rem; min-height: 290px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden; }}
.fe-panel img.art {{ width: 72%; }}

/* mock UI cards inside panels */
.fe-mock {{ background:#fff; border-radius:12px; border:1px solid {C['sand2']}; box-shadow: 0 10px 30px rgba(38,37,30,.06); padding: 1rem 1.1rem; width: 100%; max-width: 420px; font-size: .86rem; color: var(--ink2,#3B392F); }}
.fe-mock h5 {{ margin:0 0 .6rem; font-size:.86rem; font-weight:600; display:flex; justify-content:space-between; color:var(--ink); }}
.fe-mock .tag {{ font-size:.72rem; background:{C['sand']}; padding:.1rem .5rem; border-radius:9999px; color:var(--muted); font-weight:500; }}
.fe-mock .row {{ display:flex; justify-content:space-between; gap:1rem; padding:.42rem 0; border-top:1px solid {C['sand']}; }}
.fe-mock .row:first-of-type {{ border-top:0; }}
.fe-mock .warn {{ display:flex; gap:.55rem; padding:.45rem 0; border-top:1px solid {C['sand']}; line-height:1.35; }}
.fe-mock .warn:first-of-type {{ border-top:0; }}
.fe-mock .ic {{ flex:none; width:1.25rem; height:1.25rem; border-radius:9999px; display:inline-flex; align-items:center; justify-content:center; font-size:.7rem; font-weight:700; }}
.ic.o {{ background:#FFEDD5; color:#C2410C; }} .ic.g {{ background:#E7EBDD; color:#3F6212; }} .ic.s {{ background:{C['sand']}; color:var(--muted); }}
.fe-code {{ background:{C['navy']}; color:#CBD5E1; border-radius:12px; padding:1rem 1.1rem; font-family:'JetBrains Mono', ui-monospace, monospace; font-size:.78rem; line-height:1.6; width:100%; max-width:440px; white-space:pre; overflow:hidden; }}
.fe-code .k {{ color:#F9A8D4; }} .fe-code .s {{ color:{C['gold']}; }} .fe-code .c {{ color:#64748B; }} .fe-code .ok {{ color:#86EFAC; }}

/* feature cards */
.fe-cards {{ display:grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem; }}
.fe-card {{ text-decoration:none !important; color:inherit !important; display:block; }}
.fe-card .art {{ background:{C['sand']}; border-radius:12px; aspect-ratio: 32/25; display:flex; align-items:center; justify-content:center; overflow:hidden; transition: transform .2s ease; }}
.fe-card:hover .art {{ transform: translateY(-3px); }}
.fe-card .art img {{ width:100%; }}
.fe-card h4 {{ font-size:1.1rem; font-weight:500; margin:.9rem 0 .25rem; color:var(--ink); }}
.fe-card p {{ font-size:.92rem; color:var(--muted); margin:0; line-height:1.45; }}

/* quote / highlight statement */
.fe-quote {{ font-size: clamp(1.6rem, 3vw, 2.4rem); line-height:1.22; letter-spacing:-.02em; color:var(--ink); font-weight:500; }}
.fe-quote mark {{ background:{C['sand2']}; color:var(--ink); padding: 0 .2rem; border-radius:3px; }}

/* stats */
.fe-stats {{ display:grid; grid-template-columns: repeat(4, 1fr); gap:1.25rem; margin-top:2.5rem; }}
.fe-stat {{ border-top:1px solid {C['sand3']}; padding-top:1rem; }}
.fe-stat b {{ display:block; font-size:2.4rem; font-weight:500; letter-spacing:-.03em; color:var(--ink); }}
.fe-stat span {{ font-size:.92rem; color:var(--muted); }}

/* engines strip */
.fe-engines {{ display:flex; gap:.6rem; flex-wrap:wrap; justify-content:center; margin-top:1.4rem; }}
.fe-engines span {{ background:#fff; border:1px solid {C['sand2']}; padding:.5rem 1.1rem; border-radius:9999px; font-weight:500; color:var(--ink); }}

/* CTA */
.fe-cta {{ text-align:center; padding: 5.5rem 0 4rem; }}
.fe-cta .fe-h2 {{ font-size: clamp(2.4rem, 4.6vw, 3.6rem); letter-spacing:-.035em; }}
.fe-cta .fe-lead {{ max-width: 36rem; margin: 1rem auto 1.6rem; }}
.fe-cta .fe-btns {{ justify-content:center; }}

/* ---------- docs pages ---------- */
.fe-doc-head {{ display:grid; grid-template-columns: 1.4fr 1fr; gap: 3rem; align-items:center; padding: .5rem 0 2rem; border-bottom:1px solid {C['sand2']}; margin-bottom: 1.5rem; }}
.fe-doc-head .fe-h1 {{ font-size: clamp(2.2rem, 4.4vw, 3.4rem); margin:.9rem 0 .7rem; }}
.fe-doc-head .fe-panel {{ min-height: 220px; padding: .8rem; }}
.fe-doc-head .fe-panel img {{ width: 85%; }}
.fe-side-title {{ font-size:.78rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; color:var(--faint,#A9A593); margin: .4rem 0 .5rem .6rem; }}
div[class*="st-key-docnav"] [data-testid="stPageLink"] a {{ border-radius:9999px; padding: .15rem .7rem; }}
div[class*="st-key-docnav"] [data-testid="stPageLink"] a p {{ font-size:.92rem; color: var(--body); }}
div[class*="st-key-docnav"] [data-testid="stPageLink-NavLink"][aria-current="page"],
div[class*="st-key-docnav"] a[aria-current="page"] {{ background:{C['sand']}; }}
div[class*="st-key-doccontent"] {{ max-width: 52rem; }}
div[class*="st-key-doccontent"] p, div[class*="st-key-doccontent"] li {{ font-size: 1.02rem; line-height:1.7; color: var(--ink2,#3B392F); }}
div[class*="st-key-doccontent"] h2 {{ font-size:1.75rem !important; letter-spacing:-.02em; margin-top: 2.2rem; }}
div[class*="st-key-doccontent"] h3 {{ font-size:1.35rem !important; letter-spacing:-.01em; margin-top: 1.8rem; }}
div[class*="st-key-doccontent"] table {{ border-collapse:separate; border-spacing:0; width:100%; border:1px solid {C['sand2']}; border-radius:12px; overflow:hidden; font-size:.92rem; margin: .4rem 0 1.2rem; }}
div[class*="st-key-doccontent"] th {{ background:{C['sand']}; color:var(--ink); font-weight:600; text-align:left; }}
div[class*="st-key-doccontent"] th, div[class*="st-key-doccontent"] td {{ border:0; border-bottom:1px solid {C['sand2']}; padding:.6rem .8rem; vertical-align:top; }}
div[class*="st-key-doccontent"] tr:last-child td {{ border-bottom:0; }}
div[class*="st-key-doccontent"] code {{ background:{C['sand']}; color:{C['ink']}; border-radius:6px; padding:.08rem .35rem; font-size:.86em; }}
div[class*="st-key-doccontent"] pre code {{ background: transparent; padding:0; font-size: .86rem !important; line-height: 1.6; }}
div[class*="st-key-doccontent"] [data-testid="stCode"] pre, div[class*="st-key-doccontent"] pre {{ border-radius:12px !important; }}
.fe-pager {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin: 3rem 0 1rem; }}
.fe-pager a {{ display:block; text-decoration:none !important; border:1px solid {C['sand2']}; border-radius:12px; padding: 1rem 1.2rem; background:#fff; }}
.fe-pager a:hover {{ background:{C['sand']}; }}
.fe-pager small {{ color: var(--muted); font-size:.8rem; }}
.fe-pager b {{ display:block; color: var(--ink); font-weight:500; font-size:1.05rem; margin-top:.15rem; }}
.fe-pager .next {{ text-align:right; grid-column: 2; }}

/* ---------- footer ---------- */
[data-testid="stMain"] {{ container-type: inline-size; }}
.fe-footer {{ width: 100cqw; margin: 5rem 0 0 calc(50% - 50cqw); padding: 3.5rem max(2rem, calc(50cqw - 568px)) 0; background: linear-gradient(180deg, {C['page']} 0%, #E4E8E4 70%, #D9E5EC 100%); }}
.fe-footer-cols {{ display:grid; grid-template-columns: 1.4fr repeat(4, 1fr); gap: 2rem; }}
.fe-footer-cols img {{ height: 34px; }}
.fe-footer h6 {{ font-size:.82rem; color:var(--faint,#A9A593); font-weight:500; margin:0 0 .7rem; text-transform:none; }}
.fe-footer a {{ display:block; color:{C['ink2']} !important; text-decoration:none; font-size:.9rem; padding:.18rem 0; }}
.fe-footer a:hover {{ color: var(--ink) !important; text-decoration:underline; }}
.fe-wordmark {{ font-size: clamp(5rem, 17vw, 15rem); font-weight:600; letter-spacing:-.06em; line-height:.9; color:{C['ink']}; margin: 3rem 0 1.2rem; white-space:nowrap; }}
.fe-wordmark span {{ color:{C['amber']}; }}
.fe-legal {{ display:flex; justify-content:space-between; flex-wrap:wrap; gap:.6rem; font-size:.85rem; color:var(--muted); }}
.fe-legal a {{ display:inline; padding:0; }}
.fe-landscape {{ margin: 1.5rem calc(-1 * max(2rem, calc(50cqw - 568px))) 0; }}
.fe-landscape img {{ width:100%; display:block; }}

/* hidden page links used for instant navigation (see spa_navigation) */
div[class*="st-key-spa-links"],
div:has(> div[class*="st-key-spa-links"]) {{ position:absolute !important; width:1px; height:1px; overflow:hidden; opacity:0; pointer-events:none; }}

/* ---------- responsive ---------- */
@media (max-width: 900px) {{
  [data-testid="stMainBlockContainer"] {{ padding: 5rem 1rem 0; }}
  .fe-row, .fe-doc-head {{ grid-template-columns: 1fr; gap: 1.5rem; }}
  .fe-row.rev .fe-row-text {{ order: 0; }}
  .fe-cards, .fe-stats {{ grid-template-columns: 1fr 1fr; }}
  .fe-footer-cols {{ grid-template-columns: 1fr 1fr; }}
  .fe-hero-art {{ margin-left:-1rem; margin-right:-1rem; }}
  .fe-footer {{ padding: 3rem 1rem 0; }}
  .fe-landscape {{ margin: 1.5rem -1rem 0; }}
  .fe-navcta {{ display:none; }}
}}
</style>
"""


def apply_theme() -> None:
    st.html(_CSS + f'<div class="fe-navcta"><a href="{REPO_URL}" target="_blank" rel="noopener">GitHub &#8599;</a></div>')


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def pill(text: str, dot: bool = False, href: str | None = None) -> str:
    inner = ('<span class="dot"></span>' if dot else "") + esc(text)
    if href:
        return f'<a class="fe-pill" href="{href}" target="_self">{inner} &rarr;</a>'
    return f'<span class="fe-pill">{inner}</span>'


def btn(label: str, href: str, kind: str = "dark") -> str:
    ext = href.startswith("http")
    tgt = 'target="_blank" rel="noopener noreferrer"' if ext else 'target="_self"'
    return f'<a class="fe-btn {kind}" href="{href}" {tgt}>{esc(label)}</a>'


def link(label: str, href: str) -> str:
    ext = href.startswith("http")
    tgt = 'target="_blank" rel="noopener noreferrer"' if ext else 'target="_self"'
    return f'<a class="fe-link" href="{href}" {tgt}>{esc(label)} &rarr;</a>'


def footer() -> None:
    cols = {
        "Get started": [("Installation", "get-started"), ("Quick start", "get-started"), ("How it works", "./#how")],
        "Guide": [("Analysis and reports", "analysis"), ("Cleaning code", "cleaning"), ("Models", "models"),
                  ("Data contracts", "contracts"), ("Time series", "time-series")],
        "Reference": [("API reference", "api"), ("Engines and scaling", "engines"), ("Performance", "performance"),
                      ("Changelog", "changelog")],
        "Project": [("GitHub", REPO_URL), ("PyPI", PYPI_URL), ("Report an issue", f"{REPO_URL}/issues"),
                    ("Contributing", "contributing"), ("Docs source", DOCS_REPO_URL)],
    }
    col_html = "".join(
        f"<div><h6>{esc(h)}</h6>" + "".join(
            f'<a href="{u}" {"target=_blank rel=noopener" if u.startswith("http") else "target=_self"}>{esc(t)}</a>'
            for t, u in items) + "</div>"
        for h, items in cols.items())
    st.html(f"""
<footer class="fe-footer">
  <div class="fe-footer-cols">
    <div><img src="app/static/logo/flasheda-logo-light.svg" alt="FlashEDA"/>
      <p class="fe-muted" style="font-size:.9rem;max-width:16rem;margin-top:.8rem">Fixed-time EDA for datasets of any size, and validated code to clean, model, check and forecast them.</p></div>
    {col_html}
  </div>
  <div class="fe-wordmark">flash<span>eda</span></div>
  <div class="fe-legal">
    <span>&copy; {date.today().year} FlashEDA &middot; MIT License &middot; Designed &amp; developed by <b>Japanjot Singh</b></span>
    <span><a href="{REPO_URL}" target="_blank" rel="noopener">GitHub</a> &nbsp;&middot;&nbsp; <a href="{PYPI_URL}" target="_blank" rel="noopener">PyPI</a></span>
  </div>
  <div class="fe-landscape"><img src="{il.url('landscape')}" alt=""/></div>
</footer>
""")


# ---------------------------------------------------------------------------
# Instant navigation
# ---------------------------------------------------------------------------
# Links written in HTML (buttons, cards, footer, pager, links inside the docs)
# would make the browser reload the whole app. This script catches clicks on
# internal links and clicks the matching hidden st.page_link instead, which
# switches page inside the running app, like the top navigation does.

_SPA_JS = r"""
<script>
(function () {
  const P = window.parent;
  if (P.__feSpaInstalled) return;
  P.__feSpaInstalled = true;
  P.document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a || a.closest('[class*="st-key-spa-links"]')) return;
    const href = a.getAttribute("href");
    if (!href || /^(https?:|mailto:|tel:|#)/i.test(href) || href.includes("#")) return;
    const path = new URL(href, P.location.href).pathname.replace(/\/+$/, "") || "/";
    for (const link of P.document.querySelectorAll('[class*="st-key-spa-links"] a[href]')) {
      const lp = new URL(link.href, P.location.href).pathname.replace(/\/+$/, "") || "/";
      if (lp === path) { e.preventDefault(); e.stopPropagation(); link.click(); P.scrollTo(0, 0); return; }
    }
  }, true);
})();
</script>
"""


def spa_navigation(pages) -> None:
    """Render hidden page links and the click handler that uses them."""
    import streamlit.components.v1 as components

    with st.container(key="spa-links"):
        for page in pages:
            st.page_link(page, label=page.title)
        components.html(_SPA_JS, height=0)
