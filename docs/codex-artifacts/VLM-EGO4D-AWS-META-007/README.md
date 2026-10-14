# VLM-EGO4D-AWS-META-007｜官方canonical来源兼容性诊断＋有限视频HEAD（预排合同）

**2026-10-14｜PENDING_NEW_EXPLICIT_METADATA_AUTHORIZATION（非READY，严禁执行任何新云请求）。** META-006 [cd6eac2](https://github.com/floomeer83felix-source/vlm/commit/cd6eac2a69bed936c6caf143ae997fe81ed6e1b9)已一次性结束：官方v2_1/full_scale manifest完整GET 4,653,141B成功，HourVideo私有50/50顶层video UID精确命中，但组合`CANONICAL_SOURCE_HOLD`根因子项未记录，媒体桶/对象HEAD皆0。本任务只为精准解除这一门，**不重新运行006、不继承其未使用4次请求配额**。用户需要在ChatGPT明确新批准下面最多7次HTTP元数据S3尝试及唯一CSV GET≤8MiB，ChatGPT再将本ID设**唯一READY**，用户随后在原**同一Codex长会话**发送新执行消息。当前LIVE-MEDIA-002/AB与GPU训练队列一律非READY、不得自动执行。

## 固定官方源码和高优先级诊断

- 固定上游来源：`facebookresearch/Ego4d@4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb` 的 `ego4d/cli/manifest.py`、`universities.py`、`s3path.py`、`config.py`。上游`VideoMetadata` 的字段优先顺序是 `canonical_s3_location` 然后 `s3_path`；`type=mp4/video`是视频，`file_uid`和`video_uid`不可混同。上游解析S3路径为`s3://bucket/key`，`BUCKET_TO_UNIV`来自固定官方贡献桶表。**官方源码没有要求真实媒体key等于`public/{version}/full_scale/{UID}.mp4`**，这个路径只在既有 SYNTH 测试器里出现，绝不能把它当作真实合法源的必要条件。反之，不能因为CSV来自官方就自动把任意对象/外域视为安全合法。
- **阶段0，0 AWS网络**：先在私有本地只读核上轮一次性执行脚本/组合来源校验器（若原脚本不可用，明确`SCRIPT_UNAVAILABLE`），与固定上游源码/合成测试器对照。写下检查器实际字段选择、`URI方案`、官方贡献桶白名单、`key安全性`、`query/fragment`、媒体类型/UID判据、路径前缀假设及停止点的真假；只允许输出匿名`GUARD_DIFF_<CATEGORY>`，**禁止在公有Git/聊天暴露任何真实UID、URI、key、桶、region、ETag、JSON/CSV行或私有脚本**。本阶段不能看不到真实CSV还冒称已确认哪个子项在META-006失败；有真实根因证据才可写`CAUSE_CONFIRMED`，否则`CAUSE_UNKNOWN`。修复仅针对与官方源码不相符的过严规则，绝不放宽HTTPS、官方白名单、真实对象身份或下载预算。
- 输入只限已知用户此前指定的**一个**私人Windows目录顶层精确`dev_v1.0_annotations.json`，只读、非链接/reparse、0<size≤16MiB、dev结构及50顶层UID/时长；QA数组最多只取长度用于“≥2题”过滤，**答案/内容绝不用于对象排序和输出**。不扫其它盘或子目录、不读取旧实验树、不改/复制原JSON。官方manifest仅同一次合法GET时私有RAM解析，禁止上传/保存原CSV或内容。
- 新阶段的验收不要在**所有**50个UID遇到第一个非法candidate后误写“0个合法对象”：必须在RAM对50个等值命中的行做封顶的**逐UID结构分类计数**，按互斥预定义代码（如`FIELD_MISSING_OR_EMPTY`、`FIELD_CONFLICT`、`S3_URI_INVALID`、`BUCKET_NOT_IN_PINNED_OFFICIAL_LIST`、`KEY_UNSAFE`、`NOT_VIDEO_TYPE`、`AMBIGUOUS_UID_OR_OBJECT`、`VALID_CANDIDATE`）；公开仅聚合类别计数，无可重识别时间/序号/身份。含合法来源的安全候选方可按预先冻结的长度/开发QA**数量**/UID稳定哈希匿名排序，再取最多2个不同视频、不同对象；若官方row存在同一video UID多对象未可证去重则该UID HOLD，不私自挑一个。任何不安全行绝不做HEAD，**有其他合规候选是否可继续必须由冻结规则决定**，不得随执行临时换规则或忽略异常。

## 新请求预算（**仅待后续明示批准**）

1. 只使用现成私人boto3 venv+用户`ego4d`静态AWS profile，官方唯一清单为`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`。旧META-006已完成的manifest内容未持久化，因此**如需真实行级核验，本轮确须新一次受控GET**，不能谎称私有缓存仍在。禁止ST​S/LIST、默认或其它profile、SSO/IMDS/刷新、依赖安装、其它release、桶遍历/镜像、模型/GPU、私有答案外发。审批窗口：北京2026-10-25 23:59以后不发本任务新AWS请求；现场≤20分钟。
2. 请求始终串行且**整个任务真实S3 HTTP尝试≤7（包括301/403/超时/失败）**。A固定manifest桶`HeadBucket≤1`，核可信TLS区域提示；B正确区域manifest `HeadObject≤1`且200、`0<L≤8,388,608B`、ETag/VersionId身份锁；C**唯一一次**条件`GetObject≤1`、完整一致、非压缩、应用正文≤8MiB、`read_timeout=90s`、`connect_timeout=5s`；D至多2个官方贡献桶各`HeadBucket≤1`；E最多2个经安全筛选不同canonical视频各`HeadObject≤1`。最长A1+B1+C1+D2+E2=7。若候选共用同一个bucket应复用已验来源，不为凑次数重复HEAD。**媒体GET/Range/206/视频正文0**。
3. 每次真实HTTP发送前审计method/HTTPS/官方regional S3 TLS host/固定bucket-key/区域/当前阶段，**fsync匿名累计计数**；`retries={'mode':'standard','total_max_attempts':1}`、pool=1、禁代理继承与自动重定向/region重试、TLS验证正常、不拼新未知URL、失败即STOP。若缺可靠wire attempts/预算保护则任何请求之前STOP。不改原AWS配置、环境、历史ledger/锁；不尝试下载、解码、Qwen/SigLIP/GPU。请求体/SDK缓冲未精确量测不冒称网络wire字节已严格实测。
4. 有成功完整CSV与合规canonical候选才可HeadBucket/HeadObject。只报告UID匹配数、各分类聚合计数、0–2 HEAD实际次数、对象`ContentLength`是否≤3.5GiB（后续单视频候选门）、数量≤4GiB和两个合计≤8GiB、身份绑定是否可用。**HEAD200不证明有下载授权，不证明HourVideo dev_v1.0与Ego4D v2_1视频发布/PTS同钟**。若正式路径仍不能安全解释，提交`CANONICAL_SOURCE_HOLD_<匿名类别>`，不乱改官方源、增配额或发媒体GET。

## 唯一两处公有交付（正常push一次即STOP）

1. 新建`docs/codex-artifacts/VLM-EGO4D-AWS-META-007/canonical-source-classification-receipt.md`：阶段0静态校验差异类别、是否有实际行级根因证据、真实CSV A–E的发送次数/成败、UID总交集、匿名互斥来源类别汇总、安全候选是否存在、最多2媒体HEAD实际大小门、未测的PTS/版本/下载/模型均UNKNOWN或NOT_RUN。不得将0个已执行HEAD写作0个UID匹配或不存在视频。若阶段0就可以可靠认定某安全/身份矛盾，仍可在网络前SAFE_STOP，0 S3。
2. 仅在`docs/codex-results.md`末尾增加**一次**`### VLM-EGO4D-AWS-META-007`匿名父结果和报告链接。不得修改AGENTS/next-steps/research-overview/旧报告、公开代码/旧研究资产，不得上传脚本、原清单/JSON、真实URI/UID/桶region/QA答案/账户凭据/日志/checkpoint。一次正常main push即结束，不自动触发已排队MEDIA-002或GPU任务。

若完整CSV+至少1 canonical来源/HEAD真实大小合法通过，交由ChatGPT快速验收并在用户**新独立媒体GET许可**后切换已有[LIVE-MEDIA-002](../VLM-EGO4D-LIVE-MEDIA-002/README.md)；训练路线已经预排无需再写合成包。科研`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`持续。
