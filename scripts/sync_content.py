"""Regenerate the Markdown pages in content/ from a Flash-EDA checkout.

Usage:  python scripts/sync_content.py /path/to/Flash-EDA

The README is split into one file per documentation page. Links to README
anchors are rewritten to the matching page of this site, and links to
repository files point at GitHub.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_URL = "https://github.com/sjapanjots/Flash-EDA"
OUT = Path(__file__).resolve().parent.parent / "content"

# README heading -> page slug
SECTIONS = {
    "## Why FlashEDA": "why",
    "## How it works": "how-it-works",
    "## Installation": "installation",
    "## Quick start": "quick-start",
    "### 1. Analysis and reports": "analysis",
    "### 2. Target analysis and leakage": "target",
    "### 3. Cleaning code": "cleaning",
    "### 4. Features": "features",
    "### 5. Models": "models",
    "### 6. Data contracts": "contracts",
    "### 7. Comparing datasets (drift)": "drift",
    "### 8. Databases": "databases",
    "### 9. Text and personal data": "text",
    "### 10. Time series and forecasting": "time-series",
    "### 11. Notebook export": "notebook",
    "## Engines and scaling": "engines",
    "## API reference": "api",
    "## Performance": "performance",
    "## Limitations": "limitations",
    "## Development": "development",
}

# README anchor -> site page
ANCHORS = {
    "why-flasheda": "./", "how-it-works": "./", "installation": "get-started", "quick-start": "get-started",
    "1-analysis-and-reports": "analysis", "2-target-analysis-and-leakage": "target", "3-cleaning-code": "cleaning",
    "4-features": "features", "5-models": "models", "6-data-contracts": "contracts",
    "7-comparing-datasets-drift": "drift", "8-databases": "databases", "9-text-and-personal-data": "text",
    "10-time-series-and-forecasting": "time-series", "11-notebook-export": "notebook",
    "engines-and-scaling": "engines", "api-reference": "api", "performance": "performance",
    "limitations": "performance", "development": "contributing",
}
FILES = {"CHANGELOG.md": "changelog", "CONTRIBUTING.md": "contributing"}


def rewrite_links(md: str) -> str:
    md = re.sub(r"\]\(#([a-z0-9-]+)\)", lambda m: f"]({ANCHORS.get(m.group(1), './')})", md)
    for name, slug in FILES.items():
        md = md.replace(f"]({name})", f"]({slug})")
    # Any other relative file link goes to GitHub.
    return re.sub(r"\]\((?!https?://|#|\./|[a-z-]+\))([^)]+)\)", lambda m: f"]({REPO_URL}/blob/main/{m.group(1)})", md)


def split_readme(text: str) -> dict[str, str]:
    lines = text.splitlines()
    starts = [(i, SECTIONS[l.strip()]) for i, l in enumerate(lines) if l.strip() in SECTIONS]
    heads = [i for i, l in enumerate(lines) if re.match(r"^##+ ", l)]
    out = {}
    for i, slug in starts:
        level = len(lines[i].split(" ")[0])
        end = next((h for h in heads if h > i and len(lines[h].split(" ")[0]) <= level), len(lines))
        body = "\n".join(lines[i + 1:end]).strip().strip("-").strip()
        out[slug] = rewrite_links(body) + "\n"
    return out


def main(src: Path) -> None:
    OUT.mkdir(exist_ok=True)
    pages = split_readme((src / "README.md").read_text(encoding="utf-8"))
    for name, slug in FILES.items():
        body = (src / name).read_text(encoding="utf-8").split("\n", 1)[1].strip()  # drop the H1
        pages[slug] = rewrite_links(body) + "\n"
    for slug, body in pages.items():
        (OUT / f"{slug}.md").write_text(body, encoding="utf-8")
    print(f"wrote {len(pages)} pages to {OUT}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "../Flash-EDA"))
