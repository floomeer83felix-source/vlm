> **2026-11-03负责人已暂停：PAUSED_BY_OWNER / NOT_READY，当前无READY。** 用户质疑继续追加任务的必要性后，负责人决定[收束当前研究](../../research-decisions/research-stop-and-083-pause-2026-11-03.md)，不再把机制去留判断交为新一轮Codex执行。没有公开083交付，私有是否已开始UNKNOWN；已有工作保留，停止新增动作，不创建空结果/新任务。069论文仍暂停，不训练/forward/新私有缓存审计/媒体/GPU，不自动084。以下原083合同逐字保留为设计记录，旧“唯一READY”不构成执行授权。

# 083 机制再立项：先去重和设计，不再直接加训练

2026-11-03（北京时间）｜ChatGPT研究负责人。

**唯一READY：PUBLIC_SOURCE_MECHANISM_REVIEW_AND_EXPERIMENT_DESIGN。** 只做公开代码/一手文献复核和决定性实验设计；不是081/082续跑，不继承任何训练/GPU/下载预算，069论文仍暂停。

## 本次要回答的问题

在081普通对照和联合监督均未拟合、082未找到确定成因的情况下，是否还有一个**不同于已关闭方案且值得验证**的机制？允许答案为没有。交付最多一个候选；不能为了有下一任务强行给新头。

安全同步独立文档仓库，读AGENTS/最新看板/results/[082验收](../../research-decisions/post-082-cache-diagnosis-and-mechanism-reset-2026-11-03.md)，核唯一尚未交付READY。只读公开仓库，不进入私有实验根、不读封存V/q/权重/逐项输出、不做新的缓存审计。

## 1 先核现有机制，禁止换名复活

只读公开081的`head_class/relation/train/predict`及082报告，并回看以下既有设计的定义与失败边界：

- [057联合监督](../VLM-TEMPORAL-TRAIN-PILOT-057/README.md)、[059验收](../../research-decisions/post-059-directed-pair-disposition-2026-10-30.md)、[060验收](../../research-decisions/post-060-pool-transfer-disposition-2026-10-31.md)。
- [061角色对比](../../research-decisions/post-061-question-role-contrast-2026-10-31.md)、[063裁决](../../research-decisions/post-063-disposition-and-paper-plan-2026-10-31.md)、[070裁决](../../research-decisions/post-070-review-and-selector-intervention-2026-11-01.md)、[075裁决](../../research-decisions/post-075-review-and-full-model-visual-screen-2026-11-02.md)。

画清当前计算式：Qwen冻结特征、位置项进入哪里、query pool/readout、答案BCE、正确/错配relation目标。只作源码/代数论证；不import运行旧训练/scorer。区分数学上必然的不变性、实际二元决策不变和未确认的优化成因。至少给一个边界反例：为什么“当前小头没学成”不推出“所有同输入函数都无法做对”。无需新测或补算logits/梯度。

## 2 只查直接近邻

优先读一手正文方法/实验与作者代码；摘要不足以排除重合。固定四个入口：

