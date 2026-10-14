# VLM-EGO4D-LIVE-MEDIA-002｜一段真实Ego4D长视频：身份重建、有限验证与单次受控获取

**2026-10-14｜USER_APPROVED / 唯一READY（仅限本合同的单段有限官方媒体GET与必要metadata重建）。** 用户要求尽快启动真实GPU实验，故将可直接衔接[META-007真实实测](../VLM-EGO4D-AWS-META-007/canonical-source-classification-receipt.md)的单视频获取流程一次写好。META-007已安全结案，未继承其7/7已消耗请求，不复活旧MEDIA-001、META-006/007及原2段8GiB下载权限。**用户已在ChatGPT对这一具体合同明确回复「同意，不要每次问我」，新独立批准总计最多8次S3 metadata+media HTTP attempts、唯一官方manifest GET应用正文≤8MiB、最多2个对象HEAD、最多1个媒体GET且单个≤3.5GiB、媒体正文累计≤4GiB；ChatGPT已将本ID设为唯一READY。必须仍由用户在原同一Codex长期对话新发一次执行指令才能运行；不得解释为无限续传、额外样本、额外AWS请求、GPU或训练的空白授权。** 这项许可不涵盖GPU/模型/训练、其他视频或模型权重下载。

## 实际已核验的证据与缺失

