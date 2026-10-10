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

### VLM-BATCH-013 2026-10-09 20:15 北京时间 — BLOCKED_EXISTING_FFPROBE_NOT_FOUND／零媒体传输

基线main46bc361，安全同步并核唯一READY、无重复回报，读AGENTS、V1方案／任务书及指定历史。用户2段／64MiB GET／128MiB本地／CPU限定未扩大。报告：[Range与隐私阻塞收据](codex-artifacts/VLM-BATCH-013/remote-range-and-privacy-receipt.md)、[病例时钟与科学决定](codex-artifacts/VLM-BATCH-013/clock-case-control-and-science-decision.md)；新[安全组件](../prototypes/charades_range_media_clock_pilot.py)及[纯合成测试](../prototypes/test_charades_range_media_clock_pilot.py)。

| 步骤 | 状态与实际事实 |
|---|---|
| 1 | BLOCKED_CPU_TOOL：PATH未定位ffprobe，5个常见位置及3个应用已登记runtime精确候选均0；不全盘扫描／安装／读取原conda。原ZIP/train/class SHA PASS，新媒体路径祖先身份与已知metadata/docs/研究隔离、空间≥512MiB已核；完整云/写权限前置未完成，不标全PASS |
| 2 | NOT_RUN：工具门失败即停止真实流程，未读实际ID/subject冻结两例，未建私有映射；只验证合成确定性选择 |
| 3 | NOT_RUN：当前官网锚点／HEAD／ETag／实际206未知，0官方请求，未触及13GB对象 |
| 4 | NOT_RUN／UNKNOWN：真实EOCD/ZIP64/central/member安全未知；代码仅支持受限经典结构，ZIP64/descriptor/未知extra明确STOP |
| 5 | NOT_RUN：0视频、0.part、0CRC/SHA媒体收据；未创建MediaPilot根或真实ledger，不替换源／候选 |
| 6 | NOT_RUN：ffprobe版本及容器／packet PTS未知，0ffprobe执行、0帧／像素／音频访问 |
| 7 | UNKNOWN：CASE_OVERFLOW与CASE_CONTROL均CLOCK_UNKNOWN，未用CSV/FPS填媒体钟，无精确私有时长／PTS披露 |
| 8 | DONE（边界）：V1不提供动作实例真值／整体19,625条解释，不外推P1/P2／长域；A沿012限域VERIFIED，B/C HOLD |
| 9 | DONE（合成）／真实未核：标准库16方法1次16 PASS，0 FAIL/ERROR/SKIP，suite0.006秒；验证206/200、错范围/跳转/编码、跨请求失败预算、EOCD/local/CRC/安全拒绝、2成员、ffprobe与隐私等，未连接服务器 |
| 10 | DONE（停止）：V1_ACCESS BLOCKED_PRECONDITION、V1_CLOCK UNKNOWN，当前执行NO_GO；实际Range访问路径本身仍UNKNOWN，创新retain0、长域单独FAIL、GPU BLOCKED |

**实现状态PARTIAL_FAIL_CLOSED_COMPONENTS**：受限Range／经典ZIP／预算／去识别clock组件仅合成验证；端到端协调器未放行，入口即便未来找到工具仍显式阻塞，不能称已交付可自动运行的两视频抓取器。不会拿真实服务器响应现场改结构／选择／容差。之后只做本地合成验证及阻塞交付，不开展真实视频步骤。

资源：本轮官方网页GET/媒体HEAD/Range GET均0，响应正文总0B，媒体及临时媒体峰值0B，最终视频0，私有选择／PTS文件与媒体ledger未创建。0GPU／模型／QA／训练／评分／解码／画面音频人工核验、0原研究目录／conda／CUDA／锁／账本及旧源码修改、0外部联系／新标注／镜像／PR合并／自动化；原metadata树只读。

当前最小缺失事实是可验证的既有非原科研conda ffprobe入口；如需要安装或释放后续完整协调器须由用户／ChatGPT另行限定任务，本轮不做。只提交两报告、两新源码及本条5处，成功普通push后停止，保留同一聊天，不重复013或自动安排014。

### VLM-BATCH-013-FIX 2026-10-09 21:03 北京时间 — 用户直接授权代码修复；工具安装待明确批准

