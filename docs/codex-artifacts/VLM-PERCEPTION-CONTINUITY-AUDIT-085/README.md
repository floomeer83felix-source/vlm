# 085 | Perception Test 原媒体自然连续性：一次限定只读元数据核查

2026-11-04（北京时间）｜ChatGPT科研负责人制定｜**唯一 READY 父任务：LOCAL_081_CONTINUITY_METADATA_READ_ONLY**。
2026-11-04 用户明确回复“批准”，批准的是上轮[数据准入提案](../../research-decisions/temporal-alignment-data-gate-2026-11-04.md)的限定私有元数据读取：**已登记文件≤64、读取≤16MiB、CPU≤60秒；无视频画面、Qwen特征、模型权重、答案、GPU、媒体下载、解码、训练、全盘扫描。** 没有获得任何更大的数据访问/GPU预算。旧084已验收关闭，083维持PAUSED；本任务不是084重跑或083恢复。

## 0. 启动与既有任务互斥

- 使用用户当前的 Codex 会话执行一次；先在**独立的公开GitHub文档checkout**安全`git status --short; git fetch origin main`，读最新`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、`docs/research-overview.md`及本README；按AGENTS要求干净后只fast-forward。若有冲突或非正常工作树，STOP不重置不覆盖。
- 确认最新任务板只有**本085一个READY**，且results里没有085父项既往交付。若不唯一或本父已消费，STOP，绝不再跑。
- 本父仅访问已完成081（旧32来源）的**现有注册元数据**。不从GitHub公共研究记录推断任何Windows私有文件存在；不重用081媒体/下载/模型权限或所谓剩余配额。
- 在开始本地读取前，将原本已在此前081执行工作中获准使用的、**准确单一私有081受控根**作为根目录由当前Codex已有的本地授权上下文解析（必要时用户仅在本地会话提供；不上传/不写公开文档）。不得用磁盘搜索、PowerShell递归枚举、`find`/`rglob`/`os.walk`、环境变量猜测或读取别的科研项目来定位。**无精确根或路径身份存疑时记BLOCKED_MISSING_REGISTERED_ROOT并停止私有读取**，不为完成任务而扩大范围。
- 检查root为既有的081封存身份，manifest的版本/源分组与公开081报告`32 sources / 20,4,8`相容。若不能确认来源身份即`BLOCKED_IDENTITY_UNKNOWN`，不随意使用同名目录/备份。允许root内部既有manifest中**精确登记**的seal/metadata条目，仅严格所需的媒体身份、存在/尺寸/已记录时长PTS证明；对旧078/079/080引用但位于本白名单root之外的5源不追踪读取，按`EXTERNAL_REF_UNVERIFIED`计数。不能因为旧关联可追溯就越界。

## 1. 只读白名单和预算

最小读取白名单（**存在且明确由原081注册清单指向**时才读取；不是要求必须全部存在）：

- root内控制与封存元数据：`parent.json`、`manifest-seal.json`、`media-plan.json`、`media-seal`类精确注册文件、`media-*-seal.json`明确已登记条目、`metadata/summary.json`等不含标签的身份/计数结构；每个文件须登记路径/大小并先做大小和用途闸。
- root内原登记视频条目只能用`os.stat`/等价的**文件系统元数据**读取存在性和文件大小；**禁止open/read/hash/stat视频内容**、读取压缩内成员、重新检查CRC/哈希、ffprobe、媒体索引解析、抽帧或生成时间戳。旧seal已有hash只能用于比对**所记录的字面identity**，不可重新计算视频哈希。
- 仅对已经公开识别的旧081媒体注册链对应的结构性source身份作内存join；原标注`truth.json`/`answers.json`/`relations.json`及GT映射、逐项问题/预测、训练/模型张量或状态、RGB、视频、Qwen processor与tokenizer、其它任务/项目一律不读取。
- 若元数据文件本身同时含结构信息与**答案/标签、受保护的映射、完整原问题文本或个人信息**，不要读取该文件以抽取其中无关字段；计`NOT_PERMITTED_MIXED_FILE`和UNKNOWN。仅允许为纯结构注册/封存文件开文件；任何未预先确认安全性的内容不打开。
- 上限为**累计最多64个已登记文件的内容读取**、累积显式read bytes **≤16MiB (=16,777,216 B)**，不按零长度/多次读取规避计数；已打开文件重读仍累计，stat不能打开媒体。CPU处理总≤60秒，进程内存≤512MiB（如可适用），程序超出即STOP。不安装任何软件/换环境，不使用GPU/CUDA/模型/torch、无网络访问/新媒体取得/修复解码/训练/隐私目录枚举。仅本地stdio/file-stat核查，文档GitHub同步与结果推送除外。
- 采用`pathlib.Path.resolve`及`os.path.commonpath`或等效手段防止符号链接/junction逃逸；任何清单所指越界路径直接计`OUTSIDE_APPROVED_ROOT`且不读取。路径若含绝对私有路径/标识，内存用后脱敏，绝不能输出到GitHub。

## 2. 唯一研究问题与判据

**问题：旧081从Perception Test official train取得的32个已处理媒体来源，是否有现存、已封存的“同一原始自然连续录制的L—M—R”资格证据？**

严禁把旧081六排列真实RGB或三段3秒裁切单元当成自然连续视频、把三个独立事件包改称L/M/R、或从原事件排序生成的下游`36frames`推定自然相邻。确认自然L/M/R至少要具备以下**元数据层面的必要条件**：
1. 明确的**同一原始录制媒体身份**与现存的完整原始连续媒体；而非仅存在三个拼接/预切样本或生成的派生RGB。视频有时长/索引的旧封存证明，而不仅是旧文件名、三段帧数或有压缩member。
2. 同一原时间轴上三个有效且各有正时长的封存时间区间`[L_start,L_end]`, `[M_start,M_end]`, `[R_start,R_end]`；必须有原始时间戳来源标记，且按封存精度符合`L_end <= M_start <= M_end <= R_start`（若存在空隙，报告最大gap/允许容差未预设则`CONTIGUITY_UNCONFIRMED`，不能直接宣称自然紧邻）。明确区分原始录制时间和后处理重排位置。
3. 任意“多候选中段同原视频高相似性”的事实若未有独立封存不可推测。即便上述1–2满足，本父也**只能报告METADATA_CANDIDATE_EXISTS**，不能证明视觉内容、许可之外的用途、干扰难度、模型输入正确、数据独立、反捷径或科学任务已合格。
4. 原始录制/参与者物理独立性如无已存公开许可范围内的证据标UNKNOWN，不将32个Source等于32个独立拍摄。train20/dev4/test8都是旧官方train划分，旧8已看过，不能充当新盲测或外部泛化。

只据实际有资格、非混合的已登记元数据计数，分别给出：已注册old081 source总量和身份核对、现存完整原连续媒体证据数、仅裁切/重组证据数、自然同录制L-M-R候选数、timestamp不足/UNKNOWN数、越界引用数、文件缺失数、禁止混合文件数。**不要编造非穷尽类计数相加等于32，报告各计数口径与覆盖数量**。避免零证据时把所有来源称为NO_MEDIA；只能`NOT_PROVED_WITHIN_ALLOWED_METADATA`。

## 3. 可执行实现和独立软件自检

- 先写最小安全只读Python stdlib分析器`prototypes/perception_continuity_gate_085.py`：支持**明确root+明确文件白名单**（不要默认glob或扫描），强制计数/字节budget/路径约束、只读stat、JSON安全字段最低限度提取和counts。将**代码本身**作为允许的公开交付；实现必须在执行真实读之前固定范围，禁递归搜索、媒体读取、标签解码、Qwen/训练。
- 先写`prototypes/test_perception_continuity_gate_085.py`最小**合成临时目录**自检：安全root/外路径、超额度、清单缺失与未知、时间不连续、只裁切、含GT的混合文件拒绝。测试合成fixture不能冒充真实32来源数据。允许最多一次明显实现错误的定位修复并记录前后失败。
- 若合成自检无法通过或不能确保真实文件不混合标签，停止真实读取，状态`BLOCKED_SAFE_SCHEMA`。不要为了取得结果去读更多私有文件。已封存metadata schema不支持决定自然相邻时明确`HOLD_INSUFFICIENT_TIMESTAMPS`，**不做新媒体索引以补证**。

## 4. 输出、状态和停止

项目父总时长≤3600秒（从首次本轮同步**前**持久登记；助手闲置不自动剔除），私人只读CPU≤60秒；新增受控本地中间输出≤64KiB，公共报告新增≤64KiB。精确允许**五处文件 + 一条结果append**（共六处）：
1. `prototypes/perception_continuity_gate_085.py`（stdlib安全审查脚本）
2. `prototypes/test_perception_continuity_gate_085.py`（合成测试）
3. `docs/codex-artifacts/VLM-PERCEPTION-CONTINUITY-AUDIT-085/execution-receipt.md`（start/end/文件数、字节、CPU、测试及明确UNKNOWN、预算合规范围）
4. `docs/codex-artifacts/VLM-PERCEPTION-CONTINUITY-AUDIT-085/continuity-aggregate.json`（仅聚合计数、分类边界、状态）
5. `docs/codex-artifacts/VLM-PERCEPTION-CONTINUITY-AUDIT-085/research-disposition.md`（解释为什么有/没有可用自然L/M/R及下一阶段未获批项）
6. `docs/codex-results.md`**一次且仅一次**append完整085父项；根据证据为`METADATA_CANDIDATE_EXISTS / MORE_QUALIFICATION_NEEDED`、`HOLD_INSUFFICIENT_TIMESTAMPS`、`NO_CONTIGUOUS_ORIGINAL_MEDIA_EVIDENCE`或安全`BLOCKED`。**不要声称TRAINING_READY、DATASET_COMPLETE或ALGORITHM_INNOVATION**。

- 若准确原root无法从本地已批准上下文取得，先STOP私有访问，按安全`BLOCKED_MISSING_REGISTERED_ROOT`提交（只限本任务结果与脱敏证据），不通过搜索弥补。
- 源ID、原始文件名、私人绝对路径、原始记录映射、媒体/帧、原问题/GT/答案、权重/张量、逐项实验结果、其他任务目录/私人文件绝不进入公共输出。保留实际被拒绝字段的**原因类型计数**，不公开值。
- 写入前先比对`git diff --cached --name-only`必须且仅允许上述六处；旧`README.md`、`AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、旧实验、旧论文和任何私有文件均不修改。普通一次push main，不得force push或重置。推送完成后STOP，**不自动086**。GitHub的READY状态由负责人下一次审核清除；Codex不自行编辑规划文件。

## 5. 任务的研究意义不是承诺新算法

最好的正向结果只意味着：现有素材可能在原时间线上定义连续片段，可以申请以后一次具体的视频资格核验；如果纯元数据已经缺持续性，合理结论就是止步。无论哪种结果都不能自动触发训练、测试集访问或独创算法认定。

本轮额外授权只包括上述安全元数据处理；用户不必对子步骤再批准；如果需要新增文件、媒体索引、真实文本编码或进一步GPU资格，请负责人先给出一个新的明文有限合同。
