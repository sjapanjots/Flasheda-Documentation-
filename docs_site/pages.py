"""Page registry, home page and documentation page renderer."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import streamlit as st

from docs_site import illustrations as il
from docs_site.theme import REPO_URL, PYPI_URL, ROOT, btn, esc, footer, link, pill

VERSION = "0.7.0"


@dataclass(frozen=True)
class Doc:
    slug: str
    title: str
    section: str
    lead: str
    art: str
    files: tuple = field(default_factory=tuple)  # content/*.md, joined with headings


DOCS = [
    Doc("get-started", "Get started", "Get started",
        "Install FlashEDA with pip, add the extras you need, and go from a raw file to a report, cleaning code and a model in a few lines.",
        "install", (("", "installation"), ("Quick start", "quick-start"))),
    Doc("analysis", "Analysis and reports", "Guide",
        "Profile a DataFrame, a file or a database table from a fixed-size sample and get a report in the console, HTML, PDF or JSON.",
        "analyse", (("", "analysis"),)),
    Doc("target", "Target analysis and leakage", "Guide",
        "Pass the column you want to predict to see the task type, class balance, per-feature predictive power and columns that leak the answer.",
        "analyse", (("", "target"),)),
    Doc("cleaning", "Cleaning code", "Guide",
        "Turn the findings into a plain Python cleaning script for pandas, polars, DuckDB or PySpark, validated on the sample before you get it.",
        "clean", (("", "cleaning"),)),
    Doc("features", "Features", "Guide",
        "Add date parts, encodings, text statistics and predictive ratios to the cleaning plan, with day/month order never guessed.",
        "plan", (("", "features"),)),
    Doc("models", "Models", "Guide",
        "Compare a baseline, a linear model, a random forest and gradient boosting on the sample, then get preparation and training scripts.",
        "models", (("", "models"),)),
    Doc("contracts", "Data contracts", "Guide",
        "Learn what good data looks like from a sample, then check every new file against it, in Python or as a CI script.",
        "contracts", (("", "contracts"),)),
    Doc("drift", "Comparing datasets", "Guide",
        "Find schema changes and per-column drift between two datasets with PSI, KS tests, median shifts and new categories.",
        "drift", (("", "drift"),)),
    Doc("databases", "Databases", "Guide",
        "Analyse, compare and check database tables and queries through any SQLAlchemy URL, with sampling done inside the database.",
        "databases", (("", "databases"),)),
    Doc("text", "Text and personal data", "Guide",
        "Detect emails, phone numbers, card numbers and other personal data, and profile free-text columns automatically.",
        "text", (("", "text"),)),
    Doc("time-series", "Time series and forecasting", "Guide",
        "Aggregate the full data per period, profile trend, seasonality and anomalies, and backtest simple forecasts.",
        "time-series", (("", "time-series"),)),
    Doc("notebook", "Notebook export", "Guide",
        "Export the whole analysis, cleaning, training, forecast and contract check as one Jupyter notebook that runs top to bottom.",
        "notebook", (("", "notebook"),)),
    Doc("engines", "Engines and scaling", "Reference",
        "Which engine FlashEDA picks for each data size, how sampling works, and how generated code is validated per engine.",
        "write", (("", "engines"),)),
    Doc("api", "API reference", "Reference",
        "Every public function and report method, with its signature, return type and purpose.",
        "reference", (("", "api"),)),
    Doc("performance", "Performance and limitations", "Reference",
        "Measured timings on files up to 5.3 million rows, and the trade-offs that come with deciding from a sample.",
        "sample", (("", "performance"), ("Limitations", "limitations"))),
    Doc("changelog", "Changelog", "Reference",
        "All notable changes to FlashEDA. Versions follow Semantic Versioning.",
        "notebook", (("", "changelog"),)),
    Doc("contributing", "Contributing", "Reference",
        "Set up a development install and see the checks every change must pass.",
        "validate", (("Development setup", "development"), ("Contributing guide", "contributing"))),
]
BY_SLUG = {d.slug: d for d in DOCS}
PAGES: dict = {}  # slug -> st.Page, filled by app.py


@lru_cache(maxsize=None)
def read(name: str) -> str:
    return (ROOT / "content" / f"{name}.md").read_text(encoding="utf-8")


def _href(slug: str) -> str:
    return slug


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def _mock_sample() -> str:
    return """<div class="fe-mock"><h5>orders.parquet <span class="tag">Sample</span></h5>