依据用户本轮“修复”，安全刷新main仍f86a1e8；不重做已回报013，不改其阻塞报告、任务书、总览或原数据。修改[受限协调器](../prototypes/charades_range_media_clock_pilot.py)、[合成测试](../prototypes/test_charades_range_media_clock_pilot.py)并追加本条，共3处。

**修复**：移除永远终止的未放行占位，补齐独立固定路径／原工作区排除／云根／SHA前置、私有确定性两例冻结、官方锚点／许可核验、持久化跨请求预算、尾部和central索引／两成员local-header核对、有界解压／CRC／不覆盖落盘、CPU packet探测与私有时钟收据。支持经测试的单盘ZIP64 EOCD／locator、64位central及local extra，继续拒绝数据描述符、未知extra、分卷、异常flags、路径／重叠／CRC／超预算。网络64MiB／GET12／本地128MiB限制保持，并为审计临时写入保守预留空间；不作真实服务兼容性保证。

**控制入口**：默认仅工具预检，不联网／不建媒体目录。真正执行需显式execute及唯一READY、无既有父结果、匹配本受限媒体协议的parent；当前013已回报，仍拒绝重复。原工作区排除位置必须由可信执行上下文提供，未知即STOP，不提供源URL／数据目录自定义接口。ffprobe发现新增固定独立CPU-Tools落点，并检查规范目标仍不指向原科研／conda。

**验证**：保留原16方法，逐次扩展并运行5轮纯合成suite，均PASS；最终27方法0 FAIL/ERROR/SKIP，suite1.099秒。新增ZIP64、安全字段顺序、已完成父任务拒绝、默认不联网、ledger原子持久化、两成员合成提取到mock ffprobe的完整协调流程、非finite时钟及Conda重定向保护。所有HTTP、ZIP、媒体byte和PTS为虚构或mock，无真实请求／媒体运行。受限ZIP64以外未覆盖结构仍STOP，不拿测试PASS当服务器206／病例钟已核。

**工具缺口未解**：除013已查PATH／8候选外，本轮对4个有限软件根中FFmpeg相关目录作只读定位，仍未找到既有ffprobe，没有扫描原研究／Conda。已向用户询问是否允许独立安装到专用CPU工具树、不改Conda或全局PATH；截至本提交未收到安装批准，因此没有工具下载或安装。原013第1项明确禁止自行安装，本轮不推定“修复”已覆盖该新增操作。

本轮真实研究HTTP／媒体GET正文0B、0工具／媒体下载安装、0真实ffprobe、0视频／帧／音频／GPU／模型／原研究环境／隔离原数据／锁／账本更改。仅合成临时对象有测试写入，媒体试点根与真实ledger／私有病例仍未创建，A/B/C科学状态沿既有结论。代码修复可审查，实际工具就绪及服务运行仍UNKNOWN；成功push后停止，保留当前聊天与安装选择问题，不自动执行013或新媒体任务。

### VLM-BATCH-014 2026-10-09 — BLOCKED_TIMEOUT；固定工具获取安全停止，媒体继续HOLD

安全同步main至`afd21abd9da1d42a331e913eb81e4981a4bc6eed`，读取AGENTS、最新任务/结果/014及指定013/FIX历史，核唯一READY与无014回报。仅本次[来源完整性与隔离收据](codex-artifacts/VLM-BATCH-014/tool-source-integrity-and-isolation.md)、[工具就绪与代理门](codex-artifacts/VLM-BATCH-014/ffprobe-readiness-and-proxy-hold.md)、[新标准库安装器](../prototypes/isolated_ffprobe_installer.py)、[合成测试](../prototypes/test_isolated_ffprobe_installer.py)及本条5处；不修改任务书/总体总结/旧代码或原研究资产。