- [Codex a85e66a](https://github.com/floomeer83felix-source/vlm/commit/a85e66a4e6910afac5c570937246986f25ff60a5)在官方`v2_1/full_scale`同一个4,653,141B manifest全文和用户本机HourVideo `dev_v1.0`标注50个顶层UID精确匹配：45个当前固定官方贡献桶白名单合法候选、5个桶来源未在锁定表中故隔离；按预先冻结的≥30min优先和私有UID SHA256排序取前2个不同canonical对象，真实媒体HEAD200/ContentLength/身份锁2/2，**其中恰1个满足≤3.5GiB，另1个>4GiB**、合计12,897,682,214B >8GiB。不能对5个隔离来源发请求，也不能把2个加总当作可下载预算。
- **上一任务不持久保存原manifest、真实UID→bucket/key/region/ETag映射**，只有公有匿名收据；所以不能凭收据猜出哪个视频要下载。此新父任务必须在独立新授权下**重新严格核验唯一官方清单与候选身份**，并为目标对象重新做HEAD后方可单次GET。不得要求用户把真实UID、AWS key、QA、manifest或S3 URL发到聊天/GitHub。
- HourVideo`dev_v1.0`与Ego4D`v2_1`仅UID相同；发布剪辑起点/PTS/时长与QA时戳桥接均**未证**。哪怕完整获得一段也只能先成为`ONE_OFFICIAL_MEDIA_ACQUIRED_METADATA_ONLY`，不得算正式HourVideo准确率。Qwen/SigLIP/GPU训练另需独立许可。

## 数据、来源和候选重建（在本合同批准后）

1. 只读用户之前指定的一个私人Windows目录顶层`dev_v1.0_annotations.json`（0<size≤16MiB、正规无reparse、dev schema/顶层UID和正时长）；技术解析JSON可以加载结构，但**只能用顶层UID/时长和题目数组长度≥2做选样**，严禁标准答案/正确性/QA原文参与排序、训练或公共输出。不能递归全盘扫描、复制原JSON、改旧账本/锁。
2. 只使用现成独立boto3工具venv与`ego4d`静态AWS profile，不手工查看/打印/更改凭据、账户、profile或私人路径；禁止STS/LIST/额外release/镜像/CLI bulk download/SSO/默认profile/代理/TLS禁验/安装依赖、读旧科研工作区。仅官方`s3://ego4d-consortium-sharing/public/v2_1/full_scale/manifest.csv`与固定上游`facebookresearch/Ego4d@4bd10ed40b4f8d8ad26344afc2c8526f7d1dedeb`的`universities.py`贡献桶白名单。manifest正常字段优先`canonical_s3_location`后`s3_path`，拒绝空、非S3、字段冲突、非法key、未知贡献桶、模糊/重复UID、非视频类型，绝不把合成路径当实际媒体key。
3. 完整同一CSV与本地顶层video_uid精确join后，在私有RAM按META-007相同互斥分类/冻结选样规则确定排序：**优先≥30分钟，次用UID SHA256稳定序；固定前两段不同UID和canonical对象**；无45合法候选等一致性证据或排序变动即`REPRODUCIBILITY_HOLD`，不替换候选、扫其它对象或扩大本轮单段预算。按必要元数据桶地区发现和最多2个HeadObject验证它们；只有结果可重现为两个HEAD200，**恰1段0<L≤3,758,096,384B、另1段>4GiB，且2段合计与META-007收据12,897,682,214B一致**（不能仅靠模糊合计代替身份锁），才准将合格段进入GET门。两段真实身份、region、key和ETag均只保存在私人内存，GET与新HEAD当前身份绑定；若对象变化/数值不同即STOP，不按大小有利重选第三段。
4. 一段合法官方`full_scale`长视频（标注声明≥20min、开发题数≥2；优先≥30min），绝非clips/540ss/Charades/第三方镜像；目标私人目录与独立匿名持久账本均由本父任务唯一拥有，不在公有Git或原私有训练/实验/旧媒体目录内，空闲空间≥对象声明长度+2GiB。缺空间/重解析链接/原文件已存在即STOP，不能覆写或删除既有数据。

## 已获用户明确批准的有界AWS请求合同（唯一READY，仅本父任务）

- 严格串行总**≤8次S3 HTTP wire发送尝试（包括失败、301、4xx或超时）**：A固定官方manifest桶HeadBucket≤1；B区域正确的该CSV HeadObject≤1；C同对象身份锁条件GET≤1（应用正文≤8,388,608B/read_timeout=90s，必须读满并等于HEAD长度；未压缩、不Range）；D对两段已冻结安全候选的贡献桶HeadBucket≤2；E对两个不同canonical媒体对象HeadObject各≤1共≤2；F只选上述HEAD合格的一个对象媒体GetObject≤1。最坏A1+B1+C1+D2+E2+F1=**8**。某桶重复则复用可信区域而不额外发送。**其它视频GET/Range/206、恢复GET、下载器多线程、LIST/STS全部0**。本轮所有媒体正文研究GET读取累计硬上限**4,294,967,296B（4GiB）**，单个对象声明≤3.5GiB。
- 正式HTTP每次发送前必须审查精确bucket/key/HTTPS可信官方AWS商业地区主机、方法、region、阶段及已用次数，并持久`fsync`不可回滚匿名计数；`connect_timeout=5`、`read_timeout=90`、`retries={'mode':'standard','total_max_attempts':1}`、pool1，禁止自动区域跳转、代理和任何隐藏重试。官方manifest/两对象的ETag/VersionId身份绑定要在本轮一致；GET必须在本轮媒体HeadObject200和长度/可用身份锁之后，使用条件标识且绝不发送Range。错误/短读/意外响应立即STOP，本任务不得第二个GET、换视频或新run重置计数。
- **必须能够证明保守的请求数和接收总量上限真正可强制执行**：包括网络错误响应、SDK未返回buffer/TLS预读与传输异常处理；独立接收上限无法核实时`LIVE_TRANSFER_ENFORCEMENT_HOLD`并**0媒体GET**，不把HEAD的ContentLength或落盘字节误说成网卡wire/收费精确总量证明。GET的预扣须于新私人账本`STARTED`写盘fsync后才发，GET过程每块验应用字节、长度、写盘和总额，完成严格等于新HEAD声明大小才私有`.part`原子rename确认。持久STARTED中断后禁止再GET或恢复，无法证明无重放则STOP。
- 仅本任务前台墙钟≤60分钟（其中不包含GPU）；可用既存`ffprobe`仅CPU读取私有媒体容器时长/PTS元信息，工具缺失则`TIMEBASE_NOT_VERIFIED`，不得装ffmpeg/解码帧或调用模型。**北京时间2026-10-25 23:59后不得启动任何本合同AWS请求**，即使用户说明官方许可至2026-10-26；任何窗口接近导致无法在保守时间门内完成也要停止。

## 同轮附带：零GPU训练就绪度只读检查（用户要求减少轮次；不改变媒体上限）

在本父任务完成其A–F已授权阶段，**或在未开始AWS请求前的预检**，允许执行一个**不触碰GPU、不触碰训练视频内容**的CPU-only、只读、不超过2分钟的训练资格清点：只在原Codex长期会话/既有私有环境里**明确提供过的确切资产入口**查询（不得枚举全盘、搜用户下载目录或读旧科研树）以下四项匿名布尔状态：a) RTX3090本机设备存在性可否从已有非计算工具确认；b) 既存Qwen3-VL-4B-Instruct本地权重/processor是否可找到；c) 既存SigLIP本地权重/processor是否可找到；d) 是否**已明确授权且可证明与保留评测视频不同来源/不同物理素材**的合法训练视频。只验证路径或元数据存在性，不装包、不读取权重文件内容、不启动CUDA、不运行GPU/模型/解码/训练、不打开QA答案、不改训练目录和ledger。如不清楚现成确切入口，写`ASSET_ENTRY_UNKNOWN`、`TRAIN_SPLIT_UNKNOWN`即可，不得向外请求秘密路径、遍历磁盘或新增AWS调用。可把匿名四项结果合并进本父任务唯一`one-video-receipt.md`，而非新建父任务/额外结果条目。此项不得让已被安全门阻塞的媒体任务偷偷继续GET，也不改变原有唯一READY/一次push后STOP规则。

