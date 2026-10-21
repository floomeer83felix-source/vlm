# VLM-DEV-CURRENT-OBJECT-PILOT-032：固定对象条件获取与同轮真实四臂诊断

2026-10-21（北京时间）。ChatGPT研究负责人；用户Windows本地Codex执行。
**唯一READY父任务032 / PUBLIC_TARGETED_TRANSPORT_ONLY，尚未执行。**
公共定点实现可领取；私人读取、新目录、真实网络/媒体/GPU/gold由第7节用户实际发送的
一条明确新消息共同激活。031已关闭，不使用其剩余suite/网络/GPU额度，不恢复旧run。
仍沿用用户已经确认的研究许可和开发口径，不要求重新申请数据访问或追补旧source registry。

## 0. 审查结论与本轮目的

031交付[b8fa8b3](https://github.com/floomeer83felix-source/vlm/commit/b8fa8b368d2ae96e253db140768417b79effe6a8)
按 **ACCEPTED_RECOVERY_WITNESSES_AND_HEAD_METADATA / MEDIA_ACQUISITION_HOLD / REAL_QA_NOT_RUN**
结案。首且仅一suite7/7 PASS，包含真实Windows共享拒绝/释放、健康peer自然排空、
自有后代清空与独立虚构CPU score。真实原annotation两个probe均native32/Python拒绝、正文0。
四HEAD均200；四IfMatch＋显式VersionId GET均ClientError/正文0。实际HTTPS11=3 bucket＋4 HEAD＋4 GET。
GET状态/服务码当时未保留，仍UNKNOWN；末尾新增诊断代码只有静态检查，不能倒填原因。
真实decode/model/generate/GPU/gold均0，全16槽NOT_RUN，正确率UNKNOWN/4而非0/4。

本轮有一项明确、可证伪的请求修正依据：
[AWS官方Boto3 GetObject文档](https://docs.aws.amazon.com/boto3/latest/reference/services/s3/client/get_object.html)
说明显式VersionId使用s3:GetObjectVersion权限，不指定版本的当前对象使用s3:GetObject；
IfMatch不匹配返回412。**版本权限差异仅为031失败的候选解释，没有被旧错误日志证实。**
032固定采用CURRENT_IFMATCH_PINNED_RESPONSE_032，不先重复版本GET再做fallback，
不更换凭据/对象/访问权，不声称必定成功。

科学口径沿用[030开发协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)：
DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。
原028四题/20选项/16槽及ABCD/BCDA/CDAB/DABC轮转保持；P3 participant缺失披露、不作入门否决。
025窄语法/48候选→12帧、C/D同两个锚点与共享q/a/b分数、目标/tie/补齐均不变，
只比较原i≠j和i<j规则。不追旧来源、不换题、不按输出找正例。
允许原四题在032每臂新回答一次（即使旧研究答过）；不重放其他历史父任务。

## 1. A–H连续整包

| 项 | 执行与验收 |
|---|---|
| A / 新交接 | 安全同步独立docs main，重读AGENTS/board/results/overview、本合同、031两报告及030科学协议。确认唯一未交付032。完成公共定点实现后，原子创建已知018授权根下integration_032，新contract_id/run_id/032.lock/032-ledger/7200s父时钟；旧031仅第3节确切文件只读交接。 |
| B / 请求与诊断 | 按第2节拆开wire请求版本和预期响应版本：GET没有VersionId/query，IfMatch精确保留；状态先持久落账，响应版本/ETag/长度全部验证后才可读取正文。固定032门与原production绑定联通，旧031事实不改。 |
| C / 定点新见证 | 仅新test_development_transport_032.py，显式loader、非0精确测试数，最多2次各完整≤60s；不import/执行030或031旧测试。用虚构transport覆盖第4节本轮改动，首轮全PASS即进入真实阶段，不耗第二轮“复验”。 |
| D / 固定真实获取 | 原annotation准备正文0，当前一次父独占handle＋2实际拒绝probe过门；复用031四HEAD与可信region，新的HeadBucket=0/HeadObject=0，四个固定对象各≤1次当前对象条件GET，实际HTTPS总≤4。失败源四槽NOT_RUN、继续其他固定源，不替换或重试。 |
| E / 媒体与四臂 | 成功对象完整流/长度/hash/版本绑定后CPU demux/48候选，沿用生产代码与原像素；至少1源合格且GPU门过才启动唯一真实worker。固定全N4/16槽，实际≤16 generate、GPU≤900s，保持真实12帧/grid[6,12,18]/324 visual tokens及原模型/提示/解码设置。 |
| F / 一次独立score | 模型所有Job/PID实际退出、完整16槽终态、run/queue/plan/worker/launch/exit绑定后封闭队列、释放annotation handle；有真实Qwen RETURNED/INVALID才独立CPU scorer≤1open/4MiB读取四题gold。无QA返回gold0；坏快照/半读/坏gold guard消费、UNKNOWN且不重开。 |
| G / 科研报告 | 全N4的四臂终态/正确数与六配对、C=D/选择差异/目标/跨度覆盖proxy、q/a/b与图像编码/Qwen成本/截断/EOS。没有真实QA就写NOT_RUN/NOT_MEASURED，不把transport修复或fixture当科研增益。 |
| H / 一次push STOP | 只提交第6节七处，results一个032父追加，普通安全push后停止。无自动033/更多网络/新题/调参/训练，不把整包交成“测试过了等下一轮GPU”；真实前置失败则如实HOLD。 |

## 2. 固定请求形态：保留031版本的响应约束

1. 将031四HEAD的准确canonical bucket/key、region、ContentLength、带引号强ETag、
   非空VersionId冻结为032输入。不得刷新HEAD、改expected版本、跟随新latest或补猜suffix。
   P1继续与029同对象/长度/ETag/version相符；四对象长度总和应为031保留的
   6,002,290,187B，不能用公开MiB上界替代私有精确值。
2. 032只调用get_object(Bucket=原bucket, Key=原key, IfMatch=原ETag)；
   kwargs及真实线上query均**不含VersionId**，query为空；无Range/PartNumber/response override/
   presign/自制HTTP，仍用现有官方SDK静态ego4d profile/TLS/禁proxy。
   SendGate的wire_version应与expected_response_version分离，不能把expected VersionId删空。
   此profile只在固定032 run启用，无任意--drop-version/任务ID/忽略响应版本开关。
3. 实际before-send预扣和fsync后才发送；精确method/host/path/IfMatch/query、固定alias和对象跨alias去重，
   GetObject≤4/HTTPS≤4；HeadBucket和HeadObject在032门中直接拒绝。SDK/底层retry、region redirect、
   preload_content照031验证并禁止。任何额外send在传输前拒绝；失败不退款。
4. 收到真实response后，先记录TRANSPORT_RESPONSE的slot/HTTP整数status与本次请求profile，
   再进行headers门或SDK解析。HTTP200必须在raw第一次read/stream/drain前同时满足：
   x-amz-version-id == 031 VersionId，ETag == 031 ETag，Content-Length == 031精确长度，
   raw.length_remaining一致、非chunked、保留headers≤64KiB。三者缺一/不符即close、不read，源HOLD。
   相同ETag但新VersionId也拒绝；IfMatch单独不证明版本不变，ETag也不当SHA。
5. HTTP非200的正文不read、不drain，立刻close并换EmptyBody，保留实际status；
   SDK异常只额外保存≤64字符白名单service code（确实可用时），不保存Message/错误正文/
   Authorization/原始headers。由于错误正文不读，服务码可能仅数字或UNKNOWN，准确披露。
   无response的DNS/TLS/connect/read异常status=UNKNOWN并记录有界异常类型，不能虚构403。
   若response记录落账失败，关闭流并停止该源，绝不进入body读取。
6. 返回200也要等完整流和本地文件长度、实际SHA、原size/etag/version绑定成功才MEDIA_COMPLETE。
   每read前≤1MiB持久预扣，媒体正文总≤6GiB；失败partial保留且计预算，不续传/覆盖/重下。
   无条件GET、显式版本GET、同源第二GET或其他路径fallback均0。
   412/版本变化保持HOLD，不改expected或重新筛选；四源都失败则本轮GPU/gold0并结束该获取路线，
   后续只能基于真实状态另作研究负责人决策，不能自动同类重试。

032接受的媒体版本并未扩展：只能接受031冻结版本在“当前对象”响应中仍然返回的字节。
这是新scope内的单一请求profile，不是用失败槽位换另一次网络请求。

## 3. 031只读archive交接与固定032绑定

不实例化旧Journal、不拿旧锁、不调用旧check_time/prepare/finalize、改epoch/stop或复用旧RUN。
单独增加只读031 archive验证器，不放松现有030 archive_rows的“无真实动作”规则：
031确有HTTPS，不能用030的零HTTPS断言误拒绝，更不能忽略旧账本。

031完整hash链/seq/prev/结束换行及RUN.contract_id=031、root_name、REAL_031、RUN_STOPPED应核验；
要求16唯一NOT_RUN、7/7通过receipt、HTTPS/TRANSPORT_SEND=11（3 bucket/4 HEAD/4 GET）、
四HEAD实际终态200、BODY_DEBIT/MEDIA_COMPLETE/STARTED/MODEL_LAUNCH/SCORE_CONSUMED/真实gold均0。
核对031记录中有的证据，不要求当时未记录的GET status或TRANSPORT_RESPONSE凭空出现。
不得把fixture子目录的虚构score/HTTP算成真实031动作。

新读取白名单（handoff合计≤17份，各≤1MiB、每份1open）：
八个keys/cohort/nongold/plan/receipts/targets/heads029/official JSON；
031-ledger.jsonl、annotation-reference.json、execution-config.json、runtime.json；
P1-head.json至P4-head.json，以及metadata-summary.json。仅确切已知031根，不扫描历史目录。
八JSON和四factory_0/1.py、runner_0/1.py字节直接匹配031 INPUT_COMPLETE的size/SHA，
同时匹配031 OUTPUT大小；031已读入的canonical JSON就是本轮直接字节证据，
不再打开030原输入或把语义一致冒充字节一致。
只读保留的四HEAD与metadata-summary逐字段相等，匹配各OUTPUT名称/大小、
对应实际OBJECT_HEAD_TERMINAL200、原精确targets以及四GET线上versionId/预留media长度；
P1另比heads029。所有输入稳定stat/fd/完整read与新摘要由032 ledger持久记录。
031生成HEAD文件并非都有历史文件SHA；如实称“保留的031 metadata receipt交接”，
不声称已恢复不存在的历史SHA或把新算摘要倒签成031实时摘要。
本轮GET独立响应版本/ETag/长度门仍必须逐对象实际验证。

原annotation只核identity/size/mtime并和028三份完整raw receipt/profile一致，不读正文；
028 raw摘要用于最后独立scorer完整快照比对。未绑定/半读/改动输入则HOLD，
不能回扫原annotation或official manifest补数据。cached helpers保持AST同原runner，不执行原顶层。

031实际Win32/Job/独立score见证可作为这些**未改实现**的历史证据，不重跑旧7项套件。
032只增加固定root/contract/run/queue/worker/score路由及本轮预算、交接、transport门；
新suite验证032绑定拒错，真实阶段仍执行当前原文件两个probe/真实模型Job退出和最终score。
不能将031 suite receipt直接当032新transport suite通过。生产Win32/Job算法不趁机重写。

现有准确runtime/SDK Python与PATH由031已知引用交接；必要存在性检查限确切路径。
默认不重新conda解析；若准确runtime不可用可用既有确切入口1个≤20s stdlib-only child，
计CPU总额，禁止环境列表/其他目录盘点。模型/processor仍只现有获准目录，local-only。

## 4. 只测本轮变化，然后进入真实链路

新suite显式load并报告expected/run/fail/error/skip；0发现或SKIP不是PASS。
不得import旧test_development_pilot_030或test_development_recovery_031后再跑完整历史suite。
应以少量组合fixture覆盖：

- 用production client构造/transport wrapper（虚构client和response，不联网）证明没有VersionId query、
  有精确IfMatch，200三header全匹配后正文每read前已预扣，完整流可发布。
  源版本不符/缺失、仅同ETag不同版本、长度错/chunked/错误host/query/Range均0read。
- 403/404/412/5xx、header门失败、无response异常均留下准确已观测status或UNKNOWN，
  ErrorBody.read/stream/drain调用数0；service code不存在不填AccessDenied。
  能区分真实send失败和HTTP响应、child exit0与获取成功。
- 重复/跨alias相同对象、SDKredirect/retry/额外HEAD或VersionId query在真正send前拒绝；
  truncated stream的预扣/输出预约不退款，不发布MEDIA_COMPLETE。
- 031含11请求、0body、closed/16 NOT_RUN archive接受，截断/tamper/真实gold或model痕迹拒绝；
  旧030零真实动作validator保持原义。八JSON直接hash交接与HEAD/summary/version/size不一致拒绝。
- 固定032root/ledger/run/purpose/suite receipt/queue/worker/score bindings相符才进入阶段；
  031 suite/旧root/已STOP/错run/缺退出/重复slot拒绝。虚构内容验证opener0，不使用真实gold。

第一suite全PASS就连续D→G；可在剩下第二次之前修一次明确问题，第二次仍败则真实阶段STOP。
新的虚构子PID/后代合计≤8个、各完整≤3s、串行；若fixture无需child无需创建。
不要求再重复健康peer/完整Win32/真实虚构score三项旧OS演示；当前真实annotation probes仍必做。
若生产代码在PASS后又改动本轮被测关键分支，须在尚未消费的第二suite内验证，
否则这些分支标静态未验证，真实阶段不得用其绕过门。

## 5. 032新额度（旧031全部关闭；不扩大实验N）

| 资源 | 本轮硬上限 |
|---|---|
| 研究文本输入 | ≤32MiB；handoff≤17份×1MiB、精确source≤7份×1MiB、model config≤4份×1MiB、最后gold≤1open/4MiB；四角色最坏和32MiB。cache内部复读不重复原外部输入open；都在新根/账本下计费 |
| 新私有输出 | 仅已知018根/integration_032，≤384文件/12GiB；含失败partial的media≤6GiB，frame cache≤4GiB，其余含ledger/fixture≤32MiB；同名存在STOP，不换后缀/删除 |
| 实际网络 | 新HeadBucket0、HeadObject0、GetObject≤4，HTTPS实际总≤4；每固定对象至多一次；LIST/STS/presign/模型/manifest/其他host0，失败/重发不退款 |
| 媒体正文 | ≤6GiB，四对象只能031准确长度（总6,002,290,187B）；单源不大于031且仍≤4GiB。公开MiB上界P1–P4为890/2135/2263/438，不将取整当新length。每次read前≤1MiB预扣 |
| 磁盘/身份 | 每对象/frames实际预约＋2GiB余量，checked_path/no reparse与不覆盖；原031所有文件只读，未下载素材不需复制/迁移 |
| CPU/获取/父窗口 | CPU累计≤600s，媒体CPU≤1200s（各源≤300s），获取≤3600s（每GET完整≤900s），父≤7200s；握手/grace/kill/pipe drain全计入，嵌套PID保守另计 |
| 新测试 | ≤2次，每次完整≤60s；虚构PID≤8个各≤3s、串行，计CPU600内。首PASS立即真实，不做无因复验 |
| GPU与生成 | 唯一worker≤1、generate≤16（每槽一次，失败不退款）；load/编码/processor/生成全阶段≤900s，peak allocated≤18GiB、Job RAM≤24GiB；现有RTX3090/64GiB、pytorch不改 |
| 真实原annotation | 准备正文0；父非继承exclusive share handle≤1，模型期间持有；probe≤2child各≤5s，每child原生open＋Python open各≤1、均正文0。native32＋Python拒绝才通过，不改ACL |
| 评分 | 实际Qwen返回/INVALID、全部模型PID/Job实测退出及完整绑定后独立CPU scorer≤1次，gold≤1open/4MiB；guard先消费，半读/坏快照不重开；无真实QA返回gold0 |

仅现有Qwen3-VL-4B BF16/SigLIP F32、local-only/SDPA、seed19/贪心64新token，
原processor/factory/提示/选择器语义不变。实际逐调用记录12帧/grid/visual tokens和含时间文本长度，
报告q/a/b检索截断与EOS及成本。仅一次既有nvidia-smi查询、VRAM≥20GiB且无其他计算任务；
不杀peer/降dtype/换模型/减帧或OOM后重启。环境/依赖/模型/权重下载、optimizer/backward/
LoRA/训练、新人工标签、profile/凭据/ACL变更及后台继续均0。

建议CPU预扣：初始化45＋suite120＋虚构PID24＋prepare60＋可选runtime20＋实际probe10
＋GPU query10＋score60＋收尾30=479s；SDK source核验可在其实际GET完整窗口或600总额内明确计费。
这是预留建议不是实测，所有真实消耗/预约/失败应分开汇报。

## 6. 公共执行allowlist（仅七处）

1. prototypes/development_pilot_030.py：固定032 ledger/budgets/只读031交接、loader/execute去除metadata阶段、queue/score/最终回执路由；保留Win32/Job与独立score保护。
2. prototypes/development_media_030.py：固定032当前条件GET请求/响应版本分离、零HEAD/四GET发送门、状态持久化与6GiB正文门；candidate/像素不改。
3. prototypes/development_worker_030.py：只必要032固定run/queue/launch关联，不改模型/selector/提示/解码。
4. prototypes/test_development_transport_032.py：本轮新的虚构transport/交接/032绑定见证。
5. docs/codex-artifacts/VLM-DEV-CURRENT-OBJECT-PILOT-032/transport-and-real-run-receipt.md：定点差异、所有实际状态/次数/字节/退出与资源、未测分支及失败证据。
6. docs/codex-artifacts/VLM-DEV-CURRENT-OBJECT-PILOT-032/scientific-results.md：完整N4/16槽/六配对/选择差异与成本，或准确NOT_RUN/UNKNOWN。
7. docs/codex-results.md：末尾唯一032父结果追加。

不改030/031测试/报告/README、AGENTS/board/overview、旧结果、025–029基础模块或科学协议；
不复制整套runner。Git保留031请求形态与错误取证限制，不能回填历史status。
公共只匿名聚合/取整proxy；真实UID/映射/题/事件/选项/gold/预测原文、私有路径/URI/hash、
精确PTS/索引/向量/凭据/媒体/权重不公开。

科学报告必须保留full N4，缺媒体/失败/INVALID/NOT_RUN不从分母消失；未读gold的正确数UNKNOWN。
只有真实选择计算过才能说C=D；全同则NO_REALIZED_SELECTION_CHANGE，不调参找差异；
同帧同输入却回答不同是实现/可复现性问题。最高EXPLORATORY_DEV_RESULT，
不认定独立泛化/统计显著/论文创新。NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、
Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。一次普通push后STOP，不自动033。

## 7. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview和
> VLM-DEV-CURRENT-OBJECT-PILOT-032 README及引用资料，确认唯一未交付READY032。
> 按合同定点实现并完成A–H；031只读交接，不重跑030/031测试或恢复旧run/余额。
> 我在已确认有效研究许可和SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE开发口径下，
> 明确授权032一次新私人输入≤32MiB、新integration_032≤384文件/12GiB，
> 原4题/20选项/16槽每臂新答一次（即使历史答过），不换题或对象。
> 复用031冻结HEAD/region：新HEAD0；四固定对象各≤1次GetObject，实际HTTPS总≤4，
> 请求无VersionId、精确IfMatch，读取正文前响应VersionId/ETag/长度必须全部等于031；
> 不匹配/失败不重试、不改expected或fallback，媒体正文总≤6GiB、各对象只原精确长度。
> 新suite≤2×60s、虚构PID≤8各≤3s；首PASS后同轮媒体→真实四臂→独立score。
> 新generate≤16/单worker，GPU≤900s/peak allocated≤18GiB/Job RAM≤24GiB；
> CPU≤600s/媒体CPU≤1200s/获取≤3600s/父≤7200s，全部含cleanup并分账。
> 原annotation准备正文0，父非继承独占handle及2真实probe按合同零正文；
> 仅真实Qwen返回、所有模型PID/Job实测退出及队列/完整快照绑定后，
> 独立CPU scorer≤1次/1open/4MiB读取四题gold，坏gold/半读不重开。
> FAILED/INVALID/NOT_RUN留全N4/16槽，不读旧预测/gold产物、不调prompt/阈值，
> 不训练/安装/改环境、ACL、profile或凭据。按七处allowlist提交代码、两匿名报告与
> results一个032父记录，一次安全push main后停止，不自动033或增加GET/生成。