| 步骤 | 最终状态与事实 |
|---|---|
| 1 | DONE：独立docs checkout安全fast-forward，唯一READY、无重复父结果 |
| 2 | DONE：固定LOCALAPPDATA工具树、x64/Windows10+、祖先身份/reparse/云根/原研究与兄弟树排除、空闲≥1GiB与新文件权限通过；私人绝对路径不公开 |
| 3 | DONE：FFmpeg官网推荐第三方Gyan，固定9.0.2/GPLv3/同站checksum一致；两别名HEAD锁固定对象，完整包SHA未验证 |
| 4 | DONE：初15方法14 PASS/1 FAIL，修正已知长度超剩余全局预算的预读拒绝后15 PASS；首次真实初始化在任何网络/目录创建前因父目录缺失停止，核0请求，修新安装器同一固定树并加不覆盖用例，最终16 PASS、0 FAIL/ERROR/SKIP，suite0.470秒；全部先于正式网络 |
| 5 | BLOCKED_TIMEOUT：显式no-proxy/默认TLS/禁跳转的唯一包GET超时；三文本GET完成，工具ZIP部分正文13,107,200B，累计13,186,907B，GET4/HEAD3、成功完整ZIP0、重试0；无替代来源/预算重置 |
| 6 | UNKNOWN_NOT_RUN：无完整包，真实ZIP结构/白名单/CRC未知；提取0 |
| 7 | BLOCKED_PRECONDITION：ffprobe.exe未创建，版本调用0，版本/exe SHA/Authenticode UNKNOWN |
| 8 | DONE：旧媒体源码L132 build_opener(NoRedirect())及标准库默认ProxyHandler静态核验，可能继承env/系统代理；不读代理值、不执行/修改旧媒体客户端，代理门HOLD |
| 9 | DONE：私有最终2文件13,107,774B（部分包+574B账本），无exe；精确峰值UNKNOWN，初始ledger0不是峰值收据，保守文件字节上界14,155,776B＜512MiB；无原始日志/身份/二进制上传 |
| 10 | DONE：CPU_TOOL=BLOCKED，MEDIA_NETWORK_CLIENT_PROXY=HOLD，V1_MEDIA_ACCESS=NOT_RUN，B/C_EVENT_TRUTH=HOLD，创新RETAIN0，GPU BLOCKED |

冻结发布方包SHA仍为`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`，实际64B校验文本匹配；不能将其当作本轮不完整ZIP SHA通过或独立数字签名。官网约109MB只作展示值，不是完整下载大小。包HEAD精确大小没有进入最终持久ledger，故不编造精确数字。部分工具包和本轮私有账本保留原固定新工具树，未改名完整ZIP、未清理/覆盖以重试；未来恢复需新限定父任务审查，已回报014不得重跑。

本轮0 Charades网页/媒体/Range GET、0视频/STA/标注/特征/模型下载、0 PTS/真实解码/人工动作核验/GPU/模型/QA/训练，0原研究目录/Conda/Python/PyTorch/CUDA/PATH/原CSV ZIP/旧账本/旧源码改动，0外部联系/PR/后台调度。工具获取失败不能被称作工具READY或研究机制成立；按规定提交本轮5处，正常push后停止，保留同一聊天，等待ChatGPT审查。

### VLM-BATCH-015 2026-10-10 — 固定对象206续传完成；CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED，媒体HOLD

安全fast-forward独立docs checkout至main `67590a0`，读取AGENTS/任务书/结果/015合同、014来源和工具报告及旧安装器，启动时核唯一READY=015、014已回报且015无结果。新[原part/双账本与远端身份收据](codex-artifacts/VLM-BATCH-015/local-part-ledger-and-remote-identity.md)、[完整性部署与科学裁决](codex-artifacts/VLM-BATCH-015/resume-integrity-install-and-science-decision.md)、[独立标准库续传器](../prototypes/isolated_ffprobe_resumer.py)、[合成回归](../prototypes/test_isolated_ffprobe_resumer.py)及本条，共5处；014公共文件和旧私有账本未改、原part仅按本批授权追加。

