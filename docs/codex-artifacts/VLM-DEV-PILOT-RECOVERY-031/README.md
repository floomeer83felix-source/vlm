# VLM-DEV-PILOT-RECOVERY-031：定点修复并完成同一真实开发诊断

2026-10-21（北京时间）。研究负责人ChatGPT；用户当前Windows本地Codex执行。
**唯一READY父任务：031 / PUBLIC_TARGETED_REPAIR_ONLY，尚未执行。**
公共定点修复可领取；私人读取/新目录、真实SDK/媒体/GPU/gold按文末用户实际发送的
一条明确新消息激活。031是030交付经研究负责人审查后的新整包，不是030第三次测试、
旧run恢复或余额迁移。用户已确认有效研究许可和开发口径，不要求再次申请数据许可。

## 0. 原因与不变的科学目标

030交付[101b001](https://github.com/floomeer83felix-source/vlm/commit/101b00111fcf30a45309a5dda5eddd173a012005)
按 **ACCEPTED_SAFE_STOP_AND_PARTIAL_IMPLEMENTATION / REAL_QA_NOT_RUN** 结案。
首suite0发现/exit5；末suite18项16PASS/2FAIL。未做HTTP/媒体/真实模型/GPU/gold。
这不是方法负结果、来源/许可失败或证明环境损坏。

两个实际问题：Python普通open异常未给winerror，测试硬等32；健康peer已exit0却立即
查询Job活跃数得1。生产probe也只认Python winerror32，不能只改测试绕过去。
需用准确OS返回证据、真实有界Job清空等待修复，不移除保护条件。

沿用[030科学协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)，
DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。
原4题/20选项/16槽和ABCD/BCDA/CDAB/DABC不变；P3参与者缺失披露但不作本轮入门否决。
不补旧来源登记、不新筛选、不换题。025四臂/窄语法/48→12、C/D同2锚点、共享q/a/b、
目标/tie/补齐不变；只变i≠j与i<j。原028profile/完整快照绑定不变。
允许这4题在新031逐臂新回答一次，包括既往研究可能答过的同题；
030真实generate0，本轮不是重放030模型尝试，其他历史父任务仍不重跑。

## 1. A–H一次连续交付

| 项 | 工作及必须提供的实际证据 |
|---|---|
| A / 交接与新run | 安全同步独立docs main，重读AGENTS/board/results/overview、本合同、030两回执与新协议；确认唯一未交付031。先完成公共代码/静态审查，再原子建已知018根下integration_031；新RUN、contract_id=031、run_id、lock/ledger及7200s父时钟。030根只读；从其确切缓存读取既有8份nongold、4份runner/factory及必要完整ledger/annotation-reference，不重开原标注或原runner补数据。 |
| B / 精确修复 | 实施第二节Win32探针、Job排空/完整时限、显式test loader/031门、只读旧cache交接、真实runtime入口和评分绑定修复。尽量复用现有030三个生产模块，不再复制整套runner。保留原030失败tests/报告，不能删断言把失败“变PASS”。 |
| C / 新见证 | 仅运行新的test_development_recovery_031.py≤2次、每次总窗口≤60s。用虚构内容/transport验证实际Windows share拒绝＋释放、健康peer自然清空、自有超时/后代清空、同生产score路径独立child评分、输入/plan/queue/退出绑定、031固定root/旧closed拒绝、HEAD→条件GET流预算联通与现存helper接入。完整suite全部PASS、0ERROR/FAIL/SKIP并有真实OS标记才进入D；不重复030旧18项suite或025–029测试。 |
| D / 真正接入和媒体 | 新scope激活后，复用已核对030缓存的四键/选项/028完整receipt/029准确canonical对象和既有有效许可依据。当前原annotation只作身份/stat及非继承share=0 handle（正文0），实际零正文拒绝探针过门后，按第三节获取准确对象、CPU demux/48候选；不要求全4源成功，有可执行源就继续。不引入旧源排除/物理独立证书门。 |
| E / 实际四臂 | 冻结全部N4/16槽，缺媒体四槽NOT_RUN；至少1源可用且真实隔离/资源门通过才启动唯一GPU worker。现有Qwen3-VL-4B BF16、SigLIP F32、local-only/SDPA、seed19、贪心64新token，真实≤16 generate、零训练。保持原factory/helper语义，逐次实测12帧/grid[6,12,18]/324 visual tokens；选项仅prompt，C/D共享事件分数。记录时间戳文本长度差异、检索截断/EOS/成本，不按输出修prompt/重试。 |
| F / 独立评分 | 逐槽STARTED/TERMINAL持久预扣，失败不退款；全部模型Job/PID实测退出0、完整16槽终态及run/plan/queue hash一致后，封闭队列，再释放原annotation handle。仅实际有Qwen返回/INVALID后启动独立CPU score一次≤4MiB，只有四题gold、同028profile/raw摘要。guard先消费；坏gold/半读/快照变更则准确率/配对UNKNOWN、不缩N重开。 |
| G / 科研结果 | 匿名逐源/逐臂完整N4的correct及RETURNED/INVALID/FAILED/NOT_RUN、六对表、C=D/原始目标/跨度覆盖proxy与q/a/b/图像编码/Qwen成本。全C=D写NO_REALIZED_SELECTION_CHANGE；同帧同输入却答不同写实现/可复现性问题。没有真实QA写REAL_QA_NOT_RUN，不能从fixture/实施失败认定机制正负。 |
| H / 一次push STOP | 只提交allowlist定点生产改动、新031测试、两报告、results一个031父记录，保留失败和计数证据。统一安全推送main后STOP，不自动032或再重试；不重置030、不追加第三suite、下载/生成或训练。 |

## 2. 定点生产修复，不以放宽条件消掉失败

### B1. Win32原始错误＋Python观测

为探针建立明确typed Win32 CreateFileW调用（OPEN_EXISTING/GENERIC_READ），
通过use_last_error=True及失败后立即ctypes.get_last_error记录原始错误码；
返回有效handle时立即close且不read。持有share=0锁期间必须原生返回
ERROR_SHARING_VIOLATION=32；文件不存在、任意OSError、mock返回、打开成功都不算PASS。
同child也执行普通Python rb open（即使意外成功也立即close/不read），分别报告
opened/exception_kind/errno/winerror/body_bytes=0；Python拒绝可表现为errno=EACCES而winerror缺失，
必须同时有刚取得的真实Win32=32证明。不能把Python winerror=None直接当OS锁失败或成功。
释放虚构canary锁后，两种普通read-open应可成功并立即close/正文0，排除错误路径伪阳性。

生产probe与新见证使用同一实现，不能只改030 test的字符串断言。
ExclusiveRead失败路径释放已经取得的自有handle，显式检查不可继承；
原文件属性/ACL不改。真实原annotation最多2个探针child：
每child各≤1次原生open＋≤1次Python open，合计≤4次零正文尝试；
父非继承独占handle≤1，所有正文均0。任何意外成功/原生非32或未知，GPU/gold HOLD。

依据：[Python OSError字段](https://docs.python.org/3.9/library/exceptions.html#OSError.winerror)；
[Microsoft GetLastError](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror)。
文档与030观测支持修正取证方式，不证明030那次缺字段的精确成因。

### B2. Job活跃计数与真实退出

实现公用bounded wait_empty：在直接child wait后用monotonic绝对deadline反复查询
该自有Job的active count，只有实测0才签发退出receipt；查询失败/超时仍HOLD。
健康peer必须自然退出并在有界等待后为0，不能为让测试通过kill健康peer。
若实际仍有自有后代，按deadline只终止自己的Job，并等其归零；无法证实归零就不评分，
不得伪造job_active=0或按PID名称搜索/杀其他进程。
030的计数1可能有时序原因，但本合同不把它倒写为已证明的系统滞后。

启动握手、运行、grace、kill/wait和pipe drain都计入完整child窗口与阶段预算。
生产metadata/score child最长120s、suite60s、GPU900s等是完整窗口；
运行deadline应预留cleanup时间（如5s），不能在900s之后再无账本地等待。
短fixture可分work timeout与cleanup timeout，但必须在其完整3s预扣内。
监督所有自有后代；没有可靠Job退出就没有gold，即使直接PID exit0。
依据：[QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject)。

### B3. 正确发现新测试、031独立账本与cache交接

使用显式TestLoader.loadTestsFromModule/指定test case集合再TextTestRunner，
记录期望/实际测试数及fail/error/skip与实际OS证据；不要再依赖未安装__main__的runpy发现。
若用runpy必须alter_sys=True。0发现、SKIP或缺OS证据不是PASS，计入一次启动。
只有本031模块的真实成功receipt允许后续阶段；不能复用030的16个单项PASS。

Journal只增加固定031支持：root名/lock/ledger/RUN.contract_id严格一致，
不可任意task-id/后缀；030的closed/failed状态及原账本不改，禁止从031路径读030运行账本
冒充新run。旧030父deadline已过也不能改epoch或重置RUN。
读取旧030 cache时用只读完整hash-chain验证器，不实例化旧运行Journal、不拿旧OS锁、
不运行其check_time/prepare/finalize，不继承测试/输入/网络/GPU余额。
验证030确为RUN_STOPPED、16 NOT_RUN且HTTP/MODEL_LAUNCH/gold0；缓存字节与原INPUT_COMPLETE
摘要、四键/options/轮转及028profile相符，才复制必要nongold/source到新031。
新run时钟只从031创建计时；拒绝伪造/不完整/被改过的缓存。

新031失败finalize据实际receipt计数；不能复制030已写死的18 tests/2 failures/030 ID。
所有打开/写入/时窗/slot预扣共用新031 durable ledger，不因新mode/对象/聊天重领。

### B4. 未运行路径的必要接入核对

现有prepare从coordinator Python目录拼Scripts/conda.exe，不是已证的pytorch入口。
优先采用当前本地会话已确认的精确pytorch Python及SDK Python；若需通过已知确切conda入口
stdlib-only解析，只准1个≤20s自有child（含在CPU总额），输出Python/PATH，不查环境列表、
不安装/迁移或猜其他目录。不要为此再开一轮资产盘点。
实际helper/factory保持AST相等，用虚构nongold/受控fake processor核对依赖与调用，
不执行旧runner顶层、资格/gold函数。模型资产正常只读加载限原明确目录。

媒体candidate代码额外的≤1GiB/源frame cap不是030书面条件，031按全局frame cache≤4GiB
及实际frame_bytes预扣/磁盘余量裁决，不另加该隐含门，也不压缩/降分辨率改变像素。
网络门补齐按精确对象method/URL跨alias去重；HEAD→IfMatch/VersionId GET必须
在真正发送前落账，旧Generic通过不能替代新组合路径见证。

score前核对完整16个唯一slot、run_id、plan/queue/worker-input及MODEL_LAUNCH/EXIT hash；
有存活/未知Job或绑定变化时opener=0。退出0但没有相符SCORED结果/完整raw绑定时，
不能发布“评分成功”；guard消费并报告UNKNOWN，不重启score。
这些都是接口/观测修复，不改科学选择器/模型/提示/候选数量。

## 3. 新031完整资源边界（与030分账；不扩大真实实验规模）

- 研究文本输入仍≤32MiB：已知030/028/029 nongold/cache/ledger/reference≤12份，
  每份≤1MiB各1open；精确缓存runner/factory和现存SDK source合计≤7份各≤1MiB各1open；
  必要model config≤4份各≤1MiB各1open；原annotation只最终gold≤1open/≤4MiB。
  原annotation准备/index/screen/inference正文0，官方原manifest0open，
  旧来源八文件/历史逐题预测/历史gold产物0open。原实验目录不扫描。
- 仅新<AUTHORIZED_018_ROOT>/integration_031写≤384文件/24GiB，
  media（含失败partial）≤16GiB/frame cache≤4GiB/其余≤32MiB。
  同名已存在STOP，不删除/换后缀；逐对象按实际预留和2GiB磁盘余量门控。
  030原root/lock/ledger/文件全部只读，不做恢复或媒体复制（030实际媒体0）。
- 自有metadata/验证/prepare/最终score CPU窗口合计≤600s；媒体CPU≤1200s；
  网络获取窗口≤3600s；唯一GPU worker阶段≤900s；父coordinator≤7200s。
  每source媒体child≤300s、GET≤900s，metadata/score≤120s，均含cleanup；
  所有阶段/实际嵌套PID保守合计，不能拿静态cap当实际用量。
- 新031 suite≤2次、每次完整≤60s；新的虚构child/后代合计≤24个、
  每PID完整≤3s、串行，计入600s。真实拒绝probe≤2个各≤5s亦计CPU。
  建议预扣排程：cache初始化45＋suite120＋nested fixture72＋prepare60＋runtime解析20
  ＋真实probe10＋SDKmetadata90＋GPU query10＋score60＋收尾30=517s≤600；
  各项可在600内合理缩用，不能超总额；多余不是补第3suite或重启的许可。
- 至多4个固定准确官方对象：不同bucket HeadBucket各≤1/共≤4，
  HeadObject≤4、GetObject≤4，实际HTTPS总≤12；所有失败不重试、无自动region redirect、
  LIST/STS/presign/其他host/模型或manifest下载0。
  只现有隔离SDK/静态ego4d shared-file provider；TLS verify、禁proxy，
  SDK/底层retry/preload与实际before-send门照030，HEAD/error body0。
- P1保留029同对象/ETag/若有VersionId与≤890MiB；其余每对象ContentLength≤4GiB，
  媒体正文总≤16GiB。新HEAD精确长度/ETag/VersionId冻结后条件GET；
  connect≤10s/read≤90s，每read前预扣≤1MiB，失败不退款、不续传或重下partial。
  精确opaque canonical key不拼UID、不加suffix、不替换release；ETag不冒充hash。
  新HEAD发现超限/403/404/超时该源四槽NOT_RUN，继续其他固定源，不替换。
- 新真实Qwen generate≤16、每槽一次；GPU worker启动≤1；
  GPU阶段含load/编码/processor/generate累计≤900s、torch peak allocated≤18GiB、
  worker Job内存≤24GiB，原allocator硬门在load前设置。只一次既有nvidia-smi查询，
  确认无其他模型任务/可用VRAM≥20GiB，不杀peer或改系统。OOM等不重启/降dtype/模型/帧数。
- 原始annotation share-lock/明确原生+Python拒绝探针按第二节，模型存活期间持有；
  只有真实Qwen返回（含INVALID）、所有自有模型PID/Job退出且队列闭合，才独立CPU score一次。
  全N4/16槽FAILED/INVALID/NOT_RUN保留；bad gold/快照不符准确率/配对UNKNOWN，
  无实际QA返回则gold0。SKIP_NONFINITE_028 / PROJECTOR_028_V1/完整028 raw快照一致。
- 不新增模型/包/环境，不安装、升级、迁移、改profile/ACL或付费API/云GPU；
  optimizer/backward/LoRA/training0，新人工标签0，无后台继续。
  不变的媒体时间/模型预算/匿名化细则参照030 README，但本节031新预扣上限为准。

## 4. 新suite应验证的组合风险

不要复制原03018个case重新全跑。覆盖本轮新改动的少量有意义case：
真实Win32=32＋Python拒绝/释放后可open（零正文）；健康peer自然清空/自有后代仍活时
不得签退出/只终止自己Job；同生产plan/ledger/hash→真实假模型退出→独立canary score；
提前/错绑定/半读零发布且guard消费；031新run与旧030 stopped/过期cache仅交接不续跑；
实际loader非0测试；准确HEAD→GET header/字节预扣的组合；fake processor/helper依赖接通。
可以用模拟返回覆盖错误分类，但必须另有真实Windows canary/Job和独立PID评分成功，
不能以mock替代那三个实际证明。fixture不用真实QA/gold/媒体、SDK网络或ML导入。

第一suite通过就不再跑第二suite，直接接真实阶段。
有一次失败可在未消费第二次时修正；第二次仍失败则整包真实阶段STOP。
通过新见证后连续执行媒体→四臂→一次score，不把031交成“修好了等待下轮GPU”；
任何真实前置实际失败如实STOP/剩余固定源继续，不能为赶进度省门。

## 5. 公共执行allowlist（仅7处）

1. prototypes/development_pilot_030.py：定点生产probe/Job排空/031账本/交接/loader/score绑定与完整时限。
2. prototypes/development_media_030.py：031关联、对象去重/获取组合、全局4GiB frame cap一致性；不改media身份/字节/帧策略。
3. prototypes/development_worker_030.py：031关联/固定队列绑定、必要有证据的factory接入；不改prompt/模型/selector/解码。
4. prototypes/test_development_recovery_031.py：新031定点组合见证，不import旧test_development_pilot_030。
5. docs/codex-artifacts/VLM-DEV-PILOT-RECOVERY-031/repair-and-real-run-receipt.md：修复、每见证/实际OS、真实各阶段、失败/消耗/余缺。
6. docs/codex-artifacts/VLM-DEV-PILOT-RECOVERY-031/scientific-results.md：完整N4/16槽、六对表/C=D/覆盖与成本或明确NOT_RUN/UNKNOWN。
7. docs/codex-results.md：末尾一个031父记录。

不修改030测试/两份报告、其README、科学协议、AGENTS、board/overview、旧结果、
025–029基础模块；原030失败证据保留101b001版本。新修复公开差异可追溯，
不将030历史失败改称通过。公共代码无私人默认路径、原私有helper全文或真实身份。

UID/participant/来源映射、题/事件/选项/gold/预测原文、精确PTS/完整选帧索引和cosine、
私有路径/URI/hash/credentials/权重/媒体全部留私人；公仓只匿名聚合/取整proxy。
同输入却不同答写实现问题，实施失败不当方法负结果，4题不作统计/泛化/创新结论。
EXPLORATORY_DEV_RESULT最多；NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、
Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。一次普通push后STOP，不自动032。

## 6. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview和
> VLM-DEV-PILOT-RECOVERY-031 README及引用资料，确认唯一未交付READY031。
> 按031合同修复生产Win32错误取证和Job有界排空、loader/固定账本/cache/评分绑定；
> 使用031新suite最多2次，不重跑030测试或旧父任务。见证过门后同轮连续执行真实诊断。
> 我在已确认有效的研究许可和SOURCE_OVERLAP_ALLOWED开发口径下，
> 明确授权本031一次新私人输入≤32MiB及新integration_031写入≤384文件/24GiB；
> 030仅确切nongold/source/cache只读交接，不改030根/账本/epoch，不沿用余额。
> 允许原4题每臂新回答一次（即使旧研究答过），不换候选/题，完整N4/16槽。
> 新HeadBucket≤4、HeadObject≤4、GetObject≤4、实际HTTPS总≤12，失败不重试；
> 每片≤4GiB/媒体正文总≤16GiB、P1≤890MiB。现有模型零训练generate≤16，
> GPU阶段≤900s/peak allocated≤18GiB/worker Job内存≤24GiB；
> CPU≤600s、媒体CPU≤1200s、获取≤3600s、父≤7200s，
> 新suite≤2×60s/虚构PID≤24各≤3s，真实零正文probe按合同≤2个child。
> 原annotation准备正文0，父非继承独占handle与每probe原生/Python尝试均正文0；
> 只有真实Qwen返回、全部模型PID/Job退出与队列/快照绑定后，
> 独立CPU scorer最多1遍≤4MiB读取这4题gold，失败不重开。FAILED/INVALID/NOT_RUN留全分母。
> 不读旧预测/gold产物，不调prompt/阈值，不训练/安装/改环境、ACL或profile。
> 按allowlist提交定点代码、两份匿名报告及results一个031父记录，
> 一次安全推送main后停止，不自动032。
