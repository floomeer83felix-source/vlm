# Codex 执行结果回报（Codex 维护）

> **唯一用途：** 接收 Codex 执行 `docs/next-steps.md` 中唯一 READY **任务或任务包**后的脱敏事实记录。任务包可连续完成多个已授权的低风险子任务，使用**一个父任务ID、一条汇总回报**；这里是执行者报告，**不是ChatGPT已核实的科学结论**。
>
> 执行任务请先读：[next-steps.md](./next-steps.md)；所需脱敏附件上传 [codex-artifacts/](./codex-artifacts/) 的对应任务子目录；审查后的全局状态见：[research-overview.md](./research-overview.md)。

## 提交流程

1. 每次只执行一个明确标记 READY 的**父任务**。父任务若为任务包，允许按其README顺序连续完成内部子任务，但不得越过任务包边界。**VLM-001、VLM-002均已回报；当前任务是VLM-BATCH-003，原VLM-PTS-001并入其中不单独回报。**
2. 结束时先把任务README允许的小型脱敏文本证据上传到 `docs/codex-artifacts/<父任务ID>/`，再向本文件**追加一条父任务结果**，逐项描述子任务A/B/C的实际完成情况及链接；旧记录只追加更正，不覆盖、不删除。
3. 在公开 GitHub `main` **仅提交本文件和当前任务包README允许的脱敏附件**。本次VLM-BATCH-003只可新增 `docs/codex-artifacts/VLM-BATCH-003/` 下的3个指定Markdown报告、向本文件追加1条父任务记录，建议提交信息 `codex: report VLM-BATCH-003 three-part audit`。
4. 提交前检查 `git diff --cached --name-only` 及拟上传的文件正文，确保没有视频、数据、模型、权重、原始答案、凭据、绝对隐私路径、账本原文。具体规则见 [上传目录说明](./codex-artifacts/README.md)。
5. 若无法访问 GitHub、遇到同文件冲突或没有安全的提交方式，保留本地报告并向用户反馈，**不要 force push、不要自行合并覆盖**。
6. 提交后停止任务；由 ChatGPT 读这个文件，形成审查意见并更新研究规划。

## 回报模板（每项任务复制一次填写）

### [任务 ID] [YYYY-MM-DD HH:MM 北京时间] — [完成 / 部分完成 / 阻塞 / 失败]

- **本次范围**：执行了什么；哪些明确没有执行。
- **执行环境**：Windows 版本、GPU/显存概况、原工作区 Git commit（存在时）、conda/Python/Torch/CUDA/驱动版本（仅已确认项）。
- **事实与证据**：
  - 代码、运行脚本、现有模型/数据：存在 / 缺失 / 未检查，依据是什么；
  - 运行中进程、文件锁与持有者：存在 / 无 / 未确认；
  - 持久调用账本：最近 run ID、started 未终态数量、异常状态；找不到记“未确认”，不可猜测；
  - 其他异常或科学数据/身份风险。
- **资源与修改**：新增 QA 前向 = 0 或实数；下载 = 0 或实数；修改本地研究资产 = 无/列明。首次 VLM-001 应全部为零/无。
- **限制与未知**：本次不能验证什么；是否有敏感信息因此未公开。
- **Codex 建议**：下一任务是否适合解封：建议 GO / HOLD；附理由（**最终决策权在 ChatGPT/用户**）。
- **附件与追溯**：按父任务ID链接 `docs/codex-artifacts/<父任务ID>/` 的小型脱敏报告。若为任务包，分别列子任务A/B/C的附件、实际执行情况与UNKNOWN/BLOCKED；安全情况下可列相对路径/文件SHA256；GitHub提交SHA由历史自动提供，不需预填。

> 建议正文控制在300—600字，具体数据可用小表。严禁用没有读到的资料推断“无运行”“安全”“已完成”，更不能将技术核查写作科学实验通过。

---

## 已回报任务

**历史记录见下方：VLM-001、VLM-002已提交。当前等待VLM-BATCH-003的三项汇总回报。**

<!-- Codex: 在本标记后追加每次任务记录，不删除旧内容；也请保留上方模板供下轮使用。 -->

### VLM-001 2026-10-08 20:29 北京时间 — 完成

- **范围与环境**：仅审计Windows本地工作区。Windows 11专业版build 26200，RTX3090 24GiB，驱动610.47；conda24.11.3，既有pytorch环境Python3.9.21／Torch2.5.1、构建CUDA12.4、Transformers4.57.6。证据为CIM、nvidia-smi、安装元数据及静态版本文件，未测GPU运算。研究目录无Git，文档checkout基线为 `7a9751b9b952c597fe5b3f6f74cfe20f1c8baaed`。
- **事实**：本地源码、入口、三模型权重／配置、视频索引与账本存在；最新manifest的11项代码SHA匹配。4份问答账本分别有80／60／72／120个唯一开始与终态，started未终态均0，未重算科学结果。最新问答run为 `gap_directed_defusion_fresh20`，计划80行、complete；随后参考数据元数据run终态HOLD。
- **进程与未知**：6条Python未匹配研究目录或主要入口；GPU仍有桌面应用及权限不足条目，不能声称整机空闲。4个已查锁文件存在，未申请或改动锁，持有状态UNKNOWN。450份历史指纹覆盖缺项、VFR／真实PTS桥接、全量权重与视频哈希未确认。
- **资源与建议**：新增模型／GPU前向／数据集下载0，原研究资产修改0；仅文档checkout产生交付物。建议ChatGPT审核后仅对VLM-002元数据核查GO，推理／下载／后续BLOCKED任务HOLD，不自行放行。
- **附件与追溯**：[workspace-audit.md](codex-artifacts/VLM-001/workspace-audit.md)含证据类型、局限及安全相对路径／SHA。只提交本摘要和附件，提交成功即停止。

