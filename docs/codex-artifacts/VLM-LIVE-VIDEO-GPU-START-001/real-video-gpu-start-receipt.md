# VIDEO-GPU-START-001：一次真实媒体GET未完成；执行器计时错误提前终止，GPU未运行

2026-10-14（北京时间）。**A：LIVE_MEDIA_SAFE_STOP / EXECUTOR_TIMEZONE_GUARD_ERROR；B：GPU_TRAIN_SMOKE_HOLD_A_INCOMPLETE**。本轮确实完成官方清单重建和两个媒体HEAD，并对唯一合格视频发出一次条件GET，响应200且部分正文已落盘。但外层计时器的时区转换错误使执行器在约53.975分钟提前终止自己拥有的下载进程；没有完整视频、没有GPU梯度更新。

**责任与因果明确：不是AWS权限拒绝、自然网络超时或实际达到75分钟上限。** 下载当时仍在传输，执行器错误是实际停止原因。不能根据此前慢速推断若未被终止必然失败或成功。合同禁止第二次媒体GET/续传，本轮因此不修复后重新下载，也不换成部分视频或未授权旧素材训练。

## 启动、合同与本地检查

独立公有docs原工作树干净，安全同步main `1bfc8df`，重读AGENTS、任务板、结果、总览、唯一父任务README及META-007收据，确认唯一READY且无旧回报。接受新合同把4GiB定义为媒体HTTP响应应用正文预算，不把网卡/TLS/socket wire流量或费用称为数学封顶；旧MEDIA-002和META父任务不重跑、不转移剩余额度。

只读同一授权入口的精确JSON，普通无链接/reparse文件1,854,695B，≤16MiB/dev结构PASS，50个顶层UID及有限正时长，读取前后SHA RAM一致。QA仅取数组长度，不用原文/选项/答案排序、训练或输出。SDK只内部加载ego4d静态共享签名，禁其它provider/default/环境账户/刷新/STS/IMDS；不手工读取或输出密钥，不修改AWS配置。唯一既有私人SDK环境复用。

新父任务独立私人目录及祖先无reparse，未与公有checkout或原研究树重合；目标part/完成文件原先不存在。实际目标HEAD后空闲空间≥声明长度+2GiB通过。新文件仅本任务拥有，不覆盖旧文件。初始执行标记、逐发送计数与媒体STARTED完整声明长度预扣均fsync，预扣失败不退款；另有新任务入口拒绝再次启动的静态保护，未对其进行新的真实请求测试。

## A–F：8次真实S3尝试，唯一媒体GET响应200但未完整

| 阶段 | HTTP尝试 | 实际结果 |
|---|---:|---|
| A manifest桶HeadBucket | 1 | 301，可信TLS区域头通过商业区名单检查；不跟Location |
| B regional manifest HeadObject | 1 | 200，声明4,653,141B及身份锁可用 |
| C 同对象条件GetObject | 1 | 200，完整读取4,653,141B，长度/身份/非压缩一致 |
| D 两个候选贡献桶HeadBucket | 2 | 301、301，可信区域发现通过 |
| E 两个canonical对象HeadObject | 2 | 200、200，正长度/身份字段可用，大小关系复现 |
| F 唯一合格对象条件媒体GetObject | 1 | 200，GET长度/ETag及如有VersionId/编码检查通过，部分正文写入后被本任务外层错误终止；完整成功0 |

总8/8：HeadBucket3、HeadObject3、GetObject2（清单1、媒体1）。无隐藏补发/重试、Range/206、LIST/STS、额外对象或发行版本。串行pool1、connect_timeout5/read_timeout90、total_max_attempts1、显式禁代理继承、正常TLS验证；逐实际发送前核精确method、官方host/region、bucket-key、阶段次数/总8及许可窗口，fsync匿名计数。

完整CSV与本地UID唯一交集50；互斥来源分类VALID_CANDIDATE45、BUCKET_NOT_IN_PINNED_OFFICIAL_LIST5，其余6类0。45个合规候选均满足声明≥20分钟及≥2题数组长度；优先≥30分钟，再UID SHA256稳定排序取原前两个不同对象，不根据HEAD结果更换第三段。5个隔离来源没有请求。

两个HEAD的大小关系复现：恰1段≤3.5GiB，另1段>4GiB，两个合计与META-007固定聚合相符；不公开单段精确大小或身份。唯一合格段在新HEAD后使用条件身份绑定GET，不能把合计一致替代当前GET身份锁。manifest访问与两个媒体HEAD/一个媒体GET200仅支持这些实际对象的响应权限，不推广到其它来源。

## 正文预算、部分文件和账本

| 项目 | 真实结果 |
|---|---|
| 媒体GET次数/完整成功数 | 1 / 0 |
| 目标HEAD声明资格 | 0<长度≤3.5GiB；预扣完整声明长度，≤4GiB |
| 最后持久应用read计数 | 位于64–128MiB区间；非最终完整精确计数 |
| 终止后部分文件逻辑大小 | 位于64–128MiB区间；仅part，未原子rename为完成视频 |
| RAM内最后读计数 | 强制终止后不可恢复；不能把文件大小或旧快照冒充最终精确应用/网络字节 |
| 最终完成视频 | 不存在；新完整视频0 |
| STARTED/请求预算 | 保留，不退款、不清零、不再次GET |
| ffprobe/容器/packet-PTS/真实帧解码 | 全部NOT_RUN；未对part开展处理 |

