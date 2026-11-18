"""FlashEDA documentation site. Run with: streamlit run app.py"""

import streamlit as st

from docs_site.pages import DOCS, PAGES, home, make_page
from docs_site.theme import apply_theme

st.set_page_config(page_title="FlashEDA — Fixed-time EDA for data of any size",
                   page_icon="assets/logo/flasheda-mark-small-32.png", layout="wide")
st.logo("assets/logo/flasheda-logo-light.svg", size="large", link="https://github.com/sjapanjots/Flash-EDA")
apply_theme()

home_page = st.Page(home, title="Home", url_path="home", default=True)
for d in DOCS:
    PAGES[d.slug] = st.Page(make_page(d.slug), title=d.title, url_path=d.slug)

sections = {"": [home_page]}
for d in DOCS:
    sections.setdefault(d.section, []).append(PAGES[d.slug])

st.navigation(sections, position="top").run()
