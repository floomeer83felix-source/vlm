# VLM-DEV-STARTUP-RECOVERY-035：定位启动拒绝，同轮修复与真实四臂评分

2026-10-21（北京时间）。ChatGPT研究负责人；用户Windows本地Codex执行。
**唯一READY父任务035 / PUBLIC_STARTUP_REPAIR_ONLY，尚未执行。**
先完成公共定点实现。第8节用户实际发送的一条明确消息共同激活新缓存/启动探针/GPU/gold范围。
034已关闭，不重开旧run/锁/时钟，不迁移余额。既有研究许可和允许来源重合开发口径保持，
不要求重办数据访问、不追旧source登记。没有后台自动执行或下一父任务授权。

## 0. 验收与具体问题

034交付[d9143ed](https://github.com/floomeer83felix-source/vlm/commit/d9143edb9bb4d77c6b99e635c1a06443e94f850c)
按 **ACCEPTED_CACHE_AND_SHARED_RESOURCE / WORKER_SETUP_HOLD / REAL_QA_NOT_RUN** 结案。
首且仅一suite4/4 PASS；P2当前完整copy/SHA/48 RGB、真实annotation零正文拒绝通过。
当前一次query free22,928MiB/util2%/WDDM/29 C+G，设备/free过门，RESOURCE_ADMITTED实际写入。
唯一GPU指定worker实际进入，SETUP PermissionError，internal1.859s/outer2.203s，exit0/Job0；
退出与完整16槽队列真实闭合。没有WORKER_FREE_RECHECK、STARTED/回答/真实score/gold，
peak allocated/reserved未测；这2.203s是已消费的GPU阶段窗口，不证明成功CUDA初始化。

034只保存异常class/大阶段，没有具体operation/path、errno/winerror或stack。
**根因仍UNKNOWN**，不能先认定audit hook/Windows ACL/CUDA/权重损坏。
035先补可用证据，再修已定位的问题；新复现只能证明本轮事实，不倒填034未留的诊断。
不是把“模型进程exit0”当推理成功，也不是再做一个只交日志等待下一轮的任务。

科学口径沿用[030协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)：
DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。
原N4/20选项/16槽/ABCD、BCDA、CDAB、DABC不变；only-P2原BCDA四槽可执行，其余12槽NOT_RUN。
48候选→12帧、C/D同双锚点与共享q/a/b、目标/tie/补齐、i≠j对i<j、模型/提示/像素/seed/greedy不改。
不换题/扩样/读旧答案调参。网络/下载/MP4或partial正文/新demux/decode均0。

## 1. A–H连续整包

| 项 | 执行及验收 |
|---|---|
| A / 只读交接 | 安全同步独立docs main，重读AGENTS/board/results/overview、本合同、034两报告和030科学协议。确认唯一未交付035。公共实现后原子建已知018根/integration_035，固定contract/run/035.lock/035-ledger/3000s父时钟。只读第5节确切034缓存。 |
| B / 启动可观测性 | 在同一生产startup路径加细阶段、内存中有界audit拒绝记录、异常class/errno/winerror/有界frame摘要；只私存细节，公开匿名类别。不得在audit callback内递归写日志/resolve/读source/格式化locals。 |
| C / 定点新suite | 仅新test_development_startup_035.py，最多3次各完整≤60s、按代码变化才使用剩余次数。覆盖diagnostic无递归/不放权、启动探针、有限重启/聚合deadline/all-exit score和034已launch失败的archive；不重跑旧套件。 |
| D / 实际启动定位与修复 | 完整copy核验P2缓存；父annotation独占handle和2实际零正文probe后，在同一policy下最多2个真实CPU bootstrap child各≤60s：依赖imports、CPU processor/helper接通，不载模型权重/不调用CUDA/不做模型前向。首失败取得精确证据，按第3节修复并验证，第二个过门后立即E，不只交“已定位”。首个过则不补第二个。 |
| E / GPU与必要的一次恢复 | 沿用显存有界共享政策，一次新当前query/free门通过后，在一个共享900s GPU包络内最多2个串行worker。正常只启动1个；只有首worker完全未消费任何QA槽、所有自有Job/PID实测退出且有可修的技术证据才允许一次定点修复/新suite后重启。任一STARTED出现后永不重启/重答。only-P2最多4次generate。 |
| F / 完整退出与独立score | 最后封闭完整16槽，所有已launch的模型进程/Job均有真实匹配退出；有实际RETURNED/INVALID且run/plan/queue/resource/所有launch-exit/raw快照绑定后才释放handle并独立CPU scorer≤1open/4MiB。guard先消费、坏gold/半读不重开；无回答gold0。 |
| G / 科研与工程报告 | 分清原034未知根因、本轮复现定位/修复、CPU预处理、CUDA/权重/selector/QA/score各自证据；全N4终态与六配对、P2条件个案、C=D/目标/覆盖proxy/成本/tokens/截断/EOS。无实际选择/回答不能填科研指标。 |
| H / 一次push STOP | 六处allowlist统一提交，两匿名报告＋results一个035父追加，普通安全push main后STOP；无自动036/第三worker/第四suite/额外下载或科学调参。真实不可修条件如实HOLD。 |

## 2. 把PermissionError定位到具体操作

startup顺序和实际最细阶段需可追踪，至少区分：policy安装、NumPy import、Torch import、
Transformers import、VideoMetadata import、CPU processors/factory、CUDA availability/device、
global free、allocator、SigLIP load/encode/select、Qwen load/processor/generate。
首次异常即保存当前阶段，不能只保留SETUP。

- audit callback仅将**被拒事件**的event/reason、读写flags、词法路径、当前stage存入内存；
  最多16条、累计≤8KiB，callback无文件IO、真实resolve/stat、source line读取或日志框架。
  网络事件不保存连接参数/token/header；拒绝仍raise，不吞异常后继续同一失败child。
- 外层捕获保存class、errno/winerror（可缺失）、明确的本policy拒绝reason或外部OS错误类别，
  私人消息限长、traceback仅最多32个frame的filename/function/lineno，不抓locals/源码行/
  env/凭据/张量/题目正文。每个诊断artifact≤64KiB、attempt独立命名且计输出预算。
  不调用会在受限hook下再次open源码的traceback格式化路径；诊断本身失败也要留最小fallback。
- 由parent在child退出/Job0后读取这次新root诊断（内部复读），公开只
  dependency/policy/cache/CUDA/API等有证据类别、阶段、错误码和PASS/HOLD，不上传原路径/trace/身份。
  若没有匹配的拒绝事件，不能仅凭PermissionError断言audit触发；
  有本hook对应记录才能归因该事件。当前只能归因035复现，不篡改034历史。

Python官方说明audit hook可中止操作，**不是安全sandbox**；仍保留实际原文件share-lock、
非继承handle、真实拒绝probe和Job退出，不以Python callback替代OS边界。
依据：[sys.addaudithook](https://docs.python.org/3/library/sys.html#sys.addaudithook)。

## 3. 允许的修复与真实CPU bootstrap

最多2个真实bootstrap子进程，每个完整≤60s/Job RAM≤24GiB，计CPU900。
在当前真实annotation handle持有且probes已过后运行，与GPU worker共用生产policy/startup helper、
确切pytorch interpreter/PATH/local-only模型目录。不能用不同宽松policy让probe PASS。

bootstrap可import NumPy/Torch/Transformers/VideoMetadata，加载两个**CPU processor/tokenizer/config**，
按原private factory/helper用P2 nongold和既有48帧取一个固定Uniform12输入，
实测12帧/grid[6,12,18]/324 visual tokens与正常tensor类型；不是QA回答或真实选择器比较。
不调用SigLIP/Qwen模型from_pretrained，不载模型权重，不做encoder/generate/training，
不调用cuda.is_available/mem_get_info/创建CUDA tensor；可读is_initialized无初始化状态检查。
成功receipt必须有本次实际PID/Job0、完整stage、policy/code/worker config摘要，不接受mock/import-only字符串。

定位后允许在同轮做如下定点修复，科学配置hash保持不变：
- 在**自有child启动前**将TEMP/TMP、HF_HOME/HF_HUB_CACHE、TORCH_HOME/XDG_CACHE_HOME等
  已在本机版本源码或官方文档确认的必要cache路由到新root已预约子目录；
  保留offline/local_files_only/trust_remote_code=False，strip凭据。
  仅进程局部环境，不改系统/用户持久环境、原模型目录或现有用户cache，不复制权重。
- 允许纠正本项目词法path/flags/既有runtime范围或cache写入判断的实现错误。
  若确需增加read范围，仅至多4个由真实诊断精确指出且证明属于当前已安装runtime支持的
  **确切只读文件**；记录作用/来源/身份，不扫描兄弟目录、放开整个home/下载目录/其他科研根，
  不允许该例外匹配annotation、旧gold/预测、凭据或受限映射。
- 已定位的局部API返回类型/参数兼容可按确切已安装模块源码修复，保持原tensor语义、
  dtype/模型/processor/归一化/选择器/输入像素与提示不变；不能随机试参数或重答找成功。
  四份旧helper AST保持原义；025选择器/scorer及科学协议不改。
- 不关闭/移后安装audit去绕过失败，不改ACL/Windows权限，不安装/升级/换环境/driver，
  不为imports开放网络或模型child任意子进程/命令权限，不绕过原文件share拒绝。
  必须依赖这些动作、缺真实诊断或无法在两bootstrap内验证就HOLD，不作未经授权的环境修复。

HF环境配置需在库import前生效；TORCH_HOME控制Torch Hub cache目录。
依据：[HF环境变量](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables)；
[Torch Hub缓存位置](https://docs.pytorch.org/docs/stable/hub.html)。
文档只支持运行时cache配置方式，**不证明034就是cache问题**，不允许Torch Hub下载/执行远端代码。
正常bootstrap通过后立即实际GPU，不把CPU预处理通过当成真实模型/QA成绩。

## 4. 有限恢复、一个GPU总包络与所有退出证明

继续MEMORY_BOUNDED_SHARED_GPU政策：正确device0/3090/UUID/bus、当前free≥20GiB；
util只记录，C/G/C+G不单独否决，不声称空闲/独占。034旧RESOURCE_ADMITTED只历史证据。
CPU bootstrap过门后，本035最多一次新nvidia-smi query、完整child≤10s；
各GPU worker权重前最多一次global mem_get_info/free≥20GiB，allocator18GiB在load前设置，
peak allocated≤18GiB/Job RAM≤24GiB/原3090 total范围保持。不kill peer、循环等资源或重query。

**最多2个串行GPU worker启动，不是两份900s：**
- 在第一次worker启动前一次性持久预约一个900s GPU包络和绝对deadline。
  从第一launch到第二attempt结束（含中间修复/测试间隔）均在这个deadline内；
  每child完整deadline取剩余包络并预留cleanup。不得先预扣900又给第二worker再预扣900，
  不退款/重置包络，不把旧034未用时间转入。报告包络elapsed与每实际child wall，不能相加重复计时。
- 第二launch必须同时满足：第一个真实已退出且Job0、其退出receipt hash/launch绑定可验；
  整个本035 ledger **STARTED总数=0**、无RETURNED/INVALID、P2四槽尚未写终态/队列尚未关闭；
  有明确技术诊断、限第3节定点修复并通过尚未消费的新suite，900s包络尚有可用时间。
  不能因OOM/显存不足/timeout、想重算选帧或找更好输出而重启。
  第一attempt达到任何STARTED后，即使generate没有返回，也禁止第二launch。
- attempt_id只允许1/2，各有独立WORKER_ENTERED/result/diagnostics/selection/exit文件，
  避免write-once文件冲突；原P2 frames/nongold/worker配置/queue保持不变。
  各launch绑定当前已测试代码版本摘要、run/queue/resource/attempt，STARTED绑定有效attempt。
  CPU bootstrap不得mint MODEL_LAUNCH/STARTED或消耗QA预算。
- 当前父add('MODEL_LAUNCH')、worker、score不能继续硬等len(launches)==1；
  改为固定1–2且逐条匹配all-exit，不得只放宽数量不查首attempt退出。
  每launch恰有一个真实MODEL_EXIT，Job0、实际PID/exit digest、launch/run/queue/attempt一致；
  零QA失败的首attempt也不可从退出集合消失。
  最后只关闭一次QUEUE_CLOSED，绑定全部launch/exit集合、完整16唯一终态、
  原plan/worker/resource和实际产生回答的有效attempt。
- 仅最后结束/不能恢复时补齐未启动P2槽NOT_RUN；有STARTED但无回复的槽FAILED。
  预先12 unavailable槽保持NOT_RUN，无重复terminal/重置STARTED。
  所有launched Job/PID实测退出前持有annotation handle，不允许score。
  若无真实QA返回gold0；有真实返回且所有绑定齐全才独立CPU scorer一次，沿用025 full-N口径。
  最终ChildExitReceipt必须反映全部已launch/exited模型PID，不能只用最后一个PID伪装all-exit。

如需把实际诊断交给Codex修复，使用同一个存活父coordinator的有界握手：保留原annotation handle、run/ledger和既有deadline，等待范围仅当前合同的bootstrap修复或一次零QA GPU修复。修复/新suite的等待也计父时钟，GPU首launch之后还计900s包络；只接受固定下一attempt/已验证代码与配置摘要，不能执行任意握手命令。不得先退出父进程释放锁、另建epoch/重拿预算再称连续恢复；没有可靠握手或剩余时间就闭合队列HOLD。此等待限本轮，无无限轮询或跨轮后台工作。

这是本035明示的一次**零QA前技术恢复**权限，既不重放034，也不允许已开始QA重试。
首worker成功就不使用第二个；真实问题无法在额度内消除如实HOLD。
新suite最多3次各≤60s，仅首验证或真实修复后按需运行；首PASS立即推进，
后续改变关键代码要用剩余额度验证。三次用尽不补第四次，GPU包络过时不新开。

## 5. 034 archive与明确输入

只从已知integration_034读取，不回扫033/032、不实例化旧Journal或更改旧锁/时钟。
专用034 archive校验完整hash链/seq/prev/newline、REAL_034/root/run/末尾STOP；
首且仅一4-case PASS、FRAME_CACHE_VERIFIED/full SHA、1 GPU_QUERY和1真实RESOURCE_ADMITTED；
**允许并核验旧1 MODEL_LAUNCH/WORKER_ENTERED、SETUP PermissionError、MODEL_EXIT/Job0及QUEUE_CLOSED**，
全16 NOT_RUN/STARTED0/WORKER_FREE_RECHECK0/gold与SCORE_CONSUMED0，网络/媒体获取0。
旧真实资源准入与失败模型退出都要保留；不能套旧“model必须0”的033 validator误拒绝，
也不把worker exit0认成推理成功。旧GPU900预留已关闭，不重用。

handoff≤25份，每份≤1MiB（034-ledger.jsonl单份可≤2MiB），每份1外部open：
八个keys/cohort/nongold/plan/receipts/targets/heads029/official JSON；
034-ledger.jsonl、annotation-reference.json、execution-config.json、runtime.json；
worker-input.json、queue.json、expected-snapshot.json；
P2-head.json、P2-media-binding.json、P2-candidates.json；
034-final-summary-private.json、gpu-samples-private.json、
frozen-worker-032.json、frozen-snapshot-032.json、device-identity-reference.json、
worker-result.json、gpu-worker-exit-private.json。
新私人诊断留在035内部按预算读写，不借此重开旧研究文件。

八nongold/四factory_0/1.py、runner_0/1.py及有旧input摘要的metadata直接匹配034
INPUT_COMPLETE size/SHA及OUTPUT大小。旧FROZEN/queue/worker/frozen-worker-032与原16槽保持，
snapshot/frozen-snapshot-032/028三份完整raw receipt/profile及当前annotation identity/size/mtime一致。
旧MODEL_EXIT digest与actual worker-exit JSON精确相符，资源sample/身份/queue hash可验。
生成JSON没有旧SHA者只按保留OUTPUT/相关ledger证据验证，不倒签新摘要或补造旧trace。

frame唯一大输入为034/P2-frames.npy≤1open/256MiB，独立frame-cache预扣。
准确223,948,928B/完整SHA同时匹配034 input/FRAME_CACHE_VERIFIED/OUTPUT；
完整copy/fsync/前后stat/fd稳定、新SHA与48 RGB/uint8/NPY shape/有限递增times全部验证。
不能hardlink/symlink/改像素/重编码或新抽帧。P2 head/media/target关系沿用，不读MP4/partial正文。
当前worker科学配置须逐字段等于冻结版本；private factory/helper AST保持原义。
only-P2原BCDA四槽，新完整16槽queue不可缩成N1。

源文件≤8份各≤1MiB：上述4缓存source＋至多4个由本轮错误stack明确指向的已安装runtime
确切模块源码/支持文件，仅读有界源码/元数据以确认修复；不做环境或目录扫描。
config≤4份各≤1MiB：原两个model config及至多2个诊断精确指向的非凭据runtime配置。
normal local-only imports/processor/模型资产加载只在既有获准目录，禁止其他研究数据/凭据读取。

## 6. 新资源与科研边界

| 资源 | 035新上限 |
|---|---|
| 文本研究输入 | ≤48MiB；25handoff含ledger≤2MiB（其余1MiB）、source≤8×1MiB、config≤4×1MiB、gold≤1open/4MiB，角色最坏42MiB≤48 |
| 帧cache | 唯一034/P2-frames.npy≤1外部open/256MiB，与文本分账 |
| 新输出 | 仅integration_035≤128文件/512MiB；frame≤256MiB，其余含cache/诊断/fixture/ledger≤32MiB；准确预约＋2GiB余量，同名存在STOP |
| 网络/媒体 | 网络/HEAD/GET/LIST/STS/下载/MP4和partial正文/demux/decode/新帧0 |
| CPU/父 | CPU累计≤900s、父≤3000s；bootstrap≤2×60s、copy≤90s、prepare≤60s、资源query≤10s、score≤60s，cleanup和嵌套PID保守计入 |
| 新suite | ≤3×60s，仅035新模块、按实际变更使用；虚构PID≤4各≤3s（可为0），计CPU |
| GPU | 最多2个串行worker，第二个仅满足零QA恢复条件时；**共享唯一900s绝对包络**，generate全程≤4、原P2槽各≤1、18GiB peak allocated/24GiB Job RAM |
| 查询 | 新nvidia-smi≤1，util仅记录；每GPU worker加载前free复核各≤1（合计≤2），不额外起探测模型 |
| 原annotation | 准备/CPU bootstrap正文0；父非继承exclusive handle≤1、2实际probe child各≤5s、各native/Python open≤1且正文0/native32/Python拒绝；直到所有模型Job退出持有 |
| gold | 实际Qwen RETURNED/INVALID＋全部已launch模型Job/PID退出＋完整队列/快照绑定后，独立CPU≤1次/1open/4MiB读取原四题gold；guard先消费，坏gold/半读不重开，无返回gold0 |

CPU预扣建议45初始化＋180suite＋12虚构PID＋90copy＋60prepare＋120bootstrap＋20可选runtime
＋10probe＋10query＋60score＋30收尾=637s≤900；其余定点核验共享900，不作额外预算。
研究CPU额度较034增加用于实际定位/修复，GPU总额/生成规模不增加；
034曾失败的worker已结束，不计入本035两启动但其历史不抹去。
保留已有准确runtime/PATH，若必要只允许一次≤20s既有确切conda入口stdlib解析；
不环境列表/重装/升级/迁移/改系统设置。新worker/cache过程环境不等于持久环境修改。

原Qwen3-VL-4B BF16/SigLIP F32、SDPA、local-only、seed19/greedy64保持。
逐call实测12帧/grid[6,12,18]/324 visual tokens及总文本长度，报告q/a/b未截断/实际长度、
图像编码/选择/Qwen成本、EOS/截断/峰值。CPU bootstrap输入通过不能冒充GPU前向通过。
训练/backward/optimizer/LoRA/新人工标签/付费API/云GPU/权重或包下载0。

保留025 full-N4计划执行得分；NOT_RUN无正确贡献但不是已观测答错，主表列完整终态/未观测数，
六配对both_wrong含未执行者时明确披露；P2仅条件个案，不替代N4或扩大独立样本量。
gold无效/缺退出/坏绑定则准确率与配对UNKNOWN，不读旧预测/gold补分。
C=D仅真实selector后判断；全同写NO_REALIZED_SELECTION_CHANGE，不调参找差异；
同帧同prompt/tensor却答不同为实现/可复现性问题。最高EXPLORATORY_DEV_CASE，
无稳定效应/泛化/统计显著/创新结论。NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、
Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。

## 7. 公共allowlist（仅六处）

1. prototypes/development_pilot_030.py：固定035、新034 archive/缓存、局部child环境、
   CPU bootstrap监督/两attempt共享包络与全部退出/queue/score绑定、预算和回执。
2. prototypes/development_worker_030.py：共享startup helper、精细阶段/无递归诊断、
   证据驱动定点policy/局部兼容修复、035 attempt绑定；科学实现保持。
3. prototypes/test_development_startup_035.py：本轮定点组合见证。
4. docs/codex-artifacts/VLM-DEV-STARTUP-RECOVERY-035/startup-recovery-and-real-run-receipt.md。
5. docs/codex-artifacts/VLM-DEV-STARTUP-RECOVERY-035/scientific-results.md。
6. docs/codex-results.md：末尾唯一035父记录。

不改media模块、旧tests/报告/README、AGENTS/board/overview、025–029基础模块/科学协议或旧results。
所有细路径/stack/UID/映射/题事件选项gold预测原文、精确PTS/选帧/向量/hash/credentials/
原始XML/权重/媒体都留私人；公共只匿名类别/阶段/错误码/聚合与取整proxy。
不制造“034根因已知”的历史回执。一次普通安全push后STOP，不自动036。

## 8. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview及
> VLM-DEV-STARTUP-RECOVERY-035 README和引用资料，确认唯一未交付READY035，连续完成A–H。
> 我在已确认有效研究许可与SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE开发口径下，
> 明确授权035一次只读034确切缓存和合同限定runtime诊断source/config：文本≤48MiB、
> P2帧≤1open/256MiB，新integration_035≤128文件/512MiB。旧034只读、不复用余额。
> 网络/下载、MP4/partial正文、demux/decode0；原N4/20选项/16槽保持，only-P2原四槽各新答≤1次
> （即使历史答过）、全程generate≤4，其余12槽NOT_RUN。
> 允许同一实际policy下CPU bootstrap≤2×60s，真实imports/CPU processor但不载模型权重/
> 不做GPU或QA前向；定位后按合同定点修复并继续真实四臂，不只交日志。
> 允许自有child在import前将必要cache/TEMP路由新root，以及合同限定的确切runtime只读修复；
> 不移除audit/OS原文件隔离，不改ACL/永久环境或安装，不开放网络/任意子进程。
> 沿用显存有界共享政策：util仅记录，一次新query核正确设备/free≥20GiB；
> 每worker加载前再核free，peak allocated≤18GiB、Job RAM≤24GiB。
> 允许最多2个串行GPU worker，共享唯一900s绝对包络；第二个只在首Job/PID实测退出、
> 全035 STARTED=0、有技术证据并定点修复/新suite验证后启动。任何STARTED后禁止重启/重答，
> OOM/timeout不作为重启理由，不kill peer或重query。
> CPU≤900s/父≤3000s，新035 suite≤3×60s、只按真实代码变化使用，不重跑历史tests。
> 原annotation准备/CPU bootstrap正文0、父独占handle与2实际零正文probe按合同；
> 仅真实Qwen返回、全部已launch模型Job/PID退出与完整queue/raw绑定后，
> 独立CPU scorer≤1次/1open/4MiB读取原四题gold，失败/半读不重开。
> 全分母保留FAILED/INVALID/NOT_RUN，不读旧答案/预测、不换题/模型/提示或调科学阈值、
> 不训练/下载/改系统环境、profile或凭据。按六处allowlist交付代码、两匿名报告和
> results一个035父记录，一次安全push main后STOP，不自动036或扩大生成/下载。
