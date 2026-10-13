# VLM-EGO4D-AWS-META-003｜已纠正credentials文件名、核实[ego4d]节后的有限真实元数据实测

**2026-10-13 北京时间，唯一READY父任务；用户回复“True”，即在原Windows PowerShell中逐行检查标准`~/.aws/credentials`有名为`[ego4d]`的节。** 上两次`VLM-EGO4D-AWS-META-001/-002`皆已各自按`ProfileNotFound`、真实AWS请求0安全结案，**绝不能重跑其ID**。前一次失败原因已具体定位为记事本把`credentials`误存为`credentials.txt`，用户已更名为无后缀`credentials`，且采用`Select-String -Quiet`逐行核对`[ego4d]`得到True；此前`[regex]::IsMatch`结果False可能是Windows CRLF换行影响，**不可再据该错误正则判断profile缺失**。但名字/节存在**不等于密钥有效或S3权限PASS**。用户的研究目标是尽快取得真实合法视频，不要再运行合成测试、安装工具或额外研究规划。

## 一、一次性执行门及范围

1. 由用户在**原同一个Codex长期会话**主动触发。独立公有Git checkout `git status --short`干净、`git fetch origin main`安全fast-forward；重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本合同、[原META-002合同](../VLM-EGO4D-AWS-META-002/README.md)、[原META-001合同](../VLM-EGO4D-AWS-META-001/README.md)与[前次安全停止收据](../VLM-EGO4D-AWS-META-002/limited-aws-metadata-receipt.md)。**严格唯一READY=本ID、结果中无本ID旧回报**，否则STOP；不可reset/force、不修改旧父任务或账本。
2. 全部安全、隐私与来源限制继承原`META-001`合同，唯独**新的父任务ID、独立的最多4次S3 HTTP尝试预算以及用户已确证正确文件名和节名**不同。用户Ego4D官方批准确认至2026-10-26；为免时区歧义，**只可在2026-10-25北京时间23:59前发新研究请求**。CPU前台≤15分钟。复用已离线安装boto3的**单一专用私人Python venv**，不得安装/升级/更换依赖、创建第二环境、进入旧`pytorch`运行GPU、修改CUDA/旧实验树/Charades或任何历史运行账本。
3. **优先在同一Windows登录账户及标准Home下做真正boto3只读凭据提供器发现**：仅指定`Session(profile_name='ego4d')`及可信的静态共享凭据提供器，且其底层可按标准SDK约定读取配置用于签名。绝对**禁止人工cat/Get-Content/print/write/复制/枚举AWS credentials或Secret Key、Session Token、账户ID、环境变量、所有profile、邮件、私人Home路径**，不经Codex聊天/公有Git传递密钥或截图。禁止默认profile、其它用户账户、临时credential_process、SSO/IMDS/STS或不明自动刷新，不能使用`aws configure`、用户复制Access Key到命令行或以回显方式排错。可以通过标准SDK、**只输出布尔值**核对本次Windows进程视角的`~/.aws/credentials`文件是否存在、是否可识别`[ego4d]`，以及**是否为与用户刚才PowerShell相同的主机账户上下文**；如`ProfileNotFound`反复出现，报告`EXECUTION_CONTEXT_OR_AWS_PATH_HOLD`和这几个无敏感布尔事实，**同轮不换配置路径/账户补试，也不启动S3**。如profile可用但密钥空/无效，报告阶段与安全异常类别，不能输出凭据值。用户确认节名=前置条件，不直接记为`AUTH_OK`。
4. 用户之前明确授权的**唯一私人HourVideo`dev_v1.0_annotations.json`**仅在本机已有精确路径、该路径可由原授权资料直接解析时，读取顶层视频UID及`video_metadata.duration_in_seconds`建立RAM临时候选表。由于解析整个JSON实际会读取包含问答的文件字节，必须保证**不使用、不输出、不向Git提交任何QA、答案或真实UID明细**；没有明确路径就`LOCAL_UID_SOURCE_HOLD`并在首个S3请求前STOP。严禁扫描Downloads/用户目录寻找文件、猜版本或索要受限标注上传。

## 二、唯一官方数据源与请求硬门

