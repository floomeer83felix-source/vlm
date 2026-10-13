# VLM-EGO4D-AWS-META-001｜一次真实 Ego4D AWS 极小元数据预检（不下载视频）

**2026-10-13 北京时间｜唯一有限 READY 父任务，用户明确回复「同意」。** 用户同意上一轮 ChatGPT 的准确提议：「使用已有`boto3`，在严格限定范围内读取**一份**Ego4D 官方`full_scale`清单，并对**少量精确匹配的对象执行HEAD元数据查询**，核实UID、版本和实际文件大小；**不下载视频正文、不使用GPU、不公开AWS密钥**」。此任务**仅限这一轮**，由用户在**原同一个长期Codex对话主动发新消息**启动；不自动恢复已结案的`VLM-EGO4D-MEDIA-001`、`VLM-EGO4D-TOOLS-001`、`VLM-EGO4D-BOTO3-001`，其先前2段/8GiB GET预算**没有转移**。

## 1. 执行前安全门

- 在**独立公有Git文档checkout**先`git status --short`（须干净）、`git fetch origin main`、仅安全fast-forward后重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本合同、[离线映射工程收据](../VLM-EGO4D-BOTO3-001/offline-source-and-budget-receipt.md)和[工具就绪收据](../VLM-EGO4D-TOOLS-001/isolated-tool-readiness-receipt.md)。核实**恰好一个READY且为本任务、`codex-results.md`没有本任务旧回报**。任一不满足就STOP，不reset/rebase/force、不动旧锁/账本。
- 用户转述正式Ego4D批准有效至**2026-10-26**；不得在截止后的时间或时区不明的10月26日当天发起新AWS数据请求；计划仅在**2026-10-25北京时间23:59之前**可执行。默认耗时CPU前台≤15分钟，时间超过STOP。只复用上一轮实测已装boto3/botocore的**唯一私人隔离Python venv**；不切换、安装、升级、删除环境，不碰`pytorch`、CUDA/GPU、原研究工作区、HourVideo答案处理工具、Charades或任一历史资产。找不到原venv就`SDK_LOCATION_UNKNOWN` STOP，不扫描全盘，不创建第二venv，不调用Ego4D CLI。
- **凭据：**仅通过boto3标准签名功能在用户已有且**明确专用于Ego4D的命名AWS profile `ego4d`**发请求；禁止用默认/隐式账户、环境里的其它凭据或未知profile。SDK可为了请求签名**内部读取现有凭据**，但Codex脚本/终端不得手动打开、遍历、打印、复制/修改credentials、Secret Key、Session Token、邮箱或账号信息；不执行`aws configure`、登录、刷新令牌、`STS`调用、profile枚举、SSO/credential_process/EC2 IMDS等可能意外联系其它服务的凭据链。配置缺失、不明确、过期或需要网络续期时`AUTH_PROFILE_HOLD` STOP，请用户自己在Windows按官方流程私下配置，**不得把密钥放聊天/GitHub**。若不能证明不会产生隐式STS/额外AWS服务请求，则在首次AWS请求前STOP。
- 仅对**前次用户已明确指定并授权的那一个本机HourVideo `dev_v1.0_annotations.json`完整路径**允许一次只读解析，不递归探用户Downloads、不读test/sample/其它QA文件，不复制或上传该文件。只抽取最外层视频UID及`video_metadata.duration_in_seconds`，其他题目、答案、选项、canary不用于任何排序/提示/统计或输出；**JSON解析器技术上会读整份文件字节，不能谎称完全没有接触文件中QA文本，但内存不得向外暴露**。若路径未知/未授权/文件异常，`LOCAL_UID_SOURCE_HOLD`且**0 AWS请求**；不要遍历硬盘寻找文件。UID只能保留在短命私有RAM中，且不得写公网仓库/结果日志、终端或脚本命令行参数。
- 无真实媒体GET/Range、字节流下载、视频/帧/权重/特征/额外HourVideo标注下载、视频解码/ffprobe、GPU/Qwen/SigLIP/训练。**本轮允许的研究数据GET只有下文固定的一个官方CSV manifest**。不得用官方`ego4d --datasets full_scale`，不得访问其它数据集/metadata`ego4d.json`，不得到第三方镜像/跳转站下载。

## 2. 唯一发行、唯一来源、严格请求数与体量

