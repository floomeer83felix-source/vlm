# VLM-EGO4D-AWS-META-002｜用户已私下配置ego4d凭据后的首次有限真实S3预检

**2026-10-13，北京时间；唯一READY父任务；用户明确回复「已配置」，触发之前约定的下一次有限元数据验证。** 用户仅确认自己在Windows完成凭据配置，**不等于已核实配置正确/签名可用或官方数据权限**。此为**新的单次父任务**，绝非重跑已经[安全结案的META-001](../VLM-EGO4D-AWS-META-001/limited-aws-metadata-receipt.md)。目标是**立刻取得可审计的真实官方CSV UID匹配与至多两个媒体对象的HEAD体量证据**，没有合成测试/新包安装/静态规划新一轮。Ego4D官方访问用户确认至2026-10-26。本任务只授权元数据访问；真实媒体GET、GPU/Qwen/SigLIP仍为0。

## 1. 一次性执行前置门（短平快）

1. 由用户**在原同一个Codex长会话**发消息主动启动；Codex在独立的**公有docs checkout**检查干净工作树、`git fetch origin main`后安全fast-forward；重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[原META-001执行合同](../VLM-EGO4D-AWS-META-001/README.md)及失败收据、上一轮[SDK安装收据](../VLM-EGO4D-TOOLS-001/isolated-tool-readiness-receipt.md)。**恰好唯一READY=本ID，codex-results无本ID任何旧回报**，否则STOP。不得清理/重跑旧实验、Charades或既有任何父任务。
2. 严格**继承原META-001合同第1—3节的一切技术和隐私限制**，但唯一更改是**本ID、本轮独立请求计数与输出收据路径**，以及用户此刻自述“[ego4d] 已在Windows本地配置”。不把自述当远端验证PASS。使用原有且已安装boto3的**那一个私有独立venv**，不使用`pytorch`，不安装/升级/创建环境，不调Ego4D CLI或AWS CLI。**CPU前台≤15分钟，最迟2026-10-25北京时间23:59停止发新AWS请求**。
3. **私有凭据门：**boto3仅用`Session(profile_name="ego4d")`，标准本机共享文件静态凭据提供器可以内部加载刚配置的Access Key/Secret/可选Session Token，仅为签名；脚本/Codex不得直接打开、列举、回显、复制或更改credentials/config、隐藏用户名、私人目录或任何密钥；不允许访问邮箱、不向用户索取密钥，不得调用默认/其它profile、凭据环境变量、credential_process、SSO、IMDS/EC2、STS或远端令牌刷新。若新配置仍`ProfileNotFound`或不具备静态签名能力，**立即`AUTH_PROFILE_HOLD`，不重试、不自行编辑配置**。如果需要代理/重定向/非已授权网络身份也STOP；SDK底层异常只做类别+阶段脱敏摘要。
4. **只读一次原用户已授权本机HourVideo `dev_v1.0_annotations.json`**（必须使用以前明确指定的那一条完整私人路径；无则`LOCAL_UID_SOURCE_HOLD`、**0 S3请求**，不搜索电脑），仅从顶层视频记录提取视频UID及`video_metadata.duration_in_seconds`。JSON整体解析技术上会读QA内容，但**不使用、不打印/发布、不选择答案字段**；原JSON、UID明细、真实视频对象URL、bucket/key/ETag/VersionId/哈希与账户信息均只驻留私有RAM，不进入Git报告、终端或聊天。遇未知结构/字段不同即STOP，禁止用QA标签猜测。

## 2. 唯一允许的真实S3元数据访问

**完全固定，同原META-001请求白名单且新任务重新独立计数，不动历史预算：**

| 先后步骤 | 允许请求 | 条件/限额 |
| --- | --- | --- |
| 1 | `HeadObject` | **唯一官方** `s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`，最多**一次**；ContentLength必须`1..8,388,608`B、版本/ETag可绑定 |
| 2 | `GetObject` | 同一manifest最多**一次**，HEAD→GET以`IfMatch` ETag或可靠VersionId约束、检查身份和内容长度；流式应用读取合计**≤8MiB**，其他GET一律禁止 |
| 3 | `HeadObject` | 在官方manifest与原用户本机HourVideo顶层UID**精确等值匹配**后，最多**两个不同canonical原视频对象**，each一次，不读其媒体正文 |

