# VLM-EGO4D-LIVE-TRAIN-MEDIA-001｜额外一段独立训练视频：来源/分割核验与一次限量获取

**2026-10-14｜QUEUED / 需新增数据获取明确授权，非READY。** 排在已排队的 LIVE-MEDIA-002（评测保留视频）及 LIVE-AB-001（训练前对照）之后。此项仅为把真实GPU训练所需的**独立训练视频**提前排好；不是新AWS请求或媒体下载许可。若上游实际不通过，则不可执行。每轮唯一READY规则、原Codex长会话新消息触发、一次匿名收据推送后STOP均遵守AGENTS.md。

## 输入与数据隔离门

- 先验收META-006的完整官方manifest/UID canonical 来源证据、LIVE-MEDIA-002的合法评测视频与时间轴门和AB-001的固定基线收据。训练视频必须是**不同官方video_uid / 不同物理对象 / 不重叠剪辑**，且属于已核准可用于训练的官方发布分割/授权；不能把HourVideo dev_v1.0的受保护QA/答案当成训练标签，也不能以仅不同UID就证明不同采集源。未知则`TRAIN_SPLIT_HOLD`，不得用评测视频凑训练集。
- 优先复用用户已经合法持有的另一份**明确授权训练**的本机媒体；无可证隔离训练源时申请单独一次官方canonical获取。若仅剩一个合法视频，本任务STOP，不为了凑训练数据重复使用开发/测试问答。
- 如果必须再次查询manifest/媒体元数据，需在获准后冻结**唯一官方v2_1/full_scale清单**：HeadBucket≤1、HeadObject≤1、条件GetObject≤1（应用正文≤8MiB）、训练候选贡献桶HeadBucket≤1、媒体HeadObject≤1，加上媒体GetObject≤1，合计**至多6个S3 HTTP wire尝试**；不能临时扩展为全量Ego4D、目录LIST、STS、其它release或新的候选扫库。沿用META-006身份锁、可信区域、单请求无重试、HTTPS和持久fsync尝试计数；任何预算控制不可信即0 GET并STOP。
- 严格**最多一段新视频**，媒体HEAD确认的ContentLength>0且≤3.5GiB（3,758,096,384B），单媒体GET≤1次、全任务媒体正文研究读取预算≤4GiB（4,294,967,296B）且真实流量不能可靠限额则STOP；不能Range/206/恢复、第二个视频、镜像、自动重试、转移既往额度。私人目录剩余≥对象长度+2GiB，无覆写旧文件/锁/账本/原科研树。CPU可用现有ffprobe只核时钟、不额外获取工具。Ego4D获批窗口按META-006合同，仅2026-10-25 23:59（北京时间）前发新AWS请求。
- 永不把真实UID、标注QA/答案、media、区域、桶key、URL、ETag、AWS账号/凭据、本机路径、提取帧或私有日志放进GitHub。原dev评测输入不用于选择训练标签、训练/早停或超参搜索。

## 交付与判据

- 若完成，匿名收据只能写**至少一个独立训练视频取得**、官方授权与非重叠的证据级别、声明/实读字节、请求数、PTS可用性及`TRAIN_VIDEO_ACQUIRED` / `TRAIN_SPLIT_HOLD` / `TRANSFER_HOLD`。此项不会自动证明有可监督问答训练集。
- 只新建`docs/codex-artifacts/VLM-EGO4D-LIVE-TRAIN-MEDIA-001/one-training-video-receipt.md`并在`docs/codex-results.md`末尾新增一个父任务条目。不得触碰看板、历史结果、模型、训练、GPU或开发QA。正常push一次STOP。下一站[TRAIN-PREP-001](../VLM-HOURVIDEO-TRAIN-PREP-001/README.md)，不得自动运行。
