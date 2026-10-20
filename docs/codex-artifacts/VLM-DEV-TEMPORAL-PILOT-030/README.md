# VLM-DEV-TEMPORAL-PILOT-030：真实四臂开发诊断整包

2026-10-20（北京时间）。ChatGPT研究规划；用户当前Windows RTX3090本地Codex执行。
**唯一READY父任务：030 / PUBLIC_IMPLEMENTATION_ONLY。**
真实数据/网络/媒体/模型/GPU/gold由本文末尾一条用户明确启动消息同时激活；
“好的”已接受科学口径，不把它冒充尚未列明的资源操作许可。不得先跑再补授权。
合同与启动消息构成上限，后续仓库改动不自行扩张已授权范围。

[新科学协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)
是本轮科学依据。029已按SOURCE_ROUTE_STOP_MISSING_PROVENANCE关闭；
本轮不重做来源登记/新源资格门，不用029余额，不重开旧父任务。
这是用户明确接受新口径后的独立真实实验，不是029自动续跑。

## 一、明确改变与固定内容

**DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。**
允许来源可能与旧013/014/R1–R6重合；P3 participant缺失明记，不作为本轮入门否决。
不声称来源分离、未见题、held-out、物理独立或正式HourVideo成绩。
既有Ego4D/HourVideo有效研究许可、具体官方对象身份和媒体/模型资源边界仍须满足；
不要求一份现实中没有的物理独立证书，也不再追索旧登记表。

固定028四源/原题索引及20选项，N=4、16调用槽位，原ABCD/BCDA/CDAB/DABC轮转。
A Uniform、B全局Top12、C无序双锚点、D有序双锚点，完全复用025算法。
C/D同两个锚点、同a/b/q分数和补齐/tie，只差i≠j与i<j。
不修改grammar/selector/profile以满足数量，不换题、替换来源、重排或按结果省调用。

用户新启动消息明确允许这四题在新030 run每臂回答一次，即使旧研究答过同题；
这是对本030固定16槽位的有限新授权。其他历史前向禁止规则不变，
旧013–029不重跑、不导入执行旧runner顶层、不消费旧attempt或GPU余量。
旧逐题预测/金标/评分结果0读取，不用于选题、prompt、超参或结果补齐。这里“旧金标”指历史评分产物；原annotation中固定四题gold只按本合同最后一次受控新评分读取。

## 二、A–H一次连续执行

| 子项 | 实际工作与完成判据 |
|---|---|
| A / 冻结与审计 | 安全同步独立docs main，读AGENTS、board/results/overview、本合同/新协议、028/029回执与027 backend报告；确认唯一未交付030。新integration_030原子创建，新run_id和持久账本；核对四键、20选项、plan/轮转、profile和028完整原输入receipt。用户启动消息同时声明现有许可仍有效，仅本许可范围非商用研究；沿用既有Ego4D/HourVideo批准依据，不以HEAD替代许可、不另外要求新证书。若声明与已知条款冲突则STOP。 |
| B / 真实后端与隔离接通 | 复用027两个已知static factory及实际inputs(i,ids)的已知源码AST，提取原helper/system/prompt/processor配置到本轮私有adapter；不import执行旧runner。准备纯nongold worker输入与下面OS share-lock/自有PID监督，先用本轮合成见证证明保护门；不再复跑025–029 suite或做环境盘点。没有真实隔离/资源限制不能启动模型。 |
| C / 精确媒体就位 | 使用029保存的四个准确官方canonical URI与SDK官方bucket白名单、原028源/release声明。若已有确切媒体引用且有可信对象→本机文件绑定，可只读核验复用；不能猜目录/文件名或按时长/大小猜UID。否则按第三节新上限刷新metadata并单对象下载。各源独立失败记四槽NOT_RUN，继续其他固定源；不等四源都成功才做可执行部分，不换对象或借余额补源。 |
| D / 真实CPU候选 | 对每个可用固定媒体核对精确对象/字节/私有SHA及container/video duration与原声明；报告差异。与原canonical视频声明比较容差max(0.10s,2/fps)（无可靠fps则0.10s），不调偏移。可有界packet demux至EOF及48目标seek/decode，预算内完成；不要求逐帧全片pixel decode，不把B-frame packet PTS重排本身当时钟失败。48实际解码候选PTS须有限严格递增，记录实际解码量/覆盖；失败该源NOT_RUN。所有16槽及前置NOT_RUN在模型前冻结，至少1源具备媒体与隔离才进入E，否则GPU/gold0并STOP。 |
| E / 真正四臂推理 | 一次受监督GPU worker，现有Qwen3-VL-4B BF16/SigLIP F32及原local-only处理器/SDPA，seed19、do_sample=False、max_new_tokens=64；零训练。各源共享48图像特征，问题/事件A/B文本分别编码，q/a/b原始cosine仅此一次；C/D共享分数，选项只进Qwen。按原顺序每计划槽最多一次generate；真实12帧/grid[6,12,18]/324 visual tokens逐调用验证，其他总token长度可随timestamp变化。C=D也各回答，不复用答案。记录截断、EOS、成本/显存；OOM/异常不重试、不切dtype/模型/帧数，终止自有worker，余槽NOT_RUN。 |
| F / 队列关闭与独立评分 | 记录每槽RETURNED/INVALID/FAILED/NOT_RUN，Popen/Job实际确认模型PID及其自有子PID退出，关闭队列并fsync；再解除原标注共享锁并启动单独可信CPU scorer一次。按025 scorer/028profile只投影四题gold，完整原流hash/size匹配后才发布。最多一次open，错误仍消费。没有实际调用过Qwen.generate则gold0；坏gold/绑定失败报告UNKNOWN，不缩N、重开或提前验gold。 |
| G / 科研分析 | 全四源逐臂correct/N4及完成/INVALID/FAILED/NOT_RUN，六对配对表、C=D率、锚点/跨度/bin代理、选帧变化与额外q/a/b编码成本；主要看C–D，不因小样本变化宣称优势。区分实施失败和实际问答错，不从相似度猜真实事件命中/原因。不展示任何题/选项/gold/原始回答或身份。 |
| H / 一轮交付 | 只提交allowlist代码、真实运行与科学结果两报告，results末尾一个030父记录，明确所有未运行/失败与实际预算。一次普通main push后STOP，不自动031/扩大样本/训练；有真实结果也不改阈值重试，没有结果也不再自动安排同类空门。 |