**累计最多4次S3 HTTP尝试（成功/失败均计入）：官方manifest HEAD≤1、GET≤1，视频对象HEAD≤2。媒体GET/Range=0，LIST/STS=0，元数据JSON/其他CSV/其它release/其它桶探索/第三方URL=0。** 须能限制及审计 botocore 的**真实wire尝试**（含错误请求），只使用一个串行client，`retries={'mode':'standard','total_max_attempts':1}`、保守超时；禁`download_file`/TransferManager与后台隐式重试/region自动重定向。任何不能证明请求次数/来源白名单/TLS有效或远端实际权限时，fail closed，不允许靠“请求成功”倒推合规。数据GET读到的应用字节数≠全部网卡wire字节，收据应明确区分。
- 清单固定`v2_1`、`full_scale`，是Ego4D官方[manifest.py](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/manifest.py)所述位置；**不能切换`v1`/`v2`、无关数据集或镜像来补匹配**。官方视频可放在多个官方[贡献大学bucket](https://github.com/facebookresearch/Ego4d/blob/4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb/ego4d/cli/universities.py)。只接受CSV显式、无冲突的`video_uid`、`canonical_s3_location`/`s3_path`、类型为canonical full_scale视频且桶在官方白名单；如仅有`file_uid`、重复/多义对象、非S3源或来源不可信，**不猜测媒体键，更不能套用旧SYNTH假的`public/{version}/full_scale/{UID}.mp4`规则**。
- 按无需问答答案的固定规则选最多两项不同UID/不同S3 object优先≥20min及其中至少一项≥30min（如匹配），不足2项就0或1，官方CSV未找到时`V2_1_UID_JOIN_ZERO`，不扩大来源。HEAD只记录内部`ContentLength`、ETag/VersionId存在性和源版本情况；**大于4GiB的对象只标“未来旧单段预算不符”，不触发媒体GET或新预算**。若名称对应但缺乏版本/帧/时基验证，输出`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`，不把UID join当作同版认证。发现403/404/超时、清单大小超8MiB、响应不一致、代理/HTTPS或请求计数不明，停止而不是重试。
- 运行一次后立即结束本任务：不可对失败做新尝试或换provider/profile/版本。**任何视频/片段/帧/元数据包/模型下载、GPU、ffprobe、人工答题、长视频问答、训练与旧媒体预算都不属于本轮许可**。即使两段媒体HEAD皆成功，也必须STOP，等待ChatGPT下一次明确的有限视频GET许可。

## 3. 唯一可推送的公有交付

仅允许**两处**：新建`docs/codex-artifacts/VLM-EGO4D-AWS-META-002/limited-aws-metadata-receipt.md` + `docs/codex-results.md`**末尾追加恰好一条**`### VLM-EGO4D-AWS-META-002 ...`；这份合同、看板、总览、已有脚本/测试一律不改。私有临时脚本/manifest/日志/UID与凭据不能上传。提交前`git diff --cached --name-only`严格为这两个路径，检查脱敏，向main正常提交推送一次后STOP。

收据必须尽量**提供真实可用的判断而非延伸规划**：profile已就绪/远端AUTH_OK/403/UNKNOWN区分，4次请求实际每类型尝试数、manifest HEAD声明长度与实际GET应用字节数、真实`v2_1` UID精确匹配**聚合数量**、无歧义canonical视频候选数、已HEAD 0/1/2、每个是否≤4GiB及若全部已知时的合计是否≤8GiB，真正阻塞位置与实际异常**类别**，媒体GET=0/GPU=0；如未达到阶段则标`NOT_RUN/UNKNOWN`不填零匹配。不得披露真实UID、真实对象S3路径、私人路径、账号、私密签名或ETag。合理状态`META_PREFLIGHT_EVIDENCE / MEDIA_GET_HOLD`或`SAFE_METADATA_STOP / <具体原因>`。该结果**不自动放行真实媒体/实验**；尽快发main提交供ChatGPT判定后续可下载范围。

科学状态恒定：HourVideo真实开发标注50视频/1182题只有元数据容量；现阶段若HEAD到视频只说明官方对象与大小，不等于开发QA内容版本/PTS同钟；`NOVELTY=RETAIN0`，Charades`FINAL_MEDIA_STOP`。
