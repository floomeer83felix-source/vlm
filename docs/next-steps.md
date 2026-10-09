# VLM 下一步工作安排（ChatGPT 维护）

> 协作规则：**ChatGPT 负责研究规划与审查；Codex 每轮领取本文件中唯一 READY 的任务或任务包。一个任务包可依书面协议连续完成多项安全子任务，统一反馈后再审核**。执行事实写入 [codex-results.md](./codex-results.md)，脱敏附件上传 [codex-artifacts/](./codex-artifacts/)，ChatGPT 审核后更新 [research-overview.md](./research-overview.md)。
>
> 基准历史：[research-progress-2026-10-08.md](./research-progress-2026-10-08.md)（原始快照，不覆盖）。
>
> 更新日期：2026-10-09（北京时间；BATCH010一次官方下载/记录统计已验收，但时间数值质量HOLD；BATCH011唯一READY只读核验）。本文是执行入口，不代表任何新模型实验已运行。

## 一、任务看板

| ID | 优先级 | 状态 | 执行者 | 工作内容 | 完成判据 |
|---|---|---|---|---|---|
| VLM-001 | P0 | **ACCEPTED（2026-10-08）** | Codex | Windows 本地实验工作区**只读状态盘点** | [回报](./codex-results.md)与[审计附件](./codex-artifacts/VLM-001/workspace-audit.md)已提交；仅文档交付验收通过，非GPU运行放行 |
| VLM-002 | P1 | **ACCEPTED（G1 HOLD）** | Codex | 公开证据数据集许可、schema、版本与时间桥接元数据核查 | [结果报告](./codex-artifacts/VLM-002/dataset-metadata-review.md)已审查，3候选均未满足G1；不可据此运行新实验 |
| VLM-BATCH-003 | P1 | **ACCEPTED（静态交付；G1 HOLD）** | Codex | A: PTS/VFR/媒体桥接；B: 历史来源隔离与指纹缺口；C: G1无答案元数据/12帧技术合同 | [三份审计报告](./codex-artifacts/VLM-BATCH-003/README.md)与[Codex回报](./codex-results.md)由提交 [31e8151](https://github.com/floomeer83felix-source/vlm/commit/31e8151901c1c75739670acefec211f920313244)交付；只接受审计，不批准新实验 |
| VLM-BATCH-004 | P1 | **ACCEPTED（toy报告通过；G1 HOLD）** | Codex | VES请求草案、toy CPU测试、G1决策报告 | [提交462ccde](https://github.com/floomeer83felix-source/vlm/commit/462ccdec4a999ef62e67a1cb52e7392fd7e14517) 五项文件已审查；Codex报告10/10 toy通过，未独立重跑，不放行真实实验 |
| VLM-BATCH-005 | P1 | **ACCEPTED（toy18/18自报；G1 HOLD）** | Codex | A官方渠道；B合成负例；C路线裁决 | [提交7d1daf7](https://github.com/floomeer83felix-source/vlm/commit/7d1daf725fae5c7a921274e575101966ffed99a8) 五处交付已审查；18/18为Codex报告，非真实媒体验证 |
| VLM-ROUTE-006 | P0 | **ROUTE2_SELECTED（取代先前路线1）** | 用户与ChatGPT | 新主问题：无gold必要区间、固定12帧选帧策略与输入路径鲁棒性 | [新的科学预注册](./route2-no-gold-preregistration.md)及[创新初审](./route2-novelty-screen.md)；TRACE咨询稿保留UNSENT且不执行 |
| VLM-BATCH-006 | P1 | **ACCEPTED（十项有界交付；科研NO_GO_OR_PIVOT）** | Codex | 文献/创新/混杂、静态接口/许可/PTS、统计合同及toy、科学决策 | [e581039](https://github.com/floomeer83felix-source/vlm/commit/e581039970106dbec741adf502e48e5f948adad4)：4报告、2 toy、1追加已审；执行者报11/11 CPU测试通过；普通 S_q/S_t 新算法NO-GO，窄2×2仍UNKNOWN |
| VLM-DECISION-007 | P0 | **B_SELECTED（新机制研究，不继续旧采帧路线）** | 用户与ChatGPT | 保留长视频VLM高水平论文目标；旧S_q/S_t选帧/2×2提示仅作历史，不作为核心创新 | [机制重立题](./mechanism-reset-2026-10-09.md)与下一唯一READY BATCH-007；没有保留的创新机制 |
| VLM-BATCH-007 | P1 | **ACCEPTED（10项交付；RETAIN 0 / STOP THIS PORTFOLIO）** | Codex | 历史与先例、M1/M2/M3形式定义、双世界反例、toy、数据/强基线及否决 | [d82e30e](https://github.com/floomeer83felix-source/vlm/commit/d82e30e43ec31fb8600b0a61d62021017a6d59aa)：5报告+2toy+1追加符合范围；执行者报12/12 CPU单测；M1/M2/M3当前算子均可由现有逻辑/依赖缓存/判别规划模拟，无新增核心机制通过 |
| VLM-RESEARCH-GATE-008 | P0 | **CHARADES_SELECTED / EGO4D_DEFERRED（历史Ego4D未提交确认）** | 用户与ChatGPT | 因Ego4D表单报Failed to fetch，用户同意改用公开Charades／Charades-STA进行数据准入核验 | [新数据路径说明](./charades-entry-2026-10-09.md)：不是已下载数据/合法验证/新模型实验批准；原Ego4D申请意愿保留历史但不再是当前任务 |
| VLM-BATCH-008 | P1 | **ACCEPTED（10项文档交付；数据/创新/长域GO仍HOLD）** | Codex | Charades许可、STA权利、schema/join、重复实例与重叠假设、来源PTS、长域缺口、五门裁决 | [提交2544df9](https://github.com/floomeer83felix-source/vlm/commit/2544df98fa363bc62ec888682121d879f24bcec2)：严格5份脱敏报告+1条追加；Charades原license/schema仅文档条件准入，实际重复样本计数UNKNOWN，STA许可HOLD，普通新算法NO-GO，Charades单独长域FAIL |
| VLM-DATA-GATE-009 | P0 | **USER_APPROVED_METADATA_ONLY（单次官方小包下载已执行/消耗）** | 用户与ChatGPT | Charades官方约3MB原标注仅为非商业隔离CSV/时间区间/来源资格统计使用，已在BATCH010取到ZIP及CSV | 不允许第二次下载、视频/帧/STA/模型/GPU、原Windows研究环境变更；仅允许在原授权范围内对固定隔离目录**现有CSV只读元数据时间合同核验**，具体范围见[BATCH-011](./codex-artifacts/VLM-BATCH-011/README.md) |
| VLM-BATCH-009 | P1 | **STOPPED_SAFELY（路径名称误判；NO_DOWNLOAD）** | Codex | 授权与隔离预检、HEAD检查、通用元数据审计工具及合成测试；真实ZIP/CSV资格因保守路径阻塞未执行 | [首次提交bc16e38](https://github.com/floomeer83felix-source/vlm/commit/bc16e38eab35f454bc3e0ccc3c805c15c6009ed8)：5处约定交付，GET0/正文0B/P1P2 UNKNOWN；正确安全停止，**禁止原父任务重跑** |
| VLM-BATCH-009-FIX | P1 | **ACCEPTED（路径身份检查修复；未下载）** | Codex | 修正Windows absolute/resolve仅字符串不等的误报，加入samefile/设备inode/双链无reparse与缺失叶核验 | [修复提交dda8481](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)：2通用Python改动+一条附加结果；执行者报告21项合成测试通过、固定路径只读复核PASS；**未独立核Windows，也未下载或读CSV** |
| VLM-BATCH-010 | P1 | **ACCEPTED（一次官方下载与聚合交付；TIME_QUALITY HOLD）** | Codex | 官方小包1成功GET/3,519,822B、ZIP CRC/白名单、CSV schema、短域P1/P2记录候选聚合 | [提交8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)：严格2报告+1追加、原源码不改；66,500区间中19,625不通过既定数值规则，主因end>length；资格数仅过滤子集临时值，**不放行模型/视频** |
| VLM-BATCH-011 | P1 | **READY（10项只读时间合同诊断；0下载/0媒体/GPU）** | Codex | 核官方length/动作时间规范、版本sha、异常端点互斥归因及量级桶、原347 P1组和97,723 P2 pair可信性、止损 | [十项README](./codex-artifacts/VLM-BATCH-011/README.md)：仅读现有隔离CSV/类表，独立通用stdlib诊断和合成单测；2脱敏报告+2新脚本+1结果；不更改旧源码、下载文件或原研究环境 |
| VLM-PTS-001 | P1 | **INCLUDED IN VLM-BATCH-003（不可单独执行）** | Codex | 原PTS静态审计需求 | 按任务包子任务A执行，原[说明](./codex-artifacts/VLM-PTS-001/README.md)仅作背景；不重复上传 |
| VLM-003 | P1 | BLOCKED（旧gold区间诊断的manifest不再是当前路线；无新明确任务授权） | Codex | 原四臂manifest冻结，作为历史未执行工作保留 | 不得依据旧README/PR执行；任何新机制需新许可、来源、PTS、预算与用户授权 |
| VLM-004 | P2 | BLOCKED（需单独实验放行） | Codex | 小规模配对问答先导与独立复核 | 唯一 GPU 调用账本、完整分母、纠错/误伤、置信区间与成本 |

**当前唯一READY父任务：VLM-BATCH-011，仅对BATCH010已取得的本地Charades原CSV做时间区间合同/异常数值诊断，0下载、0媒体/模型/GPU。** [BATCH010提交8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)按照3处白名单交付，执行者报告1次官方小包GET成功3,519,822B、SHA256 c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866、14 ZIP成员CRC通过/提取8白名单、11列/157类/7,985训练+1,863测试行和标准库21合成用例通过；这些是执行者本机报告，ChatGPT未登录原Windows独立复算。**核心科学阻塞：66,500条动作token中19,625条（29.5%）不通过旧`0≤start<end≤length`，含异常行7,433/9,848（75.5%），主要是end>length**。有效子集中P1同类分离组347、P2异类重叠pair97,723，均仅PROVISIONAL RECORD-LEVEL，不代表完整样本/时序真值。官方[README](https://prior.allenai.org/projects/data/charades/README.txt)称length以秒计，不能未经证据缩放或截断标注。BATCH-011仅做本地只读固定CSV/version与公开官方时间合同、匿名差额桶/主因/独立交叉计算，**不再次下载、不修改原审计代码和任何原研究资产、无需新GPU许可**；在原Codex聊天由用户主动触发，完成后再STOP并等待ChatGPT审查。科学创新retain0，短域无法单独确认长视频，PTS UNKNOWN。

## 二、VLM-001：Windows 工作区恢复状态盘点（历史任务，已完成）

### 目标

在**不重跑任何模型、不修改现有环境**的情况下，弄清楚原本地 RTX 3090 研究工作区的真实状态。研究对象为长视频预算约束下的视觉证据与推理；已有尝试尚未产生经科学/创新审查支持的核心新机制。

### 允许范围

1. 只读了解本地工作区实际位置、目录用途、历史进展、run 配置、现有模型与数据清单；**不从公共 GitHub 目录缺少源码推断本地也没有源码**。
2. 只读检查 Windows GPU 情况（如 `nvidia-smi`）、活动 Python/训练进程、现存锁的**文件存在性**及可能持有者、磁盘剩余空间；无法确认锁持有者时注明“未知”，不要删除锁。
3. 只读核对现有 conda `pytorch` 环境中 Python、PyTorch、CUDA/驱动、模型及处理器版本；**不安装、升级或新建环境**。
4. 只读检查调用账本：最后运行的 run ID、planned/started/terminal 状态与数量、是否有 started 未终态、最新成功记录与异常记录；不泄漏原始答案/隐私标签。
5. 判断本地已否具备下一研究阶段的前提：源身份隔离、SHA/PTS 可追溯、GPU 串行和持久账本；把未验证的项目列为“未确认”而非“通过”。
6. 若本地工作区与这个公开文档仓库是两个目录，**不要把工作区整体推入公共仓库**；只通过文档仓库的 `docs/codex-results.md` 发送脱敏反馈，并将必要的小型文本证据放到 `docs/codex-artifacts/VLM-001/`；不得整体上传原工作区。

### 禁止事项

- 不启动新的 VLM 问答/训练/评分前向，不补跑旧题或旧候选。
- 不杀进程，不改动/删除锁、账本、环境、数据、模型、配置或原有日志。
- 不下载数据集、视频或模型，不用付费 API/云 GPU，不新增人工标注。
- 不公开模型权重、视频、原始问题答案、私有标签、凭据、Token 或暴露敏感路径的完整命令行。
- 不擅自合并旧 PR #1，也不修改本文与 `research-overview.md`。
- 首次审计仅限必要的目录与日志概要，避免打开海量视频或生成大段终端输出。

### 可参考的安全命令（按需选择，不机械全跑）

- `Get-Location`、`git status --short`、`git rev-parse HEAD`（如果工作区有 Git）。
- `nvidia-smi`（报告 GPU、显存和相关进程，输出须脱敏）。
- `conda env list` 和当前环境的版本查询；若 `conda` 不在 PATH，记录该事实，不尝试安装。
- `Get-Process python,pythonw -ErrorAction SilentlyContinue`（仅看与任务相关的进程）。
- `Get-ChildItem` 查看相关目录及账本文件元数据，不批量读原始视频/权重/私有标签。

### 输出要求与反馈路径

**以下为 VLM-001 当时的交付要求，现已完成；禁止重复执行。**

**该历史任务仅允许新增/修改两处交付物：**

1. 在已建立的目录 `docs/codex-artifacts/VLM-001/` **新建** `workspace-audit.md`，内容遵循 [附件模板与脱敏规范](./codex-artifacts/VLM-001/README.md)。这里只写必要的环境/资源/账本**汇总**，不贴原始代码、日志、视频、绝对个人路径。
2. 在 `docs/codex-results.md` **追加**一条 `VLM-001` 记录，简述执行状态，并链接 `codex-artifacts/VLM-001/workspace-audit.md`。不要修改原有历史条目。记录至少包含：

- 检查北京时间、执行机操作系统与 GPU 证明、工作区 Git commit（如有）、工具/环境版本；
- 本地活动进程、锁/账本、模型/数据/脚本是否存在的简短事实表（每项说明证据类型）；
- 不确定项、未检查项及异常，不以缺失检查当作“安全”；
- 有无修改研究工作区（理论应为无）、有无 GPU 前向（应为0）、下载（应为0）；
- 是否可以进入 VLM-002 的 **建议** GO/HOLD（Codex 不具有放行权）；
- 相关非敏感本地报告文件的路径或 SHA，可不上传日志正文。

反馈以 **约300—600字中文摘要**为宜；必要结构表可另附。完成后仅提交**上述两处文件**到公开仓库 `main`，不要顺手上传代码、数据、模型、原始评分或其他文件。提交前检查 `git diff --cached --name-only` 和两个文件内容。若无法安全写入 GitHub，停止并直接在本地对话报告阻碍，不要强推或覆盖他人提交。

### 结束条件

**VLM-001 已由 ChatGPT 于2026-10-08按GitHub交付验收通过。** 其在当次审计中仍未知的GPU锁持有状态、全量旧账本覆盖、真实PTS与来源独立性均未因此转为通过；模型推理仍 HOLD。

## 三、VLM-002：公开参考证据数据集元数据核验（历史任务，已完成，G1 HOLD）

### 目标与输入

用尽可能少的Codex额度判断是否有公开资源**在标注定义和获取条件上可能满足**固定12帧配对诊断的G1数据门。优先核查 [TRACE/VES-Bench](https://arxiv.org/abs/2608.22516) 和 [HERBench](https://herbench.github.io/)，若前两者都无法确认字段/权限，再简查 [CaST-Bench](https://woven-by-toyota.github.io/CaST-Bench/)；不得无边界搜索相近数据集。可参考尚未合并的 [PR #1](https://github.com/floomeer83felix-source/vlm/pull/1) 文献矩阵/预注册草案；它们是研究草案，不是经过证实的样本可用性证书。

### 允许工作（只查元数据，无GPU）

1. 查官方论文/项目主页、README、公开数据字典、标注文件的**元数据描述**、schema样本或版本清单；精确记录仓库commit/数据revision/split/媒体manifest是否可见。不得把论文声称直接冒充已实测字段。
2. 标注本地研究所需的许可/访问条件：视频许可与注释许可分开判断；无法核实写UNKNOWN，不以网页可访问代替许可。
3. 对每个资源记录：有无多段联合必需时间区间或参考关键帧、时间单位和坐标、可否对应同版本视频、是否能识别至少三个非重叠参考区间与 <12 个锚帧、是否存在区间外候选池。这些只做schema可行性初筛，**不得声称真实VFR/PTS对齐通过**。
4. 记录题数、视频数和操作性独立来源组数是否明确区分；报告与历史MLVU保护来源隔离如何可能实现。未知项逐条列出，**不得承诺>=40独立来源**。
5. 在证据有限时优先选择STOP/UNKNOWN，避免扩张访问链；旧AGQA访问失败不再续查。
6. 候选资源择优，列后续 G1 的最小验证动作，不启动 VLM-003 或 GPU 实验。

### 强制限制与预算

- **新增 GPU/QA/训练/评分前向 = 0；新增视频/模型/压缩包/整套数据集下载 = 0**，不修改现有 conda、CUDA、研究工作区或历史账本；不申请/删除锁。
- 只访问少量官方公开页面和必要的schema样本；建议单一响应体 <=256 KiB，累计公开元数据响应体 <=2 MiB。超限必须停止并标UNKNOWN；不得靠拆包绕过。
- 不读取本地私有答案/评分标签，不把选项答案用于新策略选择；不访问完整标注正文、敏感身份映射或受限视频。
- 不公开私人路径、授权令牌、视频、权重、原始日志或整套研究资产。

### 本次唯一交付

1. 在已创建的 [`docs/codex-artifacts/VLM-002/`](./codex-artifacts/VLM-002/) **新建** `dataset-metadata-review.md`，遵循 [README 模板](./codex-artifacts/VLM-002/README.md)，注明官方来源与版本、各数据集许可证、字段实际证据与未知、PTS/媒体映射风险、对12帧实验的适配限制和GO/HOLD建议。
2. 在 [`docs/codex-results.md`](./codex-results.md) **追加** VLM-002中文摘要并链接前述附件，保留此前VLM-001结果，不删改旧条目。
3. 只向公开仓库main提交上述两个文件；确保没有附带视频、模型、私人路径、原始注释/答案。发现提交冲突停止，不强推。

**VLM-002 已于2026-10-08按任务交付验收，G1数据门仍HOLD。** 不再重复相同官方页面和404访问链；除非ChatGPT另行明确立项，否则不下载整套数据或媒体。

## 四、VLM-BATCH-003：三项研究准备工作（历史任务包，已验收）

### 放大单轮任务规模的理由

用户希望减少Codex每做完一项就等待新的ChatGPT安排的往返。在**不突破已授权资源边界**的前提下，把原 [VLM-PTS-001](./codex-artifacts/VLM-PTS-001/README.md) 时间戳审计与两个互补的静态/技术合同任务统一打包。此前的VLM-001、VLM-002交付已完成；尚未形成可靠的新证据区间/独立来源/时间桥接数据门，**不能**按旧预注册直接构造四臂或做新问答。

### 可连续执行的三项子任务

1. **A 现有PTS/帧索引/VFR/裁剪时间桥接**：静态追踪必要解码代码与manifest字段，输出时间坐标合同、缺口、未来测试建议，不运行视频解码/模型。
2. **B 历史来源独立性、重合与指纹缺口**：只读研究现有聚合manifest及源组schema，厘清30 prepared/20 selected与约450份指纹覆盖缺项的统计定义，给出保守来源去重和探索集污染控制合同；不遍历大批媒体、不读取标准答案、不补做视频哈希。
3. **C G1数据可行性和无答案manifest合同**：在VLM-002已审查公开元数据和A/B报告基础上提出D1/D2固定12帧诊断的技术前置条件、失败码与数据集HOLD清单；**不新下载数据、不假定有40个独立源、不宣称G1 PASS、不编写或运行实验**。

**执行细节、逐项字段、提交文件名与阻塞规则：** [`docs/codex-artifacts/VLM-BATCH-003/README.md`](./codex-artifacts/VLM-BATCH-003/README.md)。这是本批的唯一有效交付合同；旧PTS任务README只作历史输入，不再单独交付。

### 边界、提交与反馈（不可放宽）

- 用户在**原来的同一个Codex聊天**发送一次继续指令，Codex安全同步文档仓库main，检查`codex-results.md`是否已存在本任务包回报，然后一次完成A→B→C；A/B单项无法核实时可先记UNKNOWN并继续其余独立安全项，不虚构缺口。
- **0新增GPU模型调用、0训练、0评分前向、0视频解码、0视频/模型/完整标注下载、0本地研究资产修改、0新conda/CUDA修改**。原锁与旧账本不可更改或重放。
- 只在公开仓库 `docs/codex-artifacts/VLM-BATCH-003/` 新增 **3个脱敏Markdown附件**（分别为 `timestamp-contract-audit.md`、`source-provenance-audit.md`、`g1-feasibility-contract.md`），以及向 `docs/codex-results.md` **追加1条 VLM-BATCH-003 汇总记录**。只提交这4处变动，不改ChatGPT维护的任务书、总览、AGENTS或任何历史结果。
- 如果先前已有 `### VLM-BATCH-003` 的完成/部分完成/阻塞记录，禁止重复执行；转请ChatGPT审查。遇到Git冲突或敏感信息泄露风险停下，不强推或扩大权限。
- **整包提交后停止本轮操作，但保留同一Codex聊天**；由ChatGPT集中科学审查并决定下一个任务包。其他任务仍BLOCKED。

### 历史任务包验收

2026-10-08 22:25北京时间，Codex以[提交31e8151](https://github.com/floomeer83felix-source/vlm/commit/31e8151901c1c75739670acefec211f920313244)交付A/B/C三份报告及1条汇总。ChatGPT已核对提交范围和证据边界：**ACCEPT 文档与静态审计交付；真实PTS/媒体对应、历史独立来源、G1数据适用性均仍HOLD**。本节只保留历史任务定义，**严禁再次执行**；后续参照新第五节。

## 五、VLM-BATCH-004：数据阻碍与toy合同验证（历史已完成）

### 为什么安排这一批

VLM-BATCH-003确证的主要风险：最近12帧路径仍按index/FPS表示时间，历史789源节点中仅339有可复用摘要、450缺项，目标VES/HER/CaST的真实参考区间、媒体许可/版本与≥40独立源仍未通过G1。继续重复静态盘点收益低。本轮改为**取得合法数据的最小请求准备 + 可运行CPU纯合成测量合同 + 明确去留标准**。旧实验数据和真实媒体、模型一概不动。

### 同一个Codex聊天框一次做完三项

- **A** 只起草VES-Bench许可、无答案schema/参考区间、视频版本/时间坐标请求（中英文），不发送邮件/Issue、不猜邮箱。
- **B** 在单独文档Git仓库的 `prototypes/` 新建Python标准库**纯合成**时间戳、源分组、D1/D2输入不变量参考原型与unittest；**实际运行toy CPU单测**，不导入原研究源码、不解码视频、不调用模型或修改环境。额外查配对时间分布与视觉token预算公平性，未知不能当通过。
- **C** 根据A/B做G1数据门HOLD条件树与toy测试报告。提出少量最有信息量的后续动作，未通过许可/真实证据前不得开展四臂/GPU实验。

**唯一交付合同：** [VLM-BATCH-004/README.md](./codex-artifacts/VLM-BATCH-004/README.md)，严格规定两个脱敏Markdown、两个toy代码文件与一条 `docs/codex-results.md` 追加结果。A→B→C连续执行，若部分未知则诚实标UNKNOWN，不反复请求数据。

### 预算、界限与结束

- 新模型/QA/训练/评分前向**0**，视频解码/视频、模型及完整数据集下载**0**，研究资产/既有conda/PyTorch/CUDA/锁/旧账本修改**0**；不发送联系邮件或GitHub Issue，不合并PR或自动后台运行。
- 本次仅允许创建 `docs/codex-artifacts/VLM-BATCH-004/ves-access-request.md`、`docs/codex-artifacts/VLM-BATCH-004/g1-decision-and-toy-test.md`、`prototypes/toy_g1_contract.py`、`prototypes/test_toy_g1_contract.py` 并在 `docs/codex-results.md` 追加一个父任务结果；公开文件必须脱敏。
- 如果同任务ID已有结果记录、资料泄漏、不可安全提交或Git冲突即停止；不可强推、重复GPU调用或修改ChatGPT维护文件。整包完成后保留原Codex聊天框，等待下次研究审查。

### 本批已完成，以下仅供历史追溯

Codex已经在 [462ccde](https://github.com/floomeer83felix-source/vlm/commit/462ccdec4a999ef62e67a1cb52e7392fd7e14517) 提交5处成果。ChatGPT检查了提交范围、文档和toy用例源码；Codex报告修正后10项unittest通过，但本助手未独立重跑。**本批ACCEPTED，不再执行。**

## 六、VLM-BATCH-005：数据访问出口、toy负例与路线裁决（历史已验收）

[完整任务包README](./codex-artifacts/VLM-BATCH-005/README.md)已在main创建。本次在**同一个Codex聊天框**连续完成：

1. A：限量查看TRACE/VES-Bench官方公开资料，核实可信的数据访问/咨询渠道和许可证说明；不发送邮件、Issue或表单。
2. B：仅修改公开文档checkout下两份纯合成toy代码，补强“至少3个互不重叠区间”、时间分布、来源UNKNOWN以及公平性UNKNOWN等反例，运行标准库CPU unittest。
3. C：提出保留gold参考区间D1/D2诊断还是转向无gold依赖科学问题的明确判断与停止阈值。所有数据集G1继续HOLD。

只允许新增两份脱敏Markdown、更新两份toy Python并向Codex结果文件追加1条任务包回报；详见README中的精确文件名。全程0GPU/模型前向、0视频解码/下载、0原实验资产修改、0对外联系。单次提交后停止，不执行VLM-003/004。

**本包结束后不默认继续相同的静态盘点。** 后续若需实际联系数据作者或修改研究命题，由ChatGPT根据证据向用户提出决策；真实GPU实验还需独立许可与G1通过。

> 发给原Codex聊天：继续下一轮；刷新GitHub main，读AGENTS.md、next-steps.md、codex-results.md与BATCH-005 README，只执行其A/B/C，按要求上传5处文件后停止。

### 已交付，不再执行

Codex于2026-10-09提交[7d1daf7](https://github.com/floomeer83felix-source/vlm/commit/7d1daf725fae5c7a921274e575101966ffed99a8)：两份脱敏报告、两份toy文件更新、Codex结果一条追加；ChatGPT核对提交范围与研究结论。执行者报告18项CPU单测通过；本助手未在本地独立运行。公开项目仓库Issues可用，不代表正式授权或专用数据申请。G1、GPU、真实PTS与来源独立性继续HOLD。

## 七、用户科研路线决策与历史状态（当前以最新决议为准）

- 原路线1：固定12帧且覆盖gold必要区间的诊断因合法数据/同版PTS/独立来源门未通过而HOLD；[TRACE咨询草案](./outreach/trace-ves-bench-inquiry-draft.md)仍为 **UNSENT历史**，用户并未授权发送。
- 原路线2：在无gold必要区间下，把问题相关选帧S_q与时间分层选帧S_t比较作为核心算法。已由 [BATCH-006提交e581039](https://github.com/floomeer83felix-source/vlm/commit/e581039970106dbec741adf502e48e5f948adad4) 所做十项审查否决**作为新算法的创新主张**；仅做条件性现象测量/窄提示路径实验的可能仍UNKNOWN，不继续当本期研究主线。
- **最新用户选择B（2026-10-09）**：保持长视频VLM/《计算机学报》水平的研究目标，放弃上述已高度重合的选帧方法方向，重新寻找可证伪**核心计算机制**。不承诺论文/新算法已成立，retain 0。

## 八、VLM-BATCH-007：10项核心机制科研审查（已验收，禁止重做）

2026-10-09，Codex通过[提交 d82e30e](https://github.com/floomeer83felix-source/vlm/commit/d82e30e43ec31fb8600b0a61d62021017a6d59aa)交付[任务协议](./codex-artifacts/VLM-BATCH-007/README.md)约定的全部8处文件：5份新脱敏报告、2份新标准库toy代码与codex-results中的单条父回报。ChatGPT已核对GitHub提交范围、五报告与两toy代码的科学边界，**ACCEPT有界交付；科研STOP THIS PORTFOLIO**。Codex报告用Python3.9.21执行12项合成unittest，12 PASS/0FAIL/ERROR/SKIP；ChatGPT没有在本地实验机上独立运行它们，故本结论仅验收执行者测试收据和静态论证。toy的117种观察模板/336个一致world-view配对及89次不当unknown→0造成的假认证都是**合成枚举，不能推成真实视频结果**。

- **M1 NO-GO**：[形式定义](./codex-artifacts/VLM-BATCH-007/candidate-mechanism-specs.md)可由普通三值partial-world监控复现；稀疏未观察域不能为「never」给真实证明。所有槽可见与完美感知是toy公理，现实感知不满足已验证门。恒UNKNOWN虽避免假认证但coverage=0。
- **M2 NO-GO**：定义的依赖无效化和局部更新可以用相同typed key与revision guard的普通AND/OR依赖缓存等价表达；toy仅检最小AND DAG，不证明OR、循环、矛盾、实际source identity可靠性。
- **M3 NO-GO**：同世界/答案映射/可能观察与成本的version-space/discriminative-clue planner能逐步模拟当前候选规则；独立真实`Ω`、观察响应`Γ`及答案真值当前不可用。未取得某先例全文不等于创新通过。
- **强先例与现实门**：NeuS-QA本轮SSL失败、一个MIT经典TMS定位错题，证据仅UNKNOWN；VideoHV/VideoSEAL等部分只读摘要，不因缺全文而认为新颖。现实负性事件标签、完整依赖真值、可区别观察oracle，以及媒体/QA许可、同版PTS/clip、来源独立、可靠视觉探测器、真实token/GPU预算均未验证。**retained mechanism = 0**。

**研究负责人裁决：STOP当前M1/M2/M3组合，不再自动发BATCH-008。** 保持长视频VLM高水平论文目标并不授权无限重复机制命名、摘要盘点或toy优化。今后只有在用户明确提供了**新的实质科学对象、有效合法数据/证据资源或其他可审查的创新线索**后，才重新设置一轮有限的创新性和可执行性门。研究范围变化之前，VLM-RESEARCH-GATE-008继续 WAIT_USER_DIRECTION。VLM-003/VLM-004、GPU/真实媒体/外部联系/原研究工作区修改继续BLOCKED。无需另开Codex聊天。

## 九、Ego4D历史数据路径：用户曾愿意审阅协议，现因申请故障暂停

**用户2026-10-09明确表示“愿意”走Ego4D正式许可路径**。ChatGPT仅登记申请意向，**没有替用户同意或签署法律协议，更没有提交任何数据许可表单或获得AWS访问权**。官方入口：[Ego4D用户许可表](https://ego4ddataset.com/ego4d-license/)；操作与来源：[Ego4D准入清单](./ego4d-access-checklist-2026-10-09.md)，以官网最终协议为准；个人可自行签个人许可，仅有正式签署权限才签机构协议。成功申请后可按官网流程获邮件审核，官网所写约48小时/14天凭据为通常说明，不保证实际时间；最近GitHub Issues也有用户反映表单故障，任何异常须按事实报状态、不擅自代联系。

**状态严格分层**：用户愿意审阅 `USER_WILLING` ≠ 用户已提交 `SUBMITTED` ≠ 正式获批 `APPROVED` ≠ 已批准下载/使用/公开衍生评估结果 `AUTHORIZED_SCOPE_CONFIRMED`。当前只处于第一层；用户回来只需说 `未提交/已提交待审批/已获批准/条款不接受/表单异常`，不要传邮箱、住址、PDF签章或AWS凭据。

**下一科研问题只作为匹配候选，不是新算法**：Ego4D MQ已有标注活动实例区间，可探索长视频反复活动的时间实例混淆及强对照；NLQ有可查询的回答窗口。必须先与已有时序grounding/事件检索文献去重、核目标视频-clip修订/PTS/来源组和数据研究/论文披露许可；不从MQ未标注活动推出全视频“不存在”。获批后仍需逐项批准最小数据子集下载/真实视频解码/GPU预算及原研究工作区变更。

**无需向原Codex聊天框发送“继续”**，没有READY父任务，历史BATCH-007不重跑，旧VLM-003/004仍BLOCKED。保留同一Codex聊天框。

**本节记录已完成的历史任务，以下十项不可再次执行；最新状态以任务看板与第十一节为准。**

## 十、Charades／Charades-STA 文档准入与科学问题核验（BATCH-008已验收）

**用户最新确认（2026-10-09）**：先不等待Ego4D的`Failed to fetch`问题解决，改以免事前申请的[Charades](https://prior.allenai.org/projects/charades)与[Charades-STA](https://github.com/jiyanggao/TALL)作为可合法独立评测**候选**。官方[Charades License for Non-Commercial Use](https://prior.allenai.org/projects/data/charades/license.txt)明示非商业研究、限制公开改造数据和第三方分发；有公开下载链接**不**免除许可。STA文本时间标注来自单独作者仓库和修订，权利/版本还需核实。当前**未取得任何数据**，不授权下载约3MB官方标注或约13GB视频。

[Charades准入与科学问题说明](./charades-entry-2026-10-09.md)与[**VLM-BATCH-008十任务README**](./codex-artifacts/VLM-BATCH-008/README.md)已写入main：

1. 原Charades许可可行性（商业/科研、署名、发表与禁止分发）；
2. Charades-STA独立注释权利与清理版本；
3. Charades动作区间/schema与公开元数据核对；
4. STA句子区间和Charades动作标签跨格式/同视频join协议；
5. 重复动作**同类多实例**能否从现有标注合法判定，以及真正可证伪指标；
6. 不同动作重叠/时间边界混淆的对照与指标；
7. 直接TAL/时间自然语言定位先例与创新性否决；
8. source/video/participant、split、同版真实PTS与来源独立门；
9. 约30秒短视频能/不能支持的结论与真正长视频外部数据缺口；
10. 数据许可/标签适用/创新/长视频适配五门裁决，最多请求用户**另行允许最小官方标注包下载**，不允许Codex现在拿数据。

**只允许6处交付**：`docs/codex-artifacts/VLM-BATCH-008/`目录5份指定小Markdown以及`docs/codex-results.md`末尾一条汇总；禁止任何真实媒体/标注下载、视频解码、模型/GPU、原研究目录/锁/账本更改、历史任务重做、PR合并与作者联系。若文献/STA权利或重复实例证据不足则标UNKNOWN/NO-GO，不为了完成10项伪造创新；全部完成并安全push后停下、ChatGPT审查。

**科研止损**：Charades平均约30秒，仅能支持短时域活动或自然语言时刻定位的初步闭环，不能单独成为长视频核心机制论文的验证集；公开TAL/TMR已有强基线。保留原M1/M2/M3否决、retain0、旧VLM-003/004 BLOCKED。

## 十一、VLM-DATA-GATE-009：用户已批准最小原标注包（仅有限授权）

**前轮审查前提**：[BATCH-008科学五门裁决](./codex-artifacts/VLM-BATCH-008/data-science-go-no-go.md)仅支持原Charades非商业研究／README字段**文档条件准入**，STA权利仍UNKNOWN，P1/P2实际合法资格计数未取得，普通TAD/TMR新算法与Charades作为单独长视频确认集仍NO-GO。不能凭官方66,500区间总数推断同视频重复实例有多少。

**用户最新明确授权（2026-10-09）**：用户确认自己的非商业研究用途符合[官方许可](https://prior.allenai.org/projects/data/charades/license.txt)，允许从[AllenAI Charades官方页面](https://prior.allenai.org/projects/charades)仅下载列为**Annotations & Evaluation Code (3 MB)**的小包，独立隔离存放，用作CSV字段、时间区间、同类重复候选、异类重叠候选和保守来源分组的聚合资格统计。此权限**不**涵盖视频/帧/STA、模型/GPU、原研究环境改动、向第三方分享标注。

已由ChatGPT冻结[Windows隔离存储与安全协议](./charades-metadata-safety-protocol-2026-10-09.md)，并下达[唯一READY父任务BATCH-009](./codex-artifacts/VLM-BATCH-009/README.md)。**ChatGPT自身未下载、未建目录、未取得真实CSV、未读用户电脑。** 只有用户主动在已有Codex聊天发启动消息，并且本地路径、安全、许可、官方资源链接检查全部通过后，才可执行这次受限获取。执行后仅能上传脱敏总体计数与通用代码；数据本身永久不进入公共GitHub。

**科学边界**：即使P1/P2资格组大于0，也只说明短片记录层有候选时段，不确认自然语言「第一次/第二次」真值、真实媒体PTS、独立自然长视频或模型准确率，更不自动创建GPU/下载媒体权限。

## 十二、VLM-BATCH-009：初次下载被安全拦截、后续路径身份修复（历史已结束）

**历史说明（2026-10-09验收后补充）**：本节以下记录009最初的授权和十项计划，不代表009仍可再次运行。实际009已`STOPPED_SAFELY`（GET0/CSV0），009-FIX是路径前置安全修复（合成test执行者报21/21）；当前唯一可触发的续接任务是[BATCH-010](./codex-artifacts/VLM-BATCH-010/README.md)，且也需用户在原Codex聊天发送启动消息。

**最新用户明确授权（2026-10-09）**：研究用途符合Charades官方非商业许可，批准**仅从AllenAI官网获得约3MB `Annotations & Evaluation Code`**，并在独立隔离目录中统计CSV/起止时间/来源资格；**不批准任何视频、Charades-STA、GPU或原实验环境改动**。权限界限不得由Codex或GitHub自动扩大。

**明确的本地存储路径**：Windows `%LOCALAPPDATA%\\VLM-Research-Isolated\\Charades-v1-Metadata\\`（解析为用户本地目录的实际路径，绝对值不得上传GitHub）。只允许`incoming/`（原ZIP）、`extracted/`（train/test CSV和类表等白名单）、`local-audit/`（local manifest）；执行前检查不是任何研究工作区、Git checkout或云同步区域，不含junction/symlink/旧文件冲突，空余至少150MiB。未知即STOP、不另挑位置。

**两份任务基础文档**：[冻结安全协议](./charades-metadata-safety-protocol-2026-10-09.md)、[唯一READY十项README](./codex-artifacts/VLM-BATCH-009/README.md)。10项内部子任务覆盖：
1. 数据许可与用户授权范围；
2. 独立Windows本地存储前置与目录安全；
3. 仅官网官方S3对应3MB包，流式总量≤8MiB、记录SHA与下载状态；
4. zip成员安全/路径/大小/加密/链接风险预检；
5. 只读取train/test CSV和固定类表真实schema，拒执行随包代码；
6. 记录完整训练/测试行数及坏区间分母；
7. P1同类非重叠区间候选及0/0.5/1s敏感性汇总；
8. P2异类时间重叠及0.5阈值汇总；
9. 仅在本机计算subject/split重叠计数、粗时长分布，隐藏具体video/subject；
10. 输出候选资格与FAIL/UNKNOWN科学结论，不能把资格非0当物理事件真值、新算法或长时域研究GO。

**GitHub只允许5处**：`docs/codex-artifacts/VLM-BATCH-009/`两份脱敏markdown（下载/完整性/schema报告、候选资格/研究决定），`prototypes/`两份不含真实数据的标准库解析代码及合成unittest，向`docs/codex-results.md`末尾追加**一条父任务结果**。绝不能上传ZIP、真实CSV、subject/video映射、script/descriptions、绝对私人路径或低样本可链接小表。只可运行标准库CPU测试和数据行解析，**0视频、0GPU、0模型、0原工作区改动**，不执行下载包评测脚本。通过安全stage、单次push后STOP。

**未执行声明**：ChatGPT本轮只更新任务材料，未向用户的Windows机器下载包、未建立隔离目录、未创建任何CSV统计。只有用户主动让**原Codex聊天**执行且执行前检查通过，才能产生新数据核验。旧VLM-003/004仍BLOCKED，研究 retain0，正式长视频数据门HOLD。

## 十三、VLM-BATCH-010：官方小包已获取、时间质量HOLD（历史已验收）

**历史任务警示**：以下为BATCH010执行前的授权与计划文本，已由[8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)执行完成。**禁止再次执行下载或重复该父任务；后续只有011只读诊断READY。**

**本轮审查结论（2026-10-09）**：BATCH-009 [提交bc16e38](https://github.com/floomeer83felix-source/vlm/commit/bc16e38eab35f454bc3e0ccc3c805c15c6009ed8)在目录`Path.absolute()`与`Path.resolve()`路径规范名称不一致时按协议保守STOP。用户直接授权的[修复提交dda8481](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)后，执行者报告通过samefile+有效物理目录ID、两条祖先链reparse点检查及canonical稳定性，21项合成标准库单测PASS。ChatGPT已审查提交变更范围和公开代码，但**未实地访问Windows独立确认路径**；原数据GET次数仍0，ZIP/CSV/P1/P2均UNKNOWN。009交付/安全阻塞应标`STOPPED_SAFELY`，修复仅为`ACCEPTED_PRECHECK_FIX`，不是实际元数据工作完成。

**下达新的父任务（而非重复旧任务）**：[VLM-BATCH-010十项受限续接README](./codex-artifacts/VLM-BATCH-010/README.md)。用户先前明确授权的那**一次**官方`Annotations & Evaluation Code`获取**未发生**，因此仅在同一限制内继续这项已获准工作；开始前务必重新核路径物理身份、没有旧文件冲突、与原RTX3090工作区/公共Git/云同步根隔离，再核当前官方链接与GET`≤8MiB`的流式硬限制、ZIP完整性/CRC/白名单、真实train/test字段及错误分母、P1同类不重叠区间、P2异类重叠区间、仅粗粒度`subject`跨split数量和长视频/创新停止门。若一项不安全/不兼容，立即BLOCKED，**本次不授权Codex边下载边修审计源码**。

**BATCH-010只准3处GitHub提交**：新增`docs/codex-artifacts/VLM-BATCH-010/download-and-schema.md`、`qualification-and-decision.md`两份脱敏结果，以及只向`docs/codex-results.md`末尾追加一条010父任务回报；不改已发布的009原型/test、协议、历史或研究计划。ZIP、CSV、任何subject/video映射、真实行和私有绝对路径都不得上传。**没有新模型/GPU/视频/STA/下载其它数据权限**；用户主动在原Codex聊天发送“执行BATCH-010”后才可开始。

## 十四、VLM-BATCH-011：Charades时间字段数值冲突的独立只读诊断（当前唯一READY）

**源事实与严格层级**：BATCH010官方ZIP SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，train CSV SHA`59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`、test CSV SHA`8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`（仅文件级，不是官方发布的独立SHA证明）。标注字段真实11列、7985/1863个视频行和157类别，原动作token 49809/16691；合法数值区间35211/11664，无效14598/5027。约75.5%视频行至少包含一个被旧规则拒绝的token，主因`end>length`；当前不能把剩余47k记录当物理事件完整真值。P1 347个同类有分离pair的组、P2 97723个异类相交pair**只是旧合同下幸存子集的几何候选，不是有效问答/新算法模型实验的许可**。

**独立官方时间合同**：[AllenAI原README](https://prior.allenai.org/projects/data/charades/README.txt)定义`actions`是`class start end`三元组，`length`为视频长度（秒），Changelog显示2017-02-27新增官方length，localize评测用25个时间点。这不能证明原CSV所有标注已无冲突，也不能通过变换时间单位来消除不通过的分母。具体数据质量根因仍UNKNOWN：既可能是标注/视频修订，也可能审计器的时间假设不适用或其他错误，不能无证据归责于官方数据。

**受限十项执行协议**：[VLM-BATCH-011 README](./codex-artifacts/VLM-BATCH-011/README.md)。用户已批准的小包下载**已经发生，不能再次GET**；只有使用固定Windows隔离目录`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`内现有CSV只读计算和官方公开文本查验可做。执行次序：①SHA/权利确认②官方时间定义及版次③独立CSV解析交叉核④互斥与重叠异常flag⑤end-length差额桶⑥每视频异常token个数聚合⑦P1子集资格验证⑧P2子集资格验证⑨隐私、来源、分母审计⑩`HOLD_TIME_CONTRACT`或证据支持下的下一步止损。禁止查看/上传原始单行、视频ID/subject/描述、低样本可逆表，禁止数值截断/猜测缩放。需先在合成数据完成stdlib单测再读真实CSV；数据/原脚本不能改变。

**只允许5处GitHub交付**：`docs/codex-artifacts/VLM-BATCH-011/`的2份脱敏报告，`prototypes/`的2份新通用只读脚本（非旧审计器修改），`docs/codex-results.md`末尾1条父任务回报。禁视频/STA、模型/GPU、真实视频PTS测量、原研究工作区与锁/conda更改、任何数据/标注再次下载及外部联系。出现审计器不稳定/真实hash不符立即停止、不得覆盖旧收据。Codex成功单次push后停止，待ChatGPT验收。

## 十五、当前研究判断（跨批保持）

- 用户保持高水平论文目标，但不假定一定成功；目前 retain 0。前期100/300题及各种已关闭候选、GAP7、BATCH-003至006**不得重跑**。
- 新机制创新门 `N`、可证伪性 `T`、非平凡有效性 `U`、合法可用标签/媒体 `D`、预算/PTS/来源 `B`、强baseline公平比较 `F` 当前**无候选PASS**。toy通过不提升这些门。
- 历史真实媒体PTS /同版剪辑/来源独立性、答题数据许可、评分隔离和真实token成本仍未在新来源验证。只做纯symbolic toy不需要视频许可，但不能由此推导真实数据可执行性。
- PR #1未合并且主要基于旧gold路线；不可直接执行旧manifest或旧GPU预算。新问题可能需要不同证据标签，先做学术可识别性/合法数据核查，再决定是否值得付出真实实验。
- 如果十项研究全部被直接先例或现实标签门否决，回报**RETAIN 0 / STOP PORTFOLIO**，不继续为凑10项编新算法。

## 十六、GitHub协作规范（不改变）

- ChatGPT维护`docs/next-steps.md`、`docs/research-overview.md`和科学立题文档；Codex仅执行唯一READY父任务并追加`docs/codex-results.md`及README明确的脱敏产物。
- 原始`docs/research-progress-2026-10-08.md`保持永久快照；历史已验收任务和原Windows RTX3090/conda`pytorch`实验工作区与公开文档checkout严格分开。
- 每轮用户在原Codex聊天发送继续信号，Codex按远端main而非旧缓存执行；安全提交1次后停止，不force push、不自动后台运行/轮询、不唤醒Codex。
