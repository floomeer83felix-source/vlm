# 文献重合与创新空间矩阵（2026-10-08）

性质：**截至2026-10-08的定向文献审查**，不是系统综述、不是已批准的算法创新性证书。只根据可见论文摘要、论文/项目主页及公开仓库描述做保守判断；必要时须阅读全文核对方法与实验。

## 1. 研究状态

基于 [原始进展](./research-progress-2026-10-08.md)，旧“检索关键帧 + Evidence Memory + 自适应补看”及随后有限候选均未达到收益和创新门槛，结论为 retain 0。当前研究仓库公开的是汇总，无法访问六份本地审计/评分材料，因此**不声称独立复算历史效应或已证明语义原因**。

## 2. 主要直接重合工作

| 研究 / 公开年份 / 资料 | 已发表或公开的主要机制/贡献（摘要级） | 与本项目候选的重合 | 本轮处置 |
|---|---|---|---|
| [A.I.R., ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1332893b662f655660c9abdf793230cf-Abstract-Conference.html) | 无训练、适应性迭代选帧，VLM语义分析与低成本候选筛选 | 主动迭代取帧 | 迭代取帧本身不可作为新贡献 |
| [Active Video Perception, CVPR 2026 Findings](https://openaccess.thecvf.com/content/CVPR2026F/html/Wang_Active_Video_Perception_Iterative_Evidence_Seeking_for_Agentic_Long_Video_CVPRF_2026_paper.html) | plan–observe–reflect；时戳证据、充分性反思与停止 | 关键帧/补看/何时停止 | 原组合重合高度明显 |
| [LensWalk, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Li_LensWalk_Agentic_Video_Understanding_by_Planning_How_You_See_in_CVPR_2026_paper.html) | 由代理调控观察范围和采样密度 | 局部密采 / 区间补看 | 不将时间范围调控单独称创新 |
| [LongVT, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_LongVT_Incentivizing_Thinking_with_Long_Videos_via_Native_Tool_Calling_CVPR_2026_paper.html) | 原生裁剪视频与全局—局部多轮工具调用 | zoom / 再观察 | 旧策略再次大规模复测不合理 |
| [EcoFrame, arXiv:2608.03918](https://arxiv.org/abs/2608.03918) | 输出不确定性驱动预算扩展，注意力引导补帧 | 停止规则 / 不确定性门控 | 朴素熵门控不足以新颖 |
| [TRACE + VES-Bench, arXiv:2608.22516](https://arxiv.org/abs/2608.22516) | 注释必需事件区间的实采帧覆盖审计；证据束递增与稳定停止 | 证据覆盖核验、停止 | “看见全部必需区间”是已有测量/方法主题 |
| [PACE, arXiv:2608.26355](https://arxiv.org/abs/2608.26355) | question factors + option-discriminative cues 检索 | 关系/选项引导检索 | 对比判别式检索不是空白 |
| [VideoHV-Agent, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Think_Then_Verify_A_Hypothesis-Verification_Multi-Agent_Framework_for_Long_Video_CVPR_2026_paper.html) | 为答案候选生成验证假设与判别线索，局部观察再回答 | 验证式补看/判断 | 不能单靠“验证而非检索”的叙述 |
| [HERBench, CVPR 2026](https://herbench.github.io/) | 每题多段分散证据；区分检索不足与融合不足；MRFS | 新计划“区分有没有看到/能否融合” | **诊断问题已被明确研究过**，只能作为起点 |
| [CaST-Bench, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_CaST-Bench_Benchmarking_Causal_Chain-Grounded_Spatio-Temporal_Reasoning_for_Video_Question_Answering_CVPR_2026_paper.html) | 标有时空区间和对象轨迹的因果链 QA 测量 | 多事件链显式可验证性 | “证据因果链”不能直接宣称新 |
| [TOC-Bench, arXiv:2605.09904](https://arxiv.org/abs/2605.09904) | 面向实体轨迹及事件时间线的时序对象一致性测评 | 身份绑定、事件一致性 | 本方向已有专门基准 |
| [VideoStir, ACL 2026](https://aclanthology.org/2026.acl-long.1656/) | 时空图组织、意图感知与多跳视频检索 | 结构化 Evidence Memory、远距关系推理 | 仅提“构图+多跳检索”不足以创新 |
| [Thinking with Drafts / SpecTemp, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Hu_Thinking_with_Drafts_Speculative_Temporal_Reasoning_for_Efficient_Long_Video_CVPR_2026_paper.html) | 轻量草稿模型与目标模型验证、时间推理协作 | 本地第二阅读者 / 双模型路由 | 类似双模型路由方向已有重合 |

## 3. 数据资源初筛（**没有下载或验证媒体**）

| 资源 | 可见证据 | 选择风险 | 当前决策 |
|---|---|---|---|
| [HERBench 项目代码](https://github.com/DanBenAmi/HERBench) / [HF 数据](https://huggingface.co/datasets/DanBenAmi/HERBench) | 面向多证据融合；公开仓库报告 lite_v2 为 **1971题/68视频**，媒体 Lite 约35GB、Full约161GB；包含关键帧/参考集合相关研究协议 | 容量不小；模型原生评测配置为 Qwen2.5-VL 和 InternVL3.5，项目所用 Qwen3-VL-4B 需要适配；须查具体注释字段、版本与许可 | **首选仅元数据/schema核验**，尚不能保证构建12帧干预 |
| [TRACE / VES-Bench](https://arxiv.org/abs/2608.22516) | 论文报告600题/348个公开视频，每题附联合必需证据时间区间，覆盖度定义明确 | 必须核对真实可获取的视频版本、样本许可、区间与帧解码对应方式 | 作为证据覆盖核查的第一候选资源之一 |
| [CaST-Bench](https://woven-by-toyota.github.io/CaST-Bench/) | 2066个问题、1015个视频，因果证据时段/框轨迹注释 | 原视频下载、版权许可和注释复杂，可能超出RTX3090阶段预算 | 备选，仅做规模与字段验证 |
| [MLVU 项目已用分区](https://github.com/floomeer83felix-source/vlm/blob/main/docs/research-progress-2026-10-08.md) | 已有工程数据与基线账本 | 旧探索来源不可当新的独立确认集；仅20源中短片 | 用于已有错误结构的文档审计，不拿旧测试冒充新验证 |

### 必须披露的版本漂移

HERBench 2026 论文摘要报告 **26,806** 题，而当前项目 README 报告 **27,936** 题，HF 最近又出现 lite_v2；这些数字不能互相替换或合并，更不能将某个版本的题目级数量当独立视频源数。进入数据步骤前，冻结准确的仓库 commit、HF revision、split、媒体manifest、文件 SHA、许可、题目与事件源 ID。禁止选择性抽取曾经观察到模型输出的测试题用于新的确认。

## 4. 研究空间的保守定义

### 不应宣称的创新

1. 原始“自适应关键帧+证据存储+停止”组合；
2. 仅增加局部密采、zoom、实体角色检索或选项区分检索；
3. 仅统计标注证据区间覆盖或按照答案稳定性终止；
4. 仅以时序图、事件链或双模型对照给已有方法改名；
5. 仅复现 HERBench 所揭示的“检索与融合均困难”。

### 可以作为**待验证科学问题**（不是已证实的论文贡献）

同一问题、同一主模型、同一**已覆盖参考必需区间**和同一12个唯一源帧预算下，非参考区间中“问题相似但可能分散注意”的帧与普通背景帧是否导致稳定、可重复的配对误伤差异？是否集中发生在明确的多段时序依赖任务，而不是静态/语言捷径任务？

此问题即使成立，也只是**现象级**贡献可能性。扰动、帧顺序敏感性与证据组织已有大量既有工作，下一轮创新审查必须阅读全文、搜索最新引用及代码，检验是否已被更直接研究；未通过不得提出正式算法。

### 对照要求

- 保持参考必需区间的源帧不变，同时固定其余槽数、提示、推理参数和输出解析；
- 记录各臂的视觉token、处理器时间、缓存/解码、前向、独立评分与整管线成本，不以名义“帧数相同”冒称成本完全相同；
- 注释区间仅可供封闭的离线实验设计；任何可部署策略不得读取标准答案或参考区间；
- 观察到准确率变化不自动推出“模型忽略视觉”或“干扰是语义原因”。

## 5. 阶段门槛

- **L1 数据门**：有可对应原视频的明确参考必需证据标注，且 ≥40 个操作性独立来源可构建等预算的预定义干预；不满足则 HOLD。
- **L2 现象门**：实验预注册且记录全部失败，配对效应在新来源有稳定方向；不能仅挑选题目、阈值或某一任务后解释。
- **L3 新颖性门**：逐条说明与上述论文可引用的算法差异；若只能重述已公开机制，则 retain 0。
- **L4 验证门**：通过源独立确认数据、强基线、跨模型验证以及真实成本对照之后，才谈期刊核心贡献。

结论：**当前没有可保留的全新算法候选。阶段一最合理成果是形成严谨的诊断预注册，而不是给失败机制起新名称。**

## 6. 审查范围限制

本矩阵是“定向摘要/项目页核对”，不是系统文献检索、全文逐段鉴别或任何算法的专利/创新保证。参考来源及数字应在后续阶段复核其版本、发布日期和实际实验条件。