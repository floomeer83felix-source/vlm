# VLM 长视频研究总览与决策日志（ChatGPT 维护）

> **定位**：滚动总结，不取代原始实验档案，也不宣称每次都已对本地实验原始账本独立复算。
>
> 更新：2026-10-09（北京时间；用户切换到Charades公开数据入口，BATCH-008唯一READY／0下载／0GPU）  
> 研究目标：形成经严格实验、创新性审查和跨来源/模型复核支持的长视频视觉推理研究，目标投稿层次参考《计算机学报》，不保证录用。

## 0. 研究协作入口

| 角色/材料 | 文件或链接 | 编辑规则 |
|---|---|---|
| 原始阶段快照 | [research-progress-2026-10-08.md](./research-progress-2026-10-08.md) | 历史事实，不覆盖 |
| ChatGPT 下达任务 | [next-steps.md](./next-steps.md) | ChatGPT 负责维护 READY/BLOCKED 与验收标准 |
| Codex 回传执行事实 | [codex-results.md](./codex-results.md) | Codex 只追加结果，保留失败/未知 |
| Codex 脱敏审计附件 | [codex-artifacts/](./codex-artifacts/) | Codex 仅提交当前 READY 任务允许的小型文本附件；原始研究资产不上载 |
| ChatGPT 审查与全局判断 | 本文件 | ChatGPT 根据反馈更新结论、记录决策 |
| 第一阶段研究审查草案 | [GitHub PR #1](https://github.com/floomeer83felix-source/vlm/pull/1) | 仍为草稿PR，包含历史负结果审计、文献重合矩阵、预注册草案；尚未合并 |

**协作纪律**：一轮一个明确READY的父任务；父任务可以按预先写好的README包含多项低风险子任务，Codex在同一个聊天框内连续执行、统一回报，ChatGPT集中审查后再安排下一批。GPU/数据下载等风险事项不因打包而自动放行；未经新授权不连续后台运行。

## 1. 目前研究状态

**总体结论：尚无经实验和创新审查证实的期刊核心新机制（retain 0）。**

用户已于2026-10-08明确要求恢复研究。Codex 已按VLM-001任务执行 Windows 本地工作区只读盘点，并在公开GitHub [提交4b57bff](https://github.com/floomeer83felix-source/vlm/commit/4b57bffdd1422a4ef7be6260aff9d3120cc26986) 中上传[脱敏审计附件](./codex-artifacts/VLM-001/workspace-audit.md)和[反馈](./codex-results.md)；ChatGPT已审查**文档交付、证据边界和GitHub提交范围**，决定接受VLM-001并仅放行VLM-002纯公开元数据核查。ChatGPT未直接登录本地机器验证硬件、原始账本或锁，Codex也没有新GPU问答、数据集媒体下载或新的科学实验结果。

### 主要约束

- 设备：Windows 本地 RTX 3090、64GB RAM，延用既有 conda `pytorch` 环境，不新建环境、不更改 Python/Torch/CUDA。
- 模型：冻结 Qwen3-VL-4B-Instruct；SigLIP 用于检索；第二模型 InternVL3-2B 的外部一致性检验尚未完成。
- 不使用付费 API/云 GPU，不新增人工标注，不对历史已开始前向进行重复调用。
- 公共仓库目前是研究文档同步点；不公开模型、视频、受限数据、私有标准答案和原始凭据。

## 2. 历史结果总表（来源为原进展快照）

| 实验 | 已记录的对照结果 | 科学处置 |
|---|---|---|
| 接口与基线 | 100题阶段完成，建立接口/成本记录 | 工程基础设施，非创新 |
| 延迟联合纠错 | 300题 × 7组合，仅4题满足严格联合纠错（约1.33%） | 独立纠错空间不足，不扩样/训练该控制器 |
| 撤回/替换 | 30题；候选14/30、初始22/30、投票23/30；纠错1误伤9 | 关闭 |
| 关系观察 | 24题，候选16/24与主要对照持平 | 关闭当前候选 |
| 局部密采 | 24题，3臂均16/24；纠错2误伤2 | 净0，关闭 |
| 弱实例绑定见证 | 24题，候选15/24，对照16/24 | 不扩样 |
| 原生Sparse12 vs多图 | 30题，原生19/30、多图22/30 | 当前原生接口不替换强基线 |
| GAP7/MATCH7/NATIVE6/IMAGE12 | 20题分别9/9/8/11；GAP7对IMAGE12纠错1误伤3 | 拆分方案未过门，不扩样 |

这些阶段使用部分重复的题目/来源，**不能累加为独立样本量**。操作性来源组件/内容SHA也不等价于实际场景独立性。最近20题多图IMAGE12最佳，但样本非常小；不声称统计优势或全领域普遍性。

### 从负结果中能说与不能说的

- 可说：当前候选在已测试样本上未取得稳定净收益；干预可能同时纠错和误伤；按成本与验证协议不值得继续试同类变体。
- 不可说：模型一定忽略了视觉、必需证据一定未被看到、所有主动视觉方法无效、或另一骨干上必然相同。
- 尚缺：同版本原视频时间桥接、独立长视频外部验证、第二模型泛化、训练方法多种子验证及可信创新性审查。

## 3. 最新科学问题（原DECISION-007已选择B：重新寻找核心计算机制）

**2026-10-09 用户最新选择B**：继续长视频VLM研究与高水平论文目标，但放弃以query-aware/uniform采帧比较、selector-only×prompt-only措辞敏感性为本次**核心算法贡献**。上述内容仍是历史测量草案，不再是当前READY执行命题。项目目前**retain 0**，没有新颖算法已成立或GPU实验已批准。

[机制复位总方案](./mechanism-reset-2026-10-09.md)提出**三个互斥的形式候选**，且每个都有强已知先例风险：

- **M1 开放世界负事实证据义务**：在稀疏且不完全的视频观察下，判定「从未发生/仅有/此前没有」何时必须UNKNOWN；研究需要什么覆盖/探测器假设才能输出条件证书，而非把“没看见”当“没有”。该方向可能属于经典三值时序逻辑/有限轨迹监控的已知情形。
- **M2 有来源和版本的可撤销断言**：矛盾新证据到来时，仅失效受依赖的子结论；强基线是经典truth-maintenance及结构化事件图。若只是普通依赖图缓存/重问，应NO-GO。
- **M3 答案假设可区分性义务**：对仍与当前观察相容的候选答案定义可区分谓词与不可识别状态；VideoHV/PACE/NeuS-QA已有假设检验及线索检索，若无实质不同算子，NO-GO。

**直接先例约束**：[NeuS-QA (AAAI2026)](https://ojs.aaai.org/index.php/AAAI/article/view/37834)已做时序逻辑+视频自动机及模型检查；[VideoHV-Agent (CVPR2026)](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Think_Then_Verify_A_Hypothesis-Verification_Multi-Agent_Framework_for_Long_Video_CVPR_2026_paper.html)已做答案假设和判别线索验证；[VideoSEAL (ICML2026)](https://proceedings.mlr.press/v306/qiu26v.html)已将规划与回答权限分离并做像素验证；[Open-o3-Video](https://proceedings.mlr.press/v306/meng26e.html)、[ENTER](https://arxiv.org/abs/2501.14194)、[VideoStir](https://aclanthology.org/2026.acl-long.1656/)均已覆盖不同结构化证据操作。**以上是公开方法/摘要级初筛，不构成任何候选原创性认证**。新包必须尽可能由证据**否决**它们，允许全淘汰。

**最新数据入口变化（用户明确同意）**：由于Ego4D许可表单出现`Failed to fetch`，先使用 [Charades/Charades-STA公开项目说明与license](./charades-entry-2026-10-09.md)做**可验证短时域标注科学问题的前置核验**；以[十项BATCH-008协议](./codex-artifacts/VLM-BATCH-008/README.md)为准，只查公开许可、STA衍生文本标注权利、字段与时间join、多实例动作与重叠混淆现象、来源/PTS、长视频外推与先例否决。原始Charades约30秒的视频不能直接当长视频论文最终确认集；目前尚未批准下载任何视频或3MB标注。新方向retain0、GPU/真实数据门HOLD，BATCH-007不复活。

**最新验收决定**：[BATCH-007十项交付](./codex-artifacts/VLM-BATCH-007/downselect-and-stop-decision.md)已按[d82e30e](https://github.com/floomeer83felix-source/vlm/commit/d82e30e43ec31fb8600b0a61d62021017a6d59aa)完成并通过文档/静态代码验收，但**三个当前形式候选均被同输入的经典强基线模拟而不保留（retain0）**：M1=三值/开放世界监控，M2=依赖缓存，M3=version-space判别线索；这是具体算子的NO-GO，不是全领域不可能创新。真实证据标签、视频许可、PTS/来源、视觉感知可信性和费用门均未通过，GPU/HOLD。当前**没有READY**，进入VLM-RESEARCH-GATE-008等用户提供实质新问题或证据资源，不自动安排BATCH-008。

## 4. 当前执行看板（2026-10-09）

| 项目 | 状态 | 负责方 |
|---|---|---|
| 原进展快照核对 | 完成（公开文档级） | ChatGPT |
| 三份第一阶段研究审查草案 | 已在PR #1提交，待审核合并 | ChatGPT |
| 任务/反馈/附件协作机制 | 已建立在main；首个附件路径已建立 | ChatGPT |
| 本地Windows环境/锁/账本验证 VLM-001 | **ACCEPTED（文档审计交付）；锁等运行前置仍未知** | Codex，ChatGPT验收 |
| 数据字段核对 VLM-002 | **ACCEPTED（报告完成、G1仍HOLD）** | Codex，ChatGPT审查 |
| 三项连续安全任务包 VLM-BATCH-003 | **ACCEPTED（仅静态交付，G1保持HOLD）** | Codex，ChatGPT审查 |
| 合法数据请求与toy合同验证 VLM-BATCH-004 | **ACCEPTED（toy测试报告通过，G1 HOLD）** | Codex，ChatGPT审查 |
| 官方访问渠道、toy反例与研究路线裁决 VLM-BATCH-005 | **ACCEPTED（toy18/18执行者报告，G1 HOLD）** | Codex，ChatGPT审查 |
| 路线决策 VLM-ROUTE-006 | **ROUTE2_SELECTED（取代旧路线1）** | 用户与ChatGPT |
| 路线2创新红队与无gold数据门 VLM-BATCH-006 | **ACCEPTED（十项交付；科学NO_GO_OR_PIVOT）** | Codex，ChatGPT审查 |
| 核心科研路线选择 VLM-DECISION-007 | **B_SELECTED（转向不同的核心机制）** | 用户与ChatGPT |
| 三候选形式机制否决研究 VLM-BATCH-007 | **ACCEPTED（十项交付；RETAIN 0 / STOP THIS PORTFOLIO）** | Codex，ChatGPT审查 |
| 数据入口切换 VLM-RESEARCH-GATE-008 | **CHARADES_SELECTED / EGO4D_DEFERRED（非READY）** | 用户与ChatGPT |
| Charades准入与可证伪现象 BATCH-008 | **READY（十项公开文献/字段/许可核查，0下载／0GPU）** | Codex |
| 原时间戳审计 VLM-PTS-001 | INCLUDED IN VLM-BATCH-003；不可单独执行 | Codex |
| 预注册冻结 VLM-003 | BLOCKED | Codex/ChatGPT |
| 新模型问答 VLM-004 | BLOCKED | Codex |
| 正式创新与外部验证 | 未开始 | ChatGPT 规划 / Codex 执行 |

## 5. 滚动研究决策日志（只追加带日期条目）

### 2026-10-08 · 原项目负结果记录（历史）

据原进展快照，原主动补看及多项后续候选未通过投入门槛，retain 0；研究暂停，等待明确恢复。

### 2026-10-08 · 用户授权恢复

用户明确要求恢复研究；开始文档审计、文献矩阵和预注册草案；GitHub草稿PR #1中包含三份材料。由于缺本地工作区访问，不启动新的GPU调用。

### 2026-10-08 · 更改长期协作方式

根据用户要求：**由Codex用本地权限执行具体小任务，把事实结果上传 GitHub；ChatGPT负责研究审查、任务规划和滚动总览**。在main建立 `next-steps.md`、`codex-results.md`、`research-overview.md`。首个可执行任务仅限 VLM-001 Windows 只读状态审计，不自动开展下一项。此文件之后随每次审查持续更新。

### 2026-10-08 · 建立单独的 Codex 附件接收目录

在公开仓库 `main` 创建 `docs/codex-artifacts/` 与 `docs/codex-artifacts/VLM-001/`，规范为每个任务仅提交必要的**脱敏、小型文本证据**，例如 Windows 工作区结构、锁/进程/调用账本聚合审计，不上传模型、原始日志、视频或敏感路径。同步更新 `next-steps.md` 和 `codex-results.md`，要求 VLM-001 交付 `workspace-audit.md` 加一条结果记录。新增的目录和协议是协作基础设施，并非已得到本地状态审计结果；VLM-001 仍为 READY，后续任务仍 BLOCKED。

### 2026-10-08 20:29后 · VLM-001 文档验收及 VLM-002 有界放行（当前）

**审核材料**：Codex的 [VLM-001工作区审计](./codex-artifacts/VLM-001/workspace-audit.md)、[Codex回报](./codex-results.md)与 [提交4b57bff](https://github.com/floomeer83felix-source/vlm/commit/4b57bffdd1422a4ef7be6260aff9d3120cc26986)；该提交只包含新增审计附件和追加回报两个文件，没有修改原历史快照或ChatGPT任务/总览。**审查性质为GitHub文件审查及内部一致性核验，不等同于ChatGPT直接访问Windows本地现场**。

审计方报告：
- Windows 11、RTX3090 24GiB、既有conda pytorch（Python3.9.21、PyTorch2.5.1、CUDA构建12.4），环境存在但未加载模型或测试GPU前向。
- 原工作区的Qwen3-VL-4B、InternVL3-2B、SigLIP文件与研究入口存在；最新manifest的11个代码哈希均匹配；未对所有模型/视频做全量哈希。
- 四份所检查QA账本分别有80、60、72、120个唯一started与terminal，所查的合计332次无started未终态；这是已选4账本的状态核查，**不是历史全部run的覆盖性证明，也不是本轮新QA**。
- 6个Python进程未明确映射到项目入口；GPU仍有其他应用/权限不全的条目，整机空闲不能确认。4个OS锁文件存在，但持有者状态UNKNOWN。
- 历史研究状态仍为PAUSED；参考数据访问最后报告HOLD。旧数据还存在约450份指纹覆盖缺项，基于FPS/索引的时间映射还不能证明真实PTS，独立来源及媒体版本桥接没有通过。
- Codex报告新增模型前向/视频解码/数据集下载=0，研究资产修改=0；本次没有提供新的问答准确率或核心机制。

**验收决策：ACCEPT VLM-001（仅任务交付）**。已经达到“安全脱敏汇总 + 来源可追溯 + 未知项与风险如实披露 + 不重复前向”的文档协议。四份账本核验、存在性与版本检查为**执行者报告**，需要原始复算时仍应在本地进行。

**放行：VLM-002 READY**，只准调查公开TRACE/VES-Bench、HERBench（必要时CaST-Bench）的官网、许可、数据版本、证据标注schema及同版本视频时间映射**元数据**；无模型/视频/大文件下载、无GPU前向、无工作区修改。新建交付位置 [VLM-002附件目录](./codex-artifacts/VLM-002/) 并在 [Codex结果文件](./codex-results.md) 追加报告，完成即停止。

**仍然 HOLD**：VLM-003（manifest/新输入合同冻结）、VLM-004（新GPU实验）、自动续作；在新模型问答前仍需实证核实OS锁持有与GPU占用、目标源真实PTS/证据桥接、独立性及成本/权限。数据公开并不自动通过G1数据门，更不是算法创新证据。

### 2026-10-08 · VLM-002 审查与工作流调整（当前）

**审查来源与归档SHA**：Codex 提交 [2c9e568](https://github.com/floomeer83felix-source/vlm/commit/2c9e568c95ce021b38c9ac3155bfb3ecc28f0b7f)，仅新增 [VLM-002元数据报告](./codex-artifacts/VLM-002/dataset-metadata-review.md) 及在 [Codex回报](./codex-results.md) 追加一条结果。ChatGPT检查了提交范围、全文报告的证据级别、数据集版本追溯和结论边界。审查性质为**执行者公开元数据审计的文件级复核**；未亲自下载数据或独立核验目标数据schema样本/媒体许可。

**ACCEPT VLM-002 的文档交付；G1数据门仍HOLD**。
- TRACE/VES-Bench：论文声明每题联合必要证据区间，公开媒体清单与revision可追溯，但本次没有确认实际问答/区间字段、标注与视频许可证或源PTS/剪辑版本桥接；不能据此开始先导。
- HERBench：公开列与非商业数据许可可追溯，嵌套支持字典缺失；MRFS是模型+选帧器下的首次答对帧数，**不是参考必要证据区间**；媒体上游条款待核。
- CaST-Bench：公开文档给mm:ss区间及对象框结构，仍没有证明实际多段联合必要性、长视频适用性、clip原点与真实PTS。
- 三者均没有通过 >=40操作性独立视频来源、三段不重叠必要区间、<12锚帧、固定12帧区间外候选池及合法媒体使用的完整G1门槛。报告的公开查询预算214936字节、无新GPU调用和无媒体下载是执行者报告，并非本助手重新执行联网计量。
- **科学判断**：不将“找到了公开数据集”当成实验成立；VLM-003的manifest冻结、VLM-004的GPU前向仍BLOCKED。避免重复失败的404/AGQA访问链。

**下一小任务**：只放行 [VLM-PTS-001](./codex-artifacts/VLM-PTS-001/README.md) 静态检查本地时间戳/FPS/PTS/VFR及裁剪桥接代码合同，目的在于限定未来实验的测量风险；0新模型调用、0视频解码、0下载，不更改现有环境或研究资产。完成后Codex上传 `timestamp-contract-audit.md` 和回报即停止。这一任务**不能改变G1 HOLD**。

**不再采用GitHub Issue推送通知**：早期测试的 `.github/workflows/vlm-push-notifier.yml` 已从 main 移除；自动生成的Issue #2已关闭。改为ChatGPT内的**每小时条件检查任务**：只针对未审查的Codex结果尝试审查及写入计划；不是实时GitHub webhook，也不保证任何自动写入成功。以任务书和研究总览的提交及被审查Codex SHA为唯一事实进度标志，不因ChatGPT自身推送重复分析或开放GPU。用户也可随时在此对话请求立即审查。

**Codex轻量领取方式（按用户实际工作方式调整）**：用户始终使用同一个Codex聊天框，不创建新会话。每次用户在原聊天发送“继续下一轮”指令，Codex安全刷新独立GitHub文档checkout `main`，重新读取 `AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`，仅执行尚未交付的唯一READY任务并上传脱敏结果，然后停止本轮操作并保留聊天。既有聊天不会自动感知GitHub更改，ChatGPT每小时自动审查也无法向该Codex聊天发送消息或唤醒它；不运行Codex常驻监控，以节省额度。实验工作区不是Git文档checkout，禁止在实验目录盲目同步远端。

### 2026-10-08 · 长期使用同一个 Codex 聊天框

用户明确要求所有本地执行继续保留同一Codex对话，不新开会话。本次相应更新main的AGENTS.md与docs/next-steps.md：每轮用户发短指令→Codex安全刷新文档repo main→重新读取最新任务书与结果文件→完成唯一READY任务并提交→停止本轮操作但不关闭对话。自动GitHub审查与Codex开始新一轮是两个独立动作，**没有ChatGPT到现有Codex聊天的自动唤醒通道**。当前科学研究任务状态未因此升级：VLM-PTS-001仍READY、VLM-003/004仍BLOCKED，GPU/视频下载仍HOLD。

### 2026-10-08 · Windows 每30分钟零Codex模型检查的试行方案

用户认可优先使用廉价Git检查来节省Codex额度。当时曾向main添加 `tools/watch-ready-task.ps1` 与 `docs/automation/windows-ready-watch.md`（**现已取消并删除，不再适用**），并更新根目录AGENTS.md与下一步任务交接说明。脚本计划通过**本地Windows任务计划程序**每30分钟读取远端 `main`，识别尚未回报的唯一READY任务，使用本机 `%LOCALAPPDATA%` 状态文件防重复提醒；**脚本自身不调用模型、不写GitHub、不启动Codex或GPU**。

当前仅完成公开仓库侧文件交付，**尚未在用户Windows机器上安装或实际验证计划任务**；需要用户让现有Codex聊天按文档本地配置并测试。原有桌面Codex聊天目前没有经验证的“由纯Git脚本无模型成本直接注入消息”的入口，因此本方案只自动识别并本地留下提示，仍需用户在同一个聊天框发送“继续下一轮”。若需要完全无人值守，必须另行授权Codex原生thread automation，并接受每次唤醒可能消耗额度的现实。研究任务READY/BLOCKED和GPU禁止条件**未变更**。

### 2026-10-08 · 取消 Windows 每30分钟本地 Git 监控方案

用户明确取消上一轮提出的 Windows Task Scheduler + PowerShell / Git 定期检查方案。在公开仓库main删除低成本轮询脚本 `tools/watch-ready-task.ps1` 和安装说明 `docs/automation/windows-ready-watch.md`，从 AGENTS.md 与任务书撤下引用。上一段“试行方案”仅保留为**历史记录，当前已撤销，不得执行**。

该方案此前只是在GitHub写好了文件，**没有证据表明已在用户 Windows 实验机中安装计划任务**。若用户或Codex已经在本地创建了名为 `VLM Ready Watch` 的 Windows 计划任务，应在本地任务计划程序中停用并删除；远端删除仓库文件不会停止已安装的本地任务。

保留“用户在同一个 Codex 聊天框发指令→Codex安全刷新main并执行唯一READY任务”的既有交接规则。原有ChatGPT每小时Codex结果审查自动化不属于被取消的半小时Windows脚本，暂时保持开启。研究任务门槛、当前READY/BLOCKED状态及GPU限制均未改变。

### 2026-10-08 · 增加Codex单轮工作量：VLM-BATCH-003（当前决定）

用户反馈VLM-002已在main提交 `2c9e568`，希望一次安排较多任务，减少反复等待ChatGPT审批。核查main仍只有VLM-PTS-001原READY，且VLM-002回报已经审核，本次**不是重跑VLM-002，也不是放行数据/GPU门**。

决策：建立 [`VLM-BATCH-003`任务包](./codex-artifacts/VLM-BATCH-003/README.md)，取代原VLM-PTS-001独立READY状态。一次交付三项：
- **A 时间戳接口静态审计**：取帧代码的帧索引/FPS和PTS、VFR、源/剪辑时间桥接；
- **B 来源/指纹隔离静态审计**：30准备/20选取源、历史450份指纹缺项的事实边界，保守来源组和污染屏蔽合同；
- **C G1可行性技术合同**：沿用VLM-002已核实元数据与A/B，列明12帧对照、无答案参考区间和许可/时间/来源前提，提出后续最小行动清单。

Codex同一个聊天框一次领取唯一READY父任务，连续执行这三个低风险子任务，**只上传3份脱敏Markdown＋向Codex结果文件追加1条VLM-BATCH-003汇总**。不需要中途三次科学审查；其中一项有UNKNOWN时仍可完成独立安全项，但不能擅自补跑模型或下载数据。ChatGPT集中验收后再安排下一批。当前所有子任务均尚未执行，**无新的问答准确率、无机制保留**。

**保持HOLD**：VLM-003/004、新GPU/QA/训练、完整数据集与媒体下载、环境/锁/账本修改、来源独立性与真实PTS/G1数据门。原先Windows每30分钟Git自动检查方案仍已取消。ChatGPT每小时审查自动任务（如实际运行成功）应只处理**父任务ID VLM-BATCH-003**的新增回报，避免单独审查包内A/B/C导致提前派新任务。

### 2026-10-08 22:25后 · VLM-BATCH-003 四文件交付验收、放行 VLM-BATCH-004（当前决策）

**审查来源**：Codex主分支提交 [31e8151](https://github.com/floomeer83felix-source/vlm/commit/31e8151901c1c75739670acefec211f920313244)，严格只包含[A时间戳合同](./codex-artifacts/VLM-BATCH-003/timestamp-contract-audit.md)、[B来源审计](./codex-artifacts/VLM-BATCH-003/source-provenance-audit.md)、[C数据门合同](./codex-artifacts/VLM-BATCH-003/g1-feasibility-contract.md)三份新脱敏附件和[Codex结果文件](./codex-results.md)的一条追加回报；未改ChatGPT任务/总览或原始历史快照。本轮检查了GitHub提交文件范围、报告内容与彼此一致性；**未进入Windows本地逐个验证代码或重算私有来源表**。

**验收结论：ACCEPT VLM-BATCH-003 文档/静态合同交付，不等于科学G1通过，更不授权GPU。**

- **A**：Codex报告最近多图/12帧路径使用 `frame_index/fps` 估算时间；旧的 `active_vlm/reference_pts.py` 整数PTS+有理时基原语以及历史PyAV解码路径存在，但未与最新12帧/媒体裁剪合同闭环。双帧平均时间标签不能用于证明“看过”参考区间。真实PTS/VFR/RGB版本绑定未实测。
- **B**：历史聚合口径 **789节点＝339份可复用摘要＋450份缺失摘要**；缺项不能当污染数，也不能拿30 prepared、20 selected充当独立事件数。项目来源组件只提供操作性隔离，跨parent/clip、同事件多视角及保护域覆盖不足仍UNKNOWN；`≥40`独立来源未证实。
- **C**：无答案schema、clip/PTS/来源版本、12唯一源帧与配对干预门被清楚列为设计前置；VES-Bench、HERBench、CaST-Bench的实际许可/必要区间/同版视频映射仍不满足G1。没有新manifest、实验结果、新算法或正式四臂运行。

**新增科学审查提醒**：D1/D2仅保证同帧数不保证**时间分布、分辨率/视觉token成本及构造质量**相同；如果这些混杂不能先冻结或量化，即使以后准确率改变也不能把变化单独归因于“问题相似的背景帧”。这应成为下轮合同测试的明确失败/UNKNOWN条件。

Codex报告本次新增GPU/QA/下载/视频解码/新测试调用=0、原研究资产修改=0；上述资源数字是执行者声明。**保留** VLM-003/VLM-004、G1数据门、真实媒体桥接、GPU/锁和完整来源独立性 HOLD；并且 retain 0，不夸大科学进展。

**下一唯一 READY：** [VLM-BATCH-004](./codex-artifacts/VLM-BATCH-004/README.md)（同一Codex聊天框一次连续完成三项低风险工作）：
1. A：写VES官方数据许可/无答案区间schema/同版媒体信息询问**草案**，不发送、不猜邮箱；
2. B：在独立公开文档Git checkout中构建Python标准库**纯合成**PTS/来源组件/12帧不变量toy原型与unittest，运行CPU小测试，不涉及真实媒体/原研究代码；
3. C：用真实toy测试结果和已审文献形成G1的可证伪去留判据，并记录尚缺权限、时钟和来源的阻碍。

只允许两份小型脱敏报告+两个toy代码文件+一条父任务汇总；不能发邮件/Issue、下载视频/完整数据、调用模型、改原研究工作区或连跑下一批。**toy单测通过只说明代数合同在合成样本上自洽，不能替代视频PTS、标注必要性、来源独立或GPU实际成本。**

### 2026-10-08 · VLM-BATCH-004 验收及数据阻碍止损计划（当前）

审查提交 [462ccde](https://github.com/floomeer83felix-source/vlm/commit/462ccdec4a999ef62e67a1cb52e7392fd7e14517) 及五处变更：`docs/codex-artifacts/VLM-BATCH-004/`两份报告、`prototypes/`两份纯合成toy代码及`docs/codex-results.md`追加回报；范围符合前次授权，旧研究文件未在该提交中修改。

**ACCEPT 交付，不放行 G1/GPU。** A：VES-Bench中英数据许可/无答案字段/同版时钟询问草案完成，**未联系作者，官方联系渠道未知**。B：执行者报告标准库CPU unittest第一次9/10（错误预期与双重改动样例冲突），修正toy用例后第二轮10/10，0跳过；GitHub公开源码静态审阅通过基本一致性，但本助手因运行环境无法访问公开原文件，**未独立复跑这10个测试**，不可说第三方确认通过。C：G1许可、正式必要区间、同版PTS与来源独立性仍未通过；三套候选数据均HOLD，模型/媒体调用=0（执行者声明）。

**对toy的额外审查发现**：现 `pair_contract` 虽要求传入的每个参考区间被某锚点覆盖，**却未强制参考区间至少3段且彼此不重叠**；其`time_bins`聚合也不能证明时间细粒度分布完全匹配。toy仅保证局部合成断言，与真实视频证据充分性、实际token预算和独立来源无关。

新唯一READY为 [VLM-BATCH-005](./codex-artifacts/VLM-BATCH-005/README.md)：A限量核实官方数据咨询/使用路径（不对外发送），B补强toy反例与实际CPU回归，C为“继续gold参考区间诊断”与“改为无gold观测鲁棒性问题”形成可证伪的路线决策。**本批完成后停止重复静态盘点，须ChatGPT与用户对数据申请或课题转向作下一次选择**，不得无期限优化toy或用它代替实证。当前 `VLM-003`/`VLM-004`、真实媒体、GPU、自动邮件/Issue、正式新manifest均BLOCKED，核心机制保留数仍为0。

### 2026-10-09 · VLM-BATCH-005 验收与研究路线选择门（最新决定）

**审查对象**：Codex提交 [7d1daf7](https://github.com/floomeer83felix-source/vlm/commit/7d1daf725fae5c7a921274e575101966ffed99a8)，仅两份 [A官方访问渠道](./codex-artifacts/VLM-BATCH-005/official-access-route.md)、[C研究路线备忘录](./codex-artifacts/VLM-BATCH-005/research-path-decision.md) Markdown、两份 `prototypes/` toy Python代码及 [Codex结果](./codex-results.md)中一条新增回报。文件范围与授权一致，未修改ChatGPT维护的计划/总览或早期研究快照。报告称无GPU/模型/真实媒体下载/研究工作区变更，是执行者声明，ChatGPT未直接访问Windows现场。

**决策：ACCEPT VLM-BATCH-005 文档与toy合同交付；G1、GPU与VLM-003/004继续HOLD。**

- **A 官方渠道**：执行者报告共访问6项官方公开页面、50299B，定位 [TRACE项目页](https://buaa-colalab.github.io/TRACE/)、[官方GitHub仓库](https://github.com/buaa-colalab/TRACE)及 [HF VES-Bench](https://huggingface.co/datasets/buaaplay/VES-Bench)。仓库开放Issues只能说明可以公开提问，**不是正式数据申请或作者答复保证**；注释与上游视频研究许可、真实无答案支持区间schema、同版媒体PTS/clip及独立来源仍UNKNOWN，未发送Issue/邮件/表单。
- **B 纯合成合同**：新 `validate_reference_intervals` 静态代码要求至少3个有序、有效且两两不重叠的必要区间；测试新增8项，原10项保留。Codex报告本轮Python3.9.21标准库 `unittest` **18项全过、0错误/跳过**。ChatGPT审查了公开测试与源文件，但**未在本地独立执行**；即便18/18属实，也只验证虚构时间/来源/输入合同，实际视频时钟、RGB、token预算、标注必要性与来源独立性一概不自动通过。
- **C 科研决策**：路线1保留“固定12帧、覆盖公开gold必要证据”的原假设，但必须先获得明确媒体与注释许可、可验证的联合必要证据区间、实际同版PTS/clip与足够保守独立来源。路线2另行预注册不依赖gold区间真值的观测鲁棒性问题，须把时间bin内漂移、画质、实际视觉token及检索规则偏差视为强反解释；不能把新问题直接宣传为创新方法。两路线均不可跳过版权、来源、评分隔离及用户GPU授权。

**科学止损**：连续多轮公开元数据、静态报告和toy测试仍没有获得可执行合法证据数据。继续同类盘点不会提供新的因果证据。下一步不是自动生成BATCH-006，而是 [VLM-ROUTE-006](./next-steps.md) **WAIT_USER_DECISION**：用户选择是否批准经审阅后向TRACE官方仓库咨询许可和无答案字段（未批准时不得发送），或转为不依赖gold必要区间的新预注册问题（也不是立即做GPU实验）。没有用户选择则**没有READY父任务**。科研机制retain 0，原数据G1 HOLD，真实PTS/来源隔离未证实。

### 2026-10-09 · 用户确认路线1，咨询稿供确认但禁止外发（最新）

用户选择**保留固定12互异源帧、以gold联合必要证据区间覆盖为诊断前提的路线1**，要求准备TRACE/VES-Bench官方咨询的下一步流程和最终正文、**未经用户确认不对外发送**。这个选择仅决定科研方向，不解除G1，也**不是授权发GitHub Issue、邮件、表单、下载或GPU**。

ChatGPT复核 [TRACE官方README](https://github.com/buaa-colalab/TRACE)公开声明600道问题/348个视频和联合必要参考区间，以及GitHub REST公开仓库元数据（Issues启用、仓库许可对象为空、未见既有Issues）。该入口可作为候选公开咨询渠道，但Issues启用并不保证任何具体账户具备发表权限、不是专用许可申请入口；数据注释与上游媒体使用许可、正式无答案字段、同版媒体的PTS/clip桥接目前仍UNKNOWN。不索取带答案样本和实际媒体，不将公开可见性误认为使用授权。

ChatGPT已经创建待用户审阅的[英文最终咨询正文、中文对照和发送流程](./outreach/trace-ves-bench-inquiry-draft.md)。文件标记**DRAFT / UNSENT**，公开存档在用户的文档协调仓库，仅供本人审核。**对TRACE团队尚未发送任何Issue、邮件或外部联系**。须用户再次明确批准具体渠道和正文之后，才可考虑实际对外投递；若渠道限制新建Issue，停止并让用户选择正式替代渠道，不能绕过权限。

**当前状态**：VLM-ROUTE-006 = ROUTE1_SELECTED / AWAIT_USER_SEND_APPROVAL；**不存在READY Codex父任务**。真实许可/必要区间/版本PTS/保守独立来源、G1、VLM-003/004和模型GPU实验均HOLD；按前次止损决策禁止继续机械重复旧元数据检索和toy审计。

### 2026-10-09 · 用户最新改选路线2（取代路线1；VLM-BATCH-006 READY）

**决定变更**：用户明确要求不再以gold必要区间覆盖为前提，制定新的可证伪假设、创新审查并安排无GPU任务。因此先前同日的路线1选择及[TRACE未发送咨询稿](./outreach/trace-ves-bench-inquiry-draft.md)已**不再是当前行动项**，但作为真实历史保留；**没有授权发送Issue/邮件**，不可暗中继续路线1。更新主分支任务板：VLM-ROUTE-006=ROUTE2_SELECTED；VLM-BATCH-006=唯一READY。

**科学初审**：[Q-Frame ICCV2025](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_Q-Frame_Query-aware_Frame_Selection_and_Multi-Resolution_Adaptation_for_Video-LLMs_ICCV_2025_paper.html)、[NAACL2024 MIF/MDF](https://aclanthology.org/2024.findings-naacl.162/)、[DIG CVPR2026](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Divide_then_Ground_Adapting_Frame_Selection_to_Query_Types_for_CVPR_2026_paper.html)、[CVPR2026 RL selector](https://openaccess.thecvf.com/content/CVPR2026/html/Qin_Efficient_Frame_Selection_for_Long_Video_Understanding_via_Reinforcement_Learning_CVPR_2026_paper.html)、[VideoStir ACL2026](https://aclanthology.org/2026.acl-long.1656/)等已涵盖query-aware选帧或intent retrieval；[2024 VideoQA empirical study](https://arxiv.org/abs/2408.04223)报告时间理解和输入问题扰动缺陷。上述仅官方公开摘要/项目页**定向初审**，不能声称selector-only与prompt-only正交比较不存在先例；必须全文/代码对比。**retain 0**，不批准新算法、论文创新或GPU。

**新预注册**：[docs/route2-no-gold-preregistration.md](./route2-no-gold-preregistration.md)，明确主要S_q-S_t配对正确率差H0=0；辅以同一候选池、source group、时间分层、多样性/负对照、真实token预算和评分隔离。次级措辞扰动仅在有独立确认合法等义问题对时执行；无证据HOLD。

**历史执行边界**：[VLM-BATCH-006任务README](./codex-artifacts/VLM-BATCH-006/README.md)已批准的是十项低风险文献/静态/合成统计工作（四份报告、两份新toy代码及一条回报），并未授权GPU或媒体；现已交付并审查，**不得重跑BATCH-006**。NG1合法数据、NG2真实媒体PTS/来源/预算与NG3样本功效仍HOLD；普通选帧算法在NG0未通过。

### 2026-10-09 · 用户调整Codex单批工作量：BATCH-006十任务版（最新授权边界）

用户明确要求每轮安排约10项相关工作，以减少Codex提交与ChatGPT审查的往返。核对GitHub main：**尚无VLM-BATCH-006执行结果**，所以直接更新现有唯一READY父任务的[README](./codex-artifacts/VLM-BATCH-006/README.md)，不新增10个分散的READY任务、不开新Codex对话。

**十项内容**：1正式文献方法/消融审查，2直接创新重合否决，3混杂/可识别性，4只读selector→IMAGE12/Qwen接口，5合法QA/视频与评分隔离，6真实PTS/media revision/来源保护，7时间/视觉token/成本公平性，8配对估计量/全分母/功效输入，9新建纯合成CPU统计合同与至少6项标准库unittest，10综合NG0—NG3科学NO-GO/条件研究决策。

**提交范围变更**：原定3份脱敏Markdown＋1条汇总，更新为4份脱敏Markdown（`novelty-and-identifiability.md`、`static-readiness-gates.md`、`prereg-and-toy-tests.md`、`scientific-decision.md`）、2份**新**toy Python（`toy_route2_pairing.py`及其unittest）、1条父任务结果共**7处文件**。10项须逐项标DONE/UNKNOWN/BLOCKED，合并后只审查一次。不能重写旧toy、旧账本或历史实验文件。

**保守预算未变**：0 GPU/模型QA/训练/评分调用、0真实视频解码/媒体下载、0原研究环境/锁/账本更改、0外部联系，至多12个公开官方论文HTML页面和一次小型toy回归；不访问完整受限身份映射或答案。CPU toy统计通过不代表真实数据可执行、创新性成立或新GPU放行。遇未知标UNKNOWN，遇权限/Git冲突停止，不能用多任务规模作为扩大权限的理由。

### 2026-10-09 · VLM-BATCH-006十项集中验收：NO_GO_OR_PIVOT，等待VLM-DECISION-007（最新）

**审查提交**：[e581039](https://github.com/floomeer83felix-source/vlm/commit/e581039970106dbec741adf502e48e5f948adad4)。差异严格为 [四份研究报告](./codex-artifacts/VLM-BATCH-006/README.md)（创新与可识别性、静态门、预注册与toy、科学裁决），新建两个 `prototypes/toy_route2_pairing*.py` 纯合成Python文件及向 `docs/codex-results.md` 追加一条父任务记录；既有AGENTS/规划文件、历史产物及原研究资产均不在提交差异中。十项按证据完整记录，部分UNKNOWN正是正确处理而非执行失败。

**正式结论**：**ACCEPT VLM-BATCH-006 有界文档与toy交付；NO-GO 将一般问题相关选帧S_q对时间分层S_t的比较包装成新算法或《计算机学报》核心机制。** 方法对照显示Q-Frame、NAACL2024 MIF/MDF、DIG2026等已有直接先例；文献有限且RL正式方法未取得，因此仅能否决宽泛创新主张，不可推断精确窄因子实验全球无人研究。 **retain 0**，不允许自命名新机制。

**值得谨慎保留的“未知”**：合法事前等义q/q′下让措辞仅改变selector，而将回答prompt固定，以及固定帧仅改prompt形成的正交2×2干预；该设计目前既无已证新颖性，也无已确认合法等义题对、可分离代码入口或实际处理器成本。在缺这些条件时不能运行，更不能以S_shuf替代等义对。作为测量/负结果研究可以有价值，但不是已通过期刊新方法。

**现实执行门**：现有旧选帧链仍混有SigLIP相关性与MMR/diversity，`question`同字段传selector和回答prompt，帧时钟仍以index/FPS为主，真实PTS、clip原点、媒体SHA/版本与保守来源组未新增实证。新数据媒体与QA许可、终态评分隔离新队列、实际视觉token和GPU成本、独立来源及功效参数仍UNKNOWN或现入口FAIL。旧20操作性组、789历史节点/450缺项不是新独立确认数据。旧gold必要区间G1不是路线2条件，**但NG1—NG3不能绕过**。

**统计与测试**：Codex报告标准库CPU纯合成配对估计器11项unittest全PASS、0失败/跳过；代码可静态审查，区分来源组等权Δ与题目池Δ、失败0与缺臂拒绝。ChatGPT尝试在隔离执行环境取得公开GitHub源码以独立重跑，但网络DNS失败，未执行测试；因此11/11**仅执行者报告**，不作为真实测量或NG通关。

**止损决定**：当前**不自动发布下一批10任务**。根据[任务看板](./next-steps.md)设置 **VLM-DECISION-007=WAIT_USER_DIRECTION**。供用户选择：
1. A 将窄2×2/问题措辞链路分离作为**条件性测量/复现**，接受它目前不是新方法，只有具备合法QA与等义pair时再安排实质新的验证；
2. B 若坚持高水平期刊新机制目标，转向**真正不同的研究对象与可识别贡献**，经用户明确批准后再设计一批8—10项不重复工作的安全任务；
3. C 暂停本方向，封存负结果。

**负责人倾向B（如果核心目标仍是新算法方法）**，而不是沿着S_q/S_t再造采样启发式。VLM-003/004、GPU、真实视频解码/下载、外部咨询、原研究环境更改全部继续BLOCKED；TRACE咨询稿仍UNSENT。用户选择之前没有READY任务，保留原Codex聊天。

### 2026-10-09 · 用户选择B并立项 VLM-BATCH-007 十项机制研究（最新）

**用户决定**：保留长视频VLM高水平期刊目标，但不以S_q/S_t、MMR、局部密采、GAP7、旧Evidence Memory、普通event graph及stop/zoom/router作新算法换名。ChatGPT已将 VLM-DECISION-007 标记 **B_SELECTED**，并在主分支[任务看板](./next-steps.md)设 **VLM-BATCH-007为唯一READY**。原 BATCH-006 的7处交付已验收，普通采帧新颖性NO-GO、retain0；不重复。

**新科学分叉（都只是候选）**：M1 open-world negative claim的观察完整性/UNKNOWN债务，M2来源/版本证据依赖下的局部撤销，M3候选答案不可区分集的证据义务。明确近邻：NeuS-QA逻辑/automata、VideoHV假设验证、VideoSEAL独立answer authority、VideoStir/ENTER事件图、传统Truth-Maintenance。无法证明具体独特的计算算子/可辨识目标时**必须NO-GO**，不可将“有时序逻辑/多证据图/能拒答”包装为创新。已写[机制重立题与文献URL](./mechanism-reset-2026-10-09.md)，不是科学通过证书。

**新任务包协议**：[VLM-BATCH-007/README.md](./codex-artifacts/VLM-BATCH-007/README.md)。用户要求一轮约10项；本轮分十任务：1历史否决，2最近先例，3M1定义，4M2定义，5M3定义，6双世界/不可能性反例，7虚构小世界标准库CPU穷举unittest，8合法媒体/标签/真实PTS/来源/视觉探测器前置，9强baseline/成本/预注册，10六门否决并最多留下1个**条件待核候选**或RETAIN0。只允许新建5份脱敏报告与2份toy代码，Codex追加**一条**父结果；统一提交后停止，留在**同一个Codex聊天框**。

**新旧安全门**：本包0模型/GPU/问答/训练/评分调用，0视频解码/媒体或整套标注下载、0原Windows工作区/环境/锁/账本修改、0外部联系、0新增人工标注。现实资料的许可、真实PTS、来源独立、标签真值与GPU预算仍UNKNOWN/HOLD；保守拒答与toy穷举不证明真实VLM的可靠性或新颖性。BATCH-007提交后ChatGPT独立审查，否则不得自动派BATCH-008。

### 2026-10-09 · BATCH-007十项正式验收与三机制组合停止（最新）

**审查对象**：[Codex提交d82e30e](https://github.com/floomeer83felix-source/vlm/commit/d82e30e43ec31fb8600b0a61d62021017a6d59aa)。差异正好为5份 `docs/codex-artifacts/VLM-BATCH-007/` 脱敏报告、`prototypes/toy_mechanism_counterexamples.py`及其单测、以及 `docs/codex-results.md` 的1条追加，**共8处**。ChatGPT读取五报告和两份toy源码，并核对任务1—10的证据层级、可反证条件和强基线，认为**ACCEPT交付**，但**不保留任何新计算机制**。未独立执行Windows原实验或toy；执行者报告Python3.9.21单次12 unittest全PASS、0失败/异常/跳过，只可当执行者测试收据。

**正式结论：RETAIN 0 / STOP THIS PORTFOLIO。**
- **M1（负事实证据债务）**：相容世界的TRUE/FALSE/UNKNOWN在当前公理下与经典三值开放世界监控等价；未知时域不可给真实never真值。toy117观察模板/336world-view配对在完美oracle假设下0误认证；错误把unknown补False产生89个**合成**假认证配对，不能说实测视频事件/新性能。
- **M2（来源依赖局部撤销）**：最小AND依赖闭包可由普通缓存达到相同更新轨迹，toy仅16个invalid masks/AND DAG，不覆盖完整OR、循环、视觉冲突；无新可验证的算子。
- **M3（答案可区分义务）**：同可行世界与合法观察response的version-space/判别clue planner可模拟现合同；真实world/support/answer映射缺独立验证，无新颖性或完整性证明。
- **文献证据限界**：NeuS-QA访问SSL失败，MIT的TMS链接实际上是错题；VideoHV/VideoSEAL等部分仅官方摘要。文献不足不等于新颖；当前一票否决是**同输入经典算子可模拟**，不是声称所有已发表系统都包含同一精确算法。
- **现实门**：负事件完整性标签、真实支持/依赖/可区分观察标签均不在已确认合法资源中；媒体/QA许可、同版PTS与clip变换、来源独立、可信视觉验证器、实际token/GPU成本仍UNKNOWN/HOLD。不能拿旧QA分数或toy真值填这些空白。

**研究止损与下一门**：[docs/next-steps.md](./next-steps.md)将BATCH-007改为ACCEPTED，新增 `VLM-RESEARCH-GATE-008=WAIT_USER_DIRECTION`，**当前0项READY**。用户如继续追求长视频VLM高水平期刊创新，需先明确**不同且可检验的核心对象、与现有算子不能简单模拟的差异，以及获得可合法验证证据的现实路径**。否则不安排另一批凭空构想的10任务包，也不默许下载、联系作者、GPU或修改原实验环境。用户继续保留原Codex聊天。

### 2026-10-09 · 用户同意推进Ego4D许可审阅（申请意向，非数据授权；最新）

**决议状态**：在前期M1/M2/M3机制组合被NO-GO之后，用户表示愿意通过Ego4D官方渠道本人审阅并在认可条款时接受协议。ChatGPT不替用户签署、申请或领取AWS密钥；**当前仅USER_WILLING_TO_REVIEW，不能断言已提交/被批准/允许下载或发表研究结果**。在[任务板](./next-steps.md)将VLM-RESEARCH-GATE-008改为`WAIT_USER_SELF_SIGN`、无新READY；Codex不得代操作。

**官方入口与执行说明**：[Ego4D许可申请页](https://ego4ddataset.com/ego4d-license/)和[官方Start Here](https://ego4d-data.org/docs/start-here/)，详情见新[本人申请与字段准入清单](./ego4d-access-checklist-2026-10-09.md)。表单支持Individual/Organization；普通个人自己按Individual审阅协议并经HelloSign签署，机构只有具授权代表才能签。官网说明审批后一般约48小时发AWS凭据，凭据14天有效，这不是保证；2026年初[官方GitHub Issues](https://github.com/facebookresearch/Ego4d/issues)有表单失败/无邮件报告，出现问题不自动替用户联系或反复提交。申请需个人资料，**不得上传到公开GitHub或聊天**。

**科学转向是“资源→问题”**：官网[Episodic Memory](https://ego4d-data.org/docs/benchmarks/episodic-memory/)已明确MQ活动多实例时间窗与NLQ回答窗口，[MQ字段](https://ego4d-data.org/docs/data/annotations-schemas/)含视频/clip ID、relative time、activity segments；可将**反复活动的实例定位/时间混淆**作为候选可反证问题，但它不是新算法，必须先核以前的temporal grounding/episodic retrieval强先例和标签适用范围。人工标注“所有看见的moment”仍不能无条件证明任意未标事件在全域不存在。用户获得许可前不得使用任何注释或视频；许可后仍须分开确认正式权利范围、同媒体版本PTS/clip/source独立、评分隔离、最小数据下载预算/路径、真实视频CPU或GPU用户单独授权。

**下一步用户只需回报一个不敏感状态**：未提交、已提交待审批、已获批准、条款不接受或申请异常；不可传AWS凭据、个人资料、签名协议。状态未获批准前，不建议另开十任务包，不恢复旧VLM-003/004，不改RTX3090实验工作区，保留原Codex聊天。

### 2026-10-09 · 用户改用免申请的Charades数据入口，开放BATCH-008（最新）

**用户指令**：针对Ego4D申请时报`Failed to fetch`，用户同意将下一批研究从等待Ego4D签约改为Charades/Charades-STA公开元数据与合适科学问题核验。此前的Ego4D申请意愿、未获批准、原研究负结果均保留作历史，不代表用户已经实际提交或获批。ChatGPT将[任务看板](./next-steps.md)的VLM-RESEARCH-GATE-008改为`CHARADES_SELECTED / EGO4D_DEFERRED`，并设置**VLM-BATCH-008唯一READY**。

**公开官方依据**：[AllenAI Charades](https://prior.allenai.org/projects/charades)提供9,848部室内日常活动视频、66,500条动作时间注释、约3MB标注评测文件及13GB 480p视频入口；[专属License for Non-Commercial Use](https://prior.allenai.org/projects/data/charades/license.txt)允许协议规定的非商业科研、限制公开发布改造数据/任何第三方分发，并规定短片段/静帧学术示例条件；不要求事先签Ego4D式个人许可，但**不等于任何使用都无版权义务**。[Charades-STA TALL作者仓库](https://github.com/jiyanggao/TALL)提供句子—视频时间区间train/test外链并提醒annotation曾清理；STA衍生文本使用权、可验证版本及与Charades源时间轴join**仍UNKNOWN**。原始Charades平均长度约30秒（[ECCV2016数据论文](https://publications.ri.cmu.edu/hollywood-in-homes-crowdsourcing-data-collection-for-activity-understanding)），它是短时域科学现象初筛与流水线入口，不是自然长视频独立数据集。

**新研究候选**：P1同类活动在同一视频内重复出现引起的**事件实例错配**，P2不同动作重叠造成的**时间边界/标签混淆**；必须先证明现有标注足以定义有效样本及清晰客观正确性。66,500总interval数不证明有多少合法的P1样本，不能由STA文字直接推“第一次/第二次”真值；如果只重复既有TAL/TMR研究则NO-GO，创新retain0。真正长视频长间隔推理仍须另外合法长视频、来源独立和真值。

**唯一低风险任务**：[VLM-BATCH-008 10项具体协议](./codex-artifacts/VLM-BATCH-008/README.md)：1原license条款，2 STA独立权利，3原标注schema，4两套标注同源join与revision，5同类重复实例可辨识性，6重叠动作边界指标，7强相关TAL/TMR先例，8来源分组/真实PTS/媒体版本，9短视频向长视频外推限制，10五门科研GO/NO-GO与唯一真正新增信息行动。Codex**只能**创建5份脱敏Markdown并向`docs/codex-results.md`追加一条总报告（共6处），不新增toy或改旧报告，单次提交后停止。

**安全约束不变**：目前用户没有授权下载即使3MB的注释压缩包、13GB视频、STA Drive文件、模型权重，也没有批准CPU解码/GPU/问答运行；0原Windows源资产/conda/CUDA/锁/账本更改、0人工标注、0外部联系、0隐私身份/答案上传。只有许可、字段和新颖性门有进一步必要且有效时，才向用户**单独申请最小标注包下载许可**；全部不达标则STOP。历史BATCH-007 ACCEPTED、M1/M2/M3 retain0；VLM-003/004依旧BLOCKED。继续使用原Codex聊天。

## 6. 下一次 ChatGPT 审查的检查顺序

1. 读 [Codex执行结果](./codex-results.md) 最后新增记录及对应提交；
2. 与 [任务书](./next-steps.md) 的任务ID/验收标准逐项核对；记录完成、未证实、偏差；
3. 必要时只看脱敏产物或 PR 差异；对无原始证据的主张标注“仅执行者报告”；
4. 形成明确 **ACCEPT / REVISE / HOLD** 与下一步科学依据；
5. 仅由 ChatGPT 更新任务书与本总览，不删除之前负结果或重写原始快照。

**提醒：** 此仓库中的总结不是原始实验数据仓库；报告中所有新准确率和创新结论必须有可审计的新来源及运行账本支撑。
