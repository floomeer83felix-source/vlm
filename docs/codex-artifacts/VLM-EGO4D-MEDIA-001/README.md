# VLM-EGO4D-MEDIA-001｜官方已获批访问：至多两段同UID长视频，严格8 GiB累计GET预算

**2026-10-12｜ChatGPT冻结一次性READY父任务｜用户明确回复「好的」批准前述「至多2段、累计8 GiB、每段≤4 GiB、0 GPU」首次真实视频获取。** 用户转述Ego4D官方批准通知有效期至**2026-10-26**；本任务在其**原来唯一连续的Codex对话**由用户主动发消息启动，**main中READY本身不会自动执行**。这是新的受限访问任务，**不恢复**旧REAL-PILOT-001、Charades/BATCH-014至020或旧下载/GPU剩余配额。

## 一、严格前置条件（任一UNKNOWN即安全停止下载，不做其它替代实验）

1. **任务与工作区门**：仅在**独立的公开Git文档checkout**做`git status --short`→`git fetch origin main`→确认可安全fast-forward→重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[HourVideo开发标注真实资格收据](../VLM-HOURVIDEO-DEV-001/local-annotation-eligibility.md)、[合成runner收据](../VLM-SYNTH-AB-HARNESS-001/synthetic-runner-receipt.md)与Ego4D官方[CLI说明](https://github.com/facebookresearch/Ego4d/blob/main/ego4d/cli/README.md)。**恰好一个READY且ID为本任务、结果末尾无本ID先前任意报告**，否则STOP；不reset/rebase/force-push、不清理其它分支/旧锁/账本。
2. **权限门**：Ego4D正式批准仅基于用户亲自转述邮件；应在本机通过**用户已经私下配置**的**唯一明确Ego4D用途AWS profile**或已存在官方 CLI 的非敏感连接检查来验证是否确有权限。有效期限到2026-10-26，**不在过期边缘（当日可能有时区歧义）发新媒体请求**；最迟2026-10-25北京时间24:00前开始且需完成。不得由Codex打开私人邮箱、复制签约文件/证书、询问/回显Access Key/Secret/Session Token、读取或上传原文credentials、登录用户账号、发外部联系/申请、修改AWS配置/环境变量或创建AWS账号/收费资源。若无已安全配置的凭据/权限不足，`CREDENTIALS_NOT_CONFIGURED_OR_DENIED`→STOP，请用户仅在本机按官方流程自行配置，**不要把凭据放入Codex聊天**。
3. **数据门**：只能按上轮 Codex 已明确取得的**那一个本地**`dev_v1.0_annotations.json`文件路径（先前用户自行指定下载目录）只读解析**顶层视频UID及`video_metadata.duration_in_seconds`字段**，不读题目内容作选样依据、不回显`qid/question/mcq_test/correct_answer_label`或任何canary；禁止漫游Downloads/全盘搜索或复制原JSON。HourVideo 50视频/1182题的**标注容量**已通过，不需重做已结案资格分析。用官方[Ego4D CLI与授权`full_scale` manifest](https://github.com/facebookresearch/Ego4d/blob/main/ego4d/cli/README.md)做私有**确切video_uid存在性**及版本标记对齐；若已有可信本地HourVideo官方`v1.0_release/video_uids/`开发集UID清单可离线交叉核对，但**绝不为此下载其他HF受保护QA、test/samples、附图/字幕/特征或视频**。不得把相近名字/clip_uid、HourVideo视频名、时长接近或任意字段误作同版匹配。**只选择Ego4D canonical`full_scale`视频，禁止`clips`、`video_540ss`、可视化文件、剪辑拼接和其他镜像/第三方链接**。
4. **不偷用答案选视频**：仅用非答案元数据的冻结确定性规则排一个私有候选序（优先至少20分钟，至少一段标注≥30分钟，如有两个均已确证可下载），仅对前面明确符合的至多2个不同**视频UID**尝试；不足2就取1或0，绝不为了填足配额扩数据源/来源范围。把私有UID↔源版本↔下载对象↔标注文件身份、来源合法性、大小依据和候选排序仅记在本地新隔离目录；公有Git和聊天不贴视频UID、密钥、完整S3 URI、视频名称、私人路径、QAs、答案、时间戳明细或可回溯组合。
5. **现有工具门**：只可利用本机**已安装且用途确认的**`ego4d`、AWS CLI / Python boto3（若已存在）及标准库。不得`pip install`、conda安装、升级/更换Torch/CUDA、下载模型、使用新工具/代理/付费API或修改用户环境。官方CLI支持按`--video_uids`精确限视频和`--no-metadata`避免附带全库元数据；**必须验证当前本机实际CLI版本/执行计划确实尊重精确过滤**，不能直接运行`ego4d --datasets full_scale`的未过滤命令、不能隐含全库元数据下载。若工具缺失，则`SAFE_TOOL_MISSING`→STOP，而非安装。
6. **来源/体量门**：下载前用已获授权官方manifest和**精确对象**`HEAD`/等价元数据得到唯一对象ID、`Content-Length`、发布版本/存储源以及支持的ETag/校验字段（私有不披露）。确认UID在开发标注与该发布版本的官方canonical full_scale中均确实匹配，**若显式版本/身份矛盾、无法辨认实际对象、长度UNKNOWN或对象出现替换迹象，STOP，不尝试GET**。不同JSON顶层键只能表示两条标注记录，不能自动证明独立原始拍摄源；本轮不宣称完成24题/12段的同钟桥接。
7. **存储/写权限门**：用户私人Windows本机明确的一个**新且不存在的隔离实验数据目录**存放下载视频、metadata与安全预算账本；优先同级私有位置，不使用公开Git checkout、旧Charades下载目录、旧Windows研究原树或Downloads任意地方，不覆盖现有视频、已有.partial、同名文件、源实验锁/ledger/research_state。检查可靠剩余磁盘空间≥计划对象大小总和+2 GiB工作余量；未知/不足STOP。不要把源视频/metadata/私有UID清单复制到公有仓库或codex日志。

## 二、硬下载预算（**8 GiB=8,589,934,592 B**，每个视频**4 GiB=4,294,967,296 B**；非承诺一定下载两段）

- **媒体下载尝试至多2个不同UID/对象**；每个官方原视频的`Content-Length`必须≤4,294,967,296B；总**所有网络GET正文累计字节**（包括官方必要的小型manifest或临时GET、HTTP失败正文、重试与部分传输）≤8,589,934,592B。与任何历史Charades配额完全隔离，但本任务自首次GET开始即**跨中断/重启不可清零**。非媒体元数据正文保守子限≤32 MiB并计入8 GiB总额；优先本地已有或只用HEAD，不得以此批量获取全库。旧历史GET/缓存不得算作新的授权视频。
- **运行前两重预算约束**：每个候选先获真实`Content-Length`和同源版本证据，若任一单视频/预期GET和≤预算则不得请求；**实际每次GET的数据流必须以持久累积的不可回退预算表/可验证的限流代码逐字节或有保守预扣上界执行**，提前为该GET+可能的传输开销预留额度，接近限额立即停；同时检查磁盘占用和临时文件。不允许依靠“CLI可能只下载两段”“最后看落地文件大小”代替传输硬限。**官方CLI若不提供可验证的传输上限和重试计数，应先STOP该方式；若本机已有安全受控的SDK，可以使用私有的、已测试的单对象HEAD+固定上界流式GET机制**（禁自动重试或必须跨重试计入实际耗用），而不能悄悄放宽计数；SDK不存在或严格流控无法证明时`TRANSFER_BUDGET_UNENFORCEABLE`→STOP。禁止并行/后台自动重试/无限循环；任何连接中断或响应大小/ETag版本不一致，保留已消费的累计预算与partial证据、停止本轮，不续跑两段以外对象。
- 只对官方S3已授权精确对象执行GET，不采纳标注内容里任意外部URL、重定向至第三方站点或未经核验的镜像；有代理/HTTPS身份不明、来源或Range206不符合期待时STOP。不可复活过去Charades的ffprobe工具下载/原部分包/resume计划。
- 成功后私有空间记录每个已完成对象的流经字节数、最终文件字节数与HEAD声明长度的一致性、源版本/ETag/可用性；计算本地SHA256只在私人安全记录中，**不把SHA冒充官方发布checksum或将multipart ETag当作MD5**。可以只读运行已存在的`ffprobe`做新下载文件的**container-level duration**（不解码像素、不扫所有packet、不转码）来检验≥20min且大致吻合HourVideo metadata；无ffprobe就记`MEDIA_DURATION_UNKNOWN`，不安装。UID对应≠逐帧PTS同钟/问答证据定位已认证，不能直接跑模型。

## 三、任务结果与失败即交接

- 至多一次实际本机试点；若前置门任何项UNKNOWN，则明确`PREFLIGHT_STOP`，**0媒体GET/0GPU**；若已成功下载1段、另一个因限制或网络停则`ONE_MEDIA_ACQUIRED_PARTIAL`；成功2段（身份、长度/来源、一致性符合）则`TWO_MEDIA_ACQUIRED_METADATA_ONLY`。任何异常都保留**实际视频GET数、已传输字节数（整数聚合）、当前私有原视频数、累计预算使用、0GPU、未满足的门**，不得假报已获得同钟、全12段或24题模型正确率。完全不需要访问24题答案或运行合成A/B程序。
- **禁止GPU/CUDA/模型运行**：0 Qwen、0 SigLIP、0训练、0VLM前向、0帧提取、0像素解码、0人工答题/标注或测试集调用。不可修改模型、环境、原研究树、原锁或旧started账本。不触碰Charades。任何真实QA评分/模型/GPU预算下一轮由用户另行批准。
- 公有Git**严格只允许**新建`docs/codex-artifacts/VLM-EGO4D-MEDIA-001/limited-media-receipt.md`一份**聚合匿名收据**，和向`docs/codex-results.md`最末尾**仅追加一条**`### VLM-EGO4D-MEDIA-001 ...`父结果。代码或预算/下载工件只可保存在本机新隔离目录，**不可提交工具脚本、视频、metadata/manifest或私有UID/QA、Ego4D AWS配置、完整URL、文件名、个人路径、密钥及内容哈希**；两处差异的`git diff --cached --name-only`必须检查并对拟上传内容脱敏。任务书与其他ChatGPT持有的`docs/next-steps.md`、`docs/research-overview.md`、`AGENTS.md`、历史回报一律不改。
- 收据至少报告：官方许可审批用户确认而本机权限访问PASS/UNKNOWN；UID join数量（聚合但不可列UID）、v1/v2或其他版本证据仅指类别、总候选/筛选数、远程大小是否逐对象已知、0/1/2实际下载成功数、总媒体文件字节数与总网络GET正文实际累计字节数及用掉的8GiB预算、是否用媒体头确认时长、工具/重试/错误情况与安全停止原因。不能把未跑的步骤填PASS。对于总GET计数若不能可靠观测，应在GET前STOP，不能在报告伪报0或按文件大小猜测网络耗量。
- 如遇用户需要自己配置凭据、安装已有工具之外的CLI、真实视频对象长于4GiB、下载需要额外元数据许可或任何歧义，按协议立即STOP并简洁请求ChatGPT重新决策，**不擅自发下个任务、扩大预算、开GPU**。安全完成后对公有main仅一次正常commit/push，保留相同Codex聊天，STOP。当前只有本任务READY，绝不以本任务通过视为后续12视频48 Qwen调用自动获批。

**研究事实边界**：HourVideo开发集50视频、1182问题只属已验收metadata层；Ego4D有效批准至10/26来自用户转述。拿到至多2段canonical视频，最多证明小样本来源/物理存在与粗时长；不是新的原创算法、QA表现/事件GT、全部12视频的独立性或时钟同版证书。研究创新`NOVELTY=RETAIN0`，Charades`FINAL_MEDIA_STOP`保持。
