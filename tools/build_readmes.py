"""Build README.md, README.zh-TW.md and README.zh-CN.md from one structure so the three languages stay in sync.

Run from the repository root:
    python tools/build_readmes.py
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "niansia930202@gmail.com"
REPO = "https://github.com/niansia/niansia/blob/main"
FILES = {"en": "README.md", "zh-TW": "README.zh-TW.md", "zh-CN": "README.zh-CN.md"}
SITE = {"en": "https://niansia.github.io/", "zh-TW": "https://niansia.github.io/zh-tw/", "zh-CN": "https://niansia.github.io/zh-cn/"}


def badge(label: str, message: str, color: str, logo: str) -> str:
    esc = lambda s: quote(s.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="")
    return f"https://img.shields.io/badge/{esc(label)}-{esc(message)}-{color}?style=for-the-badge&logo={logo}&logoColor=white"


PROJECTS = [
    # id, url, image, {lang: (tags, description)}
    ("Taiwan Exam", "https://github.com/niansia/taiwan-exam", "assets/work/taiwan-exam-social-preview.png", {
        "en": (["Agent Skill", "GSAT · 7 subjects"], "Has an AI write an original GSAT practice exam, re-solve every item without the answer, and stamp it onto the original exam templates as a question PDF and a worked-solution PDF."),
        "zh-TW": (["Agent Skill", "學測七科"], "讓 AI 原創一份學測模擬考：不看答案重新解題驗算、依官方答對率控制難度，再套用大考中心原始模板，交付題本與詳解兩份 PDF。"),
        "zh-CN": (["Agent Skill", "学测七科"], "让 AI 原创一份学测模拟考：不看答案重新解题验算、依官方答对率控制难度，再套用大考中心原始模板，交付题本与详解两份 PDF。")}),
    ("LumiGrid", "https://github.com/niansia/LumiGrid", "assets/work/cards/lumigrid.jpg", {
        "en": (["Computer vision", "NTIRE 2025"], "Low-light enhancement with a luminance-guided bilateral grid of Zero-DCE curves and a NAFNet refiner. 24.57 dB / 0.840 SSIM on 20 held-out NTIRE 2025 pairs, trained on one laptop GPU."),
        "zh-TW": (["電腦視覺", "NTIRE 2025"], "以亮度引導的 Zero-DCE 曲線雙邊網格加上 NAFNet 細修的低光影像增強。在 20 組保留的 NTIRE 2025 測試圖上達 24.57 dB / SSIM 0.840，只用一張筆電 GPU 訓練。"),
        "zh-CN": (["计算机视觉", "NTIRE 2025"], "以亮度引导的 Zero-DCE 曲线双边网格加上 NAFNet 细修的低光图像增强。在 20 组保留的 NTIRE 2025 测试图上达到 24.57 dB / SSIM 0.840，只用一张笔记本 GPU 训练。")}),
    ("KCrashLab", "https://github.com/niansia/KCrashLab", "assets/work/cards/kcrashlab.jpg", {
        "en": (["Systems reliability", "Evidence freeze"], "A simulation-first platform for deterministic, reproducible Windows driver reliability experiments: canonical cases, resumable campaigns, exact failure signatures and independently verifiable evidence."),
        "zh-TW": (["系統可靠性", "證據凍結"], "以模擬為優先的 Windows 驅動程式可靠性研究平台：標準化案例、可續跑實驗、精確失效簽章，並產生可獨立驗證的證據包。"),
        "zh-CN": (["系统可靠性", "证据冻结"], "以模拟为优先的 Windows 驱动程序可靠性研究平台：规范化案例、可续跑实验、精确失效签名，并生成可独立验证的证据包。")}),
    ("Merriv", "https://github.com/niansia/Merriv", "assets/work/cards/merriv.jpg", {
        "en": (["Model release", "Pre-alpha"], "A vendor-neutral release-evidence layer for deployable AI models that binds exact artifacts, paired evaluation, statistical policy and provenance into a portable Model Change Report."),
        "zh-TW": (["模型發布", "Pre-alpha"], "面向可部署 AI 模型的廠商中立發布證據層，把確切模型產物、配對評估、統計政策與來源資訊綁定成可攜式 Model Change Report。"),
        "zh-CN": (["模型发布", "Pre-alpha"], "面向可部署 AI 模型的厂商中立发布证据层，把确切模型产物、配对评估、统计策略与来源信息绑定成可移植的 Model Change Report。")}),
    ("ChromaRecover", "https://github.com/niansia/ChromaRecover", "assets/work/cards/chromarecover.jpg", {
        "en": (["Computer vision", "Public alpha"], "A local-first toolkit that recovers spatial structure carried by subtle colour differences, tests competing hypotheses, keeps auditable artifacts and abstains when evidence is weak."),
        "zh-TW": (["電腦視覺", "Public alpha"], "以本機運算為核心的電腦視覺工具，還原由細微色彩差異承載的空間結構；比較多種假設、保留可稽核產物，證據不足時選擇不作判定。"),
        "zh-CN": (["计算机视觉", "Public alpha"], "以本地运行为核心的计算机视觉工具，恢复由细微色彩差异承载的空间结构；比较多种假设、保留可审计产物，证据不足时选择不作判断。")}),
    ("NoveltyAudit", "https://github.com/niansia/NoveltyAudit", "assets/work/cards/noveltyaudit.jpg", {
        "en": (["Scholarly reasoning", "Alpha"], "An evidence-first Agent Skill for adversarial novelty audits: it freezes claims before retrieval, finds Minimal Prior Sets, applies historical cutoffs and records what the search could not establish."),
        "zh-TW": (["學術推理", "Alpha"], "以證據為優先的學術新穎性對抗審查 Agent Skill：檢索前凍結主張、找出 Minimal Prior Sets、套用歷史時間截點，並記錄搜尋未能建立的部分。"),
        "zh-CN": (["学术推理", "Alpha"], "以证据为优先的学术新颖性对抗审查 Agent Skill：检索前冻结主张、找出 Minimal Prior Sets、应用历史时间截点，并记录搜索未能建立的部分。")}),
]

T = {
    "en": {
        "alt": "Niansia: M.S. student in Computer Science at NYCU, working on AI security, computer vision and vision-language models",
        "langs": f"[繁體中文]({REPO}/README.zh-TW.md) · [简体中文]({REPO}/README.zh-CN.md) · **English**",
        "badges": [("Website", "niansia.github.io", "c0673a", "githubpages", ""), ("Research", "AI Security · CV · VLM", "8f6bb3", "googlescholar", "#research"), ("Portfolio", "10 projects", "3f9b74", "files", "work/")],
        "email": "Email",
        "tagline": "Researching the security, robustness and reasoning of visual and multimodal AI,<br>and turning research questions into tools whose evidence can be checked and reproduced.",
        "about_h": "About", "about": [
            "I studied Computer Science at **Yuan Ze University (YZU)** and am an M.S. student in Computer Science at **National Yang Ming Chiao Tung University (NYCU)**, currently on a one-year leave. I work where **AI security, computer vision and vision-language models** meet, with a focus on reliable multimodal reasoning and evaluation.",
            "I like to turn research questions and practical needs into reproducible tools: each claim should come with the evidence to check it."],
        "now_h": "Now", "now": [
            ("✍️", "Preparing submissions to **CVPR 2027** (VLM-related), **ICCV 2027** (DiT-related) and **COLM 2027**."),
            ("🚀", "**[Taiwan Exam](https://github.com/niansia/taiwan-exam)**, an Agent Skill for original GSAT practice exams, public since 28 September 2026."),
            ("🌙", "Built **[LumiGrid](https://github.com/niansia/LumiGrid)** for NTIRE 2025 low-light enhancement: +8.1 dB over the course pipeline it started from."),
            ("🎓", "On a one-year leave from the NYCU master's program.")],
        "int_h": "Research interests",
        "int": [("🛡️ AI & multimodal security", ["Security and robustness of multimodal AI", "Adversarial and failure-mode analysis", "Content integrity and verification", "Trustworthy, auditable evaluation"]),
                ("👁️ Vision & multimodal intelligence", ["Computer vision and vision-language models", "Multimodal reasoning and memory", "Evaluation under real-world uncertainty", "Reproducible failure analysis"])],
        "proj_h": "Featured projects", "more": "All projects and interactive demos →",
        "tools_h": "Tools", "tools_alt": "Python, PyTorch, OpenCV, scikit-learn, C#, .NET, React, TypeScript, Node.js, SQLite, Git",
        "lab_alt": "A snail-hooded cat types at a research terminal while evidence checks and a small pipeline light up.",
        "contact_h": "Contact",
        "contact": f"I welcome thoughtful conversations about AI security, CV / VLM reasoning, trustworthy machine learning, reproducibility and research tooling, whether that is reading papers together, reproducing a result, designing a benchmark or turning a rough idea into a prototype that can be checked.\n\n📮 **[{EMAIL}](mailto:{EMAIL})**",
        "signal_alt": "A small signal travels along a circuit path into an envelope, inviting research conversations.",
    },
    "zh-TW": {
        "alt": "Niansia：陽明交大資工碩士生，研究 AI 安全、電腦視覺與視覺語言模型",
        "langs": f"**繁體中文** · [简体中文]({REPO}/README.zh-CN.md) · [English]({REPO}/README.md)",
        "badges": [("個人網站", "niansia.github.io", "c0673a", "githubpages", ""), ("研究方向", "AI 安全 · CV · VLM", "8f6bb3", "googlescholar", "#research"), ("作品集", "10 個專案", "3f9b74", "files", "work/")],
        "email": "Email",
        "tagline": "研究視覺與多模態 AI 的安全性、穩健性與推理能力，<br>並把研究問題做成證據可以被檢查、也能被重現的工具。",
        "about_h": "關於我", "about": [
            "我畢業於**元智大學（YZU）資訊工程學系**，目前是**國立陽明交通大學（NYCU）資訊工程碩士生**，現正休學一年。研究主要落在 **AI 安全、電腦視覺與視覺語言模型**的交會處，特別關注可靠的多模態推理與模型評估。",
            "我喜歡把研究問題和實際需求做成可重現的工具：每一個結論，都應該附上能檢查它的證據。"],
        "now_h": "最近在做", "now": [
            ("✍️", "準備投稿 **CVPR 2027**（VLM 相關）、**ICCV 2027**（DiT 相關）與 **COLM 2027**。"),
            ("🚀", "2026 年 9 月 28 日正式公開 **[Taiwan Exam](https://github.com/niansia/taiwan-exam)**：讓 AI 出原創學測模擬考的 Agent Skill。"),
            ("🌙", "完成 **[LumiGrid](https://github.com/niansia/LumiGrid)**（NTIRE 2025 低光影像增強），比出發點的課堂作法高 8.1 dB。"),
            ("🎓", "陽明交大碩士班休學一年中。")],
        "int_h": "研究興趣",
        "int": [("🛡️ AI 與多模態安全", ["多模態 AI 的安全性與穩健性", "對抗攻擊與失效模式分析", "內容完整性與驗證", "可信任、可稽核的評估"]),
                ("👁️ 視覺與多模態智慧", ["電腦視覺與視覺語言模型", "多模態推理與記憶", "真實世界不確定性下的評估", "可重現的失敗案例分析"])],
        "proj_h": "精選專案", "more": "全部作品與互動展示 →",
        "tools_h": "使用工具", "tools_alt": "Python、PyTorch、OpenCV、scikit-learn、C#、.NET、React、TypeScript、Node.js、SQLite、Git",
        "lab_alt": "戴蝸牛帽的小貓在研究終端機前打字，旁邊的證據檢查與流程節點輪流亮起。",
        "contact_h": "聯絡與合作",
        "contact": "\n".join([
            "> **想一起研究嗎？**", ">",
            "> 如果你也對 **AI 安全、CV／VLM 推理、可信任機器學習、實驗重現或研究工具**有興趣，歡迎來找我聊聊研究構想、資料集與模型失效案例喵", ">",
            "> 不論是一起讀 paper、重現實驗、設計 benchmark、分析不尋常的模型結果，或把一個還很模糊的想法慢慢做成可運作、可驗證的 prototype，我都很樂意參與喵", ">",
            "> 如果你正在尋找研究夥伴、有跨領域題目想討論，或剛好發現值得深入研究的 dataset、evaluation setting 或 failure case，也都可以寄信給我喵", ">",
            f"> 聯絡信箱是 **[{EMAIL}](mailto:{EMAIL})**，我可能無法每次都立刻回覆，但有看到就會認真閱讀喵", ">",
            "> 也期待遇見願意一起把問題想深、把實驗做紮實，並把研究過程整理得更可重現的人喵", ">",
            "> `(=^･ω･^=)`"]),
        "signal_alt": "小訊號沿著電路線移動，最後送進信封，邀請交流研究。",
    },
    "zh-CN": {
        "alt": "Niansia：阳明交大资工硕士生，研究 AI 安全、计算机视觉与视觉语言模型",
        "langs": f"[繁體中文]({REPO}/README.zh-TW.md) · **简体中文** · [English]({REPO}/README.md)",
        "badges": [("个人网站", "niansia.github.io", "c0673a", "githubpages", ""), ("研究方向", "AI 安全 · CV · VLM", "8f6bb3", "googlescholar", "#research"), ("作品集", "10 个项目", "3f9b74", "files", "work/")],
        "email": "Email",
        "tagline": "研究视觉与多模态 AI 的安全性、鲁棒性与推理能力，<br>并把研究问题做成证据可以被检查、也能被复现的工具。",
        "about_h": "关于我", "about": [
            "我毕业于**元智大学（YZU）资讯工程学系**，目前是**阳明交通大学（NYCU）资讯工程硕士生**，现正休学一年。研究主要落在 **AI 安全、计算机视觉与视觉语言模型**的交汇处，特别关注可靠的多模态推理与模型评估。",
            "我喜欢把研究问题和实际需求做成可复现的工具：每一个结论，都应该附上能检查它的证据。"],
        "now_h": "最近在做", "now": [
            ("✍️", "准备投稿 **CVPR 2027**（VLM 相关）、**ICCV 2027**（DiT 相关）与 **COLM 2027**。"),
            ("🚀", "2026 年 9 月 28 日正式公开 **[Taiwan Exam](https://github.com/niansia/taiwan-exam)**：让 AI 出原创学测模拟考的 Agent Skill。"),
            ("🌙", "完成 **[LumiGrid](https://github.com/niansia/LumiGrid)**（NTIRE 2025 低光图像增强），比出发点的课堂做法高 8.1 dB。"),
            ("🎓", "阳明交大硕士班休学一年中。")],
        "int_h": "研究兴趣",
        "int": [("🛡️ AI 与多模态安全", ["多模态 AI 的安全性与鲁棒性", "对抗攻击与失效模式分析", "内容完整性与验证", "可信赖、可审计的评估"]),
                ("👁️ 视觉与多模态智能", ["计算机视觉与视觉语言模型", "多模态推理与记忆", "真实世界不确定性下的评估", "可复现的失败案例分析"])],
        "proj_h": "精选项目", "more": "全部作品与互动展示 →",
        "tools_h": "使用工具", "tools_alt": "Python、PyTorch、OpenCV、scikit-learn、C#、.NET、React、TypeScript、Node.js、SQLite、Git",
        "lab_alt": "戴蜗牛帽的小猫在研究终端前打字，旁边的证据检查与流程节点轮流亮起。",
        "contact_h": "联系与合作",
        "contact": "\n".join([
            "> **想一起研究吗？**", ">",
            "> 如果你也对 **AI 安全、CV／VLM 推理、可信赖机器学习、实验复现或研究工具**感兴趣，欢迎来找我聊聊研究构想、数据集与模型失效案例喵", ">",
            "> 不论是一起读 paper、复现实验、设计 benchmark、分析不寻常的模型结果，还是把一个仍然模糊的想法慢慢做成可以运行、可以验证的 prototype，我都很乐意参与喵", ">",
            "> 如果你正在寻找研究伙伴、有跨领域问题想讨论，或刚好发现值得深入研究的 dataset、evaluation setting 或 failure case，也都可以发邮件给我喵", ">",
            f"> 联系邮箱是 **[{EMAIL}](mailto:{EMAIL})**，我可能无法每次都立刻回复，但看到后一定会认真阅读喵", ">",
            "> 也期待认识愿意一起把问题想深、把实验做扎实，并把研究过程整理得更可复现的人喵", ">",
            "> `(=^･ω･^=)`"]),
        "signal_alt": "小信号沿电路线移动，最后送进信封，邀请交流研究。",
    },
}


def build(lang: str) -> str:
    c, site = T[lang], SITE[lang]
    badges = [f'<a href="{site}{path}"><img src="{badge(label, msg, color, logo)}" alt="{label}: {msg}"></a>' for label, msg, color, logo, path in c["badges"]]
    badges.append(f'<a href="mailto:{EMAIL}"><img src="{badge(c["email"], EMAIL, "2a2230", "gmail")}" alt="Email: {EMAIL}"></a>')
    cover = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/readme/cover-{lang}-dark.jpg">\n'
             f'  <img src="assets/readme/cover-{lang}-light.jpg" width="100%" alt="{c["alt"]}">\n</picture>')
    now = "\n".join(f"- {icon} {text}" for icon, text in c["now"])
    interests = "".join(
        f'<td width="50%" valign="top">\n\n### {title}\n\n' + "\n".join(f"- {x}" for x in items) + "\n\n</td>\n" for title, items in c["int"])
    cells = []
    for name, url, img, text in PROJECTS:
        tags, desc = text[lang]
        cells.append(f'<td width="50%" valign="top">\n<a href="{url}"><img src="{img}" width="100%" alt="{name}"></a>\n\n'
                     f'**[{name}]({url})** &nbsp;{" ".join(f"<code>{t}</code>" for t in tags)}\n\n<sub>{desc}</sub>\n</td>')
    rows = "".join(f"<tr>\n{cells[i]}\n{cells[i + 1]}\n</tr>\n" for i in range(0, len(cells), 2))
    return f"""<div align="center">

{cover}

{c["langs"]}

{" ".join(badges)}

<sub>{c["tagline"]}</sub>

</div>

## {c["about_h"]}

{c["about"][0]}

{c["about"][1]}

## {c["now_h"]}

{now}

## {c["int_h"]}

<table width="100%">
<tr>
{interests}</tr>
</table>

## {c["proj_h"]}

<table width="100%">
{rows}</table>

<p align="right"><a href="{site}work/">{c["more"]}</a></p>

## {c["tools_h"]}

<p align="center"><img src="https://skillicons.dev/icons?i=python,pytorch,opencv,sklearn,cs,dotnet,react,ts,nodejs,sqlite,git&perline=11" alt="{c["tools_alt"]}"></p>

<p align="center"><img src="assets/readme/research-lab.gif" width="960" alt="{c["lab_alt"]}"></p>

## {c["contact_h"]}

{c["contact"]}

<p align="center"><img src="assets/readme/contact-signal.gif" width="960" alt="{c["signal_alt"]}"></p>
"""


if __name__ == "__main__":
    for lang, name in FILES.items():
        (ROOT / name).write_text(build(lang), encoding="utf-8", newline="\n")
        print("wrote", name)