### VLM-002 2026-10-08 北京时间 — 完成（G1 HOLD）

- **范围**：依据 `19a4e42` 的READY任务，仅查TRACE/VES-Bench、HERBench，前两者关键信息不足后简查CaST-Bench。读取官方页面、README、许可、版本／文件目录与Viewer info字段，不读实际标注行或答案。
- **事实**：VES公开revision与348个视频路径可确认，联合必要区间是官方声明；Viewer仅给video列，注释／视频许可及真实问答区间字段UNKNOWN。HER列schema和非商业CC BY-NC-SA许可可确认，但视频沿上游条款；MRFS依赖模型／selector，详细字典404。CaST的test元数据80题、目录56个MP4；字典给`mm:ss`区间与逐秒框，注释CC BY4.0、视频另适用SAV条款。版本、来源与官方链接详见附件。
- **限制与资源**：均未实证三段必要／非重叠、<12锚点、区间外池、真实PTS或≥40独立来源。23个受控直接响应共214936B、最大42968B；初始检索工具流量未独立计量，不填0。3项404保留，未扩大访问链。新增模型前向／视频／完整标注下载0，原工作区与环境修改0。
- **建议与附件**：所有候选G1仍HOLD；优先澄清VES许可和无答案区间字典，是否继续由ChatGPT审查。[dataset-metadata-review.md](codex-artifacts/VLM-002/dataset-metadata-review.md)为唯一附件。仅提交这两处，完成即停止，VLM-003／004不执行。

### VLM-BATCH-003 2026-10-08 22:25 北京时间 — 完成

- **范围**：按main `17a88e2` 最新AGENTS与任务包连续完成A/B/C。复用上轮未提交的PTS审计；只读必要源码、聚合字段及已验收报告，PR #1仅参考固定head `df892ee7` 草案，未合并。
- **A 完成／运行UNKNOWN**：[时间戳合同](codex-artifacts/VLM-BATCH-003/timestamp-contract-audit.md)。最近runner仍index/FPS；历史PyAV路径与纯PTS模块存在，但不构成当前12帧／裁剪版本桥接。列明时钟字段、融合平均标签风险及未来测试设计，本轮不执行。
- **B 完成／独立性HOLD**：[来源审计](codex-artifacts/VLM-BATCH-003/source-provenance-audit.md)。789历史节点、339可用摘要、450未提供摘要；缺项不是污染数或独立事件数，具体split原因分布UNKNOWN。30 prepared、20 selected是已有操作性统计，不能承诺40独立来源。给出保守组件、跨split污染和toy验收合同。
- **C 完成／G1 HOLD**：[G1合同](codex-artifacts/VLM-BATCH-003/g1-feasibility-contract.md)。三候选许可／支持／同版PTS等缺口保留；列出无答案投影字段、D1/D2的12唯一帧不变量与最多3项澄清建议，没有新manifest、可行题数或创新结论。
- **资源与停止**：新增数据集检索／研究数据下载／模型QA／视频解码／测试运行0，原代码／环境／锁／账本修改0；只同步文档和参考PR。仅提交3附件＋本摘要，完成即停，不执行VLM-003／004，等待ChatGPT整包审查。

### VLM-BATCH-004 2026-10-08 22:41 北京时间 — 完成（toy通过；G1 HOLD）

- **A 完成／未发送**：[VES请求草案](codex-artifacts/VLM-BATCH-004/ves-access-request.md)中英双语，分开询问注释／视频许可、无答案区间字典及媒体／源组时钟资料。联系地址UNKNOWN，未猜邮箱、发送邮件或Issue。
- **B 完成／实际CPU测试**：[toy合同](../prototypes/toy_g1_contract.py)与[unittest](../prototypes/test_toy_g1_contract.py)仅标准库和虚构输入，无研究源码imports。既有Python3.9.21执行10项：首次9过1失败，用例同时改锚点而先报身份错，预期为预处理错；仅修正新toy用例并补输入校验后，第二轮10过0失败0跳过。两轮框架均报告0.005秒，不含启动。无真实token仍TOKEN_BUDGET_UNKNOWN，时间匹配资料缺失明确标记。
- **C 完成／不放行**：[G1去留与测试报告](codex-artifacts/VLM-BATCH-004/g1-decision-and-toy-test.md)给出许可→必要支持→真实PTS版本→至少40保守源→12帧／混杂→再授权条件树。toy不认证实际数据、来源、语义充分性或新算法；无法取得合法支持时交ChatGPT调整问题。
- **资源与停止**：两轮toy CPU单测；模型／GPU／QA／视频解码／研究数据下载／原资产及环境修改0，外部联系0。仅提交两报告、两代码和本摘要，完成即停，VLM-003／004继续BLOCKED。