| 步骤 | 状态与真实证据 |
|---|---|
| 1 | DONE：独立docs安全同步、单READY/无重复父结果，原014不重跑 |
| 2 | DONE：固定工具树身份/no reparse/已知cloud roots/原研究及兄弟树排除、x64/Windows10+/空闲≥1GiB；原part13,107,200B/PK签名、旧ledger574B/累计13,186,907B/4GET/3HEAD/4事件及末PACKAGE STOPPED吻合；只有2旧文件 |
| 3 | DONE：首26方法全PASS，suite1.447秒；合成阶段加“失败探测不得解锁后缀”后最终27方法全PASS，0 FAIL/ERROR/SKIP，suite1.400秒；全部先于真实网络，真实响应后不改代码 |
| 4 | DONE：固定Gyan9.0.2对象两次HEAD资格一致，Content-Length114,768,076B/ZIP类型/同强ETag；ETag只留私有ledger，显式no-proxy/默认TLS/禁跳转 |
| 5 | DONE：1B原尾端探测206逐字匹配，随后唯一If-Range后缀GET101,660,876B；两请求实际206、精确范围/长度/identity/同ETag通过，0重试/整包重下/网页GET |
| 6 | DONE：拼合part114,768,076B，完整SHA与冻结发布方60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba完全一致并最终重核；不追认014原ETag |
| 7 | DONE：真实ZIP安全/预算及全成员CRC PASS，只独占提取ffprobe.exe、LICENSE、README.txt三文件；旧part/旧ledger保留，无extractall/其他exe或DLL提取 |
| 8 | DONE：一次ffprobe -version、timeout10秒、返回0、9.0.2-essentials_build-www.gyan.dev；exe SHA私有复核一致，Authenticode UNKNOWN_NOT_CHECKED；0媒体输入 |
| 9 | DONE：新独占续传ledger继承旧事件/预算、读前持久保守预留；本轮实际/预留101,660,877B相等，两轮实际/计费114,847,784B；前缀和旧ledger SHA不变；最大观测逻辑和325,212,443B，瞬时账本预留上界326,261,019B＜512MiB，精确物理峰值未测 |
| 10 | DONE：TOOL_RANGE_SUPPORT VERIFIED_206、CPU工具仅publisher-hash scope AVAILABLE；媒体PROXY_HOLD/V1_MEDIA_ACCESS NOT_RUN、B/C HOLD、创新RETAIN0、GPU BLOCKED |

资源：015新增HEAD2/GET2（探测1B+后缀101,660,876B），014+015总HEAD5/GET6，重试0；继承13,186,907B，新增101,660,877B，总114,847,784B≤157,286,400B，剩余42,438,616B，未新增额度。最终私有6文件逻辑字节220,068,317B，新ledger1,823B/旧ledger574B，无 `.next`残留；完整原part不改名/不删。峰值逻辑和含提取原子发布两个硬链接名的保守重复计数，不能称物理磁盘分配峰值；另1MiB涵盖瞬时账本，不隐瞒计量边界。

强ETag与1字节探测只证明本次对象稳定/边界一致；完整发布方SHA才验证现存旧前缀和新后缀共同组成冻结包。发布方同站SHA不是独立签名或无恶意软件保证，版本检查不是媒体时钟/语义真值。0 Charades请求/媒体Range/视频/STA/标注/特征/模型下载，0 PTS/视觉解码/画面或动作人工核验/GPU/模型/QA/训练，0原科研环境/Python/PyTorch/CUDA/Conda/PATH/旧CSV ZIP/旧账本/旧源码/任务书或总体总结改动，0外部联系/PR/后台调度。私有ETag/部分指纹/exe SHA/本地ledger/工具包/exe不上传；只提交规定5处，正常push后停止，保留原聊天等待ChatGPT审查，不解除旧媒体代理门或自动执行新任务。

### VLM-BATCH-016 2026-10-10 — 媒体客户端禁代理代码修复，40项纯合成PASS；真实媒体NOT_RUN

独立docs checkout安全fast-forward至main `c6a3149`，重读AGENTS/最新任务与结果/016合同/013原合同和媒体源码及测试，核唯一READY=016、无既有结果。仅[HTTP代理威胁与修复](codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md)、[合成收据与科学门](codex-artifacts/VLM-BATCH-016/code-only-test-and-science-gate.md)、[媒体协调器](../prototypes/charades_range_media_clock_pilot.py)、[其合成测试](../prototypes/test_charades_range_media_clock_pilot.py)和本条5处，不重跑013/014/015，不改其历史或工具资产。