<div class="row"><span>True row count</span><b>from file metadata</b></div>
<div class="row"><span>Sample drawn</span><b>5,000 rows, uniform</b></div>
<div class="row"><span>How</span><b>seeded DuckDB reservoir</b></div>
<div class="row"><span>Full file loaded</span><b>never</b></div></div>"""


def _mock_warnings() -> str:
    return """<div class="fe-mock"><h5>report.warnings <span class="tag">Analyse</span></h5>
<div class="warn"><span class="ic o">!</span><span>Possible target leakage: refund_issued</span></div>
<div class="warn"><span class="ic s">i</span><span>price: 97% of values are numbers stored as text</span></div>
<div class="warn"><span class="ic s">i</span><span>city: 5 spellings collapse to 2 after trim/lower-case</span></div>
<div class="warn"><span class="ic s">i</span><span>price: skewness 1.7076</span></div></div>"""


def _mock_plan() -> str:
    rows = [("drop columns ['order_id']", "high"), ("convert 'price' to numbers", "medium"),
            ("trim and lower-case 'city'", "medium"), ("fill nulls in 'price' with 20.01", "medium"),
            ("log transform 'price'", "medium")]
    body = "".join(f'<div class="row"><span>{esc(s)}</span><span class="tag">{r}</span></div>' for s, r in rows)
    return f'<div class="fe-mock"><h5>plan.review() <span class="tag">Plan</span></h5>{body}</div>'


def _mock_code() -> str:
    return ('<div class="fe-code"><span class="c"># Generated by FlashEDA — engine: polars</span>\n'
            '<span class="k">import</span> polars <span class="k">as</span> pl\n\n'
            '<span class="k">def</span> transform(lf: pl.LazyFrame) -&gt; pl.LazyFrame:\n'
            '    <span class="c"># order_id: numeric ID column</span>\n'
            '    lf = lf.drop([<span class="s">\'order_id\'</span>])\n'
            '    lf = lf.unique(maintain_order=<span class="k">True</span>)\n'
            '    ...\n\n'
            '<span class="c"># Lazy scan + streaming sink</span>\n'
            'transform(pl.scan_csv(SOURCE)).sink_parquet(OUTPUT)</div>')


def _mock_validate() -> str:
    return ('<div class="fe-code"><span class="k">&gt;&gt;&gt;</span> code = fe.clean(<span class="s">"orders.csv"</span>, engine=<span class="s">"polars"</span>)\n'
            '<span class="k">&gt;&gt;&gt;</span> code.validate()\n'
            '<span class="ok">[OK] polars: matches reference on 5,000 sampled rows</span>\n\n'
            '<span class="k">&gt;&gt;&gt;</span> code.save(<span class="s">"clean_orders.py"</span>)\n'
            '<span class="c"># plain Python, no dependency on FlashEDA</span></div>')


def home() -> None:
    st.html(f"""
<section class="fe-hero">
  {pill(f"New in {VERSION}: risk, confidence and approval for every cleaning step", dot=True, href="changelog")}
  <h1 class="fe-h1">Exploratory data analysis<br/>in a flash</h1>
  <p class="fe-lead">FlashEDA analyses a fixed-size sample, so a 100-million-row file takes about as long as a 100-thousand-row one. Then it writes validated code to clean, model, check and forecast it.</p>
  <div class="fe-btns">{btn("Get started", "get-started")}{btn("View on GitHub", REPO_URL, "light")}</div>
  <div class="fe-install"><span>$</span> pip install <b>flasheda</b></div>
  <div class="fe-hero-art"><img src="{il.url('hero')}" alt="A huge dataset is sampled into a small grid of points, which becomes a report and a validated script"/></div>