### VLM-BATCH-005 2026-10-09 08:28 北京时间 — 完成（18项toy通过；G1 HOLD）

- **A 完成／未联系**：[官方渠道](codex-artifacts/VLM-BATCH-005/official-access-route.md)。6项官方页面／版本接口共50299B，全200，定位项目→仓库／HF入口，仓库has_issues=true；许可、专用申请及实际区间字段仍UNKNOWN，没有猜邮箱或发送消息，旧请求草案未改。
- **B 完成／CPU实测**：仅修改[标准库toy](../prototypes/toy_g1_contract.py)与[测试](../prototypes/test_toy_g1_contract.py)。保留原10方法、增8负例，强制≥3有序非重叠区间，拒无效端点；粗bin相同细时间不同明确UNKNOWN，真实token仍UNKNOWN，保护组件不被缺证据洗白。Python3.9.21本轮1次18过、0失败／error／跳过，suite0.010秒，不含启动。
- **C 完成／待选择**：[路线裁决](codex-artifacts/VLM-BATCH-005/research-path-decision.md)。路线1仅在许可、无答案必要支持、同版PTS和≥40保守源等证明成立后再申请G1；否则建议停止gold覆盖前提，另审无参考区间真值鲁棒性问题，列时间、画质、token与检索四类替代解释。用户需决定是否咨询或调整命题，没有新科学结果。
- **资源与停止**：0模型／GPU／QA、0视频解码／媒体下载、0外部联系、0原研究资产及环境修改。只提交本轮5处；完成后停止，不再默认静态调查，VLM-003／004仍BLOCKED。

### VLM-BATCH-006 2026-10-09 09:22 北京时间 — 完成（证据缺口保留；NO_GO_OR_PIVOT）

基线main328f450，重新读取最新版十项README；路线2不再用gold必要区间构造输入。四份报告链接：[新颖性与识别性](codex-artifacts/VLM-BATCH-006/novelty-and-identifiability.md)、[静态门](codex-artifacts/VLM-BATCH-006/static-readiness-gates.md)、[预注册与toy](codex-artifacts/VLM-BATCH-006/prereg-and-toy-tests.md)、[综合裁决](codex-artifacts/VLM-BATCH-006/scientific-decision.md)。

| 任务 | 状态与事实 |
|---|---|
| 1 | UNKNOWN：核查5直接先例，4个预印本方法／消融HTML；RL正式全文、MIF最终版细节未取得，不推为新空白 |
| 2 | DONE：普通S_q/S_t等已有直接重合；S_shuf和措辞路径因子独特性仍UNKNOWN |
| 3 | DONE：列10项强反解释与未来控制，仅策略总体效应，不作注意力因果宣称 |
| 4 | DONE：静态追踪现question→SigLIP→旧MMR12→IMAGE/Qwen；query与prompt共用字段，无新执行 |
| 5 | UNKNOWN：新QA／媒体许可与目标版隔离未确认，旧终态scorer代码存在不代表新数据通过 |
| 6 | UNKNOWN：真实PTS／clip／来源门缺实证；450缺项不是污染数，不重哈希或复用封存 |
| 7 | UNKNOWN：真实token、时间漂移、selector／wall成本未实测，12帧不保证等算力 |
| 8 | DONE：来源组等权Δ及全失败分母、缺臂边界、检验条件和功效UNKNOWN参数明确 |
| 9 | DONE：新[标准库toy](../prototypes/toy_route2_pairing.py)和[unittest](../prototypes/test_toy_route2_pairing.py)；Python3.9.21本轮1次11 PASS、0 FAIL/ERROR/SKIP，suite0.001秒，原toy未改 |
| 10 | DONE：NG0普通新方法FAIL、窄设计UNKNOWN；NG1/NG3 UNKNOWN，NG2现接口不满足及新证据UNKNOWN；结论NO_GO_OR_PIVOT |

直接取得9个官方HTML响应共2129480B，未超12页；论文编号定位另用少量检索工具，方法结论只据官方实读资料。0 PDF／媒体／完整标注下载、0模型／GPU／QA／真实评分、0视频解码、0原研究资产／环境／锁／账本修改、0外部联系／PR合并。仅提交4报告＋2新toy＋本条回报共7处，完成即停，VLM-003／004继续BLOCKED。

### VLM-BATCH-007 2026-10-09 10:24 北京时间 — 完成（RETAIN 0／STOP THIS PORTFOLIO）

