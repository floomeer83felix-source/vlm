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
