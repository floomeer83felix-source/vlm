# VLM-DEV-REFERENCE-AND-STARTUP-036：有界恢复标注引用，独立推进合成启动与真实四臂

2026-10-22（北京时间）。ChatGPT研究负责人；Windows本地Codex执行。
**唯一READY父任务036 / PUBLIC_REFERENCE_AND_STARTUP_ONLY，尚未执行。**
第8节用户实际发送的一条完整消息激活新私人metadata/字节核验/CPU启动/GPU/gold范围。
035已关闭，不恢复其run/锁/时钟、旧suite或余额，不改旧报告。既有研究许可与开发口径保持。
本轮明确增加“可信CPU一次字节哈希”例外；不能以旧035的准备正文0许可自动执行此操作。

## 0. 035验收及下一步为什么分为独立分支

035交付[2615512](https://github.com/floomeer83felix-source/vlm/commit/2615512fce25b4c87be6d610f4a14408505e76f2)
按 **ACCEPTED_CLOSED_HANDOFF_AND_FRAME_COPY / CURRENT_ANNOTATION_REFERENCE_HOLD /
REAL_STARTUP_NOT_RUN** 结案。新suite首且仅一次5/5 PASS，含合成/静态见证。
prepare实际在原annotation checked_path/lstat报FileNotFoundError/WinError2，exit1/Job0；
当前原文件handle、probe、真实bootstrap/ML import、query/GPU/gold均0。
另一个独立frame分支完成223,948,928B/完整SHA/48RGB/NPY验证。
这是精确路径查询失败，不证明文件被删、已移动、ACL失败或其他位置不存在。
034原SETUP PermissionError仍UNKNOWN，035没有复现它。

036同轮完成两个独立工作：
一是仅在明确很小的metadata范围内核对当前原标注引用，并对唯一候选做一次label-blind字节核验；
二是即使原标注尚未找到，也用**全合成问题/选项/画面**实际运行依赖/CPU processor启动，
取得PermissionError细节并修可修问题。合成成功绝不能冒充真实数据/QA/原文件隔离通过。
只有真实标注引用恢复、当前原文件OS锁/probes与其他条件都通过，才进入P2真实四臂/score。
若仍缺确切标注位置，完成独立启动分支后明确请求用户在本地Codex提供完整路径，
**不自动再安排同类路径搜索、不生成GPU结果，也不下载替代标注。**

沿用[030科学协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)：
DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。
原N4/20选项/16槽和ABCD/BCDA/CDAB/DABC、only-P2原BCDA四槽保持；
48→12、C/D共享q/a/b与双锚点/目标/tie/补齐、i≠j对i<j、模型/提示/像素/seed/greedy不改。
P3 participant缺失只披露，不追旧registry/换题/扩大媒体。

## 1. A–H一包连续交付

| 项 | 工作与判据 |
|---|---|
| A / 新只读交接 | 安全同步独立docs main，重读AGENTS/board/results/overview、本合同、035两报告、035恢复合同与030科学协议。确认唯一未交付036。公共实现后新建已知018根/integration_036，固定contract/run/036.lock/ledger、3000s父时钟；只读第5节确切035文件。 |
| B / 定点实现与新suite | pilot/worker增加035缺引用archive、nongold配置与当前引用分开、合成startup role、label-blind SHA绑定和修复receipt/code/policy验证；先测本轮变化，≤3次新suite各≤60s，按变更使用。原035五项不重跑。 |
| C / 独立真实合成启动 | 从已核nongold缓存只提取既有模型/processor/helper/runtime配置；构造全合成question/event/options和零像素frames。自有canary handle下最多3个实际CPU bootstrap，各≤60s，共用生产policy/startup；精确诊断、定点修复并复验。模型权重/CUDA/encoder/generate/真实gold0。无需原annotation存在即可做本项。 |
| D / 有界原引用恢复 | 只按第2节精确旧路径/至多2小目录metadata/可选用户已明确给的唯一新路径核对；最多唯一候选1open/4MiB纯字节SHA，禁止decode/JSON parse/gold字段或body日志。与原028完整size/SHA一致才更新本036当前reference，保留旧记录和科学快照。 |
| E / 条件真实四臂 | C通过且D建立真实绑定后，当前真实annotation父独占handle与2零正文probe通过；一次新设备/free门后按原P2四槽执行。最多2串行GPU worker共用900s绝对包络，第二个仅首退出Job0/全run STARTED=0/证据驱动修复经新suite与必要合成bootstrap复验后允许。 |
| F / 独立score | 全16终态、全部模型Job/PID真实退出、run/plan/queue/resource/各launch-exit/当前引用及原raw快照一致后封闭队列、释放真实handle；有RETURNED/INVALID才独立CPU score≤1open/4MiB，guard先消费、失败不重开。 |
| G / 双分支科研报告 | 分别报告reference定位/字节核验/当前OS锁、合成imports/processor/修复、真实模型/selector/QA/score。原N4和未执行者保留，合成输入不计样本/正确率。没有真实选择/回答则UNKNOWN/NOT_MEASURED。 |
| H / 一次push STOP | 六处allowlist统一交付、results唯一036父追加，普通安全push后STOP。缺路径时必须给出需用户提供的具体输入项（在本地交付，不公开路径/JSON），无自动037或新搜索/GPU预算。 |

## 2. 标注引用核对与明确新增的字节哈希例外

### 2.1 先metadata，不猜文件

- 从已认证035 annotation-reference和prepare-exit-private读取旧路径与具体失败component，
  当前再次作有限lstat/stat，区分旧字符串/父目录/盘符是否可用；metadata探测合计≤32个确切path，
  无body读。不能用公开报告的WinError2推断已删除或直接构造新数据路径。
- 如果当前本地Codex会话中用户已经**明确给出新的原标注完整路径**，只核对该一个额外候选；
  视频路径/某个下载文件夹不算原标注路径，不能从过往无关媒体名猜annotation文件。
- 否则只可各一次非递归scandir：
  旧路径parent，以及其直接parent（合计≤2目录/每目录最多64个entry）；
  目录必须是旧引用直接导出的普通无reparse目录；盘符根、用户home、不可访问/reparse目录跳过，
  不换第三个目录、不列驱动器/全盘/兄弟子目录、不递归。
  先按entry名称过滤；仅同旧basename（Windows大小写归一）的entry才可stat，计入上述32个确切path上限。
  只保留名称匹配且size等于原raw size的候选metadata；
  不保留/上传其他文件名。超过64项标TRUNCATED，不能声称查尽或选一个当唯一。
- 多个路径如指向同一实际FileID可去重。原路径本身或用户明确提供的唯一路径优先作确切核对；
  搜索来源候选只有在允许范围完整、唯一且无歧义时才能进入一次SHA验证。
  没候选/多义/截断/超界则D HOLD，不多hash、不改basename/扩展名找近似文件。
  本轮目录统计与当前路径事实留私人；公开只匿名状态/计数。

### 2.2 只可信CPU一次raw字节核验，不解码答案

这是对旧“准备原annotation正文0”的**唯一明确新例外**：
至多1个候选、1个rb open、实际读取≤4MiB，可信stdlib-only CPU child≤20s；
只按原三份028完整raw receipt的准确size分块hashlib.sha256.update(bytes)。
**禁止decode、JSON parser/projector、gold字段提取、repr/body日志、缓存原文件或传给ML进程。**
先消费ANNOTATION_HASH_CONSUMED与字节预算；半读/打不开/变化/mismatch同样消费，不重开或换候选。

要求当前file size等于原size且≤4MiB，checked_path/no reparse，path/fd同一对象，
前后stat/fstat自比较稳定，完整计数和SHA与原028三份完整receipt及frozen-snapshot-032一致。
不修改、重新序列化/修复JSON、不接受“语义相同”或新版本；摘要不符D HOLD。
这个trusted child不import ML、不联网，只输出count/size/SHA与稳定性/当前identity/private path，
不输出raw bytes或labels；没有正确性反馈可用于选择候选。
依据：[hashlib字节update](https://docs.python.org/3/library/hashlib.html)；
[os文件metadata/scandir](https://docs.python.org/3/library/os.html#os.scandir)。

只有完全一致才能写本036 ANNOTATION_REFERENCE_BOUND：
新path/当前device+FileID/size/mtime、原size/SHA/profile与证据hash均绑定，保存旧reference副本；
允许同内容文件在移动/复制后FileID/mtime不同，不能再硬等旧028物理FileID。
历史三receipt和frozen-snapshot保持原值，新binding明确连接旧内容摘要与当前物理对象，
不是改历史或把新文件当新科学样本。
正常prepare/score应分别验证“历史receipt原绑定”和“当前物理对象经SHA绑定”，
不能把二者身份相等继续写成不可恢复条件，也不能删掉所有身份检查。

可信SHA结束后关闭其读handle。后续真实父另一次非继承exclusive share handle正文0，
在实际CPU/P2模型阶段持有；2真实probe各native/Python open正文0/native32/Python拒绝，
当前handle/metadata必须对应新binding，变化即HOLD。
**模型/合成bootstrap从不读取原标注正文；最终gold仍只在全部真实模型退出后另1open/4MiB。**
本轮最多两次数据正文open：可信SHA一次＋最终gold一次，分别记账/隔离。
SHA不是gold解码或科学评分，不能据此填正确率，也不声称全机所有gold副本不可达。

## 3. 无原标注依赖的全合成startup分支

035的真实bootstrap被缺文件挡住，本轮C明确允许在真实reference尚未恢复时独立执行：
- 提取已绑定的原模型root/config、runtime、system/helper语义，制作
  role=SYNTHETIC_STARTUP_ONLY的单独bootstrap config，真实worker配置/FROZEN不可覆盖。
  问句/事件/五选项全部用固定虚构内容，48帧为新建零像素/虚构像素，times/duration/fps为固定合成值。
  可用已验证NPY shape metadata生成同shape，但不读P2 RGB作合成画面、不夹真实题目/答案。
  合成数组只在内存，不另写大NPY；fake控制内容不当新科研标注或样本。
- 父持有**自有虚构canary**的非继承exclusive handle，bootstrap child作零正文拒绝见证，
  随后按同一生产install_policy/startup imports/CPU processors/helper执行。
  此处canary仅合成控制；绝不签ORIGINAL_LOCK、ANNOTATION_REFERENCE_BOUND、
  REAL_BOOTSTRAP、RESOURCE_ADMITTED或MODEL_LAUNCH。
  合成PASS也不能让D失败时进入真实GPU。
- 最多3个实际CPU bootstrap、每个完整≤60s/Job RAM≤24GiB；
  首个成功不无因重复，失败后按诊断修复才用剩余次数；第三次可以用于零QA GPU恢复后的startup复验。
  NumPy/Torch/Transformers/VideoMetadata实际imports、AutoProcessor/tokenizer/config与CPU helper/grid实测，
  但不调用SigLIP/Qwen模型from_pretrained/encoder/generate，不创建CUDA tensor或初始化CUDA。
  可读torch.cuda.is_initialized状态；CPU helper输入全部CPU、实际12帧/grid[6,12,18]/324 tokens。
- 继续细stage、最多16拒绝事件/8KiB内存、最多32无locals/源码行的frame摘要，
  callback不IO/resolve/log、拒绝仍raise；每诊断≤64KiB、原路径/stack只私人留存。
  有匹配denial才归因audit，无该记录不凭PermissionError猜audit/ACL/CUDA。
  035没有实际复现、034缺trace的事实保留，不用036日志倒填旧原因。
- 修复仍限自有child import前必要HF_HOME/HF_HUB_CACHE、TORCH_HOME/TEMP等路由新root、
  已安装runtime的≤4确切只读支持文件、经明确模块源码证明的局部参数/返回类型兼容。
  不开放整home/其他研究目录，不移除/移后audit，不改ACL/永久环境/driver、不安装/下载，
  不开放模型child网络或任意子进程，不改科学model/prompt/selector/像素/dtype/greedy。
  合成配置的虚构字段不是改变真实科学worker；真实配置仍逐字段等于frozen-worker-032。

即使D失败也完成C允许的诊断/修复，不再因缺original handle使纯合成imports全部0。
C无法修复时给准确阶段/拒绝类别/缺的具体输入；不能把source字符串断言当真实CPU兼容PASS。

## 4. 修复035未实际运行分支的代码绑定，再条件真实运行

静态复核发现035的REPAIR_ACCEPTED仅检查当前code_hash与CONTINUE，
SUITE_RESULT没有绑定测试时code_hash，也未要求新suite发生在repair request之后。
另一个接入点是GPU修复后policy变量未从accepted response更新；
若exact-read policy版本改变，第二worker可能仍用旧版本。
这些是未运行路径的静态发现，**不是035已发生的违规或034 PermissionError成因**。

036须定点修复：
- SUITE_RESULT及新suite完整receipt记录生产代码/新suite/参数配置hash；
  每REPAIR_REQUEST落账明确seq、request/diagnostic/current science/policy/code摘要。
  CONTINUE只在该request之后有实际完整PASS、测试code等于当前code时接受；
  绑定具体suite receipt/hash/seq，不接受旧PASS、仅手写tested=true或旧response重放。
- startup-policy固定最多1..3个不可覆盖版本，accepted repair明确下一policy_id/hash，
  父据此更新后续bootstrap/worker参数；worker/launch/score均验证相符policy和测试代码。
  第一成功后不更改，后续startup代码/policy改动必须用剩余实际合成bootstrap验证，
  同时使用剩余new suite；未验证不能靠换mode继续。
- current annotation成功后，实际prepare重新核当前binding/stat，保持真实worker science hash/16槽；
  真实父ORIGINAL_LOCK＋2probe、C的本轮code/policy实测PASS共同过门才允许query/GPU。
  合成receipt role和真实source/queue/input hash独立验证，不用其虚构题/图像构造真实回答。
- 沿用显存有界共享政策：一次本036 nvidia-smi query≤10s，正确device0/3090/UUID/bus、
  free≥20GiB；util/context只记录，不以≤20%否决。每真实worker权重前free复核各≤1，
  allocator18GiB在load前设置、Job RAM24GiB和peak allocated18GiB保持，OOM不重启/不kill peer。
- 最多2串行真实GPU worker，共用唯一900s绝对包络，从首launch到末attempt结束，
  中间修复/测试/合成复验间隔也计入。正常仅1个；第二个仅首所有Job/PID已真实退出、
  全run STARTED=0、P2尚无terminal/queue未关闭、有技术证据并完成最新测试/必要bootstrap时允许。
  任何STARTED后禁止重启/重答，OOM/timeout/想找更好结果不能作为恢复理由。
  原P2 BCDA每槽≤1、generate合计≤4；attempt文件独立、不覆盖，不退款/重置/追加900s。
- 保留同一父coordinator的有界修复握手/真实handle/run/deadline，
  不先退出/换root或epoch再称恢复。所有launch/exit逐条绑定actual private receipt/attempt/
  run/queue/resource/policy/code；全部模型PID/Job0后最后一次完整QUEUE_CLOSED。
  独立score前的ChildExitReceipt包含全部模型PID，不只最后attempt；
  guard先消费，一次≤4MiB/四题gold/full raw SHA及新current identity一致才发布。
  D或C失败、无真实Qwen返回则gold0，所有16槽按原映射NOT_RUN/FAILED/INVALID保留。

## 5. 035 archive与输入白名单

本036只读integration_035，不回扫034/033、不实例化旧Journal/锁或改旧epoch。
035确实在prepare前段失败，**没有worker-input.json/runtime.json/queue.json/
expected-snapshot.json等新prepare输出**；不能向不存在的035文件取handoff或要求PREPARED/FROZEN。
真实worker/model配置从已认证frozen-worker-032与execution-config.runtime恢复，原snapshot由frozen-snapshot-032提供。

handoff≤20份，各≤1MiB（035-ledger.jsonl可≤2MiB），每份1外部open：
八个keys/cohort/nongold/plan/receipts/targets/heads029/official JSON；
035-ledger.jsonl、annotation-reference.json、execution-config.json、device-identity-reference.json；
P2-head.json、P2-media-binding.json、P2-candidates.json；
frozen-worker-032.json、frozen-snapshot-032.json；
035-final-summary-private.json、prepare-exit-private.json、startup-policy-1.json。
035原frame-source-reference指向旧034只用于历史，不据此重开034；本轮frame只取035实际副本。

专用035只读archive验证全hash链/seq/prev/newline/REAL_035/root/run/STOP；
首且仅一5-case PASS、完整frame input/OUTPUT/FRAME_CACHE_VERIFIED SHA与48RGB，
prepare exit1/Job0及其FileNotFound stderr、copy exit0/Job0、16唯一NOT_RUN/NO_MODEL_QUEUE_CLOSED。
BOOTSTRAP/GPU_QUERY/GPU_ENVELOPE/RESOURCE_ADMITTED/MODEL_LAUNCH/STARTED/SCORE_CONSUMED/
gold/网络/媒体获取均0。保留035当前reference未认证事实，不能按034已launch archive规则误拒绝。

八nongold/四factory_0/1.py、runner_0/1.py及有input摘要的metadata直接匹配035 INPUT_COMPLETE size/SHA；
frozen-worker-032/frozen-snapshot-032与原plan/三完整028 receipt一致，生成JSON用OUTPUT/相关事实核验，
不虚构历史SHA或改旧物理身份。只有第2节新SHA绑定可以连接当前文件新identity。
新frame唯一大输入035/P2-frames.npy≤1open/256MiB，准确223,948,928B/全SHA匹配035链；
完整copy/fsync/stat+fd稳定、48 RGB/uint8/NPY/times验证，不改像素/新解码。

source≤8份各≤1MiB：4缓存helper/runner＋至多4个真实诊断明确指向的已安装runtime确切模块/支持文件；
config≤4份各≤1MiB：2原model config＋至多2个诊断明确指向的非凭据runtime配置。
正常现有runtime/processor/模型local-only加载限原获准目录，不环境盘点或复制/下载权重。
旧预测/gold产物/其他source登记/原manifest0open。

## 6. 本轮新测试与资源

新test_development_reference_startup_036.py，最多3×60s，显式expected/loaded/run与FAIL/ERROR/SKIP、
测试时code/policy/config摘要；0发现/skip不算PASS。只按首实现/实际修复使用剩余次数，
不import或重跑035五项/旧套件，不重复旧OS演示。
有意义fixture组合须覆盖：
有限目录cap/超界/同名多义/旧path失效、唯一候选hash一致可重绑新FileID，
SHA不符/半读/字节预算不退款、无decode/gold opener；
无真实reference时合成startup仍可运行、合成role不能触发GPU/score；
035缺prepare输出archive正常handoff/篡改与伪model拒绝；
旧suite/code或request顺序/旧policy/replayed CONTINUE不放行，
新policy确实传给下一bootstrap/worker、两个attempt all-exit/零QA恢复/score-opener0。
fixture用虚构文件/字节/frames，不读真实annotation/联网/ML；
真实合成CPU bootstrap才证明本机imports/processor兼容。

| 资源 | 本036新上限 |
|---|---|
| 文本研究输入 | ≤48MiB；20handoff含ledger2MiB（其余1MiB）、source≤8×1MiB、config≤4×1MiB、annotation integrity≤1open/4MiB、最后gold≤1open/4MiB；角色最坏41MiB≤48 |
| frame | 仅035/P2-frames.npy≤1外部open/256MiB，独立计账 |
| 路径metadata | 精确path stat≤32；非递归目录≤2/各≤64 entries；当前会话用户明确给的新原标注路径≤1。无全盘/递归/第三目录 |
| 新私有输出 | 仅integration_036≤128文件/512MiB；frame≤256MiB，其余含cache/canary/trace/fixture/ledger≤32MiB；精确预约＋2GiB余量，同名存在STOP |
| CPU/父 | CPU累计≤900s、父≤3000s；合成bootstrap≤3×60s、reference metadata≤20s、trusted raw hash≤20s、copy≤90s、prepare≤60s、query≤10s、score≤60s，cleanup/嵌套PID计入 |
| 新suite | ≤3×60s；虚构PID≤4各≤3s（可为0），计CPU；无第四suite/旧测试 |
| GPU | 最多2串行worker共用900s绝对包络，only-P2≤4generate/原槽各≤1、18GiB peak allocated/24GiB Job RAM；第二个仅零QA技术恢复条件满足时 |
| 查询 | 一次新nvidia-smi；每worker权重前free复核各≤1，无后台/等待低util/kill peer |
| 原annotation | 仅trusted hash准备时≤1open/4MiB原始bytes；模型/合成bootstrap0B。实际父另1次非继承exclusive handle、2真实probe各≤5s/各native+Python open≤1且正文0 |
| 最后gold | 真Qwen返回/INVALID＋全部模型退出/完整绑定后独立CPU≤1次/1open/4MiB，仅原四题gold；guard消费、失败不重开；否则0 |

CPU预扣建议45初始化＋180suite＋12虚构PID＋90copy＋60prepare＋180合成bootstrap
＋20metadata＋20raw hash＋20可选准确conda解析＋10真实probe＋10query＋60score＋30收尾
=737s≤900。分开报告预扣/实测wall、synthetic role/真实CUDA与QA、integrity/gold/body bytes，
不把上限当测得消耗或将wall当逐PID CPU/kernel时间。
固定Qwen3-VL-4B BF16/SigLIP F32/SDPA/local-only/seed19/greedy64；
训练/backward/optimizer/LoRA/新人工标签/云GPU/付费API/安装/永久环境/ACL/profile/凭据修改0。

科学报告保留025 full-N4执行口径与各终态/未观测者；NOT_RUN不是已观测答错，
six-pair both_wrong若包含未执行者明确披露。P2仅条件个案、不能替换N4/算独立泛化。
真实selector前C=D/anchors/coverage/retrieval/token/EOS均NOT_MEASURED；
真实C=D全同写NO_REALIZED_SELECTION_CHANGE，不调科学阈值/提示找差异。
合成CPU成功不是Qwen/机制成绩；最高EXPLORATORY_DEV_CASE，
NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP、TRAIN-GPU HOLD。

## 7. 公共allowlist（仅六处）

1. prototypes/development_pilot_030.py：固定036/035 archive、nongold/reference分开、
   有界metadata＋一次raw SHA/current binding、独立合成startup监督、
   修复后的tested-code/policy握手与真实GPU/all-exit/score保护。
2. prototypes/development_worker_030.py：合成role/config/frames与实际startup共享、
   有界diagnostics、证据驱动局部修复及正确policy/attempt/code关联；
   科学worker/模型/selector/prompt不改。
3. prototypes/test_development_reference_startup_036.py：本轮新组合见证。
4. docs/codex-artifacts/VLM-DEV-REFERENCE-AND-STARTUP-036/reference-startup-and-real-run-receipt.md。
5. docs/codex-artifacts/VLM-DEV-REFERENCE-AND-STARTUP-036/scientific-results.md。
6. docs/codex-results.md：末尾一个036父追加。

旧tests/报告/README/AGENTS/board/overview/025–029基础模块/科学协议/历史results不改。
细path/目录名/trace/UID/映射/题事件选项gold预测原文/精确PTS选帧/向量/hash/credentials/
原始XML/权重/媒体不公开，公共仅匿名类别/阶段/计数/取整proxy。
路径仍缺时只明确请求用户给当前原标注完整路径，勿索取JSON内容；
本包一次普通安全push STOP、不自动037或增加搜索/下载/生成。

## 8. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview、
> VLM-DEV-REFERENCE-AND-STARTUP-036 README及引用资料，确认唯一未交付READY036，连续完成A–H。
> 我在已确认研究许可及SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE开发口径下，
> 明确授权036只读035确切缓存与合同限定runtime诊断：文本≤48MiB、
> P2帧≤1open/256MiB；新integration_036≤128文件/512MiB，不恢复035或沿用余额。
> 允许精确path stat≤32、旧标注parent及其直接parent最多2个普通目录非递归metadata枚举、
> 每目录≤64 entries；若当前本地会话已有我明确给的新原标注完整路径，可核对该唯一额外path。
> 不递归/全盘/第三目录；只唯一无歧义候选可由可信CPU1open/≤4MiB做纯字节SHA，
> 禁止decode/JSON parse/gold提取/body日志。完整size/SHA匹配原028快照才重绑本036当前identity，
> 原receipt/科学输入不改；hash失败/半读不换候选重开。
> 允许不依赖原标注的全合成CPU startup≤3×60s，在自有canary锁和同一生产policy下，
> 用虚构题/选项/零像素frames实际imports/CPU processors/helper，模型权重/CUDA/模型前向0；
> 精确定位并做合同限定cache/runtime/API修复。合成PASS不能冒充真实OS锁/QA或放行GPU。
> 真实原标注绑定恢复后才准父独占handle及2实际零正文probe、真实P2四臂与独立score；
> 原N4/20选项/16槽保持，only-P2原四槽各新答≤1（即使历史答过），generate总≤4。
> 沿用显存有界共享政策，一次当前query核正确设备/free≥20GiB，util仅记录；
> 最多2串行GPU worker共用900s绝对包络/18GiB allocated/24GiB Job RAM，
> 第二个仅全run STARTED=0、首Job实测退出、证据驱动修复经最新suite/必要合成复验后允许。
> 任一QA开始后禁止重启/重答，OOM/timeout不重启，不kill peer或重query。
> CPU≤900s/父≤3000s、新suite≤3×60s，修复必须绑定request之后的当前code/policy真实PASS。
> 模型/合成startup原标注正文0；最后仅真Qwen返回、全部model Job/PID退出和队列/raw/current绑定后，
> 独立CPU scorer≤1次/1open/4MiB读原四题gold，失败/半读不重开；无真实返回gold0。
> 网络/下载/MP4和partial正文/新解码/训练/安装/改永久环境、ACL、profile或凭据0。
> 即使缺当前原标注也完成独立合成启动分支；仍缺时报告需我在本地提供完整路径，不再扩大搜索。
> 按六处allowlist交付代码、两匿名报告和results一个036父记录，
> 一次安全push main后STOP，不自动037或追加搜索/下载/生成。
