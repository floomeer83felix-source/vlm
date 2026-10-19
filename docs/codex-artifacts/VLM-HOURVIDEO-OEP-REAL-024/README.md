# VLM-HOURVIDEO-OEP-REAL-024｜未见HourVideo真实OEP零训练推理试点

**2026-10-19：QUEUED / NEEDS_NEW_EXPLICIT_MEDIA_QA_GPU_AUTHORIZATION / NON_READY。当前禁止执行。**

ChatGPT已完成新真实科学试点的完整设计，详见 [冻结协议](../../research-protocols/real-oep-pilot-2026-10-19.md)。不创建重复合成toy、CPU资产预检或原009电影自监督训练。023仅证明纯合成规则逻辑正确，未证明问答提升。

**此README目前不是Codex执行授权。** 必须用户单独明确批准：至多2个新HourVideo/Ego4D视频录制source-groups、各最多24条nongold问答和这批题的最终独立CPU-only gold评分、至多2个媒体源的官方有限读取/必要下载(总≤28GiB；每源≤14GiB)、私有新增素材/缓存总≤32GiB，以及RTX3090至多25累计GPU分钟/≤240次Qwen QA generate、CPU媒体阶段≤900s/父执行≤3600s、峰allocated≤18GiB。不能由本README或“继续”推定批准。

用户授权后，ChatGPT必须先更新本README状态和docs/next-steps.md，把本任务改为唯一READY，用户再在活跃Codex私聊发一次执行指令。届时父任务一次串行完成：

1. 独立docs checkout安全main fast-forward、读AGENTS/next-steps/codex-results及当前合同，检查024唯一READY且没有024结果。旧实验Git/ledger不得重置、覆盖。
2. 严格仅用用户新授权的nongold source-group/题文证据选2条物理独立且从未在R1–R6用过的来源，冻结≤48条QA及确定性双事件语法识别，不看gold。如少于12个显式双事件题，GPU0并报告真实试点不适用，不为凑数放宽。
3. 仅从两条固定授权真实媒体精确条目/官方Ego4D源获取合法视频，执行有限校验与PTS/资源门，不扫描其他文件或替代源。既有验证文件优先；下载上限见冻结协议，HTTP预算和持久匿名ledger必须严格监督。
4. 冻结同48候选/12帧真实Qwen+SigLIP管线对比五臂Uniform12、GlobalTop12、12bin、unordered、OEP_RANK_REAL_024；真实rank百分位只代表打分排名，不是023 synthetic阈值的可校准证据。所有事件词仅来自nongold题文、禁止用选项/gold/参考时间推断AB真值。限时限显存、异常即STOP，不重试失败/提升额度/训练。
5. 全部GPU及模型子进程退出、队列日志稳定后唯一CPU scorer才可在限定本轮新QA范围打开gold一次，保留full denominator及匿名paired结果。结果不等于hourvideo正式榜单或论文创新。
6. 一次性完成真实执行所需的最小代码集成：允许新增通用公共原型 prototypes/hourvideo_oep_real_024.py，以及配套纯合成接口/安全门测试 prototypes/test_hourvideo_oep_real_024.py（两者都只存公共算法/输入接口、不可带任何个人实际路径、ID、访问凭据或原始答案；不能改旧017/018/019/023源码）。经未来明确新媒体/GPU授权后，在本父任务安全CPU门通过的前提下直接复用既有Qwen/SigLIP及023 selector，必要时由上述新runner执行零训练前向。若runner无法安全调用现有私有推理组件或缺权重时报告HOLD，不临时安装/迁移环境。公开main总共**最多4处**：以上可选的2个新Python文件、唯一匿名 docs/codex-artifacts/VLM-HOURVIDEO-OEP-REAL-024/real-oep-pilot-receipt.md、codex-results.md末尾完整父任务条目。允许的额外纯合成接口测试计入同一父墙钟，不另下一个toy任务；不得把测试PASS当QA提升。不得上传私人媒体路径/片名、UID/QA/gold/来源映射/hash、模型权重、预测逐条或原始日志。一次常规安全push后STOP。

GPU训练任务 VLM-HOURVIDEO-TRAIN-GPU-001 **仍独立HOLD**。024仅零训练的有限模型推理。持续 NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。
