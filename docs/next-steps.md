# VLM 下一步工作安排（ChatGPT 维护）

> 协作规则：**ChatGPT 负责研究规划与审查，Codex 仅执行本文件中标记 READY 的单个任务**，执行事实写入 [codex-results.md](./codex-results.md)，必要的脱敏文本证据上传 [codex-artifacts/](./codex-artifacts/)，ChatGPT 审核后更新 [research-overview.md](./research-overview.md)。
>
> 基准历史：[research-progress-2026-10-08.md](./research-progress-2026-10-08.md)（原始快照，不覆盖）。
>
> 更新日期：2026-10-08（北京时间）。本文件是执行任务入口，不代表任何实验已经运行。

## 一、任务看板

| ID | 优先级 | 状态 | 执行者 | 工作内容 | 完成判据 |
|---|---|---|---|---|---|
| VLM-001 | P0 | **ACCEPTED（2026-10-08）** | Codex | Windows 本地实验工作区**只读状态盘点** | [回报](./codex-results.md)与[审计附件](./codex-artifacts/VLM-001/workspace-audit.md)已提交；仅文档交付验收通过，非GPU运行放行 |
| VLM-002 | P1 | **ACCEPTED（G1 HOLD）** | Codex | 公开证据数据集许可、schema、版本与时间桥接元数据核查 | [结果报告](./codex-artifacts/VLM-002/dataset-metadata-review.md)已审查，3候选均未满足G1；不可据此运行新实验 |
| VLM-PTS-001 | P1 | **READY（仅静态代码审计）** | Codex | 审查本地FPS/帧索引与真实PTS/VFR、裁剪版本桥接的静态契约 | [提交脱敏时间戳审计报告](./codex-artifacts/VLM-PTS-001/README.md)和Codex回报；0视频解码/0模型调用/0环境改动 |
| VLM-003 | P1 | BLOCKED（等 VLM-002 与方案审查） | Codex | 冻结新诊断实验 manifest、来源去重、四臂输入契约与预算估算 | 数据来源、分母、帧/PTS、成本与错误处理均可审计 |
| VLM-004 | P2 | BLOCKED（需单独实验放行） | Codex | 小规模配对问答先导与独立复核 | 唯一 GPU 调用账本、完整分母、纠错/误伤、置信区间与成本 |

**当前只有 VLM-PTS-001（静态时间戳/帧桥接审计）可执行。VLM-001、VLM-002 均完成文档交付验收，VLM-002 G1数据门仍HOLD；VLM-003/VLM-004仍BLOCKED。** 用户全程使用**同一个 Codex 聊天框**；每次用户在该聊天框发送“继续下一轮”时，Codex都必须安全刷新文档仓库main、重新读取最新任务书/结果文件，并执行尚未交付的唯一READY任务。不要常驻轮询，也不要因GitHub推送自行启动下一轮。ChatGPT在可用的自动任务中约每小时检查一次新Codex结果，不代表实时push webhook，自动审查成功必须以本文件及研究总览实际写入为准。

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

## 四、VLM-PTS-001：时间戳与源媒体版本静态契约审计（当前唯一READY）

### 为什么现在做

VLM-002 的 [元数据审查](./codex-artifacts/VLM-002/dataset-metadata-review.md)指出：
- VES-Bench最匹配“联合必要区间”的论文定义，但实际QA区间schema、视频/注释许可、媒体版本和PTS仍UNKNOWN；
- HERBench列schema可见，但不能把MRFS当作必要锚帧真值；视频上游许可与嵌套支持区间未核；
- CaST-Bench提供mm:ss的证据区间字段描述，但真实PTS/clip零点和三段必要性仍未证明。

因此当前**不能**冻结D1/D2新实验manifest。为了避免未来即使找到数据仍因原有FPS/帧索引时间戳损害证据判定，先做极小范围的静态时间戳契约审计（不是实验）。

### 本轮Codex任务和验收

请阅读 [VLM-PTS-001/README.md](./codex-artifacts/VLM-PTS-001/README.md) 的全部协议，完成以下**一项任务**：

