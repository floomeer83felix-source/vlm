# VLM-EGO4D-AWS-META-004｜新下载HourVideo开发JSON精确接入，同轮完成有限官方S3元数据验证

**2026-10-13 北京时间｜用户已确认再次从获准HF官方页面下载HourVideo dev标注，且向ChatGPT指定了本机接收目录。本合同随唯一READY由用户在原Codex长会话显式激活，授权本轮仅有限真实metadata请求，不授权媒体GET或GPU。** 当前GitHub不保存用户私人完整本机路径或JSON/UID。执行时用户在**给Codex的私有激活消息**直接指定唯一下载目录，Codex不得向公有Git或脱敏回报透露该路径。旧`VLM-EGO4D-AWS-META-001/-002/-003`皆结案，尤其META-003已证`ego4d`静态profile本机加载PASS、但其旧标注路径不存在或未过体量门；**不重复旧任务ID**。用户希望立即开始实验：本轮应一次完成本地文件门＋最多4个限定S3 HTTP请求，不再单独安排合成测试/额外工具安装。

## 1. 同轮启动门与用户提供的私有输入

1. 用户于**原同一个长期Codex会话**发一条消息激活唯一READY；独立公有checkout须先`git status --short`干净、`git fetch origin main`并安全fast-forward，重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[上次META-003安全收据](../VLM-EGO4D-AWS-META-003/limited-aws-metadata-receipt.md)、[已验收真实标注结构的早期报告](../VLM-HOURVIDEO-DEV-001/local-annotation-eligibility.md)、[原AWS metadata技术合同](../VLM-EGO4D-AWS-META-001/README.md)、[上一轮源约束](../VLM-EGO4D-AWS-META-003/README.md)。必须唯一READY为`VLM-EGO4D-AWS-META-004`，且`docs/codex-results.md`无本ID旧结果；否则STOP、不reset/force、不激活其它已结案任务。
2. 用户在**私人Codex激活消息**给出**一个Windows绝对下载目录**。本轮只检查这个目录顶层，不使用旧Downloads路径、不递归、不检索磁盘其它目录或用户profile、不枚举浏览器记录。首先只查`dev_v1.0_annotations.json`这一**精确基础名**；如果确实不存在，允许唯一一次**顶层、只针对`dev_v1.0_annotations*.json`的有限文件名＋文件大小匹配**以容忍浏览器添加的` (1)`后缀；多个文件/零文件/目录重解析或链接/不是正规文件→`LOCAL_UID_SOURCE_HOLD`立即STOP。不能默默改读`dev_v1.0.json`、test或samples；若候选非单文件或用途不明，不随机选、不改名、不移动/复制。
3. 对唯一文件本机只读检查实际字节大小，**0 < size ≤ 16,777,216 B（16MiB）**、JSON可完整解析（只在RAM、不落盘），用已验收的`tools/hourvideo_dev_preflight.py`源码/旧审计结构**只读参考**（不要重跑QA资格工具或解析明文问答作为选样），抽取开发标注的**顶层`video_uid`及`video_metadata.duration_in_seconds`**和固定版本字段。完整JSON解析必然在内存见到QA数据，但**不得在候选选择、日志、日志异常、Git或命令行用题目/选项/答案/私有ID、canary**；不会对JSON做任何修改、重新下载或传输。验证有且仅有dev格式/非空UID且无冲突，若实际schema不兼容则`ANNOTATION_SCHEMA_HOLD` STOP。**早期50视频1182QA仅历史事实，本轮如果实际视频元数据数有变化只报匿名计数，不冒充新版本的50/1182已复算**。检查原文件字节前后不变，未打印路径/文件名编号/UID/QA。若文件>16MiB，先报实际大小区间`OVER_16MIB`而不擅自读大文件；切不可再次硬编码先前失败的3MiB复合门且不说明分项失败。
4. 只复用原有**同一私人隔离boto3 venv**；静态`ego4d`命名profile本机已由META-003确认能识别、可在本轮SDK内部为签名读取，但不等于远端AUTH_OK。不可手动打开/打印/复制AWS credentials、token、配置文件内容、账号、profile列表、私人用户名路径。不可访问默认/其它profile、credential_process、SSO、IMDS、STS或未知自动刷新；不能`aws configure`、安装AWS CLI/Ego4D CLI、换Conda/GPU环境或改AWS配置。若仍`ProfileNotFound`/空凭据/无法静态签名则`AUTH_PROFILE_HOLD`且AWS请求0；不绕开密钥要求。对系统代理、TLS或地区发现存在不确定时STOP，不禁证书、不打印错误原文。
5. **最长CPU前台15分钟；不晚于2026-10-25 23:59北京时间发新AWS请求**（官方访问用户确认至10月26日）。整轮**只有一次实际现场尝试**；失败不偷偷补查另一路径/另一release、不重跑本ID、不继续旧MEDIA/Charades/真实Qwen任务。

## 2. 固定S3来源及最多4次请求，一次查到真实UID和对象长度

