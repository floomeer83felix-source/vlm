# VLM-LIVE-VIDEO-GPU-START-001｜单轮真实视频获取＋RTX3090真实梯度训练技术试跑（唯一父任务包）

**2026-10-14｜USER_REQUESTED_IMMEDIATE_EXPERIMENT / READY（唯一READY，限定本合同；非无限GPU/云请求许可）。**

## 为什么不再做META/合成轮

[3ef8559](https://github.com/floomeer83felix-source/vlm/commit/3ef855983c879ac34852ff9382ed57620409fd85)已将LIVE-MEDIA-002按其当时合同安全结案：S3请求0/8、视频GET0、视频0、GPU0，实际卡在`LIVE_TRANSFER_ENFORCEMENT_HOLD`——现有SDK只验证应用层read，不能以其证明全部TLS/socket缓冲与网卡wire计费字节都被精确控制。**这不是网络拒绝或视频不合规，也不允许重跑旧002**。用户连续要求“不要每次问我”且本轮明确“快点开始实验”；之前明确同意限于**一段≤3.5GiB的合法原视频**、最多8次S3 metadata+媒体HTTP、清单≤8MiB、媒体响应正文累计≤4GiB。本新父任务包只延续这**同一尚未实际获取的唯一视频目标**、使用全新独立fsync计数账本与≤8次同等上限；绝不把旧002的0/8重新编号冒称残余可用、增加第二个视频或总数据下载。它额外以用户“开始实验”的明确要求批准**单次有上限RTX3090本地GPU技术训练试跑**：≤100次optimizer steps、GPU总累计≤20分钟，零外部模型服务/新权重/付费GPU。**必须用户在原同一Codex长期聊天新发执行消息**；GitHub任务更新不会自动唤醒本机。若因预算、环境、训练使用许可或完整性门停止，诚实STOP，不后台轮询/重跑。

本包的两个顺序子任务为 **A：真实单视频获取（优先）→ B：真实GPU训练技术验证**。严格只有一个READY父任务包；A合格且私人视频到手后，**可以同一轮直接进行B而不再请求“是否开始训练”**。若A失败，B只有在已明确提供过确切入口且有合法训练许可的**另一份真实本地视频**可证明时才能进行；不得凭猜路径、扫盘、用合成数据、用HourVideo QA/答案或旧Charades违规媒体补足。只向公共Git汇报一次匿名父任务包结果，末尾一条，不自触发后续任务。用户指令不是扩大任何尚未列明的授权。

## A. 官方唯一来源与真实限量下载：实用可核的传输合同

1. 固定先前[META-007匿名实测](../VLM-EGO4D-AWS-META-007/canonical-source-classification-receipt.md)及[官方源码固定版本](https://github.com/facebookresearch/Ego4d/tree/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb)：官方manifest唯一`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`；用户授权的一个私人`dev_v1.0_annotations.json`（非链接正规文件≤16MiB，解析顶层50 UID/时长及开发QA**数量**，答案/QA原文不参与挑选）；同一`ego4d`静态AWS profile及现有独立boto3。不得另翻release、推测媒体key、改AWS凭据/环境、访问非白名单桶、扫描全盘、下载模型、Charades或其它媒体。
2. 每次真实HTTP发送前钩子验证method、TLS官方AWS商业区域region-specific host、源bucket/key、阶段、最大尝试数，**每个S3 wire attempt无秘密fsync记录**，进程串行、`connect_timeout=5`、`read_timeout=90`、`total_max_attempts=1`、pool=1、禁代理、TLS验证、不自动重定向或区域二次请求；错误也消耗尝试数，禁止LIST/STS/Range/206/恢复/multipart TransferManager/隐式重试。许可截止北京时间2026-10-25 23:59，若剩余墙钟不足安全完成，不发请求。
3. **整个新父任务仅最多8次S3 HTTP尝试**，严格A manifest桶HeadBucket≤1；B regional manifest HeadObject≤1；C同对象ETag/VersionId身份锁完整条件GetObject≤1（应用完整CSV正文≤8,388,608B、与HEAD完全相符、无压缩）；D从固定官方贡献者桶对最多两个不同候选bucket HeadBucket≤2；E不同canonical对象HeadObject≤2；F从两者中唯一满足≤3.5GiB对象条件媒体GetObject≤1。候选UID/来源白名单筛选及排序**完全复现META-007**：50顶层UID唯一匹配、45合规/5隔离、均≥20分钟与≥2QA数量，优先≥30分钟其次UID SHA256稳定排序；不按视频大小替换第三个候选，需复现前两个HEAD200、身份字段与`一段≤3.5GiB、另一段>4GiB、合计12,897,682,214B`；偏差即STOP、0媒体GET。
4. **对用户已批准的“正文预算”采用可实现的可核规则**：视频HeadObject`0<ContentLength≤3,758,096,384B`（3.5GiB）；媒体**HTTP响应应用正文**本轮总读取≤4,294,967,296B（4GiB），所有GET在发出前预先保守`fsync STARTED`消耗对象HEAD声明完整长度，即便失败也不退还；HTTP正确ContentLength/无ContentEncoding变化/无Range且GET与HEAD ETag或VersionId一致，受控同步逐块read、校验计数并以≤4GiB强制拒绝超量应用读取；私人磁盘空余≥媒体对象长度+2GiB；写入本任务新专用私有`.part`，完整字节数=新HEAD大小才atomic rename，不覆盖任何旧文件或锁。传输异常、短读、超量、对象身份/容器不一致即STOP，**不得尝试第二个GET或从部分文件续传**。
5. **明确更正此前不可执行的附加门**：在此任务中“≤4GiB”指**S3媒体GET响应应用body字节预算**，不宣称完整网卡/TLS/socket/wire字节精确≤4GiB。正常HTTPS/TLS包头与SDK缓冲不算研究body，实际wire流量通常大于body且**目前不可精确认证其总字节**。**这是公开、明确的预算语义，不能伪称实现了物理wire流量严格封顶；网络流量可能超过4GiB，总AWS费用亦非数学保证。** 以ContentLength事前资格、HTTP单次GET、关闭重试、逐响应正文byte计数及stream早停来约束可控应用/对象大小，不要求为控制TLS层实现自制网络驱动。若用户或实际提供者条款要求**网卡总wire字节硬上限**，必须`NETWORK_WIRE_HARD_CAP_REQUIRED_HOLD`并0媒体GET；绝不假称该硬上限已实现。仍应保证真实HTTP发送次数可审计，不可因Socket额外请求突破总8次。
6. 只使用已存在的`ffprobe`做CPU容器/声明时长/PTS基础检测（若存在），不得安装工具。HourVideo dev-v1.0↔Ego4D v2_1同版/剪辑起点/PTS桥接无独立证据时`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`；**不把这个视频算正式QA评测，不输出官方准确率**。本包用于技术训练的此段视频**永久从后续正式held-out HourVideo QA评测候选中排除**，防止训练曝光与之后评分污染。只要合法使用授权不含训练用途，B必须HOLD而不得自动据AWS访问许可推断可训练。阶段A总墙钟≤75分钟，遇所有拦截条件立即STOP。

## B. 真正的RTX3090梯度训练技术试跑（一次，非正式Qwen微调）

前提：A得到完整可读取、许可允许本地研究训练的真人第一视角视频且CPU能用现成解码工具，从Windows现有`pytorch`环境**非破坏性验证torch CUDA可用/RTX3090真实CUDA张量分配**；原GPU上无其它冲突任务、不会杀进程/解锁/改CUDA或conda、不安装或联网下载包。若本机已有SigLIP视觉编码器与处理器的**确切本地入口**且能安全加载，则优先只读冻结特征提取；否则可用现成CPU解码工具仅从**真实视频帧**提取确定性RGB均值/直方图/低分辨率特征后在GPU训练小型时序次序预测head；不允许换成全合成帧冒充真实训练。Qwen3-VL本机权重若未知不强求GPU载入，不因此卡住时序head的训练试跑。本任务不读取HourVideo QA文本/选项/答案进行训练/挑checkpoint/选择seed，**不是Qwen3-VL微调或论文定量结果**。

- 只针对当前新下载的**一个实际视频**做本机低成本的时间顺序二分类自监督头任务：冻结的CPU特征来源（或本机已存在、冻结的视觉模型）不更新参数，head≤2层/可训练参数≤100,000，AdamW固定seed，一次run，**≤100个真实`loss.backward(); optimizer.step()`更新，GPU总累计≤20分钟（包括特征/训练的GPU时间），峰值显存监控**。CPU从视频按物理PTS最多抽256帧、仅少量低分辨率帧进入私人内存；训练/validation按时间连续块分离并保留缓冲时间，不按QA/答案选帧，验证不作官方基准。批量≤8、无新的远程数据/权重下载，checkpoint≤64MiB且只在本任务私人目录内可选保存一次；私人临时总新增≤512MiB（不含A已计的视频）。
- **科学资格说明**：同一video的时间窗拆分并不构成独立视频级held-out，且该视频原属于HourVideo dev候选；只能得`REAL_VIDEO_GPU_TRAINING_TECH_SMOKE`，不得报告正式长视频QA性能、独立评测、论文新机制PASS或泛化。真实执行了GPU的forward/backward/optimizer.step、更新可训练参数且loss有限才可用此名；仅GPU探测/合成数据训练不能称之。若没有可读真实帧、合法训练用途、torch CUDA不可用、软件接口不存在或任何OOM/NaN/冲突，记录`GPU_TRAIN_SMOKE_HOLD_<stage>`，**不安装新包、不增GPU预算、不重试训练**。
- 本包不会触发原`LIVE-AB-001`≤4次Qwen推理或`TRAIN-GPU-001`正式独立素材≤200步合同。后续真正科学A/B与独立训练集需先满足各自已经冻结的证据门，不能用此smoke冒充这些任务完成。**避免以快速工程训练代替高质量研究**。

## 一次公有脱敏交付与停止

只允许新增`docs/codex-artifacts/VLM-LIVE-VIDEO-GPU-START-001/real-video-gpu-start-receipt.md`和在`docs/codex-results.md`末尾追加唯一`### VLM-LIVE-VIDEO-GPU-START-001`一次父任务结果；不能改ChatGPT-owned看板、AGENTS、旧结果、旧工具/代码、原实验树、账本或私有资产。报告子阶段A–F真实尝试数、manifest完整性/45合规和2个HEAD与可取得唯一视频、媒体GET≤1及真实应用body字节/完成与否、下载和ffprobe情况；B实际CUDA是否可用、是否真实视频帧、optimizer steps、GPU分钟、head参数变化、loss有限、峰值VRAM、未证训练/评测时轴分割，STOP原因。所有真实UID、S3源URI/key/region/ETag、私人绝对路径、受保护QA/答案、视频/帧/特征、模型权重/ckpt、执行脚本与秘密日志不得公有上传。一次正常main push即STOP、原Codex聊天保留。权限并不自动赋予后续第二视频、Qwen训练或背景自主续跑。
