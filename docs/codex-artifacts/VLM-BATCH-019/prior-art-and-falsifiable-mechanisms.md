# VLM-BATCH-019：先例与可证伪机制

2026-10-10。结论先行：`NOVELTY=RETAIN0`。下列H1/H2/H3是待否证问题，不是已提出的新算法；通用换时钟/记忆/证据/压缩/置信弃答版本均NO_GO_AS_NOVEL_CORE。未跑实验、toy、模型或任何论文代码。

## 方法与证据分级

这是限定来源的scoping screen，不宣称穷尽PRISMA综述。先读六候选的官方入口与用户种子，再查arXiv摘要/HTML、CVF正式元数据和AAAI期刊HTML，日期边界2023至2026-10-10。检索组合包括“long video question answering selective prediction calibration abstention 2025 2026”“repeated event instance binding long video temporal grounding 2026”“temporal grounding uncertainty calibration conformal video 2026”。只保留原始论文/作者项目证据；聚合博客、镜像和检索出的PDF不作机制证据、不打开文件。文献综述技能只用于证据与反证结构；用户仅Markdown/禁模型与代码要求覆盖其PDF/AI制图/脚本流程。

题名、发表状态与机制分别核。P=正式元数据或作者camera-ready说明；A=只核摘要；H=额外读到HTML。预印本不写已录用，作者报告效果不作为本项目结果。摘要未说明的算子、标注字段和假设一律UNKNOWN。

## 必查六先例

