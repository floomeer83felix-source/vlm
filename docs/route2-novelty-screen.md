# 路线2初步创新性与重合风险审查（2026-10-09）

> **性质：ChatGPT的公开论文页面/摘要级定向初筛，不是系统综述，更不是新机制通过或期刊创新性认证。** 必须由 VLM-BATCH-006 对最直接论文的实验设计、消融和代码进行深入检查。仍维持 **retain 0（尚无新方法）**，禁止声称“问题感知采帧”“12帧固定预算”或“鲁棒性”本身具有创新性。

## 1. 近期直接竞争与文献事实

| 代表作 | 可核实公开依据与主要贡献 | 与路线2重合及初步判定 |
|---|---|---|
| [Q-Frame, ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_Q-Frame_Query-aware_Frame_Selection_and_Multi-Resolution_Adaptation_for_Video-LLMs_ICCV_2025_paper.html) | query-aware帧选择、CLIP匹配与多分辨率预算，训练免调 | 与`S_q`及固定预算高度重合；**不能重报为新采帧器** |
| [M-LLM Based Video Frame Selection, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/html/Hu_M-LLM_Based_Video_Frame_Selection_for_Efficient_Video_Understanding_CVPR_2025_paper.html) | 以空间、时间监督学习query相关关键帧，冻结下游Video-LLM | 问题感知和效果对比已经被系统研究 |
| [Self-Adaptive Sampling, NAACL 2024](https://aclanthology.org/2024.findings-naacl.162/) | 显式比较question-aware MIF与question-agnostic MDF | `S_q`与问题无关对照并非新设想 |
| [Divide, then Ground (DIG), CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Divide_then_Ground_Adapting_Frame_Selection_to_Query_Types_for_CVPR_2026_paper.html) | 全局query偏均匀、局部query偏query-aware，依问题类型适配 | query类型效应和简单uniform比较**已研究**，新工作必须纳入类型分层强基线 |
| [Efficient Frame Selection via RL, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Qin_Efficient_Frame_Selection_for_Long_Video_Understanding_via_Reinforcement_Learning_CVPR_2026_paper.html) | 学习选帧组合价值，指出单帧query relevance可能误导 | “相似度高不一定更好”不新；不得用它包装一个未训练启发式 |
| [WFS-SB, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Wavelet-based_Frame_Selection_by_Detecting_Semantic_Boundary_for_Long_Video_CVPR_2026_paper.html) | 以多尺度语义边界+多样性分配帧 | 必须有时间结构/多样性强基线，不能只对uniform |
| [VideoStir, ACL 2026](https://aclanthology.org/2026.acl-long.1656/) | 时空图与意图相关多跳检索 | question intent、远距多帧检索和结构化记忆均不新 |
| [VideoQA in the Era of LLMs: An Empirical Study, 2024](https://arxiv.org/abs/2408.04223) | 分析视频时间推理、对抗视频扰动及题目/选项变化敏感性 | **输入/提问扰动敏感性不是空白**；路线2须核查是否已专门分离selector-only与prompt-only路径 |

更广义的主动观察、局部密采、证据覆盖、检索/结构化阅读与停止的先前重合，参见未合并的 [PR #1文献矩阵草案](https://github.com/floomeer83felix-source/vlm/blob/df892ee7a2100c632d08cc4cacd25e3aa32d12e6/docs/novelty-gap-matrix.md)。本文件只是补充并改变研究前提，不合并该PR，也不抹去其历史负结果。

## 2. 可以暂作为严格科学问题，而不是“新算法”的角度

**主角度**：在匹配12个唯一源帧预算、时间/处理器成本及来源控制时，question-conditioned采帧对正确率的配对总体效应是否稳定，是否被仅使用question-agnostic diversity或时间分层的对照解释？

**更值得检验但证据尚不足的次角度**：对有独立有效等义改写的question，将改写**只施加在选帧器**而将回答提示保持不变，是否观察到不一致；与固定帧、仅改变回答提示的prompt-only扰动相比，能否区分选择链路脆弱性与语言表达脆弱性？这属于待核实的实验设计差异，**没有证明前人未研究**。若缺合法预审等义改写，次角度不可执行；不能用模型自行生成的改写在未评估语义情况下宣称等义。

**核心否决原则**：只证明“问题感知挑帧比均匀好/差”“不同帧会改变答案”“12帧控制预算”“某些问题类型更依赖相关帧”“LLM怕文本改写”，都属于已有文献覆盖或自然效应；**不足以成为《计算机学报》级新方法**。

## 3. VLM-BATCH-006需要完成的novelty red-team

对直接相关的至少Q-Frame、NAACL2024、DIG2026、CVPR2026 RL selector、2024 empirical study **逐项阅读可访问正式方法段/消融（HTML优先）**，补充其它一至两篇必要文章。至少列：

- 该论文的明确单位（source video / frame / segment）、query如何进入selector、frame budget与真实token控制、强基线、是否直接检查选择扰动、是否区分selector-only和prompt-only、是否报告按来源独立估计；
- 该论文支持/不支持的证据级别：实际看到方法/实验/图表还是仅摘要。没看到写 UNKNOWN，不以推测标“未研究”；
- 路线2在**可观测估计量、对照干预、数据来源和技术路径**上的具体差异；如果仅换数据、换模型、换词而已，提出 **NO-GO**，不得许诺创新；
- 提供最多2个有价值但明确未证实的差异化方向（优先可证伪选择链路分离，而非新的采帧启发式）及**一票否决证据**：例如直接先例已做同一因子对照，或数据/预算无法隔离关键混杂。

不要把引用列表的长短当作创新完成度。文献初筛无法替代后续独立复核、真实数据与跨来源/模型验证。

## 4. 当前科学裁定

- **已证明“新颖”**：无。
- **可暂行定义的主要现象估计量**：question-conditioned vs time-stratified uniform的全来源配对准确率差。
- **需专门验证的新对照可能性**：selector-only query扰动 × prompt-only扰动的正交设计；目前仅是假设，且来源合法性/等义验证未知。
- **科学发布门**：先完成理论可识别性、正式数据使用许可、来源/时钟与计算公平性审查；再申请用户独立GPU预算，而非继续无界堆toy或静态备忘录。
