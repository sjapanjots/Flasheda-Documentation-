"""Render the SVG illustrations to WebP files in static/illustrations/.

Browsers draw the SVGs' turbulence and displacement filters pixel by pixel,
which is slow on ordinary devices. Pre-rendered images look identical and are
cached by the browser. Run after changing docs_site/illustrations.py:

    python scripts/render_illustrations.py

Needs Playwright with Chromium (pip install playwright && playwright install chromium).
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from docs_site.illustrations import STATIC_DIR, sources  # noqa: E402

SCALE = 2        # render at 2x for sharp images on high-density screens
QUALITY = 0.86   # WebP quality


def main() -> None:
    from playwright.sync_api import sync_playwright

    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        for name, uri in sources().items():
            data_url = page.evaluate(
                """async ([uri, scale, q]) => {
                    const img = new Image(); img.src = uri; await img.decode();
                    const c = document.createElement('canvas');
                    c.width = img.naturalWidth * scale; c.height = img.naturalHeight * scale;
                    c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
                    return c.toDataURL('image/webp', q);
                }""",
                [uri, SCALE, QUALITY],
            )
            out = STATIC_DIR / f"{name}.webp"
            out.write_bytes(base64.b64decode(data_url.split(",", 1)[1]))
            print(f"{out.name:28} {out.stat().st_size / 1024:6.1f} KB")
        browser.close()


if __name__ == "__main__":
    main()
