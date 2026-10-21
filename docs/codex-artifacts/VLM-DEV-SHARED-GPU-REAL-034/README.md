# VLM-DEV-SHARED-GPU-REAL-034：显存有界共享运行，完成P2四臂与独立评分

2026-10-21（北京时间）。ChatGPT研究负责人；用户Windows本地Codex执行。
**唯一READY父任务034 / PUBLIC_SHARED_GPU_INTEGRATION_ONLY，尚未执行。**
公共定点实现可领取；第7节用户实际发送的一条明确消息共同激活新缓存/GPU/gold范围，
并接受本轮显存有界共享政策。公共READY、旧033许可或过往预算不能自动激活本轮真实运行。
033已关闭；不重开旧run/锁/时钟、不复用旧suite/GPU余额，不要求重新申请已确认的数据研究许可。

## 0. 验收与本轮改变

033交付[91157ef](https://github.com/floomeer83felix-source/vlm/commit/91157ef4838f11f45153a4b017dc4c0b34e5e2a4)
按 **ACCEPTED_CACHE_HANDOFF_AND_OFFLINE_FIX / RESOURCE_WINDOW_HOLD / REAL_QA_NOT_RUN** 结案。
P2原帧cache已完整复制：223,948,928B、48 RGB摘要/uint8/shape/有限严格递增时间全部验证。
新两suite均6/6 PASS；真实prepare/独占handle/2零正文probe通过。
实际两次query观察同一3090/UUID/bus、WDDM，free22,915/22,919MiB、util16%/22%。
最初parser要求minor_number=0，被真实N/A触发033_DEVICE_IDENTITY/child exit1；
后来修正并用剩余suite验证，没有重query。第二样本22%另超原20%上限，
所以修parser也不能让那次观测合格。没有RESOURCE_ADMITTED、模型/生成/GPU/gold，全16槽NOT_RUN。
不得把原child异常倒写成实际执行过的threshold异常，也不把修后的parser宣称已通过真实准入。

本轮**明确替换运行政策**，不是把033历史HOLD改成PASS：
NVIDIA的GPU util是短采样期间有kernel执行的时间比例，无法单独说明进程归属、显存容量
或未来持续负载；20%是上一轮操作阈值，并非科学预注册的自变量或厂商安全界限。
034允许设备已有C/G/C+G上下文及较高短时利用率；**利用率只记录，不再作为启动否决阈值**。
不提高利用率阈值去寻找“合格低负载样本”，不连续等待/重复采样。
仍要求正确设备、足够当前free显存、18GiB allocator上限/24GiB Job RAM/900s完整时限，
不保证全局独占、无peer或绝无OOM。用户须在同一启动消息明确接受该共享条件。
没有真实QA输出被用来制定这个运行政策；科学输入/算法/输出规则保持不变。

依据：[NVIDIA query/identity/Utilization](https://docs.nvidia.com/deploy/nvidia-smi/index.html)；
[PyTorch mem_get_info](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.mem_get_info.html)；
[allocator fraction](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.set_per_process_memory_fraction.html)。
这些资料解释API语义，不认证本机当前状态；不得安装NVML/改driver以“完善监控”。

沿用[030开发协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)：
DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。
仅复用P2已有48帧，网络/下载/MP4或partial正文/demux/decode均0。
原N4/20选项/16槽/ABCD、BCDA、CDAB、DABC轮转完整保留；P2四槽执行，其余12槽NOT_RUN。
025窄语法、48→12、C/D同双锚点/共享q/a/b、目标/tie/补齐、i≠j对i<j均不改。
P3 participant缺失仅披露，不追旧registry/来源独立证书，不换题或扩样。

## 1. A–H同轮任务

| 项 | 工作与必须提供的证据 |
|---|---|
| A / 新交接 | 安全同步独立docs main，重读AGENTS/board/results/overview、本合同、033两报告及030科学协议。确认唯一未交付034。先完成公共实现，再原子创建已知018根/integration_034，新contract/run/034.lock/034-ledger/2400s父时钟；033只读第3节确切文件。 |
| B / 定点接入 | pilot/worker仅实现固定034、新archive/缓存交接、一次资源query及共享政策、run/resource/queue/score绑定；保留已修WDDM身份兼容、Win32/Job和科学实现。关闭旧运行入口，不复制runner。 |
| C / 本轮新见证 | 新test_development_shared_gpu_034.py最多2次各完整≤60s；少量虚构XML/缓存/ledger验证本轮差异。首PASS即真实；不重跑033六项或031 OS演示，不新排模型/数据资格任务。 |
| D / 当前缓存与隔离 | 只读一次033/P2-frames.npy≤256MiB，copy到新根并匹配033已验证完整SHA、48 RGB摘要及NPY结构，原像素/时间保持。准备原annotation正文0；父非继承独占handle与两个真实零正文probe必须实际过门。 |
| E / 真实四臂 | 一次当前设备/free查询过门后立即唯一GPU worker；加载前一次global free核验，原P2四槽BCDA各generate≤1，总≤4。真实跑SigLIP/selector/processor/Qwen，逐调用核对12帧/grid[6,12,18]/324 visual tokens。 |
| F / 一次score | 全模型Job/PID实测退出、完整16槽终态及run/plan/worker/queue/resource/launch/exit一致后封闭队列，释放annotation handle；有真实RETURNED/INVALID才独立CPU scorer≤1open/4MiB，完整028 raw快照/profile绑定，guard消费后失败不重开。 |
| G / 科研解释 | 全N4终态/执行得分/六配对与未观测者，P2条件个案，C=D/选择差异/目标/跨度proxy、检索/图像编码/Qwen成本、真实tokens/截断/EOS。没有实际回答就明确NOT_RUN，不从资源修复推导效应。 |
| H / 一次push STOP | 六处allowlist统一交付、results一个034父追加，普通安全push后STOP。不自动035、增加下载/worker/生成或改prompt/阈值；真实异常照实记录，不能隐瞒失败。 |

## 2. MEMORY_BOUNDED_SHARED_GPU_034（不再以利用率低于20%为前提）

- 用一个受控stdlib child执行**最多一次**既有nvidia-smi -q -x -i 0，
  从启动到capture/parse/清理完整≤10s，计CPU600。完整有界XML≤64KiB、exit0/Job0，
  不静默截断、不用旧033样本代替、不等待低利用率、不循环/第二query/后台dmon或pmon。
- 固定query index=0、RTX3090，非空可用UUID与bus必须匹配033两份一致观测的设备身份，
  UUID/bus仅私人保留。minor_number仅metadata，N/A或不同于Unix minor0不单独否决；
  实际命令index/UUID/bus错误、缺失身份或多设备歧义仍HOLD，不按空值猜设备。
- 当前free显存要求准确MiB单位、有限数值且≥20GiB。缺失/N/A/错单位/不足均HOLD。
  util与driver model/context数量为观测：合法0..100%如实记录，N/A/缺失/非有限值记UNKNOWN；
  util未知或>20%本身均不阻止启动。不得把UNKNOWN记0、22%记空闲或宣称没有其他模型。
  不做进程命令行/目录/身份盘点，不以C+G数量否决或虚构纯桌面白名单。
- 新RESOURCE_ADMITTED只由本034实际query生成，绑定run/queue/profile/采样摘要/设备。
  它证明的是“当前设备身份/free通过＋用户接受共享政策”，不签发空闲/独占证书。
  父、worker和score均验证这条receipt；033旧profile/旧样本永远不能直接放行034。
- 唯一worker内权重加载前，保留一次torch.cuda.mem_get_info(0)核global free≥20GiB，
  实际device名称/total与现有3090范围一致；该CUDA初始化/查询计入GPU900s。
  不足或异常即退出，不通过二次worker/查询/降精度恢复。
  allocator fraction在load前设置18GiB/total，逐阶段/调用保留peak allocated≤18GiB，
  报告peak reserved；Job RAM≤24GiB、GPU完整窗口≤900s不变。
- 允许共享不意味着预留全设备资源；fraction约束PyTorch caching allocator，
  不能冒称所有CUDA/driver分配的全局硬上限。OOM/timeout/设备异常不重启，
  不更换模型/dtype/像素/帧数，不改compute mode/driver/电源/时钟、暂停或kill peer。
  已有明确用户任务冲突或OS/CUDA明确拒绝仍停止，不以共享政策覆盖明确冲突。

本政策只改变执行资源条件，不改变数据准入、gold隔离、科学选择/预测或预算。
一条用户启动消息同时接受上述条件并给本轮新scope，无额外激活确认循环。

## 3. 只读033 archive与直接缓存交接

不实例化旧Journal/锁、不修改旧epoch、RUN_STOPPED、输入或frame。
增加专用033 archive验证器，保留旧030/031/032 validator原义：
完整hash链/seq/prev/末尾换行及RUN_STOPPED、REAL_033/root/run，
两条suite均6/6 PASS且run一致，16唯一NOT_RUN；
真实HTTP/媒体获取/STARTED/MODEL_LAUNCH/WORKER_FREE_RECHECK/RESOURCE_ADMITTED/SCORE_CONSUMED/gold均0；
恰有一次FRAME_CACHE_VERIFIED/完整frame input摘要和2次GPU_QUERY，
实际resource child exit1/Job0（原parser失败保留），copy/probe等实际阶段Job0。
033的模型/媒体获取确实0，但有frame读和resource query；不得用旧零动作断言误拒绝。
无需对旧16%/22%用新政策重算PASS，更不能补一条历史RESOURCE_ADMITTED。

文本handoff≤22份、每份≤1MiB（033-ledger.jsonl单份可≤2MiB），各1外部open：
八个keys/cohort/nongold/plan/receipts/targets/heads029/official JSON；
033-ledger.jsonl、annotation-reference.json、execution-config.json、runtime.json；
worker-input.json、queue.json、expected-snapshot.json；
P2-head.json、P2-media-binding.json、P2-candidates.json；
033-final-summary-private.json、gpu-samples-private.json、
frozen-worker-032.json、frozen-snapshot-032.json。
只确切033根，不扫描原研究目录/032/其他历史缓存或新manifest。

八JSON/四factory_0/1.py、runner_0/1.py直接匹配033 INPUT_COMPLETE size/SHA及OUTPUT大小。
P2 HEAD/candidates/annotation等有033输入摘要者按相应cache alias直接校验；
033 FROZEN.plan_hash/worker_hash绑定完整plan/worker-input，worker等于保留frozen-worker-032；
expected snapshot等于frozen-snapshot-032，原三份028 raw receipt/profile一致。
旧queue完整16槽/原run/only-P2 availability需相符，但不是本034运行队列。
P2 media/HEAD/target/版本/候选关系保留，生成JSON缺历史SHA者按OUTPUT大小和相关ledger事实交叉核验，
不把新摘要倒签成旧摘要，不回原annotation/MP4补资料。

frame唯一大输入为**033/P2-frames.npy**，≤1外部open/256MiB，单独frame-cache类别预扣。
当前完整size/SHA必须同时匹配033 INPUT_COMPLETE(frame-cache)、FRAME_CACHE_VERIFIED及OUTPUT；
路径/fd身份与前后stat稳定，完整chunked copy/fsync到新根后重算SHA一致，
再复用033 stdlib NPY/48 RGB hash/有限严格递增时间验证。
033已有223,948,928B完整file SHA证据可直接继承；不再把它当“尚无历史完整SHA”的032场景。
不能hardlink/symlink、改像素、补帧/解码；不符HOLD、不续读原MP4或旧partial。
原033帧的完整验证不是034当前输入自动通过，当前copy证据仍实际取得。

新root原样保留科学worker配置/完整source列表/20选项/16槽及rotation，
新queue.available固定P1=false/P2=true/P3=false/P4=false；
其他12槽NOT_RUN/NOT_AVAILABLE_FROM_CLOSED_CACHE，P2四槽按原BCDA。
父与worker同时限制only-P2/原slot/每槽一次/总STARTED≤4，不加入任何后来可用的媒体。
runtime沿用准确pytorch Python/PATH/模型路径；不再盘点环境。
若确切runtime失效，仅既有准确conda入口一次≤20s stdlib解析（CPU总额内），失败STOP。

## 4. 本轮定点见证与实际执行纪律

仅新test_development_shared_gpu_034.py，不import/运行旧test_development_cached_gpu_033或030–032套件。
fixture不联网、不读真实缓存/annotation/gold、不导入ML/GPU：
- 单次真实格式XML能以WDDM minor=N/A/稳定UUID/bus准入；util22%/100%或N/A仅如实记录，
  free合格即可；free不足/NaN/错单位/设备或UUID错/截断XML/多设备拒绝。
  此测试证明新操作规则，不用“放宽旧expected”改033历史测试。
- closed033两PASS/0模型/完整frame SHA链可交接；tamper/缺STOP/错误frame摘要/
  有真实model或gold拒绝。小NPY完整copy/shape/48RGB与逐字节摘要不符拒绝。
- 固定034 root/run/purpose/新suite、单QUERY/RESOURCE_ADMITTED及queue/worker/score绑定；
  旧033 profile/旧资源receipt/错run/错queue或退出摘要拒绝、opener0。
  full16 slots、only-P2/BCDA/≤4STARTED规则保留，科学worker字段变化拒绝。
- production网络/媒体获取事件仍在落账门硬拒绝；execute不调用get/demux/decode。
  同一query槽、STARTED或gold guard重入拒绝，不靠更换mode/新对象领取余额。

显式expected/loaded/run、FAIL/ERROR/SKIP；0发现/skip不是PASS。
最多2个新suite各完整≤60s，首PASS立即真实prepare/copy/当前probes/query→GPU→score。
有一次明确失败可修定点问题并用尚未消费第二suite验证；二次仍败停止。
PASS后关键分支再改也要在剩余suite内验证，不以static冒充真实已测。
虚构PID≤4各≤3s（无需可为0），计CPU600；不重复031实际OS/独立虚构score演示。
原Win32/Job与完整窗口/退出算法保持；当前真实annotation探针和模型退出仍实际验证。
GPU/生成失败不重启、score失败不重开，不交成“资源门过了等待下一轮GPU”。

## 5. 034新额度与科学表达

| 资源 | 本轮硬上限 |
|---|---|
| 文本研究输入 | ≤40MiB；handoff≤22份（21×1MiB＋ledger≤2MiB）、source≤4×1MiB、config≤4×1MiB、最后gold≤1open/4MiB；角色最坏35MiB≤40 |
| 帧cache输入 | 仅033/P2-frames.npy≤1open/256MiB，独立预扣，不能混进文本计数或漏记 |
| 新私有输出 | 仅integration_034≤128文件/512MiB；frame≤256MiB，其余含ledger/fixture≤32MiB；精确预约＋2GiB余量，同名存在STOP、不改suffix/覆盖 |
| 网络/媒体 | 所有研究HTTP/HEAD/GET/LIST/STS/下载0；MP4/partial正文、demux/decode/新帧0；原033/032只读，不续传 |
| CPU与父 | CPU累计≤600s、父≤2400s；copy验证≤90s、prepare≤60s、资源child≤10s、scorer≤60s，cleanup/嵌套PID均计入 |
| 新测试 | ≤2×60s，虚构PID≤4各≤3s、串行计CPU；不重跑旧suite |
| GPU | 唯一worker≤1、仅P2原四槽generate≤4，每槽一次；imports/load/编码/processor/生成/内存复核全阶段≤900s，peak allocated≤18GiB、Job RAM≤24GiB |
| 当前GPU查询 | nvidia-smi≤1次、无util阈值；worker权重前mem_get_info≤1次；无等待循环/重query/kill peer |
| 原annotation | 准备正文0；父非继承exclusive share handle≤1，模型期间持有；2实际probe child各≤5s，每child native/Python open各≤1，均正文0且native32/Python拒绝才过 |
| 最后gold | 实际Qwen RETURNED/INVALID＋全模型Job/PID实测退出＋完整队列/快照绑定后，独立CPU≤1次/1open/4MiB读取原四题gold；guard先消费，坏gold/半读不重开，无返回gold0 |

建议CPU预扣45初始化＋120suite＋12虚构PID＋90copy＋60prepare＋20可选runtime＋10probes
＋10query＋60score＋30收尾=557s≤600。分开报告预扣/实测wall与真实字节、未测分支，
不能把窗口当逐PID CPU实测。模型正常在原批准目录local-only只读加载，不下载任何资产。
Qwen3-VL-4B BF16/SigLIP F32、SDPA、seed19/greedy64、helper AST/prompt/processor不变。
逐调用实测12帧/grid[6,12,18]/324 visual tokens，另报总文本长度、q/a/b截断和检索/图像/Qwen成本、
EOS/生成截断、模型阶段/峰值。optimizer/backward/LoRA/训练/新人工标签/云GPU/付费API、
安装/迁移/环境或ACL/profile/凭据修改0。

保留025 full-N4计划执行得分口径，不改scorer。gold完整有效时NOT_RUN无正确贡献，
但不是已观测答错；主表列RETURNED/INVALID/FAILED/NOT_RUN/未观测数，六配对说明原both_wrong
包含未执行者，不能解释成三个真实共同错误。另列P2条件个案，不能取代N4/算独立泛化证据。
gold未验证/退出或绑定不符时准确率与配对UNKNOWN，不用旧答案/预测补分。
C=D仅实际selector后判断；全同则NO_REALIZED_SELECTION_CHANGE，不调参寻找差异；
同帧同prompt/tensor却答不同为实现/可复现性问题，不能叫顺序机制收益。
最高EXPLORATORY_DEV_CASE；单个P2正负均不支持稳定效应/统计显著/创新。
NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。

## 6. 公共allowlist（仅六处）

1. prototypes/development_pilot_030.py：固定034、新033 archive/直接SHA帧交接、
   一次显存有界共享resource/queue/execute/score绑定与新回执；保留Win32/Job算法。
2. prototypes/development_worker_030.py：必要034/profile/resource/only-P2四槽关联，
   保留加载前free/allocator门，其他模型/selector/提示/processor不改。
3. prototypes/test_development_shared_gpu_034.py：本轮新定点见证。
4. docs/codex-artifacts/VLM-DEV-SHARED-GPU-REAL-034/shared-gpu-and-score-receipt.md。
5. docs/codex-artifacts/VLM-DEV-SHARED-GPU-REAL-034/scientific-results.md。
6. docs/codex-results.md：末尾一个034父结果。

不改media模块、旧tests/报告/README、AGENTS/board/overview、025–029基础模块或科学协议，
不重写033 HOLD/旧采样/错误。公共无私人默认路径或受限helper全文；
只匿名聚合/终态/取整proxy，不公开UID/映射/题事件选项gold预测原文、私有路径/URI/hash、
原始XML/PID名单/精确PTS/选帧索引/向量/凭据/媒体/权重。
一次普通安全push后STOP，不自动035或追加运行。

## 7. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview及
> VLM-DEV-SHARED-GPU-REAL-034 README和引用资料，确认唯一未交付READY034，连续完成A–H。
> 我在已确认有效研究许可及SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE开发口径下，
> 明确授权034一次只读033确切缓存：文本≤40MiB、P2帧≤1open/256MiB；
> 新integration_034≤128文件/512MiB。不重开033/沿用余额，不重跑旧tests。
> 本轮网络/下载、MP4/partial正文、demux/decode均0；只完整核验并复制原P2的48帧。
> 原N4/20选项/16槽/轮转保持，仅P2四槽可各新答一次（即使历史答过），其余12槽NOT_RUN。
> 我明确接受MEMORY_BOUNDED_SHARED_GPU_034：允许现有C/G/C+G上下文及较高短时利用率，
> 利用率仅记录，不再要求≤20%或设备空闲/独占；只做一次当前nvidia-smi query，
> 正确3090/UUID/bus且free≥20GiB才启动，worker加载前再核free一次；
> 不杀peer/循环等待，OOM或timeout不重启，显存/时限/退出/gold保护不取消。
> 允许唯一GPU worker/generate≤4，GPU总≤900s/peak allocated≤18GiB/Job RAM≤24GiB；
> CPU≤600s/父≤2400s，新suite≤2×60s，首PASS同轮真实四臂→独立score→科研报告。
> 原annotation准备正文0、父独占handle和2真实零正文拒绝probe按合同；
> 仅真实Qwen返回、所有模型PID/Job实测退出与完整队列/快照绑定后，
> 独立CPU scorer≤1次/1open/4MiB读取原四题gold，失败/半读不重开。
> 全分母保留FAILED/INVALID/NOT_RUN，未执行不解释成已观测答错；
> 不读旧预测/gold产物，不换题/模型/提示或调科学阈值，不训练/安装/改环境、ACL、profile或凭据。
> 按六处allowlist交付代码、两匿名报告和results一个034父记录，
> 一次安全push main后STOP，不自动035或增加生成/下载。
