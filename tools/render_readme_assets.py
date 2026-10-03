"""Render the profile README pictures, drawn like niansia.com: the hero (3 languages x light/dark) and the featured
project tiles (one per project, language and theme), as WebP with transparent corners.

Requires Playwright with a Chrome channel and Pillow. Run from the repository root:
    python tools/render_readme_assets.py            hero + tiles (tile data: PROJECTS in tools/build_readmes.py)
    python tools/render_readme_assets.py --cards    re-render the 2:1 source pictures in assets/work/cards from diagrams
    python tools/render_readme_assets.py --lumigrid <dark input.jpg> <LumiGrid output.jpg>
"""

from __future__ import annotations

import asyncio
import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_readmes import PROJECTS  # noqa: E402

README = ROOT / "assets" / "readme"
TILES = README / "tiles"
WORK = ROOT / "assets" / "work"
CARDS = WORK / "cards"
LANGS = ("en", "zh-TW", "zh-CN")
THEMES = ("light", "dark")
FONT = next((str(p) for p in (Path(r"C:\Windows\Fonts\seguisb.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")) if p.exists()), None)

# project id -> diagram in assets/work, drawn onto a 1280x640 source card (--cards)
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


def webp(png: bytes, dest: Path, quality: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.open(io.BytesIO(png)).save(dest, "WEBP", quality=quality, method=6, alpha_quality=90)


async def render_art() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": 1280, "height": 430}, device_scale_factor=2)
        hero = (ROOT / "tools" / "readme_hero.html").as_uri()
        for lang in LANGS:
            for theme in THEMES:
                await page.goto(f"{hero}?lang={lang}&theme={theme}")
                await page.evaluate("document.fonts.ready")
                await page.wait_for_timeout(500)
                webp(await page.screenshot(omit_background=True), README / f"hero-{lang}-{theme}.webp", 86)
        tile = (ROOT / "tools" / "readme_tile.html").as_uri()
        page = await browser.new_page(viewport={"width": 540, "height": 452}, device_scale_factor=2)
        for p_ in PROJECTS:
            for lang in LANGS:
                for theme in THEMES:
                    await page.goto(f"{tile}?lang={lang}&theme={theme}")
                    data = {"id": p_["id"], "name": p_["name"], "status": p_["status"], "kind": p_["kind"], "pitch": p_["pitch"][lang],
                            "focus": p_.get("focus", "50% 50%"), "src": (ROOT / p_["src"]).as_uri()}
                    await page.evaluate("d => render(d)", data)
                    await page.wait_for_timeout(150)
                    webp(await page.screenshot(omit_background=True), TILES / f"{p_['id']}-{lang}-{theme}.webp", 84)
        await browser.close()


async def render_cards() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        card = await browser.new_page(viewport={"width": 1280, "height": 640})
        for name, src in CARD_SOURCES.items():
            tmp = CARDS / "_card.html"  # a file URL so the page may load local images
            tmp.write_text(CARD_HTML.format(src=(WORK / src).as_uri()), encoding="utf-8")
            await card.goto(tmp.as_uri())
            await card.wait_for_timeout(400)
            tmp.unlink()
            Image.open(io.BytesIO(await card.screenshot())).convert("RGB").save(CARDS / f"{name}.jpg", quality=86, optimize=True)
        await browser.close()


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--lumigrid":
        lumigrid_card(Path(sys.argv[2]), Path(sys.argv[3]), CARDS / "lumigrid.jpg")
    elif sys.argv[1:2] == ["--cards"]:
        asyncio.run(render_cards())
    else:
        asyncio.run(render_art())
        print("hero + tiles written to", README.relative_to(ROOT))