### 2.1 固定官方发行与资料来源

- 固定只检查**Ego4D发行`v2_1`**的**`full_scale`**清单。它是官方CLI[固定源码](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/config.py)当时的`VERSION_DEFAULT`；但**HourVideo`dev_v1.0`不等于Ego4D发行`v1`或`v2_1`，此查询只是测试候选UID在`v2_1`清单中是否出现，不许据此认定同钟/同剪辑/相同像素版本**。未匹配就`V2_1_UID_JOIN_ZERO` STOP，不继续查`v1`/`v2`、其它CSV或数据镜像。
- manifest唯一可GET的精确对象由官方[manifest.py固定源码](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)确定：S3桶`ego4d-consortium-sharing`、键`public/v2_1/full_scale/manifest.csv`。这不是用户传入的URL，不从标注内容得到、不拼接不可信输入。官方`file_uid`与`video_uid`可能不同，`canonical_s3_location`/`s3_path`是媒体源字段；**不可把前轮测试用的`public/{release}/full_scale/{UID}.mp4`当成真实对象键**。
- 对媒体候选，严格检查manifest行包含**精确视频`video_uid`**与非冲突的`canonical_s3_location`或`s3_path`，且是`full_scale`语义的**原视频记录**；有非空`file_uid`、`type=file/json`、来源多义/重复UID不同对象、视频UID缺失则该候选一律不HEAD，歧义覆盖待选样本则STOP。不猜video_uid↔file_uid或clip_uid映射。源S3桶必须在官方[universities.py固定白名单](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)的值域内（可能与manifest桶不同），S3键非空/无../路径穿越、疑似镜像、非S3 URI、重复相冲突或桶未授权一律STOP。除了官方清单中已核字段外不做媒体对象键猜测。
- 从已准本地HourVideo顶层UID集合与CSV做**纯RAM内精确等值join**。可扫描50个本地顶层UID与至多8MiB官方manifest的所有行（不用QA答案选样）；按视频声明时长≥1200s优先、尽量至少一个≥1800s（如匹配且类型无歧义）、冻结确定性候选排序，最多选**两个不同UID、不同官方媒体S3对象**做HEAD。若两项不足，只查1项或0项，别换发行/数据源或扩大HEAD数。UID出现在`v2_1`仅是`UID_PRESENT_IN_V2_1`，**真实HourVideo↔Ego4D媒体版本与PTS严格同版仍`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`**。

### 2.2 绝对请求额度（本父任务不可重置）

- **最多4个经用户批准的S3 API HTTP尝试**，按顺序：①恰好至多**1次** `HeadObject`官方manifest；②若HEAD声明正文为已知且**0 < ContentLength ≤ 8,388,608字节（8 MiB）**，且ETag/VersionId足以绑定身份，才至多**1次**`GetObject`获取该**唯一manifest**；③完整验证manifest和UID匹配之后，对确切两个以内的canonical媒体对象至多**2次**`HeadObject`；**总S3 HEAD≤3、S3 GET≤1、任何媒体GET=0、S3 LIST=0、STS=0**。不执行无关数据查询，失败/403/404/异常/超时/重定向/隐式重试即STOP，**不得多发一次补救查询**。不发第三方HTTP、CloudWatch、credential-check API。
- 用受控`boto3.session.Session(profile_name='ego4d')`和仅一`s3` client，使用botocore`Config(retries={'mode':'standard','total_max_attempts':1}, connect_timeout=5, read_timeout=12, max_pool_connections=1)`；禁止`download_file`/`TransferManager`、并行、后台线程/自动补偿、Range/206与意外重试。实际HTTP发起前检查请求**方法、HTTPS host/桶、bucket、key、GET白名单**；如果无法监测/限制真实wire尝试（含区域重定向、SDK隐藏请求），`REQUEST_BOUND_UNENFORCEABLE`→不发请求。凭据刷新不得偷偷请求STS，代理/TLS身份不确定则STOP，不禁证书/关TLS校验/改系统代理。
- GET manifest使用`IfMatch`绑定HEAD ETag或可靠`VersionId`，核GET响应`ContentLength`与HEAD一致、`ContentEncoding`非压缩/不明则拒绝；读流分块**最多8MiB实际应用正文**，每次严格检查累计且超过即关流STOP、不可无限内存/落盘。SDK/TCP预取流量可能大于应用read值，**不谎称全部线上wire字节被精确硬限**；本轮允许的只是HEAD确认文件≤8MiB且流读取上限。若没有可验证身份锁/内容长度/限读条件则不GET，不能尝试猜URL。内容不得包含真实视频字节、答案或别的研究数据。
- HEAD媒体只收`ContentLength`、`ETag`、`VersionId`可用性及相应成功/拒绝状态。若`ContentLength`>4GiB则标记该媒体**不符合旧单视频4GiB计划**，但HEAD本身仍算正常验证；两段文件总声明大小如超过旧8GiB也仅报告不符，**不得在本任务下载或自动调整配额**。不把ETag当官方MD5、同文件内容hash或版本同钟证书。媒体授权只是HEAD，不读任何媒体字节、Range或首帧。
- 超额、桶/身份未知、未匹配、AWS权限403、账号没专用profile或无法执行request-count守卫，**如实`SAFE_PREFLIGHT_STOP`**；不安装软件、不新建环境、不转换成另一个S3/HTTP方案。强制无自动重试，在本轮同一Codex会话**最多一次现场尝试**；原Codex报错/请求部分成功后不能重开一个新run绕过4请求计数。用户未授权额外请求，不向用户索取密钥/凭据输出。