## 三、新资源硬上限（全部新预算；不是实测消耗）

| 项目 | 本轮上限与消费规则 |
|---|---|
| 固定题/调用 | 4题×4臂=16槽；Qwen generate≤16，每槽预扣且失败不退款；真实GPU worker启动≤1，不因崩溃/新聊天重启。NOT_RUN保留完整N4。 |
| GPU阶段 | 累计≤900s（15分钟），含load/图像与文本编码/selection/processor/generate；PyTorch peak allocated≤18GiB；同一worker Job进程内存≤24GiB。仅一次既有nvidia-smi只读查询确认无其他模型/训练任务且可用VRAM≥20GiB，桌面占用记录、不杀其他任务；无法测量/约束就GPU0。 |
| CPU/父时限 | metadata/新验证/接入/最终评分自有进程窗口合计≤600s；媒体demux/decode≤1200s；网络获取窗口≤3600s；GPU阶段≤900s；父coordinator≤7200s。各阶段预留前不启动，嵌套自有PID保守计入本阶段，不能双用不同阶段余额。 |
| 子进程 | metadata/score各≤120s；新suite≤2次，每次≤120s且计入600s；其中虚构worker≤12个、各≤5s、串行且总计入600s；媒体每源≤300s/合计1200s；每GET≤900s/总获取3600s；GPU child≤900s。仅终止自己持有的Job/PID，管道≤64KiB/路、固定错误码，原始模型reply每槽≤8KiB且仅私人。 |
| 新S3 metadata | 每不同官方bucket HeadBucket≤1、合计≤4；每固定对象HeadObject≤1、合计≤4；有029可信region可复用，region未知才discovery。实际HTTPS总上限见下，失败不重试或自动跳转；记录bucket状态/region，不重犯029状态未持久化。 |
| 单对象GET | ≤4个精确固定canonical对象各1次GetObject，单对象ContentLength≤4GiB，研究媒体实际正文累计≤16GiB；P1须与029同对象且ContentLength≤890MiB并核对已保留ETag/VersionId（若有），变化则该源HOLD。P2–P4新HEAD定值，超过4GiB直接NOT_RUN，不读正文。 |
| 实际网络发送 | HeadBucket≤4＋HeadObject≤4＋GetObject≤4，合计**≤12次实际HTTPS发送**，每失败尝试/SDK隐藏重发也消费且同slot拒绝第二次。只现有隔离Ego4D SDK/静态ego4d profile，GET/HEAD以外API0，无LIST/STS/presign、额外manifest/模型GET、resume/Range/重试或重新下载.partial。 |
| 新私人写入 | 仅已知018根下新integration_030，≤384文件/24GiB；其中media（包括.partial）合计≤16GiB、frame cache≤4GiB、其余metadata/code/日志≤32MiB。逐次按已知对象长度、该源frame cache预留与2GiB余量核对目标volume空间；所有写入前预扣并防溢出。现存同名root即STOP，不删/换后缀。 |
| 研究文本输入 | 028/027/029已知nongold交接≤12份、每份≤1MiB各1open；已知runner/factory及现有SDK source合计≤7份、每份≤1MiB各1open；必要现有model config≤4份、每份≤1MiB各1open。原annotation只在最后score≤1open/≤4MiB。最坏27MiB，硬总≤32MiB。 |
| 其他原资料 | 原annotation准备/index/screen/inference正文0；旧来源八文件/旧QA/旧gold/旧预测/旧评分0open；官方原manifest0open（复用029绑定投影）；研究目录扫描0。无模型/环境/包下载、升级、训练、人工label、系统/ACL/profile改写。 |

