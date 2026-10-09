# 方向B：长视频VLM核心机制的重新立题与否决门（科学负责人草案）

> 日期：2026-10-09（北京时间）｜状态：**MECHANISM EXPLORATION / RETAIN 0 / NO GPU**。用户已明确选择原 VLM-DECISION-007 的 **B：保持长视频VLM高水平论文目标、放弃把已有问题相关采帧当新算法**。本文是待证伪的候选集与机制识别计划，不是论文创新性、性能提升或正式实验授权。

## 0. 为什么再次转向

历史负结果可复核概述：[2026-10-08快照](./research-progress-2026-10-08.md)、[BATCH-006创新审查](./codex-artifacts/VLM-BATCH-006/novelty-and-identifiability.md)及[否决记录](./codex-artifacts/VLM-BATCH-006/scientific-decision.md)。截至本轮**retain 0**。已否决/高度重合：query-aware vs uniform采帧、SigLIP/MMR重排行、简单 Evidence Memory、迭代补看/停止、zoom、原生帧融合GAP7、第二模型路由、一般事件图/验证代理。旧20个操作性源与可访问toy不证明跨源改善。新方向必须改变**可证明的计算状态、更新规则或可识别的科学问题**，而非把旧采样/检索替换成一个新词。

公开先例强烈限制候选范围（以下为科学负责人**官网/正式论文摘要级初筛**，并非完整novelty clearance；Codex需要做方法层核验）：