| 合同八项 | 状态及证据 |
|---|---|
| 1 | DONE：干净独立checkout安全同步、单READY/无重复结果、指定文件已读 |
| 2 | DONE：项目页/许可GET、固定媒体ZIP HEAD和所有Range共用原默认ProxyHandler风险；静态核工具入口、响应/预算/任务守卫，未读取实际代理配置 |
| 3 | DONE：新增唯一build_media_opener，ProxyHandler({})/默认验证TLS/NoRedirect；新增fixed_request精确三官方HTTPS URL/方法，禁整包媒体GET/未知源/编码，所有网络路径共享安全实例；显式308拒绝兼容当前Python |
| 4 | DONE：原27方法AST完全保留、新增13，总40；首轮38 PASS/1 FAIL/1 ERROR/0 SKIP，suite3.605秒；308别名缺失与空headers夹具问题修正，最终40 PASS、0 FAIL/ERROR/SKIP，suite3.724秒 |
| 5 | DONE：现有Python -B仅运行合成unittest，setUp阻断未mock网络和subprocess；0真实preflight/execute/ffprobe/HTTP/工具或视频读取 |
| 6 | DONE：AST常量完全一致；既有节点只NoRedirect/RangeClient/run_pilot的网络入口有差异，其余函数/类不变；64MiB/128MiB/12次/两例、源SHA、隔离、ZIP/CRC/时钟和ffprobe参数未变 |
| 7 | DONE：仅两报告+媒体代码/测试两处修改+本条结果，未上传代理值/映射/真实数据/日志/工具或私人路径 |
| 8 | DONE：MEDIA_CLIENT_PROXY_POLICY CODE_LEVEL_VERIFIED；REAL_MEDIA_RANGE_206 UNKNOWN，V1_MEDIA_ACCESS NOT_RUN，科学B/C HOLD、GPU BLOCKED，提交后停止 |

新增反例覆盖代理环境污染、Windows combined/env/registry代理发现函数mock异常且不调用、TLS与不安全context、301/302/307/308读前拒绝、精确URL/方法与有界Range/If-Range、四条路径共享opener、200/416/源变化、文本编码/大小/未知源读前停止、失败字节与预算不重置、已完成013即便仍READY也拒绝、无备用Request/urlopen入口。原27项的ZIP64/CRC/路径/两例/账本/时钟与mock协调流程不删改。测试只处理虚构BytesIO/ZIP/MP4/mock ffprobe及合成临时文件，没有读取已部署CPU工具或任何真实视频。

本轮研究HTTP GET/HEAD/Range（Charades页面、许可、媒体及Gyan）全部0，正文0B、真实媒体落盘0、真实ffprobe调用0、PTS/画面解码/人工动作核验/GPU/模型0；GitHub文档Git同步和推送仅属授权交接。0原科研目录/Conda/Python/PyTorch/CUDA/PATH/系统代理/工具隔离包与账本/原CSV ZIP变更，0外部联系/PR/后台调度。CPU工具可用仅沿015已验收报告，本轮未重新验证；A沿012限域，B时间质量/C事件真值HOLD、Charades单独长域FAIL、创新RETAIN0。

边界如实保留：旧默认预检先调用ffprobe版本；执行父任务门是READY/既有结果/README关键字检查，不能解析完整许可语义；媒体ledger仍读取后add，未升级015式读前保守计费。本轮不运行这些真实入口、不扩大代理修复为完整媒体访问GO；后续须独立任务审查执行门、记账与真实服务。正常push后停止，保留原聊天等待ChatGPT验收，不自动创建017或启动媒体。

### VLM-BATCH-017 2026-10-10 — BLOCKED_SYNTHETIC_GATE_FAILED；离线补强交付，真实媒体未开始

独立docs checkout安全同步main `9e7bd45`，核唯一017 READY/无结果，重读AGENTS/任务板/结果/017合同、013原协议、015工具收据、016源码/威胁报告和总览。本轮仅[访问与预算阻塞收据](codex-artifacts/VLM-BATCH-017/media-v1-access-and-budget-receipt.md)、[两例时钟与科学裁决](codex-artifacts/VLM-BATCH-017/two-case-clock-and-science-decision.md)、[媒体协调器](../prototypes/charades_range_media_clock_pilot.py)、[合成测试](../prototypes/test_charades_range_media_clock_pilot.py)及本条5处；历史013—016公共产物、原metadata/工具账本和科研环境不改。

