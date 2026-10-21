"""Build README.md, README.zh-TW.md and README.zh-CN.md from one structure so the three languages stay in sync.

Run from the repository root:
    python tools/build_readmes.py
The pictures come from tools/render_readme_assets.py (hero + project tiles) and
tools/render_yuki_svgs.py (the contribution animation). PROJECTS here is also what the tiles are rendered from.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/niansia/niansia/blob/main"
# Redrawn daily by .github/workflows/yuki-contributions.yml (tools/render_yuki_svgs.py) on the `output` branch.
CONTRIB = "https://raw.githubusercontent.com/niansia/niansia/output/yuki-eats-contributions"
FILES = {"en": "README.md", "zh-TW": "README.zh-TW.md", "zh-CN": "README.zh-CN.md"}

# Featured projects, three to a row. src: the picture in the tile's window (focus: CSS object-position of the crop).
PROJECTS = [
    {"id": "zerostel", "name": "Zerostel", "url": "https://github.com/zerostel/zerostel", "src": "assets/work/zerostel-demo.png",
     "status": "v0.1.1", "kind": "AI agents", "pitch": {
         "en": "Flight recorder for AI coding agents: every step logged, every change one undo away.",
         "zh-TW": "AI 寫程式工具的行車紀錄器：每一步都在時間軸上，改壞了一個指令就復原。",
         "zh-CN": "AI 写代码工具的行车记录仪：每一步都在时间轴上，改坏了一个命令就恢复。"}},
    {"id": "taiwan-exam", "name": "Taiwan Exam", "url": "https://github.com/niansia/taiwan-exam", "src": "assets/work/taiwan-exam-social-preview.png",
     "status": "released", "kind": "agent skill", "pitch": {
         "en": "An original AI-written GSAT mock exam, re-solved and typeset as two PDFs.",
         "zh-TW": "讓 AI 原創學測模擬考，不看答案重新解題驗算，交付題本與詳解兩份 PDF。",
         "zh-CN": "让 AI 原创学测模拟考，不看答案重新解题验算，交付题本与详解两份 PDF。"}},
    {"id": "lumigrid", "name": "LumiGrid", "url": "https://github.com/niansia/LumiGrid", "src": "assets/work/cards/lumigrid.jpg", "focus": "50% 100%",
     "status": "NTIRE 2025", "kind": "vision", "pitch": {
         "en": "Luminance-guided curve grids + NAFNet for low light: 24.57 dB on held-out NTIRE 2025 images.",
         "zh-TW": "亮度引導曲線網格加 NAFNet 的低光增強，在 NTIRE 2025 保留測試圖達 24.57 dB。",
         "zh-CN": "亮度引导曲线网格加 NAFNet 的低光增强，在 NTIRE 2025 保留测试图达 24.57 dB。"}},
    {"id": "adversarial-lab", "name": "Adversarial Lab", "url": "https://github.com/niansia/adversarial-lab", "src": "assets/work/cards/adversarial-lab.jpg",
     "status": "live demo", "kind": "AI security", "pitch": {
         "en": "FGSM and PGD attacks in your browser; adversarial training still holds 85% at ε = 0.3.",
         "zh-TW": "在瀏覽器裡發動 FGSM 與 PGD 攻擊：一般模型掉到 0%，對抗訓練仍守住 85%。",
         "zh-CN": "在浏览器里发动 FGSM 与 PGD 攻击：普通模型降到 0%，对抗训练仍守住 85%。"}},
    {"id": "kcrashlab", "name": "KCrashLab", "url": "https://github.com/niansia/KCrashLab", "src": "assets/work/cards/kcrashlab.jpg",
     "status": "simulated", "kind": "reliability", "pitch": {
         "en": "Simulation-first Windows driver reliability runs that end in independently checkable evidence.",
         "zh-TW": "模擬優先的 Windows 驅動程式可靠性實驗，最後產出可獨立驗證的證據包。",
         "zh-CN": "模拟优先的 Windows 驱动程序可靠性实验，最后产出可独立验证的证据包。"}},
    {"id": "chromarecover", "name": "ChromaRecover", "url": "https://github.com/niansia/ChromaRecover", "src": "assets/work/cards/chromarecover.jpg",
     "status": "public alpha", "kind": "vision", "pitch": {
         "en": "Local-first recovery of structure carried by subtle colour differences; abstains when unsure.",
         "zh-TW": "本機運算還原細微色差承載的空間結構，證據不足時選擇不作判定。",
         "zh-CN": "本机运算还原细微色差承载的空间结构，证据不足时选择不作判定。"}},
]

T = {
    "en": {
        "alt": "Niansia, working on AI security, computer vision and vision-language models. Yuki, a cat-eared researcher, stands beside a terminal.",
        "langs": f"[繁體中文]({REPO}/README.zh-TW.md) · [简体中文]({REPO}/README.zh-CN.md) · **English**",
        "about_h": "About",
        "about": "I work where **AI security, computer vision and vision-language models** meet, and I like turning research questions into reproducible tools: every claim should come with the evidence to check it.",
        "int": [("🛡️", "AI & multimodal security", ["robustness of multimodal AI", "adversarial and failure-mode analysis", "content integrity", "auditable evaluation"]),
                ("👁️", "Vision & multimodal intelligence", ["computer vision and VLMs", "multimodal reasoning and memory", "evaluation under real-world uncertainty", "reproducible failure analysis"])],
        "now_h": "Now",
        "now": [("✍️", "Preparing submissions to CVPR, ICCV and COLM 2027."),
                ("⏪", "**[Zerostel](https://github.com/zerostel/zerostel)**, a flight recorder and time machine for AI coding agents, public since 5 October 2026."),
                ("🚀", "**[Taiwan Exam](https://github.com/niansia/taiwan-exam)**, an Agent Skill for original GSAT practice exams, public since 28 September 2026."),
                ("🌙", "Built **[LumiGrid](https://github.com/niansia/LumiGrid)** for NTIRE 2025 low-light enhancement: +8.1 dB over the course pipeline it started from.")],
        "proj_h": "Featured projects",
        "tools_h": "Tools & activity", "tools_alt": "Python, PyTorch, OpenCV, scikit-learn, C#, .NET, React, TypeScript, Node.js, SQLite, Git",
        "lab_alt": "Yuki the cat trots over my GitHub contribution calendar and eats every day that has contributions; redrawn every day.",
    },
    "zh-TW": {
        "alt": "Niansia：研究 AI 安全、電腦視覺與視覺語言模型。穿白袍的貓耳研究員 Yuki 站在終端機旁。",
        "langs": f"**繁體中文** · [简体中文]({REPO}/README.zh-CN.md) · [English]({REPO}/README.md)",
        "about_h": "關於我",
        "about": "我的研究落在 **AI 安全、電腦視覺與視覺語言模型**的交會處，也喜歡把研究問題做成可重現的工具：每一個結論，都應該附上能檢查它的證據。",
        "int": [("🛡️", "AI 與多模態安全", ["多模態 AI 的安全性與穩健性", "對抗攻擊與失效模式分析", "內容完整性與驗證", "可信任、可稽核的評估"]),
                ("👁️", "視覺與多模態智慧", ["電腦視覺與視覺語言模型", "多模態推理與記憶", "真實世界不確定性下的評估", "可重現的失敗案例分析"])],
        "now_h": "最近在做",
        "now": [("✍️", "準備投稿 CVPR、ICCV 與 COLM 2027。"),
                ("⏪", "2026 年 10 月 5 日公開 **[Zerostel](https://github.com/zerostel/zerostel)**：AI 寫程式工具的行車紀錄器和時光機。"),
                ("🚀", "2026 年 9 月 28 日公開 **[Taiwan Exam](https://github.com/niansia/taiwan-exam)**：讓 AI 出原創學測模擬考的 Agent Skill。"),
                ("🌙", "完成 **[LumiGrid](https://github.com/niansia/LumiGrid)**（NTIRE 2025 低光影像增強），比出發點的課堂作法高 8.1 dB。")],
        "proj_h": "精選專案",
        "tools_h": "工具與足跡", "tools_alt": "Python、PyTorch、OpenCV、scikit-learn、C#、.NET、React、TypeScript、Node.js、SQLite、Git",
        "lab_alt": "Yuki 貓在我的 GitHub 貢獻月曆上小跑，把每個有貢獻的日子吃掉；每天自動更新。",
    },
    "zh-CN": {
        "alt": "Niansia：研究 AI 安全、计算机视觉与视觉语言模型。穿白大褂的猫耳研究员 Yuki 站在终端旁。",
        "langs": f"[繁體中文]({REPO}/README.zh-TW.md) · **简体中文** · [English]({REPO}/README.md)",
        "about_h": "关于我",
        "about": "我的研究落在 **AI 安全、计算机视觉与视觉语言模型**的交汇处，也喜欢把研究问题做成可复现的工具：每一个结论，都应该附上能检查它的证据。",
        "int": [("🛡️", "AI 与多模态安全", ["多模态 AI 的安全性与鲁棒性", "对抗攻击与失效模式分析", "内容完整性与验证", "可信赖、可审计的评估"]),
                ("👁️", "视觉与多模态智能", ["计算机视觉与视觉语言模型", "多模态推理与记忆", "真实世界不确定性下的评估", "可复现的失败案例分析"])],
        "now_h": "最近在做",
        "now": [("✍️", "准备投稿 CVPR、ICCV 与 COLM 2027。"),
                ("⏪", "2026 年 10 月 5 日公开 **[Zerostel](https://github.com/zerostel/zerostel)**：AI 写代码工具的行车记录仪和时光机。"),
                ("🚀", "2026 年 9 月 28 日公开 **[Taiwan Exam](https://github.com/niansia/taiwan-exam)**：让 AI 出原创学测模拟考的 Agent Skill。"),
                ("🌙", "完成 **[LumiGrid](https://github.com/niansia/LumiGrid)**（NTIRE 2025 低光图像增强），比出发点的课堂做法高 8.1 dB。")],
        "proj_h": "精选项目",
        "tools_h": "工具与足迹", "tools_alt": "Python、PyTorch、OpenCV、scikit-learn、C#、.NET、React、TypeScript、Node.js、SQLite、Git",
        "lab_alt": "Yuki 猫在我的 GitHub 贡献日历上小跑，把每个有贡献的日子吃掉；每天自动更新。",
    },
}


def picture(light: str, dark: str, alt: str, width: str) -> str:
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
            f'<img src="{light}" width="{width}" alt="{alt}"></picture>')


def build(lang: str) -> str:
    c = T[lang]
    hero = picture(f"assets/readme/hero-{lang}-light.webp", f"assets/readme/hero-{lang}-dark.webp", c["alt"], "100%")
    interests = "\n".join(f"- {icon} **{title}** · " + " · ".join(items) for icon, title, items in c["int"])
    now = "\n".join(f"- {icon} {text}" for icon, text in c["now"])
    tiles = []
    for p in PROJECTS:
        base = f"assets/readme/tiles/{p['id']}-{lang}"
        tiles.append(f'<a href="{p["url"]}">{picture(base + "-light.webp", base + "-dark.webp", p["name"] + ": " + p["pitch"][lang], "32%")}</a>')
    grid = "\n<br>\n".join("\n".join(tiles[i:i + 3]) for i in range(0, len(tiles), 3))
    return f"""<div align="center">

{hero}

<sub>{c["langs"]}</sub>

</div>

## {c["about_h"]}

{c["about"]}

{interests}

## {c["now_h"]}

{now}

## {c["proj_h"]}

<p align="center">
{grid}
</p>

## {c["tools_h"]}

<p align="center"><img src="https://skillicons.dev/icons?i=python,pytorch,opencv,sklearn,cs,dotnet,react,ts,nodejs,sqlite,git&perline=11" alt="{c["tools_alt"]}"></p>

<p align="center">{picture(CONTRIB + "-light.svg", CONTRIB + "-dark.svg", c["lab_alt"], "960")}</p>
"""


if __name__ == "__main__":
    for lang, name in FILES.items():
        (ROOT / name).write_text(build(lang), encoding="utf-8", newline="\n")
        print("wrote", name)