| 原始公开来源/时间 | 已核机制/范式 | 与本题重叠及不得再主张的贡献 | 阅读范围 |
|---|---|---|---|
| [VideoTree作者页](https://videotree2024.github.io/) / [arXiv 2405.19209](https://arxiv.org/abs/2405.19209)，2024预印本、CVPR2025 | 查询相关聚类选帧、树表示、广度/深度自适应展开，caption送回答模型 | “关键帧检索+分层索引+粗到细补看”已被覆盖；仅重命名证据树不新 | P/A，项目方法段 |
| [ReWind arXiv 2411.15556](https://arxiv.org/abs/2411.15556)，2024-11-23；[CVF正式元数据](https://openaccess.thecvf.com/content/CVPR2025/html/Diko_ReWind_Understanding_Long_Videos_with_Instructed_Learnable_Memory_CVPR_2025_paper.html)，CVPR2025 | 指令条件动态记忆读写、记忆指导高分辨率相关帧选择 | “Evidence Memory+记忆引导补看”不是原创；temporal fidelity不等于本研究已核PTS | 正式CVF检索元数据可见，直接HTML读失败；机制按原arXiv摘要A核，不假称读过PDF/全文 |
| [VideoMind 2503.13444v3](https://arxiv.org/abs/2503.13444v3) / [作者项目](https://videomind.github.io/)，2025起、2026-02-21版，ICLR2026 camera-ready | planner/grounder/verifier/answerer，Chain-of-LoRA切角色 | 定位—核查—回答证据代理及多角色验证已有；“先找证据再回答”不新 | P/A，题名采用Temporal-Grounded版本 |
| [Seeing Is Believing / EV²-Bench与DynamicSelect](https://ojs.aaai.org/index.php/AAAI/article/view/38031)，AAAI2026，2026-03-14，DOI10.1609/aaai.v40i13.38031 | 可核时空视觉证据评估、动态语义选择与分层token压缩 | 证据质量benchmark/自适应压缩本身已被覆盖；本轮未核其实体schema/许可，不能借它当已有真值 | P/A，不取PDF |
| [LongVideoBench 2407.15754](https://arxiv.org/abs/2407.15754)，NeurIPS2024 D&B | referred context与跨场景关联，视频/字幕交错QA | 跨分钟指代与顺序推理benchmark已有；不能把“多时刻信息”单独当贡献 | P/A；创建过程另读v1 HTML |
| [EgoSchema 2308.09126](https://arxiv.org/abs/2308.09126)，2023-08-17 | temporal certificate sets刻画内在时间依赖，实际输入3分钟 | 多时刻证据充分度/长依赖评估不是空白；3分钟不能冒充自然小时 | A，官网时长交叉核 |

## 2026增补最近邻（不是新数据准入）

| 来源/版本状态 | 对候选机制的直接约束 |
|---|---|
| [Explicit Abstention Knobs](https://arxiv.org/abs/2601.00138v2)，v2 2026-01-15，预印本；[HTML](https://arxiv.org/html/2601.00138v2) | 视频QA置信门控、risk–coverage与证据截断诊断已存在；置信阈值不能独占为H1/H3机制 |
| [COVER: Conformal Coverage Guarantees for Any Video Temporal Grounder](https://arxiv.org/abs/2608.07434v1)，2026-08-07，页面仅称投稿AAAI2027，未视为录用 | 后处理非符合度校准/边界扩展与概率覆盖已有；保证依赖可交换性，视频内相关样本并非当然有效。H1不能只给区间扩大再称风险可控 |
| [Grounded Entity Biographies](https://arxiv.org/abs/2609.38155v1)，2026-09-29预印本；[HTML](https://arxiv.org/html/2609.38155v1) | 视觉同实例关联、跨事件biography与episodic证据联合检索；还处理未解决的身份关系。普通H2身份记忆与不确定关联注释直接碰撞，并非只“同名词汇”先例 |
| [Grounding with Confidence](https://arxiv.org/abs/2609.39883v3)，2026-09-30起、2026-10-08 v3，预印本 | 区间级置信头，将候选生成与接受分离，支持固定候选池的预算/阈值排序与拒绝；H3“给候选打分再省预算”已不够 |
| [Hour-long grounding/search decomposition](https://arxiv.org/abs/2606.12300v1)，2026-06-10预印本 | ExtremeWhenBench与检索后定位说明小时级search/recognition分解已有。仅说“长时定位是搜索问题”不新；未核新benchmark许可，不加到六候选的准入表 |

另定位到[On the Consistency of Video Large Language Models in Temporal Comprehension，CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/html/Jung_On_the_Consistency_of_Video_Large_Language_Models_in_Temporal_CVPR_2025_paper.html)正式检索元数据，但直接HTML不可得，细方法SOURCE_UNAVAILABLE/UNKNOWN；只作必须后续核的先例风险，不凭题名断定算子相同。上述五预印本虽未验证正式录用，也不能从新颖性审查中删除。

## H1：坐标不可识别与回答风险的联合处理

假说：同版映射有可核不确定集时，将坐标失效、证据定位和答案错误分别建模，可以在等覆盖/成本下减少“答案看似正确却绑定错误时间证据”的接受。它不同于宣称统一减offset即可提升；当前没有新算子或定理，核心创新UNKNOWN。

设映射集合M、定位集合I，工程强基线应直接构造 `J=union_{m in M} m(I)` 并拒绝没有可识别映射的样本；再加COVER/普通QA门控。联合错误定义为“答错或证据错或版本/坐标无效”的并集。只有每一子风险都有有效标签/条件，才能讨论风险上界；不能用置信度代替坐标标签，不能在跨域失配下沿用可交换性保证。

| 项目 | 预注册约束（未来许可成立才可测试） |
|---|---|
| GT/独立来源 | Ego4D具文档化窗口但常规NLQ非小时；HourVideo具长域却未证对应窗口。独立长域同版时钟/定位GT尚UNKNOWN，不能用QA答案补齐 |
| 强基线 | 正确确定性转换+恒等输入、最坏映射并集、COVER、普通置信校准/弃答、VideoMind式核查；同一backbone、帧/候选池 |
| 可测预测 | 非零且相同覆盖（纸面目标≥60%）时，联合错误较最强工程/校准组合下降≥2个百分点，视频分组CI支持正向；同时报告区间面积/弃答/错时证据接受，不能全弃答获0风险 |
| 强反例 | 两个不可区分版本允许不同offset，schema和观测相同而真实证据不同：没有新信息就不可能确定恢复；只把两区间扩大并集不会产生新信息 |
| NO_GO | 全部收益由正确offset转换解释；简单union+COVER等效；无可核版本/GT；只在合成注入而非独立真实来源有效。此时降为工程合同，不做新算法 |

## H2：重复事件实例的身份与因果顺序分离

假说：在同对象反复进入相似状态的长域中，区分“对象是同一个”与“事件是哪一次”，能减少first/last类顺序错误。GEB已覆盖物理对象关联，VideoMind/LongVideoBench已有定位与关联；所以只建实体图或加时间戳记忆立即NO_GO_AS_NOVEL_CORE。残余是可否证诊断，不是已保留方法。

| 项目 | 预注册约束 |
|---|---|
| GT/独立性 | 需要跨分钟同对象ID、不同事件实例边界/序号与歧义标签；六候选中此联合GT尚未证。NLQ窗口不穷举，LVBench任务名不是已发布实例表；HourVideo/Ego4D不能算独立外测 |
| 强基线 | GEB同实例biography与身份未决注释、ReWind、VideoTree、VideoMind；明确对象ID条件与同名/无ID对照，成本一致 |
| 可测预测 | 成对重复实例绑定/顺序准确率较最强同预算基线提升≥2个百分点，普通单事件性能不显著受损；另测可识别反事实顺序稳定性。题目/字幕单独基线和映射乱序对照必须报告 |
| 强反例 | 两世界已观察帧/字幕相同，未观察区间中两个外观等价事件的真实身份/先后不同：记忆容量不能补不可识别信息；把对象身份正确当事件序号正确会失败 |
| NO_GO | 新方案可由GEB连接/索引或普通排序模拟；GT缺失/需未经许可新人工标注；只凭文本泄漏或视频剪辑伪造“因果真值”。当前H2主机制NO_GO，评价门HOLD |

## H3：同预算下证据充分度的校准诊断

假说：模型答案置信与可核证据覆盖分离，在同帧/token/候选/实际wallclock下能识别正确猜测并控制证据错误接受。EV²-Bench、EgoSchema证据范式、DynamicSelect和Grounding with Confidence已覆盖核心普通版本；校准流程本身是强基线，不是原创。

| 项目 | 预注册约束 |
|---|---|
| GT | 独立视频上的QA标签与必要/充分证据集合分别存在，标注允许使用且不会泄漏给观察/选择器。LongVideoBench创建过程引用帧可能有帮助，实际发布/充分性标签UNKNOWN；EV²实体与许可未核 |
| 强基线 | DynamicSelect、VideoTree、等容量直接候选置信排序、普通校准弃答/COVER、EV²标准证据评估；作者大模型分数不能与本地小模型直接比较，需记录同模型适配差异 |
| 可测预测 | 等覆盖/成本下错误证据接受下降≥2个百分点，QA与证据双指标CI支持；成本计预编码/重观察/所有调用/校准标签采集；比较空证据、无关证据与相似干扰，不用答案稳定代替真值 |
| 强反例 | QA回答始终相同且正确、证据支持为空：准确率和置信稳定都不能证明grounding。若选择器只是多看更多帧，所谓校准收益应被等预算基线消去 |
| NO_GO | 无独立充分度GT；只有QA增益/额外token；置信排序或现有证据指标完全复现增益；样本仅少数易题。当前仅协议候选，机制RETAIN0 |

以上数值是未来纸面决策门槛，不是实测提升、功效分析或已安排实验。任何假说须先通过[六门可行性](paper-feasibility-and-exit-gates.md)，按视频/基础来源划分探索—校准—审计，不用test继续选路线；校准标签及原答案与policy接口隔离。缺功效/样本时写UNKNOWN或停止，不能为了期刊目标保留一个已被普通基线模拟的“创新”。