| 合同步骤 | 最终状态与实际证据 |
|---|---|
| 1 | DONE：安全fast-forward、单READY/无既有017结果；017合同与013/014/015/016回报规范文本SHA绑定通过，许可先于任何主流程副作用 |
| 2 | DONE（代码）：严格只准017、禁关键词冒充、默认不调用工具；读前原子flush/fsync不可退reserve，actual/charged分离，文本/Range统一64MiB/GET≤12；强ETag、固定015 bin/收据SHA/无PATH回退，016禁代理/TLS/源守卫保留 |
| 3 | 最终离线DONE但执行门曾失败：原40方法保留+16新方法；首外部55PASS/1FAIL（漏reserve的mock夹具）后56PASS，suite4.837秒；唯一execute内置合成失败即停止；随后只合成诊断并补祖先mock，双上下文最终56PASS，0FAIL/ERROR/SKIP，suite6.629/10.190秒 |
| 4 | BLOCKED_BEFORE_PREFLIGHT：主流程正式metadata SHA/物理隔离/CPU工具版本均NOT_RUN，版本实际调用0 |
| 5 | NOT_RUN：未读取正式train行、冻结实际两候选或建selection.json；样本算法不改 |
| 6 | NOT_RUN：项目/许可GET0、S3 HEAD0/Range0、工具GET0；官方当前强ETag/206/ZIP结构UNKNOWN，不归因服务器 |
| 7 | NOT_RUN：真实保存视频0、MediaPilot根未建、真实私有媒体占用0B |
| 8 | NOT_RUN：CASE_OVERFLOW/CASE_CONTROL均未运行，packet-PTS调用0，0画面/人工动作核验 |
| 9 | DONE（阻塞范围）：实际与保守已计研究正文0B，真实ledger不存在，media根/ledger存在性只读复核false；不拿合成ledger当实跑记录，无私人路径/ID/PTS上传 |
| 10 | DONE：MEDIA_RANGE_206 UNKNOWN、V1_CLOCK UNKNOWN，B/C HOLD，A沿012限域、创新RETAIN0/长域FAIL/GPU BLOCKED，安全停止不安排018 |

**一次机会的完整简史**：外部首56方法55PASS/1FAIL/0ERROR/SKIP、suite3.981秒，修旧mock客户端漏reserve；第二轮56全PASS。静态核017实际合同/历史SHA、预算、原40名字及科学/ZIP/代理函数保持后，仅启动一次明确017 `--execute`；它在内置套件返回SYNTHETIC_GATE_FAILED，没有越过该门。离线临时合成LOCALAPPDATA/原工作区变量复现为55PASS/1ERROR（旧Conda路径测试的AuditError），原因是旧resolve mock与新增祖先检查不兼容；补夹具check_ancestors mock后两上下文56全PASS，未重启execute、未在真实网络响应后改策略。该次内置旧mock没有完全屏蔽祖先stat，不宣称完全0身份元数据触达；没有真实工具内容读取/调用或主流程原ZIP/CSV读取。

保守预扣、fsync故障、短读/超时不退、跨文档/Range总预算、旧013/未授权父任务版本0、冻结合同/历史漂移、无工具回退、弱ETag/错total、13GB整GET拒绝均有新增纯合成反例。原40场景保留，夹具按预扣/强ETag/严格许可规则适配；没有降低预算或改变冻结选择/ZIP/时钟公式/packet命令。最终PASS证明离线代码和测试夹具状态，不追认已经停止的execute为成功，也不允许同父任务再试。

本轮真实研究HTTP及正文0、预留0、版本/PTS调用0、媒体文件/媒体私有峰值0；GitHub授权Git同步/交付另列，不算研究HTTP。0真实下载视频/整档/STA/工具/特征/模型、0视觉解码/人工重标注/GPU/训练，0原科研/Conda/CUDA/PATH/锁/元数据或工具包及旧账本写入、0外部联系/PR/后台调度。正式本机SHA/CPU工具/隔离门仍未跑，只沿015旧验收事实，不伪造病例钟或科学成功。仅五处正常push后停止，保留原聊天，等待ChatGPT审查新限定任务；不自动重跑017或安排018。

### VLM-BATCH-018 2026-10-10 — 两成员有界获取完成，V1两臂CLOCK_UNKNOWN；最后机会停止

独立docs安全fast-forward至main `3e1abe4`，重读AGENTS/任务/结果/018合同、017访问及科学报告、016安全源码/015工具收据/总览，启动时唯一018 READY且无回报。仅新[前置与HTTP资源收据](codex-artifacts/VLM-BATCH-018/preflight-and-http-resource-receipt.md)、[两例PTS与科研裁决](codex-artifacts/VLM-BATCH-018/two-case-pts-and-research-decision.md)、[协调器](../prototypes/charades_range_media_clock_pilot.py)、[原合成测试](../prototypes/test_charades_range_media_clock_pilot.py)及本条五处；013—017不重跑/不改历史。