## 唯一公有交付/停止状态

- 新`docs/codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/one-video-receipt.md`：匿名报告本轮A–F实际发送与成功/失败计数、manifest完整性与50 UID匹配、候选分类一致性、2个媒体HEAD是否重现大小门、GET 0或1、STARTED预扣、应用正文与落盘容量**仅汇总或区间**、存储/容器PTS检查是否通过、资源消耗和停止状态；不公开单段可重识别确切大小/UID/媒体URI、区域/桶/ETag、QA/答案/帧、私人账户、凭据/脚本/路径/账本、视频或模型权重。
- `docs/codex-results.md`末尾只增**一个**`### VLM-EGO4D-LIVE-MEDIA-002`及报告链接；**不得改**看板、总览、旧结果、任何公共代码、旧科研环境/媒体/锁或实验成果。正常一次push main后STOP。真实结果只能是`ONE_OFFICIAL_MEDIA_ACQUIRED_METADATA_ONLY`或有具体原因的`LIVE_MEDIA_SAFE_STOP/HOLD`。**本合同的执行权限仅限上文metadata与单视频GET，不包含GPU、模型或训练；后续[真实GPU A/B合同](../VLM-HOURVIDEO-LIVE-AB-001/README.md)有已预排的具体40 GPU分钟/4次前向上限，但须到达媒体真实可用、来源/时间轴与模型门后才能确认独立运行权限，不得由本任务自行越级执行**。保持`RELEASE_AND_CLOCK_BRIDGE_UNKNOWN`直至独立证据、`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`。

## 减少往返的用户偏好（不扩大合同）

用户不希望对同一个已经批准的父任务反复询问。执行器应在本次新用户启动指令之后，**一次连续执行所有已获准的A–F安全子阶段**（在预算及独立前置门均PASS时），不中途让用户逐个批准每次HeadBucket、manifest GET或条件媒体GET。只在触发STOP或完成后提供一次脱敏报告。**不得因此转而使用LIVE-AB-001或TRAIN-GPU-001的GPU预算、获取第二个视频、重试失败GET或自动唤醒下一执行轮**。