**唯一允许的官方清单**由[Meta Ego4D固定官方源码](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)确定：
`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`。仅固定发布`v2_1`、集合`full_scale`，任何其它`v1`/`v2`、clip/540ss/annotations、`ego4d.json`、HF其他文件、第三方镜像均禁止请求。用户批准Ego4D直到2026-10-26，不证明当前AWS Key有效、S3权限或HourVideo`dev_v1.0`同版。

**严格顺序和新的本任务总上限：**
- (1) 对唯一官方manifest最多 **1次`HeadObject`**；需真实声明`0 < ContentLength ≤ 8,388,608 B`（8MiB）、ETag或VersionId可稳定绑定；否则STOP。
- (2) 同一对象最多 **1次`GetObject`**，用`IfMatch`或合法版本ID约束，校验响应`ContentLength`与未压缩内容一致、禁Range/206，**应用读取总字节≤8MiB**，任何大小未知/ETag突变/附加跳转/压缩不明STOP；不得用`download_file`、自动TransferManager、并行预取、重试来突破预算；只将清单在私有RAM解析，不写到Git或日志。
- (3) 清单全部校验并与本机已定位HourVideo**顶层真实UID做精确RAM等值join**后，仅接受`video_uid`且类型为canonical原视频、有无冲突`canonical_s3_location`/`s3_path`（不是`file_uid`、clip或测试合成程序的伪`public/{version}/full_scale/{UID}.mp4`），源bucket必须属于[Meta官方贡献者桶白名单](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)，key非空且无越界/非S3源。不确定即不HEAD。按声明时长≥20分钟、尽量有一项≥30分钟的固定排序最多选择**2个不同UID/不同canonical对象**，各最多**1次`HeadObject`**。真实HEAD只统计对象`ContentLength`、ETag/VersionId是否存在、单个≤4GiB/两段合计≤8GiB是否满足；绝不媒体GET/Range、像素或音视频帧/字幕下载。
- **所有实际S3 HTTP发起attempt累计≤4（manifest HEAD1、GET1、媒体HEAD2），包括失败请求**，S3 LIST0、STS0、任何媒体GET0。S3 client单线程串行且`botocore Config(retries={'mode':'standard','total_max_attempts':1},connect_timeout=5,read_timeout=12,max_pool_connections=1)`，验证每次wire请求的HTTPS host、method、Bucket/Key、次数，阻止内部重定向、区域discover、代理绕过及隐式重试。若无法通过严格请求钩子保证上限，`REQUEST_BOUND_UNENFORCEABLE`**首个网络请求前停止**，不靠成功日志倒推。这只认证受控metadata GET的应用读上限，不冒称实际网卡wire字节恒等。
- 实际`v2_1` UID match>0仅能标`UID_PRESENT_IN_V2_1`，**不等于HourVideo dev_v1.0的真实媒体裁剪/PTS/题目时间轴兼容**。不得选择匹配数以外视频，也不能将HEAD大小当下载许可。对象长度不符旧4GiB门只报拒绝，不放宽计划。若manifest 403/404/无候选/超预算/文件不可解，明确阶段和原因后立即STOP，**不换源或重试**。

## 3. 唯一公有提交及直接对接下次媒体获取

**公有repo最多且只能两处变更**：
1. 新`docs/codex-artifacts/VLM-EGO4D-AWS-META-004/limited-aws-metadata-receipt.md`，匿名事实：源文件合法存在/体量分项检查与schema门、抽取的顶层视频数（没有真实UID）、profile静态加载/远端AUTH实际状态、4次S3请求按操作/成功/失败计数、manifest HEAD长度及GET**应用字节数**、v2_1精确UID命中总数、无歧义可HEAD候选数、最多2对象HEAD的结果和每个≤4GiB/两者合计≤8GiB，版本/同钟/线上的字节硬门仍UNKNOWN；媒体GET0/GPU0。失败只填已完成阶段，其余`NOT_RUN/UNKNOWN`，不能把未读输入当“UID匹配0”。
2. `docs/codex-results.md`**末尾追加一条** `### VLM-EGO4D-AWS-META-004`，链接同轮实际收据，不虚构远端AUTH OK、UID匹配或实验结果。

**绝不上传**用户私有磁盘路径/用户名/文件名实际编号、原JSON、真实UID/qid、QA/答案、canonical S3媒体对象URL/ETag/VersionId、原manifest内容、用户邮件、AWS Key/Secret/Token、私有临时脚本/日志/签名请求、任何视频或媒体片段。官方固定manifest桶/公共代码链接可引用；统计计数与PASS/UNKNOWN可公开。私有本地脚本/临时数据仅现成隔离目录保留必要受保护审计计数，不碰旧实验锁/账本/HourVideo原标注及Charades。

Git prepush检查`git diff --cached --name-only`仅上述2路径；正常main push**一次**后STOP，等待ChatGPT验收；不因用户希望尽快实验就擅自开始媒体GET或GPU。**下一次有实际官方对象长度和有效源身份后，ChatGPT将优先申请新的单段/小流量真实媒体下载与RTX3090模型对照授权，不再追加合成工具轮次。** `NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`保持。
