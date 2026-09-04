<div align="center">

# 嗨，我是 Niansia 👋

[繁體中文](https://github.com/niansia/niansia/blob/main/README.zh-TW.md) · **简体中文** · [English](https://github.com/niansia/niansia/blob/main/README.md)

### 国立阳明交通大学硕士生 · 目前休学一年

**AI 安全 × 可信赖评估 × 证据导向系统**

研究视觉与多模态智能系统的安全性、鲁棒性与推理能力。

**目前为阳明交通大学硕士生，现正休学一年。**

[个人网站](https://niansia.github.io/zh-cn/) · [研究方向](https://niansia.github.io/zh-cn/#research) · [作品集](https://niansia.github.io/zh-cn/work/) · [Email](mailto:wilbur930202@gmail.com)

</div>

## 关于我

我毕业于**元智大学（YZU）计算机科学专业**，目前就读**国立阳明交通大学（NYCU）硕士班**，现正休学一年。我的研究主要关注 **AI 安全、计算机视觉与视觉语言模型**的交叉领域，尤其是可靠的多模态推理与模型评估。

我把研究问题转化为可复现的实验与可运行的系统。目前的项目包括 [KCrashLab](https://github.com/niansia/KCrashLab)，一个用于可复现 Windows 驱动程序可靠性研究的确定性平台，以及 [ContextSec](https://github.com/niansia/ContextSec)，一个面向 AI 编程代理的产品安全决策层。

## 研究兴趣

<table>
<tr>
<td width="50%" valign="top">

### 🛡️ AI 与多模态安全

- 多模态 AI 的安全性与鲁棒性
- 对抗攻击与失效模式分析
- 内容完整性与验证
- 可信赖、可审计的评估

</td>
<td width="50%" valign="top">

### 👁️ 视觉与多模态智能

- 计算机视觉与视觉语言模型
- 多模态推理与记忆
- 真实世界不确定性下的评估
- 可复现的失败案例分析

</td>
</tr>
</table>

## 精选项目

<table>
<tr>
<td width="50%" align="center" valign="top">
<a href="https://github.com/niansia/ContextSec"><img src="assets/work/contextsec-decision-flow.svg" width="100%" alt="ContextSec 确定性产品安全决策流程"></a><br>
<strong><a href="https://github.com/niansia/ContextSec">ContextSec</a></strong><br>
<sub>研究预览阶段、面向 AI 编程代理的确定性产品安全决策层。系统从有界的代码仓库证据推导实际适用的风险包、组合跨场景控制项，并输出可验证的 Control Evaluation Ledger 与明确的发布门禁。</sub>
</td>
<td width="50%" align="center" valign="top">
<a href="https://github.com/niansia/Merriv"><img src="assets/work/merriv-release-evidence-flow.svg" width="100%" alt="Merriv 模型发布证据架构"></a><br>
<strong><a href="https://github.com/niansia/Merriv">Merriv</a></strong><br>
<sub>仍处于 pre-alpha 阶段、面向可部署 AI 模型的厂商中立发布证据层。系统将确切模型产物、配对评估、统计策略、来源信息与回归起点绑定为可移植的 Model Change Report，供模型升级前独立验证。</sub>
</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">
<a href="https://github.com/niansia/KCrashLab"><img src="assets/work/kcrashlab-evidence-flow.svg" width="100%" alt="KCrashLab 确定性崩溃研究证据流程"></a><br>
<strong><a href="https://github.com/niansia/KCrashLab">KCrashLab</a></strong><br>
<sub>已完成证据冻结的 Windows 驱动程序可靠性研究平台，涵盖规范化案例、可续跑实验、精确失效签名、触发条件最小化、3/3 模拟重放与语义证据验证，并明确区分模拟证据与受控的 Windows lab 路径。</sub>
</td>
<td width="50%" align="center" valign="top">
<a href="https://github.com/niansia/ChromaRecover"><img src="assets/work/chromarecover-architecture.png" width="100%" alt="ChromaRecover 证据优先的计算机视觉架构"></a><br>
<strong><a href="https://github.com/niansia/ChromaRecover">ChromaRecover</a></strong><br>
<sub>实验性 public alpha、以本地运行为核心的 Python 计算机视觉工具，用于恢复由细微色彩差异承载的空间结构。系统会比较多种色彩证据假设、保留可审计产物，并在证据不足时选择不作判断。</sub>
</td>
</tr>
</table>

## 使用工具

`Python` · `PyTorch` · `OpenCV` · `scikit-learn` · `Jupyter` · `C# / .NET` · `React` · `TypeScript` · `Node.js` · `SQLite` · `Git`

## 联系与合作

> **想一起研究吗？**
>
> 如果你也对 **AI 安全、CV／VLM 推理、可信赖机器学习、实验复现或研究工具**感兴趣，欢迎来找我聊聊研究构想、数据集与模型失效案例喵
>
> 不论是一起读 paper、复现实验、设计 benchmark、分析不寻常的模型结果，还是把一个仍然模糊的想法慢慢做成可以运行、可以验证的 prototype，我都很乐意参与喵
>
> 如果你正在寻找研究伙伴、有跨领域问题想讨论，或刚好发现值得深入研究的 dataset、evaluation setting 或 failure case，也都可以发邮件给我喵
>
> 联系邮箱是 **[wilbur930202@gmail.com](mailto:wilbur930202@gmail.com)**，我可能无法每次都立刻回复，但看到后一定会认真阅读喵
>
> 也期待认识愿意一起把问题想深、把实验做扎实，并把研究过程整理得更可复现的人喵
>
> `(=^･ω･^=)`