基线main3cbe50c，按最新版十项README研究M1／M2／M3；原选帧路线仅用公开历史摘要，不读原评分或重跑。五份报告：[先例与已否决路线](codex-artifacts/VLM-BATCH-007/prior-art-and-rejected-directions.md)、[候选机制规范](codex-artifacts/VLM-BATCH-007/candidate-mechanism-specs.md)、[形式边界与toy](codex-artifacts/VLM-BATCH-007/formal-limits-and-toy-results.md)、[可行性与强基线](codex-artifacts/VLM-BATCH-007/feasibility-and-baselines.md)、[最终否决](codex-artifacts/VLM-BATCH-007/downselect-and-stop-decision.md)。

| 任务 | 状态与事实 |
|---|---|
| 1 | DONE：旧负结果与不可重投边界、至少5种换名否决；不把历史探索当确认 |
| 2 | DONE／UNKNOWN：10个不同官方URL尝试，9个HTTP200；NeuS SSL失败；MIT定位实际为视觉论文，TMS方法UNKNOWN，不由缺全文宣称创新空白 |
| 3 | DONE／NO-GO：M1三值一致世界合同；未覆盖且无可信正事件必须UNKNOWN，现实感知不满足toy oracle |
| 4 | DONE／NO-GO：M2版本／源／证据依赖与撤销合同；普通完整依赖cache可模拟最小算子，OR／循环／冲突不由AND toy认证 |
| 5 | DONE／NO-GO：M3允许观察到一致假设的映射；无gold筛选，强判别clue／版本空间规划可模拟，正式先例不足仍UNKNOWN |
| 6 | DONE：同观测不同never的双世界、恒UNKNOWN零coverage、缓存等价及不可区分合法动作反例 |
| 7 | DONE：新[标准库原型](../prototypes/toy_mechanism_counterexamples.py)与[测试](../prototypes/test_toy_mechanism_counterexamples.py)，共194行；Python3.9.21本轮1次12 PASS、0 FAIL／ERROR／SKIP，suite0.007秒，不含启动 |
| 8 | DONE／UNKNOWN：三类独立真值、许可／隔离／PTS版本／来源／视觉验证器／资源门；必须新人工标签时当前授权NOT FEASIBLE，不取得实际标签 |
| 9 | DONE：同计算对象、同输入／成本的三值监控／TMS/cache／判别clue强基线；全planned失败分母、source聚类和功效未知参数，不承诺真实QA次数 |
| 10 | DONE／RETAIN 0：六门分别判定；未形成充分创新或现实GO。任务交付是否ACCEPT由ChatGPT审查；停止本候选组合，不擅自生成下一READY任务 |

toy枚举117种观测模板、336个一致世界—观测配对；理想三值规则错误TRUE／FALSE均0，故意unknown→0产生89个假never认证配对。不是视频结果或新算法优势。新颖性审查使用用户指定GPT-6.1-sol ultra子任务。

文献访问10个URL尝试／9响应，响应正文总3405089B；仅公开HTML，部分是摘要证据。1项SSL失败不绕过证书／重试，错误TMS定位不换页；URL及证据级别见先例报告。0 PDF／媒体／模型／完整QA下载、0 GPU／模型／训练／QA／真实评分、0视频解码／导帧、0原研究目录／环境／进程／锁／账本修改、0旧实验重跑／新人工标注／外部联系／付费API／PR合并／自动化。仅提交指定8处，成功push后停止本轮，保留当前聊天框。

### VLM-BATCH-008 2026-10-09 12:07 北京时间 — 完成（文档初筛；机制RETAIN 0／长视频GO HOLD）

基线main eb2c53f；安全fast-forward后重新读取唯一READY任务、AGENTS、结果、最新README及指定历史摘要。只审公开网页和脱敏历史，不取得任何研究数据。五份报告：[许可与出处](codex-artifacts/VLM-BATCH-008/licenses-and-provenance.md)、[标注与join](codex-artifacts/VLM-BATCH-008/annotation-and-join-contract.md)、[可证伪问题与先例](codex-artifacts/VLM-BATCH-008/falsifiable-questions-and-novelty.md)、[时钟／来源与长域差距](codex-artifacts/VLM-BATCH-008/temporal-provenance-and-longvideo-gap.md)、[五门裁决](codex-artifacts/VLM-BATCH-008/data-science-go-no-go.md)。

