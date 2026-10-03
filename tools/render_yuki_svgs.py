"""Animated SVGs for the profile READMEs, drawn like the terminal on niansia.com with Yuki's cat form.

    python tools/render_yuki_svgs.py contributions [--data calendar.json] [--out dist]
        Yuki trots over the last year's contribution calendar and eats every day that has contributions.
        Without --data it asks the GitHub GraphQL API (token from $GITHUB_TOKEN, else `gh auth token`).
        A GitHub Actions workflow (.github/workflows/yuki-contributions.yml) runs this daily and publishes
        the two files to the `output` branch.
    python tools/render_yuki_svgs.py contact [--out assets/readme]
        A terminal that types a short "let's research together" note and mails it; Yuki sits on the window.

Standard library only. The cat frames are the generated sprite from niansia.com (assets/readme/yuki-cat/,
exported from niansia.github.io assets/lab/yuki/cat/cat.webp); nothing here draws the character itself.
Both commands write a light and a dark file for <picture> with prefers-color-scheme.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import math
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "assets" / "readme" / "yuki-cat"
LOGIN = "niansia"
MONO = "'SFMono-Regular',ui-monospace,Menlo,Consolas,'Liberation Mono',monospace"

# niansia.com theme tokens (styles.scss :root and [data-theme='dark']) plus the contribution scale.
THEMES = {
    "light": {"surface": "#fdfdff", "rail": "#f5f6fb", "ink": "#262938", "muted": "#626779", "accent": "#5854b8",
              "accent2": "#c9578b", "line": "#dce0ec", "wash": "#edecfb", "green": "#387b68",
              "cells": ["#ebedf5", "#d9d4fb", "#b3abf3", "#8a7fe0", "#5854b8"], "shadow": "#5854b81f"},
    "dark": {"surface": "#191b24", "rail": "#151720", "ink": "#e9eaf4", "muted": "#a4a9bd", "accent": "#b3adff",
             "accent2": "#ff9cc6", "line": "#343746", "wash": "#2c2946", "green": "#8bd4b4",
             "cells": ["#242633", "#3b3768", "#5a52a8", "#8c84e6", "#b3adff"], "shadow": "#00000066"},
}
DOTS = [("#ed998f", "#d8877e"), ("#ecd09c", "#d9bc88"), ("#a7ccba", "#90b5a3")]
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
HEART = "M0 3.2C-1.6 1.8-4 .1-4-2 -4-3.4-2.9-4.4-1.7-4.4-.9-4.4-.3-4-.0-3.4.3-4 .9-4.4 1.7-4.4 2.9-4.4 4-3.4 4-2 4 .1 1.6 1.8 0 3.2z"
# Throat point of each cat frame in its 350x306 cell (niansia.github.io yuki-cat.js WEAR): where a bite lands, and
# the point frames are aligned on so switching poses does not make her jump.
CHIN = {"walkA": (283, 170), "walkB": (283, 164), "leap": (287, 225), "happy": (251, 163), "sit": (227, 141), "stand": (274, 156)}
CW = 9.0   # character advance used for textLength, so typing steps land on character boundaries in any mono font


def frame(name: str) -> str:
    return "data:image/webp;base64," + base64.b64encode((CAT / f"{name}.webp").read_bytes()).decode()


def f(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def kt(times: list[float], L: float) -> str:
    """keyTimes from seconds, clamped and strictly increasing (SMIL rejects ties)."""
    out, last = [], -1.0
    for t in times:
        k = min(1.0, max(0.0, t / L))
        if k <= last:
            k = min(1.0, last + 1e-4)
        out.append(k); last = k
    out[0], out[-1] = 0.0, 1.0
    return ";".join(f"{k:.4f}" for k in out)


def window(w: int, h: int, x: int, y: int, c: dict, title: str, right: str) -> str:
    dots = "".join(f'<circle cx="{x + 24 + i * 20}" cy="{y + 20}" r="6" fill="{a}" stroke="{b}"/>' for i, (a, b) in enumerate(DOTS))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{c["surface"]}" stroke="{c["line"]}" filter="url(#sh)"/>'
            f'<path d="M{x} {y + 40}h{w}" stroke="{c["line"]}"/>{dots}'
            f'<text x="{x + 92}" y="{y + 25}" class="t" font-size="13" fill="{c["muted"]}">{esc(title)}</text>'
            f'<text x="{x + w - 22}" y="{y + 25}" class="t" font-size="12" fill="{c["muted"]}" text-anchor="end">{esc(right)}</text>')


def typed(cid: str, x: float, y: float, text: str, t0: float, t1: float, L: float, hide: float, size: int = 15, fill: str = "", cls: str = "t") -> tuple[str, str]:
    """A line typed character by character between t0 and t1 (seconds), shown until `hide`. Returns (defs, body)."""
    n = len(text)
    times = [0.0] + [t0 + (t1 - t0) * i / n for i in range(n + 1)] + [hide, L]
    widths = [0] + [CW * i for i in range(n + 1)] + [0, 0]
    clip = (f'<clipPath id="{cid}"><rect x="{f(x - 2)}" y="{f(y - size - 2)}" height="{size + 10}" width="0">'
            f'<animate attributeName="width" dur="{f(L)}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt(times, L)}" '
            f'values="{";".join(f(v + (4 if v else 0)) for v in widths)}"/></rect></clipPath>')
    body = (f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{size}" fill="{fill}" clip-path="url(#{cid})" '
            f'textLength="{f(CW * n)}" lengthAdjust="spacingAndGlyphs">{esc(text)}</text>')
    return clip, body


def shown(t0: float, t1: float, L: float) -> str:
    """Discrete opacity: visible from t0 to t1 in every loop."""
    if t0 <= 0:
        return f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt([0, t1, L], L)}" values="1;0;0"/>'
    return f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt([0, t0, t1, L], L)}" values="0;1;0;0"/>'


def svg(w: int, h: int, c: dict, defs: str, body: str, label: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><defs><filter id="sh" x="-5%" y="-10%" width="110%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="{c["shadow"][:7]}" flood-opacity="{int(c["shadow"][7:], 16) / 255:.2f}"/></filter>{defs}</defs>'
            f'<style>.t{{font-family:{MONO};white-space:pre}}.walk{{animation:step .32s steps(1) infinite}}.walk.b{{animation-delay:-.16s}}'
            f'@keyframes step{{0%{{opacity:1}}50%{{opacity:0}}}}.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}'
            f'@media (prefers-reduced-motion:reduce){{.walk.b{{display:none}}}}</style>{body}</svg>')


# ---------------------------------------------------------------- contributions

def calendar(login: str) -> dict:
    token = os.environ.get("GITHUB_TOKEN") or subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    query = ('query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions '
             'weeks{contributionDays{date contributionCount contributionLevel weekday}}}}}}')
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": query, "variables": {"login": login}}).encode(),
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "yuki-readme"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def contributions(cal: dict, theme: str, today: str) -> str:
    c = THEMES[theme]
    W, H = 960, 336
    pitch, cell = 15, 12
    weeks = cal["weeks"]
    x0 = (W - (len(weeks) * pitch - 3)) / 2
    y0 = 134
    days = [(ci, d) for ci, wk in enumerate(weeks) for d in wk["contributionDays"]]
    total = cal["totalContributions"]
    centre = lambda ci, r: (x0 + ci * pitch + cell / 2, y0 + r * pitch + cell / 2)
    # Targets: every day with contributions, column by column, snaking down one column and up the next.
    targets = sorted([(ci, d) for ci, d in days if d["contributionCount"] > 0], key=lambda t: (t[0], t[1]["weekday"] if t[0] % 2 == 0 else -t[1]["weekday"]))

    # Timeline (seconds). The cat leaps in near the first target, trots to each one and eats it.
    T_TYPE0, T_TYPE1 = .3, 1.5
    first = centre(*((targets[0][0], targets[0][1]["weekday"]) if targets else (len(weeks) // 2, 3)))
    start = (max(x0 + 20, first[0] - 70), first[1])
    t_land = T_TYPE1 + .6
    steps, pos, t = [], start, t_land
    raw = []
    for ci, d in targets:
        p = centre(ci, d["weekday"])
        raw.append((p, min(1.1, max(.13, math.dist(pos, p) / 230)), d))
        pos = p
    walk_total = sum(r[1] + .14 for r in raw)
    squeeze = min(1.0, 15.0 / walk_total) if walk_total else 1.0      # a busy year still loops in ~25 s
    pos = start
    for p, dur, d in raw:
        t_arrive = t + dur * squeeze
        steps.append({"from": pos, "to": p, "t0": t, "t1": t_arrive, "day": d})
        t = t_arrive + .14 * squeeze
        pos = p
    if not targets:   # a quiet year: she trots across and sits down
        end = (start[0] + 200, start[1])
        steps.append({"from": start, "to": end, "t0": t, "t1": t + 1.5, "day": None}); t += 1.5; pos = end
    t_done = t + .1
    t_line1 = t_done + 2.0
    L = t_line1 + 2.6
    t_reset = L - .7

    defs, body = [], [window(W - 20, H - 20, 10, 10, c, f"{LOGIN}@home: ~/contributions", f"updated {today}")]
    clip, line = typed("cmd", 46, 86, "yuki eat --contributions --last-year", T_TYPE0, T_TYPE1, L, L, fill=c["ink"])
    body.append(f'<text x="30" y="86" class="t" font-size="15" fill="{c["accent"]}">$</text>'); defs.append(clip); body.append(line)
    # month labels
    seen = None
    for ci, wk in enumerate(weeks):
        m = wk["contributionDays"][0]["date"][:7]
        if m != seen and ci < len(weeks) - 2:
            if seen is not None or wk["contributionDays"][0]["date"][8:] <= "07":
                body.append(f'<text x="{f(x0 + ci * pitch)}" y="{y0 - 10}" class="t" font-size="10" fill="{c["muted"]}">{dt.date.fromisoformat(m + "-01").strftime("%b")}</text>')
            seen = m
    # empty slots for every day, coloured cells on top for the days she will eat
    # (full weeks as one patterned rect; the current, partial week cell by cell)
    defs.append(f'<pattern id="emp" x="{f(x0)}" y="{y0}" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse"><rect width="{cell}" height="{cell}" rx="2.5" fill="{c["cells"][0]}"/></pattern>')
    full = len(weeks) - (len(weeks[-1]["contributionDays"]) < 7)
    body.append(f'<rect x="{f(x0)}" y="{y0}" width="{full * pitch - 3}" height="{7 * pitch - 3}" fill="url(#emp)"/>')
    body.append("".join(f'<rect x="{f(x0 + ci * pitch)}" y="{f(y0 + d["weekday"] * pitch)}" width="{cell}" height="{cell}" rx="2.5" fill="{c["cells"][0]}"/>' for ci, d in days if ci >= full))
    hearts, eaten = [], 0
    counter = [(0.0, f"eaten {0:>4} / {total}", "")]
    for s in steps:
        d = s["day"]
        if not d:
            continue
        ci_x, cy = s["to"]
        te = s["t1"]
        lv = LEVELS.get(d["contributionLevel"], 1) or 1
        body.append(f'<g transform="translate({f(ci_x)} {f(cy)})"><rect x="-6" y="-6" width="{cell}" height="{cell}" rx="2.5" fill="{c["cells"][lv]}">'
                    f'<animateTransform attributeName="transform" type="scale" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt([0, te - .05, te + .06, te + .2, t_reset, L], L)}" values="1;1;1.4;0;0;1"/></rect></g>')
        hearts.append(f'<g transform="translate({f(ci_x)} {f(cy - 10)})"><path d="{HEART}" fill="{c["accent2"]}" opacity="0" transform="scale({1 + lv * .12:.2f})">'
                      f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt([0, te, te + .08, te + .7, L], L)}" values="0;0;1;0;0"/>'
                      f'<animateMotion dur="{f(L)}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="{kt([0, te, te + .7, L], L)}" calcMode="linear" path="M0 0v-22"/></path></g>')
        eaten += d["contributionCount"]
        counter.append((te, f"eaten {eaten:>4} / {total}", f'nom! {d["date"]} +{d["contributionCount"]}'))
    body += hearts

    # the cat: outer group moves (translate), inner group faces (scale ±1); the chin of the frame sits on the target
    CWd, CHd = 104, 90.9                      # display size of a 350x306 cat cell
    keys, vals, faces, fkeys = [0.0, T_TYPE1, t_land], [f"{f(start[0] - 60)} {f(start[1] - 90)}"] * 2 + [f"{f(start[0])} {f(start[1])}"], [], []
    facing = 1
    for s in steps:
        keys += [s["t0"], s["t1"]]
        vals += [f"{f(s['from'][0])} {f(s['from'][1])}", f"{f(s['to'][0])} {f(s['to'][1])}"]
        if abs(s["to"][0] - s["from"][0]) > 1:
            facing = 1 if s["to"][0] > s["from"][0] else -1
        faces.append((s["t0"], facing))
    keys += [L]; vals += [vals[-1]]
    face_k, face_v = [0.0], ["1 1"]
    for tt, fc in faces:
        if f"{fc} 1" != face_v[-1]:
            face_k.append(tt); face_v.append(f"{fc} 1")
    face_k.append(t_done); face_v.append("1 1")
    face_k.append(L); face_v.append("1 1")
    img = lambda name: f'<image href="{frame(name)}" x="{f(-CHIN[name][0] / 350 * CWd)}" y="{f(-CHIN[name][1] / 306 * CHd)}" width="{CWd}" height="{f(CHd)}"/>'
    walking = (f'<g>{shown(t_land, t_done, L)}<g class="walk">{img("walkA")}</g><g class="walk b">{img("walkB")}</g></g>')
    leaping = f'<g>{shown(0, t_land, L)}{img("leap")}</g>'
    happy = f'<g>{shown(t_done, L, L)}{img("happy")}</g>'
    body.append(f'<g><animateTransform attributeName="transform" type="translate" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt(keys, L)}" values="{";".join(vals)}"/>'
                f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt([0, T_TYPE1, T_TYPE1 + .15, t_reset, L - .1, L], L)}" values="0;0;1;1;0;0"/>'
                f'<g><animateTransform attributeName="transform" type="scale" dur="{f(L)}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt(face_k, L)}" values="{";".join(face_v)}"/>'
                f'{leaping}{walking}{happy}</g></g>')
    # happy burst
    if steps:
        hx, hy = steps[-1]["to"]
        for i, (dx, dy) in enumerate([(-20, -58), (0, -66), (20, -56)]):
            body.append(f'<path d="{HEART}" fill="{c["accent2"]}" opacity="0" transform="translate({f(hx + dx)} {f(hy + dy)}) scale(1.5)">'
                        f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt([0, t_done + i * .15, t_done + .2 + i * .15, t_reset, L], L)}" values="0;0;1;0;0"/></path>')

    # footer: counter, last bite, progress bar, legend; then the result line
    fy = y0 + 7 * pitch + 30
    for i, (t0, text, bite) in enumerate(counter):
        t1 = counter[i + 1][0] if i + 1 < len(counter) else t_reset
        body.append(f'<g>{shown(t0, t1, L)}<text x="30" y="{fy}" class="t" font-size="13" fill="{c["ink"]}">{esc(text)}</text>'
                    f'<text x="230" y="{fy}" class="t" font-size="13" fill="{c["accent2"]}">{esc(bite)}</text></g>')
    bar_w = 200
    widths = [bar_w * (int(t.split()[1]) / total if total else 0) for _, t, _ in counter]
    body.append(f'<rect x="30" y="{fy + 10}" width="{bar_w}" height="4" rx="2" fill="{c["cells"][0]}"/>'
                f'<rect x="30" y="{fy + 10}" width="0" height="4" rx="2" fill="{c["accent"]}"><animate attributeName="width" dur="{f(L)}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{kt([t for t, _, _ in counter] + [t_reset, L], L)}" values="{";".join(f(v) for v in widths)};0;0"/></rect>')
    lx = W - 40 - 5 * 15 - 70
    ly = 85   # on the command line, out of her way
    body.append(f'<text x="{lx}" y="{ly}" class="t" font-size="11" fill="{c["muted"]}">less</text>'
                + "".join(f'<rect x="{lx + 34 + i * 15}" y="{ly - 10}" width="{cell}" height="{cell}" rx="2.5" fill="{col}"/>' for i, col in enumerate(c["cells"]))
                + f'<text x="{lx + 34 + 5 * 15 + 4}" y="{ly}" class="t" font-size="11" fill="{c["muted"]}">more</text>')
    result = f"{total} contributions in the last year, all eaten. nya~ (=^･ω･^=)" if total else "a quiet year so far. sitting here waiting for commits, nya~"
    clip, line = typed("res", 46, fy + 44, result, t_done + .3, t_line1, L, t_reset, size=14, fill=c["green"])
    defs.append(clip)
    body.append(f'<text x="30" y="{fy + 44}" class="t" font-size="14" fill="{c["green"]}">{shown(t_done + .3, t_reset, L)}✓</text>{line}')
    label = f"Yuki the cat eats {LOGIN}'s GitHub contribution calendar: {total} contributions in the last year."
    return svg(W, H, c, "".join(defs), "".join(body), label)


# ---------------------------------------------------------------- contact

def contact(theme: str) -> str:
    c = THEMES[theme]
    W, H, top = 960, 384, 104
    L = 13.0
    lines = [
        ("  topics    AI safety · CV/VLM reasoning · trustworthy ML · reproducibility", c["ink"]),
        ("  together  read papers · reproduce results · design benchmarks · prototypes", c["ink"]),
        ("  promise   every mail gets read, nya", c["muted"]),
    ]
    defs, body = [], [window(W - 20, H - top - 12, 10, top, c, f"{LOGIN}@home: ~/contact", "say hello")]
    y = top + 82
    clip, line = typed("c1", 46, y, "cat collaborate.txt", .6, 1.6, L, L - .5, fill=c["ink"])
    defs.append(clip); body += [f'<text x="30" y="{y}" class="t" font-size="15" fill="{c["accent"]}">$</text>', line]
    for i, (text, col) in enumerate(lines):
        t0 = 2.0 + i * .25
        body.append(f'<text x="30" y="{y + 30 + i * 26}" class="t" font-size="14" fill="{col}" textLength="{f(len(text) * 8.4)}" lengthAdjust="spacingAndGlyphs">'
                    f'{shown(t0, L - .5, L)}{esc(text)}</text>')
    y2 = y + 30 + 3 * 26 + 14
    cmd = 'mail -s "let\'s research" niansia930202@gmail.com'
    clip, line = typed("c2", 46, y2, cmd, 3.6, 5.8, L, L - .5, fill=c["ink"])
    defs.append(clip); body += [f'<text x="30" y="{y2}" class="t" font-size="15" fill="{c["accent"]}">{shown(3.4, L - .5, L)}$</text>', line]
    # sending bar
    y3 = y2 + 28
    body.append(f'<g>{shown(6.0, L - .5, L)}<text x="30" y="{y3}" class="t" font-size="14" fill="{c["muted"]}">  sending</text>'
                f'<rect x="132" y="{y3 - 10}" width="300" height="8" rx="4" fill="{c["cells"][0]}"/>'
                f'<rect x="132" y="{y3 - 10}" width="0" height="8" rx="4" fill="{c["accent"]}"><animate attributeName="width" dur="{f(L)}s" repeatCount="indefinite" '
                f'keyTimes="{kt([0, 6.1, 7.4, L - .5, L], L)}" values="0;0;300;300;0"/></rect></g>')
    body.append(f'<text x="446" y="{y3}" class="t" font-size="14" fill="{c["green"]}">{shown(7.5, L - .5, L)}✓ delivered, talk soon (=^･ω･^=)</text>')
    # cursor parked after the last typed command until the mail is sent
    body.append(f'<rect class="cur" x="{f(46 + CW * len(cmd) + 3)}" y="{y2 - 13}" width="8" height="16" rx="1.5" fill="{c["accent"]}" opacity=".7">{shown(5.8, 7.5, L)}</rect>')
    # envelope flies from the bar to Yuki, who sits on the window's top edge
    cat_x, cat_y = W - 150, top + 1          # where her paws touch the frame
    CWd, CHd = 120, 104.9
    env = (f'<g opacity="0"><rect x="-13" y="-9" width="26" height="18" rx="3" fill="{c["surface"]}" stroke="{c["accent"]}" stroke-width="2"/>'
           f'<path d="M-12 -7 0 2 12 -7" fill="none" stroke="{c["accent"]}" stroke-width="2"/><path d="{HEART}" fill="{c["accent2"]}" transform="translate(0 3) scale(.7)"/>'
           f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt([0, 7.4, 7.5, 8.6, 8.8, L], L)}" values="0;0;1;1;0;0"/>'
           f'<animateMotion dur="{f(L)}s" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="{kt([0, 7.45, 8.7, L], L)}" calcMode="spline" keySplines="0 0 1 1;.3 0 .2 1;0 0 1 1" '
           f'path="M440 {y3 - 6}C560 {y3 - 120} {cat_x - 120} {cat_y - 40} {cat_x - 30} {cat_y - 40}"/></g>')
    img = lambda name: f'<image href="{frame(name)}" x="{f(cat_x - CHIN[name][0] / 350 * CWd)}" y="{f(cat_y - 302 / 306 * CHd)}" width="{CWd}" height="{f(CHd)}"/>'
    body.append(f'<g>{shown(0, 8.7, L)}{img("sit")}</g><g>{shown(8.7, L, L)}{img("happy")}</g>{env}')
    for i, (dx, dy) in enumerate([(34, -74), (52, -92), (70, -70)]):
        body.append(f'<path d="{HEART}" fill="{c["accent2"]}" opacity="0" transform="translate({f(cat_x + dx)} {f(cat_y + dy)}) scale(1.6)">'
                    f'<animate attributeName="opacity" dur="{f(L)}s" repeatCount="indefinite" keyTimes="{kt([0, 8.8 + i * .18, 9.0 + i * .18, 11.6, 12.0, L], L)}" values="0;0;1;1;0;0"/></path>')
    label = "A terminal types a note inviting research collaboration and mails it; Yuki the cat sits on the window and cheers when it is delivered."
    return svg(W, H, c, "".join(defs), "".join(body), label)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=["contributions", "contact"])
    ap.add_argument("--data", help="contribution calendar JSON (the GraphQL contributionCalendar object or a full response)")
    ap.add_argument("--out", help="output folder")
    ap.add_argument("--login", default=LOGIN)
    a = ap.parse_args()
    if a.what == "contributions":
        if a.data:
            raw = json.loads(Path(a.data).read_text(encoding="utf-8"))
            cal = raw.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar", raw)
        else:
            cal = calendar(a.login)
        out = Path(a.out or ROOT / "dist")
        today = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date().isoformat()
        render = lambda theme: contributions(cal, theme, today)
        name = "yuki-eats-contributions"
    else:
        out = Path(a.out or ROOT / "assets" / "readme")
        render, name = contact, "contact-terminal"
    out.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        p = out / f"{name}-{theme}.svg"
        p.write_text(render(theme), encoding="utf-8")
        print("wrote", p.relative_to(ROOT) if p.is_relative_to(ROOT) else p, f"{p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
