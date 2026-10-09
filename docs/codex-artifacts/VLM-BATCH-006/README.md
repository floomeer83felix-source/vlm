# VLM-BATCH-006：路线2创新性红队与无gold可行性门

**授权须以 docs/next-steps.md 中 VLM-BATCH-006 的 READY 状态为准。** 用户保留同一个Codex聊天，一个父任务包一次做完A/B/C，提交后停止。

## 0. 目标与输入

用户明确将原路线1替换为**路线2：不依赖gold必要证据区间**，研究固定12唯一源帧预算下question-conditioned选择的效果与选择路径鲁棒性。路线1的公开TRACE咨询草案仅作历史，**未授权发送**。

从独立GitHub文档checkout安全刷新main，重新读取 AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md、docs/route2-no-gold-preregistration.md 和 docs/route2-novelty-screen.md。复用BATCH-003至005历史结论。若codex-results.md已存在本父任务的结果，禁止重复领取。

## A：反新颖性审查（方法和消融）

**交付** docs/codex-artifacts/VLM-BATCH-006/novelty-red-team.md（2–4页）。

定向核对至少五项正式工作的方法、实验与消融，优先Q-Frame ICCV2025、Self-Adaptive Sampling NAACL2024、DIG CVPR2026、Efficient Frame Selection via RL CVPR2026、VideoQA Empirical Study 2024，必要时补VideoStir、WFS-SB与CVPR2025 M-LLM采帧。引用已给在创新初审文件中。最多打开10份不同公开官方/会议文档，HTML优先，不下载整篇PDF/受限论文或视频。

逐项写明：问题是否进入selector、frame/token预算约束、时间分布对照、是否已分离selector-only问题扰动与prompt-only扰动、统计抽样单位及本文自己的证据层级（摘要/方法/消融/UNKNOWN）。没读到的方法不可反推“前人没做”。若已有同一设计直接先例，就标NO-GO，不换名称救援。创新审查完成不意味着保留新机制。

## B：合法数据与现有接口有界静态门

**交付** docs/codex-artifacts/VLM-BATCH-006/no-gold-feasibility.md（2–3页）。

只检查已有本地研究工作区的**小范围源码声明和聚合schema/字段名**；不读取私有答案、原始评分、完整身份表，不扫描视频。列Qwen3-VL-4B/IMAGE12/SigLIP的现行输入及query绑定、候选帧、PTS/clip版本/sha/source分组、问题文本能否只给selector、最终提示独立、真实视觉token是否有可审计接口。只读静态，证据不足写UNKNOWN。

新数据门不再要求gold证据区间，但必须核验**媒体与问答数据研究许可、合法正确答案隔离评分、真实媒体PTS/时基与版本、历史来源污染屏蔽、12唯一源帧和可比处理器成本**。既有20操作性source group不是新外部确认组，不能由旧789节点或450缺项声称独立样本充足。给出PASS/UNKNOWN/FAIL表、估计样本量/配对不一致率/最小有用效应所缺字段，禁止重用先前240次QA预算。

给H-P主比较（问题相关S_q vs 时间分层S_t）及多样性S_d、shuffled-question负对照；H-S若缺合法事前验证的等义问法，则标NOT FEASIBLE，不生成改写标注。区分策略总效应与纯语义因果效应，并记录时间bin内PTS、画质、token、来源、问题类型等反解释。

## C：可证伪预注册补强与GO/NO-GO建议

**交付** docs/codex-artifacts/VLM-BATCH-006/preregistration-review.md（1–2页）。

对H-P提出单一主要估计量 E[Y(S_q)-Y(S_t)]、H0=0双侧备择、预定来源组、全计划分母/失败/构造排除、配对误伤和纠错、统计区间与未来确认集、强对照。H-S只能在可用且验证过的等义改写对上执行；必须区分selection-only与prompt-only。列文献同构、数据版权/答案隔离、PTS与源重合、实际token/成本控制等一票否决条件。

给出主要问题是否仅属复现、条件性可测现象、或仍存可审查的新设计空间；不能直接声称算法创新或发表价值。明确任何后续真实媒体、GPU、环境变化、外部联系都需用户**逐项另行授权**。如果数据/文献证据不足，可建议STOP而不是继续生成无边界调查任务。

## 硬边界与唯一交付

- 0 GPU、模型问答/推理/训练/评分前向，0视频解码、帧导出、受限媒体或完整标注下载，0原研究工作区、conda/CUDA、锁/旧账本/历史记录修改，0对外联系/Issue/PR合并。
- 不新增人工标注、模型改写语义标签或真实manifest。不访问私有题目和标准答案。公开仓库只接收小型脱敏文本。
- 一次提交仅新建上述A/B/C三份Markdown，外加在 docs/codex-results.md **追加一条VLM-BATCH-006父任务结果**。不要修改AGENTS、任务书、研究总览、路线2草案、历史快照或PR。
- 先安全fast-forward独立文档checkout，核对父任务没有回报；提交前审查stage精确路径和敏感内容，冲突即停止、不强推、不覆盖。
- A若受限，写UNKNOWN并继续B/C其他安全部分。三项结束后统一上传，停止本轮，**保留原Codex聊天框**；G1历史gold门不再是本方向条件，但新的合法数据门依然HOLD，VLM-003/004和GPU依旧BLOCKED。
