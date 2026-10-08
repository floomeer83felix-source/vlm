# VLM-BATCH-003：三项低成本研究准备工作（唯一 READY 任务包）

**授权状态**：本 README 只有在 [任务书](../../next-steps.md) 将 **VLM-BATCH-003** 标记为 **READY** 时生效。一个连续执行轮次包含下面三项静态/元数据工作；**不需要三次分别等待 ChatGPT 审核**。历史 VLM-PTS-001 已合并到本任务包，不再单独领取，不重复做相同检查。

## 0. 执行前读取

- GitHub `main` 最新：`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、`docs/research-overview.md`。
- 当前本地旧实验目录与独立 GitHub 文档 checkout 的边界，参考 [VLM-001 审计](../VLM-001/workspace-audit.md)。
- [VLM-002 数据元数据审计](../VLM-002/dataset-metadata-review.md) 和旧 [VLM-PTS-001 任务描述](../VLM-PTS-001/README.md)，避免重复查错过的链接。
- 如 `codex-results.md` 已有 `### VLM-BATCH-003 ...` 完成/部分完成/阻塞报告，**不得重新执行本任务包**，交由ChatGPT审查重新授权。

## 1. 子任务 A：时间戳/媒体桥接静态审计（约 1–2 页）

**报告文件**：`timestamp-contract-audit.md`。

继承旧 VLM-PTS-001 静态协议，只读追踪：

1. 当前 `frame_index / fps` 生成相对时间的代码路径和 manifest 时间字段；记录安全相对路径、函数名或代码指纹。
2. 是否已有真实 PTS/timebase/VFR 的接口、静态依赖与测试断言；是否保存裁剪零点、源视频版本SHA与真实帧PTS。
3. 分别定义 `frame_index`、`nominal_fps`、`frame_pts`、`time_base`、`clip_offset`、`source_time`、`video_sha`，并列出当前可用/未知/不满足、失败码、边界容差。
4. 给出不改代码的最小 **验证合同与测试设计**（预期输入/输出、断言、出错时HOLD），不解码、不运行测试、不修改现有源码。

只读小范围本地代码、manifest和依赖元数据；**0视频解码，0GPU**。不能把静态可行性当作时间坐标准确性已实测。

## 2. 子任务 B：来源去重与探索污染隔离静态审计（约 1–2 页）

**报告文件**：`source-provenance-audit.md`。

以 [VLM-001](../VLM-001/workspace-audit.md) 的「30个 prepared、20个 selected、约450份历史指纹覆盖缺项」为待核事实，不把这些数字冒称互异来源。只读小范围已有 **聚合 manifest、来源索引/schema、排除规则、代码的源身份处理函数**，回答：

1. 现有 `video_id`、媒体sha、原始来源ID、上游parent、clip范围、事件/场景/上传者关联、数据集revision、历史实验组是否分别存在？哪些可用于审计，哪些UNKNOWN？
2. 为什么报告450份覆盖缺项？仅在现有聚合记录足以说明时给出定义、分母及阻碍；不能通过遍历所有视频、补算大规模媒体哈希或读取历史答案强行填平。
3. 给出未来**保守来源组键**、交叉split污染屏蔽、重复/近重复处理、缺失时宁可归为UNKNOWN/保守大组的合同；对至少40个独立来源仍不得承诺达标。
4. 提供一个只针对 synthetic/toy metadata 的示例及静态验收矩阵（可用 Markdown 伪代码，不实现为工作区改动），说明新来源进入探索前必过的条件。

禁止上传私有身份映射、原始题ID、视频名列表、完整sha清单或受限索引；禁止媒体扫描/重复哈希。

## 3. 子任务 C：G1数据门与 D1/D2 诊断可执行性合同（约 1–2 页）

**报告文件**：`g1-feasibility-contract.md`。

只根据 **VLM-002已批准的公开审计材料**、此任务包A/B的静态审计、GitHub PR #1预注册**草案**制作**条件性**技术合同：

