# VLM-EGO4D-AWS-META-006｜已认证官方清单的单次慢速读取与最多两段视频HEAD

**2026-10-14｜USER_APPROVED / 唯一READY（仅限本合同的有界metadata访问）**。用户在ChatGPT收到META-006的明确方案后回复「同意」，批准**新独立一轮**最多7次固定官方S3 HTTP元数据尝试、同一官方manifest最多1次条件GET且应用正文≤8MiB、read_timeout=90秒、最多2个canonical视频HEAD；媒体GET/GPU均为0。ChatGPT已据此将本ID设为**唯一READY**；须用户在**原同一Codex长期会话新发启动消息**才可执行。旧`VLM-EGO4D-AWS-META-005`已完成安全阻塞并结案，**不重跑005、不继承其余4个S3尝试或先前媒体2段8GiB限额**。本文件/排队不授权云请求、媒体或GPU。

## 本次只修复真正的阻塞

[上轮Codex 895f260](https://github.com/floomeer83felix-source/vlm/commit/895f2602cc4d27d4e5b38a1e3249ae386c1d2120)真实报告：用户本机新下载HourVideo`dev_v1.0_annotations.json`1,854,695B、50个顶层video UID/duration记录、开发结构PASS；现成`ego4d`命名静态AWS profile已可对**官方固定对象**签名。上轮`HeadBucket`可信`x-amz-bucket-region`区域提示PASS；region-correct `HeadObject` 200、官方manifest完整ContentLength **4,653,141B**、条件身份锁ETag可用；`GetObject` 200、长度/身份/无压缩PASS，但boto3 `read_timeout=12s`下应用读取2,555,904B后`ReadTimeoutError`。该GET**未成功取得完整清单**，不能解析partial或推断HourVideo真实UID映射/视频对象大小。当前唯一新工程原因是小CSV单次流读取超时；**不要再安装工具、运行合成实验或扫描其它版本**。

## 执行规则

1. 在公有Git独立checkout安全`fetch + fast-forward`、检查干净工作区、唯一READY恰为本ID且`docs/codex-results.md`不存在任何本ID旧回报。读`AGENTS.md`、本README、`docs/next-steps.md`、`docs/codex-results.md`及[上轮真实收据](../VLM-EGO4D-AWS-META-005/region-aware-limited-metadata-receipt.md)、[上轮区域合同](../VLM-EGO4D-AWS-META-005/README.md)，遵守全部来源/凭据/隐私门。只有此前用户已明确指定的一个私人Windows下载目录中的`dev_v1.0_annotations.json`可只读解析，要求普通非链接文件0<size≤16MiB、dev schema/顶层UID与有限正时长可核，QA/答案只可能随整体JSON技术解析进入私有RAM但不得参与选帧、映射、输出或Git；找不到文件即STOP，**0 S3**。严禁递归全盘扫描、上传私有JSON或其UID。
2. 复用唯一现成私人boto3工具venv和`ego4d`静态profile；SDK仅内部加载秘密签名，不手工读/列/输出/修改credentials、AWS profile、token、私有路径/账号。禁止`aws configure`、其它profile/默认账户、SSO/STS/IMDS/credential_process、额外官方Ego4D版本、其他数据源、镜像、Charades、依赖安装、旧研究环境/ledger/锁、GPU/Qwen/SigLIP、ffprobe/解码或视频下载。**用户已确认Ego4D许可截止2026-10-26；北京时间2026-10-25 23:59后不得发本轮新AWS请求。** 本轮前台总墙钟≤20分钟。
3. **唯一数据源**：官方Ego4D`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`，只对该桶与官方贡献者桶白名单做有限S3 metadata访问，不修改`v2_1`、不得用synthetic假媒体路径猜key。若前次私有区域信息无法经**同一AWS来源可信证据**在本轮重用，则按上轮A阶段对**固定官方manifest桶最多1次`HeadBucket`**读取经验证的`x-amz-bucket-region`；不信任301 Location第三方跳转，不把该区域提示当远端AUTH_OK。
4. **正式S3全部HTTP wire发送尝试总计≤7，包括4xx/超时/失败。** 完全沿用META-005 A–E白名单和顺序：A官方manifest桶`HeadBucket`≤1；B确认区域后对固定官方manifest`HeadObject`≤1、要求200且0<ContentLength≤8,388,608B、身份锁ETag/VersionId；C**只一次**同对象条件`GetObject`≤1，全文必须逐块读完且不超过8MiB、长度与HEAD完全一致、无压缩/Range/206；D经完整CSV与私有HourVideo顶层`video_uid`精确join后，仅≤2个官方贡献视频桶`HeadBucket`各1次；E最多2个不同真实canonical`full_scale`视频对象`HeadObject`各1次。总最多A1+B1+C1+D2+E2=7，**媒体GET/Range/LIST/STS全部0**。不为零匹配改查其他release，不根据`file_uid`猜`video_uid`，同一个真实UID多个canonical对象冲突即HOLD。匹配视频时长优先≥20分钟且≥2本机授权开发QA（只能在完成合法对应且用户已许可范围内做最小题数过滤，绝对不读答案值作为选择依据），尽量有≥30分钟。只记录总命中数、≤2对象HEAD长度是否≤4GiB和合计≤8GiB，**仍不证明dev_v1.0媒体与v2_1音视频PTS/剪辑起点一致**。
5. **唯一本轮参数变化：将manifest小CSV单次流的`read_timeout`由12秒提升到**90秒**，`connect_timeout=5`、`retries={'mode':'standard','total_max_attempts':1}`、`max_pool_connections=1`；若无内建完整线程级限时，必须实现程序级总墙钟≤20分钟的保守停机门。**失败绝不重试任何GET、补发Range/206、自动切区域或继续解析partial清单，不在本ID新run重置计数。GET前静态验证HTTP方法/HTTPS官方AWS商业区域/固定bucket-key/阶段计数、逐wire attempt持久无秘密fsync计数和不使用代理/TLS禁验；发现隐藏botocore重试、区域自动发现、302/301跳转或不能确保请求上限，网络前或出现异常后STOP。SDK/TLS已收未read字节难以精确计数，不可把应用实际读字节冒充网络wire计费字节硬证。**
6. 如GET完整，**必须在同一任务**解析官方CSV、只在私有RAM与真实HourVideo 50视频UID做严格等值join、确认官方`canonical_s3_location`/来源贡献桶白名单与真实对象类型，无冲突才最多执行2个媒体HEAD；成功只代表实际UID候选、对象元数据和大小，不自动认证HourVideo发布/时间轴。真实`v2_1`零匹配要如实报告零（只有成功完整解析才可写0），禁止切`v1`或给测试答案编造实际映射。任一失败立即报告真实`SAFE_METADATA_STOP / <具体阶段>`，不得超额、重试或前往下游视频GET/GPU。

## 唯一两处公有交付（正常向main一次push即STOP）

1. 新`docs/codex-artifacts/VLM-EGO4D-AWS-META-006/long-timeout-metadata-receipt.md`：匿名实际CSV对象HEAD/GET状态、完整GET应用字节/声明长度、读超时或成功、S3按A–E阶段实际HTTP发送数≤7、精确UID交集**聚合计数**（如完整CSV读取成功）、0–2媒体HEAD与单个≤4GiB/合计≤8GiB的PASS/HOLD；区分`AUTH_OK`仅当前manifest/贡献桶实际响应、`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`、`MEDIA_GET_NOT_AUTHORIZED`，确认0媒体GET、0GPU。未执行阶段`NOT_RUN`不能说零匹配或已知视频大小。
2. `docs/codex-results.md`**末尾只新增一条**`### VLM-EGO4D-AWS-META-006`，链接唯一收据与真实结论。不得改旧结果、任务看板/总览/本README/任何代码；不得上传真实UID、原始manifest/JSON/问答/答案、区域字符串/媒体桶-key、ETag/URL、AWS账户/密钥、安装资产或私人临时脚本。

如果这次完整CSV及至少一个canonical媒体HEAD大小通过，**立即停止并交给ChatGPT依据已预排[MEDIA-002](../VLM-EGO4D-LIVE-MEDIA-002/README.md)申请新的单视频≤3.5GiB/一次媒体GET正文≤4GiB许可**；该媒体与[RTX3090小样本AB-001](../VLM-HOURVIDEO-LIVE-AB-001/README.md)均仍QUEUED，媒体GET/GPU未获授权，不可自动继续。科学`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`维持。