| 任务 | 状态与确证／限制 |
|---|---|
| 1 | DONE：官方非商业研究／评估用途初筛；禁止公开改造数据及第三方分发，必要学术短例有条件允许；主体与具体披露匹配仍UNKNOWN |
| 2 | DONE／UNKNOWN：TALL公开格式与anno cleaning声明可见，独立代码／STA注释许可及外链clean revision未知；Charades-Ego许可正文与原许可相同，不更宽松 |
| 3 | DONE：官方README直接给id/subject/scene/actions/length等；真实行与端点政策未知；v1定位是25时刻frame-mAP，不是实例det-mAP |
| 4 | DONE／UNKNOWN：固定类区间与sentence moment语义分开，ID／split／媒体revision／时间映射合同明确；实际join未验，不造ordinal或negative真值 |
| 5 | DONE／UNKNOWN：P1同类分离实例资格、wrong-instance与完整分母合同；66,500总区间不能推重复资格，数量／完整物理实例序列未知 |
| 6 | DONE／UNKNOWN：P2异类重叠、tIoU／边界／归因、强TAD/TMR、纠错／误伤和泄漏防线；真实资格与模型现象未测 |
| 7 | DONE／NO-GO：六论文页（5正式摘要＋1方法预印本）核直接对象；普通TAL/TMR、多moment／边界核验不是新机制，窄错误测量价值UNKNOWN |
| 8 | DONE／UNKNOWN：subject字段不证明participant-by-split隔离，267用户不等于独立N；无媒体则PTS、clip/version和来源门不能通过 |
| 9 | DONE／NO-GO（单独长域确认）：官方论文平均约30秒，只能短域PoC；拼接不作自然长视频独立确认，合法长域真值／资源仍UNKNOWN |
| 10 | DONE：LEGAL/SCHEMA仅原Charades文档条件PASS，IDENTIFIABILITY未知、普通新算法NOVELTY FAIL、Charades单独LONGVIDEO FAIL；机制retain0，最终GO HOLD |

仅暂列P1／P2两项未验证测量问题，各需一次固定revision的资格计数作为新增事实，不是已证实创新。下一步只建议由用户／ChatGPT另审原Charades约3MB官方注释评测包的最小授权、独立保管和脱敏计数；此批未下载、不创建数据目录，不自动放行STA、13GB媒体、GPU或下一包。

资源：12个不同直接官方网页／论文HTML均200，正文响应794823B；另一次3query定位检索，搜索工具网络流量未计量，不把正文字节当全部流量。未打开PDF／Drive／zip／视频／标注或特征文件；0真实模型／GPU／QA／训练／评分、0视频解码、0原研究代码／环境／锁／账本修改、0历史实验／toy重跑、0私有身份或答案读取、0外部联系／Issue／新标注／付费API／PR合并／自动化。仅提交指定5报告及本条追加共6处，成功push后停止，保留当前聊天。

### VLM-BATCH-009 2026-10-09 14:46 北京时间 — BLOCKED_STORAGE_REALPATH_MISMATCH／NO_DOWNLOAD

基线main71a24ab，安全同步并重新读取最新唯一READY任务及冻结协议，确认无本批先前记录。用户已批准非商业研究的官方单包元数据分析；**硬路径复核失败即停止，不放宽检查或改变目录**。报告：[下载前置与schema阻塞](codex-artifacts/VLM-BATCH-009/download-integrity-and-schema.md)、[资格与科学停止决定](codex-artifacts/VLM-BATCH-009/qualification-and-science-decision.md)。

| 任务 | 本轮状态／实际事实 |
|---|---|
| 1 | DONE：官网license与BATCH-008正文逐字节一致；确认仅原官方小包、非商业、隔离统计和禁止分发 |
| 2 | BLOCKED：固定变量路径的PowerShell父子隔离／reparse／4个已知云根／空间≥150MiB和新目录写测试先PASS，下载前Python absolute/resolve一致性复核报STORAGE_REALPATH_MISMATCH；最终不通过 |
| 3 | HEAD_ONLY／NO_DOWNLOAD：唯一官方HTTPS S3锚点，HEAD200/application-zip、3519822B，ETag/Last-Modified已记录；**数据GET0、成功0、重试0、落盘正文0B**，archive SHA／实际ZIP大小UNKNOWN |
| 4 | UNKNOWN／未开始：无ZIP，签名／CRC／中央目录不能验收；新工具只做合成安全逻辑测试 |
| 5 | UNKNOWN／未开始：未解压、未取得真实CSV/header/encoding/class table，不执行包内代码 |
| 6 | UNKNOWN／未开始：真实行、非法区间／ID／缺字段／重复分母未统计，不能填0异常 |
| 7 | UNKNOWN／未开始：P1所有实际候选数和分母未知，无ordinal/negative问题生成 |
| 8 | UNKNOWN／未开始：P2所有实际pair/group/video总数未知，无模型／因果／边界结果 |
| 9 | UNKNOWN／未开始：真实subject交集、时长与source/PTS/clip版本均未取得新证据 |
| 10 | DONE（停止裁决）：STOP_OR_UNKNOWN、DATA_SCHEMA未验证、候选统计UNKNOWN；长域单独确认继续FAIL，机制retain0，不安排下一下载／GPU任务 |

新[通用标准库工具](../prototypes/charades_metadata_audit.py)及[合成测试](../prototypes/test_charades_metadata_audit.py)没有真实行、身份或私人路径。Python3.9.21两轮suite：首次13方法中12通过、1个反斜杠成员子断言失败（Windows ZipInfo规范化掩盖原始名）；补原始成员名／NUL／特殊字符／文件父路径冲突检查且保留断言，第二轮13 PASS、0 FAIL/ERROR/SKIP。两轮suite各0.002秒，不含启动；发生在数据获取之前，不代表真实ZIP／CSV通过。未运行实际CSV审计CLI。