</section>

<section class="fe-section">
  {pill("About")}
  <p class="fe-statement">Profiling tools tell you what's wrong with a dataset. <span>FlashEDA also writes the fix, as plain Python for pandas, polars, DuckDB or PySpark, and runs it on the sample before handing it over.</span></p>
  <hr class="fe-rule"/>
</section>
""")

    rows = [
        ("Sample", "Any size, in fixed time", "The true row count comes from file metadata or <code>count(*)</code>, then a uniform random sample of 5,000 rows is drawn without loading the full data.", "Analysis and reports", "analysis", _mock_sample()),
        ("Analyse", "Every problem, in one report", "Missing values, numeric and categorical profiles, correlations, text and personal data, and with a target: task type, class balance, predictive power and leakage.", "Target and leakage", "target", _mock_warnings()),
        ("Plan", "Engine-neutral steps, each with a reason", "Findings become a list of steps such as drop, fill, convert and encode. Each has a risk level and a confidence, and high-risk steps wait for approval.", "Cleaning code", "cleaning", _mock_plan()),
        ("Write", "Code for the engine that fits", "A writer turns the plan into a standalone script for pandas, polars, DuckDB or PySpark, so the same plan scales from a laptop to a cluster.", "Engines and scaling", "engines", _mock_code()),
        ("Validate", "Code you can trust", "Every generated script runs on the sample and its output is compared row by row with a pandas reference implementation before you get it.", "Quick start", "get-started", _mock_validate()),
    ]
    row_html = "".join(
        f"""<div class="fe-row{' rev' if i % 2 else ''}">
  <div class="fe-row-text">{pill(tag)}<h3 class="fe-h3">{title}</h3><p>{text}</p>{link(f"Read {lnk}", href)}</div>
  <div class="fe-panel">{mock}</div>
</div>""" for i, (tag, title, text, lnk, href, mock) in enumerate(rows))
    st.html(f"""
<section class="fe-section" id="how">
  <div class="fe-head-row">
    <div><h2 class="fe-h2">How FlashEDA works</h2><p class="fe-lead fe-muted" style="margin-top:.6rem;font-size:1.05rem">Sample, analyse, plan, write and validate, in seconds.</p></div>
    {btn("Get started", "get-started")}
  </div>
  {row_html}
</section>
""")

    cards = [
        ("clean", "Clean", "Validated cleaning scripts with reasons for every step.", "cleaning"),
        ("models", "Train", "Model comparison plus prep and training scripts.", "models"),
        ("contracts", "Guard", "Data contracts that fail a CI job on bad files.", "contracts"),
        ("drift", "Compare", "Schema changes and drift between datasets.", "drift"),
        ("databases", "Databases", "Sampling inside Postgres, DuckDB and more.", "databases"),
        ("text", "Text & personal data", "Find emails, phones and card numbers.", "text"),
        ("time-series", "Forecast", "Trend, seasonality and backtested forecasts.", "time-series"),
        ("notebook", "Notebook", "Everything as one runnable notebook.", "notebook"),
    ]
    card_html = "".join(
        f'<a class="fe-card" href="{href}" target="_self"><div class="art"><img src="{il.url("step-" + art)}" alt=""/></div>'
        f"<h4>{title}</h4><p>{desc}</p></a>" for art, title, desc, href in cards)
    st.html(f"""
<section class="fe-section">
  <div class="fe-head-row"><div><h2 class="fe-h2">What it's for</h2>
    <p class="fe-lead fe-muted" style="margin-top:.6rem;font-size:1.05rem">One package from the first look at the data to a checked pipeline.</p></div>
    {btn("Read the guide", "analysis", "light")}</div>
  <div class="fe-cards">{card_html}</div>
