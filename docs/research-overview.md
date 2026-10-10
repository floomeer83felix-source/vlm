# VLM 长视频研究总览与决策日志（ChatGPT 维护）

> **定位**：滚动总结，不取代原始实验档案，也不宣称每次都已对本地实验原始账本独立复算。
>
> 更新：2026-10-10（北京时间；用户批准纯公开H1强先例红队＋Ego4D/HourVideo合法同版链静态深挖，BATCH020唯一READY；下载/GPU均禁止）  
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
| Charades准入与可证伪现象 BATCH-008 | **ACCEPTED（10项文档；真实数据与长域仍HOLD）** | Codex，ChatGPT审查 |
| Charades最小原标注许可 VLM-DATA-GATE-009 | **USER_APPROVED_METADATA_ONLY（一次下载已消耗，不许第二次GET）** | 用户本人 / ChatGPT |
| 原Charades标注资格统计 BATCH-009 | **STOPPED_SAFELY（GET0，P1/P2 UNKNOWN）** | Codex，ChatGPT审查 |
| Windows存储检查修复 BATCH-009-FIX | **ACCEPTED（仅修复/测试；未下载）** | Codex，ChatGPT审查 |
| 续接官方最小元数据包 BATCH-010 | **ACCEPTED（ZIP/CSV结构与聚合交付；区间质量HOLD）** | Codex，ChatGPT审查 |
| 现有Charades时间合同独立核验 BATCH-011 | **ACCEPTED（数值交付；同版时间语义HOLD）** | Codex，ChatGPT审查 |
| 下一科研路线 VLM-RESEARCH-DECISION-012 | **USER_SELECTED_CHARADES_ALIGNMENT（非READY的用户决策）** | 用户、ChatGPT |
| Charades官方评测对齐及时间质量分层 BATCH-012 | **ACCEPTED（工程frame label对齐；质量/事件HOLD）** | Codex，ChatGPT审查 |
| 未来科研证据范围 VLM-RESEARCH-GATE-013 | **USER_APPROVED_V1_CONDITIONAL（媒体试点限额授权）** | 用户、ChatGPT |
| Charades两视频官方Range与CPU时钟核验 BATCH-013 | **STOPPED_SAFELY（原任务已结束，0媒体传输）** | Codex，ChatGPT审查 |
| BATCH-013-FIX受限协调器/ZIP64补齐 | **ACCEPTED_CODE_ONLY（合成27 PASS报告，0真实媒体）** | Codex，ChatGPT审查 |
| 独立CPU ffprobe工具门 VLM-CPU-TOOL-GATE-014 | **USER_APPROVED_ISOLATED_FFPROBE_INSTALL（有限授权、尚未执行）** | 用户、ChatGPT |
| 发布者SHA固定的独立ffprobe部署 BATCH-014 | **STOPPED_SAFELY / CPU_TOOL_BLOCKED（部分ZIP超时；0部署）** | Codex，ChatGPT审查 |
| 工具部分包恢复或止损 VLM-CPU-TOOL-GATE-015 | **USER_SELECTED_SAME_OBJECT_RESUME（研究方向已定、非READY）** | 用户、ChatGPT |
| 同源工具ZIP仅一次断点续传 BATCH-015 | **ACCEPTED（固定发布方整包SHA和CPU ffprobe可用）** | Codex，ChatGPT审查 |
| 媒体客户端显式禁代理/固定HTTPS BATCH-016 | **ACCEPTED_CODE_ONLY（40合成PASS收据，真实媒体0）** | Codex，ChatGPT审查 |
| 条件式两例Charades媒体时钟试点 BATCH-017 | **STOPPED_SAFELY / CODE_DELIVERABLES_ACCEPTED（内置合成失败，0真实媒体）** | Codex，ChatGPT审查 |
| Charades最后一次媒体试点方向决策 VLM-RESEARCH-CHOICE-018 | **USER_APPROVED_LAST_V1_TRY（非READY方向决策已结束）** | 用户、ChatGPT |
| Charades最后一次双环境门限V1试点 BATCH-018 | **ACCEPTED_ENGINEERING / V1_CLOCK_UNKNOWN / FINAL_MEDIA_STOP（非READY）** | Codex，ChatGPT审查 |
| BATCH018之后长域科研方向选择 VLM-RESEARCH-POST018-DIRECTION | **USER_APPROVED_STATIC_LONGVIDEO_SCREEN（仅公开网页，无媒体）** | 用户、ChatGPT |
| 六长视频资源与原创机制公开静态审查 BATCH-019 | **ACCEPTED_STATIC_DELIVERABLES / NO_DATA_OR_NOVELTY_GO（非READY）** | Codex执行、ChatGPT验收 |
| H1强先例与Ego4D/HourVideo合法同版桥接 BATCH-020 | **READY（八项纯公开静态反证；三Markdown＋一追加）** | Codex执行，ChatGPT审查 |
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

### 2026-10-09 · VLM-BATCH-008十项Charades文档验收与下一最小数据门（最新）

