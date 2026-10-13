# VLM-EGO4D-AWS-META-005｜固定官方对象的AWS区域探测＋真实清单＋2段canonical媒体HEAD

**2026-10-13｜用户已在ChatGPT明确回复「同意」：新批准本任务最多7次严格限定的真实S3 metadata HTTP attempts、唯一官方manifest GET应用正文≤8MiB、至多2视频HEAD、0媒体GET/GPU。** 这是本ID独立的新批准而非原任务剩余额度；**只有`docs/next-steps.md`显示本ID恰好唯一READY，且用户再在原同一Codex长期对话主动发送激活消息后方可执行**。本README提交和看板激活本身不表示Codex已开始S3访问。不得把先前父任务剩余请求/2段8GiB媒体下载预算迁移至本任务。旧`META-001/002/003/004`均已结案，不得重跑。

## 科学与工程依据

[Codex上一轮真实收据](../VLM-EGO4D-AWS-META-004/limited-aws-metadata-receipt.md)明确：当前用户提供的新下载目录内，HourVideo`dev_v1.0_annotations.json`唯一文件1,854,695B、完整JSON解析/结构/50顶层视频元数据/读取前后不变均PASS；本机隔离boto3的专用`ego4d`静态profile可加载；唯一向官方Ego4D`v2_1/full_scale/manifest.csv`全球S3 endpoint按us-east-1签名的HEAD得到**HTTP301**，请求后立即停止，无自动区域重定向/补试、实际S3共1次，CSV/媒体GET0、GPU0。301**不是**远端认证PASS、账户403或Ego4D用户审批被拒。AWS[官方HeadBucket API说明](https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadBucket.html)及[botocore HeadBucket文档](https://docs.aws.amazon.com/botocore/latest/reference/services/s3/client/head_bucket.html)表明：即使HeadBucket未获ListBucket权限，其响应头`x-amz-bucket-region`通常仍会指明桶的正确区域。**不猜测区域，不信任第三方镜像或301 Location作为新bucket/key授权**；如官方区域提示缺失/非允许AWS商业区区域即STOP。

## 1. 启动门/数据身份

1. 独立公有Git文档checkout须干净并fetch/fast-forward`main`，读`AGENTS.md`、看板、本合同、`docs/codex-results.md`、前[原META-004合同](../VLM-EGO4D-AWS-META-004/README.md)与其真实收据、[Ego4D官方manifest固定源码](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)和[官方贡献桶列表](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)。要求本ID**恰好唯一READY**、结果文件无本ID此前回报；否则不访问任何私人文件/AWS并STOP，禁止force/reset或重开旧父任务。
2. 用户在**私有Codex激活消息**提供上轮同一个HourVideo JSON所在的唯一Windows本地下载目录（**绝不写在公共Git**），Codex仅精确核该目录顶层`dev_v1.0_annotations.json`，若确无精确名才至多一次顶层`dev_v1.0_annotations*.json`唯一匹配。无其他目录递归搜索、已知旧Downloads路径、Windows账户扫描或改变原JSON。0<size≤16MiB、普通文件无reparse/symlink、dev结构/顶层UID和时长可读，直接只在私有RAM提取视频UID与时长；不分析/打印QA/答案、选项、canary、原JSON/完整uid列表，解析技术上读到QA字节必须说明不用于排序与输出。若本地输入未过门**0 AWS**。
3. 复用已经安装好boto3/botocore的**唯一私人隔离venv**、仅以标准共享配置的命名`ego4d` profile为AWS签名。SDK内部可访问凭据但脚本/终端不得手工读、复制、打印或更改密钥、Token、账户、配置，禁default/其它profile、credentials环境变量、SSO/STS/IMDS/credential_process/刷新链。不得安装工具、修改PATH、Conda`pytorch`/CUDA、原实验树/旧lock/ledger、HourVideo文件、旧Charades；无GPU、Qwen、SigLIP、视频像素或音频解码、ffprobe、训练。**CPU前台≤15分钟；仅2026-10-25北京时间23:59前允许新AWS数据请求**（用户确认Ego4D正式审批至2026-10-26）。
4. 官方manifest唯一白名单S3对象为`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`；release固定`v2_1`，不因无UID命中改查`v1/v2`、其它manifest/annotations、官方CLI批量下载或第三方桶。精确匹配本地真实顶层`video_uid`而不是`file_uid`，仅接受清单显式无冲突的canonical`full_scale`视频`canonical_s3_location`/`s3_path`，源桶在**官方源码固定贡献者bucket白名单**，key安全且不是剪辑/镜像。查原始时长优先≥20min且至少一个≥30min（有则）；最多2个不同UID与不同媒体对象。UID命中仅说明`UID_PRESENT_IN_V2_1`，`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`永远保留，不能冒充真实HourVideo问答的同视频时间轴/PTS已证。

## 2. 本轮已获用户批准、但仍需唯一READY及Codex主动启动的7次严格HTTP请求

须在发任何S3请求之前设计**单进程串行、逐HTTP attempt计数且持久记账**的white-list sender，禁HTTP redirect或botocore bucket-region自动重定向/隐式重试；`botocore.config.Config(retries={'mode':'standard','total_max_attempts':1},connect_timeout=5,read_timeout=12,max_pool_connections=1)`，每个实际wire发送前核`HTTPS`主机只在`amazonaws.com`相应商业区regional S3合法域内、请求方法和bucket/key恰好本阶段许可、总尝试仍≤7。若不能审计内部wire attempt或出现代理/TLS问题、未知region字符串/自动补发，就在再次发送前`REQUEST_BOUND_UNENFORCEABLE` STOP。不调用普通aws-cli或官方下载器、无`download_file`/TransferManager、多线程、缓存匿名迁移/恢复自动重试，不关闭TLS证书或接受301 Location未授权源。

阶段严格如下：
- **A. 首先**只对固定官方manifest bucket`ego4d-consortium-sharing`发**1次HeadBucket**（S3 HTTP HEAD，未得到200也允许在本机RAM从可信AWS TLS响应头`x-amz-bucket-region`读取region；如果400/403但官方区域头存在，**不当AUTH_DENIED或AUTH_OK**，仅可继续后续精确object HEAD）。此HEAD不读取任何清单/媒体正文，**不是ListObjects**。验证region语法为真实AWS商业区Region、不接受多义/非官方区/HTTP Location新对象、无区域提示即STOP。原上一轮HEAD的301区域头未记录，本次不推断/复制旧状态。按官方S3规范生成region-specific client/签名（无未授权跳转），不能直接把301目标host任意透传。
- **B. 对唯一官方manifest regional endpoint**做**1次`HeadObject`**，须200且`1≤ContentLength≤8,388,608`、有ETag或可靠VersionId可用于条件GET绑定；若401/403/404/301/400、不明大小或来源不确定STOP，不再改region/重新发HEAD。
- **C. 同一manifest**做**1次`GetObject`**，只读取其CSV，IfMatch/VersionId绑定B的对象并核完整长度和ContentEncoding非压缩及无Range/206，内存流式读**应用正文≤8MiB**，失败时关stream，**不能将应用已读字节误称全部socket/wire字节**；解析一次、绝不写公共Git/日志。唯一许可研究数据GET正文只此一份；其他所有GetObject/任何媒体GET禁止。
- **D. 仅当真实UID等值join及canonical媒体来源验证通过**，最多对**2个不同候选视频所在桶**分别发**0或1次HeadBucket**定位其正确region（若与A同一已知桶可复用区域而不发；若两个候选来自同一桶也只查一次）。若403带官方区域提示，可用于下一步，不擅自认身份被拒。任何不可信bucket/region/跳转提示STOP。
- **E. 对最多2个合规canonical媒体对象**各做**1次`HeadObject`**于D核实region-specific S3 endpoint；只获取`ContentLength`及ETag/VersionId是否存在，统计单段≤4GiB、全部候选累计≤8GiB。若大于旧额度报不合格，**不可扩大下载额度或尝试其它视频替代**，不读媒体内容/帧/音频。

**总计最坏**：A1+B1+C1+D≤2+E≤2 = **≤7个S3 HTTP尝试（含4xx/301/失败），且manifest GetObject≤1、其应用正文≤8MiB，媒体HeadObject≤2、HeadBucket≤3、HeadObject总≤3、S3 LIST/STS=0、媒体GET/Range=0、GPU=0**。若候选共用一个bucket，真实请求数更少。任何请求非预期响应、超时或跳转即STOP，不换其它Ego4D数据源/region猜测、不得在同一任务第二次“修复重跑”，不让中止后账户/脚本重置预算。GET请求失败正文与HTTP网络成本独立如实报告，不以0 application-byte宣称网卡wire全0。

## 3. 脱敏可验收结果与停机

公有Git**只能两处改动**：新增`docs/codex-artifacts/VLM-EGO4D-AWS-META-005/region-aware-limited-metadata-receipt.md`＋`docs/codex-results.md`末尾追加**恰好一条**`### VLM-EGO4D-AWS-META-005`。只能列用户已同意的固定**公有manifest桶/版本**、非敏感汇总如profile加载PASS、manifest bucket区域发现`PASS/FAIL`（**不要上传区域原文也可**）、A/B/C/D/E各实际HTTP尝试/响应阶段、GET应用读取字节数、真实dev顶层视频数、Ego4D`v2_1` UID join聚合数量、2个候选对象是否HEAD成功/大小≤4GiB与合计≤8GiB、未证媒体PTS桥接、媒体GET0、GPU0。**绝不上传原标注、QA/UID/qid、私人下载目录/账户、AWS Secret或AccessKey/Token、实际canonical媒体S3 URI/key/hash/ETag、响应签名/Header原文、底层trace或私人代码/临时manifest**。预提交核恰好2个allowlisted路径，正常向main push一次即STOP，保留同一Codex聊天待ChatGPT验收；结果无论`META_PREFLIGHT_EVIDENCE / MEDIA_GET_NOT_AUTHORIZED`或`SAFE_METADATA_STOP`都不自动放行后续视频下载、GPU或恢复已结案MEDIA父任务。任何媒体下载必须有用户**新明确允许对象数/单体和累计GET字节、持久hard accounting、精确官方对象和版本桥接**后的独立任务。HourVideo开发集50视频/1182QA上一阶段已验收、目前新JSON元数据50视频；本任务不复读答案，不冒充科学效果。`NOVELTY=RETAIN0`及Charades`FINAL_MEDIA_STOP`保持。
