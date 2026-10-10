# VLM 下一步工作安排（ChatGPT 维护）

> 协作规则：**ChatGPT 负责研究规划与审查；Codex 每轮领取本文件中唯一 READY 的任务或任务包。一个任务包可依书面协议连续完成多项安全子任务，统一反馈后再审核**。执行事实写入 [codex-results.md](./codex-results.md)，脱敏附件上传 [codex-artifacts/](./codex-artifacts/)，ChatGPT 审核后更新 [research-overview.md](./research-overview.md)。
>
> 基准历史：[research-progress-2026-10-08.md](./research-progress-2026-10-08.md)（原始快照，不覆盖）。
>
> 更新日期：2026-10-10（北京时间；BATCH016禁代理CODE_LEVEL验收，BATCH017唯一READY（先离线修门，后一次条件式2视频V1）；真实媒体仍0）。本文是执行入口，不代表任何新模型实验已运行。

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
| VLM-DATA-GATE-009 | P0 | **USER_APPROVED_METADATA_ONLY（官方下载已完成；仅读已有资料）** | 用户与ChatGPT | 已批准并完成唯一Charades官方注释ZIP取得；011/012只读核查及原评测脚本查验属于既定有限元数据用途 | **禁止第二次下载、原CSV/ZIP编辑、原始标注与脚本公开分发、视频/STA/GPU/模型使用及原实验目录变更**；BATCH012已结束，若需媒体/额外数据必须用户再明确批准 |
| VLM-BATCH-009 | P1 | **STOPPED_SAFELY（路径名称误判；NO_DOWNLOAD）** | Codex | 授权与隔离预检、HEAD检查、通用元数据审计工具及合成测试；真实ZIP/CSV资格因保守路径阻塞未执行 | [首次提交bc16e38](https://github.com/floomeer83felix-source/vlm/commit/bc16e38eab35f454bc3e0ccc3c805c15c6009ed8)：5处约定交付，GET0/正文0B/P1P2 UNKNOWN；正确安全停止，**禁止原父任务重跑** |
| VLM-BATCH-009-FIX | P1 | **ACCEPTED（路径身份检查修复；未下载）** | Codex | 修正Windows absolute/resolve仅字符串不等的误报，加入samefile/设备inode/双链无reparse与缺失叶核验 | [修复提交dda8481](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)：2通用Python改动+一条附加结果；执行者报告21项合成测试通过、固定路径只读复核PASS；**未独立核Windows，也未下载或读CSV** |
| VLM-BATCH-010 | P1 | **ACCEPTED（一次官方下载与聚合交付；TIME_QUALITY HOLD）** | Codex | 官方小包1成功GET/3,519,822B、ZIP CRC/白名单、CSV schema、短域P1/P2记录候选聚合 | [提交8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)：严格2报告+1追加、原源码不改；66,500区间中19,625不通过既定数值规则，主因end>length；资格数仅过滤子集临时值，**不放行模型/视频** |
| VLM-BATCH-011 | P1 | **ACCEPTED（独立数值复算交付；时间语义HOLD）** | Codex，ChatGPT审查 | 只读原SHA固定CSV、官方README证据分级、互斥主因/δρ/异常行分布、独立复算P1/P2、测试及脱敏 | [提交1aed0de](https://github.com/floomeer83felix-source/vlm/commit/1aed0dea70faa7a446e63637be4772f4668270a2)：精确5处交付；原66,500/19,625、P1=347、P2=97,723均复现，但**时间合同仍无同版媒体/标注桥接**；不可当最终真值/新算法证据 |
| VLM-RESEARCH-DECISION-012 | P0 | **USER_SELECTED_CHARADES_ALIGNMENT（已决策，非READY）** | 用户、ChatGPT | 用户明确选择先修复Charades评测规则误配，暂不换数据集；但不批准原CSV编辑或数据/媒体/GPU再次获取 | [BATCH-012十项协议](./codex-artifacts/VLM-BATCH-012/README.md)：首先只读验证现有ZIP内官方`Charades_v1_localize.m`，再严格区分官方25时点相容性、越界质量、P1/P2语义；避免将评测兼容冒充真值修复 |
| VLM-BATCH-012 | P1 | **ACCEPTED（官方帧级label对齐；B/C时间真值HOLD）** | Codex，ChatGPT审查 | 固定ZIP原`Charades_v1_localize.m`只读源码与规则核对、纯stdlib 25点模拟/分层统计、19合成测试、匿名差异 | [提交e46f1d7](https://github.com/floomeer83felix-source/vlm/commit/e46f1d794118c5c2efbb0f15f0fc84dad5d4f04b)：恰好5处；官方正cell705,470、旧strict正cell398,287、差异307,183=官方正cell的43.54%；**只说明原strict不能代表官方frame-label政策，不认证视频端点/P1P2真值或新算法** |
| VLM-RESEARCH-GATE-013 | P0 | **USER_APPROVED_V1_CONDITIONAL（视频许可已批准，非实际下载）** | 用户、ChatGPT | 用户已额外批准最多2段Charades官方480p视频、远程GET正文累计≤64MiB、本地视频/临时文件≤128MiB，以及仅现有CPU容器和packet-PTS时间钟核验 | [已批准V1试点提案](./charades-media-boundary-pilot-proposal-2026-10-09.md)与[受限BATCH-013任务](./codex-artifacts/VLM-BATCH-013/README.md)；13GB整档、画面查看/解码、STA、GPU/模型与原科研目录仍禁止；按需Range不可行立刻STOP |
| VLM-BATCH-013 | P1 | **STOPPED_SAFELY（缺既有ffprobe，0媒体/GET）** | Codex，ChatGPT审查 | V1前置：SHA/源目录及工具检查，阻塞后仅交离线合成HTTP/ZIP安全组件 | [原013提交f86a1e8](https://github.com/floomeer83felix-source/vlm/commit/f86a1e8e7a2e31b40d9c1bd7f1b135d16ae25204)：规定5处交付；ffprobe有限范围未找到、16合成用例PASS（执行者报）、0网络请求/0视频；原父任务**已结束，禁止重跑** |
| VLM-BATCH-013-FIX | P1 | **ACCEPTED_CODE_ONLY（ZIP64/协调器/执行门；27合成测试）** | Codex，ChatGPT审查 | 原013完成后独立修补Python协调器/ZIP64/私有ledger/下载+packet-clock合成链路与防重复执行；本轮只有3处提交 | [提交75af33c](https://github.com/floomeer83felix-source/vlm/commit/75af33c56342bce4af94f7d70d1cada7ebdb8667)：2源码+1结果，执行者报27/27合成PASS、0真实媒体GET、0ffprobe；**代码未通过真实206/PTS环境验证，不是媒体实验GO** |
| VLM-CPU-TOOL-GATE-014 | P0 | **USER_APPROVED_ISOLATED_FFPROBE_INSTALL（授权已用作首次受限尝试；未完成部署）** | 用户与ChatGPT | 用户允许仅为CPU V1在独立目录下载安装经出版者哈希验证的ffprobe；BATCH014在已收取部分工具ZIP后超时安全停止 | 保留既有工具来源/版本/部署边界；**当前没有新READY**，工具尚不可用，下一次获取需在新父任务冻结断点恢复或重试与既有ledger连续性的证据，未经用户后续方向决定不自动发送工具GET |
| VLM-BATCH-014 | P1 | **STOPPED_SAFELY / CPU_TOOL_BLOCKED（工具GET超时，未安装）** | Codex，ChatGPT审查 | 固定Gyan 9.0.2发布方checksum/来源与路径预检、仅合成安装器测试、限额工具GET、静态审查013媒体代理 | [提交6bec3ab](https://github.com/floomeer83felix-source/vlm/commit/6bec3ab3e7e41571b8878e30c36b26ca710fd060)：严格5处交付，16个最终合成测试执行者报PASS；官网文本+工具GET正文共13,186,907B，其中ZIP部分13,107,200B后直连socket timeout；SHA全包/ZIP结构/ffprobe -version未做，原父任务**已结束，不可重跑** |
| VLM-CPU-TOOL-GATE-015 | P0 | **USER_RESUME_APPROVED_AND_EXECUTED（已验收，不再READY）** | 用户、ChatGPT | 用户许可范围内从旧部分ZIP有界续传完成，未重置014正文预算/账本 | 已由[BATCH015](./codex-artifacts/VLM-BATCH-015/resume-integrity-install-and-science-decision.md)执行者报告确认整包发布方SHA、CRC、白名单与单次ffprobe-version通过；原媒体ProxyHandler问题仍HOLD且GPU未授权 |
| VLM-BATCH-015 | P1 | **ACCEPTED（固定SHA完整ZIP续传与独立CPU ffprobe可用）** | Codex，ChatGPT审查 | 旧014部分包/ledger与来源身份核验，真实206强ETag，唯一后缀恢复，固定发布方SHA/ZIP CRC/最小提取/一次版本检查 | [提交b0d163f](https://github.com/floomeer83felix-source/vlm/commit/b0d163f9f9ea76c4887b08109a729d0bb47b4033)：恰好5处交付，执行者报27/27合成PASS、原part保留，HEAD2/GET2/206、完整SHA一致、`ffprobe 9.0.2`版本PASS、014+015工具实际正文114,847,784B；**仅工具已就绪，媒体/时间真值完全未运行** |
| VLM-MEDIA-CLIENT-GATE-016 | P0 | **CODE_LEVEL_VERIFIED（静态与合成，实网未验证）** | ChatGPT，Codex | 原`urllib`媒体默认代理已显式禁用，HTTPS固定3个官方地址、禁全媒体GET与HTTP重定向，40项纯合成测试 | [BATCH016代码报告](./codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md)记录完整客户端路径和合成证据；**不能据此声称S3有206或B/C时间真值PASS** |
| VLM-BATCH-016 | P1 | **ACCEPTED_CODE_ONLY（禁代理和精确HTTPS请求门；真实媒体仍未访问）** | Codex，ChatGPT审查 | 先前媒体程序默认代理隐患静态定位并修复，保留固定源/禁跳转和原安全预算规则 | [4c3e8bf](https://github.com/floomeer83felix-source/vlm/commit/4c3e8bf14ad9c62806be85e26e0492cfea5ebf93)：恰好5处，原27+新13=40合成unittest由执行者报PASS，0真实GET/ffprobe/GPU；**ledger读取后计费与父授权晚于版本调用两项新执行前门待017修复** |
| VLM-MEDIA-V1-GATE-017 | P0 | **USER_PREVIOUSLY_APPROVED_CONDITIONAL_TWO_VIDEO_V1（本轮须先安全补强）** | 用户、ChatGPT | 用户之前已明确批准仅2段官方480p Charades视频、媒体研究GET总正文≤64MiB、本地媒体/临时≤128MiB、CPU容器及packet PTS；视频媒体从未下载 | [唯一BATCH017任务](./codex-artifacts/VLM-BATCH-017/README.md)：先离线让授权在任何ffprobe/HTTP前验真，并在各网络read前持久化预算预留、≥52合成PASS；否则STOP且0媒体；成功才允许一次受限V1真实试点，任何ZIP/时钟问题不自动复做 |
| VLM-BATCH-017 | P1 | **READY（条件式：先安全门+合成≥52 PASS，再最多两视频V1 CPU时钟）** | Codex | 修严格父任务许可和读前持久计费；前置元数据SHA/隔离/CPU工具/官方Range206；只对合法唯一两目标下载与packet-PTS钟对照 | [BATCH017十项README](./codex-artifacts/VLM-BATCH-017/README.md)：原64MiB媒体预算不扩权，媒体GET≤12次，0下载整包/镜像/STA/视频画面/模型/GPU；2份脱敏报告+原媒体程序与test两处+1条结果共5文件，失败就STOP |
| VLM-PTS-001 | P1 | **INCLUDED IN VLM-BATCH-003（不可单独执行）** | Codex | 原PTS静态审计需求 | 按任务包子任务A执行，原[说明](./codex-artifacts/VLM-PTS-001/README.md)仅作背景；不重复上传 |
| VLM-003 | P1 | BLOCKED（旧gold区间诊断的manifest不再是当前路线；无新明确任务授权） | Codex | 原四臂manifest冻结，作为历史未执行工作保留 | 不得依据旧README/PR执行；任何新机制需新许可、来源、PTS、预算与用户授权 |
| VLM-004 | P2 | BLOCKED（需单独实验放行） | Codex | 小规模配对问答先导与独立复核 | 唯一 GPU 调用账本、完整分母、纠错/误伤、置信区间与成本 |

**当前唯一READY是VLM-BATCH-017，一次性、严格条件式的真实Charades两视频V1媒体时钟试点（首先离线补安全门，未通过则0媒体GET）。** [BATCH016提交4c3e8bf](https://github.com/floomeer83felix-source/vlm/commit/4c3e8bf14ad9c62806be85e26e0492cfea5ebf93)已通过GitHub静态审查：严格2匿名报告+媒体协调器与合成test两处+结果1条，执行者报告原27+新13共40合成PASS、`ProxyHandler({})`明确禁Windows/env代理继承、固定HTTPS官网2文本源/S3媒体ZIP来源、TLS默认验证与禁重定向，**本轮0真实媒体/ffprobe/GPU**。BATCH015已按发布方SHA部署CPU ffprobe9.0.2。遗留`Ledger`是read后累加而未先持久预留，`run_pilot`在父任务授权前就执行`ffprobe -version`，因此017先将父门/严格许可置于任何副作用前、所有文本+媒体GET用持久read前预算预留、保留原64MiB总体额度/12GET/128MiB媒体隔离/强ETag和HTTP206，全**合成≥52 PASS**且真实Windows元数据SHA/路径/工具预检均通过后，才准以**原用户已经明确同意的最多2段官方480p、仅CPU容器packet-PTS**范围，尝试从官方约13GB整ZIP通过Range索引和2个唯一MP4成员，禁止下载整个ZIP或镜像、不得转下载STA/长视频/GPU/画面分析。官方S3是否实际支持206、是否可在64MiB以内获取所需两个选定成员，**均未知，失败即STOP、不重试**。即使实际成功两段也只是2例媒体/CSV `length`时钟对照，无法证实原动作真实时间或外推19,625 strict越界token，B/C科学真值HOLD，novelty retain0/longvideoFAIL。仅新017父任务可执行，原013至016均已结案，不得重复或自动017后的任务。ChatGPT只核GitHub并创建新协议，尚未调用用户Windows或发送任何媒体请求。

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

## 十四、VLM-BATCH-011：Charades时间合同独立数值诊断（已验收，禁止重做）

**本节先前记录BATCH011的执行计划；该父任务已由1aed0de一次提交完成，不得再执行。最终科学状态见下方第十五节。**

**源事实与严格层级**：BATCH010官方ZIP SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，train CSV SHA`59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`、test CSV SHA`8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`（仅文件级，不是官方发布的独立SHA证明）。标注字段真实11列、7985/1863个视频行和157类别，原动作token 49809/16691；合法数值区间35211/11664，无效14598/5027。约75.5%视频行至少包含一个被旧规则拒绝的token，主因`end>length`；当前不能把剩余47k记录当物理事件完整真值。P1 347个同类有分离pair的组、P2 97723个异类相交pair**只是旧合同下幸存子集的几何候选，不是有效问答/新算法模型实验的许可**。

**独立官方时间合同**：[AllenAI原README](https://prior.allenai.org/projects/data/charades/README.txt)定义`actions`是`class start end`三元组，`length`为视频长度（秒），Changelog显示2017-02-27新增官方length，localize评测用25个时间点。这不能证明原CSV所有标注已无冲突，也不能通过变换时间单位来消除不通过的分母。具体数据质量根因仍UNKNOWN：既可能是标注/视频修订，也可能审计器的时间假设不适用或其他错误，不能无证据归责于官方数据。

**受限十项执行协议**：[VLM-BATCH-011 README](./codex-artifacts/VLM-BATCH-011/README.md)。用户已批准的小包下载**已经发生，不能再次GET**；只有使用固定Windows隔离目录`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`内现有CSV只读计算和官方公开文本查验可做。执行次序：①SHA/权利确认②官方时间定义及版次③独立CSV解析交叉核④互斥与重叠异常flag⑤end-length差额桶⑥每视频异常token个数聚合⑦P1子集资格验证⑧P2子集资格验证⑨隐私、来源、分母审计⑩`HOLD_TIME_CONTRACT`或证据支持下的下一步止损。禁止查看/上传原始单行、视频ID/subject/描述、低样本可逆表，禁止数值截断/猜测缩放。需先在合成数据完成stdlib单测再读真实CSV；数据/原脚本不能改变。

**只允许5处GitHub交付**：`docs/codex-artifacts/VLM-BATCH-011/`的2份脱敏报告，`prototypes/`的2份新通用只读脚本（非旧审计器修改），`docs/codex-results.md`末尾1条父任务回报。禁视频/STA、模型/GPU、真实视频PTS测量、原研究工作区与锁/conda更改、任何数据/标注再次下载及外部联系。出现审计器不稳定/真实hash不符立即停止、不得覆盖旧收据。Codex成功单次push后停止，待ChatGPT验收。

## 十五、BATCH-011验收与先前路线抉择（历史已结束）

**交付验收**：实际[提交1aed0de](https://github.com/floomeer83felix-source/vlm/commit/1aed0dea70faa7a446e63637be4772f4668270a2)恰好改5处：`docs/codex-artifacts/VLM-BATCH-011/`两份脱敏报告、`prototypes/`两份全新stdlib脚本、`docs/codex-results.md`追加一次。无ZIP/CSV/个人映射进入GitHub，未修改旧原型/原科研资产。执行者报告原隔离ZIP/train/test SHA均与010固定值一致，旧规则的66,500原token/46,875通过/19,625失败、P1 347组/P2 97,723pair及其它参照聚合一致。它证明**两个解析实现按同一个条件给出相同计数**，不证明该条件被真实媒体时间语义支持。执行者报告合成测试首次14 PASS，增强补充披露后15 PASS，**增强后的完整程序未再实跑真实CSV**；ChatGPT仅审查GitHub结果与代码，不声称本机复算。

**新增记录级事实**：越过length的动作区间中，至少8,747条超过1而不超过5（以文档所述秒尺度解释）；异常token/视频行总比率约29.5%/75.5%，Train/Test异常行比例约73.8%/82.5%。347个P1合格同类组有270个所在行另有数值异常；97,723个P2有效几何重叠pair有67,280个所在行另有异常。余项77组与30,443对也只是在“当前数值规则且整行未包含异常”的**关联计数**，不是跨媒体/语义验证成功的真值样本。当前`DATA_INTERVAL_QUALITY=HOLD_RANGE_CONFLICT`，`TIME_CONTRACT=HOLD`，`DATASET_FOR_NATURAL_LONGVIDEO=FAIL`，`ORIGINAL_MECHANISM=RETAIN0`，`GPU=BLOCKED`。

**外部新颖性危险信号（公开资料，不扩展数据授权）**：[ACL2025正式长文 Perfect Times](https://aclanthology.org/2025.acl-long.1000/)已从Charades视频构造时间关系与动作完成/持续的多语种VLM问答；[作者公开仓库](https://github.com/ologin/PerfectTimes)声称包含更新的时间顺序动作注释`video_annotations.csv`及问答生成器。该工作不是P1“同类重复实例”命题的严格同一对象证明，但直接覆盖了“用Charades动作时间关系自然语言QA得到新基准/机制”这一宽泛新颖性宣称。不要下载其视频/注释或直接调用repo脚本，版权/来源修订和科学先例对比仍待独立授权/定义。

**研究下一门`WAIT_USER_DIRECTION`而不是BATCH012自动READY**：A. 如果继续Charades，则先找到**无需未获授权媒体的可靠同版标注时间坐标来源、修订记录和与length同原点的证据**，并且提出相对于ACL2025 Perfect Times与TAL/TMR强基线独有的可辨识问题；若找不到则STOP Charades作为核心证据。B. 如果目标是自然长视频VLM创新，优先选择**可公开申请/无需审批而具合法原媒体和可验证时间真值、跨源独立的真正长时域基准**，重新单独授权最小必要数据；不要因Charades样本非零而继续无边界元数据/合成研究。用户未选定前0新READY、0第二次原Charades小包下载、0新数据/视频/STA、0GPU及原Windows资产改动。

## 十六、VLM-BATCH-012：官方定位评测政策对齐已验收（禁止重做）

**以下十项为历史已执行计划，不再是Codex新授权。BATCH012只完成官方标签政策工程对齐，未修正原动作或通过媒体真值门。**

**用户2026-10-09明确答复“同意”**：优先修复当前Charades的`end>length`检查与官方frame-localization标准的不一致，暂时不转向另一个数据集。此次是**口径/评测兼容性修复**，不是修改或重新发布原始标注。原ZIP和两个CSV仍在Windows固定隔离目录；用户没有批准任何新媒体、STA、GPU或原Windows研究环境改动。

**核心对照**：旧两套数值程序一致复算66,500原动作token中19,625不通过`0≤start<end≤length`，但该强条件是为评估精确区间真值而自设的筛查，不能假定它是官方frame-mAP要求。官方[Charades README](https://prior.allenai.org/projects/data/charades/README.txt)写定位在`j*length/25, j∈{0,…,24}`取25个时间点。官方脚本`Charades_v1_localize.m`原字节已经在合法取得的Charades.zip中（是否真实存在仍由任务执行时安全确认）；只许**用zipfile内存读取短文本，不提取到磁盘，更不执行MATLAB**。原包SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，两个CSV SHA与010/011保持一致；签名不符STOP。

**10个具体子任务与交付**：[VLM-BATCH-012 README](./codex-artifacts/VLM-BATCH-012/README.md)冻结：①授权/SHA/目录身份；②ZIP中实际官方定位评测器的时点和端点比较证据；③官方frame label、数值边界质量、实例/关系语义真值三层严格区分；④标准库实现有来源证明的25点标签采样；⑤先运行全合成反例unittest；⑥旧strict与官方标签的匿名正cell/记录差异；⑦越界类型与官方可命中采样点数量；⑧P1/P2既有347/97723候选对边界的保守影响，不臆造真实顺序；⑨仅聚合脱敏/小格及互补抑制；⑩`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY`、`TIME_RANGE_QUALITY`与`EVENT_TRUTH`分别判PASS/HOLD/FAIL。若原评测器缺失或规则不能静态核，报告`UNKNOWN`而非伪造官方相容性；不能仅靠30%端点越界证明原数据坏。

**仅允许5处GitHub提交**：`docs/codex-artifacts/VLM-BATCH-012/`两份脱敏报告，`prototypes/`两份纯stdlib全新对齐器+合成测试，`docs/codex-results.md`末尾**一条**012父任务回报。0其它原始数据/标注/官方脚本全文上传、0旧程序修改、0源目录写入、0下载/视频/STA/推理GPU/训练、0原Windows研究文件/conda/锁/账本触碰。一个正常push成功后停止当前轮，由ChatGPT审查再决定是否仍需同版媒体时间证据或改数据集。**修复A不自动宣布B/C PASS**。

## 十七、VLM-RESEARCH-GATE-013：用户已批准条件式最小视频V1访问（历史方向决策）

**状态更新**：本节原文曾记录“等待视频访问授权”，现用户已经明确批准**限制在2段/64MiB/CPU packet-PTS的条件式V1**。该历史等待描述不再是当前状态；当前唯一可执行任务见下方BATCH013与顶部任务表。**视频尚未访问，不能把READY当已成功取得媒体。**

**最新替代决定（2026-10-09）**：用户已明确选择方案A，不再等待选择A/B；但仅选择研究方向**不构成媒体下载授权**。具体试点范围、官方整ZIP无法逐视频直接点取的风险、预算及未来授权条件以[方案A试点提案](./charades-media-boundary-pilot-proposal-2026-10-09.md)为准。以下保留了BATCH012验收时的历史判断。

**BATCH012审查报告**：[官方代码/政策](./codex-artifacts/VLM-BATCH-012/official-evaluator-code-and-policy.md)、[三层宏观对照](./codex-artifacts/VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)、[提交e46f1d7](https://github.com/floomeer83felix-source/vlm/commit/e46f1d794118c5c2efbb0f15f0fc84dad5d4f04b)。按唯一SHA固定Charades ZIP内官方评测器的文本静态证据，25点时间采样为`(j/25)*length`（零基j=0…24；对应MATLAB先除后乘操作次序），原动作class区间`start<=t<=end`两端包含，多同类动作仅令对应真值cell置1，而不是累积事件实例。官方frame-localization**不要求**先通过`end<=length`才构造正label；旧`0<=start<end<=length`是我们额外的严格时间区间资格筛选，不能代表官方评价政策。

**三层结论不能串门**：A`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY=VERIFIED_WITHIN_STATED_SCOPE`（仅限合法原ZIP评测器文本转义与有限规范数值模拟；未经MATLAB端到端mAP/媒体帧认证）；B`TIME_RANGE_QUALITY=HOLD`（仍有19,625原动作不满足额外strict规则，不能因frame-hit宣称每条端点真实正确）；C`P1/P2_EVENT_TRUTH=HOLD`（实例身份、完整正负事实、媒体PTS/同版映射、自然来源独立性尚无证据）。执行者报告官方正cell705,470、strict正cell398,287，差异307,183个（43.54%的official positive cells），非独立动作N，也不是mAP。原strict可评同类重复347组与异类交叠97,723对仍未升级科研真值。纯合成unittest 19 PASS，原CSV只读分析一次，ChatGPT仅静态审查GitHub结果，**未独立实算用户Windows上的原CSV**。

**科学止损与下一最小证据门**：既有[ACL2025 Perfect Times](https://aclanthology.org/2025.acl-long.1000/)与动作时序QA工作使简单Charades时间QA缺原创性；Charades本身均长约30秒，不能单独提供自然长视频论文最终确认。为避免一轮轮工程复盘，暂停分配新任务：用户可选择①未来另行核定具体**合法小规模视频＋同版媒体PTS/帧时钟**证据以评估B/C（必须先明确授权、样本上限及隔离来源，现未允许），或者②把Charades保留为**短视频工程/官方frame-mAP对照**，先做无需下载的长域新数据集许可/时间合同研究方案，之后再明确授权所需数据。**任何选项都不自动放行GPU或原研究环境。** 无新用户指令前`VLM-RESEARCH-GATE-013=WAIT_USER_SCOPE_DECISION`、0READY、0媒体/STA/额外数据/模型调用。

## 十八、VLM-BATCH-013：已在CPU工具门安全停止（历史父任务，不得重跑）

**本节以下内容是013原执行前的任务计划，现已因缺既有ffprobe安全停止；其后FIX只是源码审查交付，当前不允许按此旧任务再次联网或启动。最新状态见下方工具门。**

**新增用户明确授权（2026-10-09）**：方案A继续Charades，同意仅官方480p视频最多2段、总HTTP GET正文**≤64MiB（67,108,864B）**，包含ZIP尾部、中央目录、远程local header和成员及一切失败传输字节；本地全部本轮媒体+临时字节**≤128MiB**。仅使用已有CPU软件读取容器与**packet PTS**，不可观看/导出视频帧、不进行视觉动作时间标注；禁止13GB整包或所有用户未同意的GPU/模型/原工作区变更。

**技术约束**：官网是13GB 480p ZIP URL，**不存在已证实的官方单视频公开URL**。可能的ZIP Range读取须遵守HTTPS官方域、稳定对象/ETag、每个GET实际`206 Content-Range`、拒绝`200`全包、网络全局ledger≤64MiB、最多12次Range请求、远程ZIP64/EOCD/中央目录及成员CRC/symlink/path/offset验证，所有前置合成安全测试先PASS，才允许任何真实视频Range。成员匹配来自已固定SHA的本地train CSV，确定性私密选择1个越界`start<L<end, end-L∈(1,5]`与1个干净对照；如果两者无法在官方包中安全唯一取得且预算足够，则STOP，不选择方便的替代、不改任何CSV。

**物理隔离**：`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，独立于原`Charades-v1-Metadata`、公有Git docs、RTX3090实验树和同步目录。保留媒体仅本地，不上传GitHub。执行者先核路径祖先/reparse、原metadata包SHA/许可、剩余磁盘空间≥512MiB、`ffprobe`已存在；缺工具/路径不清则STOP，不安装依赖/改conda/启动原GPU。

**分析层级与私密交付**：V1对照CSV`length`与所选2个MP4容器duration/start、视频stream`time_base`/rate、首末**packet PTS/DTS**等值；包时间戳不等于已解码帧时间与真实视觉动作完成。GitHub只能披露粗类别化CASE_OVERFLOW/CASE_CONTROL时钟匹配与可审查的方法/预算收据，不能公开视频/subject IDs、两例精确时长/端点/PTS、帧、ZIP或媒体sha。即使2例匹配，B区间质量和C事件真值仍HOLD，不能泛化至19,625条旧越界token；V2视觉核验需另外申请用户授权。

**十项执行与严格交付**：[BATCH013完整README](./codex-artifacts/VLM-BATCH-013/README.md)顺序为①授权/环境/源SHA②确定性私有样本③官方Range协议④安全ZIP索引⑤仅需两MP4受控下载⑥CPU ffprobe packet时间⑦与CSV时间合同比对⑧科学止损⑨预算/身份/合成单测⑩三层裁决；第⑨测试**必须在任何真实GET之前通过**，允许前置排列。只交5处：`docs/codex-artifacts/VLM-BATCH-013/`2份**脱敏**报告；`prototypes/`2份不含真实数据的通用stdlib代码和合成unittest；`docs/codex-results.md`末尾1条013父结果。**单次普通push后STOP**；任何下载失败/源无法安全索引即`BLOCKED`，不是必须花完授权额度。

## 十九、BATCH-013-FIX代码交付验收与CPU工具授权更新（历史）

**后续状态更新**：本节此前称“未获工具安装许可”，但用户已在2026-10-09明确批准**仅独立CPU ffprobe工具**的下载/隔离安装。原013不可重跑；当前唯一READY为下方BATCH014。媒体访问/代理直连仍HOLD，详见[工具任务](./codex-artifacts/VLM-BATCH-014/README.md)。以下旧文本保留为决策历史。

**明确区分父任务和修复**：原013提交[f86a1e8](https://github.com/floomeer83felix-source/vlm/commit/f86a1e8e7a2e31b40d9c1bd7f1b135d16ae25204)完成5处交付，但由于PATH、常见位置及有限登记runtime候选未找到既有ffprobe，正确在第1项停止。没有选真实视频、未访问官网Range/HEAD、媒体GET/正文0B、PTS/clock UNKNOWN；不能称已下载失败或官方服务器不支持206。新的[75af33c代码修复](https://github.com/floomeer83felix-source/vlm/commit/75af33c56342bce4af94f7d70d1cada7ebdb8667)共3处：更改已有通用协调器与synthetic unittest、`docs/codex-results.md`追加一条独立`BATCH-013-FIX`，没有再次运行原013。Codex报告5轮合成测试最终27/27 PASS，ZIP64/受限传输/本地ledger/取两成员/mock-ffprobe链条与父任务完成后禁止执行检查得到合成覆盖；**ChatGPT仅核文件/源码及测试方法，未在用户Windows实测或真实GET**。这只能标`ACCEPTED_CODE_ONLY`。

**下次执行前的额外独立安全核查**：当前源码`urllib.request.build_opener(NoRedirect())`可经Python默认ProxyHandler继承环境/系统代理；这与既定“不得通过代理/镜像取得视频”的协议可能冲突。其网络运行须明确拒绝或禁用代理，并增补相关纯合成测试；不能因27项通过就声称直连/来源安全已PASS。其他如HTTPS官方页面源码anchor、206/ETag、ZIP64具体格式、Windows reparse/CPU工具独立路径、两视频都在预算内仍未实地验证，继续由fail-closed机制限制。

**唯一待用户决定的`VLM-CPU-TOOL-GATE-014=WAIT_USER_TOOL_SCOPE_APPROVAL`**：是否批准由Codex在**不触碰原科研环境、不改PATH/Conda**的独立`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`部署一个经过公开来源、哈希与安装体积审计的**CPU ffprobe工具**，只为未来V1 packet-PTS研究使用。**目前没有安装许可**；来源、最终文件大小、合法分发与下载预算亦未最终冻结，故不得自行下载或安装。若用户同意，先只建立独立来源/体积核验的最小协议；同时由ChatGPT检查代理防护并另授新唯一READY父任务，**不重跑已结束013**。如果拒绝则保持媒体试点阻塞，原≤2视频/64MiB许可不会自动扩大。B/C事件真值、GPU和视频画面仍HOLD。

## 二十、VLM-BATCH-014：工具获取因直连超时安全结束（历史任务）

**本节以下曾是BATCH014的执行前许可/任务计划。实际BATCH014已由6bec3ab结案，工具ZIP仅部分下载、ffprobe未安装，不得重跑本父任务；现以顶端任务看板和下一节的015决策门为准。**

**新增明确用户授权（2026-10-09）**：允许我们**仅在**Windows`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`部署经来源、发布方SHA与体积核验的CPU ffprobe，不改原Conda/PATH/研究工作区/CUDA或其它软件，不自动启动视频/媒体/Packet-PTS、GPU/视觉。ChatGPT这轮只更新Github任务与研究文档，**没有访问用户Windows、没有下载工具或视频**。

**独立供应链依据**：[FFmpeg官方](https://ffmpeg.org/download.html#build-windows)公开承认直接只提供源码并给出Windows预编译[Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)入口。Gyan明确发布`ffprobe.exe`且其64位静态包按其说明为GPLv3，release essentials固定FFmpeg 9.0.2，ZIP页称约109 MB。本次**冻结而非使用随日期变化的latest**：`https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip`，与同发布者`.sha256`文本严格核对固定`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`。发布方SHA只是**同源完整性检验**，没有独立开发者数字签名证明；HTTPS重定向/包内容/许可版本任何一项改变就STOP。默认无代理直连、不安装7z、winget、conda或修改PATH。

**资源限额与执行门**：本批**只针对工具**所有GET正文合计`≤150MiB`，私有ZIP/临时/只提取ffprobe与许可证总本地占用`≤512MiB`，磁盘剩余≥1GiB；必须检查实际LOCALAPPDATA/云同步/原工作区物理路径隔离及reparse、事先跑合成HTTP和ZIP安全单测≥12、无任意软件或数据执行；只有发布方checksum一致、完整ZIP SHA匹配、白名单ZIP安全、`ffprobe.exe -version`成功才标工具就绪。不得向公共Git提交工具包、exe或私人目录信息。

**单一任务[完整README](./codex-artifacts/VLM-BATCH-014/README.md)共10项**：①项目/权限/单READY②隔离与磁盘③供应链/GPL和固定checksum④先做synthetic安全反例⑤无代理TLS/限额下载ZIP⑥安全CRC及白名单提取⑦独立exe仅`-version`⑧媒体网络协调器代理漏洞**静态**审查，留下一批修复⑨资源和脱敏收据⑩工具/媒体分门决定。**只允许5处GitHub交付**：`docs/codex-artifacts/VLM-BATCH-014/`2脱敏报告、`prototypes/`两份独立stdlib安装工具+纯合成测试、`docs/codex-results.md`末尾一次父任务回报。成功提交后STOP，原Codex聊天继续留存。

**科研主门继续HOLD**：BATCH014成功仅是工具的`CPU_TOOL=AVAILABLE`，**不是**已从Charades官网取得两段媒体、更不是视频时钟/原标注结束点或P1/P2语义真值已验证。BATCH013及其FIX都已结束；后续必须先单独修复媒体客户端`urllib`代理继承问题，并由ChatGPT新建唯一READY父任务后才可在旧用户限额授权内考虑有界媒体访问。不能自动重跑013。TIME_BOUNDARY_QUALITY=HOLD，P1/P2 EVENT_TRUTH=HOLD，NOVELTY RETAIN0，长域FAIL作为Charades单独确认，GPU BLOCKED。

## 二十一、VLM-CPU-TOOL-GATE-015：用户选择安全断点续传（历史决策）

**2026-10-10补充**：用户已选定继续安全断点续传，不再处于等待A/B方向。以下历史文本中“等待用户”仅为当时状态；最新可执行入口是下方唯一BATCH015。**仍没有远端ETag/206或原本地文件的直接验真，因此必须fail-closed。**

**安全止损收据**：原[6bec3ab](https://github.com/floomeer83felix-source/vlm/commit/6bec3ab3e7e41571b8878e30c36b26ca710fd060)严格5处文件。原[供应链与资源报告](./codex-artifacts/VLM-BATCH-014/tool-source-integrity-and-isolation.md)与[代理继续HOLD报告](./codex-artifacts/VLM-BATCH-014/ffprobe-readiness-and-proxy-hold.md)记录官方引导、固定Gyan 9.0.2发布方checksum`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`文本通过；但工具ZIP只接收到**13,107,200B**后socket timeout。本轮网页/校验文本及工具ZIP所有GET正文累计**13,186,907B**，一次工具尝试、0重试、0完整ZIP、0CRC/白名单提取、0`ffprobe -version`；在本机新隔离根遗留部分`.part`与私有账本两个文件总13,107,774B。完整包SHA与FFprobe可运行性均UNKNOWN/NO。此为**安全停止并如实报告**，不是工具安装成功。执行者报最终16纯合成test PASS（初次测试曾FAIL，修复后通过），ChatGPT只核GitHub静态证据未远程复跑。

**恢复的科研经济原则**：不应因13MB已取得就无条件再尝试109MB。若用户决定继续，优先以**不执行旧014**的新最小任务检查在原冻结对象上是否有稳定ETag/长度/HTTP Range206，并在新合同中一次性限定只允许相同对象继续读剩余字节；现有13,186,907B必须接续累计记账，不能另算150MiB；原13,107,200B部分数据要在同版、可靠offset及文件完整性可证明时才可用，否则STOP并重新征求方向。不可更换到别的发布包、最新版本、镜像或原Windows研究目录，不做任何视频/ffprobe PTS实测，更不可复用已完成013/014任务入口。

**尚需独立解决的技术债**：原[013媒体协调器](../prototypes/charades_range_media_clock_pilot.py)仍可能从`urllib`默认ProxyHandler继承环境/Windows代理。014工具安装器已显式禁代理，但不代表旧媒体程序已修复；就算以后ffprobe可执行，仍需新父任务在合成反例中先证明媒体端禁代理、预算与ZIP成员安全，再考虑已另行批准的最多两视频/64MiB V1试点。当前无任何媒体GET/GPU授权扩大，Charades B边界和C事件真值继续HOLD，科学创新retain0。

**状态**：`VLM-CPU-TOOL-GATE-015=WAIT_USER_CONTINUATION_CHOICE`（非READY）。等待用户说“继续做安全续传方案”或“暂时停止工具路线”；**本轮GitHub状态更新不是要求Codex马上再次联网**。

## 二十二、VLM-BATCH-015：强ETag/206与ffprobe独立工具就绪验收（历史已结束）

**2026-10-10最新执行事实**：015已由b0d163f完成并经ChatGPT验收，旧part后缀、发布方整包SHA与版本检查报告PASS；原015计划不再可执行。仅公开协议与历史，不得重跑或自行消费剩余工具/媒体预算。最新唯一READY转向下方BATCH016离线HTTP禁代理代码修复。

**新增用户决定**：明确“继续安全断点续传方向。请先核对原部分工具包、同源ETag/Range206、剩余累计预算及安全条件，在GitHub制定新的有限任务；禁止重跑014，不得下载Charades媒体或使用GPU。”本批是**工具供应链已批准范围内的新、仅一次条件性续接**，不构成新的150MiB额度或新的Charades数据授权。

**可核而尚未验的事实**：Gyan目前公开9.0.2 release essentials ZIP约109MB，发布方SHA`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`沿014冻结；旧014报告的原part=13,107,200B、原ledger body=13,186,907B，工具全部GET上限157,286,400B故剩余144,099,493B。ChatGPT仅阅读GitHub收据与旧安装器代码，未访问用户Windows上的`.part`或`tool-ledger.json`；尝试自身无代理直连HEAD得到DNS解析失败，**不能声称Gyan当前服务器Range206、ETag或真实Content-Length通过**。若已存在原part不一致/旧ledger缺失/源码发现不能安全append/禁代理，则STOP，不得猜。

**十项强制合同**：[完整BATCH015 README](./codex-artifacts/VLM-BATCH-015/README.md)：①Git单READY与014已结案核验；②原固定WindowsCPU工具根的.part/旧只读ledger/隔离/空间核验；③合成至少18 tests先PASS；④对同一固定Gyan URL只发最少HEAD（新强ETag只证明新会话稳定，旧ETag未留存）；⑤用真实`206`先读≤4KiB原part边界匹配，再只允许一次`If-Range`强ETag保护的后缀Range正文追加，200/416/代理/跳转/超限立即STOP；⑥SHA验证整份发行包后才算补全同源；⑦ZIP/CRC/白名单提取，独立exe只能`-version`；⑧CPU工具与媒体/V1科学门分离；⑨原014账本不改、另建累计继承的新持久ledger及匿名报告；⑩明确STOP和预算收据。**新增工具GET最多2次，0自动重试；014+015所有工具GET正文≤150MiB，磁盘≤512MiB，源版本9.0.2和SHA不变，完整SHA不符则无任何exe执行**。

**GitHub只许5处**：`docs/codex-artifacts/VLM-BATCH-015/`两份脱敏报告，`prototypes/`两份全新通用std-lib resumer/tests，`docs/codex-results.md`末尾一条父结果。不允许编辑014旧原型/测试/报告，013旧媒体协调器、原数据、原科研工作区、Conda/PATH、现存part前缀和ledger历史、其它看板/总览；0Charades视频/Range/PTS/GPU/模型/视觉/V2。成功push后STOP，ChatGPT验收后才能决定媒体程序代理安全修复的新任务，**不能自动重跑013/014**。

## 二十三、VLM-BATCH-016：媒体客户端禁代理/HTTPS安全代码交付已验收（历史）

**2026-10-10历史状态补充**：BATCH016按4c3e8bf已结案为`ACCEPTED_CODE_ONLY`，此前本节“016唯一READY”属执行前历史文字。当前可执行入口为下方017：原受限V1媒体许可仍有效，但先修授权/账本并通过全部synthetic门，失败绝不联网。

**先验工程突破的科学边界**：BATCH015 Codex实际取得114,768,076B的Gyan 9.0.2 ZIP整包，由014旧13,107,200B前缀和唯一206后缀拼成；SHA256与供应商固定值`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`匹配，并通过全成员CRC、白名单最小部署。执行者报CPU ffprobe `-version`成功（9.0.2），工具旧GET+新GET实际合计`114,847,784B`、剩余`42,438,616B`，无独立开发者签名或ChatGPT机器本地复验。`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED`，**只表示以后有CPU packet检查工具，不是任何Charades视频/媒体PTS数据、原时间误差已验证。**

**下一唯一阻塞项**：旧[013-FIX媒体客户端](../prototypes/charades_range_media_clock_pilot.py)`RangeClient`构造`urllib.request.build_opener(NoRedirect())`，默认会安装受环境/Windows代理影响的ProxyHandler；这有违原限制的直接官方HTTPS来源/禁止镜像代理。`MEDIA_CLIENT_PROXY=HOLD`，不得因为015工具部署成功而自动运行原013父任务（已结案）或视频V1。用户此前允许最多2段官方480p/总GET≤64MiB/本地媒体≤128MiB/V1只读取CPU packet时钟，但**BATCH016这次仅执行纯源码/模拟测试**，实际0 Charades/media/Gyan HTTP，0 CPU ffprobe调用/视频/PTS/GPU/模型。

**新[8项受限任务书](./codex-artifacts/VLM-BATCH-016/README.md)**：①安全fast-forward和唯一READY+历史父任务核验；②逐个检查既有代码的官网许可页面、S3 ZIP HEAD和Range是否继承代理；③仅修改原媒体协调器显式`ProxyHandler({})`、TLS默认验证、无重定向/固定官方HTTPS域，保留原流量/目录/ZIP防护；④修改原合成测试覆盖污染代理设置、系统代理检查被模拟为异常、共享opener/HTTP降级、错误响应不读正文等，最终≥30纯合成用例PASS；⑤禁止`run_pilot(execute=True)`及任何真实网络/ffprobe执行；⑥提交前检查只有受限网络安全差异；⑦恰好5处：2份016脱敏报告、原媒体代码、原测试、`docs/codex-results.md`追加一次；⑧`CODE_LEVEL_VERIFIED`与`REAL_MEDIA_RANGE=UNKNOWN`严格区分，推送后STOP等ChatGPT验收。任何模拟测试发现额外未覆盖风险→报告HOLD，不得为了通过扩大权限/下载来源或放宽预算。

## 二十四、VLM-BATCH-017：安全门先行、仅一次有界真实视频V1时钟核验（唯一READY）

**前批结论**：[BATCH016报告](./codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md)与[纯合成收据](./codex-artifacts/VLM-BATCH-016/code-only-test-and-science-gate.md)对三固定官方HTTPS来源的`urllib`显式禁代理、TLS证书验证、禁止重定向/整包GET的代码修补提供静态证据；执行者报40合成PASS；两真实数据未获取、CPU工具未执行、媒体PTS仍未知。本批首次将实际媒体尝试安排在**事先用户独立批准过的最多2段/媒体HTTP GET正文≤64MiB、本地媒体≤128MiB、CPU packet-PTS**预算之内，不因Gyan工具106MB续传事实推断AllenAI视频服务器同样支持Range。

**017的前置安全修复（无任何真实研究网络）**：必须先将原`Ledger`从`response.read`后才`add`改为**每次≤64KiB读取前原子持久保存预留上界、crash/短读保守计费不退**，同时让`run_pilot`先核`VLM-BATCH-017`唯一READY+未回报+明确的媒体许可scope、后允许检查独立CPU ffprobe，否则连版本调用都不能执行。保持原BATCH016的显式禁代理/HTTPS白名单；旧40 synthetic test全部保留、至少新增12个极端反例，**≥52 PASS**后才准读取真实原CSV/ZIP与官方媒体网站。不通过直接STOP、0媒体网络字节；新程序不能为修bug任意扩大许可/改数据源/降低安全阈值或重新跑013/014/015/016。

**真实一次性分支（前置全部通过才触发）**：在用户Windows受限`Charades-v1-Metadata`中只读核固定原元数据CSV/ZIP SHA、原研究工作区及同步/跨目录reparse边界；唯一新媒体根`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`事先不存在、按冻结算法私密选一例`0≤start<length<end,end-length∈(1,5]`和一例整行strict合法且相近长度的train视频。检官方项目页/许可仅两个文本固定来源且计入64MiB，官方S3 ZIP须有唯一实际URL、HEAD稳定强ETag/长度，全部尾部/ZIP64中央目录/local header和两成员请求都需真实HTTP206，回应HTTP200整个13GB时**不读任何正文并STOP**；GET总≤12，所有实际+保守预算≤64MiB，原包CRC/成员身份/文件展开预算≤128MiB。不能拿服务器目录结果重选“恰好能拿到的更小视频”。任何前置、远端、预算、ZIP/媒体工具阻塞就一次STOP，不下载整包/改镜像/新模型。成功后仅`ffprobe` CPU容器/packet PTS同CSV`length`和越界end做两例类别化对照，不执行画面/帧解码、人工物理动作重标、GPU。

**10项任务与严格交付**：[017 README](./codex-artifacts/VLM-BATCH-017/README.md)依序：父授权→记账/授权入口代码修复→≥52合成单测→隔离/来源/CPU工具实地预检→冻结两例→按需真实206 ZIP安全索引→≤2成员受限落盘→仅CPU ffprobe video packets→隐私/账本收据→层级裁决并STOP。GitHub只准5处：2份脱敏试点报告，更新原`prototypes/charades_range_media_clock_pilot.py`与原合成test，向`docs/codex-results.md`末尾追加**1条017父任务**，任何非白名单文件不改；不得公开视频ID/subject、细时长/PTS/类/私人路径/ZIP成员、原真实注释行或受限媒体，保留既有隔离工具/元数据/原科研工作区/所有历史报告与任务板不改。主科研结论：A旧012仅frame标签口径VERIFIED，B时间质量/C P1P2事件真值仍HOLD，Charades独立长域外推FAIL/创新retain0/GPU BLOCKED。**新017须用户在原Codex聊天显式触发，GitHub READY不等于自动实验。**

## 二十五、当前研究判断（跨批保持）

- 用户保持高水平论文目标，但不假定一定成功；目前 retain 0。前期100/300题及各种已关闭候选、GAP7、BATCH-003至006**不得重跑**。
- 新机制创新门 `N`、可证伪性 `T`、非平凡有效性 `U`、合法可用标签/媒体 `D`、预算/PTS/来源 `B`、强baseline公平比较 `F` 当前**无候选PASS**。toy通过不提升这些门。
- 历史真实媒体PTS /同版剪辑/来源独立性、答题数据许可、评分隔离和真实token成本仍未在新来源验证。只做纯symbolic toy不需要视频许可，但不能由此推导真实数据可执行性。
- PR #1未合并且主要基于旧gold路线；不可直接执行旧manifest或旧GPU预算。新问题可能需要不同证据标签，先做学术可识别性/合法数据核查，再决定是否值得付出真实实验。
- 如果十项研究全部被直接先例或现实标签门否决，回报**RETAIN 0 / STOP PORTFOLIO**，不继续为凑10项编新算法。

## 二十六、GitHub协作规范（不改变）

- ChatGPT维护`docs/next-steps.md`、`docs/research-overview.md`和科学立题文档；Codex仅执行唯一READY父任务并追加`docs/codex-results.md`及README明确的脱敏产物。
- 原始`docs/research-progress-2026-10-08.md`保持永久快照；历史已验收任务和原Windows RTX3090/conda`pytorch`实验工作区与公开文档checkout严格分开。
- 每轮用户在原Codex聊天发送继续信号，Codex按远端main而非旧缓存执行；安全提交1次后停止，不force push、不自动后台运行/轮询、不唤醒Codex。