</section>

<section class="fe-section">
  <p class="fe-quote">A 100-million-row file takes about as long as a <mark>100-thousand-row one</mark>, and the code it writes is <mark>run on the sample</mark> before you ever see it.</p>
  <div class="fe-stats">
    <div class="fe-stat"><b>0.56 s</b><span>analyse a 5.1M-row Parquet file</span></div>
    <div class="fe-stat"><b>2.5 s</b><span>analyse, plan, write and validate cleaning code for a 1M-row CSV</span></div>
    <div class="fe-stat"><b>0.6 s</b><span>compare two 1M-row files</span></div>
    <div class="fe-stat"><b>0.3 s</b><span>analyse a 1M-row SQLite table, 5,000 rows transferred</span></div>
  </div>
  <p class="fe-muted" style="font-size:.85rem;margin-top:1rem">Measured on synthetic data with typical problems. {link("All timings", "performance")}</p>
</section>

<section class="fe-section" style="text-align:center">
  {pill("Engines")}
  <h2 class="fe-h2" style="margin-top:1rem">Same plan, four engines</h2>
  <div class="fe-engines"><span>pandas</span><span>polars</span><span>DuckDB</span><span>PySpark</span></div>
</section>

<section class="fe-cta">
  <h2 class="fe-h2">Try it in one line</h2>
  <p class="fe-lead">Requires Python 3.9 or newer and pandas 2.0 or newer. Optional extras add polars, DuckDB, scikit-learn, SQL and Spark support.</p>
  <div class="fe-btns">{btn("Read the docs", "get-started")}{btn("PyPI", PYPI_URL, "light")}</div>
</section>
""")
    footer()


# ---------------------------------------------------------------------------
# Documentation pages
# ---------------------------------------------------------------------------

def _sidebar(current: str) -> None:
    with st.container(key="docnav"):
        for section in ("Get started", "Guide", "Reference"):
            st.html(f'<div class="fe-side-title">{section}</div>')
            for d in DOCS:
                if d.section == section:
                    st.page_link(PAGES[d.slug], label=d.title)


def render_doc(slug: str) -> None:
    doc = BY_SLUG[slug]
    idx = DOCS.index(doc)
    st.html(f"""
<div class="fe-doc-head">
  <div>{pill(doc.section)}<h1 class="fe-h1">{esc(doc.title)}</h1><p class="fe-lead">{esc(doc.lead)}</p></div>
  <div class="fe-panel"><img src="{il.url('step-' + doc.art)}" alt=""/></div>
</div>""")
    nav, body = st.columns([1, 3.4], gap="large")
    with nav:
        _sidebar(slug)
    with body:
        with st.container(key="doccontent"):
            for heading, name in doc.files:
                if heading:
                    st.markdown(f"## {heading}")
                st.markdown(read(name))
        prev_d = DOCS[idx - 1] if idx > 0 else None
        next_d = DOCS[idx + 1] if idx < len(DOCS) - 1 else None
        parts = ""
        if prev_d:
            parts += f'<a href="{prev_d.slug}" target="_self"><small>&larr; Previous</small><b>{esc(prev_d.title)}</b></a>'
        if next_d:
            parts += f'<a class="next" href="{next_d.slug}" target="_self"><small>Next &rarr;</small><b>{esc(next_d.title)}</b></a>'
        st.html(f'<div class="fe-pager">{parts}</div>')
        st.html(f'<p class="fe-muted" style="font-size:.85rem">Something unclear? {link("Edit or report it on GitHub", REPO_URL + "/issues")}</p>')
    footer()


def make_page(slug: str):
    def page() -> None:
        render_doc(slug)
    page.__name__ = "page_" + slug.replace("-", "_")
    return page