实际网络仅当前官网／license／README三项文本及数据HEAD，无数据正文请求。隔离目录仅最小准备与来源HEAD元数据，无.part／ZIP／CSV；路径失败后不作进一步诊断、不修改目录或比较规则。0视频／STA／Ego／模型／特征下载、0真实模型／GPU／QA／评分／解码、0原研究资产／环境／锁／账本变更、0私人答案／来源映射读取、0外部联系／新标注／PR合并／历史重跑／自动化。仅提交规定5处并停止；后续应由用户／ChatGPT另审只读路径诊断，不重做本已回报父任务，保留同一聊天。

### VLM-BATCH-009-FIX 2026-10-09 15:00 北京时间 — 用户直接授权的路径检查修复完成

依据用户本轮“修复”，仅诊断并修复上条阻塞，不重新执行已回报的BATCH-009或新增数据请求。安全同步main仍为bc16e38；任务书的旧READY状态未覆盖已存在的父结果，计划与原阻塞历史未改。

**根因与证据**：Windows对固定任务根返回另一规范名称，Path.absolute与Path.resolve词法不同，但os.path.samefile为真，device/inode一致且inode非零；规范名称再次resolve稳定，实际目录仍位于解析后的LOCALAPPDATA内。逻辑／规范两条祖先链均无symlink／reparse；原目录与父目录身份不同，不依赖全零文件ID误判。旧检查把名称不相等直接等同存储风险，造成保守误报；本轮确认的是命名差异，不猜具体账户／别名形式，也不披露私人路径。

**修改**：[工具](../prototypes/charades_metadata_audit.py)改为双祖先链检查、现有锚点的samefile及device/inode双核验、规范名称稳定性和缺失叶的后缀一致性。保留固定变量路径、reparse拒绝、身份未知／不同拒绝，不跳过检查、不换目录。后续新建.part仍必须经现有父目录身份核验；ZIP／下载／CSV规则均未修改。

**验证**：[合成测试](../prototypes/test_charades_metadata_audit.py)保留原13方法，增8项：现存／缺失叶、不同行名同文件身份、异身份／缺失拒绝、samefile失败、两条链重解析点拒绝、全零identity拒绝、canonical不稳定拒绝。本轮1次21 PASS，0 FAIL/ERROR/SKIP，suite0.033秒，不含启动。另对固定任务根与尚未创建的.part路径作一次只读复核：路径门PASS、LOCALAPPDATA规范包含PASS、已知研究／文档根与4个登记云根不重合；没有创建或写入隔离数据文件。

**边界**：本轮数据GET／下载／CSV解析／真实资格统计均0，没有更新本地来源manifest或修改存储落点；合成测试只用虚构临时对象。0GPU／模型／视频／STA／真实解码／原研究资产或环境修改。修复了这一个路径检查阻塞，不意味着整个数据／ZIP／schema／科学门已通过。仅提交两代码和本条追加共3处；成功push后停止，保留原聊天，后续元数据执行需明确新安排，不自动重跑BATCH-009。

### VLM-BATCH-010 2026-10-09 15:43 北京时间 — 受限获取与统计完成；HOLD_RANGE_CONFLICT

基线mainabe39e1，重新读取唯一READY任务与冻结协议；009／009-FIX不重跑、不改写。仅提交[下载与schema](codex-artifacts/VLM-BATCH-010/download-and-schema.md)、[资格与决定](codex-artifacts/VLM-BATCH-010/qualification-and-decision.md)及本条，共3处；既有审计源码未改动。

| 步骤 | 状态与实际证据 |
|---|---|
| 1 | DONE：用户原单包／非商业授权仍适用；旧incoming/extracted为空、旧GET0 manifest已核并保留 |
| 2 | DONE：固定变量路径身份／双链无reparse／stable canonical、研究与docs及4登记云根隔离、空间≥150MiB和新空写探针通过，未更换位置 |
| 3 | DONE：重新读取官网/license/README，唯一官方HTTPS S3锚点及本轮HEAD200/ZIP/3519822B，许可一致 |
| 4 | DONE：实际1尝试／1成功GET／0重试，收到并落盘3519822B，8MiB流式硬限；SHA256 c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866；official_sha256 UNKNOWN |
| 5 | DONE：14 ZIP成员、9591127B声明解压、CRC及路径/类型/预算检查PASS；仅8白名单提取，另外6不提取／执行，包内license与官网一致 |
| 6 | DONE／QUALITY HOLD：真实11列、157类、7985/1863行；原动作49809/16691，数值有效35211/11664，无效14598/5027，含异常行5896/1537，完整分母保留，主因end>length；未修正或缩放 |
| 7 | DONE／语义UNKNOWN：P1 gap>0组252/95，>0.5组227/86，>1组206/82，涉及视频215/77；混合歧义52/24，非物理实例／ordinal真值证书 |
| 8 | DONE／语义UNKNOWN：P2 overlap pair66089/31634，strong49454/24059；有效异类pair分母96802/45696；不是模型错误或关系真值 |
| 9 | DONE／来源PTS UNKNOWN：subject214/53、union267、cross-split交集0，video ID交集0；粗length合并桶<30秒3837、30—<60秒5943、60—<300秒68、≥300秒0，不充媒体时长证明 |
| 10 | DONE：DATA_SCHEMA结构已核、DATA_INTERVAL_QUALITY HOLD_RANGE_CONFLICT；P1/P2仅规则通过子集的非零候选，STOP_OR_UNKNOWN不扩展；retained机制0，长视频单独确认FAIL，GPU无授权 |

