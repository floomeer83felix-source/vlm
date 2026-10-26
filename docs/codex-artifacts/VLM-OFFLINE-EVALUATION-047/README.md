# 047已归档：固定夹具软件验收通过

2026-10-26：[负责人验收](../../research-decisions/post-047-offline-evaluation-disposition-2026-10-26.md)已关闭047。
**ACCEPTED_OFFLINE_SOFTWARE_IN_FIXED_SCOPE / REAL_DATA_SCORER_NOT_QUALIFIED；当前0 READY。**
60个suite例与5个CLI核查均通过；负责人独立重建256格、25份输入封存及10个输出摘要一致。
实现/CLI限本轮数学夹具，真实标签/视频/模型/GPU均未运行；通用输入类型加固与真实scorer资格未认证。
本父已消费，不重跑、不自动048或继续增加夹具/框架补丁，不继承旧额度。
以下执行合同保留历史，其中READY/启动消息已失效。

# 047：离线区间评测与结果核算整包

2026-10-25（北京时间）。**CLOSED / ACCEPTED_OFFLINE_SOFTWARE_IN_FIXED_SCOPE / NOT_RERUNNABLE。**
父任务：VLM-OFFLINE-EVALUATION-047，当前唯一READY。用户在046关闭后要求“一直继续下去”，
据此下达常规标准库CPU实现，不需要再次确认本范围；不包含新下载、媒体、真实标签/预测、模型或GPU。

本包一次交付：可导入的评分/聚合/核算库、命令行入口、必要验证器、完整固定用例证据和一条父回报。
它实现[既有设计](../../research-protocols/natural-video-clock-feasibility-design-2026-10-24.md)尚未落地的评测层；
不是新算法、自然视频实验或已具备投稿贡献。046与旧任务全部保持关闭。

## 1. 冻结依据与边界

[contract-fixtures.json](./contract-fixtures.json)原始UTF-8/LF SHA256：
`5485d7c097b74d78a002c4822c874386a6427faf5567e73c925216abba562063`。
其中24个parser例、7个IoU例、4个完整64格软件夹具、强制故障类别和共享成本例全部为本轮自造数学数据，
统一标明SYNTHETIC_SOFTWARE_CONTRACT_NOT_RESEARCH_DATA。绝不是视频/模型/人工标注观测，不累加研究样本量。

