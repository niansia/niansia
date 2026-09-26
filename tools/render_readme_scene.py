"""Render the two small, self-contained animations used by the profile READMEs.

Requires Pillow. Run from the repository root with:
    python tools/render_readme_scene.py
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "readme"
OUT.mkdir(parents=True, exist_ok=True)
SCALE = 2
FRAMES = 24

INK = "#101820"
PANEL = "#15222b"
PANEL_LIGHT = "#1b3038"
LINE = "#365158"
MUTED = "#83a0a4"
TEXT = "#dce9e6"
MINT = "#75d8bf"
MINT_DIM = "#3d8f82"
YELLOW = "#f3e9be"
YELLOW_EDGE = "#cfc390"
FACE = "#fff8e3"
LAVENDER = "#c5b9d9"
PINK = "#e9a9b4"
HAIR = "#a9c3d0"

FONT_MONO = next((p for p in (
    Path(r"C:\Windows\Fonts\CascadiaCode.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    Path("/System/Library/Fonts/Menlo.ttc"),
) if p.exists()), None)
FONT_SANS = next((p for p in (
    Path(r"C:\Windows\Fonts\seguisb.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
) if p.exists()), None)


class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width * SCALE, height * SCALE), INK)
        self.d = ImageDraw.Draw(self.image)

    def box(self, xy, fill, outline=None, radius=0, width=1):
        rect = tuple(round(v * SCALE) for v in xy)
        self.d.rounded_rectangle(
            rect, radius=radius * SCALE, fill=fill, outline=outline,
            width=width * SCALE,
        )

    def line(self, points, fill, width=1, joint="curve"):
        pts = [(round(x * SCALE), round(y * SCALE)) for x, y in points]
        self.d.line(pts, fill=fill, width=width * SCALE, joint=joint)

    def ellipse(self, xy, fill=None, outline=None, width=1):
        self.d.ellipse(tuple(round(v * SCALE) for v in xy), fill=fill,
                       outline=outline, width=width * SCALE)

    def arc(self, xy, start, end, fill, width=1):
        self.d.arc(tuple(round(v * SCALE) for v in xy), start, end,
                   fill=fill, width=width * SCALE)

    def poly(self, points, fill, outline=None, width=1):
        pts = [(round(x * SCALE), round(y * SCALE)) for x, y in points]
        self.d.polygon(pts, fill=fill)
        if outline:
            self.d.line(pts + [pts[0]], fill=outline, width=width * SCALE)

    def text(self, xy, value, size, fill, mono=False):
        path = FONT_MONO if mono else FONT_SANS
        font = (ImageFont.truetype(str(path), size * SCALE)
                if path else ImageFont.load_default(size=size * SCALE))
        self.d.text((round(xy[0] * SCALE), round(xy[1] * SCALE)),
                    value, font=font, fill=fill)

    def small(self):
        return self.image.resize((self.width, self.height), Image.Resampling.LANCZOS)


def backdrop(c: Canvas, footer=False):
    w, h = c.width, c.height
    c.box((2, 2, w - 3, h - 3), PANEL, LINE, 17, 1)
    for x in range(24, w - 12, 26):
        for y in range(22, h - 10, 26):
            if x < 315 or x > 910:
                c.ellipse((x, y, x + 1, y + 1), fill="#2c4148")
    if not footer:
        c.line([(25, 52), (w - 25, 52)], LINE)
        c.ellipse((29, 26, 38, 35), fill=MINT)
        c.text((47, 20), "NIANSIA  /  FIELD LAB", 15, TEXT, mono=True)
        c.text((756, 22), "research in progress", 12, MUTED, mono=True)


def draw_mascot(c: Canvas, frame: int):
    bob = 1 if frame in (2, 3, 4, 14, 15, 16) else 0
    blink = frame in (5, 6, 18)
    paw = -2 if frame % 6 < 3 else 2

    # A tiny snail-hooded cat, echoing the profile avatar without using it as an asset.
    c.arc((53, 91, 313, 284), 190, 348, "#3b6f71", 2)
    for x, y in [(69, 172), (270, 105), (291, 202)]:
        c.ellipse((x - 3, y - 3, x + 3, y + 3), fill=MINT_DIM)

    c.ellipse((219, 141, 302, 228), fill=LAVENDER, outline="#8d85a7", width=3)
    c.arc((236, 160, 286, 211), 160, 480, "#817b99", 4)
    c.arc((247, 171, 275, 199), 170, 465, "#817b99", 3)
    c.ellipse((88, 160, 252, 265), fill=YELLOW, outline=YELLOW_EDGE, width=3)
    c.poly([(107, 121 + bob), (107, 74 + bob), (139, 98 + bob)],
           YELLOW, YELLOW_EDGE, 3)
    c.poly([(203, 98 + bob), (230, 71 + bob), (234, 130 + bob)],
           YELLOW, YELLOW_EDGE, 3)
    c.ellipse((91, 76 + bob, 246, 225 + bob), fill=YELLOW,
              outline=YELLOW_EDGE, width=3)

    # Rounded feelers make the silhouette recognizable at thumbnail size.
    c.line([(128, 82 + bob), (123, 58 + bob)], YELLOW_EDGE, 6)
    c.line([(212, 82 + bob), (217, 56 + bob)], YELLOW_EDGE, 6)
    c.ellipse((113, 48 + bob, 132, 67 + bob), fill=YELLOW,
              outline=YELLOW_EDGE, width=2)
    c.ellipse((208, 46 + bob, 227, 65 + bob), fill=YELLOW,
              outline=YELLOW_EDGE, width=2)
    c.ellipse((111, 99 + bob, 229, 211 + bob), fill=FACE,
              outline="#dccfa5", width=2)
    c.arc((119, 99 + bob, 222, 158 + bob), 2, 180, HAIR, 15)
    c.arc((116, 101 + bob, 198, 158 + bob), 15, 170, "#8aaec1", 7)
    if blink:
        c.arc((135, 147 + bob, 153, 156 + bob), 15, 165, INK, 2)
        c.arc((187, 147 + bob, 205, 156 + bob), 15, 165, INK, 2)
    else:
        c.ellipse((139, 143 + bob, 149, 156 + bob), fill=INK)
        c.ellipse((191, 143 + bob, 201, 156 + bob), fill=INK)
        c.ellipse((142, 145 + bob, 145, 148 + bob), fill=FACE)
        c.ellipse((194, 145 + bob, 197, 148 + bob), fill=FACE)
    c.ellipse((122, 164 + bob, 143, 174 + bob), fill=PINK)
    c.ellipse((198, 164 + bob, 219, 174 + bob), fill=PINK)
    c.poly([(166, 162 + bob), (174, 162 + bob), (170, 167 + bob)], "#856f6c")
    c.arc((161, 162 + bob, 171, 175 + bob), 2, 130, "#856f6c", 2)
    c.arc((169, 162 + bob, 180, 175 + bob), 50, 175, "#856f6c", 2)
    for side in (-1, 1):
        x = 124 if side == -1 else 216
        c.line([(x, 172 + bob), (x + side * 13, 169 + bob)], "#9f9587", 1)

    # Keyboard and paws overlap the face subtly, suggesting active typing.
    c.box((128, 205, 284, 264), "#24414a", "#6ea899", 9, 2)
    c.box((139, 215, 272, 252), "#10252b", "#3d6667", 4, 1)
    c.text((172, 219), "</>", 24, MINT, mono=True)
    c.line([(123, 265), (289, 265)], "#839a92", 5)
    c.ellipse((116 + paw, 205, 145 + paw, 225), fill=FACE,
              outline=YELLOW_EDGE, width=2)
    c.ellipse((261 - paw, 207, 288 - paw, 227), fill=FACE,
              outline=YELLOW_EDGE, width=2)


def main_frame(frame: int):
    c = Canvas(960, 280)
    backdrop(c)
    draw_mascot(c, frame)

    c.box((338, 70, 921, 239), "#0f1b22", LINE, 11, 1)
    c.box((339, 71, 920, 105), PANEL_LIGHT, radius=10)
    c.line([(339, 105), (920, 105)], LINE)
    for i, color in enumerate((PINK, YELLOW_EDGE, MINT)):
        c.ellipse((353 + i * 17, 84, 361 + i * 17, 92), fill=color)
    c.text((419, 79), "lab://reproducibility", 14, TEXT, mono=True)
    c.text((782, 83), "live session", 11, MUTED, mono=True)

    c.text((360, 119), "$ python -m evaluate", 15, MINT, mono=True)
    lines = [
        ("01", "visual evidence", "captured"),
        ("02", "reasoning trace", "checked"),
        ("03", "experiment", "reproducible"),
    ]
    for i, (number, label, result) in enumerate(lines):
        y = 151 + i * 28
        c.text((359, y), number, 13, MUTED, mono=True)
        c.text((395, y), label, 14, TEXT, mono=True)
        c.text((562, y), result, 13, MINT if (frame + 3) // 5 % 3 == i else MUTED, mono=True)
        c.line([(360, y + 24), (714, y + 24)], "#294049")
    if frame % 8 < 5:
        c.box((550, 126, 559, 145), MINT, radius=1)

    c.line([(738, 120), (738, 225)], LINE)
    c.text((760, 119), "pipeline", 12, MUTED, mono=True)
    stages = [("input", 152), ("inspect", 181), ("proof", 210)]
    c.line([(776, 163), (776, 213)], MINT_DIM, 2)
    for i, (label, y) in enumerate(stages):
        active = (frame // 4) % 3 == i
        c.ellipse((769, y - 3, 783, y + 11), fill=MINT if active else "#325b5d",
                  outline="#a8efdb" if active else MINT_DIM, width=1)
        c.text((798, y - 7), label, 13, TEXT if active else MUTED, mono=True)

    c.text((355, 249), "observe   /   test   /   verify", 13, MUTED, mono=True)
    c.ellipse((886, 252, 895, 261), fill=MINT if frame % 8 < 4 else MINT_DIM)
    return c.small()


def footer_frame(frame: int):
    c = Canvas(960, 130)
    backdrop(c, footer=True)
    c.text((33, 25), "<", 25, MINT, mono=True)
    c.text((57, 26), "hello, world!", 19, TEXT, mono=True)
    c.text((36, 64), "open to thoughtful research notes", 13, MUTED, mono=True)

    # A message moves across an actual circuit route toward the mail endpoint.
    c.line([(432, 65), (524, 65), (540, 48), (665, 48),
            (681, 65), (770, 65)], LINE, 2)
    for x, y in [(524, 65), (665, 48), (770, 65)]:
        c.ellipse((x - 4, y - 4, x + 4, y + 4), fill=PANEL, outline=MINT_DIM, width=2)
    path = [(432 + t * 7, 65) for t in range(14)]
    path += [(529 + t * 2, 61 - t * 2) for t in range(8)]
    path += [(545 + t * 8, 47) for t in range(15)]
    path += [(665 + t * 2, 48 + t * 2) for t in range(9)]
    path += [(683 + t * 7, 65) for t in range(13)]
    x, y = path[(frame * 3) % len(path)]
    c.ellipse((x - 6, y - 6, x + 6, y + 6), fill=MINT, outline="#d4fff0", width=1)

    c.box((796, 33, 909, 96), "#203943", "#7caca4", 8, 2)
    c.poly([(803, 44), (851, 73), (901, 44)], "#335b61", "#9bc3b7", 2)
    c.line([(802, 87), (839, 62)], "#9bc3b7", 2)
    c.line([(903, 87), (864, 62)], "#9bc3b7", 2)
    c.ellipse((845, 65, 857, 77), fill=PINK)
    c.text((802, 103), "say hello", 11, MUTED, mono=True)
    return c.small()


def save_gif(name: str, frames: list[Image.Image], duration: int):
    # One shared palette prevents color flicker between optimized GIF frames.
    palette = frames[0].quantize(colors=112, method=Image.Quantize.MEDIANCUT)
    gif_frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE)
                  for frame in frames]
    gif_frames[0].save(OUT / name, save_all=True, append_images=gif_frames[1:],
                       duration=duration, loop=0, optimize=True, disposal=2)


if __name__ == "__main__":
    save_gif("research-lab.gif", [main_frame(i) for i in range(FRAMES)], 110)
    save_gif("contact-signal.gif", [footer_frame(i) for i in range(FRAMES)], 95)
    print(OUT / "research-lab.gif")
    print(OUT / "contact-signal.gif")
