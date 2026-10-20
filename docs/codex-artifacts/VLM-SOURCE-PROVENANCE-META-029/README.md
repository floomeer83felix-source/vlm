# VLM-SOURCE-PROVENANCE-META-029：来源台账、固定候选资格与有限媒体HEAD整包

2026-10-20。研究负责人：ChatGPT；执行者：用户当前本地Codex会话。
本合同由028交付后的研究审查下达，**不是028自动续跑**。

**唯一READY父任务：029 / PUBLIC_PROVENANCE_CPU_ONLY。** 公共代码和虚构数据验证可领取；
下表私人读取/写入及真实S3 HEAD只有用户发送本合同末尾的明确新指令后才激活。
普通“继续”、仓库READY、旧AWS配置成功或028许可均不包含本次新数据/联网范围。
合同与启动时用户消息共同构成上限，后续仓库修改不扩张已授权范围。

## 起点与本轮目标

028交付[157ffd8](https://github.com/floomeer83felix-source/vlm/commit/157ffd8a26b0e632e57cb52b4215c8b99de8678d)
按 **ACCEPTED_CPU_COHORT_HANDOFF_PARTIAL / REAL_PILOT_HOLD** 审结。
ChatGPT静态审查八处允许差异及17项新测试，没有独立运行测试或访问私人输入。
执行者报告50来源/1182题完整解析、原语法28题、冻结4题/20选项/16计划槽位；
`SKIP_NONFINITE_028 / PROJECTOR_028_V1`当前三遍各跳过同一流中的1个未保留NAN类别值。
这不认证严格JSON，不倒推027历史失败字节；本轮不再读取原标注或改容器口径。

028的8份旧记录在有限白名单下均未恢复UID；这是**投影未获身份**，不是底层文件
没有身份。原`source_group`数组不能靠位置猜UID，但真实写入代码若证明它是
`(video_source, origin_video_id)`，并证明该artifact确由相应写入版本产生，
就可以按已证schema解释为来源组。**恢复精确旧UID不是组排除的唯一合法途径**；
已证origin组也可用于保守排除，必须保留不唯一映射和未知项。

本轮一次连续完成A–H，交付可审查的来源台账、P1–P4资格矩阵、实际媒体大小/访问
元数据及下一真实执行的具体资源提案。无真实QA、GPU、gold、媒体正文或下载。
若追溯后仍缺确切登记表/写入绑定，列出准确缺失引用并停止这条来源路线，
**不自动再排一个同类schema/资格/盘点父任务**。独立可完成部分继续交付。

## A–H连续任务

| 子项 | 工作与完成判据 |
|---|---|
| A / 固定起点与输入账本 | 安全同步独立文档checkout；读AGENTS、最新board/results/overview、本合同及028两份回执、027 backend静态报告；确认唯一未交付029。冻结输入角色、现存精确引用、版本/文件绑定、各次打开和上限。028四个源/原题索引及profile绑定只读；QA正文/选项/event值不读取，不创建新题或新plan。 |
| B / schema与写入代码 | 对已知旧记录先做一次完整流schema观察，只记录字段路径/容器类型/数组形状，不解码scalar值；动态map-key视为私人身份候选，不公开。对≤6个已有确切引用的实际producer/qualifier/runner源码做一次有界AST静态读取，不import/execute/eval。追踪实际输出字段、tuple/list/map-key语义、登记表引用和artifact写入绑定；无证明即UNKNOWN，不按字段名相似或任意UUID字符串猜身份。 |
| C / 旧来源登记恢复 | 仅对B已证字段作第二次有界投影，可读明确UID、video_source/origin组、participant、release/version、已知derivative关系与准确媒体引用。覆盖旧013/014及R1–R6，分别标明artifact已找到、writer已绑定、UID/组/participant/派生各自状态。若源码中含确定的非gold来源登记字面量，可用受限AST提取该明确结构；若引用外部registry，只可读取本表预算内、事先确切解析出的那个文件。找不到就给缺失引用类别，不目录扫描或读QA/预测结果补身份。 |
| D / 独立官方join | 一次完整读取已缓存官方manifest，按实际header保留必要字段，联合请求028固定4源及已证旧UID/origin组，不依赖标注index，不限于028保留的50行。组可多对多：保留所有匹配canonical UID/已知participant/派生，非唯一不能选第一条冒充精确旧UID。UID、recorded-origin组、participant和known-derivative证据分开。source_group已证即可判相应组重合；缺失/冲突不等于不重合。 |
| E / 固定四候选与现存媒体 | P1–P4逐一对旧013/014/R1–R6核对上述证据并报告PASS/OVERLAP/UNKNOWN及原因。P3 participant缺失只有实际可信证据能补齐，不能由不同UID/时长推断。四题/20选项/16文字plan保持不变；任何失败不得换候选、换题或默默缩分母。若现有可信记录直接给出确切本机媒体入口，可对≤4个对应文件各做一次stat（不读正文/哈希/probe）；无准确引用则UNKNOWN，不构造路径或扫描磁盘。 |
| F / 有限官方HEAD | 仅在用户本次明确授权且精确canonical对象引用/官方桶/可信region/静态profile/现有SDK均过门后，对最多4个固定候选的官方对象各一次HeadObject；必要时仅一次HeadBucket查region。实际HTTPS发送总≤5次，零GET/LIST/STS/媒体正文；细则见下。来源排除未完成不妨碍独立HEAD元数据，但HEAD成功绝不补成来源PASS。缺前置条件则该分支HOLD，完成其他项。 |
| G / 新见证与真实执行提案 | 只运行本轮新离线suite≤2次：覆盖writer证明/未证tuple拒绝、artifact绑定不符、独立旧组join、多canonical歧义、participant未知、固定候选不替换、真实发送次数和失败不退款、SDK重试/region重发被门控、GET/未知host拒绝、错误内容不泄露。全部虚构数据/transport，无真实网络。依据实际资格和HEAD/本机stat，写清原text N=4、未来可提议资格子集及排除、准确资源已知/未知、下载字节上界、仍需的权利/媒体/模型/OS隔离/gold授权；不在本轮启动它。 |
| H / 一次交付 | 只提交allowlist内代码/两份匿名报告，results追加一个029父结果，区分已执行/静态/fixture/未运行。报告所有失败、预扣/实际计数、完整性和剩余缺证。一轮一次普通main push后STOP；不自动030、不修环境或追加网络。 |

不得把“source_group语义已在某段源码出现”直接当作该私有artifact确由它产生。
绑定至少要有已知运行记录/对应写出关系/版本证据支持；仅目录邻接、文件名或同样时长不足。
源码literal只能提取已证非gold来源结构，不枚举或公开源码中的题文、答案、canary、prompt或模型输出。

## 新私人CPU输入与写入边界

精确入口沿用本地Codex会话已经确认的引用及本轮已读producer明确引用；
不要求重复上传，不搜索任意研究目录，不沿用旧父任务余量。无准确入口则相应项HOLD。
所有研究输入由**新的029持久OS锁/预扣/终态账本**统一管理，进程/continuation共享，
失败、未完整EOF或崩溃消耗已预留的角色/字节，不退款、不换路径别名重新计数。
文件身份与各自前后稳定性沿用已审原语义，拒绝变更/不完整流；不为029再放宽guard。

| 输入角色 | 本轮新上限 | 允许保留 |
|---|---|---|
| 已知028/027 nongold最小交接artifact | ≤16份，各≤1MiB，各1次open | 固定键、profile/version、来源/分组/已知引用、必要receipt完整性字段；question/options/event/gold/prediction/PTS数组值全部skip。摘要和身份只留私人。 |
| 原8份旧元数据及必要producer直接引用registry | 合计≤8个确切文件，各≤1MiB；各schema≤1次、已证身份投影≤1次，共≤16open | 第一遍不解码scalar；只有schema完整并已证字段才可第二遍投影。若需要registry，必须占8个文件名额；不得读第9份或重开已消费角色。 |
| 实际producer/qualifier/runner源码 | ≤6份，各≤1MiB，各1次open | AST字段/写入/登记关系及必要非gold来源literal；不执行源码、不做模型环境盘点。 |
| 已缓存官方canonical manifest | ≤1次open、≤8MiB，完整EOF才可用 | 实际header、固定候选/已证旧源的UID/origin/participant/release/version/canonical/时长及明确对象URI字段；无列不得补造。 |
| 原混合标注、旧逐题预测/gold、真实媒体正文 | **0次open / 0B** | 禁止为恢复身份重跑index/screen/inference或读取原QA、模型完整回答。媒体stat是上表E的独立精确限额，不是正文许可。 |

上述正文研究输入最坏46MiB，硬总上限仍**48MiB**；metadata网络headers另见F，
不得用总额空余扩张每角色次数。凭据仅由下述既有静态SDK正常使用，不进入研究输入产物。
完整schema读取仍使用现有skip-only projector及已接受的028绑定；不得另造宽松JSON清洗器、
全文mixed-container decoder、任意字符串提取器或复制原文件。

只在已知`<AUTHORIZED_018_ROOT>/integration_029`新建私有目录，全部新增
**≤128文件/32MiB**；同名既存则STOP，不删除/换后缀绕过。旧目录/锁/账本/文件只读。
公共fixture用独立文档checkout中的本轮临时目录，不能借此进入原实验根。
自有CPU/HEAD子进程各≤120s，累计受控进程窗口保守合计≤600s；
coordinator窗口≤1200s；新suite启动≤2（每次预留120s），无额外fixture worker、
后台任务、GPU查询、Torch/模型导入、包安装/升级、新环境、系统/ACL/profile改写。
预算需在启动前持久预扣，超时仅终止自己持有的本轮child，不碰不明进程/旧锁。

## F：新增官方S3 HEAD范围（须启动消息明确接受）

这项是**新的metadata网络许可提案**。已有配置或旧META任务不能自行激活。
沿用本机既有隔离Ego4D boto3/botocore SDK和专用`ego4d`静态shared-credentials
profile；缺失即HOLD，不安装/迁移/修配置。SDK调用仅在本分支child中允许。
不手工输出/复制凭据，禁环境/SSO/进程/容器/IMDS等凭据provider和STS/认证网络。
静态profile gate与SDK provider白名单必须在任何网络前确认，拒绝可刷新/外部provider；
必要的凭据只在内存中供本次已授权签名请求使用，日志中不得出现。

- 对象必须来自本轮真实官方manifest的明确canonical URI，或既有官方来源/receipt及
  实际生产代码证明的确定映射。只用已经核实的官方桶和区域端点；
  **不能仅凭UID猜拼S3 key、猜bucket/region、用v2_1代v1、访问任意URL或下载manifest**。
- 最多**1次HeadBucket + 4次HeadObject，总5次实际outbound HTTPS发送**。
  有可信region则不用HeadBucket；每个固定对象槽位只用一次，失败不重发、不补对象。
  同一对象重复别名共用一次，不因4题分配多次请求；没有准确URI即该候选HEAD_HOLD。
- botocore `total_max_attempts=1`，关闭自动重试并设置connect/read timeout各≤10s；
  不把此配置单独当作阻止region redirect的证明。实际before-send位置先持久预扣，
  核对HTTPS method=HEAD、精确host/bucket/key、候选/请求槽位，SDK隐藏重发/跳转同样受限。
  HeadBucket若得可信region，在未发对象请求前一次选定；HeadObject region错误不重试。
  若SDK无法可靠安装实际发送门，真实网络0并HOLD，不以外层调用数冒充发送数。
- 只允许HEAD，无GetObject/List/PUT/Range/presign/STS/其他host；不读取对象正文。
  任意异常响应出现body则关闭、不消费并HOLD。每请求保留响应headers≤64KiB，
  该上限指保留量，不声称已证明原始wire字节硬上限；不公开原始错误响应/请求日志。
- 仅私人保存规范对象引用、ContentLength、ETag、VersionId（若有）、LastModified、
  region和安全状态码。公开只用P1–P4、大小向上取整MiB上界/合计、状态及证据类别。
  ETag不等于内容校验和或版本认证；VersionId缺失就UNKNOWN，不虚构immutable版本。
  200只证明该次凭据可HEAD该对象，不替代有效用户许可/研究使用权、媒体完整性或物理独立。
  403/404/region/timeout按观察分类，不扩大为无该视频或无合法使用权。
- 请求失败不通过延长超时/重试/改host/改profile续跑。即使F缺证仍交付A–E/G/H。

技术依据（执行前不另增网络查询）：[AWS HeadObject](https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/head_object.html)
说明HEAD只取对象metadata；[botocore Config](https://docs.aws.amazon.com/botocore/latest/reference/config.html)
说明total_max_attempts包含首次尝试。本合同额外要求实际发送门，不能靠文档假设SDK无重定向。

## 来源口径、未来实验与止损

- 已证UID/记录origin组/participant/known-derivative分别裁决。不同UID不证明不同录制，
  缺字段不能自动PASS；同组匹配要保守排除其全部已知canonical别名。
  本轮目标最高为 **RECORDED_GROUP_SEPARATION_ONLY /
  PHYSICAL_RECORDING_INDEPENDENCE_UNKNOWN**，不要求凭现有metadata伪造物理独立证书。
- 不能因某候选不合格替换028已冻结题。G可以**提议**下一合同的合格子集，但必须清楚写
  原冻结4题及每项排除，在任何真实模型输出前由研究负责人另行冻结新N、轮转和完整分母；
  本轮028文字plan不改，不运行或计分，不能把16计划槽位冒充16次已准生成。
- 下一提案对实际可用N给出4N调用、48N共同候选帧、12帧/臂等原设计量，
  下载上界以HEAD ContentLength/准确本机stat为据；有缺失就UNKNOWN，不按时长猜码率。
  下载缓存/临时空间可给明确**拟议**数值与依据；CPU解码/GPU时长/token/峰值VRAM
  若无本批实测只列历史参考和拟议cap，不声称测得或已授权。不启动后端再补数。
- 当前真实backend静态factory/closure证据复用027报告；本轮源码读取只解决来源写入语义。
  processor/token一致、真正模型资源约束、OS gold拒绝及最后独立评分仍须后续具体合同；
  不能由Python逻辑门或HEAD成功认证。无权利/来源组闭合则真实运行NO_GO/HOLD。
- 如果B–D仍不能恢复013/014或R1–R6登记关系，最终列出准确缺失的登记/版本证据，
  交回用户/研究负责人作补充该具体资料或停止该来源路线的决定；**不自动030再试一遍**。
  无新模型对照结论：REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；
  CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。

## 公共执行allowlist（仅7处）

1. `prototypes/source_provenance_029.py`：通用有界schema/已证字段映射/组join/固定候选资格/HEAD实际发送门。
2. `prototypes/source_provenance_coordinator_029.py`：可审查公开协调器，public fixture与明确授权private/head模式分开；真实入口来自本机私有参数，不写进源码。
3. `prototypes/test_source_provenance_029.py`：本轮新合成证据/传输门测试；不调用任何旧suite。
4. `prototypes/temporal_pilot_coordinator_027.py`：仅在确有需要时为Journal增加固定029 contract/root白名单并复用原子预算能力；不改027/028模式、解析/题型/监督器或放宽原guard。能直接复用则不改。
5. `docs/codex-artifacts/VLM-SOURCE-PROVENANCE-META-029/source-and-media-metadata-receipt.md`：A–F/G验证及资源/失败/证据等级匿名回执。
6. `docs/codex-artifacts/VLM-SOURCE-PROVENANCE-META-029/real-execution-proposal.md`：固定四候选资格、原N/提议子集、媒体与成本、明确仍待授权项或路线停止理由。
7. `docs/codex-results.md`：末尾仅一个029父结果，链到两报告并列A–H状态。

不改本README、AGENTS、board/overview、旧报告/旧测试/025研究协议/adapter/scorer/supervisor。
不上传真实UID/来源映射/组键/participant值、题/选项/gold/预测/私有路径/URI/摘要/凭据、
原始manifest/代码literal/媒体或响应。公共报告可写schema证据类别和匿名裁决，动态字段键不公开。
公共代码只含虚构例子。提案没有测得的量保持UNKNOWN，不制造空成功收据。
检查stage路径及内容后一次普通push main，禁止force/reset/rebase，失败留现场并汇报，随后STOP。

## 用户发送给当前Codex的一条启动指令

下列消息同时授权本轮必要私人CPU范围和新增有限S3 HEAD；用户实际发送才生效：

> 安全同步独立GitHub文档仓库main，重新读取AGENTS.md、docs/next-steps.md、
> docs/codex-results.md、docs/research-overview.md及029 README，确认唯一未交付READY
> VLM-SOURCE-PROVENANCE-META-029。我明确授权README所列新029范围：
> 对已知精确028/027最小交接、旧元数据/直接引用registry、producer源码和缓存官方manifest
> 做有界nongold来源/schema读取（累计≤48MiB，原标注/QA/gold/预测/媒体正文0），
> 只在已知018根下新integration_029写≤128文件/32MiB；CPU≤600s、coordinator≤1200s、
> 新离线suite≤2。另明确允许既有隔离Ego4D SDK使用静态ego4d profile，
> 仅对有官方精确canonical引用的固定P1–P4做HEAD元数据：HeadBucket≤1、
> HeadObject≤4、总实际HTTPS发送≤5，失败不重试，媒体GET/LIST/STS/正文均0。
> 按A–H连续完成schema/writer核实、旧来源台账、独立组join、固定四候选资格、
> 现存媒体精确stat/有限HEAD、新离线见证和实际资源提案；缺证如实HOLD并完成其他独立项。
> 不换题或候选，不重跑028或任何旧任务/旧测试，不做模型/Torch/GPU/真实gold/下载/
> 安装/配置/ACL改变。只提交allowlist代码、两份匿名报告及results一个029父记录；
> 一次安全推送main后停止，不自动030。