时间IoU仅使用已有交集/并集公式。参考ActivityNet固定
[Evaluation/utils.py](https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/utils.py)
Git blobb73fd335d3f97ec40b5e66dd81004bd5ca2f7192，只读公式，不运行该Python2/NumPy/联网文件、不安装或复制整套评测器。
本包不是ActivityNet官方评测等价实现。Python标准库[json说明](https://docs.python.org/3/library/json.html)中的
object_pairs_hook/parse_constant可用于拒绝重复键/非标准常量；不用新版本专有API或更换本机Python。

现有停止条件仍约束真实入口；本次独立工作不获取/修复下载、不访问旧文件、不扩受控时钟/缓存变体。
[负责人方向说明](../../research-decisions/post-046-offline-evaluation-direction-2026-10-25.md)明确它只能关闭计算软件缺口，
不能代替素材、标注桥接、题目语义或模型实证。

## 2. 范围和资源

- 仅现有标准库Python，单计算线程、Job RAM≤512MiB，不导入NumPy/PyAV/Torch/Transformers/模型工具。
- 新私有根为独立文档checkout同级`vlm-private-047`，存在即STOP；父链/新根无reparse/symlink。
  不扫描旧根、盘符、下载目录、私人日志/QA/gold/预测/runtime。起步空闲≥16MiB+2GiB。
- suite最多初轮一次≤60秒；仅有确切错误定位时允许一次修复回归≤60秒，保留失败；无第三轮。
  核心CLI完整示例和拒绝路径合计受监督≤60秒，全部CPU子阶段累计≤180秒，父从首次本地执行起≤3600秒。
- 只可借用040公开Job/Process平台blob3e56faf30afea1bed850c085bceb2afcc4fb257c作外层监督；
  不运行040或其它历史工作/tests。监督截止仅在父自己时钟内判断，不把父绝对perf_counter数值传给另一解释器相减。
  不派计时修复/网络故障矩阵；无法证明自有进程退出则停止，不处理其它任务/锁。
- 新根≤16MiB/512文件。单输入≤4MiB、最多5个明确输入文件；单模型式回答字符串UTF-8≤8192B；
  每题有效区间≤128，rational整数位长≤4096bit。超限明确拒绝，不截取有利部分。
- 应用网络/HTTP、媒体读取/解码、真实标注/QA/旧预测、processor配置/权重、模型/forward/generate/GPU、
  安装/环境改变/新人工答案均0。进程内拒绝网络和无关路径；标准库/新模块/本轮新根/明确公共合同为精确只读范围。
  本轮fixture构造不是模型模拟实验，也不声称安全hook是对抗性隔离证明。

按AGENTS安全同步main并重读AGENTS/看板/results/总览/本README/fixture，核唯一READY和本父无既报。
公共来源允许GitHub文档同步，不允许执行时向参考项目的blocklist/API、媒体或其它数据发请求。
首次实现前明确接口/schema和numeric policy，做本轮源码/fixture/配置封存；实现失败只保留未知，不换研究条件。

## 3. 必须实现的计算合同

### A. 分离的输入及严格答案解析

核心以显式参数接收plan、gold registry、logical-class map、physical records及cost records。
CLI只可读取本轮新根中本轮生成且标明synthetic_fixture=true的数学夹具，逐个精确路径和文件hash登记；
库为以后独立scorer复用保留接口，047不接触真实文件。禁任意目录递归发现或回退读旧预测。

plan固定8源：S01–S06=HIGH_OFFSET，S07–S08=CFR；每源Q01/Q02，B0/P/N/T，共64个唯一(source,query,arm)。
每源T=240秒仅为软件fixture；真实来源的180–900秒等准入条件不由此认证。
source/query使用复合键，Q01可在不同source内出现；重复/缺失/额外ID、改层数/题数/臂/分母应REJECTED_PLAN，
保留expected_logical_cells=64及错误，不输出缩小分母的分数。8个ID不证明物理来源独立。

raw response必须是唯一JSON对象，恰start/end两个JSON数字，类型bool/字符串/null/嵌套、重复键、
NaN/Infinity/数值溢出、数组、围栏/解释、多个对象、尾逗号均INVALID；只容忍合法JSON空白。
JSON整数/小数统一转有限IEEE754 binary64（包括parse时溢出检查），再以as_integer_ratio作精确有理数运算；
gold/T用明确有界rational字符串，不先round。要求0≤start<end≤T，不裁剪、不交换、不从文本截取。
字段顺序不同不改变结果。实际保留raw UTF-8字节hash及错误类型，不输出虚构的模型答案。

plan/registry/class map/record输入分别封存，评价时核输入字节hash；不在评价中自动改写封存以接受变动。
gold独立入口不进入模型式prompt或等价类key；本模块没有模型阶段，不能因此认证未来完整流程不会泄漏标签。

### B. 有效答案集合、未知与失败优先级

每个(source,query) registry至少含T、clock_bridge_status、question_identity_status、
answer_set_status及非空valid_intervals，每个区间在0≤s<e≤T内。
registry的T及clock_id必须与plan的同源声明相符，不通过拟合偏移或修改T救场。
同版时钟映射必须声明VERIFIED、题目声明IDENTIFIABLE_EXISTING、集合声明COMPLETE_DECLARED，缺失/未知/不合法即
SCORING_UNKNOWN，保留原因和空分值；不能删掉坏区间后继续评分或把未知填0。
这些字段只是外部资格声明的校验，不能仅凭格式/叙述ID/动作字符串自动证明题目可识别或答案集合完整。
当前数学fixture可由构造赋值；真实世界的资格仍需新证据，047不补标签/人工答案。

固定集合上的单一预测得max_k IoU(prediction,interval_k)，不是把断开区间拼成union或包围盒。
集合/资格必须在模型结果之前固定；不得按每个预测换gold。区间顺序重排结果不变，匹配并列时用固定序号/排序规则作诊断，
不以匹配ID改变主分。报告这是本项目明确的多有效区间政策，不冒称标准数据集官方任务合同。

先判断gold/clock/question资格；若未知，即使返回INVALID/FAILED/TIMEOUT/NOT_RUN也不能偷填主分0。
资格有效时RETURNED且解析合法才算IoU；INVALID、FAILED、TIMEOUT、NOT_RUN（含缺失计划结果）主分0且保留原状态。
FAILED携带合法JSON也不能转成功。SCORING_UNKNOWN和运行状态分列，未知不是模型错误或自然科研阴性。

### C. 固定分母、来源配对与触发值

每臂16逻辑题完整保留，每源两题先平均；主比较只在6个HIGH_OFFSET源等权求P−B0、N−B0。
CFR两源单独，另列全部8源/16题/64格状态及覆盖率，不能把64格/patch/重复输入当64个独立样本。
R@0.5按精确IoU≥1/2；P/B0、N/B0纠正/误伤/均正确/均错误按题配对，并另报未知配对数。
端点误差只作合法响应的辅助量并明确覆盖率，不替代失败保留的主指标。

主量所需任一题SCORING_UNKNOWN则该主汇总为SCORING_UNKNOWN/JSON null，
可另列known_subset_descriptive及覆盖率，但不能用其替代主结论或悄悄缩分母。
所有64格可计分时，另给预设数值条件：high-source mean(P−B0)≥1/10且至少4/6源为正；
未知不得判false/失败。这个字段必须叫practical_numeric_condition，仅为描述性计算，
不能自动给科学GO、GPU/扩样/投稿许可，也不证明真实素材/执行完整性等外层门成立。
不报独立显著性/p值或置信泛化结论。软件夹具中的true/false不是研究发现。

### D. 逻辑格与声明物理记录映射

等价类仅接受外层已封存的“实际输入+模型/生成/上下文”复合fingerprint；047不计算视觉tensor、
不以arm/source/map/code身份制造DIFF或推定相等。fixture用带fixture前缀材料的SHA256作声明key，
必须标记DECLARED_FIXTURE_IDENTITY_NOT_REAL_MODEL_INPUT。

同一类的多个逻辑格只引用一个physical record，传播该记录的同一响应/失败，不额外生成。
physical_id对应不同类、同一类有多个物理尝试、重复/冲突记录一律REJECTED_RESULT_MAP，
不能择优取一条；缺少结果在计划中保留NOT_RUN。坏映射不产出貌似合法分数/数值触发。
报告planned logical64、declared classes、recorded physical attempts及各状态，不把声明记录数当实测generate次数；
本轮实际模型调用始终0。G01声明48类/48记录，G02为64，均不改变8个声明source单位或当前真实观测0。

### E. 共享成本、包含式时段和时钟域

cost_id唯一，logical格/臂可以多次引用同一shared_prepare cost_id，但只记一个事件一次；
重复cost事件ID或冲突元数据使cost结果UNKNOWN，不择优。
支持parent_cost_id与inclusive时段：唯一run_envelope outer wall和phase子项分别报告，
不把outer再加到phase，也不把嵌套letterbox加进已包含它的shared_prepare。
无计量/不完整记录是COST_UNKNOWN，不填0；评分本身可独立有效。

每个start/end都含明确clock_domain和有界数值；只有同域、顺序正确才求duration。
父子跨域不相减/拟合offset，不由自报domain字符串声称物理时钟已同步。
兄弟phase有重叠、缺失覆盖或跨域时，不把其和标为端到端latency；可单列各自duration与已知outer。
fixture C01：outer10，prepare2/generate6/score2，内含letterbox1/2；共享prepare被4格引用仍只收2。
10+1/2或outer10+phase10都不得当总延迟。将046那类不同数值原点声明为不同域的数学负例只核拒绝运算，
不进行调度器/下载器修复，不声称再现了046的Windows现场。

## 4. 一轮实现与验证

新增`prototypes/offline_evaluation_047.py`和`prototypes/test_offline_evaluation_047.py`。
核心可独立导入，另有参数明确的CLI；stdlib，不导入历史工作负载。
按固定fixture生成规则构造全部4个64格文件；它们是软件验收输入，不能呈现为研究结果图或模型答题。
第一次suite覆盖JSON表、IoU表、四完整网格、全部mandatory_faults、共享计费和包含式/混时钟拒绝。
reference路径不得调用被测parse/IoU/aggregate函数计算expected；用独立Fraction公式/闭式期望及不变量，
至少核顺序不变性、重复alias不增物理数/来源数、失败/未知优先级、不缩分母。
以两条函数表达同一段代码不算独立oracle。

四网格主期望已事前固定：
- G01全1；P−B0=0、正源0、数值条件false；声明输入类48。
- G02 B0=2/3、P=5/6、N=1、T=0；P−B0=1/6，N−B0=1/3，正源4、数值条件true；
  高层P/B0的12题R@0.5均正确，纠正/误伤均0；不可将IoU改善与阈值纠正混称。
- G03只把G02的S01/Q01/P改成INVALID，64格仍可计分，P−B0=1/12、正源3、条件false。
- G04只将G02的S01/Q01 bridge改UNKNOWN，未知4格、可计分60；主量和条件UNKNOWN，不作0或部分均值替代。

suite通过后，额外从CLI读取已封存fixture跑四网格及一个坏映射拒绝示例，
用独立post-exit读取器核JSON/CSV的固定分母/数值/null/状态与封存摘要，禁止只测内存函数。
输出目录不存在才写，不覆盖原结果。必要的一次定位修复/回归预算与全部失败保留；CLI失败不重跑择优。
某独立模块阻塞仍按合同完成可做的安全模块并统一报告PARTIAL，不擅改schema/门槛救PASS。

## 5. 交付与停止

执行者只允许新增五个文件并追加一次results（总六处变更）：
- `prototypes/offline_evaluation_047.py`
- `prototypes/test_offline_evaluation_047.py`
- 本目录`offline-evaluation-receipt.md`
- 本目录`contract-case-results.csv`：所有预登记例/故障类及初轮/回归状态完整保留，明确数学fixture；不预填PASS
- 本目录`fixture-grid-summaries.json`：四网格、CLI封存/校验摘要、成本例及未知/拒绝状态；每项synthetic=true
- `docs/codex-results.md`：仅末尾一条047父结果

回执写实际实现/CLI命令/封存、全部失败及修复依据、真实assertion/用例数、各监督wall/Job CPU/峰RAM/active0、
根配额和未实现部分。不得把assertion数、64格fixture、声明physical record数当自然/模型样本；
当前媒体/真实标签/真实预测/processor/model/GPU0，NOVELTY=RETAIN0。
不改README/fixture/规划/旧代码或旧证据，不上传私有路径/资料。核stage仅六处，普通push main一次后STOP。
completed/partial/blocked任一回报消费047，不自动048、后台轮转、GPU/下载或投稿。

用户在当前本地Codex聊天发送一次即可启动：

> 安全同步GitHub文档仓库main，重读AGENTS、任务板、结果和VLM-OFFLINE-EVALUATION-047的README/contract-fixtures.json，执行唯一尚未交付的READY父任务047。按合同一次完成标准库离线评分、固定分母/来源配对、声明等价类与共享成本核算、必要tests和CLI证据，统一脱敏推送后停止。仅本轮自造数学夹具；网络、媒体、真实标签/旧预测、processor、模型/GPU、安装均0，不重跑旧任务。
