"""Render every SVG in a folder to PNG so you can look at it before publishing.

usage: python preview.py <svg_dir> <png_dir>
needs: pip install playwright && python -m playwright install chromium

The SVG is inlined into the page: screenshotting a bare .svg document times out,
and <img src="file://..."> inside about:blank renders as a broken image.
"""
import os
import sys

from playwright.sync_api import sync_playwright

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
names = sorted(f for f in os.listdir(src) if f.endswith(".svg"))
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 820, "height": 600})
    for f in names:
        with open(os.path.join(src, f)) as fh:
            pg.set_content('<body style="margin:0;background:#fff">' + fh.read() + "</body>")
        pg.wait_for_timeout(100)
        pg.locator("svg").first.screenshot(path=os.path.join(out, f[:-4] + ".png"))
        print("ok", f)
    b.close()