frame cache使用保持像素一致的RGB/无损表示；不得为满足上限另加JPEG有损压缩或改变原helper预处理。原始分辨率导致超4GiB则相关源NOT_RUN，不偷偷降图。

正常本地模型/processor/SDK依赖加载是本轮明确允许的API操作，限已知现存资产/库目录，
不冒称全部权重/依赖磁盘I/O计入32MiB研究文本预算。权重只读、不复制进integration_030。
slot STARTED必须在generate前fsync；返回的受限原文/严格解析/TERMINAL逐槽持久化。worker异常后STARTED但无终态记FAILED，未开始记NOT_RUN，不因崩溃补答。

新根的自己媒体/帧/nongold输出可按既定阶段使用，但不重开原始研究输入换alias退款。
确切入口沿用当前本地Codex已知028/029 artifact和027源码引用，不要求用户重复给原路径，
不猜缺失媒体路径、不搜原实验目录。真实输入不在ChatGPT本次规划环境访问。

## 四、媒体获取的可审查实现要求

新metadata phase只用029已保存的完整官方canonical投影与确认过的四个opaque URI；
核对其UID与固定四键/release1声明，SDK官方bucket白名单和可信region，不能用UID猜key、
追加.mp4或以v2_1替换v1。已有可信region避免无用discovery；未知region用本次该bucket
唯一HeadBucket读取可信响应region，再一次固定对象endpoint，错误不重发。
用户现有批准/有效许可声明作为本轮权利依据；若明确许可范围不覆盖某对象则不获取。

沿用029在credential resolution前仅装静态shared-file provider的做法，
不读取/输出/复制凭据，不触发SSO/IMDS/容器/外部credential_process/STS，
不改profile或系统环境；本轮client禁proxy、TLS verify开启、SDK total_max_attempts=1。
真正before-send持久门核对method/host/bucket/key和slot，禁自动region resends。
底层retry/preload静态绑定现有SDK，不能只靠外层调用数认证实际发送数。

GetObject只在HEAD200、精确ContentLength/ETag（及若有VersionId）预扣并冻结后发送，
用IfMatch及已知VersionId绑定；弱/缺失ETag且无可用版本绑定则HOLD。
请求connect timeout≤10s、body read timeout≤90s、每GET墙钟≤900s；
Body不得被SDK预载或transfer manager并发获取。收到GET headers后在任何read前核对
状态/ContentLength/ETag/VersionId及固定对象，失配关闭不读、不重试。

流式chunk≤1MiB，每次read前持久预扣该次最大读取量；失败/崩溃预扣不退款。
对象和总预留不得超HEAD长度/4GiB/16GiB；到声明长度后确认SDK EOF/响应完整性，
不得为了探测多余字节读越预算。保存新根独占.partial，完成长度/流EOF/私有SHA/稳定性后
仅同目录原子rename，不复制整媒体造成双份，不覆盖原文件。失败部分保留并计入24GiB。
ETag不当内容hash；私有本地SHA只证本地字节连续性，不伪造远端checksum或immutable证书。
头部保留每次≤64KiB，仅记安全状态/常量错误类别；不公开URI/headers/签名/错误正文。

HeadBucket/HeadObject绝不读body；GET合法媒体正文只在上述门后读。
若某源HTTP403/404/timeout/资源不足，只记录观察与四槽NOT_RUN，其他固定源可继续。
没有补选、重传、剩余3次再试P1或延长超时的隐含权限。