**固定Ego4D官方发布`v2_1`的`full_scale`清单**，由[固定官方代码](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)指定：`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`。**全部实际HTTP尝试≤4，且是以下有序请求的上限：** 清单`HeadObject`≤1；仅若成功证实`0 < ContentLength ≤ 8,388,608 B`、S3 ETag/VersionId可绑定身份，才在同一对象`GetObject`≤1（条件`IfMatch` / version、正文实际应用读取≤8MiB）；完整解析仅此一份清单并与顶层本地UID等值join后，至多对**两个不同、无歧义、官方真实canonical原视频对象**各做`HeadObject`≤1。**媒体GetObject / Range=0、LIST=0、STS=0、额外manifest/ego4d.json/其它Ego4D版本/外部镜像/第三方请求=0**；失败后不得再次请求或自动换release。
- SDK一个S3 client串行执行，`botocore.config.Config(retries={'mode':'standard','total_max_attempts':1}, connect_timeout=5, read_timeout=12, max_pool_connections=1)`，不开多线程/TransferManager/`download_file`。需要可审计地在实际发送前拦截每次wire HTTP attempt，验证TLS、bucket/key/verb/次数和无隐藏重试、自动region重定向或未授权的凭据服务请求；无法约束就`REQUEST_BOUND_UNENFORCEABLE` STOP，不为跑通而关闭SSL或越权。请求不成功/权限403/404/签名校验错误等只记非敏感类名、发生阶段、请求数；不尝试额外STS身份检查。
- 真实S3媒体源绝非先前纯合成程序硬编码的`public/{release}/full_scale/{UID}.mp4`模板。以**真实CSV里的`video_uid`（非`file_uid`）**和`canonical_s3_location`/`s3_path`为准；仅接受原始full_scale视频、无歧义同一UID/对象、且媒体桶来自[官方贡献方bucket白名单](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)，拒绝不可信uri、缺字段、多对象映射、文件数据或clip。按顶层时长≥20min优先且尽量至少一个≥30min（如有），最多两媒体对象HEAD。若0匹配只报告`V2_1_UID_JOIN_ZERO`，**禁止改查v1/v2或更多视频数据集**。仅记录HEAD响应声明`ContentLength`、ETag/VersionId是否存在以及对象≤4GiB、两段声明总量≤8GiB的**聚合判断**，不下载一字节视频，也不私自调整下载上限。
- `IfMatch`/版本锁、无压缩、声明长度一致性、8MiB应用流上限不等于可核证线上所有wire字节上限；若实际预读取或异常无法严限，关流按合同停止并标`LIVE_BODY_BYTES_BOUND_UNKNOWN`。尤其真实官方UID相同**不证明HourVideo dev_v1.0问答的实际版本、剪辑/起点/PTS一致**；结论最多`UID_PRESENT_IN_V2_1`，`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`必须保留。

## 三、匿名输出与停止

可交付**恰好两处公有改动**，除此不改脚本、旧研究记录、看板、总览或旧README：
1. `docs/codex-artifacts/VLM-EGO4D-AWS-META-003/limited-aws-metadata-receipt.md`：只写安全汇总，包括本机Profile可发现/静态签名就绪与否、AUTH/权限状态、实际S3 request尝试≤4各类计数、HEAD已知manifest大小和实际应用GET总字节、v2_1 UID聚合匹配数、无歧义候选数、0/1/2媒体HEAD结果与≤4GiB/累计≤8GiB判断，真实release/PTS未知、0媒体GET/0GPU，以及本轮第一次实际阻塞与`NOT_RUN`。**不得公开任何真实UID、对象S3路径、账号、私人Windows目录/用户名、Access Key、Secret/Token、原始异常文本、完整ETag/VersionId或任何受保护QA/原清单字节**。
2. `docs/codex-results.md`末尾追加**唯一一条**`### VLM-EGO4D-AWS-META-003`引用收据与核心实际计数、远端是否真的AUTH_OK，不把0请求称为云端验证。

在公有文档checkout预提交核 `git diff --cached --name-only`**严格只有上述两路径**，本机私有脚本、临时CSV/UID或AWS身份不得push；一次正常Git main push后停止，保留原长期Codex会话等待ChatGPT验收和下一轮有界合法真实媒体下载独立授权。不得因用户催实验自动开始`GetObject`媒体或GPU。成功交付`META_PREFLIGHT_EVIDENCE / MEDIA_GET_NOT_AUTHORIZED`，或安全停止`SAFE_METADATA_STOP / <具体阻塞>`，**两者都不等于已取得真实视频或GPU实验结果**。HourVideo 50段/1182 QA仅原标注审计结论、科学`NOVELTY=RETAIN0`及Charades`FINAL_MEDIA_STOP`持续。