| 一手来源 | 必须排除的重复主张 |
|---|---|
| [CRPO v2，2605.21988](https://arxiv.org/html/2605.21988v2) | 反事实视频、答案随任务相关变化而变/不变、segment reordering收益；这些概念已非空白 |
| [Tracing the Arrow of Time，2605.07568](https://arxiv.org/html/2605.07568v1) | 时序信号流失、连接器诊断和时间保留投影 |
| [TimeBlind，2602.00288](https://arxiv.org/abs/2602.00288)及[作者仓库](https://github.com/Baiqi-Li/TimeBlind) | 视频/问题最小配对、四格指标和时间组合诊断 |
| [Text encoders bottleneck compositionality，EMNLP2023](https://aclanthology.org/2023.emnlp-main.301/) | 问题向量组合信息/角色信息瓶颈；不能直接把CLIP结论套到当前Qwen |

最多另补两篇直接近邻；不做宽泛文献海搜。记版本、URL、方法节/公式/作者代码位置、读到的证据与未取得部分。读不到正文就UNKNOWN，不以二手摘要宣布创新。没有安装/抓取整仓/数据/模型/媒体；公开文本读取总≤20MiB，作者代码只取相关小文件。检索服务底层流量不可见则如实列覆盖，不造精确wire统计。

## 3 最多一个候选，必须给出可否证差异

先列最多三个机制判断（含“关闭、不保留”），最终最多保留一个。每个保留候选须具体到：

1. 当前视频和当前问题如何映射到答案的公式/伪代码；训练时的额外监督与推理时可用信息分开。推理不读反事实视频、答案、源ID、人工事件槽位/真值区间；合成诊断的oracle事件码只作单测，不冒充真实推理输入。
2. 与普通时间adapter、CRPO、旧059/061/070分别有什么**算子或可检验假设差异**。一般位置编码、flatten顺序特征、注意力、反向问题相减、事件时间差、损失加权本身不称首次。普通强基线不能因比旧头好就被升格为创新；没有明确差异就REJECT/RETAIN0。
3. 一个会推翻候选的反例，以及现有081/082究竟提供了什么支持、还有什么缺证。不能把“解释了旧失败”写成已证事实；候选和普通对照如何避免同一未拟合问题必须说明。

## 4 决定性实验只设计，不执行

若保留候选，只交一份可直接审阅的最小实验合同草案，按顺序设门：

- **先可学性资格**：标准顺序保留对照先在无真实数据的已知顺序合成问题，以及事前固定的极小train-only子集上拟合全排列/互补问题。规定确定的取样规则、final step/预算、成功阈值及不足即STOP；不看开发/test选择超参或样本。该资格本身不认科研创新。若尚无法具体规定一个合理可学对照，不能提出全量新训练。
- **再机制比较**：基础模型、能正常拟合的强普通适配器、候选和破坏其关键机制的对照；可训练参数量、数据、初始化/种子、优化预算和checkpoint政策匹配，明确额外监督成本。新架构收益与新监督收益分开，否则不归因联合机制。最低同时看单项、相关交换FLIP/无关交换HOLD、完整配对/源级全对及当前视频相对固定视频控制的收益。
- **后来源变化**：说明什么才算未用来源、来源重叠如何影响结论。先不新增benchmark访问或人工标签，不把当前8组开发test说成独立确认。给定量保留/关闭门、分组单位和不确定性方法；预先固定，不能看结果改门。
- 列所需CPU/GPU、新forward/小头训练更新数、输入/代码白名单、一次性停止规则和最小必要授权。没有明确证据和成本就不请求训练。此处仅设计，不执行任何forward/backward/优化/训练，也不自动提出任务084执行。

若没有保留候选，`decisive-design.md`改写为明确的NO_JUSTIFIED_NEW_EXPERIMENT及缺失证据/关线条件，不用虚构方案填表。

## 5 简洁交付与停止

文档研究父轮≤3600秒，从首次同步前登记时间，不扣助手空闲；只要起点缺失就如实UNKNOWN，不倒填。新文件合计≤2MiB，不安装、不写新模型/训练代码；无需新Windows科学Job、模型准入或重复资源审计。遇到一手来源不可达记录缺证，在已有证据范围完成判断，不另开网络修复任务。

**精确五处交付**：本目录`execution-receipt.md`、`prior-art-and-mechanism-screen.md`、`decisive-design.md`、`execution-summary.json`，以及`docs/codex-results.md`唯一追加一条083。只能写研究审查/实验设计，**不写论文正文**。摘要给`ONE_CANDIDATE_FOR_REVIEW`或`RETAIN0 / NO_JUSTIFIED_NEW_EXPERIMENT`，两者都不是机制成立/训练获批。

安全审查、普通push main后STOP。历史数据/代码/results前缀/旧论文/规划文件均不改；任何新训练、GPU、媒体、原始数据、完整Qwen或小头前向、梯度补算和私有文件访问均0。负责人验收后再决定是否立项并仅请求确有必要的新授权，不自动084。