1. 只读检查本地现有视频采帧、稀疏解码器、时间戳打包和manifest字段的必要代码片段（安全相对路径/函数名/摘要即可）；明确`frame_index/fps`、真实PTS、VFR、裁剪时间零点、同版本媒体文件哈希的关系与缺口。
2. 检查已有PTS-aware依赖与测试声明（静态检查），列出最小可核验的输入/输出字段合同、错误标记与未来测试方案；**不修改代码、不运行视频、不启动模型**。
3. 新建 `docs/codex-artifacts/VLM-PTS-001/timestamp-contract-audit.md`，只上传脱敏文本、字段/风险矩阵、未知项；在 `docs/codex-results.md` 追加 `VLM-PTS-001` 摘要并链接附件。仅提交这两个文件到main。
4. 原本地Windows RTX3090研究目录、模型、实验日志、锁、conDA/PyTorch/CUDA保持原样，0 GPU/QA、0下载、0视频解码；不得读取/上传私有答案。
5. 一旦提交完成就停止，不继续VLM-003/004。GitHub冲突不强推，未知写UNKNOWN。

**PASS只表示静态接口风险已查清**，不会自动消除VLM-002数据G1 HOLD、旧450来源指纹隔离缺口、锁持有未知或创新性门槛。

### Codex 如何在同一个聊天框领取更新任务（不持续消耗额度）

**用户一直使用现有 Codex 聊天框，不需要建立新会话。** 在用户发送“继续下一轮”这类指令时，Codex按下面流程开始新执行轮次：

1. 确认GitHub**文档仓库 checkout**的位置，不要对非Git的本地实验目录盲目git pull。
2. 在文档checkout执行 `git status --short` 和 `git fetch origin main`；读取 `git show origin/main:AGENTS.md`、`git show origin/main:docs/next-steps.md`、`git show origin/main:docs/codex-results.md`、`git show origin/main:docs/research-overview.md`。若工作树干净且可快进，按安全方式同步；存在冲突则STOP并报告，不reset/rebase/force push。
3. **每一轮都重新读取GitHub上的最新任务状态**，忽略此前聊天中曾经READY的旧任务、缓存的AGENTS文本。AGENTS.md对已开启聊天不会自动热加载，所以要主动查看最新文件。
4. 只有任务看板中恰好一项READY、该任务ID尚未在Codex结果中交付时，才执行这一项；否则STOP并报告。
5. 只按任务专用README上传脱敏结果，完成后STOP本轮操作，**但保留同一个聊天框**。等待用户在同一聊天发送下一条简短指令；不要长时间轮询、自动执行BLOCKED任务或启动GPU。

**用户在原Codex聊天框只需发一句：**

> 继续下一轮：先安全同步GitHub文档仓库main，重新读取AGENTS.md、docs/next-steps.md、docs/codex-results.md，只执行尚未交付的唯一READY任务，按要求上传报告后停止。

GitHub的更新不会自动唤醒空闲Codex，ChatGPT的每小时审查自动化也无法直接给该Codex聊天框发消息。用户已取消 Windows 每30分钟 Git/PowerShell 检查方式，不应安装或使用该本地计划任务；本项目仍由用户在同一个 Codex 聊天框发送“继续下一轮”来领取任务。

## 五、研究判断依据（当前有效）

- 历史已测试候选没有保留；不重跑100题基线、300题先导、撤回/替换、关系观察、密采、弱实例绑定、原生Sparse12或GAP7。
- 暂定下一科学问题：固定12源帧且覆盖公开参考必需时间区间时，非参考区间不同帧组成是否会改变问答正确率与误伤？**这是待证伪的现象，不是已通过创新审查的新算法。**
- 新数据/实验不可仅凭已有汇总直接开跑：优先核实标注与真实视频源对齐、许可、来源独立性、预算及评分隔离。
- 本次阶段一文献/预注册草案在 [PR #1](https://github.com/floomeer83felix-source/vlm/pull/1) 中，**尚未并入main，供审查参考**。

## 六、GitHub 协作原则

- **ChatGPT 编辑**：`docs/next-steps.md`、`docs/research-overview.md`；必要时另存复核结论。
- **Codex 编辑**：只向 `docs/codex-results.md` 追加按任务ID标识的事实反馈，并将本轮任务所需的脱敏文本附件放到 `docs/codex-artifacts/<任务ID>/`；不回写或删改旧条目，纠错用新条目。
- **原始快照**：`docs/research-progress-2026-10-08.md` 永久保留为当日历史记录，不改写过去结论。
- 每次用户在 ChatGPT 请求“审查最新结果/安排下一步”，ChatGPT 先读三个协作文件和本轮差异，给出接受/退回/HOLD并更新任务文档。
- 不默认后台持续轮询、自动运行、自动合并或自动放行GPU；需要时由用户发起下一轮。