Python3.9.21；本轮指定合成suite1次21 PASS、0 FAIL/ERROR/SKIP，0.034秒（不含启动）；未为本次获取修改代码。真实标准库审计1次成功返回，摘要／CSV／ZIP／文件版本hash和010 manifest只在固定隔离树，不进入GitHub。约29.5%原动作未通过数值规则、约75.5%行含异常；原因未核，不声称数据损坏或单位已知。发现冲突后停止进一步数据诊断，仅整理已有宏观收据，未查看实例／身份明细或调整parser。正小计数1—9抑制，时长只披露合并粗桶，避免反推split小单元。

资源：唯一官方数据正文3519822B，另3公共文本正文76881B，HTTP头／工具流量未计量；未获取其它数据、媒体、STA、Ego、模型／特征。0真实模型／GPU／QA／训练／评分／解码、0原研究代码／环境／锁／账本修改、0外部联系／新标签／PR合并／自动化；不公开真实CSV、文字、video/subject映射或账户路径。原一次下载授权已消耗，不能再次获取。下一真正信息需求是独立核清动作起止与length的时间合同及规则适用性，应另行明确受限只读任务；不自动创建011或放行视频/GPU。成功push后停止并保留同一聊天。

### VLM-BATCH-011 2026-10-09 16:12 北京时间 — 只读独立诊断完成；HOLD_TIME_CONTRACT

基线main5496956，安全同步并重新读取最新AGENTS、唯一READY任务、结果及指定010／安全协议。报告：[官方时间合同与完整性](codex-artifacts/VLM-BATCH-011/official-time-contract-and-data-integrity.md)、[宏观诊断与裁决](codex-artifacts/VLM-BATCH-011/aggregate-range-diagnostics-and-decision.md)；新[标准库诊断器](../prototypes/charades_time_contract_diagnostic.py)及[纯合成测试](../prototypes/test_charades_time_contract_diagnostic.py)，共5处交付，不修改旧原型或任何原数据。

| 任务 | 状态与可核事实 |
|---|---|
| 1 | DONE：固定root身份核验及原ZIP/train/test SHA与任务书完全一致；类表与固定ZIP唯一类表字节一致，157类；无获取／重解压／源树写入 |
| 2 | DONE／UNKNOWN：读取已固定官方README公开文本缓存，SHA与010一致；length秒、三元组结构、2017新增length、25点frame-mAP DOCUMENTED；全部端点同单位／同原点／同版媒体仍UNKNOWN，无新HTTP |
| 3 | DONE：先合成14 PASS，再独立csv/Decimal／区间算术1次实算；66500 token、7985/1863行、有效46875/失败19625及所有参考P1/P2键与010相符，只复用旧路径安全检查 |
| 4 | DONE：主因parse→length→time→class→negative→order→range→OK互斥且原计数sum=66500；flag可重叠，不将其和当不同坏token；小主因及其关联range宏观值补充隐匿 |
| 5 | DONE：δ桶(0,0.1]221、(1,5]8747、>5的两桶0；ρ(0,0.01]610、(0.1,1]545、>1为0；中间桶／位置大边际隐藏以防反推小格，未给实际样本 |
| 6 | DONE：全9848行异常token负担0/1/2—3/4—7/8+为2415/2190/3390/1761/92；Train/Test异常行率约73.8%/82.5%，仅字段层描述，不认证媒体时钟或独立源 |
| 7 | DONE／PROVISIONAL：原P1 gap>0组347、>0.5组313、>1组288复现；270个gap>0组位于另含invalid的行，不生成ordinal，其他可反推小余项的关联不披露 |
| 8 | DONE／PROVISIONAL：原P2 overlap97723/strong73513复现，67280 overlap pair所在行含invalid；pair不独立，不作为模型误判／关系真值 |
| 9 | DONE：源行／ID／文字／细表不输出；正小格及linked/complementary margins跨split/all联动隐藏，额外保护候选总数减关联值产生的小余项；不上传实跑JSON |
| 10 | DONE：DOCUMENTED／NUMERICALLY_OBSERVED／UNKNOWN分层；HOLD_TIME_CONTRACT、创新retain0、Charades单独长域FAIL、PTS未知、GPU BLOCKED，不猜缩放或截断 |

测试与时序：既有Python3.9.21，首次14合成方法PASS、0 FAIL/ERROR/SKIP，suite0.003秒后才读取真实来源。独立算术实跑1次，引用来源SHA固定、只读，未在真实样本上调规则。公开前审查发现“候选总数−异常行关联数”的小余项风险，随后仅合成新增抑制测试，最终15 PASS、0 FAIL/ERROR/SKIP，suite0.003秒。未再读真实CSV；最终源码算术不变、披露守卫加强，仅作合成验证，不声称最终源码再次实跑。源树／ZIP／CSV／manifest写入0。