同步流每块≤1MiB，读前检查剩余声明长度和4GiB余量，返回后校验长度/累加/写盘；每16MiB flush/fsync及计数快照。未达到完整字节=新HEAD长度的终点，完整性和atomic rename门没有通过。应用计数是返回执行器的read字节；SDK未返回缓冲、TLS开销、网卡wire总量未精确计量。完整声明长度仍保守预扣，不能把此次部分传输当新任务自动可用剩余下载权限。

## 执行器错误：原记录保留并追加更正

为将75分钟阶段上限保守覆盖前检，外层使用本轮Git同步时间作为UTC锚点，并记录自己的下载进程身份。Windows私人SDK虚拟环境有解释器启动器和实际解释器两个同任务父子进程；最初按单进程判断发现两项，未终止，随后按精确脚本后缀、父子链、父监督入口与创建时间核实唯一实际工作进程。没有杀其它进程或操作旧GPU锁。

错误有两个相关的PowerShell日期类型处理点：ConvertFrom-Json把ISO日期解析为DateTime后，先与ISO字符串比较创建时间造成误报，安全拒绝终止；改为UTC ticks比对后确认身份。**但阶段锚点仍通过DateTimeOffset.Parse的隐式字符串转换处理DateTime，丢失UTC时区语义并按本地时区重解释，使经过时间多算约480分钟。** 这导致把实际约53.975分钟误判为超过外层阈值，错误提前停止唯一下载。

原错误停止事件及STARTED账本没有覆盖/删除；新增更正事件记录正确相对耗时与EXECUTOR_TIMEZONE_GUARD_ERROR，并向本任务追加式匿名账本写入终止记录，保留8次尝试和全长度预扣。已静态改为直接DateTimeOffset类型转换；没有再执行下载、没有第二次GET，也没有宣称这一修复已通过新真实任务验证。自己的下载解释器和启动器均已退出，私有监督器返回终止状态，不能当下载成功。

因此本轮约54分钟结束获取，未超75分钟，但**未按预期完成获取是执行器错误造成的任务失败**。网络确实偏慢，却未观察到自然ReadTimeoutError、HTTP拒绝或校验异常；不转嫁根因。

## B：未执行GPU训练，不伪报环境失败或成功

在准备阶段，仅现有pytorch环境的模块存在性检查确认torch、PyAV、OpenCV、NumPy接口入口存在，既存独立ffprobe文件存在；没有安装依赖/下载权重/更新Python、Torch、CUDA。CPU解码和GPU训练私人代码进行了AST语法检查并准备好，但**没有调用训练程序**。公开Ego4D[许可草案](https://ego4d-data.org/pdfs/Ego4D-Licenses-Draft.pdf)列明研究/开发/训练用途，本轮未查看私人签署文本；不能以AWS响应替代签署资格证明。A未完成已足够阻止B，未进一步冒充所有训练许可或运行时门已通过。

| B项目 | 本轮实际 |
|---|---|
| 真实帧抽取/特征 | 0 / NOT_RUN |
| GPU冲突查询/本任务GPU互斥锁 | NOT_RUN / 未取得；不操作旧锁 |
| torch CUDA可用性/实际CUDA张量分配 | NOT_RUN / 0次；不判断3090不兼容 |
| GPU forward/backward/optimizer.step | 0 / 0 / 0 |
| GPU训练分钟 | 0 |
| 可训练参数构建/参数变化/loss有限性 | NOT_RUN，不能把准备的代码当执行证据 |
| 峰值VRAM实测/验证分割 | NOT_RUN / NOT_RUN |
| checkpoint/Qwen/SigLIP运行 | 0 / 0 / 0 |

没有另一份已明确确切入口及合法训练用途的真实视频可证明，未扫描原研究树、下载目录或旧Charades，也未用合成帧、part、dev QA/答案补足B。新任务私人目标UID哈希的未来held-out排除标记已在GET前保守记录；不公开哈希/真实UID，也不将该标记称实际训练曝光证据。

## 唯一交付与停止

仅本收据及codex-results末尾一次父结果。无原JSON/CSV/UID/对象/桶region/ETag、私有路径/进程ID/精确时间戳、视频/帧/特征、权重/脚本/账本/原日志上传。原科研树、Conda/PATH/AWS配置、旧实验、旧工具/代码/ledger/锁不改；无新依赖、付费服务、云GPU、额外数据/模型、后台续跑或下游任务。

正常main push后STOP并保留聊天，交ChatGPT审查执行器计时错误和下一步有界恢复合同；不自行新增批次、重开本ID或退款额度。RELEASE_AND_CLOCK_BRIDGE_UNKNOWN、NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP保持。没有ONE_OFFICIAL_MEDIA_ACQUIRED_METADATA_ONLY或REAL_VIDEO_GPU_TRAINING_TECH_SMOKE成功结果。