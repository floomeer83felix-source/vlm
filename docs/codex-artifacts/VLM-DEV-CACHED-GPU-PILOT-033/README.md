# VLM-DEV-CACHED-GPU-PILOT-033：复用P2候选帧，完成真实四臂与独立评分

2026-10-21（北京时间）。ChatGPT研究负责人；Windows本地Codex执行。
**唯一READY父任务033 / PUBLIC_CACHED_GPU_INTEGRATION_ONLY，尚未执行。**
先实施公共定点改动。第7节用户实际发送的一条明确新消息同时激活本轮私人缓存读取/写入、
新GPU与最终gold范围，并明确接受第2节资源政策；公共READY本身不激活这些操作。
032结案，不恢复旧run/锁/时钟，不用其未用suite/GPU余额。研究许可与允许来源重合开发口径已确认，
无需重新申请数据访问或调查旧source登记。

## 0. 审查与本轮目标

032交付[2636333](https://github.com/floomeer83felix-source/vlm/commit/2636333f08b694c84c516a30c2c0ef828729ae40)
按 **ACCEPTED_TRANSPORT_AND_P2_CANDIDATES / GPU_RESOURCE_HOLD / REAL_QA_NOT_RUN** 结案。
新suite首且仅一次6/6 PASS；四个当前对象GET均200，正文前响应版本/ETag/长度绑定031。
P2完整取得并通过CPU候选检查；P1/P3/P4分别超时，partial留原032不续传。
P2候选48帧、95,226 packets/0 corrupt/0 missing、时间有限且严格递增，
duration/span约3174s、声明差<0.01s。不是绝对时钟或事件召回认证。
真实原annotation两probe均native32/Python拒绝/正文0，独占handle保留到关闭。

唯一nvidia-smi成功，free22,813MiB已过20GiB，但旧all('C' not in type)因37个C+G记录失败。
[NVIDIA官方Processes说明](https://docs.nvidia.com/deploy/nvidia-smi/index.html#processes)
定义C+G为同时存在Compute/Graphics contexts；它不是瞬时负载或独立模型任务数。
不能倒写032“确有37个训练任务”，也不能倒写“已证全部只是桌面进程、GPU持续空闲”。
032没有放宽旧门；model/generate/GPU/gold0，全16槽NOT_RUN，准确率UNKNOWN。

033是研究负责人明确改变资源政策后的新有界执行：
**只用已通过的P2帧缓存，不再下载，不补另外三源**，原N4/16槽不变，只有P2四槽可启动。
沿用[030开发科学协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)：
DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE，P3 participant缺失仅披露。
原4题/20选项、ABCD/BCDA/CDAB/DABC轮转、48→12、C/D同双锚点与共享q/a/b、
目标/tie/补齐、i≠j对i<j、原模型/提示/processor/贪心设置均不变。
不是把P2改成新benchmark N1；不以缺媒体为由换题/替代来源或追求正例。

## 1. A–H同轮交付

| 项 | 工作与实际验收 |
|---|---|
| A / 新交接 | 安全同步独立docs main，重读AGENTS/board/results/overview、本合同、032两报告及030科学协议。确认唯一未交付033。公共实现后原子建已知018根下integration_033、新contract/run/033.lock/033-ledger/2400s父时钟。032只读第3节确切缓存。 |
| B / 定点实现 | 原030 pilot/worker仅新增固定033、只读032 archive/帧缓存交接、零网络/只P2四槽和第2节资源门；保留Win32/Job、score保护与模型科学实现。不复制runner、不改旧报告/tests。 |
| C / 少量新见证 | 只新test_development_cached_gpu_033.py，显式loader，最多2次各完整≤60s；仅虚构XML/缓存/ledger验证第4节变化，无旧套件、联网或ML/GPU。首PASS即进入D，不重复031 OS演示或032 transport演示。 |
| D / 复用真实候选 | 新scope激活后只读一次032的P2-frames.npy（≤256MiB），完整复制到新根并核对48个原RGB摘要、NPY shape/dtype与候选metadata；不读取MP4/partial正文、不重新demux/decode/抽帧。原annotation只身份/stat；当前父独占handle与2零正文实际probe必须过门。 |
| E / 真正四臂 | 按第2节两次短窗资源门过后，唯一GPU worker；仅P2四个原槽最多各generate一次，原其余12槽NOT_RUN。实际跑SigLIP q/a/b、四臂选择、原helper/processor和Qwen回答，核实12帧/grid[6,12,18]/324 visual tokens；不因C=D而更改算法或重答。 |
| F / 独立score | 所有模型Job/PID实测退出、全16槽终态、run/plan/worker/queue/launch/exit一致，先封闭队列再释放annotation handle。有真实RETURNED/INVALID才一次独立CPU scorer≤1open/4MiB；同028完整快照/profile，guard先消费，失败不重开。 |
| G / 科研解读 | 匿名逐源/逐臂终态、全N4计划执行得分与六配对、P2单个已执行个案、C=D/选择差异/目标/跨度proxy、检索/图像编码/Qwen耗时、真实token/截断/EOS。区分NOT_RUN与观察到答错，不把3个缺媒体当3个算法负例。 |
| H / 一次push STOP | 六处allowlist统一提交，results一条033父追加、安全普通push后STOP。不自动034、不增加GPU worker/生成/下载，不交成“门修好待下一轮”；实际前置或模型失败照实结案。 |

## 2. 新资源政策：WINDOWS_SHARED_LOW_LOAD_033

这是本轮明确替换“进程type含C即禁止”的运行条件；**不要求设备零上下文或全局独占**。
短窗观测不证明没有其他模型、未来无竞争或全机空闲；只支持在用户明确接受的共享条件下尝试
一次≤900s/≤18GiB allocated的任务。不得把C+G认成纯图形，也不得把所有C类一律过滤后假称无peer。

- 在一个受控stdlib child内，最多执行**两次**既有nvidia-smi只读查询，间隔≥1s；
  两次从启动到清理共享完整≤20s窗口（计CPU600内），没有等待低负载的循环/第三次query。
  可沿用已实际支持的nvidia-smi -q -x -i 0，严格有界完整capture/parse，不静默截断成假完整输出。
  原始XML仅私人保留；公开仅匿名聚合。无pmon/dmon后台监控、进程命令行/目录/凭据扫描。
- 两次都必须成功，锁定同一device0/RTX3090与同一UUID（UUID仅私人），
  free显存均≥20GiB、GPU利用率均为有限0..100且**≤20%**。字段缺失/N/A、解析失败、
  设备不同、任一超限均HOLD；不把UNKNOWN当0或沿用032旧22,813MiB。
  利用率是该采样窗口有kernel执行的时间占比，不是每个进程的负载归因。
  20%是本轮保守操作阈值，不是NVIDIA推荐或无竞争证明。
- 记录driver model及C/G/C+G等类型数量作为上下文，不用数量/类型单独否决。
  不要求WDDM每进程显存都可得（官方说明该模式可能不可用），
  不按basename做臆造桌面白名单，不调查/暂停/kill其他进程，不改driver/compute mode/时钟。
  若已有明确用户任务冲突或OS/CUDA明确拒绝，仍停止；不以低负载覆盖已知冲突。
- 模型worker必须绑定本033 RESOURCE_ADMITTED receipt的run/device/queue/profile；
  启动前没有真实合格receipt则MODEL_LAUNCH=0。
  在唯一已启动worker内、权重加载前，再一次torch.cuda.mem_get_info(0)核对global free≥20GiB；
  不足/异常HOLD，不另启动探测模型、不重复查询等资源。该调用及CUDA初始化均计GPU900s。
- 权重加载前设置原torch.cuda.set_per_process_memory_fraction(18GiB/total_memory)，
  保留peak allocated≤18GiB、峰reserved记录、24GiB Job RAM与完整GPU≤900s。
  allocator限制不等于全设备显存/所有CUDA非Torch分配的硬隔离；不能这样宣传。
  OOM/资源变化/模型异常不重启、不改dtype/分辨率/帧数或模型，不终止peer。

依据：
[NVIDIA Processes/Driver Model/Utilization](https://docs.nvidia.com/deploy/nvidia-smi/index.html)；
[PyTorch mem_get_info](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.mem_get_info.html)；
[allocator fraction](https://docs.pytorch.org/docs/stable/generated/torch.cuda.memory.set_per_process_memory_fraction.html)。
文档只解释观测/API语义，不认证本机当前状态或替代实际receipt。

## 3. 032 closed archive与缓存交接

只从确切integration_032只读，不拿旧锁、不实例化旧Journal/改时钟、不更改/删除旧partial。
不放松030/031 archive规则；增加专用032完整hash链/seq/prev/末尾RUN_STOPPED验证：
REAL_032/run/root一致、首且仅一6-case PASS、16唯一NOT_RUN、四HTTPS/TRANSPORT_SEND/200 RESPONSE
对应同四对象且无新HEAD、仅P2 MEDIA_COMPLETE及其GET/candidates阶段exit0/Job0；
其他三个GET超时退出且Job0；真实STARTED/MODEL_LAUNCH/SCORE_CONSUMED/gold均0。
032有真实body/媒体，不能套用“旧零body”validator误拒绝，也不能把fixture子树当真实动作。

研究文本handoff白名单≤20份（每份≤1MiB，**032-ledger.jsonl单份可≤2MiB**）：
八个keys/cohort/nongold/plan/receipts/targets/heads029/official JSON；
032-ledger.jsonl、annotation-reference.json、execution-config.json、runtime.json；
worker-input.json、queue.json、expected-snapshot.json；
P2-head.json、P2-media-binding.json、P2-candidates.json；
032-final-summary-private.json、gpu-resource-exit-private.json。
每份外部输入1open，完整read/前后stat/fstat/摘要由新ledger持久记录，不扫目录、原manifest或旧来源文件。

八JSON与四factory_0/1.py、runner_0/1.py直接匹配032 INPUT_COMPLETE size/SHA及OUTPUT大小。
P2 head与032原cache_P2-head摘要绑定；media-binding与head/准确target/200响应slot/
MEDIA_COMPLETE长度相符；原FROZEN.plan_hash/worker_hash精确绑定plan与worker-input。
旧queue只用于核对固定16槽/原run/available(P2=true，其余false)，不能作为033运行队列。
原annotation-reference/expected-snapshot与三份028完整receipt及当前identity/size/mtime一致。
031/032部分生成JSON没有历史内容SHA，按保留receipt/OUTPUT大小/相关ledger证据交叉验证，
不能要求缺失的旧SHA凭空出现，也不能倒签033新摘要成032实时摘要。

仅P2-frames.npy可作为大输入，≤1open/≤256MiB，单独记frame-cache类别，
不挤进每份1MiB文本输入限制，也不从全局输入计费中漏掉。
复制前预约新根相同文件所需精确size，checked_path/no reparse、前后identity/stat/fstat稳定，
正文分块完整复制/新SHA并fsync，不能hardlink/symlink引用或修改旧文件。
在新根读取NPY，allow_pickle=False、uint8、48×H×W×3、实际shape/字节数与候选一致，
48个RGB摘要逐个匹配原candidate列表，时间有限严格递增，EOF/packet/duration元信息保持。
新SHA是本轮copy完整性证据；没有032历史NPY整文件SHA时不得冒称有。
不重选/改像素/重编码，缓存不符STOP、不回MP4补解码。

新worker-input须与032 FROZEN的科学字段/提示/slots/model保持一致；prepare可以复核原两config、
helper AST及runtime，按原字段生成等值配置，不能把来源列表缩成P2导致题/slot重排。
新033queue保存完整16槽和available={P1:false,P2:true,P3:false,P4:false}，
P1/P3/P4十二槽预先终态NOT_RUN/NOT_AVAILABLE_FROM_CLOSED_032；P2按原BCDA顺序执行。
STARTED只允许P2、四个原slot/arm各一次，总≤4；worker和score同时验证固定availability。
其余alias即使其他目录恰有媒体或后来下载完成也不加入本轮。

032旧模型/gold实际0；本轮四次是新有界回答，允许这些题历史研究可能答过。
runtime沿用032准确pytorch Python/PATH/模型目录，不重新盘点环境；若确切runtime不可用，
仅可用既有确切conda入口1个≤20s stdlib-only child解析（计CPU），失败STOP。
模型正常local-only资产只读加载在原批准目录，不视作额外数据下载；不新增/迁移环境。

## 4. 本轮少量有意义的新测试

仅新test_development_cached_gpu_033.py；不import或运行030/031/032旧套件。
fixture用虚构XML/metadata/小NPY/ledger，无真实媒体、QA/gold、ML导入、GPU或联网：
- C+G存在但两短窗资源合格可通过；free不足/高负载/N/A/NaN/错单位/不同device/错UUID/
  truncated输出均拒绝，两个样本不足不通过；不以process类型或数量伪造负载值。
- 正常032 partial-media closed archive可交接，tamper/截断/未STOP/有model或gold拒绝；
  eight cache byte hash、P2 head/length/frame mismatch拒绝；小NPY只读copy完整，size/hash不符不入队。
- 固定033root/run/suite/RESOURCE_ADMITTED/queue/worker绑定，旧032 receipt不能放行；
  16槽完整，only-P2/≤4STARTED规则在生产父与worker均有效，错availability/重slot拒绝。
- production score绑定在完整退出前opener0；有四P2终态＋十二NOT_RUN的完整fixture可通过逻辑门，
  run/queue/资源receipt/退出错绑拒绝；不再重复031实际独立虚构PID评分演示。
- 网络/get/metadata/decode入口不由033execute调用；在生产033实际send预扣门硬拒绝HTTPS事件，
  即使错误调用旧媒体helper也在任何实际传输前拒绝。不读取SDK/凭据试探联网。

显式expected/loaded/run、FAIL/ERROR/SKIP/receipt，0发现或skip不是PASS；
新suite≤2次各完整≤60s，首PASS即真实，二次仍败停止。虚构PID≤4各≤3s（无需求可为0），计CPU600。
同轮PASS后若改变本轮关键被测分支，必须用尚未消费的第二suite验证，否则不进入真实路径。
Win32/Job/评分算法保持031既有实现，只改固定033路由；真实本轮probes/模型退出/score仍实际执行。

## 5. 033新额度与科学报告

| 资源 | 新上限/约束 |
|---|---|
| 文本输入 | ≤40MiB；handoff≤20份（19×1MiB＋ledger≤2MiB）、source≤4×1MiB、config≤4×1MiB、gold≤1open/4MiB；各角色最坏33MiB≤40 |
| 大缓存输入 | 仅032/P2-frames.npy，≤1open/256MiB；独立预扣与完整copy摘要，不读旧MP4或partial正文 |
| 新输出 | 仅integration_033，≤128文件/512MiB；frame cache≤256MiB、其他含ledger/fixture≤32MiB；精确预约＋2GiB磁盘余量，同名存在STOP、不换suffix/覆盖 |
| 网络/媒体解码 | 研究网络HEAD/GET/LIST/STS/所有下载0；MP4/partial正文0；demux/decode/新增帧0；不对三partial续传或重下 |
| CPU/父窗口 | 累计CPU≤600s、父≤2400s；frame copy/核验≤90s，准备≤60s，telemetry child≤20s，scorer≤60s，cleanup全部计入 |
| 新suite | ≤2×60s；虚构PID≤4各≤3s、串行计CPU，无旧suite |
| GPU | 唯一worker≤1，原P2四槽generate≤4、每槽一次；总GPU阶段含imports/load/编码/processor/生成/内存复核≤900s，peak allocated≤18GiB、Job RAM≤24GiB |
| GPU资源读取 | nvidia-smi只读实际query≤2、间隔≥1s/总child≤20s；通过后唯一worker内加载前mem_get_info一次；不后台等待、循环或kill peer |
| 原annotation | 准备正文0；父非继承exclusive share handle≤1；2 probe child各≤5s，每child native+Python open各≤1次，均正文0，native32/Python拒绝才继续 |
| gold | 仅真实Qwen RETURNED/INVALID＋全模型Job/PID实测退出＋队列/快照绑定后，独立CPU≤1次/1open/4MiB读取原四题gold；guard先消费，坏gold/半读不重开，无真实返回gold0 |

建议CPU预扣：初始化45＋suite120＋虚构PID12＋copy验证90＋prepare60＋可选runtime20
＋probes10＋资源20＋score60＋收尾30=567s≤600。上限不是实测，分别报告预约/实际wall、
body/文本/frame读写、每Job/PID退出和未测分支，不把预扣当真实消耗。
不新增模型、包或依赖；Qwen3-VL-4B BF16/SigLIP F32/local-only/SDPA/seed19/greedy64不变。
allocator上限必须load前设置，逐call核实12帧/grid[6,12,18]/324视觉token，
另报时间戳引起总文本长度差、q/a/b未截断/实际长度、EOS/生成截断和检索/图像/Qwen成本。
训练/backward/optimizer/LoRA/新人工标签/付费API/云GPU/环境或ACL/profile修改0。

score实现沿用025全N4规则，不改历史统计口径。gold完整有效时，未返回槽在原固定计划执行得分中
无正确贡献，但**不是已观测答错**。主表同时列full N4、correct_known、RETURNED/INVALID/FAILED/
NOT_RUN、未观测数；六配对说明原both_wrong单元包含未执行者，不将其解释为三道真实共同错误。
另报P2一个已执行个案的四臂结果，注明“条件性个案，不能取代N4/扩大独立样本”。
gold未验证、缺退出或score绑定失败时准确率/配对UNKNOWN，不能据已有预测补答案。

C=D只在实际SigLIP/selector跑过后判断；全同则NO_REALIZED_SELECTION_CHANGE，不调参找差异。
同帧同prompt/tensor却不同回答记实现/可复现性问题，不能说顺序约束获益。
一个P2个案的正负均不建立稳定效应/统计显著/来源独立/泛化/创新。
最高EXPLORATORY_DEV_CASE；NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、
Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。

## 6. 公共执行allowlist（仅六处）

1. prototypes/development_pilot_030.py：固定033、新预算/032 archive/帧交接、零网络与only-P2队列、
   两短窗resource receipt/execute/score绑定与实际收尾；Win32/Job算法保留。
2. prototypes/development_worker_030.py：033固定run/resource/queue/only-P2≤4次绑定、
   权重前一次free核验，其他模型/selector/processor/prompt不改。
3. prototypes/test_development_cached_gpu_033.py：本轮新组合见证。
4. docs/codex-artifacts/VLM-DEV-CACHED-GPU-PILOT-033/cached-gpu-and-score-receipt.md。
5. docs/codex-artifacts/VLM-DEV-CACHED-GPU-PILOT-033/scientific-results.md。
6. docs/codex-results.md：末尾一个033父结果。

不改development_media_030.py/旧tests/旧报告/README、AGENTS/board/overview、025–029基础模块/
科学协议或历史results；原032资源门失败与partial证据保留。公开无私人默认路径/受限helper全文。
公共只匿名终态/聚合/取整proxy，不上传UID/来源映射/题事件选项gold预测原文、私有路径/URI/hash/
原始XML/PID名单/精确PTS选帧索引/向量/凭据/媒体权重。一次安全push后STOP，不自动034。

## 7. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview及
> VLM-DEV-CACHED-GPU-PILOT-033 README和引用资料，确认唯一未交付READY033，连续完成A–H。
> 我在已确认有效研究许可及SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE开发口径下，
> 明确授权033一次只读032确切缓存：文本≤40MiB、P2帧缓存≤1open/256MiB；
> 新integration_033≤128文件/512MiB。不重开032、不沿用余额、不重跑旧tests。
> 本轮网络/下载、MP4/partial正文、demux/decode均0；只复制并完整核验已合格P2的48帧。
> 原N4/20选项/16槽及轮转保持，仅P2四槽可各新回答一次（即使历史答过），其余12槽NOT_RUN。
> 我明确接受033共享GPU资源政策：不要求零C+G上下文/全局独占；最多两次短窗query、
> 各free≥20GiB且GPU利用率≤20%才启动，worker加载前再核对free一次，不杀peer或循环等待。
> 允许唯一GPU worker/generate≤4，GPU累计≤900s/peak allocated≤18GiB/Job RAM≤24GiB；
> CPU≤600s/父≤2400s，新suite≤2×60s，首PASS同轮实际四臂→独立score→科研报告。
> 原annotation准备正文0、当前父独占handle与两个真实零正文拒绝probe按合同；
> 仅真实Qwen返回、全部模型PID/Job实测退出与完整队列/快照绑定后，
> 独立CPU scorer≤1次/1open/4MiB读取原四题gold，坏gold/半读不重开。
> FAILED/INVALID/NOT_RUN保留全分母，不把未执行当已观测答错，不读旧预测/gold产物、
> 不换题/模型/提示或调阈值，不训练/安装/改环境、ACL、profile和凭据。
> 按六处allowlist提交代码、两匿名报告和results一个033父记录，
> 一次安全push main后STOP，不自动034或追加生成/下载。
