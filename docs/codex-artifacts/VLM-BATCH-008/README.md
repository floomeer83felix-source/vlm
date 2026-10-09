# VLM-BATCH-008｜Charades / Charades-STA：10项免申请数据准入与科学问题核验

**日期2026-10-09｜授权以主分支 `docs/next-steps.md` 中本父任务唯一READY为准。** 用户同意暂时搁置Ego4D报错申请流程，切换至Charades作为**短视频真值/科学问题准入候选**，但未授权下载任何标注或视频。继续用原Codex聊天，一次连做10项、最多6处文本文件单提交后停止；不是10个可独立扩权的任务。

**必读**：`AGENTS.md`, `docs/next-steps.md`, `docs/codex-results.md`, `docs/research-overview.md`, [Charades入门、授权与科学假设](../../charades-entry-2026-10-09.md)，[上轮机制NO-GO](../VLM-BATCH-007/downselect-and-stop-decision.md)，原快照。Ego4D [历史申请清单](../../ego4d-access-checklist-2026-10-09.md)不再是主动申请任务。**如 `docs/codex-results.md` 已有本批回报，不重做。** 安全拉取独立文档checkout的main，本地未提交更改或冲突STOP不覆盖。

## 1—2：许可与不同标注的来源链

**1｜Charades原始许可可操作条款。** 逐句阅读 [官方License for Non-Commercial Use](https://prior.allenai.org/projects/data/charades/license.txt)与[官方项目页](https://prior.allenai.org/projects/charades)。用`ALLOWED / PROHIBITED / UNKNOWN`明确学术非商业使用、模型评测、发表必要的短例图示、重新发布改造数据、第三方分发、商用、许可携带与责任。不能把公开13GB链接等同于任意重分发。确认目标使用方式是否可能被许可覆盖；有争议保持UNKNOWN，不擅自向作者写信。

**2｜Charades-STA权利与修订。** 核对[ICCV2017 TALL作者仓库](https://github.com/jiyanggao/TALL)对train/test句子时间标注的明确schema、清理修订、代码许可与注释来源。只有作者公开下载链接不足以证明衍生句子无限制使用/再发布；分别标公开可见、许可UNKNOWN、清理版本UNKNOWN。参考 Charades-Ego官方许可差异作候补，不下载任何Drive文件。

**交付①** `docs/codex-artifacts/VLM-BATCH-008/licenses-and-provenance.md`：2项结论、确切URL、条款证据级别，约2–3页。

## 3—4：标注合同而非偷读数据

**3｜公开资料可确认的原始Charades字段。** 根据Charades官方README/论文可访问方法描述写schema：video key、action label/category、start/end、文本描述、duration、train/test及评测脚本。每个字段清楚标明`DIRECTLY_SEEN / INFERRED / UNKNOWN`；**不打开3MB标注包**，不可宣称逐行样本通过。说清楚exhaustively annotated是某注释协议的声明，不是任意未标事件都不存在的世界真值。

**4｜STA与原始Charades join、时间轴与版本合同。** 分别定义ID join、STA视频句子窗口与原标签区间的语义类型区别、同一视频时钟/clip origin、cleaned version、split mapping、文本句子改写与负样本推导的不适用条件。必要时给一个`TOY SCHEMA ONLY`例子（文字格式），不创造真实样本。若官方网页未证实join字段相容，标UNKNOWN而非默认自动连结。

**交付②** `docs/codex-artifacts/VLM-BATCH-008/annotation-and-join-contract.md`，约2–3页。

## 5—7：可测现象、指标和直接先例

**5｜重复实例能否被已有时间区间严格测量。** 构造事前可证伪`P1`：同类别同video至少2个**有可复核不重叠定义**的活动实例时，查询实例是否出现时间交换/误认？写问题粒度、标注歧义、采样分母、多次段与同类重叠排除、何种合法标签才允许ordinal question。**不能因66,500总区间就推断存在足量多实例测试源**，真实资格数UNKNOWN，需未来标注小包计数。

**6｜重叠行为/边界混淆可测合同。** 对`P2`定义同/异动作窗口重叠阈值、时间IoU和边界偏差、模型答案/定位输出、无答案泄漏、纠错及误伤、语义歧义和强基线。区分行为多标签TAL与句子moment retrieval，不把旧S_q/S_t换名称当创新。

**7｜创新性与既有基线红队。** 阅读至多6篇直接相关正式工作可公开的方法摘要/HTML，优先Charades ECCV2016/HCOMP2016、TALL ICCV2017、近期multiple action instances/event ordering/overlap-aware TAL/TMR 论文。对每个P1/P2/STA定位条目指出**现有工作是否已研究相同估计对象**，先例和精确证据范围，`REPLICATION_ONLY / POTENTIAL_MEASUREMENT / UNKNOWN / NO-GO`。不能因为用Qwen3-VL或换时长就宣称新机制；若全部已有则提议STOP。

**交付③** `docs/codex-artifacts/VLM-BATCH-008/falsifiable-questions-and-novelty.md`，约3–4页。每个任务独立编号，最多2个候选可暂留作为**未验证现象**，机制retain0。

## 8—9：现实视频适配与长时域真实性

**8｜来源/媒体/时间门。** 基于已有VLM审计仅列video/session/participant/场景可能群组、split屏蔽、同一长短版本/真PTS/timebase/clip起点、source group和可审计帧键要求；前述267用户不能替代实际participant-by-split映射。现有时钟`index/FPS`不得叫真实PTS；没有媒体也不能验收真实时间或来源独立。无需Windows本地源码访问，若仅查看已审计聚合报告也足够，禁止扫描本地媒体或读取私有身份表。

**9｜30秒数据对最终长视频研究的有效性。** 独立写`short-domain proof-of-concept`可验证什么、永远不能证明什么。给下一**真正长时域**测试集需要的时长、事件跨段依赖、合法视频与文本/时间真值、来源隔离、真实PTS、zero-/few-shot迁移/强基线、跨来源和预算条件。Charades短片拼接不能被当作自然长视频独立confirm，视频内容解码未获授权。若无合适长时域数据，**最终论文GO=HOLD**。

**交付④** `docs/codex-artifacts/VLM-BATCH-008/temporal-provenance-and-longvideo-gap.md`，约2–3页。

## 10：一次清楚的数据与研究决策

**10｜LEGAL / SCHEMA / IDENTIFIABILITY / NOVELTY / LONGVIDEO五门** `PASS / FAIL / UNKNOWN`，加明确STOP条件：许可不允许目标用途；STA独立权利无法确认；缺真实样本同类重复而P1不成立；区间标注不支持自然语言ordinal真值；直接先例覆盖且没有新可识别问题；无法取得独立真正长视频外推资源。避免为完成10项而发明算法或把toy扩成GPU计划。

若初步license允许非商业研究、标注字段清晰且存在有价值的新信息需求，**下一步仅建议向用户提出是否允许官方3MB左右`Annotations & Evaluation Code`的最小下载/计数授权**（先列存储位置及许可义务），此批不得自行下载。不能提出13GB视频或GPU的自动放行。STA若权利未确认，其标注保持HOLD。最终给最多2个待实证问题或`NO-GO`，每条有可证伪条件和需要的**单个**新增事实。

**交付⑤** `docs/codex-artifacts/VLM-BATCH-008/data-science-go-no-go.md`，约1–2页。

## 全局资源和提交约束

- 最多12个**不同的公开官方网页/论文HTML**，不以Google Drive/zip/video的可点击链接代替实际授权；如果限流/404/无法取方法，记录UNKNOWN，停止该方向反复重试。只复用既有审计/公共文档，不全盘查找。
- **0下载Charades原始/STA标注包（即使3MB）、视频（13GB）、帧、特征或其他数据；0真实视频解码/抽帧；0GPU/模型QA/训练/评分前向；0原Windows研究代码/环境/conda/CUDA/锁/账本修改；0私有答案/来源映射读取；0对外联系、Issue、付费API、PR合并、新手工标注。**
- 纯论文/许可证内容的网页阅读允许；不可将官方标注整包、真实视频/QA/私人视频身份或重发布数据推送到公共仓库。不更改旧历史/旧toy或计划。单纯许可证文本的小段引证和官方URL可写进公开文档，不能将完整条款大量复制。
- **一次GitHub push仅允许6处**：本任务书列出的五份新Markdown报告 + 向`docs/codex-results.md`末尾追加一条 `### VLM-BATCH-008 ...` 父任务回报，逐项1—10写DONE/UNKNOWN/NO-GO及资源计数/确证来源。**不得改本README/ChatGPT计划/总览/原代码；不得创建toy脚本。**
- 提交前仅stage这些路径，审阅`git diff --cached --name-only`及脱敏、检查未重复任务记录；safe fast-forward/正常push，遇冲突或权限/隐私风险立即STOP、不force push。提交后停留原Codex聊天，等待ChatGPT独立审查和用户单独数据下载许可决策；不自动启动BATCH-009/旧GPU。
