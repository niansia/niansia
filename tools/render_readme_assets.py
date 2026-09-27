"""Render the profile README cover (3 languages x light/dark) and the uniform 2:1 project cards.

Requires Playwright with a Chromium/Chrome channel and Pillow. Run from the repository root:
    python tools/render_readme_assets.py
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "assets" / "readme"
WORK = ROOT / "assets" / "work"
CARDS = WORK / "cards"
LANGS = ("en", "zh-TW", "zh-CN")
THEMES = ("light", "dark")
FONT = next((str(p) for p in (Path(r"C:\Windows\Fonts\seguisb.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")) if p.exists()), None)

# project id -> source image in assets/work (rendered onto a 1280x640 card)
CARD_SOURCES = {
    "merriv": "merriv-release-evidence-flow.svg",
    "kcrashlab": "kcrashlab-evidence-flow.svg",
    "chromarecover": "chromarecover-architecture.png",
    "noveltyaudit": "noveltyaudit-architecture.png",
}
CARD_HTML = """<!doctype html><html><body style="margin:0;width:1280px;height:640px;overflow:hidden;
background:radial-gradient(900px 500px at 50% 40%,#fffdf9,#f3ece2)">
<img src="{src}" style="position:absolute;inset:44px 56px;width:calc(100% - 112px);height:calc(100% - 88px);object-fit:contain;
filter:drop-shadow(0 18px 30px #2a22301f)"></body></html>"""


def lumigrid_card(src_in: Path, src_out: Path, dest: Path) -> None:
    """Before/after split of a held-out NTIRE 2025 test image, cropped to 2:1."""
    a, b = Image.open(src_in).convert("RGB"), Image.open(src_out).convert("RGB")
    w = 1280
    a, b = (im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) for im in (a, b))
    top = (a.height - 640) // 2
    a, b = a.crop((0, top, w, top + 640)), b.crop((0, top, w, top + 640))
    out = b.copy()
    cut = int(w * 0.42)
    out.paste(a.crop((0, 0, cut, 640)), (0, 0))
    draw = ImageDraw.Draw(out)
    draw.rectangle((cut - 2, 0, cut + 1, 640), fill=(255, 255, 255))
    font = ImageFont.truetype(FONT, 26) if FONT else ImageFont.load_default()
    for x, label in ((28, "input"), (cut + 28, "LumiGrid · 24.57 dB")):
        w = draw.textlength(label, font=font)
        draw.rounded_rectangle((x, 584, x + w + 32, 626), radius=21, fill=(21, 20, 42))
        draw.text((x + 16, 590), label, font=font, fill=(245, 239, 230))
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, quality=86, optimize=True)


async def main() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": 1280, "height": 400}, device_scale_factor=2)
        cover = (ROOT / "tools" / "readme_cover.html").as_uri()
        for lang in LANGS:
            for theme in THEMES:
                await page.goto(f"{cover}?lang={lang}&theme={theme}")
                await page.evaluate("document.fonts.ready")
                await page.wait_for_timeout(600)
                png = README / f"cover-{lang}-{theme}.png"
                await page.screenshot(path=str(png))
                Image.open(png).convert("RGB").save(png.with_suffix(".jpg"), quality=88, optimize=True, progressive=True)
                png.unlink()
        card = await browser.new_page(viewport={"width": 1280, "height": 640})
        for name, src in CARD_SOURCES.items():
            tmp = CARDS / "_card.html"  # a file URL so the page may load local images
            tmp.write_text(CARD_HTML.format(src=(WORK / src).as_uri()), encoding="utf-8")
            await card.goto(tmp.as_uri())
            await card.wait_for_timeout(400)
            tmp.unlink()
            await card.screenshot(path=str(CARDS / f"{name}.png"))
            png = CARDS / f"{name}.png"
            Image.open(png).convert("RGB").save(CARDS / f"{name}.jpg", quality=86, optimize=True)
            png.unlink()
        await browser.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 4 and sys.argv[1] == "--lumigrid":  # --lumigrid <dark input.jpg> <LumiGrid output.jpg>
        lumigrid_card(Path(sys.argv[2]), Path(sys.argv[3]), CARDS / "lumigrid.jpg")
    else:
        asyncio.run(main())