| 步骤 | 本轮真实结果 |
|---|---|
| 1 | DONE：安全Git/单READY/无重复回报，018父门先于工具/元数据/目录/HTTP |
| 2 | DONE：018完整合同SHA规范重算，017历史段落SHA加入，013—016旧pin保留；原预扣/TLS/禁代理/NoRedirect/固定URL/ZIP/样本/时钟算法和限额未改 |
| 3 | DONE：原56场景保留+3新方法，总59；普通discover59PASS/suite6.546秒，独立子进程loadTestsFromName普通/模拟各59PASS、suite6.546/6.474秒，均0FAIL/ERROR/SKIP；同测试集合SHA33b41c66276b80f9be73456c57b386291dee9671d96efd1b71900196ad039387；未有失败后仍执行 |
| 4 | DONE：真实execute仅1次；程序内置普通/模拟环境各59PASS，SOURCE_SHA_AND_ISOLATION PASS、015固定bin/私有部署及exeSHA核验PASS、9.0.2版本实际调用1次/返回0，无工具下载回退 |
| 5 | DONE：固定SHA train按原公式先选并私有冻结1越界/1严格合法对照、两个唯一身份，随后才看远端；未重选/泄露ID |
| 6 | DONE：项目/许可锚及固定许可SHA、唯一S3 HEAD强ETag/identity/长度、后续精确If-Range206/ZIP索引/local头守卫通过；无镜像/代理/跳转或200整包正文回退 |
| 7 | DONE：两指定成员CRC/大小/预算通过、保存2 MP4；GET10/HEAD1、actual=charged=1,979,817B，无重试/整包下载 |
| 8 | DONE（采集）/UNKNOWN（同钟）：CPU v:0/file/show_packets探测2次，CASE_OVERFLOW及CASE_CONTROL均CLOCK_UNKNOWN；B帧标志触发冻结守卫，未改阈值/重新probe/看画面 |
| 9 | DONE：10事件COMPLETE，read=reserved/pending0；最终6私有文件逻辑和882,420B，最大观测逻辑和1,243,981B；加1MiB核算2,292,557B＜128MiB，精确物理峰值未测；只公开聚合指标 |
| 10 | DONE：SOURCE_SHA_AND_ISOLATION/FFPROBE_VERSION PASS、MEDIA_ZIP_RANGE206 VERIFIED_FOR_SELECTED_MEMBERS、V1_CLOCK UNKNOWN；B/C HOLD、A沿012限域、创新RETAIN0/长域FAIL/GPU BLOCKED；最后机会停止不安排019 |

本轮实际与不可退保守研究正文1,979,817B≤67,108,864B，总GET10≤12、S3 HEAD1；CPU版本1次+两容器/packet探测2次，共3次ffprobe调用，没有追加/重试。最终私有媒体根6文件（两MP4、两clock审计、选择映射、网络ledger），incoming为空、无ledger.next，两视频私有SHA与探测记录只读复核一致。峰值按文件名逻辑和记录，原子发布时硬链接名重复保守计数，不当物理分配峰值；原小额AUDIT_RESERVE不改，额外1MiB核算本次观测峰值仍远低于128MiB。014/015工具预算/旧包/旧账本不重置或挪为媒体额度；无用户原科研/Conda/PATH/CUDA/锁/原CSV ZIP写入。

两个B帧标志触发原classify_clock早期UNKNOWN，不能写同钟MATCH/DIFFERS或异常end已物理确认；保留原始video packet/容器元数据仅于私有clock文件，不输出个体ID/subject/class、精确长度/FPS/PTS/DTS/end、单成员偏移/大小、私有hash/绝对路径/代理值。安全获取成功只证明此次固定来源/两预选成员可取，不是事件真值或长视频研究成功。0观看/像素解码/人工重标注/STA/模型/GPU/训练，0其它工具或数据下载，0外部联系/PR/后台调度。

按用户最后机会合同停止Charades媒体获取，不消费余留额度再开批；Charades仅可作短域工程对照，长视频合法数据和科学重新定位交由ChatGPT评估，当前原创机制仍RETAIN0。只五处普通push后停止，保留原聊天等待验收，不自动019/V2/GPU或新数据路线。