技术参考：[AWS GetObject](https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/get_object.html)。
本轮要求的IfMatch/版本/长度/实际发送预扣是合同边界；实现必须公开可审查。

## 五、真正的本轮gold隔离与可信评分

原annotation精确入口来自已知027源码与028完整receipt；父只作身份/stat检查，
为隔离持有**1次正文0B的非继承独占handle**，不提前读任何annotation字节。
Windows CreateFileW(OPEN_EXISTING, GENERIC_READ, share-mode=0)，不改ACL/文件属性。
独占成功后，在单独nongold探针child最多2次尝试普通read-open原入口/已知规范别名：
预期ERROR_SHARING_VIOLATION，均不得read正文；意外打开立即close并整包GPU/gold HOLD。
先用新根虚构canary验证同一OS路径，属于本轮新suite，不用真实gold做内容自测。
探针≤2个自有child、各≤5s计入600s，不额外跑历史fixture worker。

父在所有模型child存活期间始终持有该handle，handle不可继承，
模型子进程只拿本轮nongold文件和帧路径；模型加载前由父Job/管道握手许可。
实际监督其Job/PID生命期、父异常则Kill-on-Job-Close仅终止本轮worker；
不得用任意boolean、同进程callback或模型内audit hook替代实际退出证据。
GPU child无原annotation句柄/凭据，网络禁用；Python读取allowlist也阻止已知其他旧QA/
预测/gold路径。不要复制导致020问题的递归Path.resolve全局open hook；
原模型本地DLL加载所需API不能被随意阻断再当成环境损坏。

Microsoft说明share-mode=0会拒绝后续read/write/delete open直到handle关闭；
参考[CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)。
这是本轮已识别原annotation文件的OS共享拒绝，不是全机任何未知答案副本或恶意
特权/native raw-disk进程的全面sandbox认证。报告实际保证及残余边界，不夸大。

所有16槽终态、model Job无存活进程、退出receipt与run/queue/hash相符后，
父先关闭队列/fsync并关闭自己的模型侧资源，再释放独占handle，启动独立可信CPU scorer。
score预扣guard写入磁盘后才能open原annotation；任何失败不重启scorer。
最多1遍≤4MiB，profile SKIP_NONFINITE_028 / PROJECTOR_028_V1，
只解码四固定题correct_answer_label，其他保护值词法skip；
用028完整raw digest/size和本轮plan/ledger/退出receipt绑定后才发布聚合。
期间原文件变更/不完整读取/坏gold导致UNKNOWN，不更换快照或再跑模型补答。

## 六、实现与验证边界

新增公开030模块承载可审查协调器、持久OS锁/hash链账本、分阶段预算、实际SDK发送门、
可继承的文件身份/完整流绑定、独占share-lock、自有Job监督和CPU score入口。
可复用025 adapter/scorer与026/027已审纯函数/锁/错误码思想，但不能直接调用其
fixture-only的5秒/16或24虚构worker/600s合同当成生产GPU授权，也不放宽旧模块的限制。
030自己固化新run/路径与本表cap；不得创建另一个对象、mode、聊天或后缀绕过消费记录。

公共实现阶段的新suite只用独立docs checkout临时目录/虚构integration_030，不进入018根；实际用户启动后若尚未跑suite，才可在新授权根做本轮suite。两种模式共享本父任务最多2次suite额度，不能公共/私人各跑2次。

两次以内新suite应集中验证新的真实连接风险：全部16槽冻结和终态/denominator、
输入绑定不符/半读拒绝、GOLD提前零opener、Windows canary share拒绝/释放后独立评分、
自有Job退出/超时及健康peer不误杀、SDK实际发送去重/低层retry、GET长度/ETag/version/
字节预扣/截断、OOM不重启、媒体不可用四槽NOT_RUN、fixture完整四臂→退出→独立score。
只用虚构数据/transport，不重跑025–029 tests，不用合成pass冒充真实processor或OS结果。
suite缺陷可在尚有第2次启动额度时修正；仍失败则本轮真实阶段STOP，不再补第3次。

本轮GPU从进程启动到结束只有一次；Job/显存/墙钟门在重工作前有效，
若硬性资源门无法实施则不加载模型，不以“想试一下”替代。
加载前用现有Torch allocator per-process memory fraction实现≤18GiB的本进程分配边界，并监测实际peak；这不宣称覆盖所有driver/非Torch显存。峰allocated超过18GiB、900s或Job内存边界时记FAILED/NOT_RUN并终止自己的worker；
不依赖启动后的第一次OOM来提高cap。没有optimizer/backward、LoRA或training step。若C/D对某题选中同一12帧且实际prompt/tensor绑定一致却回答不同，报告可复现性/实现问题，不把差异归因顺序约束；全部C=D时明确NO_REALIZED_SELECTION_CHANGE，不改规则补找正例。