1. VES-Bench、HERBench、CaST-Bench分别在数据许可、schema、联合必要参考区间、时间版本桥接、历史/事件独立性、12唯一源帧与区间外候选池、评分隔离方面打上**已证实/作者声明/UNKNOWN/不满足**；三者仍G1 HOLD，除非有新经批准的真实核验（本次不允许）。
2. 草拟未来用 **无答案元数据投影** 制备 manifest 的最小字段集合与类型：`source_group_id`、`media_revision`、`video_sha`、`clip_time_origin`、`time_base`、`reference_intervals`、`provenance_partition`、`frame_pts`、`failure_reason` 等；注明必需/可选、版本追溯及离线注释与评分答案隔离。
3. 将原预注册固定12帧D1/D2主要对比的构造**前置条件**写为不变量，不伪造 k 值、可行题数、帧预算或干预效应；标注暂不可执行的环节。
4. 提出下一轮 **最多3项高信息量、低成本阻碍澄清动作**（可包括作者许可/字段字典请求*草案*，但不发送邮件），以及如果三候选不合格时的研究转向判据；**Codex提出建议，不擅自判定创新通过**。
5. 给出下一步科学裁决建议：HOLD/可条件准备，明确新GPU运行必须再次授权；不能因此直接解封 VLM-003/004。

避免重新爬取VLM-002已访问的23个响应/404链接；默认**0新增外部检索、0网络数据下载**，仅允许从已固定公开报告与本地静态元数据推导。论文摘要和已有公开资料不等于实际原始数据schema。

## 4. 整包共用硬性边界

- **0**模型QA/训练/评分前向；**0**视频解码；**0**模型/视频/完整数据集/压缩包下载；**0**新增人工标注；**0**付费API、云GPU。
- 原Windows RTX3090实验目录、现有 `pytorch` conda环境、CUDA、研究代码、锁、账本、日志、媒体和模型权重**一律只读**；不得清理、修复或解锁。
- 不读取/泄露私有答案、标准标签、逐题评分、身份可重识别的完整映射，或私人绝对路径。公开仓库只收三份小型**脱敏Markdown**摘要。
- 每个子任务只读必要文件，避免全盘遍历；文件不能确认就标UNKNOWN，不用猜测或高成本试错补齐。静态代码如有受限权限，子任务标BLOCKED，不扩大权限。
- **每个子任务目标约1–2页，每份不超过20KiB**。不要把短任务变成无界研究综述、软件重构或新模型实验。

## 5. 运行顺序及阻塞处理

- 在同一个既有Codex聊天框，由用户发起一次“继续下一轮”后：**A → B → C**；A/B是独立只读审计，哪一个遇阻只报告该项UNKNOWN/BLOCKED，并**允许继续执行其余无依赖的低风险静态工作**；C基于真实已得到的A/B信息，不得假造缺失。
- 不应为某个未知自动复试失败链接、跳到旧探索题或重复已经完成的问答。
- 若出现资料泄漏、可能修改原资产、Git冲突、锁/权限安全异常，应停止本轮并写清阻碍；不会自行跑超出本任务包的研究。
- 不因“3份报告写完”宣布G1通过或授权模型调用。

## 6. 唯一 GitHub 提交与验收

在 `main` 中，本次**只允许**新增：

1. `docs/codex-artifacts/VLM-BATCH-003/timestamp-contract-audit.md`
2. `docs/codex-artifacts/VLM-BATCH-003/source-provenance-audit.md`
3. `docs/codex-artifacts/VLM-BATCH-003/g1-feasibility-contract.md`

并**追加** `docs/codex-results.md` 的单条汇总记录，标题必须为：

```markdown
### VLM-BATCH-003 YYYY-MM-DD HH:MM 北京时间 — 完成 / 部分完成 / 阻塞
```

正文用 A/B/C 逐项标记完成、未知、阻碍和附件链接，列出本次0次GPU/QA/下载/视频解码、原研究资产改动0、下轮建议及不应解除的HOLD。**不要删改历史记录、不要改任务书/研究总览/AGENTS，也不要向原 VLM-PTS-001 目录重复上传**。

提交前检查 `git diff --cached --name-only` 与全部拟公开内容，只stage上述4处。Git冲突或历史差异无法安全快进即停止；不能强推。一次安全提交完成后**停止本轮执行，但保留原Codex聊天框**，由 ChatGPT 集中审查三项后规划下一批。

**验收目标**：3份范围有限、来源可追溯、区分未知的技术合同 + 1条汇总回报，能让ChatGPT决定是否值得继续追证据数据集、工程时间坐标修复、或调整研究课题；并不要求得到新的准确率或论文新机制。
