# VLM-HOURVIDEO-OEP-REAL-024｜未见HourVideo真实OEP零训练推理试点

**2026-10-19：READY / USER_APPROVED_SINGLE_RUN_MEDIA_QA_GPU_PILOT（唯一READY，尚未执行）。** 用户在ChatGPT中收到024的具体资源及数据范围后明确答复**“批准”**。本授权只对024这一次父任务生效；需要用户在活跃Codex私人聊天另发一次执行指令方可执行。

ChatGPT已完成新真实科学试点的完整设计，详见 [冻结协议](../../research-protocols/real-oep-pilot-2026-10-19.md)。不创建重复合成toy、CPU资产预检或原009电影自监督训练。023仅证明纯合成规则逻辑正确，未证明问答提升。

**本轮已获得用户单次明确授权，仅限以下上限：**新HourVideo/Ego4D录制源组最多2条、与旧R1–R6及彼此的物理采集/剪辑来源隔离必须正面证明；每条至多24道新nongold题、合计至多48道，仅在生成/ledger终止后由单独CPU评分者一次性读取**这批题的gold**。可只读访问为此精确必要且历史已明确授权的非金标来源组/版本映射和媒体入口元数据；优先使用已在合法许可范围的精确本地新来源。仅必要时从**固定官方Ego4D条目**进行授权的HTTP媒体读取/下载，实际正文≤28GiB总、每条≤14GiB，私人新增媒体/缓存/结果≤32GiB；需查官方访问许可仍有效。RTX3090总GPU推理占用≤25分钟（含加载、SigLIP/Qwen特征和前向），Qwen QA generate≤240，PyTorch peak allocated≤18GiB，CPU媒体阶段≤900秒，父单调墙钟≤3600秒。实验仅**零训练**，无新的训练权限、Torch环境安装/修复、新模型下载、云/API、未授权受限数据或过往任务额度继承。

**先CPU资格后资源消耗**：仅对上述获准的精确源元数据和nongold题进行最小安全访问，先验证来源权限、当前许可有效性、真实来源组正面独立性、恰当版本/时间基准、确定性的题文双事件分解与至少12条可用题；不得仅据UID不同推断实际独立，不得用旧R1–R6已看题或gold调策略。任何必要入口未知、权限过期、可用双事件题<12或物理来源独立UNKNOWN → STOP并提交合法脱敏HOLD；**未过CPU门不得下载媒体或调用GPU**。不得为了达标扫描磁盘、另找非固定视频、变更规则或查看gold。资格过关后，在既定media/GPU预算内一轮执行全部五臂。中途失败计入真实尝试与冻结分母，不能通过重跑/改seed凑结果。

在用户已于当前ChatGPT会话授予上述一次新许可、且GitHub看板唯一READY=024后，Codex依照以下父任务顺序执行：

1. 独立docs checkout安全main fast-forward、读AGENTS/next-steps/codex-results及当前合同，检查024唯一READY且没有024结果。旧实验Git/ledger不得重置、覆盖。
2. 严格仅用用户新授权的nongold source-group/题文证据选2条物理独立且从未在R1–R6用过的来源，冻结≤48条QA及确定性双事件语法识别，不看gold。如少于12个显式双事件题，GPU0并报告真实试点不适用，不为凑数放宽。
3. 仅从两条固定授权真实媒体精确条目/官方Ego4D源获取合法视频，执行有限校验与PTS/资源门，不扫描其他文件或替代源。既有验证文件优先；下载上限见冻结协议，HTTP预算和持久匿名ledger必须严格监督。
4. 冻结同48候选/12帧真实Qwen+SigLIP管线对比五臂Uniform12、GlobalTop12、12bin、unordered、OEP_RANK_REAL_024；真实rank百分位只代表打分排名，不是023 synthetic阈值的可校准证据。所有事件词仅来自nongold题文、禁止用选项/gold/参考时间推断AB真值。限时限显存、异常即STOP，不重试失败/提升额度/训练。
5. 全部GPU及模型子进程退出、队列日志稳定后唯一CPU scorer才可在限定本轮新QA范围打开gold一次，保留full denominator及匿名paired结果。结果不等于hourvideo正式榜单或论文创新。
6. 一次性完成真实执行所需的最小代码集成：允许新增通用公共原型 prototypes/hourvideo_oep_real_024.py，以及配套纯合成接口/安全门测试 prototypes/test_hourvideo_oep_real_024.py（两者都只存公共算法/输入接口、不可带任何个人实际路径、ID、访问凭据或原始答案；不能改旧017/018/019/023源码）。经未来明确新媒体/GPU授权后，在本父任务安全CPU门通过的前提下直接复用既有Qwen/SigLIP及023 selector，必要时由上述新runner执行零训练前向。若runner无法安全调用现有私有推理组件或缺权重时报告HOLD，不临时安装/迁移环境。公开main总共**最多4处**：以上可选的2个新Python文件、唯一匿名 docs/codex-artifacts/VLM-HOURVIDEO-OEP-REAL-024/real-oep-pilot-receipt.md、codex-results.md末尾完整父任务条目。允许的额外纯合成接口测试计入同一父墙钟，不另下一个toy任务；不得把测试PASS当QA提升。不得上传私人媒体路径/片名、UID/QA/gold/来源映射/hash、模型权重、预测逐条或原始日志。一次常规安全push后STOP。

**重要执行边界**：Gold只能在所有生成子进程退出、队列及防泄漏账本冻结后由独立CPU scorer读取1次；选帧计算不得读正确答案、参考时间、旧实验回放日志或把题目选项当事件。真实rank proxy与合成tau=0.70不是概率校准；若回退B或该题不可拆分，必须如实报fallback而不是更换题或抽样。024上限仅支持≤2个来源的探索性真实研究，不支持显著性、正式榜分、跨来源泛化/方法原创性结论。无完整资源监督和既有私有推理管线可安全调用时停止，不以“READY”掩盖不可运行的条件。此前已完成023和TRAIN-PREP等不可再运行。只有公开两份可选新的024代码、一份匿名024回执及codex-results的一条结果可变更，个人来源/路径/UID/QA/gold/原始日志/媒体哈希不得上传。

GPU训练任务 VLM-HOURVIDEO-TRAIN-GPU-001 **仍独立HOLD**。024仅零训练的有限模型推理。持续 NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。
