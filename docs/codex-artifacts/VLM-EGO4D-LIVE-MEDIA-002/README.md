# VLM-EGO4D-LIVE-MEDIA-002｜首次一段真实canonical长视频的严格限量获取（候选已排队，非READY）

**2026-10-13｜QUEUED / REQUIRES_NEW_MEDIA_GET_AUTHORIZATION。** 用户希望尽快进入正式实验；本文件预先把视频获取合同写好，**当前不批准任何媒体GET、Range或下载**，不能执行，也不能继承已结案MEDIA-001的2视频/8GiB额度。只有上游当前唯一READY的[慢速完整清单META-006](../VLM-EGO4D-AWS-META-006/README.md)提交被ChatGPT核验并明确出现一个真实合法候选且安全硬门可实现、用户**另行明确批准**本合同的视频字节/次数后，才可以在看板上使本ID**成为唯一READY**。启动仍由用户在原同一Codex长会话发新指令；META-006仍是当前唯一READY，不得因为看到本README同时跑媒体。

## 直接接续META-006的资格

1. 只有从**官方同一版本`v2_1/full_scale`清单真实`video_uid`→合法canonical对象映射**和同一UID的HourVideo`dev_v1.0_annotations.json`顶层候选，才允许进一步考察。媒体必须是真正原始full_scale长视频（非clip/540ss/镜像/Charades），本地标注声明时长≥20min且该UID至少2个合格开发QA（答案仅用于评分），优先≥30min。**当前UID命中/版本对应/对象长度均UNKNOWN，不得假造**。即使在v2_1清单匹配UID，也**不证明HourVideo dev_v1.0与Ego4D v2_1视频裁剪/起点/PTS同钟**；下载后的技术验收只能先标`MEDIA_PROVENANCE_CANDIDATE`，若不能验证时间轴/发行桥接，不得计算“HourVideo正式准确率”。
2. 仅用本机已有的命名`ego4d`静态AWS凭据和已安装的`boto3`私有工具venv。选择**一段**，来源/region已由META-006真实官方HEAD认证，`ContentLength`已知且`0<L≤3,758,096,384 B`（3.5GiB，保留安全余量），ETag/VersionId等可靠身份绑定与前次HEAD一致；媒体源bucket在Ego4D官方贡献桶白名单，URL/key完整身份仅私人内存/执行私有资产，不提交Git。不能用S3默认全球端点猜区域或默认profile，不能在本轮扫其他UID/区域挑对象。磁盘私人目标目录可用≥对象大小+2GiB空间，不在Git checkout、原实验树、旧缓存/ledger/Charades数据树内。**无这些条件即`MEDIA_PREFLIGHT_HOLD`并0媒体GET**。
3. 绝不触碰AWS密钥/Session Token内容、HourVideo原JSON完整答案/UID/signed URL、Git或聊天中的源数据。只允许本轮新创建的一个私人下载目录和一次性持久不可抵消的计数账本；不覆写/迁移用户旧文件。不安装包、不登录/配置、不触碰`pytorch`或任何GPU模型。任何未经书面准许的默认CLI批量获取、多线程`download_file`/TransferManager、region重定向、自动重试、第三方中转或其它媒体源均禁止。

## 冻结的首段下载上限（仅待将来另行明确授权）

- **官方媒体GET最多1次，最多1个对象；没有隐藏重试或恢复GET，任何网络失败立即停止。** 单对象最多3.5GiB。**本任务所有研究数据GET响应正文累计硬上限4GiB = 4,294,967,296B**（包括媒体/任何错误GET正文，且不将META-006的独立清单GET重复计算到此父任务）；元数据GET新额度为0。保守地在请求前预扣该对象可能传输的全部上界，必须在同一个私有持久账本`STARTED`写盘`fsync`后才发送；只允许同一可信region+HTTPS+固定bucket/key+条件ETag/VersionId+不变ContentLength。`retries={'mode':'standard','total_max_attempts':1}`，禁止自动区域重定向、Range/206、额外对象/HTTP或后台下载。服务器ContentLength未知/不同、ContentEncoding变化、数据首包签名/版本不一致、断链或unexpected redirected response都STOP，**不能重新GET续传**。
- 在调用网络GET之前，Codex必须通过受控客户端证明确切的**HTTP发送尝试数和累计接收/错误正文/重试的上界**可硬限制（超长接收fail-close，未读取缓冲/wire流量无法认证则`LIVE_TRANSFER_ENFORCEMENT_HOLD`并**0媒体GET**）。S3单对象HEAD声明≤3.5GiB与GET单次字节封顶4GiB不是网络计费全流量的形式化证明；不把本地文件大小或SDK读取块数冒充真实wire总字节。不扩大额度、不改试第二个候选补偿失败。
- 流写仅到本任务专用私有`.part`文件，逐块核写入/应用读取字节数与预扣，完成后核实际磁盘文件字节=HEAD值、前后对象标识一致且总额内，再以原子rename确认为本任务拥有的唯一媒体文件。可使用**已有**`ffprobe`做CPU容器/时长/PTS非像素检查，若无工具则报告`TIMEBASE_NOT_VERIFIED`，绝不下载/安装ffmpeg、抽帧、上GPU。没有真实Timebase/时长证据，不能强制判QA正式可评分。
- 未到手时`0`真实媒体，成功只允许`ONE_OFFICIAL_MEDIA_ACQUIRED_METADATA_ONLY`，不自动进入下一阶段GPU。实际新文件/账户/视频/私有路径/UID/帧/标注/许可证绝不可提交Git。**用户Ego4D批准至2026-10-26；最迟2026-10-25 23:59北京时间完成请求启始，否则STOP。**

## 交付/接力

只允许公共repo新`docs/codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/one-video-receipt.md`和`docs/codex-results.md`末尾唯一`### VLM-EGO4D-LIVE-MEDIA-002`一条，报告匿名总量：授权资格/1次或0次媒体GET、最大预扣和实际可核应用字节、落盘体量区间、成功完整性/声明时长/Timebase已证与否、无效字节/超额/停止状态、无GPU。不得报告真实UID/对象URI/ETag或上传私有文件、QA/答案/密钥；旧结果不能更改。一次正常main push后STOP，等待ChatGPT对下一[真实GPU A/B试验计划](../VLM-HOURVIDEO-LIVE-AB-001/README.md)验收/单独批准。GPU预算不随媒体下载许可自动产生。历史HourVideo50视频1182QA属既有标注审计，`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`保持。