## 3. 私密边界、交付与科学解读

- 授权实际AWS工作仅限**已获批准的专用boto3 venv**与一个新**短命私有本机脚本/运行临时目录**；代码和临时原始manifest/UID/S3 bucket-key/ETag/VersionId/凭据/完整HTTP响应/Windows路径/命令行真实参数都不得上传公共Git或复制进Codex对话。如实际需持久审计请求上限，仅在用户私人新隔离目录保存**不含秘密的计数器/聚合账本**，不可触碰旧MEDIA任务或其它研究锁。不得将任何AWS access token放进命令行、日志、提交、聊天。公共报告里**只能是数字聚合与PASS/HOLD标签**，官方固定manifest桶/版本代码可引用，但**不得公开实际匹配UID、媒体对象名、完整S3路径、内容hash或多字段可重新识别的细节**。异常信息先脱敏，杜绝SDK底层Exception原文泄漏。
- 收据至少包含：合法访问用户确认与本机AWS使用`AUTH_OK / AUTH_NOT_CONFIGURED / AUTH_DENIED / NOT_TESTED`，成功/失败各类允许API请求数量与是否有隐藏请求不确定性，manifest HEAD长度/GET**实际应用正文总字节**（一份限8MiB），匹配`v2_1`的UID数量（聚合）、去重安全可HEAD候选数与实际HEAD 0/1/2，远程元数据已知长度与≤4GiB数量、合计大小是否≤8GiB（仅若都已知），来源/发布版本证据类别与仍未证成的`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`，原始媒体GET0、GPU0、是否存在工具/权限/网络/大小阻塞与下一门。没进行的检查`NOT_RUN`，不把未查的UID join数量当0；不得把Ego4D批准自动当AWS AUTH_OK，也不得把UID相同当媒体PTS同钟认证。
- **公有Git唯一允许两处修改**：①新建`docs/codex-artifacts/VLM-EGO4D-AWS-META-001/limited-aws-metadata-receipt.md`（匿名聚合事实与安全停止状态）；②`docs/codex-results.md`末尾**只追加一次**`### VLM-EGO4D-AWS-META-001`，链接收据与核心数字/UNKNOWN。不得新增/提交私有GET代码、官方CSV、UID名单、凭据、视频、metadata临时文件，不更改`docs/next-steps.md`、`docs/research-overview.md`、`AGENTS.md`、本合同、合成程序/旧回报。严格`git diff --cached --name-only`恰好两条路径、审查脱敏后一次普通main push并**STOP**，Codex不得自行放行下一轮媒体下载/GPU。
- **验收类型：**`META_PREFLIGHT_EVIDENCE`（已查到真实官方元数据，仍`MEDIA_GET_NOT_AUTHORIZED`）或`SAFE_METADATA_STOP`（有具体可审计阻塞，实际0或部分限定请求）。两者都不能代表真正同版媒体或真实长视频QA性能。HourVideo标注结构50视频/1182题及此前合成32单测已通过但不可替代本轮远端核实。科研`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`、所有真实模型/GPU/训练HOLD持续。