## 七、公共执行allowlist（仅7处）

1. prototypes/development_pilot_030.py：新固定030协调器/账本/OS隔离/网络/CPU score与调度。
2. prototypes/development_media_030.py：通用准确对象获取/绑定/CPU候选/限制，不含真实入口。
3. prototypes/development_worker_030.py：nongold-only实际模型adapter/四臂调用入口，无默认模型/数据路径或import-time重工作。
4. prototypes/test_development_pilot_030.py：本轮新连接见证。
5. docs/codex-artifacts/VLM-DEV-TEMPORAL-PILOT-030/real-run-receipt.md：实际输入/来源口径、许可声明、HTTP/媒体/OS/PID/token/GPU/失败/预算。
6. docs/codex-artifacts/VLM-DEV-TEMPORAL-PILOT-030/scientific-results.md：完整N4/16槽、逐源四臂/六配对/选帧/C=D/成本/限制与是否值得扩大。
7. docs/codex-results.md：末尾只追加一个030父结果，链接两报告。

不改本README/新协议、AGENTS、board/overview、025–029公共代码、旧tests/报告/历史结果。
若复用代码遇真实接口缺陷，允许在新的030 adapter内作有明确见证的局部适配，
不得静默改算法、旧contract或多开来源预检。准确私有原helper只留新私有目录，
公共代码只提供通用函数/虚构fixture，不复制含私人路径/题文的旧代码。

公仓不出现真实UID/组/参与者、原题/事件/选项/gold/逐题模型原文、路径/URI/摘要、
权重、媒体或凭据。原始预测只留私人供一次可信评分；精确PTS/完整选帧索引/a/b/q向量仅私人，公开跨度取整秒及匿名覆盖汇总，其他公开仅匿名聚合/代理指标。
报告应区分实现/fixture/实际OS/实际API/实际模型测得/未执行。
本轮未产生真实QA时明确REAL_QA_NOT_RUN，不能以测试通过或HEAD当效应结果。
有QA也最多EXPLORATORY_DEV_RESULT，NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED，
Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。一次安全push main后STOP，不自动031。

## 八、用户发送给当前Codex的一条完整启动消息

下面消息由用户实际发送才启动真实资源阶段；它不需要再回ChatGPT等待另一轮“激活”：

> 安全同步独立GitHub文档仓库main，重新读取AGENTS、next-steps、codex-results、
> research-overview、VLM-DEV-TEMPORAL-PILOT-030 README和新开发诊断协议，确认唯一未交付READY030。
> 我接受SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE的开发集诊断：
> 原4题可与旧源/旧题重合，不声称独立验证；本新030 run允许这4题逐臂各回答一次，
> 包括旧研究可能答过的题，旧父任务/原记录不重跑不改。
> 我确认本轮继续在我已有的有效Ego4D/HourVideo研究许可范围内使用素材。
> 明确授权README的私人输入/新integration_030写入、准确官方metadata和单对象媒体获取：
> HeadBucket≤4、HeadObject≤4、GetObject≤4，实际HTTPS合计≤12，失败不重试；
> 每视频≤4GiB、媒体正文总≤16GiB，P1≤890MiB，新私人输出≤384文件/24GiB。
> 明确授权现有RTX3090/Qwen3-VL-4B/SigLIP零训练推理：最多16次generate、
> GPU阶段累计≤900秒、peak allocated≤18GiB、worker Job内存≤24GiB；
> CPU接入/验证/评分≤600秒、媒体CPU≤1200秒、获取窗口≤3600秒、父≤7200秒。
> 原混合标注准备正文0；允许非继承独占handle正文0及最多2次零正文拒绝探针，
> 仅在所有模型PID退出、队列封闭且实际调用过Qwen.generate后，独立CPU scorer读原标注
> 最多1遍≤4MiB，只保留这4题gold、匹配028profile/完整快照，失败不重开。
> 新suite≤2次，不跑历史测试/QA，不换候选/题，不调prompt/阈值、不训练、
> 不下载模型/包或改环境/ACL/profile。按A–H一次完成媒体→真实四臂→独立评分→科研分析；
> 失败/NOT_RUN保留原N4/16槽，缺门如实STOP。只提交allowlist及一个030父结果，
> 一次安全推送main后停止，不自动031。
