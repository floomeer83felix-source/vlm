# VLM-SYNTH-AB-HARNESS-001｜一次合成数据 A/B 配对运行器、评分、断点恢复的可执行工程交付

**2026-10-11｜ChatGPT唯一 READY 父任务（用户明确回复「同意」）**。这是等待 Ego4D 官方媒体访问批准期间的**一次性 CPU/标准库、纯合成数据、代码与测试**工作：交付可运行程序+自动测试+脱敏结果；不是再做文献报告，也不是对真实 HourVideo QA、Qwen 或 SigLIP 的模型测量。执行者为**原来同一个 Codex 长会话**，需由用户发送新消息主动启动；提交后停止，无自动下一批。

## 0. 刚性安全门

1. 在**独立公共文档 Git checkout**里先`git status --short`、`git fetch origin main`、`git show origin/main:docs/next-steps.md`、`git show origin/main:docs/codex-results.md`，干净且仅可 fast-forward 时同步；重读`AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、此 README、`docs/experiment-first-reset-2026-10-10.md`、原`VLM-REAL-PILOT-001/README.md`及现有小型`prototypes/toy_route2_pairing.py`（只作兼容参考）。**恰好一个 READY = 本父任务且 results 不存在本 ID 的任何回报**才能开始；否则 STOP。不覆盖/重跑已结案 REAL-PILOT、BATCH-014–020、Charades 或任何历史 run。
2. 仅运行**公共 checkout 中的新纯 Python 标准库代码**和自造虚构样例。**0 GPU、0 CUDA、0 Qwen/InternVL/SigLIP 真实推理、0 Torch/transformers/视频解码/ffprobe、0 模型加载、0 真实 QA/JSON 读取、0 Hugging Face/AWS/Ego4D 访问、0 视频/权重/标注下载**。不探用户 Downloads、不可访问已取得的`dev_v1.0_annotations.json`或任何历史受限 QA，亦不可碰原 Windows 研究工作区、模型资产、运行账本、锁、`research_state.json`、Conda环境、私有路径或密钥；不安装依赖、不修改系统环境、不调用付费服务、不建立后台任务。GitHub 用于允许的文本/代码交接而非获取数据。
3. 科学状态不变：已实测开发集**标注层**存在50视频记录/1182合法标签题；用户仍未收到 Ego4D 官方视频批准。此轮**只在虚构输入上演练**，不得声称真实 24 题成绩、真实长视频自然时长、真实 GPU 时延、PTS/版本匹配已通过；`NOVELTY=RETAIN0`、`CHARADES_FINAL_MEDIA_STOP`、历史一切安全停止保持。

## 1. 真正可交付的工程模块（限定新增文件）

在`prototypes/hourvideo_synthetic_ab_runner.py`实现**可由命令行执行的完整合成配对 dry-run**，只用 stdlib；优先设计简单可靠的 API、类型约束和可审查的安全停止，不要生成另一个文档性计划：

A. **固定合成试验合同**：纯虚构数据12个不同虚构视频，每个2道虚构五选一 QA，24题配对；每个虚构视频声明≥1200秒，其中≥4视频≥1800秒；一致随机种子、冻结 manifest/policy/run_id（或等价不可变配置）并验证恢复时不许更换版本、seed、问题数、帧预算、选帧逻辑/答案键。样例ID显式前缀`SYNTH_`且与任何真实UID、问题/标准答案、canary毫无关系。**该数据由脚本在内存生成**，绝不读取本地真实QA/下载路径。未来真实绑定只能在另外一轮明确批准后完成；本轮程序默认且只支持`--synthetic`，任何`--real`、自定义`--annotations`、`--video`等必须失败关闭。
B. **两臂协议**：A在虚构的整段持续时间上均匀产生最多12个**唯一、单调、界内**采样时间点；B先产生最多48个候选时间点，以注入的**虚构 query-only scorer**对候选排序、确定性去重和不超过12帧选择；选择器 API 只能看到虚构 question、duration、候选位置及固定 policy/seed，**不能看到选项、ground-truth label、模型生成答案或评分结果**。两臂固定同样12帧送入「虚构 VLM stub」，不加载SigLIP/Qwen；如果真实 scorer 或模型 adapter 未实现，**fail closed/NOT_INTEGRATED**，不偷偷以样例分数代替真实模型。记录B虚构候选数和名义选取数，清晰区分**CPU测试次数、模拟时长与真实成本**。未来VFR/packet PTS需要先同版证明，此处只验证`duration_seconds`抽象，不宣称精准媒体采帧。
C. **评测/隔离**：对每个虚构题都记录冻结的 A/B 两臂独立响应/状态，评分函数在生成之后**才读取单独持有的虚构正确标签**；选帧、策略选择、VLM stub 和未来模型提示不可接触答案。严格 24 planned QA / 48 planned arm attempts 的固定分母；正确、错误、无效/失败或未终态分别独立计数（不能用只成功部分当分母）；配对矩阵`both_correct`、`both_wrong`、`B_corrects_A_wrong`、`B_harms_A_correct`、`invalid_pairs`（定义应自洽）；视频级12簇及≥20/≥30min分层汇总。可以提供带固定种子的**视频为簇**的 bootstrap 不确定性作为诊断工程测试，但必须显著标注「SYNTHETIC_ONLY / 不具有真实统计推断意义」；不得输出模拟正确率作为研究成绩。标明12帧是Qwen名义输入上限，**不意味着两臂总计算成本相同**；B候选评分/检索成本须单独列出**虚构操作数**而非GPU实测时间。
D. **可恢复账本 / 超预算止损**：在**新建、未存在、独立的临时 synthetic 测试目录**写入不可变 manifest、每臂尝试`STARTED`及`TERMINAL`（或等价不可逆状态），保证原子保存/写入与恢复、一次性预扣最多48次尝试、冲突进程的互斥/拒绝（保守 fail closed），拒绝相同 arm 重复调用；模拟在`STARTED`之后崩溃时恢复**不再重试**，该臂计入失败/未终态，另一个未开始的臂是否继续须遵循原冻结预算；已终态响应不得覆盖、成对问题不失踪。运行前检查代码路径不会意外读取原研究账本，不能删除别人的锁；仅清理由本次`tempfile`创建且确认独占的临时目录。模拟`max_attempts=48`硬上限（包括失败/崩溃），预算已满即STOP并报告未完成条目，不能人工免费重试。限时/异常回报保留全分母，**真实GPU预算始终0，不实现任何真实模型启动**。用进程中断模拟测试路径，不创建后台监控或系统常驻服务；避免睡眠等待和非必要并发执行。
E. **自验与防泄漏**：`python -B -m unittest prototypes/test_hourvideo_synthetic_ab_runner.py -v`和`python -B prototypes/hourvideo_synthetic_ab_runner.py --synthetic --self-test`（若实现CLI可另指定短命临时输出根路径）必须可在**不安装任何依赖**下退出码0、明确报告合成测试次数；至少覆盖①12×2与≥4个长样例 ②A≤12唯一顺序帧 ③B≤48候选→≤12帧且问句变动时分数变化 ④selector不能接触ground truth ⑤24/48固定分母含失败 ⑥纠错/误伤/两臂皆对皆错/无效 ⑦恢复等价 ⑧`STARTED`中断不重试 ⑨超过预算拒绝 ⑩修改manifest/policy拒绝恢复 ⑪并发重复/冲突拒绝 ⑫非法真实输入标志拒绝，外加边界非法时间长度/重复题目/选择label等负例。只把**虚构、脱敏**的状态/计数发到公共Git。运行实际0模型、0GPU。
F. **运行方式与边界**：帮助说明写在模块docstring/CLI`--help`，要能给下一轮用户实际复现。样例 dry-run 输出默认只显示`SYNTHETIC_ONLY`、固定分母、预算与自检状态，任何内部虚构答题正确率和虚构开销仅作为测试断言/示例可见，不能写入科研主结论。若当前公开toy原型无兼容基础，就独立新模块，不得修改旧toy、Charades代码。**无需访问本机任何真实文件证明API**。

## 2. 严格交付路径与停止

**允许修改的公共 Git 路径恰好以下四项；不要求所有四项都改，但除四项外任何修改都不允许：**

1. `prototypes/hourvideo_synthetic_ab_runner.py` —— **新增**，具有可执行合成配对运行、评分、原子 ledger+恢复代码，禁止仅搭空壳、伪函数或文档；
2. `prototypes/test_hourvideo_synthetic_ab_runner.py` —— **新增**，真实运行std-lib unittest覆盖至少12项关键断言，包括 crash/resume/拒绝真实输入；
3. `docs/codex-artifacts/VLM-SYNTH-AB-HARNESS-001/synthetic-runner-receipt.md` —— **新增**，只报告合成测试实际命令、用例数/通过/失败、运行次数、代码边界、合成账本/恢复行为、未知与下一轮真媒体门，不上传 JSON、manifest实值、合成模拟分数当研究结果；
4. `docs/codex-results.md` —— **尾部仅追加一次** `### VLM-SYNTH-AB-HARNESS-001 ...`，链接唯一收据和两个程序，明确真实GPU=0、真实Qwen/SigLIP=0、视频/QA下载/读取=0、Ego4D媒体仍HOLD。

不编辑`docs/next-steps.md`、`docs/research-overview.md`、`AGENTS.md`、此README、任何已有原型/工具、任何旧run或历史回报。Git前确认只在4路径内，完全没有真实QA、答案、视频ID、私人path/token、原素材/权重/结果。一个父任务最多**一次正常 main push**，失败只回报、不force/rebase、不开Issue/PR、不自行放行后续真实视频/GPU任务。若测试写不出可运行代码，实话报告`ENGINEERING_BLOCKED`，不以大量纸面说明代替交付。正常提交后 STOP，等待ChatGPT验收。

## 3. 性质和未来接入界面

测试通过后可判`SYNTHETIC_HARNESS_PASS`（**工程代码可运行**），绝不判`REAL_VLM_EVALUATION_GO`。当前Ego4D签约≠官方访问批准，HourVideo官方访问+开发集数量PASS≠真实媒体许可、timebase、版本桥接、历史账本隔离、GPU预算/锁已获证。若未来收到Ego4D批准，仍须经用户另一次明确限定读取、媒体下载/版本校验及模型调用预算授权，才能把真实适配器接入独立受控代码。A/B只是已有传统基线诊断，当前没有保留的论文新机制。
