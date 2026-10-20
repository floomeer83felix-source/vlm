# VLM-TEMPORAL-EVIDENCE-ADAPTER-025｜真实实验数据、配对选帧与末期评分接口

**2026-10-20｜唯一 READY / PUBLIC_CODE_CPU_ONLY / 待用户触发执行。**

用户已授权审查、规划并把下一工作任务写入 GitHub。本次规划提交下达本任务，
不声称025已经执行。下一执行轮由用户在现有Codex会话触发；本README只放行
下述公共源码和虚构fixture验证，不放行任何私人数据读取或GPU。

## 目的与不可继承的历史

[已完成nongold审查](../../research-reviews/nongold-feasibility-audit-2026-10-20.md)
发现024的两源/至少12题门与原筛选口径不相容，明确双事件时间间隔形式又是
28源各1题。024拟采用的rank支持门不能认证事件存在；023原ordered最多4锚点与
unordered最多2锚点也不构成干净的顺序对照。旧评分器不能直接满足生成后一次性批次gold边界。

本任务交付可供后续真实wrapper接入的**数据投影、冻结队列、等配额选帧和独立评分接口**，
不再重复素材/环境盘点，也不以合成PASS替代真实实验。逐条遵循
[025冻结协议](../../research-protocols/temporal-distance-diagnostic-2026-10-20.md)。
不改023/024，不复跑013–024任何父任务；TRAIN-GPU继续HOLD。

## 一轮内连续完成的工作

1. 安全同步独立公开文档checkout的main，重读AGENTS、next-steps、codex-results、
   research-overview、本README、025协议和其三份公开审查依据。核实唯一READY=025、
   无既有025结果、checkout干净；冲突就停止，不reset/rebase/force或触碰原实验目录。
2. 新增`prototypes/temporal_evidence_adapter_025.py`，只用Python标准库：
   实现有界streaming JSON的两种nongold投影视图、窄时间间隔语法、48候选/12帧的
   A/B/C/D四策略及不可变四臂轮转计划。C/D恰好两个不同锚点，唯一差别为i≠j与i<j；
   raw cosine只是排序分数，无rank置信门。模块无真实文件默认路径、网络、模型执行开关、
   动态import或运行时依赖。输入流只能由调用者注入；本轮一律`io.StringIO`虚构资料。
3. 新增`prototypes/temporal_evidence_scorer_025.py`：独立、导入无副作用、生成前不可调用
   gold opener的末期评分接口；按协议检查冻结terminal ledger及退出receipt、一次性guard，
   只投影本批gold，坏gold返回HOLD而不缩分母。明确逻辑receipt不等于真实OS隔离认证。
   025不启动任何真正生成/评分子进程读取真实资料；实际GPU supervisor集成留待新合同。
4. 新增`prototypes/test_temporal_evidence_adapter_025.py`，用虚构JSON/问题/选项/金标/PTS/
   分数/stub ledger覆盖协议第6节全部反例和端到端链路。用断言证明：解码边界、答案扰动
   不影响选帧、两锚点配额、已给顺序约束、提前评分零open和一次末期评分。不得只计测试数，
   每个关键边界都要有能失败的见证；不能把opaque fixture秘密写进错误日志。
5. 仅运行025新测试，优先一次，最多2次（首轮失败只允许一次静态修订后的验证）；
   每次自有stdlib child硬超时60秒，全部025受控动态CPU累计≤180秒，测试父协调器
   单调墙钟≤240秒。实现编辑和普通Git协作不冒称动态CPU。只用既有Python，
   禁第三方import、pip/conda、Torch/CUDA查询；测试child内不再启动子进程。无可靠超时监督则静态交付，
   写`DYNAMIC_NOT_RUN`，不得扩预算或将旧023测试算作本轮PASS。
6. 新增唯一`cpu-adapter-contract-receipt.md`，分别记录数据投影、语法、C/D控制、队列、
   末期评分的PASS/FAIL/NOT_RUN与必要限制、实际测试次数/时间/失败修订；静态接口
   就绪不等于私有runner完成接入、权限有效、OS隔离实证或真实QA获益。`codex-results.md`
   末尾只追加一条父结果`### VLM-TEMPORAL-EVIDENCE-ADAPTER-025`。
7. 审查脱敏与staged allowlist，单次安全普通push到main后STOP，失败也不自动重试push、
   不另立补测/资格父任务、不自动进入真实数据/GPU阶段。

## 仅允许的五处执行交付

1. `prototypes/temporal_evidence_adapter_025.py`（新）
2. `prototypes/temporal_evidence_scorer_025.py`（新）
3. `prototypes/test_temporal_evidence_adapter_025.py`（新）
4. `docs/codex-artifacts/VLM-TEMPORAL-EVIDENCE-ADAPTER-025/cpu-adapter-contract-receipt.md`（新）
5. `docs/codex-results.md`（仅末尾一条025父记录）

本README、协议、next-steps、overview和审查材料属于本次规划提交，不是025执行时
可改文件。不得提前创建空结果/回执，或把本轮写任务说成执行通过。

## 硬边界与验收

025私人元数据/媒体/QA/选项/gold/旧预测/source map/模型访问均0，目录扫描0，
GPU/模型前向/训练/研究下载/环境修改0；不得重新打开已获一次性审查的两份私人入口。
不得上传真实UID、人物/文件身份、私人路径/摘要、原题/选项/答案/模型输出或媒体。
普通GitHub文档同步不属于研究数据下载。所有测试例子必须人工虚构，不能复制私有题文。

`PUBLIC_ADAPTER_CONTRACT_PASS`只在全部规定断言通过时成立；否则诚实给出
`PARTIAL/HOLD`和未满足项。真实N、合法未见物理来源、精确时间桥接、实际runner调用、
真实QA效应均不在本轮验收范围。下一真实pilot拟最多4源各1题/四臂，仅作记录组隔离
诊断，物理录制独立仍UNKNOWN；这一新研究口径及实际资格、成本、GPU/gold范围都须
另行有证据后获用户明确接受和新授权，不能沿024严格独立门或这份README自行开始。

**REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
Charades FINAL_MEDIA_STOP。**
