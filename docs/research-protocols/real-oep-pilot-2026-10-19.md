# VLM-OEP 真实研究试点冻结协议（2026-10-19）

状态：ChatGPT 公开科研设计已完成；VLM-HOURVIDEO-OEP-REAL-024 等待用户单独批准新数据和GPU，当前不执行。

## 数据选择：为何转向真正的HourVideo新源

旧017/018在已观察开发样本上有SigLIP问题相关Top12优于Uniform12的探索性迹象，强制分bin没有一致优势。023双事件有序证据selector的31项纯合成测试通过，但未输入真实视觉特征、题目事件、Qwen答案或真实事件实例；synthetic tau=0.70不是SigLIP cosine的真实置信度。

主实验优先 HourVideo 官方 v1.0 dev 的尚未使用来源（50个20–120分钟级候选视频，1182题）。官方明确禁止基准进入训练语料。视频属于Ego4D来源，获取和使用另受Ego4D许可约束： https://github.com/keshik6/HourVideo 及 https://ego4d-data.org/docs/start-here/ 。不能由开源代码Apache许可推出视频训练或下载不限权。R1–R6已经看过，永远不作为024新盲测、阈值调优、模型挑选或最终独立test。

对比调研：Video-MME-Logical（EMNLP Findings 2026）官方 CC BY 4.0 数据集有375视频Mini、约352MB、120条中间状态题，适合作短时结构化时序逻辑诊断：https://huggingface.co/datasets/marcuskwan/video-mme-logical 。但其问题可能是按键、符号序列、状态追踪或要求reference image，未必包含两个可由题文明确拆分的事件，也不是一小时视频；不纳入024主长视频正确率或媒体额度。Video-MME-v2的多方视频版权更需独立许可，不自动获取：https://github.com/MME-Benchmarks/Video-MME-v2 。

## 024 单次零训练真实对照：冻结后待执行

A. 新素材和泄漏安全门：最多两条由已有授权nongold dev source-group元数据所指的全新HourVideo/Ego4D物理录制源，与R1–R6及彼此在真实拍摄/片段/剪辑来源组上独立。不能只靠不同UID证明。必须有真实适用的许可和精确官方素材入口；用户新批准前不得访问私人metadata、视频和QA。允许后的新媒体总HTTP正文上限28GiB（每条14GiB）、新私有媒体/缓存总32GiB；已有独立验证的本地同源文件优先，凭据、源URL、UID绝不公开。不合规立即STOP，无目录枚举、镜像或替代下载。

B. 不泄漏的样本门：先只用新获许可的nongold题文/任务类型、已获许可的非敏感来源分组，冻结白名单 Temporal Sequencing、Sequence Recall、Temporal Distance、Pre-requisites、Causal；从最多2个源各取最多24条，总最多48；确定性的题文before/after/then/earlier/later双事件拆分规则必须在读取答案之前固定，无选项/答案/参考时间或模型预测作事件提取输入。若可拆的双事件题少于12，直接NO_ELIGIBLE_TWO_EVENT_PILOT，GPU=0，不改变阈值/样本挑选或重跑旧题。

C. 五臂同条件：A Uniform12、B原SigLIP globalTop12、C旧48候选分12bin各top1、D unordered事件anchor、E OEP_RANK_REAL_024。每题同48个真实PTS候选，采样12个真实视频帧，同Qwen3-VL-4B、旧冻结prompt/seed19、do_sample=False及64 output tokens；顺序轮转，金标隔离，错误和未运行全入分母。事件子查询只来自固定无答案的文本规则，不能额外让LLM推测gold。SigLIP分别计算整题/事件A/事件B的cosine并统计额外文本embedding成本。真实分数按冻结的稳定rank百分位映射到单位域，再输入保留023逻辑的OEP有序pair机制；这是独立命名的rank代理而非校准证据概率，不得宣称synthetic tau0.70直接具备语义置信度。OEP失败必须原样fall back B，不取巧重选对照。

D. 一轮预算：最多240个Qwen QA generate、RTX3090实际GPU阶段累计最多25分钟（包括本轮加载/编码/前向）、Torch peak allocated不超过18GiB、CPU媒体解码/探测总不超过900秒、父单调墙钟不超过3600秒。官方媒体正文上限28GiB，每条14GiB，新私人媒体/临时文件上限32GiB。禁止安装或更新依赖、下载新的模型、外部云/API、训练/optimizer、自动提高预算或重复跑失败条目；如GPU资源/锁冲突立即停止，不终止他人进程。

E. 生成全部结束、账本冻结后，只有一个独立CPU scorer才能按新用户许可打开此次最多48条的gold一次。只能公开匿名每源correct/N、五臂差值、paired discordant cells、invalid/not_run、event可拆分/真实OEP回退比例、真实visual token与附加计算时延、GPU峰值和资源使用。未知的annotation-t0→PTS及正式源组身份维持UNKNOWN，不上传私有身份/原始题答/模型权重/帧/预测日志。

F. 不超过2源/48题只是非常有限的探索性pilot，不做统计显著性或泛化、官方HourVideo榜分、论文创新/强基线领先、真实OEP事件身份/真值声明。未来论文实验还需更多完全未见源组、至少AKS及可公平实现的GenS/2026时序方法、source级不确定性、完整event证据机制验证。如果效果为负、不能可用地拆事件或合法独立数据门不达标，停止扩大GPU，不再做重复合成任务。

科学标志继续 NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。

## 一次性实验授权（2026-10-19）与尚须现场通过的闸门

用户已看到此前明确说明的024上限并在本轮回复“批准”；**这只授权本任务一次真实未见来源的零训练研究试点**：2条新HourVideo/Ego4D录制来源组、每组≤24新非金标题/总≤48道及GPU生成后独立CPU scorer的本轮gold一次性评分，精确既有授权非保护source-group/版本元数据和合法固定两视频入口，官方必要HTTP传输总≤28GiB/每源≤14GiB、私有新增≤32GiB，RTX3090 GPU总≤25min/生成≤240/allocated峰≤18GiB、CPU媒体≤900s/父≤3600s。旧009/017/018及TRAIN-GPU-001额度和资产授权不继承；不训练、不装包/修CUDA、不下载模型或访问新无关媒体。

**唯一READY=VLM-HOURVIDEO-OEP-REAL-024，但GitHub变化并不会启动Codex。** Codex在收到用户活跃私人会话的新执行指令后首先必须查权利/凭据是否当下有效、精确source-group独立证据及≥12道确定性双事件问题；任何门不通过/UNKNOWN，必须在媒体下载和GPU之前保守停止并回报，不能因READY称资格已过，更不能从不同UID臆造物理独立或读旧答案。通过才一次完成真实五臂公平零训练推理，独立最后评分；任何变更预算、研究数据或正式训练都需新的用户明确授权。`NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、Charades`FINAL_MEDIA_STOP`。