**已验收提交**：[2544df9](https://github.com/floomeer83felix-source/vlm/commit/2544df98fa363bc62ec888682121d879f24bcec2)仅涉及[五份Charades审核报告](./codex-artifacts/VLM-BATCH-008/README.md)及 `docs/codex-results.md` 单条汇总共6处，符合授权；无新增原研究代码／toy或提交数据。ChatGPT已核验文件内容、证据层次和研究止损，**ACCEPT文档交付**，而不是批准数据获取、科学创新、视频/GPU实验。Codex自报12个官方/论文HTML页面共约795kB响应正文、0媒体/标注/模型获取、0本地原工作区改动；这是执行者资源陈述，不是ChatGPT对其远端Windows的独立监控。

**研究五门裁决**：

| 门 | 当前结果 | 学术含义 |
|---|---|---|
| LEGAL | 原Charades官方非商业研究许可类别**条件可讨论**；具体主体/用途合规待用户确认；STA权利UNKNOWN | 不得把“无需先填表”说成可商用/无限分发或已经正式授权所有场景 |
| SCHEMA | 官方README有id/subject/actions三元组/length/split文档，可核字段；**真实CSV与端点尚未验** | 官方帧级localize评测25个时间点mAP，**不是**实例det-mAP/tIoU，拟新增指标不可借官方评测脚本声称已验证 |
| IDENTIFIABILITY | P1同类独立重复实例资格UNKNOWN；P2异类重叠实例资格UNKNOWN | 总66,500区间数不等于合法实例资格；不能将记录顺序当“第一次/第二次”或未标当never |
| NOVELTY | 常规多标签TAD/TMR、多moment定位作为新算法**FAIL**；窄错误测量可能性UNKNOWN，retain 0 | TALL、Dual DETRs、FlashMMR/TIME等直接先例已高度重合，需拒绝换名式创新 |
| LONGVIDEO | Charades均长约30秒，**单独作为自然长视频验证FAIL**；合法长域外部数据UNKNOWN | 拼接短片不产生独立自然长域确认或小时级长时推理证据 |

**唯一新增事实路径**：经用户单独批准，才可从[AllenAI官方Charades页](https://prior.allenai.org/projects/charades)获得官方约3MB`Annotations & Evaluation Code`压缩包，放在公共Git checkout及旧RTX3090研究环境外的**独立隔离目录**，仅读CSV/类表/README/license并检查真实header、version hash、视频时长/时间格式、同类不重叠与异类重叠资格和invalid/ambiguous分母，输出不能重建受限样本的脱敏聚合统计。**当前没有下载授权、没有已验证的样本资格或实验许可**；STA的Drive注释、Charades视频13GB/原始帧、GPU、真实PTS认证、新问答／旧实验全HOLD。

**当前用户决策门**：[任务看板](./next-steps.md)记录`VLM-DATA-GATE-009=WAIT_USER_DOWNLOAD_APPROVAL`；**没有新READY、不给原Codex直接“继续”指令**。用户需明确非商业研究用途符合原许可，并对最低必要官方标注包下载及隔离存放授权。得到许可后，由ChatGPT另定一次受限的数据资格计数合同和停止条件；若拒绝则保留HOLD。哪怕资格数非0，也不是新机制PASS，仍需另选合法自然长视频外部确认材料及科学差异化才可谈实验预算。

### 2026-10-09 · 用户批准Charades最小标注下载并冻结Windows隔离安全协议（最新）

**明确的新授权**：用户确认其研究符合Charades非商业学术许可，并**仅**批准从官方[Charades项目页](https://prior.allenai.org/projects/charades)下载约3MB `Annotations & Evaluation Code` ZIP，用于独立隔离目录CSV、时间区间、P1/P2候选资格及来源聚合统计；明示**不授权视频（包括13GB版）、STA、GPU、原研究环境改动**。ChatGPT未替用户下载或访问其Windows电脑，尚无真实标注分析结果。

**存储位置冻结**：Windows环境变量`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`，默认分`incoming/`（单个ZIP）、`extracted/`（仅train/test CSV、类别表、合法README/license）、`local-audit/`（本地manifest及非公开中间聚合）。Codex执行前要检查目录确实不在原RTX3090工作区、公有docs Git checkout、OneDrive等同步目录且无reparse/junction、≥150MiB空闲；未知就STOP，不换到另一个路径。公有仓库不能出现用户绝对路径、真实数据行/subject/video映射、原始描述或微小可逆分组。

**安全协议和唯一任务**：[独立数据安全协议](./charades-metadata-safety-protocol-2026-10-09.md)和[BATCH-009十项任务书](./codex-artifacts/VLM-BATCH-009/README.md)。只有官方页面标为3MB的注释/评测S3链接，下载上限8MiB及一次有限重试；ZIP中央目录和路径/链接/尺寸/加密检查；白名单读取CSV和class table，不执行任何压缩包脚本、不读视频；对真实header、坏区间/重复ID、同类严格不重叠的P1组、异类重叠的P2组、train/test subject交集**只做脱敏总数**。用现有Python标准库纯CPU处理，并为聚合逻辑建立合成单测；允许交付两份脱敏研究报告、两份不含真实数据的通用stdlib代码和结果日志的一条追加，共5处文件。单次提交后停止，不自动申请下一步。

**研究门仍HOLD**：原Charades license/schema此前仅文档条件PASS，新统计未运行。即使获得非零资格总数，也不提供自然语言“第一次/第二次”序列真值、不证实真实媒体PTS或模型性能；该数据均长约30秒，仍不能直接支撑自然长视频核心机制论文。M1/M2/M3已NO-GO、创新retain0、STA权利UNKNOWN、GPU和旧VLM-003/004 BLOCKED。用户后续在**原Codex聊天**发执行信号才真正开始，本轮不后台下载。

### 2026-10-09 · BATCH-009安全阻塞/FIX修复审查，启动唯一受限续接BATCH-010（最新）

**本轮用户通知“已上传结果”后ChatGPT核对GitHub**：包含[首次结果bc16e38](https://github.com/floomeer83felix-source/vlm/commit/bc16e38eab35f454bc3e0ccc3c805c15c6009ed8)和[后续修复dda8481](https://github.com/floomeer83felix-source/vlm/commit/dda8481a330c4cfa1e734511ad59e7d8f7571d4f)两次提交。首次5处变更（2份报告、2份通用审计/test、1条父结果），执行者在Python`absolute()`与`resolve()`路径字符串不等时**在实际数据GET前STOP**。此前PowerShell检查本地隔离目录/云同步/空间PASS；官方唯一S3入口`HEAD200`，报告`Content-Length=3,519,822B`、ZIP类型；未取得正文，GET/重试0、CSV/ZIP真实数据0、P1/P2/source与真实PTS均UNKNOWN。**科学状态不是完成数据统计，而是受控安全停止**。

**修复回报边界**：后续FIX修改`prototypes/charades_metadata_audit.py`、其test及追加一条结果，共3处，解释Windows给同一目录返回不同规范拼写；新逻辑要求`os.path.samefile`及nonzero dev/inode一致、两条祖先链无reparse点、规范链稳定和新叶归属一致。执行者报告固定隔离根只读复核PASS与21项标准库合成unittest全PASS，**ChatGPT仅审查提交及静态源码，未访问/独立运行用户Windows路径测试**。FIX无数据GET、ZIP/CSV下载、真实统计，也不授权自动重做父任务009。任务板因此将009设为`STOPPED_SAFELY`，009-FIX独立记为`ACCEPTED_PRECHECK_FIX`。

**新READY**：[VLM-BATCH-010完整受限任务](./codex-artifacts/VLM-BATCH-010/README.md)在**未使用的用户原有一次官方小包许可内**继续；不增加视频、STA、GPU、原研究目录/旧锁/conda或模型使用权限。用户必须在原Codex聊天主动发继续信号，执行前**再次完整核对**官方许可/HTTPS S3、固定Windows`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`路径/原研究和公共Git隔离、≥150MiB空余、同目录物理身份与两条链无reparse点。官方ZIP体量限制8MiB流式硬拒绝，ZIP成员安全/CRC及仅CSV/类别表白名单，生成本地原始元数据的**匿名宏观聚合**，GitHub仅交两份脱敏报告和一条010父结果（3处），不修改已验收审计代码和历史。任一新安全检查失败STOP而非边运行边修代码。

**仍未成立**：没有真实同视频同类非重叠P1资格数、异类并发P2资格数、实际subject交集、合法自然长视频外部确认、真实PTS或新VLM算法贡献。前轮机制retained0，Charades短域不是长时域数据；即便010成功，也只能判记录层资格与是否进一步科学投入，不放行任何视频/GPU。任务板[docs/next-steps.md](./next-steps.md)唯一READY=010，之前009/FIX不准重跑，保留原Codex聊天。

### 2026-10-09 · VLM-BATCH-010首次真实Charades原标注统计的验收（最新）

**验收来源**：[提交8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)，严格2份脱敏报告+[结果](./codex-results.md)一条，3处既定变更，无历史代码/原实验资产改动。ChatGPT已阅读[官方包/结构报告](./codex-artifacts/VLM-BATCH-010/download-and-schema.md)、[P1/P2资格统计](./codex-artifacts/VLM-BATCH-010/qualification-and-decision.md)和GitHub提交文件列表，验收**安全范围与统计回报交付**，不是独立复跑用户Windows的原始CSV或认定科学结论有效。

**数据安全收据（执行者报告）**：用户此前批准的唯一AllenAI官方`Charades.zip`，1次GET成功/0重试/3,519,822字节，在8MiB硬限制内；本地SHA256`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，但无可核独立官方SHA256，ETag不代替该核。ZIP14成员、声明展开9,591,127B、路径/CRC/大小与名单检查PASS；只提取8份允许的CSV/类表/README/许可，不执行评测脚本。对用户原Windows固定隔离目录的身份检查，执行者报告通过，原研究/GPU/conda/锁/账本未触碰；无视频/STA/GPU/模型/人工标签/外部联系。ZIP与全部CSV仅保存在私有隔离目录，**绝不可进入公共GitHub**。数据包一次授权已被消耗，后续不得再次GET或改资源路径。

**真正的科学增量（记录层，非媒体真值）**：两个实际CSV，共9,848行train7,985/test1,863，11字段及157类，`actions`66,500条token。按预注册的`0≤start<end≤length`和类别等规则，合法数值动作train35,211/test11,664=46,875；**不通过19,625=29.5%，主因`end>length`；含任一不通过标注行7,433/9,848=75.5%**。将它称为“旧规则与原标注冲突”，不是数据文件损坏已证实。用户本地旧审计器用Decimal计算，执行者报告21项CPU合成test通过；本助手没有独立复算真实数据。

| 未验证科研候选 | 现有规则下的真实聚合总数 | 禁止的推论 |
|---|---:|---|
| P1 同视频同类至少一对分离区间 `gap>0` | 347组、涉及292个视频；`gap>0.5`313组、`gap>1`288组 | 不是347个物理独立事件或完整排序真实QA，也不能确保其余标注不影响资格 |
| P2 同视频异类时间区间交集`>0` | 97,723 pair、涉及8,019视频；强重叠73,513 pair | pair非独立N、不是模型错误或真实关系真值；受上游区间冲突影响 |
| 来源分组 | 267个字面subject；train214/test53，跨split subject ID交集0 | 不认证不同人/场景/家庭真的独立，也不认证跨数据版本泄漏排除 |
| 时长 | 9,848条length中5分钟以上为0；<30秒3,837，30—60秒5,943，60—300秒68 | CSV length不是媒体真实PTS，本来源单独长视频论文确认**FAIL** |

**公开官方关键佐证**：[Charades README](https://prior.allenai.org/projects/data/charades/README.txt)列`actions`为class-start-end三元组、`length`为以秒计的视频长度，并说明2017-02-27加入官方length字段，localize脚本25个等距时刻。**文档表面定义不支持未经实证擅自把30%越界解释为单位错误/进行缩放或截断**；无法判断冲突起因是不同修订/标注历史还是审计规则前提不适用。当前`DATA_SCHEMA=STRUCTURALLY_VERIFIED`，`DATA_INTERVAL_QUALITY=HOLD_RANGE_CONFLICT`、`P1/P2=PROVISIONAL_RECORD_LEVEL`、`PTS=UNKNOWN`、`NOVELTY_RETAIN0`、`LONGVIDEO_SINGLE_DATASET_FAIL`、`GPU=BLOCKED`。只有时间合同明确且严格科学先例审查通过才可再议新实验。

**唯一下一READY任务**：[VLM-BATCH-011 十项只读时间合同诊断](./codex-artifacts/VLM-BATCH-011/README.md)，在原用户批准的本地CSV/时间区间统计用途内**仅仅读取已下载SHA固定的原train/test CSV与类表，0新增下载、0新文件写原隔离目录、0原审计器更改**；单次纯stdlib合成测试后进行互斥错误因子+差额范围桶+视频层分布、原347/97723计数独立交叉验、先例与单位释义证据分级、泄漏/敏感小格隐匿，不泄露任一原始video/subject/class组合。只交2份脱敏报告、2个通用新脚本及一条结果（5处）。无实际字符或媒体时钟的基础证据则`HOLD_TIME_CONTRACT`，不自动下发下一轮数据/模型任务。用户在原Codex聊天主动启动，GitHub变动不会唤醒Codex。

### 2026-10-09 · BATCH-011独立数值验证验收及Charades科研止损（最新）

**交付核验**：[BATCH-011提交1aed0de](https://github.com/floomeer83felix-source/vlm/commit/1aed0dea70faa7a446e63637be4772f4668270a2)，严格2份脱敏报告、2份新通用stdlib代码+1条结果回报共5处；无已存CSV/ZIP重下载、原资产修改或修改老审计器。ChatGPT阅读[官方时间合同与完整性报告](./codex-artifacts/VLM-BATCH-011/official-time-contract-and-data-integrity.md)、[匿名差额/科学决定](./codex-artifacts/VLM-BATCH-011/aggregate-range-diagnostics-and-decision.md)及两份源码。执行者报告SHA固定、两解析器按同一数值合同复现原`66500` tokens/`19625`失败、P1`347`与P2`97723`；首次14合成测试PASS、修改披露抑制后15合成测试PASS，但最终披露代码未再次使用真实CSV计算。**并非ChatGPT独立取得本地原CSV复算，也不证明已建立媒体同原点时钟。** 仅接受交付/计数一致性，科学`HOLD_TIME_CONTRACT`。

**异常的新增可核数值**：绝对超范围差额`end-length`在(1,5]的记录至少8747条，不能统称小幅小数舍入；绝对差额或相对差额另有因避免还原小格而隐藏的分布。按行含至少一个不通过动作的比例，Train约73.8%，Test约82.5%；合计7433/9848行。P1严格gap>0合格组347中，270位于另含invalid动作的行（剩77仍只是符合当前规则的记录级余项）；P2异类重叠对97723中，67280与异常行共存（另一30443也不能认证同版媒体事件关系）。与原BATCH010一致，无基于新数据更改规则。直到有可靠同版动作端点和`length`时钟桥接信息前，旧`0≤start<end≤length`只是方便的数值筛选假设；非零候选不是真实排序、物理重复动作、语义并发或新VLM方法优势。

**直接学术先例新信息**：2025年ACL长文[Perfect Times](https://aclanthology.org/2025.acl-long.1000/)（Loginova & Ortega Loguinova）已经将Charades短视频用于动作完成、持续/时间关系的多语种多选VLM问答；[作者公开repo](https://github.com/ologin/PerfectTimes)还列出更新的时间顺序动作注释和问题模板。**已有公开论文覆盖的是宽泛的Charades temporal MCQA，不能据此断言P1严格同类实例错配已被完全解决。** 但不能将“基于Charades区间自动造时序问答”当新论文核心贡献。新增衍生注释的独立法律权利/来源修订和时钟映射未核；不下载或复制其数据/视频。

**最新科研决策**：BATCH-011`ACCEPTED`；`TIME_CONTRACT=HOLD`，`DATASET_AS_NATURAL_LONGVIDEO=FAIL`，`ORIGINAL_METHOD=RETAIN0`，`PTS=UNKNOWN`，`GPU/VIDEO/STA=BLOCKED`，用户已经授权的一次官方ZIP下载额度全部消耗，原ZIP/CSV只能按原许可保留本地，禁止任何公有重发布。**当前没有READY Codex父任务**；新`VLM-RESEARCH-DECISION-012=WAIT_USER_DIRECTION`由用户与ChatGPT确定是先找合法可证的同版时间坐标修订证明，还是优先寻找合法自然长时域视频+真值材料。不能因为009—011已花力气就继续在同一短视频数据上制造重复式toy/时间诊断，也不能直接拿另一个公开GitHub repo的更新标注替换原ZIP。

### 2026-10-09 · 用户确定保留Charades，优先修复官方评测口径与数值范围门混淆（最新）

**用户最新决定**：同意先不换数据集，将下轮由`WAIT_USER_DIRECTION`改为**Charades官方定位评测标准对齐与时间质量分层修复**；此“修复”严格表示**校验器和评测口径的修复、区分本来不同的问题**，不是认为源CSV损坏已证实或允许动原数据。上批[011独立只读核验](./codex-artifacts/VLM-BATCH-011/aggregate-range-diagnostics-and-decision.md)确定66,500原动作token中19,625不能通过我们自设的`0≤start<end≤length`，含异常视频行7,433。旧P1同类分离347组、P2异类重叠97,723 pair仅记录几何，`TIME_CONTRACT=HOLD`不变。不能因机器重新算出一致数字就宣称时钟语义成立。

**新的关键官方证据**：[Charades README](https://prior.allenai.org/projects/data/charades/README.txt)区分`actions`三元组、`length`为视频秒数与`Charades_v1_localize.m`在视频时长范围内等间隔采样25个时间点（0, L/25, …, 24L/25），其定义不直接要求`end≤length`才能纳入每点官方目标标签。然而源码实际起止比较、同类别聚合、无效端点策略需首先**从已获许可的固定SHA ZIP中只读核对原评测器文本**；不能凭README替代原脚本，不能执行MATLAB或下载官方评测器第二份。

**五项受控目标与科学门**：
1. 源完整性/许可：BATCH010官方ZIP SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，CSV与类表指纹须匹配，原Windows`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`目录只读、身份隔离核验；不新GET、不改ZIP/CSV。
2. 官方源码层`OFFICIAL_FRAME_COMPATIBILITY`：从ZIP内存读取唯一`Charades_v1_localize.m`文本，最多256KiB，核评测实际25点/端点/同类合并行为与现有`end>length`区间在采样点的贡献，只有取得脚本证据才准制作可比公式与标准库模拟；未取得就UNKNOWN/STOP。
3. 数据质量层`TIME_BOUNDARY_QUALITY`：把越界情况独立分`within`、`crosses video end`、`starts outside`、`invalid`并展示宏观分母；哪怕官方frame采样能接受越界条目，也**不**认证原标注端点精确、同一时间轴或物理事件真值。
4. 科学真值层`P1/P2_EVENT_TRUTH`：旧347/97723候选在严格筛选下只是几何资格，新官方评测对照不能生成可靠first/second QA、真实媒体PTS、模型错误、自然长视频或新机制；创新retain0，高水平论文目标不因评测器对齐自动PASS。
5. 可复现与隐私：只汇总训练/测试总体、官方帧级正label cell个数和与strict政策的差异、无效/越界类型、P1/P2保守效应；不输出frame×video×class矩阵、CSV行、脚本文本全文、受限标注或个人身份映射。合成反例先PASS，才可读真实CSV。未有模型预测不能计算官方mAP。

**唯一Codex READY**：[VLM-BATCH-012十项任务书](./codex-artifacts/VLM-BATCH-012/README.md)。Codex仅可提交该README指定2份脱敏报告、2份新标准库纯CPU源码+合成测试、`docs/codex-results.md`追加一条结果，共5处；旧原型/ZIP/CSV/研究环境/锁/账本不能编辑，0视频/帧/STA/新数据集/GPU/模型推理，0外部联系/PR合并。ZIP内原`.m`仅内存只读，不能执行或上传，校验失败STOP。**ChatGPT本轮只更新GitHub任务，没有从用户Windows读取原ZIP、没有运行校验/模拟或解决时间真值。** 保留用户原Codex聊天并需主动发送执行消息，提交结果后STOP等待科学审查。

**学术定位与下一岔路**：2021 AGQA补充材料曾指出部分Charades动作起止时间并不准确（不能仅靠官方评测兼容纠正）；2025 ACL`Perfect Times`已有基于Charades时间关系VLM问答，继续使用Charades需明确短域评测/原始区间真值/论文创新的不同证据。即使本轮`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY=VERIFIED`，`TIME_RANGE_QUALITY`和`EVENT_TRUTH`仍可HOLD。Charades约30秒不单独支持自然长视频论文；再进一步的媒体/PTS/长域合法资源必须另行选择与获权，不自动安排BATCH013。

### 2026-10-09 · BATCH-012验收：官方25点采样规则与额外strict过滤不等价（最新）

**交付与可信度分层**：检查[提交e46f1d7](https://github.com/floomeer83felix-source/vlm/commit/e46f1d794118c5c2efbb0f15f0fc84dad5d4f04b)：恰好两份脱敏报告、两份新stdlib通用源码及`docs/codex-results.md`追加一条父回报，共5处，没有上传ZIP/CSV/官方完整.m脚本，也未改原审计器/Windows模型环境。ChatGPT审阅了[官方评测器文本证据报告](./codex-artifacts/VLM-BATCH-012/official-evaluator-code-and-policy.md)、[三层对照及GO/NO-GO](./codex-artifacts/VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)、新代码及合成测试源码，但**未直接登录用户Windows复算原文件或执行MATLAB**。执行者报告此前合法下载的固定SHA`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`ZIP内唯一`Charades_v1_localize.m`，4,649B/155行，成员SHA`83eb3a2f30c87cc45db76235886f8d5331edb943acfdee8bab5656c5d51e0096`，仅在内存读/静态核其真实采样表达式；零新增HTTP/ZIP提取/数据写入。19项纯合成unittest报告1次全部通过，再执行一次合法现有CSV只读聚合。

**科学上确实修正的口径错误**：原官方脚本为每个视频在`t=(j/25)*length`（j=0..24，binary64先除后乘）取25点，在动作`start<=t<=end`时给对应class/point布尔正标签，多相同class动作布尔OR。它**没有**先将`end>length`的动作过滤掉。我们旧审计器`0<=start<end<=length`是额外区间质量条件，不能称作官方`frame-mAP`的标注构造合同。按Codex本地模拟的9,848行×25×157=38,653,400总cell，官方规则正cell **705,470**，先严格丢弃范围越界时正cell仅**398,287**，差异**307,183**（官方正cell的43.54%）。这不是307,183个动作或独立事件，更不是本轮计算的模型mAP。至少19,000条此前严格拒绝且`end>length`的动作token还能命中官方时间点（以预定1000宽度范围披露而非确数）。区间命中无需与媒体端点真实性等价。

**三层门独立冻结**：A`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY=VERIFIED_WITHIN_STATED_SCOPE`（本ZIP源码至有限、可解析、正length的25点label模拟；没运行MATLAB/端到端模型/真实媒体PTS，不认证浮点所有边界）；B`TIME_RANGE_QUALITY=HOLD`（原66,500 token中19,625不通过旧strict门，至少8,747条`end-length`介于1–5个CSV秒尺度，不擅自裁切/放缩/“救回正确”）；C`P1/P2_EVENT_TRUTH=HOLD`（原严格347同类分离组及97,723异类重叠pair仍是区间几何候选，即使grid-hit资格相同也不构成自然语言实例顺序真值）。创新机制retained0，Charades短域不独立证明自然长视频论文，原媒体/视觉/时钟/外部来源均未认证，GPU依旧BLOCKED。对外最可复用的是**官方评测标签构造与数据质量筛选分离**的准入机制，未来换数据集也先做此项口径核实以免重复损失。

**下一步不是无边界再检查**：BATCH012`ACCEPTED`，当前**没有任何READY**，用户需要先决定`VLM-RESEARCH-GATE-013=WAIT_USER_SCOPE_DECISION`：是否为B/C真值验证另行提出**合法且最小媒体样本+同版视频时钟证据**的独立授权，还是将Charades留作短视频工程对照、优先为真正自然长视频研究寻找合法可用的长时域公开素材（先做公开许可/时间合同准入，不直接下载）。没有用户明确的新媒体/STA/GPU许可，Codex不能继续下载、解码、运行模型或更新原研究工作区。先例[ACL2025 Perfect Times](https://aclanthology.org/2025.acl-long.1000/)仍限制简单Charades时序QA创新宣称，不因工程修复自动放宽。原ZIP与CSV留在约定的私有隔离目录，不能转存GitHub。

### 2026-10-09 · 用户选择方案A：Charades最小媒体PTS/标注边界试点，媒体授权仍单独等待（最新）

**用户决定**：在BATCH012官方25时点标签模拟成功、时间质量与事件真值继续HOLD后，用户回复“A”，即选择**继续Charades的真实视频—标注时间边界核验**，暂时不转向新数据集。此选择是研究路径决策，**没有独立授权下载或读取任何视频字节**；原BATCH010元数据单包授权已使用，不能扩大。ChatGPT只核公开官方项目页、README、license并完成[两视频有界试点提案](./charades-media-boundary-pilot-proposal-2026-10-09.md)与[任务看板](./next-steps.md)状态更新，未发媒体Range GET、无新文件访问或模型执行，当前没有任何Codex READY任务。

**关键准入风险**：[AllenAI官方Charades项目页](https://prior.allenai.org/projects/charades)公开视频入口为**480p整ZIP约13GB**和原版整包约55GB，**没有明确列出官方逐视频URL**。公开[官方README](https://prior.allenai.org/projects/data/charades/README.txt)描述转码mp4及原版帧率/分辨率保持行为，不能自动推论480p版的PTS与CSV`length`和动作端点都同一版本；[non-commercial license](https://prior.allenai.org/projects/data/charades/license.txt)限制向第三方分发/修改后公开发布原数据。一个极小两视频试点在权限、媒体选取和HTTP Range技术上**尚未证明实际可获取**；HEAD信息不足以证明206 Range或可低流量读取ZIP成员。**必须拒绝为了做两个视频实验而直接下载13GB整包**，除非另有用户明确新授权（本研究当前不建议）。

**两阶段证据协议（尚未执行）**：[详细方案A](./charades-media-boundary-pilot-proposal-2026-10-09.md)预计最多2个train split视频：一个在CSV中满足`start<length<end`且`end-length`在(1,5]，一个同等时长量级、尽量不同subject且无数值异常的匹配对照。仅私有本地固定选择，不能公开原video/subject身份或行。**V1**若另获用户批准，媒体下载正文总量拟≤64MiB（包含ZIP末尾/目录等range读取）、本地媒体总占用拟≤128MiB、固定独立Windows目录`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，只读用**已存在**CPU ffprobe/ffmpeg观察容器duration/start_time、stream time_base、首尾帧PTS，和CSV length/end对照。若Range不支持、回整包200、ZIP成员不可确定、要装依赖或需要超过预算，**立即STOP**，不能改用镜像、13GB整包或原RTX3090实验环境。**V2**任何可视核对/人工事件边界认定/模型分析必须**再单独授权**。

**科学边界**：V1即使可行，只检验**最多两例**的容器/媒体时钟与CSV一致性，不代表全部19,625条越界时段已修复；不能以PTS时钟报告确认动作起止的视觉真值。原BATCH012的A frame-label政策仍`VERIFIED_WITHIN_STATED_SCOPE`，B`TIME_RANGE_QUALITY=HOLD`，C`P1/P2_EVENT_TRUTH=HOLD`，创新retain0、自然长域Charades独立确认FAIL、GPU/视频下载依旧**未获授权**。下一唯一门：用户是否单独批准上述**最多两段、总网络≤64MiB、仅V1 CPU媒体钟**的条件式试点；在此之前不得新增READY或触发Codex视频任务。

### 2026-10-09 · 用户正式批准Charades最多两段官方480p视频的V1时钟核验（最新）

**用户额外明确授权**：在已选择方案A继续Charades的基础上，用户回复“批准”确认：[V1两视频条件式试点](./charades-media-boundary-pilot-proposal-2026-10-09.md)。授权仅涵盖**最多2段Charades官方480p视频**、全部HTTP GET响应正文（包括ZIP tail/central directory/local headers、媒体数据和失败已读字节）**总≤64MiB**，本地本轮媒体＋临时文件合计**≤128MiB**，且仅使用本机既有CPU`ffprobe`核**MP4容器元信息、视频packet PTS/DTS与timebase**。不授权13GB整ZIP、视频画面/音频人工观察、像素帧解码/抽帧、视觉事件标注、Qwen/GPU/模型训练/推理、STA、Ego4D或原RTX3090实验目录/conda/CUDA/锁/账本改动。**许可范围是条件授权，不保证一定有可获取的两段视频；本轮ChatGPT未下载任何媒体或访问用户Windows。**

**官方访问技术门**：[AllenAI Charades下载页](https://prior.allenai.org/projects/charades)公开的480p链接指向整个约13GB`Charades_v1_480.zip`，不是已验证的独立MP4直链。必须从官方域名稳定S3对象用HTTPS `206 Content-Range`按需检验ZIP EOCD/ZIP64、中央目录及两成员，实际206不支持、服务器返回200整包、索引无法可靠解析、源版本/压缩CRC/成员映射不唯一、或总流量超过64MiB预算，**立即STOP，不允许下载整包或改第三方镜像**。限最多12个Range GET、全部正文全局字节ledger、逐块stream/响应范围与同对象ETag确认、媒体本地128MiB实存硬限。要在真正网络GET之前首先通过与所有相关错误分支覆盖的**纯合成HTTP/ZIP标准库unittest**，不能靠真实服务响应现场修改来源选择和规则。

**冻结样本与隔离路径**：原合法取得的Charades注释仍只读保留在`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`，SHA与BATCH010-012固定；新媒体仅写独立`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`，事先校验Windows实际物理路径、无reparse/symlink/junction/云同步、无与Git checkout或原研究资产相交、≥512MiB磁盘空闲及工具已安装。私有确定性选1训练视频`0≤start<length<end,end-length∈(1,5]`，另选1整行无数值越界的train对照，时长粗匹配且优先不同subject。身份、zip成员名、精确端点与媒体sha只存本地，公共GitHub只提交匿名总体计数/结论，不得反推出两例来源。

**V1证据与不能做什么**：现有CPU`ffprobe`只读取容器/视频包的PTS等元信息，**不使用`-show_frames`或输出像素/截图，不视觉判断动作实例是否出现**。单个MP4的container/stream duration、start、video packet首末时刻可能不完全等价；时钟差异应分`CLOCK_APPROX_MATCH / DIFFERS / UNKNOWN`而非恣意把某种时刻当真实视频末帧。即便成功最多2例，也只支持这两例的媒体/CSV时间原点线索，不能推广19,625条旧strict不通过动作、P1=347组、P2=97,723对，更不能令B时间质量/C实例真实边界/论文创新自动通过。BATCH012官方frame label政策继续限域VERIFIED，B/C保持HOLD，创新retain0，Charades不足自然长视频独立confirm。

**唯一READY父任务**：[VLM-BATCH-013完整受限10项执行README](./codex-artifacts/VLM-BATCH-013/README.md)。在原Codex聊天由用户主动启动，安全读取AGENTS/任务看板/结果和协议，按源完整性→隔离/已有工具→合成test→私有2例选择→206 ZIP索引安全→小量最多两MP4→CPU packet PTS→匿名时钟裁决执行。**只许5处公共GitHub提交**：2份脱敏报告、2份独立通用stdlib pilot与synthetic test、`docs/codex-results.md`尾部一条父任务回报；绝不上传原video/压缩片段/具体video/subject映射/小格PTS/帧/私人路径，也不触碰旧计划。任一前置不通过就交BLOCKED收据后STOP，不因用户已授权就必须消耗所有预算或完成媒体取得。成功普通push即停留原Codex聊天，等待ChatGPT验收。任何V2视觉真实性、更多数据、GPU预算均须以后**单独向用户申请**。

### 2026-10-09 · VLM-BATCH-013阻塞验收与75af33c独立源码修复审查（最新）

**原父任务状态**：[原BATCH-013提交f86a1e8](https://github.com/floomeer83felix-source/vlm/commit/f86a1e8e7a2e31b40d9c1bd7f1b135d16ae25204)按任务书5处交付（两份脱敏报告+两份标准库源文件+一条结果），在第1项**既有独立CPU ffprobe不可定位**的工具门安全停止。有限PATH/常见路径/登记runtime检查未发现可用入口，不构成“全机绝无ffprobe”；对已存原标注ZIP/training/classes哈希，执行者报告匹配。**全部Charades媒体HTTP网页/HEAD/Range请求0、返回正文0B、新视频0、packet PTS=UNKNOWN**；新媒体根和私有选择/账本未创建，原研究conda/CUDA/锁/模型没有触碰。不能以“取媒体失败”描述，因为并未尝试远端取样。原父任务已追加回报，**不得重做013**，任务书历史READY不可继续引用。

**本轮用户报告的独立修复**：[提交75af33c](https://github.com/floomeer83felix-source/vlm/commit/75af33c56342bce4af94f7d70d1cada7ebdb8667)，**恰好3处文件**：改`prototypes/charades_range_media_clock_pilot.py`及对应synthetic unittest，另向`docs/codex-results.md`追加`VLM-BATCH-013-FIX`条目，不更改历史阻塞报告/任务板/原ZIP/CSV。执行者报告在本机完成5轮合成测试扩展、最终**27项测试全部PASS**；GitHub源文件中亦可枚举27个test方法。新源码涵盖：单盘ZIP64 EOCD/locator/central extra等有限受支持格式、按需官方206 Range两媒体成员协调、持久化64MiB网络请求字节及128MiB本地临时+媒体账本、确定性私密选样、限制原工作区和重解析路径、packet ffprobe mock、对完成父任务和非唯一READY严格拒绝。**所有测试的HTTP/视频/PTS均为虚构或mock，ChatGPT没有在Windows复测，不能宣称真实服务器、CSV媒体映射、PTS时钟已验收。** FIX未下载媒体、未安装CPU工具、未运行真实ffprobe、不重跑013。

**独立审查新发现：网络代理隐患**。当前Python静态源码有`urllib.request.build_opener(NoRedirect())`：NoRedirect仅拒绝HTTP重定向，但标准库的默认ProxyHandler可能继承系统或环境代理。原试点限定直接官方HTTPS来源、禁止代理/镜像，故未来真实Range GET之前必须补充**明确禁用代理/验证直连**的安全审查及synthetic防回归测试。也不能把新增ZIP64解析的有限合成覆盖当成所有13GB真档可处理。**新代码本身代码交付ACCEPTED_CODE_ONLY，不是执行GO**。

**下一门`VLM-CPU-TOOL-GATE-014=WAIT_USER_TOOL_SCOPE_APPROVAL`，当前没有READY。** Codex进一步查找独立`ffprobe`也未发现现成入口，提出过是否在`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`隔离部署仅CPU工具的问题。**用户尚未单独批准下载安装新CPU工具**，因此目前不能获取其安装包或改PATH、Conda、原科研工作区；来源/许可证/安装体积与哈希仍须先核定。用户原已批准**最多2个视频/64MiB全部GET正文/128MiB本地/仅CPU packet-PTS**的条件试点仍限定范围，但不等于工具安装批准或旧父任务复跑许可。得到新的独立用户决定后，应先由ChatGPT制定隔离工具的供应链/成本上限与代理安全修复，发放**全新唯一READY父任务**，失败就STOP。BATCH012 A官方frame标签政策仍限域VERIFIED，B时间边界质量与C事件真值均HOLD，Charades不是独立长视频证明，科学创新retain0，GPU/V2视频画面核验继续BLOCKED。

### 2026-10-09 · 用户批准独立CPU ffprobe工具供应链获取与隔离部署（最新）

**本轮新增的清晰用户授权**：在BATCH013因“没有找到现有非原科研Conda的ffprobe”安全停止、[BATCH013-FIX提交75af33c](https://github.com/floomeer83felix-source/vlm/commit/75af33c56342bce4af94f7d70d1cada7ebdb8667)仅补齐有限ZIP64与协调器合成测试之后，用户明确回复**“批准”**独立CPU ffprobe安装方案。授权**只**为后续V1两视频packet时间轴研究准备工具；可以在固定Windows独立根`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`内经来源/发布者SHA/ZIP安全核验获取并白名单提取一份CPU ffprobe.exe，最多运行一次`-version`。**这不是再次运行BATCH013、Charades视频下载/Range、帧解码/视觉研究、GPU/模型、Conda/CUDA/RTX3090原研究资产编辑或全局PATH更改许可**。ChatGPT这轮只写GitHub文档，没有实际下载工具或进入用户Windows，工具状态仍UNKNOWN。

**供应链冻结与范围校验**：[FFmpeg官方下载页](https://ffmpeg.org/download.html#build-windows)声明其直接提供源码，推荐Gyan.dev与BtbN这类第三方Windows编译提供者；[Gyan.dev Windows构建页](https://www.gyan.dev/ffmpeg/builds/)列出含ffprobe的x64静态发布包，release essentials 9.0.2 ZIP官网约109MB、GPLv3，2026-10-09从官网对应SHA链接解出固定`https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip`及其[发布者checksum文本](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip.sha256) SHA256 `60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`。**这只是发布同源hash校验，不是发布者数字签名或独立供应链密码学证明；FFmpeg项目没有直接签署此Windows二进制。** 如具体URL、版本、当前hash/许可证或ZIP数据不符合上述冻结值，即STOP，不改用latest/镜像/7z工具/系统安装器，不扩大许可。

**新唯一READY任务**：[VLM-BATCH-014十项隔离工具任务](./codex-artifacts/VLM-BATCH-014/README.md)要求：（1）旧项目/唯一READY/无旧父结果，（2）原实验树与真实LOCALAPPDATA/云目录物理隔离、磁盘≥1GiB，（3）FFmpeg→Gyan供应链及固定SHA+GPL说明，（4）至少12个纯合成安全用例先PASS，（5）明确禁代理/TLS/重定向、工具全部GET正文合计**≤150MiB**、本地总占用**≤512MiB**、一次成功ZIP下载有限重试，（6）标准库ZIP中央目录/路径/ZIPCRC/压缩安全且只提取唯一`ffprobe.exe`及必要许可，（7）绝对私有路径一次`ffprobe -version`健康检查，不读任何视频/CSV，（8）**只静态审查**原BATCH013-FIX网络协调器可能默认继承Python系统`ProxyHandler`的风险，不修改/放行该媒体客户端，（9）用户隐私/预算/供应链收据，（10）工具、视频和科学门分别记录并停止。只交2份脱敏报告、2份新的纯标准库安装器与synthetic unittest、`docs/codex-results.md`末尾1条父任务回报，共5处；不能提交.exe、ZIP或私有安装路径、历史代码/计划改动。

**仍在HOLD的媒体门与科学限度**：BATCH013原父任务已STOPPED_SAFELY并上传回报，不能重跑；BATCH013-FIX是ACCEPTED_CODE_ONLY，虽然27个合成用例由执行者报告通过，但真206/ZIP64/packet媒体时钟未验证。当前`urllib.request.build_opener(NoRedirect())`对媒体HTTP默认代理配置存在风险，需要后续独立新父任务**修复/验证无代理**后，才能考虑已有限授权的最多2个Charades视频、媒体全部GET正文≤64MiB和本地媒体≤128MiB的V1试点。014取得独立ffprobe也不会自动消费媒体授权或建立时间真值。Charades A官方25点frame label已限域VERIFIED；B时间边界质量/C同类事件实例真值继续HOLD，创新retain0、单独自然长时域验证FAIL、GPU仍BLOCKED。

### 2026-10-09 · BATCH-014工具下载安装超时后验收：部分包保留，禁止重跑（最新）

**已验收文件与可信度**：[提交6bec3ab](https://github.com/floomeer83felix-source/vlm/commit/6bec3ab3e7e41571b8878e30c36b26ca710fd060)严格5处（[供应链与隔离收据](./codex-artifacts/VLM-BATCH-014/tool-source-integrity-and-isolation.md)、[就绪/代理门](./codex-artifacts/VLM-BATCH-014/ffprobe-readiness-and-proxy-hold.md)、新`prototypes/isolated_ffprobe_installer.py`及虚构unittest、`docs/codex-results.md`只追加一个014结果）。Codex执行者报告安全sync/固定隔离预检、FFmpeg官网→Gyan.dev第三方x64/GPLv3发布来源与9.0.2同站checksum固定`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`一致，工具客户端显式`ProxyHandler({})`/TLS/NoRedirect。首次合成测试发现长度超额剩余预算预读未拒绝并修复，随后修正新根父目录处理，**最终16个synthetic unittest通过（执行者本地回报，ChatGPT静态阅读源码/方法，未独立在Windows跑）**。这属于按安全边界合规终止的工程交付，而不是工具可执行性PASS。

**硬资源收据与根因**：所有本轮GET正文**13,186,907字节**，包括官网文本27,484B、Gyan页52,159B、发布方checksum64B以及**固定9.0.2 ZIP GET仅13,107,200B后直连socket timeout**；4次GET/3次HEAD，ZIP成功全包0、额外重试0。私有部分ZIP和持久账本两个文件共13,107,774B，精确峰值存储UNKNOWN，保守上界14,155,776B；工具完整包SHA、真实ZIP结构/CRC、解压和`ffprobe -version`均**未执行/UNKNOWN**，0 ffprobe.exe安装。发布者SHA文本匹配不是实际不完整ZIP SHA已验证。原文档checkout除本次5处外没有其他变更，0原Windows实验工作区/Conda/CUDA/模型/锁/旧数据修改，0 Charades媒体/Range/PTS/帧/STA/GPU。

**专门留待未来的新门，不作自动补救**：`VLM-BATCH-014=STOPPED_SAFELY / CPU_TOOL_BLOCKED`，014回报已经存在，不允许Codex重跑原父任务、覆盖part/账本/从零算150MiB。当前唯一`VLM-CPU-TOOL-GATE-015=WAIT_USER_CONTINUATION_CHOICE`（**没有READY**）；如果用户愿意继续，应另行制定单个有界新父任务，优先核实原冻结对象的Content-Length、稳定ETag与206 Range续传可行性，并验证现存私有part长度/最后位置/文件hash与原累计账本**连续记账**；如果不支持可靠续传则STOP、不能换镜像或一次性任意重下工具，未取得新执行权限不能发任何新工具正文GET。不得因历史“允许下载ffprobe”自动反复重试，需用户选择新方向。若暂停则保留现状，不删除用户部分文件。

**学术和网络门仍未改变**：[BATCH013-FIX媒体网络客户端](../prototypes/charades_range_media_clock_pilot.py)还存在`urllib.request.build_opener(NoRedirect())`隐式ProxyHandler风险，014工具安装器禁代理不能替媒体端背书。CPU工具即使未来安装成功，仍需新媒体验证协议及代理防回归；目前视频GET/真实packet-PTS均0，B时间质量与C事件真值继续HOLD，Charades作为自然长视频独立基准FAIL，原始方法创新retain0，模型/GPU不可用。本轮ChatGPT只更新GitHub任务看板/总览，未访问用户Windows/工具部分包或触发后台下载。

### 2026-10-10 · 用户选择同源有界断点续传：015唯一READY，原Windows与206尚未验证（最新）

**授权与真实执行严格区分**：用户明确回复“继续安全断点续传方向。请先核对原部分工具包、同源ETag/Range206、剩余累计预算及安全条件，在GitHub制定新的有限任务；禁止重跑014，不得下载Charades媒体或使用GPU。” ChatGPT核对[BATCH014来源与隔离收据](./codex-artifacts/VLM-BATCH-014/tool-source-integrity-and-isolation.md)、[资源记录](./codex-results.md)、[原工具安装器](../prototypes/isolated_ffprobe_installer.py)后，制定[新BATCH-015唯一父任务](./codex-artifacts/VLM-BATCH-015/README.md)；没有读取用户Windows原part/ledger、没有在用户机器上发出HEAD/Range/GET，也没有调用ffprobe。尝试ChatGPT所在环境对固定Gyan ZIP发**无代理HEAD**时，独立环境DNS无法解析`www.gyan.dev`，**不能据此认定目标服务器停机或有/无206支持**。公开[Gyan构建页](https://www.gyan.dev/ffmpeg/builds/)现仍列9.0.2 release essentials ZIP约109MB，但网页展示的大小不等于当前实际HEAD Content-Length/strong ETag/206事实。此不确定性是新父任务的首要STOP门。

**当前可复核的确定预算（执行者报告，未本机复算）**：014原GET正文累计`13,186,907B`（三网页/发布方checksum与原工具ZIP），其中原ZIP部分`13,107,200B`，原父任务4 GET/3 HEAD，1工具包GET未完成，软件未安装。原工具正文硬限150MiB=`157,286,400B`，剩余严格`144,099,493B`（包括可能的新小量206测试和失败已读响应正文，不能另算150MiB）。原部分文件在`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\incoming\ffmpeg-9.0.2.zip.part`，原私有`local-audit/tool-ledger.json`；这是上轮报告指出的预期路径与字节数，**未实地证明现存文件未被更改或ledger仍完整**。

**对同源身份的科学和工程证据分级**：014没有保存首次GET对应的稳定ETag/完整包Content-Length，也没有公开部分文件SHA。因此015必须先只读核Windows固定原part(13,107,200B)及014ledger(body 13,186,907B、events/失败状态/4 GET/3 HEAD)，路径/reparse/cloud/原研究区排除及磁盘，然后**先合成≥18单测**覆盖账本继承与预算/断电，再只对同一固定Gyan9.0.2 ZIP发最多2次HEAD与至多2次GET（≤4KiB旧part尾端匹配206探测+**唯一**原offset后缀206 GET），要求strong ETag、精确Content-Range/Length、identity传输、禁代理TLS/禁跳转、If-Range及全局账本跨批连续、任何200整包都不读正文；0自动重试。**新HEAD强ETag只能约束新会话，不能追证014初次13MB所属对象。只有拼合得到完整ZIP的SHA256完全匹配原冻结发布方值`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`，才说明原part与新suffix共同组成已知发布包**；不匹配STOP，不删旧part/ledger、不换源或重新下完整包。

**恢复成功上限**：只有经固定SHA核真实ZIP安全目录、CRC、版本/许可证、无重复/危险路径、预算≤512MiB后才可向独立`CPU-Tools/ffprobe/bin/`白名单提取唯一`ffprobe.exe`并运行一次`-version`，无需修改PATH/Conda/CUDA/原研究代码/锁。失败则只交匿名STOP收据。此父任务只许[README中5处白名单](./codex-artifacts/VLM-BATCH-015/README.md)：2脱敏报告、2份全新纯stdlib续传器及虚构HTTP/ZIP测试、`docs/codex-results.md`尾部一次015回报。禁止重跑已回报014、改原014代码/ledger历史/part前缀，媒体相关`GET`完全为0、GPU/真实视频PTS/模型及视觉画面均不授权。

**研究主门不随工具自动提升**：BATCH012官方frame标签A限域VERIFIED；Charades边界B/事件实例C继续HOLD、创新retain0、自然长视频独立支持FAIL。媒体协调器013-FIX还可能默认继承Python环境/系统代理设置，`MEDIA_NETWORK_CLIENT_PROXY=HOLD`，本批不得修改/运行旧媒体脚本。即使工具可用，只有ChatGPT审查后重新安排独立媒体安全修复/新父任务，才可考虑原用户之前有限的最多2视频/64MiB的合法媒体V1试点，绝不自动启动。Codex执行启动仍需用户在**同一原聊天**主动发指令；GitHub READY不是后台执行。

### 2026-10-10 · BATCH015完整工具恢复已验收；只放行016禁代理离线安全修复（最新）

**交付精确范围**：[BATCH015提交b0d163f](https://github.com/floomeer83felix-source/vlm/commit/b0d163f9f9ea76c4887b08109a729d0bb47b4033)严格5处：2份匿名报告（[原part/Range/双账本](./codex-artifacts/VLM-BATCH-015/local-part-ledger-and-remote-identity.md)、[真实包SHA/工具就绪](./codex-artifacts/VLM-BATCH-015/resume-integrity-install-and-science-decision.md)），两份全新Python resumer/合成tests以及`docs/codex-results.md`一条父回报。ChatGPT通过连接的GitHub逐份审阅报告与代码、核27个unittest方法；**并未访问用户Windows原part/ledger/可执行程序、也未独立实际执行GET/版本测试**。Codex报告最初26个合成测试PASS，增补“失败探测不允许后缀续传”后最终27 PASS，均在真实网络前完成。

**真实工具来源/帐本合规证据（基于执行者回报）**：原014部分ZIP普通单链接原文件13,107,200B及旧574B账本一致，旧全部工具GET正文13,186,907B未重置/未重写。015仅2个HEAD核同一固定9.0.2 Gyan ZIP对象的`Content-Length=114,768,076B`和同strong ETag；实际1B原尾边界206探测字节匹配，紧接唯一一次`If-Range` 206后缀GET读101,660,876B，均固定源/NoRedirect/显式禁代理、ETag/Content-Range/Content-Length完整验证，0镜像/全包重下/重试。全包114,768,076B的SHA256等于冻结发布方`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`，并再次只读复核；`zipfile`安全成员及全CRC PASS，**仅**在原独立CPU工具树白名单释放`bin/ffprobe.exe`、LICENSE和README.txt，不释放其它二进制。独立CPU`ffprobe -version`实际调用一次、返回0、`9.0.2-essentials_build-www.gyan.dev`，没有视频输入。**固定发布方SHA不是独立数字签名或恶意软件安全证明**，`Authenticode=UNKNOWN_NOT_CHECKED`。

**资源与隐私**：本轮实际工具GET正文101,660,877B（1B探测+后缀），两轮工具总GET正文**114,847,784B**，仍低于原150MiB=157,286,400B且剩余42,438,616B；没有新拨款。新HEAD2/GET2、重试0；原part前缀/原ledger保留不改（仅原part append），新私有ledger独占创建。最终本地6文件逻辑和220,068,317B，最大观测逻辑和325,212,443B、含额外1MiB暂存保守上界326,261,019B<512MiB，**精确物理磁盘峰值未测**。私有ETag/部分sha/ffprobe exe hash/本地路径/旧ledger及ZIP均不提交公开GitHub；0 Charades视频/Range、0媒体packet-PTS/画面/动作观察/模型GPU、0原Windows实验环境/Conda/PATH/CUDA/原metadata改动。

**三层技术结论**：`BATCH015=ACCEPTED`；`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED`限于执行者Windows和同发布方SHA来源；`TOOL_RANGE_SUPPORT=VERIFIED_206`仅适用于Gyan固定工具ZIP**不**能外推至AllenAI视频档；旧[013-FIX媒体客户端](../prototypes/charades_range_media_clock_pilot.py)仍用`urllib.request.build_opener(NoRedirect())`可能默继承系统/环境`ProxyHandler`，故`MEDIA_NETWORK_CLIENT_PROXY=HOLD`，即使工具成功也**不得重跑旧013或自动发起已限额许可的2段视频GET**。Charades官方frame标签A保持旧012限域VERIFIED、B区间质量/C事件真值HOLD，创新retain0、长视频外推FAIL、GPU BLOCKED。

**唯一新READY是无真实媒体的安全代码父任务**：[VLM-BATCH-016 README](./codex-artifacts/VLM-BATCH-016/README.md)：八项任务，精确更改`prototypes/charades_range_media_clock_pilot.py`及其合成test，显式禁代理`ProxyHandler({})`、TLS默认验证、禁止HTTP重定向、固定官网网页与媒体ZIP URL白名单，检查所有真实urllib路径，并用≥30纯合成unittest反例验证不从系统获取代理及200/错误Content-Range防泄漏/预算/老013完成锁继续有效。额外2份脱敏报告和`docs/codex-results.md`尾部1条共5处白名单。**0真实Gyan/Charades GET或HEAD、0实际ffprobe命令、0视频/PTS/模型GPU**；代码门PASS不构成媒体V1真实网络GO。Codex提交后STOP，由ChatGPT复核是否值得启动另一个独立媒体试点父任务。当前不因投入了16轮审计就默认算法创新；学术本体机制retain0。

### 2026-10-10 · BATCH016纯代码安全验收；017以既有两视频授权设唯一条件式V1（最新）

**已独立GitHub代码审查**：[BATCH016提交4c3e8bf](https://github.com/floomeer83felix-source/vlm/commit/4c3e8bf14ad9c62806be85e26e0492cfea5ebf93)精确五处：`docs/codex-artifacts/VLM-BATCH-016/`两份[代理路径与修复](./codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md)、[测试收据/科学门](./codex-artifacts/VLM-BATCH-016/code-only-test-and-science-gate.md)，原`prototypes/charades_range_media_clock_pilot.py`与其test，以及`docs/codex-results.md`尾部一条016回报。ChatGPT用Github审查完整逻辑与新增合成反例方法，**没有访问Windows运行任何命令**。Codex报告原27测试保留新增13，总40纯合成`unittest`最终PASS；首轮308 redirect handling和测试假header问题导致1 FAIL/1 ERROR，修正后没有失败/跳过。新增专用`build_media_opener()`明确`ProxyHandler({})`，TLS默认证书验证/NoRedirect，统一`fixed_request()`精确许可3个官方HTTPS来源（2篇文本+1 S3媒体ZIP）及方法白名单，S3只限HEAD或显式bounded Range/If-Range GET；全部官网/许可/ZIP HEAD/Range共享同一禁代理实例，没有新URL或兜底`urlopen`。从代码静态和执行者合成测验可授予`MEDIA_CLIENT_PROXY_POLICY=CODE_LEVEL_VERIFIED`，**而不是**真实线路/TLS对端或AllenAI的206/视频版时钟可用性已验证。执行者报告本批0 Charades/Gyan GET/HEAD、0媒体/PTS/ffprobe/GPU/模型、0私有研究环境变更，旧预算64MiB媒体网络/128MiB盘/两视频/12 GET冻结不变。

**研究所需最后的网络前安全门**：进一步查看原媒体协调器残余`Ledger`：原`read_response`和`RangeClient.text`均在实际`response.read(n)`**之后**才`ledger.add(n)`，若进程在read成功后、记账前退出可低报预算；原`run_pilot`会在检查父任务READY/历史回报之前先调用`ffprobe -version`，属于权限顺序不够严。BATCH016专注代理没有授权修改这些路径，故这不是016验收失败，但**真实联网必须先补足**。新媒体会使用另一套独立预算，不得挪用BATCH014/015工具原150MiB。媒体官方S3 ZIP约13GB的HEAD/强ETag/206/ZIP64/member可得性至今未证；工具包Gyan的206成功不能充当AllenAI录像对象证据。

**先前用户有明确的V1有限媒体授权**：最多2段官方480p视频、研究GET全部HTTP正文≤64MiB=67,108,864B、本地媒体/临时≤128MiB=134,217,728B、CPU既有ffprobe仅packet PTS和容器元信息，**不授权13GB整包、镜像/系统代理/STA、视频图像/动作人工观看、训练模型/GPU/原科研workspace改动**。BATCH015 ffprobe9.0.2工具现已在独立CPU-Tools隔离目录按供应商固定ZIP SHA与一次version由执行者报告可用，没有消耗媒体预算。因此ChatGPT推出[唯一BATCH017完整十项协议](./codex-artifacts/VLM-BATCH-017/README.md)：**先**修父任务许可在ffprobe/任何副作用前核验、所有官网文本及媒体Range的实际读取前持久保守reserve网络额度、崩溃不退、GET≤12/禁重试；**再**在纯虚构场景使原40项测试保留加≥12项共≥52 PASS；**再**只读核Windows原metadata ZIP/CSV/类表固定SHA和隔离、既有CPU ffprobe工具，以冻结的确定算法选1越界`0≤start<length<end,end-length∈(1,5]`与1严格合法训练视频，先选后核远端。只有所有门PASS，才准一次性有界访问官网文本和官方S3 ZIP的HEAD/206尾部ZIP64目录/指定两成员，预算不够/返回200整档/强ETag缺/ZIP不可安全解析即STOP；成功只做两例MP4容器与video packet PTS/CSV `length`的类别化对照。不允许抄出两视频身份/精确PTS或人工动作边界真值。新父任务完成只交2匿名报告、两项现有媒体代码/tests修改和一条总回报（5处），**不自动启动018**。

**科学状态**：即使017取得真实两个MP4的container、first/last video packet时刻并与`length`对比，最多得到2例时钟与版本线索，`OFFICIAL_FRAME_LABEL=A_VERIFIED_WITHIN_012_SCOPE`维持；`B_TIME_BOUNDARY_QUALITY=HOLD`、`C_P1/P2_EVENT_TRUTH=HOLD`，不能认为原19,625条strict拒绝标注都真实错误/都可修正；独立自然长视频适用性FAIL、原创机制retained0、GPU继续BLOCKED。ChatGPT本轮只发布GitHub协议，不执行媒体HTTP或直接读取用户Windows；**READY不等于两段视频已经下载或可下载**。

### 2026-10-10 · BATCH017仅代码及合成夹具成功，实际execute在内置合成门安全STOP（最新）

**GitHub交付验收与实际执行必须分开**：[BATCH017提交1641817](https://github.com/floomeer83felix-source/vlm/commit/1641817a05911d008373963d5cea88a45f1cb8b6)严格5处：两份脱敏[真实访问与预算收据](./codex-artifacts/VLM-BATCH-017/media-v1-access-and-budget-receipt.md)、[两臂时钟科学门](./codex-artifacts/VLM-BATCH-017/two-case-clock-and-science-decision.md)，修改`prototypes/charades_range_media_clock_pilot.py`及其仅合成test，`docs/codex-results.md`尾部只追加一次父任务报告。ChatGPT通过连接的GitHub逐项检查文件、读源码与风险，**未登录用户Windows重新运行**。本批保守父任务权限先于任何工具/存储/网络，017合同及013—016历史段SHA绑定、只接受017且检查READY和既有回报、非执行模式无工具副作用；媒体`Ledger`增加`charged_bytes`及独立`body_bytes`，每次真实`response.read`之前先对≤64KiB块持久原子fsync保守预扣（失败/短读不退）、官网和许可文本/媒体Range共用原64MiB上限与GET≤12；强ETag、固定015 CPU ffprobe私有路径及只读私有部署收据校验、016显式禁代理/TLS/无跳转/固定URL逻辑保留。**这些是按代码审查和执行者测试的工程修复结论，不是实际媒体证据。**

**真实执行停于哪一道门**：Codex先在普通本地环境将原40合成测试扩展为56（新增16），首轮55PASS/1FAIL是旧模拟Range缺`reserve`，修正后56全PASS。**仅一次真正`--execute --parent-task VLM-BATCH-017`**，但是此入口自带的合成`unittest`在原Windows研究工作区环境变量下，因为旧“拒绝Conda路径”的合成测试`Path.resolve` mock与新的祖先`check_ancestors`冲突，抛`AuditError`，所以报`BLOCKED_SYNTHETIC_GATE_FAILED`并停止。后续仅离线在合成`LOCALAPPDATA`及模拟原工作区环境中复现并补虚构路径mock，最后普通上下文56/56 PASS、模拟工作区上下文56/56 PASS；**未再启动真实execute，不允许把最终回归PASS追认为真实试点PASS**。这还暴露测试隔离细节：出错的旧mock没有完全屏蔽只读祖先文件身份stat，因此仅能说没有正式受保护内容的读取或工具调用，不能夸称对所有真实文件元数据完全0触达。

**无用户媒体消耗与真值绝不升级**：本批0真实官方项目/许可GET、0 S3 HEAD或Range GET、0媒体研究HTTP实际正文与保守预留字节、0 Gyan工具GET、0新MP4/MediaPilot根或实际网络ledger；原train/ZIP/classes SHA的**正式本机预检未执行**，已部署ffprobe的**本轮正式路径/版本调用未执行**，两例身份根本未选择/未获取、packet-PTS=NOT_RUN。不能凭这批判定服务器是否206/ZIP可读、媒体`length`是否对应真实视频钟、动作`end`是否正确，亦不可产生任何P1/P2实例事实。科学层A`OFFICIAL_FRAME_LABEL=VERIFIED_WITHIN_012_SCOPE`，B`TIME_RANGE_QUALITY=HOLD`，C`P1/P2_EVENT_TRUTH=HOLD`，原创机制`RETAIN0`，Charades作为自然长时域唯一数据`FAIL`、GPU/模型/视频可视真值`BLOCKED`均未改变。

**当前科研管理决定**：`BATCH017=CODE_DELIVERABLES_ACCEPTED / EXECUTION_STOPPED_SAFELY`，旧017唯一execute已经用过并在`docs/codex-results.md`有回报，**严禁复跑或抹去ledger/历史结果**。目前`VLM-RESEARCH-CHOICE-018=WAIT_USER_NEXT_PILOT_DECISION`、**没有READY任务**。用户需明确决定是否在旧媒体许可上限内给一个**全新且只再一次**的有界CPU时钟试点父任务（前置必须正式执行上下文和普通上下文合成检查均PASS），或止损结束Charades媒体获取，把它保留为短视频标签政策/质量工程对照，之后转向具有真实长视频与可审核时钟/许可合同的数据源。**不经用户再次明确选择就不能自动创建018 READY或重新发起网络请求。**

### 2026-10-10 · 用户明确同意最后一次全新Charades受限V1父任务BATCH-018（最新）

**授权事实和执行事实严格分开**：用户在知道[017的安全阻塞提交1641817](https://github.com/floomeer83felix-source/vlm/commit/1641817a05911d008373963d5cea88a45f1cb8b6)的情况下明确答复“同意”，仅准**再给一次新父任务**而不是重跑旧017。ChatGPT核已验收017的[阻塞报告](./codex-artifacts/VLM-BATCH-017/media-v1-access-and-budget-receipt.md)：017唯一正式execute在内置纯合成门被`SYNTHETIC_GATE_FAILED`阻断，未执行真实metadata SHA/媒体根/ffprobe/HEAD/GET/PTS，真实媒体正文/预留均0B；随后仅离线修旧Conda相关路径mock并报告普通环境和模拟工作区环境各56 PASS，不推断真正媒体已验证。新019等后续任务**不自动安排**。用户此前对最多2段官方480p、GET实际正文与保守预留≤64MiB、本地媒体+临时≤128MiB、既有CPU ffprobe packet-PTS的有限许可继续适用，但此次**不扩张**，禁止13GB全档/55GB版/STA/GPU/模型/视觉像素、旧研究环境更改及任何下载镜像。

**唯一READY是[完整BATCH-018十项合同](./codex-artifacts/VLM-BATCH-018/README.md)**。Codex在原持续聊天由用户显式启动，先安全fast-forward公开docs checkout、读取AGENTS/next-steps/codex-results/017阻塞/本018任务书，确认唯一READY=018且018未回报、013–017全部已结案；仅修改既有媒体协调器`PARENT`和新018`CONTRACT_SHA`，并将017公开回报段落SHA加入`HISTORY_SHA`，继续固定旧历史哈希，不通过假合同或仅关键词绕过权限门。原媒体`Ledger`已在017代码中采用各≤64KiB`response.read`前不可退原子fsync预扣（真实body与charged分别计、text和Range合用），016明确`ProxyHandler({})`/默认TLS证书验证/NoRedirect/三固定官方URL，ZIP64/CRC/样本冻结/时钟公式不得放宽。

**前置关键纠错**：要在**任何真实execute前**，先以普通离线环境和带模拟`VLM_ORIGINAL_WORKSPACE`等的**实际相关执行变量上下文**分别运行完整纯合成unittest集；原56方法必须保留、新增至少2个环境/路径身份异常反例，目标两上下文各**≥58全PASS、0FAIL/ERROR/SKIP**，并确认内置`unittest.defaultTestLoader`在这两上下文的集合/结果一致。既有模拟`Path.resolve`与`check_ancestors`的问题只能通过合成fixture修复，不改生产路径/Conda安全约束。前置有任何失败、合成触及私人祖先文件或任务pin不匹配→STOP，**不调用正式`--execute`，0媒体GET**；全部通过才允许**唯一一次**`--execute --parent-task VLM-BATCH-018`，程序内部也必须先验父任务和合成门，之后才准正式本地原metadata SHA/隔离目录/015独立CPU工具与最多一次`-version`，再冻结1越界/1严格合法私有train视频，核官方项目/许可和唯一S3媒体ZIP HEAD/强ETag/206尾部索引/ZIP64/两成员预算。官方S3实际206、成员能否≤64MiB取得和同版PTS均**尚未证实**，Gyan工具ZIP支持206不代表AllenAI视频ZIP可取。

**真实V1试点成败的科学资格**：若全部前置通过，Codex才能在HTTP GET总≤12、所有实际与保守预扣≤64MiB、本地全部私有占用≤128MiB、无重试/无整包/无镜像/禁代理/强ETag/Range206/CRC的前提下取得预选最多2 MP4，并仅用现有CPU ffprobe检查封装duration/start、视频stream timebase/fps和packet PTS/DTS/duration，相比CSV`length`与异常end作**两例**类别化记录。不得公开视频身份/subject/class/精确时长/PTS或视觉人工事件真值。即使2例成功，B原时间边界质量和C P1/P2真实实例仍HOLD，旧19,625 strict不通过≠已核不准，A官方frame标签沿012限域VERIFIED；Charades作为自然长视频独立资源FAIL、原创机制retain0/GPU BLOCKED。

**5处交付和最终止损**：BATCH018严格只交`docs/codex-artifacts/VLM-BATCH-018/`2份脱敏访问及科学报告、`prototypes/charades_range_media_clock_pilot.py`/原synthetic test两项最小变更、`docs/codex-results.md`尾部一条018父结果，正常commit/push后立即停止，由ChatGPT独立核源码/收据并更新看板；用户私有Windows资源不会在公共仓库出现。**018是本条Charades媒体获取路线的最后一次机会：若安全门或服务器/媒体钟仍无法给出可信证据，止损而非默认再开019**。本轮ChatGPT只写GitHub任务/科研管理材料、没有用户Windows访问、没有实际下载任何媒体或工具、没有调用GPU。

### 2026-10-10 · BATCH018双视频实际工程验收，但同钟仍UNKNOWN；关闭Charades媒体获取（最新）

**最终一次真实V1已执行并严格区分“可获取”与“科学同钟”**：[Codex提交2453b88](https://github.com/floomeer83felix-source/vlm/commit/2453b88a732504f3ac2abe9bc2934f59291cc022)恰好五处允许文件——[HTTP/隐私/隔离收据](./codex-artifacts/VLM-BATCH-018/preflight-and-http-resource-receipt.md)、[两例PTS与科学结论](./codex-artifacts/VLM-BATCH-018/two-case-pts-and-research-decision.md)、原媒体协调器及其纯合成unittest、`docs/codex-results.md`尾部一条018父任务。ChatGPT审查GitHub提交差异与函数`classify_clock`、59个test方法，**未在用户Windows独立运行探测，也未打开真实MP4、CSV、私有ledger或精确packet记录**。017历史失败仍保留；018将父任务/合同hash迁至018并追加017历史回报SHA，媒体源及安全/时钟核心逻辑未改，旧13–17父任务不可重跑。

**安全门与访问资格（Codex Windows执行者报告）**：旧56合成方法保留并新增3项，普通`unittest discover`59PASS、普通和合成工作区子进程`loadTestsFromName`各59PASS、唯一真实`--execute`内部双环境各59PASS（均0FAIL/ERROR/SKIP），先于私有资产及网络操作。原metadata ZIP/train/classes固定SHA/Windows物理隔离、独立CPU ffprobe9.0.2的私有执行文件SHA与收据校验PASS。旧原算法先从train CSV私密冻结1条strict越界视频和1条全strict合法匹配对照，再查官方服务器。官网项目页与许可锚固定核过，官方唯一S3 480p ZIP对象HEAD1，强ETag/identity/长度、后续`206 Content-Range`、If-Range、单盘ZIP索引/ZIP64、两个唯一成员local header/CRC及预算核验PASS；总计10个研究GET、**实际HTTP正文1,979,817B、读前fsync保守预留1,979,817B**（应用层响应读取量而非TLS总流量）、总额远低于64MiB，成功在独立MediaPilot保存**2 MP4**，未获取13GB整ZIP、镜像、STA，也没有请求重试。

**工具/私有占用**：`ffprobe -version`一次、两本地MP4的video stream packet探测各一次，共3次独立CPU调用；无像素/音频帧观看/解码、视觉动作重标、模型训练/GPU。独立媒体根仅6个本批私有文件（2 MP4、2 clock元数据报告、私有候选映射、原子ledger），最终逻辑字节和882,420B，最高观测文件名逻辑和1,243,981B；加额外1MiB缓冲保守计算2,292,557B≤128MiB，**精确Windows物理分配峰值未测**。所有GET事件完整、实际/保守计费相同，工具014/015预算/包和历史ledger不改，用户原科研工作区/Conda/CUDA/PATH/原metadata与先前模型均未触碰。真实媒体ID、subject、动作/精确end、容器时长、fps、PTS/DTS、私有视频文件SHA等**只保留本地、未发布GitHub**。

**为何工程成功仍不得宣布时间轴修好**：现有`classify_clock`使用先验保守条件；两个实际视频stream均存在`has_b_frames>0`标志，程序在做同钟比较前就给`CASE_OVERFLOW=CLOCK_UNKNOWN`、`CASE_CONTROL=CLOCK_UNKNOWN`，且未改容差或针对单个B帧重排列作进一步辨识。B帧标志**不等于媒体/CSV一定不同钟、不等于标注错误**；视频packet PTS获取成功也不证明视觉动作起止时刻。既有旧012 `OFFICIAL_FRAME_LABEL=A_VERIFIED_WITHIN_012_SCOPE`仅官方frame评价口径，`B_TIME_RANGE_QUALITY=HOLD`、`C_P1/P2_EVENT_TRUTH=HOLD`，创新`RETAIN0`，Charades缺自然长时域独立外推=FAIL；原19,625条strict`end≤length`不通过不能解释成已核实坏标注，更不能据两病例改动P1/P2原语义真值。`CASE_LIMITED_COMPLETE`仅说明工程流程完成，**`V1_CLOCK=UNKNOWN`是科学结论**。

**按用户“最后一次”授权正式止损**：`BATCH018=ACCEPTED_ENGINEERING / V1_CLOCK_UNKNOWN / FINAL_MEDIA_STOP`，所有原013–018的READY归历史，当前**0 READY**，不启动旧程序重做、不创建自动019/额外Charades媒体GET/其它镜像/V2画面/GPU。MediaPilot两原视频及容器/packet PTS、原私有ledger按协议继续本地隔离保留，既不删除也不发布或搬进旧RTX3090工作区。下一决策`VLM-RESEARCH-POST018-DIRECTION=WAIT_USER_RESEARCH_DIRECTION`仅为科研方向选择；建议先无新增数据下载和模型运行，以官方版权许可/公开同版音视频与annotation时间轴合同/自然长视频分布/学术新颖性和时间ground truth可审计标准，静态对比真正长视频语料及潜在新机制，再由用户另行批准新方向/明确任务。不能将Charades短视频抽样数值或旧候选P1/P2当顶刊论文已经通过证据门。

### 2026-10-10 · 用户同意长视频与原创机制公开静态筛选：BATCH-019当时唯一READY（历史授权）

**为何切换科研重点**：[BATCH018最终两案例报告](./codex-artifacts/VLM-BATCH-018/two-case-pts-and-research-decision.md)执行者报告：最后一次合法Charades媒体GET10、总正文1,979,817B，安全取得2个已冻结官方MP4并CPU采集video packet元数据；但`has_b_frames`触发先验保守规则，两臂均`CLOCK_UNKNOWN`，因此不能认证CSV`length`或动作`end`与媒体时间钟，P1/P2事件语义真值仍HOLD。该来源短视频无法作为真正长视频论文的独立主证据，旧`RETAIN0`未改。此后用户回应“好的”，同意下一步**只对公开网页与论文做静态数据源/机制初筛**，不是批准再取Charades媒体、运行模型或签署新数据许可证。BATCH018的`FINAL_MEDIA_STOP`及两段已获取视频/PTS私有隔离永久保留，不迁移/外传，015独立CPU工具与RTX3090原环境也不使用。

**ChatGPT已完成一轮可复核的静态公开源搜集**：[初筛证据种子](./long-video-static-screening-seed-2026-10-10.md)，来源只含官方数据站、GitHub网页README/公开dataloader、论文公开摘要/HTML。候选最先检查：
- [Ego4D 官方schema](https://ego4d-data.org/docs/data/annotations-schemas/)已显示canonical视频`video_start_pts`与timebase整数、clip/video双时间原点和NLQ annotation字段，**这只是存在可审计映射字段、没有认证任何实际视频同钟**；[官方获取流程](https://ego4d-data.org/docs/start-here/)明文要求先签授权以访问数据**与标注**，Ego4D仓库软件MIT不能充当原视频数据许可。
- [HourVideo](https://github.com/keshik6/HourVideo)有500段Ego4D来源20–120min视频、12,976多选QA，是自然长输入的公开候选，但数据集明确禁止进入训练语料，且与Ego4D不是独立素材来源，其QA答题不等于带起止的物理事件GT。
- [LongVideoBench](https://github.com/longvideobench/LongVideoBench)论文声称最长约1h，官方[loader](https://github.com/longvideobench/LongVideoBench/blob/main/longvideobench/longvideobench_dataset.py)显式`duration`、帧采样时间与`starting_timestamp_for_subtitles`字幕偏移；这些不同时间原点需实证合约，官方CC-BY-NC-SA-4.0声明不自动覆盖所有第三方网页原视频权利。
- [Video-MME](https://github.com/MME-Benchmarks/Video-MME)包括30–60min长split，但官方明确原视频版权归来源权利人、限制再分发和其他用途，QA不是物理时间区间注释；[MLVU](https://github.com/JUNJIE99/MLVU)、[LVBench](https://github.com/zai-org/LVBench)都声明第三方视频版权不归项目自身且可能经过剪裁/重链，需查时间版本、媒体合法性和长时真实分布。3min/题[EgoSchema](https://egoschema.github.io/index.html)最多为短时控制，不能借Ego4D来源伪称小时视频验证。

**强先例导致“经验式故事”无法声称原创**：[VideoTree CVPR2025](https://videotree2024.github.io/)查询自适应粗到细、[ReWind CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/html/Diko_ReWind_Understanding_Long_Videos_with_Instructed_Learnable_Memory_CVPR_2025_paper.html)记忆更新与指导抽帧、[VideoMind ICLR2026](https://videomind.github.io/)planner-grounder-verifier-answerer、[Seeing Is Believing: EV²-Bench / DynamicSelect AAAI2026](https://ojs.aaai.org/index.php/AAAI/article/view/38031)时空证据评估与动态压缩均已有论文。可考虑的`H1`时钟不确定性可控风险/弃答、`H2`重复事件实例身份证据与反事实顺序、`H3`预算约束下的校准证据充分性**都只是可证伪假说**，必须对照最强近邻和独立视觉/时序GT；不能把普通时钟换算、加时间戳、分层记忆或证据输出当科学原创。`NOVELTY=RETAIN0`直到有新实验与先例扣除的证据。

**新增唯一READY父任务**：[VLM-BATCH-019八项纯公开静态审查合同](./codex-artifacts/VLM-BATCH-019/README.md)。Codex须在用户同一个长期聊天内主动触发，安全只更新公有docs Git，核唯一019 READY且无旧019回报；各查六个数据来源的代码vs标注vs原视频版权、输入自然长时分组、canonical video/clip/packet PTS及字幕时间偏移对应关系、真实事件区间GT的存在与否，至少六项论文强先例与两三个可否证机制假说、未来合法媒体/标签与GPU前置门。**绝不下载数据集媒体/标注/字幕/QA/论文PDF文件、运行ffprobe/软件、注册Ego4D、访问旧Windows私有Charades素材或科研环境、安装模型或使用GPU**。仅交`docs/codex-artifacts/VLM-BATCH-019/`四份Markdown报告及`docs/codex-results.md`尾部一条共5文件，0代码文件修改。安全push后STOP，ChatGPT审查后才可能向用户请求一个独立新研究方向/新授权。`SCREEN_PRIORITY`不等于`DOWNLOAD_GO`或`NOVELTY_GO`，缺官方许可/媒体PTS时写UNKNOWN/RESTRICTED，严禁承诺已解决Charades旧边界异常。

### 2026-10-10 · BATCH019静态报告验收，数据及原创性准入仍HOLD（最新）

**文档范围审计**：[24b771e](https://github.com/floomeer83felix-source/vlm/commit/24b771ef9c83e929579372a982ea17cd6edbbdb8)相对3d784c2只新增四份`docs/codex-artifacts/VLM-BATCH-019/` Markdown并在`docs/codex-results.md`末尾新增23行，共5处，无源码、计划/总览或旧报告修改。ChatGPT读完[许可/长域矩阵](./codex-artifacts/VLM-BATCH-019/official-dataset-license-duration-matrix.md)、[时间基/GT合同](./codex-artifacts/VLM-BATCH-019/timebase-provenance-and-groundtruth-contracts.md)、[创新先例/反例](./codex-artifacts/VLM-BATCH-019/prior-art-and-falsifiable-mechanisms.md)、[论文退出门](./codex-artifacts/VLM-BATCH-019/paper-feasibility-and-exit-gates.md)，审查八任务结构、六候选与六必查+五新增先例，抽查Ego4D官方schema/NLQ长度、LVB v1 HTML和2026 COVER/GEB/interval confidence原始摘要。仅接受有界静态交付及当前UNKNOWN/HOLD口径；未复验执行者的Windows、网络日志，也未下载数据、运行模型/GPU。

**证据与风险**：Ego4D`video_start_pts`/timebase及video/clip坐标可作为未来合法版本映射的纸面合同，不构成文件级MEDIA_CLOCK_PASS；NLQ clip平均约10min、最长20min，不能充当小时评测GT。HourVideo500段20–120min来自Ego4D，不是独立来源，且benchmark数据严禁进入训练。LongVideoBench v1 Table3六格数量相加3,761、摘要写3,763，保留源内冲突及当前发布版本UNKNOWN，不把引用frame index自动提升为必要/充分事件GT。Video-MME、MLVU、LVBench媒体版权/剪裁版本/事件实例标签链仍未闭合；Code LICENSE不授权原视频。H1时钟不确定联合风险与H3证据校准仅存待否证研究问题，COVER/Explicit Abstention/Grounding with Confidence/EV²-Bench等近邻强；H2普通物理对象身份记忆与GEB先例直接重合，当前NO_GO_AS_NOVEL_CORE。现有论文还缺**新算子、独立真值、合法源、相同输入和预算的强基线与实际效应**，所以`NOVELTY=RETAIN0`，不承诺期刊可发表性。

**裁决与权限**：`BATCH019=ACCEPTED_STATIC_DELIVERABLES`、`LONG_DURATION=STATIC_EVIDENCE_PARTIAL`、`LEGAL_MEDIA=HOLD`、`TIMEBASE=UNKNOWN`、`EVENT_GROUND_TRUTH=HOLD`、`PRIOR_ART=NOVELTY_RETAIN0`、`DEVICE_COST=UNKNOWN`。`SCREEN_ONLY_PRIO1`优先Ego4D↔HourVideo合法同版桥接和H1强反例，但不等于新执行授权。BATCH018的两病例`CLOCK_UNKNOWN`/Charades`FINAL_MEDIA_STOP`、旧B/C HOLD全部延续。`DOWNLOAD_APPROVED=NO`，0新READY，GPU/训练/ffprobe/模型和新标注、数据合同签署均BLOCKED。下一个科研动作标记`WAIT_USER_POST019_DECISION`（非READY）；用户决定继续仅公开资料定向填缺口或停止当前路线后，ChatGPT才可另行定义独立有界父任务。Codex同一长期聊天不自行启动020或唤醒执行。

### 2026-10-10 · 用户明确选择下一科研边界：BATCH020仅公开H1红队与Ego4D/HourVideo许可同版审查（最新）

**方向决策**：用户在BATCH019四份公开报告验收后回复“按你的建议”，按ChatGPT提出的低风险优先级，进一步核**H1是否在COVER/普通区间并集/正确时钟换算/置信弃答基线之外有可证伪的新操作**，以及**Ego4D和HourVideo同源原媒体/标注的法律许可与canonical→HourVideo实际版本映射是否公开可追溯**。不扩大为H2/H3新算法开发、Charades补救或媒体/模型实验。现有[COVER arXiv 2608.07434](https://arxiv.org/abs/2608.07434)已覆盖有条件的temporal coverage，不能把联合分数或名义风险保证无独立标签即称原创；[Ego4D官方start here](https://ego4d-data.org/docs/start-here/)要求协议访问原数据与标注，[HourVideo README](https://github.com/keshik6/HourVideo)明禁benchmark数据加入训练集，两者不能被各自软件许可豁免。两数据集来源同源，不能假装独立外测；标准化/裁剪公开字段也不认证单文件PTS与QA标签同钟。

**任务与硬停止**：[VLM-BATCH-020完整八项任务书](./codex-artifacts/VLM-BATCH-020/README.md)为唯一READY，Codex只能在同一个长期聊天收到用户新一轮主动消息、确认唯一READY且此前无020父回报后执行：公开网页官方许可/版本审计、H1核心算子与最强零假说形式反证、两个不可区分世界、最多一个真正残余问题（若存在），最后独立纸面LEGAL/TIMEBASE/GT/NOVELTY/COST五门。全程禁止任何视频/字幕/QA/标注JSON或论文PDF文件下载、账户注册/签署数据协议/联系作者、ffprobe/代码/模型/GPU/原私有实验资产。只上传`docs/codex-artifacts/VLM-BATCH-020/`三份Markdown和`docs/codex-results.md`尾部一条共4处，不能改ChatGPT任务/总览/旧报告。正常push即STOP，不自动021。现有`NOVELTY=RETAIN0`、`LEGAL_MEDIA=HOLD`、`TIMEBASE=UNKNOWN`、`EVENT_GT=HOLD`、`DEVICE_COST=UNKNOWN`、`GPU=BLOCKED`与Charades`FINAL_MEDIA_STOP`持续有效。静态否证若让H1 NO_GO，就应退出H1，而非擅自改为新实验。

## 6. 下一次 ChatGPT 审查的检查顺序

1. 读 [Codex执行结果](./codex-results.md) 最后新增记录及对应提交；
2. 与 [任务书](./next-steps.md) 的任务ID/验收标准逐项核对；记录完成、未证实、偏差；
3. 必要时只看脱敏产物或 PR 差异；对无原始证据的主张标注“仅执行者报告”；
4. 形成明确 **ACCEPT / REVISE / HOLD** 与下一步科学依据；
5. 仅由 ChatGPT 更新任务书与本总览，不删除之前负结果或重写原始快照。

**提醒：** 此仓库中的总结不是原始实验数据仓库；报告中所有新准确率和创新结论必须有可审计的新来源及运行账本支撑。