- [NeuS-QA, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/37834)：问题翻译为时序逻辑，视频自动机+model checking，找logic-verified segments；所以**“首次时序逻辑检验/事件自动机”已不成立**。
- [VideoHV-Agent, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Think_Then_Verify_A_Hypothesis-Verification_Multi-Agent_Framework_for_Long_Video_CVPR_2026_paper.html)：先拟答案假设、用discriminative clue验证后回答；所以**“先假设再查证”已不成立**。
- [VideoSEAL, ICML 2026](https://proceedings.mlr.press/v306/qiu26v.html)：分离规划与answer authority并以pixel inspection门控，专门研究correct-but-ungrounded；所以**“分开规划与核验、最终答案必须有证据”已不成立**。
- [Open-o3-Video, ICML 2026](https://proceedings.mlr.press/v306/meng26e.html)、[Seeing Is Believing, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38031)：显式时空证据grounding已有强先例。
- [ENTER (2025/2026)](https://arxiv.org/abs/2501.14194)、[Semantic Event Graphs (2026)](https://arxiv.org/abs/2601.06097)、[VideoStir, ACL 2026](https://aclanthology.org/2026.acl-long.1656/)：一般事件图、结构化memory、多跳视频查询高度重合。
- [CVPR2025 temporal consistency](https://openaccess.thecvf.com/content/CVPR2025/html/Jung_On_the_Consistency_of_Video_Large_Language_Models_in_Temporal_CVPR_2025_paper.html)：时序grounding一致性probe和verification tuning已有先例。
- [PACE, 2026](https://arxiv.org/abs/2608.26355)、[TRACE, 2026](https://arxiv.org/abs/2608.22516)：判别式证据线索、已访问证据核查和停止亦非空白。

注意：这些引用不能证明下述**精确定义**无人提出；无直接先例仅为UNKNOWN，不是PASS。

## 1. 三个刻意区分的竞争机制候选（不是一起做）

| ID | 核心对象/可观察承诺 | 最强直接先例风险与一票否决 | 必须构造的反例 |
|---|---|---|---|
| **M1：开放世界的负证据债务账本** | 对「从未发生、只有A做过、A之前没有B」等负性/排他性断言，维护已观察时间段、未知未观察段、探测器假阴性上界及尚欠的观察义务，输出 TRUE/FALSE/UNKNOWN（或带假设的风险界）。只对**明确穷尽观察且完备探测的受限域**才可能给“未发生”结论。 | NeuS-QA时序逻辑、VideoSEAL grounding、经典三值时序/监控与选择性预测；若等价逻辑/unknown域及证明义务已是已知直接做法，只能复现。不能声称稀疏看12帧就可证明负事实。 | 两个底层真实视频世界在已看帧完全相同但未看间隔中事件不同，任何仅看这些帧的系统都不能可靠判定负事实。 |
| **M2：带来源依赖的可撤销事件断言** | 视频证据事件作为带版本、可见性、来源及观测置信边界的依赖节点。新证据与旧证据冲突时，仅撤销**受该证据依赖的答案子结论**，未受影响的结论保持稳定，输出可审计的revision trace而非笼统重问。 | 经典Truth Maintenance Systems、Event Graph/VideoStir、VideoSEAL和verification-agent；若只是普通依赖图+缓存失效/反证重跑，NO-GO。必须有视觉时间/源约束的不可替代差异。 | 有共享来源、相互矛盾的观察和不相干结论：新证据反证时哪些结论应被撤销，哪些绝不可被洗白或无端撤销？ |
| **M3：候选答案间不可区分集的证据义务** | 不直接选下一帧，而定义一组当前观测下仍一致的可行答案假设，识别它们的**可区别谓词、未验证依赖和不可识别区间**；只有在明确条件下才生成可审计的证据义务，不把类似clue当答案真值，也不宣称停止保证。 | VideoHV-Agent/ PACE的discriminative clue、NeuS-QA逻辑检查、TRACE evidence bundle。若仅换名“答案对比线索”，立即NO-GO。 | 两个候选答案在当前观察下都成立；某下一观察能够区分、某个只与话题相关的观察无法区分；若所有合法观察都不能区分则显式UNKNOWN。 |

**重要限制**：上述只是**三个互斥的研究线索**，不可合成“事件图+三值逻辑+代理”后声称新机制。Codex任务先各自形式化并与最接近的同类模型做逐条对照，**可以淘汰三个、保留零个**。M1目前的理论负例可最清楚地陈述，但经典open-world监控/认识逻辑重合风险很高；不是默认赢家。M2/M3亦有强先例，所有创新声明均HOLD。

## 2. 否决式科学计划：不靠“合成PASS”保证创新

### 建模与可识别性

- 每候选明确状态空间 `O`（观测片段/真实PTS/typed媒体版本/来源及视野范围）、未观测集合 `U`、允许的答案/事件谓词 `H`、更新算子 `T`、合法输入、返回 `CERTIFIED_UNDER_ASSUMPTIONS / REFUTED / UNKNOWN` 的充分条件。
- **形式安全性**只能在明确公理（完备感知器、覆盖所有相关时间/视野、可信观测与时钟）下成立；没有公理时证明弱得多的「不知道就不强行判」不变量。绝不推出真实VLM perception满足这些公理。
- 非对称性：看见一次事件在一定条件下能反驳“从未发生”；没有看见一次事件在稀疏观测下**不能**支持其否定，且相机外、遮挡、截断、VFR/时间偏移可能使视觉证据本身UNKNOWN。
- 形式陈述必须有最小**正例、反例、退化/平凡基线**：如恒输出UNKNOWN虽无假肯定但不可用；只做full-video scan不是12帧可部署预算。对每个候选要求至少一个与强基线可产生不同可验证行为的条件，若不存在或只能更换命名则淘汰。

### 可检验指标与统计约束（未来，不是本批实验）

在用户另行授权、取得合法数据且有真实感知证据后才允许用：未支持断言率、错误自信率/覆盖风险曲线、可撤销更新的局部性与错误保持率、区分义务命中率、正确率—拒绝率—全部真实耗时成本；纯合成可以验证算法逻辑但不能替代现实感知可靠性。统计单位仍是**独立来源组**，QA标准答案及来源保护集不得进入候选选择过程。与NeuS-QA、VideoSEAL、VideoHV等**机制匹配**强对照，而非仅uniform。

### 硬约束与唯一权限

本次只建立[**VLM-BATCH-007（十项无GPU研究包）**](./codex-artifacts/VLM-BATCH-007/README.md)。不跑视频、模型、QA、训练，不改既有Windows实验目录/conda/CUDA/锁/账本，不联系外部作者，不下载新数据/媒体，不合并PR。阅读有限官方文献/公开代码片段与本地小量静态接口仅为确认候选是否具有可实现差异；若许可、新颖性或数据缺口阻断，按**UNKNOWN/NO-GO**回报。

**成功条件**不是出现好看的toy数字，而是有一条可检验、未被直接先例消解的结构性命题，配有不变量、反例、可构造的独立实证数据与强基线，且仍需通过ChatGPT再审。否则**RETAIN 0、停止这一候选集**，不得生成新循环任务。