至少8747条差额在1—5的CSV秒尺度内，不能都解释为≤0.1微小舍入，但不能据此证明单位错、数据坏或固定剪辑偏移。P1和P2多数记录候选与异常行共存，77—347组／30443—97723 pair只是两种数值口径的关联计数变化，不是可靠事件或QA数界。下一唯一支持需求是可独立核验的同版标注／媒体时间坐标说明，由ChatGPT另行限定；不联系作者、不获取媒体或自动建012。

本轮研究HTTP／数据下载0B、0GPU／模型／QA／训练／评分／视频／STA／特征／真实解码、0原研究环境／锁／账本改动、0外部联系／新标签／PR合并／后台自动化。只上传上述2报告＋2新纯stdlib文件＋本追加，原009/FIX/010结果及计划／总览均保留，成功push后停止并保留原聊天。

### VLM-BATCH-012 2026-10-09 18:22 北京时间 — 官方采样合同对齐；A限域VERIFIED／B与C HOLD

基线main72eee14，安全同步并核唯一READY／无重复回报，读取AGENTS、协议、010/011及最新任务书。仅新[源码政策报告](codex-artifacts/VLM-BATCH-012/official-evaluator-code-and-policy.md)、[三层宏观对照](codex-artifacts/VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)、[标准库对齐器](../prototypes/charades_official_time_alignment.py)、[合成测试](../prototypes/test_charades_official_time_alignment.py)及本条，共5处；原CSV、旧代码／结果、计划／总览不改。

| 任务 | 状态与真实证据 |
|---|---|
| 1 | DONE：固定root身份及ZIP/train/test/类表SHA与冻结值一致；类表157，原包额度不再获取，无源树写入 |
| 2 | DONE：只读中央目录安全验证后，内存读取唯一Charades_v1_localize.m，4649B/155行，SHA83eb3a2f30c87cc45db76235886f8d5331edb943acfdee8bab5656c5d51e0096，目标CRC PASS；未打开其他脚本文本／提取／执行.m |
| 3 | DONE：A标签构造、B互斥质量与非互斥flags、C事件真值分别冻结；原token全分母66500，无截断／缩放／统一舍入 |
| 4 | DONE：按源L22/24、L125/138/141、L58，25点binary64先除后乘、两端inclusive、同类bool OR；实际有限可解析端点及正length路径模拟，无帧矩阵／score输出 |
| 5 | DONE：先运行19合成方法，1次19 PASS、0 FAIL/ERROR/SKIP，suite0.007秒（不含启动）；覆盖越界命中、短段miss、零/极短length、同类合并、浮点次序与隐匿，后才统计真实CSV |
| 6 | DONE：实际只读聚合1次；official正cell530129/175341，总705470，strict301498/96789，总398287，额外307183，占official43.54%；全cell分母38653400；这是标签差异，不是mAP或模型错误 |
| 7 | DONE／B HOLD：within46875，crosses_end及关联大边际隐藏，starts_outside合法类别0，invalid小格隐藏；end>L/start≥L质量flags保留。至少19000条end>L且strict拒绝记录仍网格命中（固定1000宽粗桶），不认证原端点正确 |
| 8 | DONE／C HOLD：旧strict合法记录本轮均命中点，strict∩grid-hit仍P1=347/P2=97723；其270组/67280对关联另含strict拒绝token的行；纯official point labels扩大为精确event候选NOT_COMPARABLE |
| 9 | DONE：小格、父子差额、linked Train/Test/Total和quality关联计数在实跑前已设抑制；只公开宏观cell与粗桶，真实行／IDs／矩阵／原.m全文／私人路径／本地JSON均不上传 |
| 10 | DONE：A VERIFIED_WITHIN_STATED_SCOPE用于短域label政策工程对比；B TIME_RANGE_QUALITY HOLD，C EVENT_TRUTH HOLD，创新retain0、Charades自然长域单独FAIL、PTS未知、GPU BLOCKED |

源码明确t=(j−1)/25·L、s≤t≤e，而非先end≤L过滤；因此旧strict不应被称作官方frame-label构造。模拟保持double操作次序及原端点，不产生mAP，未验证MATLAB/JIT／跨语言解析全域逐bit重现或媒体帧身份。正class/point cell是同类OR后的统计，不是动作token／实例／独立N；official额外cell不意味着19,625条都是真实正确。

本轮源SHA和中央目录／目标CRC只读，旧CSV及旧原型未改；真实CSV分析1次，规则未按真实数据调整。0研究HTTP／新包／视频／STA／Ego／帧／特征／模型下载、0GPU／QA／训练／预测评分／真实解码、0执行MATLAB、0原隔离树／manifest／研究环境／锁／账本写入、0外部联系／人工标签／PR合并／后台任务。发布只含5规定产物，原始数据继续固定隔离保管；成功push后停止，保留原聊天，不自动安排013或解除科学门。
