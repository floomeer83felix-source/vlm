# 040：工程故障对照、消融与成本

2026-10-24，Asia/Shanghai。**CPU_FAULT_HARNESS_COMPLETE / NO_DISTINCT_MECHANISM_EVIDENCE。**
结论允许否定原先期待：F达到本轮保护目标，强SQLite参照B1也达到相同目标；
没有足够证据把文件claim组合命名为新事务或新可靠性机制。
只支持这个Windows、受控进程故障和公开SHA工作负载范围的工程观察。

## A：权限、冻结与公平性

独立文档main由干净状态安全快进至`ee24885`；AGENTS、当前board/results/overview、
040合同/协议、指定018/039公开历史收据及必要公开Win32结构已读。
040为唯一未交付READY；144逻辑格信息通道候选暂缓，不访问旧私人交接目录。
历史VLM运行只能证明当时执行史，不与本轮CPU负载拼成同一次比较。

首个临时输出前，目标卷实测空闲**433,251,799,040B**，
要求**2,281,701,376B=128MiB+2GiB**，随后用tempfile.mkdtemp创建恰两个新040根。
无旧锁删除、旧epoch恢复、GPU/模型/真实QA或新数据访问。

三份独立stdlib模块：[runner](../../../prototypes/auditable_runner_040.py)、
[benchmark](../../../prototypes/benchmark_auditable_runner_040.py)、
[关键验证](../../../prototypes/test_auditable_runner_040.py)。运行时不导入030/025/026/038/039。
源码、540行planned队列、参数及策略在正式工作前封存；正式run有排他once标记，
开始后没有源码/阈值/顺序修改、重跑坏例、补抽样或第二套正式结果。

|sealed item|SHA256|
|---|---|
|auditable_runner_040.py|a82810e4a5909aa1978f15ede6222be6616ae0b651a55c4b4431d17be2f48381|
|benchmark_auditable_runner_040.py|b00726681a9e5d6affb6be14e7d9bcad503d54f881b2eb9a486aadbcb0d23e93|
|test_auditable_runner_040.py|98baf70155a568860ef1fe0e9c462ab6820a19f1ec872db81e55d4cd1acdd675|
|planned queue|2af04ad6a6085fb929a86e104125b77fee40fb5223c1a5c320e1e53356193cef|

| 配置 | 执行前持久消费 | 实际payload绑定 | 整组退出评分门 | 持久实现 |
|---|---|---|---|---|
| B0 |无|无|仅直接子进程returncode/timeout|成功缓存、原子结果、manifest/code/config检查|
| B1 |有|有|有|SQLite唯一key、BEGIN IMMEDIATE、FULL/DELETE、独立score唯一键|
| F |有|有|有|排他claim/fsync、按key串联收据与终态、一次评分标记|
| F-NOBIND |同F|仅收集不强制匹配|同F|仅去掉payload准入条件|
| F-NOCONSUME |无|同F|同F|仅去掉前置排他消费，仍保留成功缓存/评分门|
| F-NOEXIT |同F|同F|取消整组退出条件|其余F行为不变，外部清理仍在|

B0没有被故意省略直接returncode检查，因此本轮EARLY_SCORE没有使它误准入；
F的直接子进程非零退出也被拒绝，F-NOEXIT仅移除了F赖以拒绝“尚在运行”的整组退出门。
所有方案收到相同的worker收据字段。结果先检验是否与收据实际payload摘要自洽，
再由bind策略决定是否必须匹配冻结输入。因为工作结果本身就是SHA256原payload，
若偷偷在所有配置中额外比较计划结果摘要，就等价重新装回被消融的输入绑定。
外部oracle始终按原始payload独立检查输入与结果，二者违反分别记录。

工作主体确实执行64次对原payload的SHA256；另有收据用实际输入摘要及源码摘要，
所有配置相同。实验不是模型推理；不能从这些成本推算Qwen延迟或GPU吞吐。

## B/C：真实OS链与新验证

所有工作进程采用CREATE_SUSPENDED→加入本轮Job→ResumeThread，早于Python用户代码。
未设置breakaway许可；登记后代通过OS继承所属Job，观察器核验其确实属于该组。
工作组至多2个worker和1个后代，512MiB committed上限；每格外层5s。
调度进程独立于工作组，每个请求由新OS进程提交，另受自己的Job监督。
后代有独立2s自退出上限；只有本轮归属可证的进程允许清理。

新suite仅一次：**12/12 PASS，0FAIL/ERROR/SKIP**。
其中6个真实OS开发格标为SUITE_SMOKE，未混入正式CSV；其余为公共API/绑定/坏缓存/
不完整claim/固定队列等断言。没有第二次suite或额外开发smoke。

|family|profile|actual work|terminal|injection|violations|group0|
|---|---|---|---|---|---|---|
|N1K|B1|1|RETURNED|NOT_APPLICABLE|-|1|
|DUP_ACTIVE|F|1|RETURNED|DELIVERED|-|1|
|DUP_ACTIVE|F-NOCONSUME|2|VIOLATION|DELIVERED|DUPLICATE_EXECUTION|1|
|CRASH_AFTER_WORK|F|1|UNKNOWN|DELIVERED|-|1|
|DESCENDANT_ALIVE|F-NOEXIT|1|VIOLATION|DELIVERED|PROCESS_STILL_ALIVE|1|
|INPUT_DRIFT|F-NOBIND|1|VIOLATION|DELIVERED|INPUT_BINDING,RESULT_INCORRECT|1|

suite监督窗口3.656s，6格wall合计3.328s；包括1次实际重复执行、真实exit17、
已退父进程且仍活后代、实际末字节变化。suite主进程exit0后，外层曾观测到非零Job
成员计数并请求了一次本轮Job终止，随后实测active0；不能声称整轮完全没有终止请求，
也不能仅凭该计数推断具体仍活进程。该事实不算方案保护能力；正式与clean外层均自然排空。

## D：正式540格完整分母

**计划540、尝试540、可核查闭合540；未运行0、FAILED0、UNSUPPORTED0、未送达0。**
180正常格无故障注入，360故障格均取得实际送达证据。
660次独立调度请求、580次实际工作入口，低于720上限；60个登记后代。
540格均实测工作组active0，最大逐格wall0.779324s≤5s。

终态为RETURNED310、VIOLATION90、REJECTED100、UNKNOWN40。
UNKNOWN是崩溃后不能合法恢复的真实完成损失，不是保护成功或运行故障率样本。
“证据闭合540”指注入、准入及进程观察可审；不把40个UNKNOWN变成已知成功结果。
每家族10重复只反映这一机器调度变化，不是独立系统或真实故障发生率。

|profile|N|violation cells|bad admissions|duplicate cells|extra work|normal legal|safe-fault legal|UNKNOWN|consumed unrecoverable|consumed zero work|
|---|---|---|---|---|---|---|---|---|---|---|
|B0|90|40|40|20|20|30/30|10/30|0|0|0|
|B1|90|0|0|0|0|30/30|30/30|10|10|0|
|F|90|0|0|0|0|30/30|30/30|10|10|0|
|F-NOBIND|90|10|10|0|0|30/30|30/30|10|10|0|
|F-NOCONSUME|90|20|20|20|20|30/30|20/30|0|0|0|
|F-NOEXIT|90|20|20|0|0|30/30|10/30|10|10|0|

正常30格与可安全完成故障30格（DUP_ACTIVE/EARLY_SCORE/DESCENDANT_ALIVE）分别保留分母。
B0的可安全故障仅10/30合法、F-NOCONSUME20/30、F-NOEXIT10/30；
B1/F/F-NOBIND各30/30。不能用“总拒绝率高”充当有效性。

|profile|family|N|V cells|V times|Dup|L|U|REJECTED|delivered|outer fallback|
|---|---|---|---|---|---|---|---|---|---|---|
|B0|N1K|10|0|0|0|10|0|0|0|0|
|B0|N64K|10|0|0|0|10|0|0|0|0|
|B0|N1M|10|0|0|0|10|0|0|0|0|
|B0|INPUT_DRIFT|10|10|10|0|0|0|0|10|0|
|B0|DUP_ACTIVE|10|10|10|10|0|0|0|10|0|
|B0|CRASH_AFTER_WORK|10|10|10|10|0|0|0|10|0|
|B0|RECEIPT_MISMATCH|10|0|0|0|0|0|10|10|0|
|B0|EARLY_SCORE|10|0|0|0|10|0|0|10|0|
|B0|DESCENDANT_ALIVE|10|10|10|0|0|0|0|10|10|
|B1|N1K|10|0|0|0|10|0|0|0|0|
|B1|N64K|10|0|0|0|10|0|0|0|0|
|B1|N1M|10|0|0|0|10|0|0|0|0|
|B1|INPUT_DRIFT|10|0|0|0|0|0|10|10|0|
|B1|DUP_ACTIVE|10|0|0|0|10|0|0|10|0|
|B1|CRASH_AFTER_WORK|10|0|0|0|0|10|0|10|0|
|B1|RECEIPT_MISMATCH|10|0|0|0|0|0|10|10|0|
|B1|EARLY_SCORE|10|0|0|0|10|0|0|10|0|
|B1|DESCENDANT_ALIVE|10|0|0|0|10|0|0|10|0|
|F|N1K|10|0|0|0|10|0|0|0|0|
|F|N64K|10|0|0|0|10|0|0|0|0|
|F|N1M|10|0|0|0|10|0|0|0|0|
|F|INPUT_DRIFT|10|0|0|0|0|0|10|10|0|
|F|DUP_ACTIVE|10|0|0|0|10|0|0|10|0|
|F|CRASH_AFTER_WORK|10|0|0|0|0|10|0|10|0|
|F|RECEIPT_MISMATCH|10|0|0|0|0|0|10|10|0|
|F|EARLY_SCORE|10|0|0|0|10|0|0|10|0|
|F|DESCENDANT_ALIVE|10|0|0|0|10|0|0|10|0|
|F-NOBIND|N1K|10|0|0|0|10|0|0|0|0|
|F-NOBIND|N64K|10|0|0|0|10|0|0|0|0|
|F-NOBIND|N1M|10|0|0|0|10|0|0|0|0|
|F-NOBIND|INPUT_DRIFT|10|10|10|0|0|0|0|10|0|
|F-NOBIND|DUP_ACTIVE|10|0|0|0|10|0|0|10|0|
|F-NOBIND|CRASH_AFTER_WORK|10|0|0|0|0|10|0|10|0|
|F-NOBIND|RECEIPT_MISMATCH|10|0|0|0|0|0|10|10|0|
|F-NOBIND|EARLY_SCORE|10|0|0|0|10|0|0|10|0|
|F-NOBIND|DESCENDANT_ALIVE|10|0|0|0|10|0|0|10|0|
|F-NOCONSUME|N1K|10|0|0|0|10|0|0|0|0|
|F-NOCONSUME|N64K|10|0|0|0|10|0|0|0|0|
|F-NOCONSUME|N1M|10|0|0|0|10|0|0|0|0|
|F-NOCONSUME|INPUT_DRIFT|10|0|0|0|0|0|10|10|0|
|F-NOCONSUME|DUP_ACTIVE|10|10|10|10|0|0|0|10|0|
|F-NOCONSUME|CRASH_AFTER_WORK|10|10|10|10|0|0|0|10|0|
|F-NOCONSUME|RECEIPT_MISMATCH|10|0|0|0|0|0|10|10|0|
|F-NOCONSUME|EARLY_SCORE|10|0|0|0|10|0|0|10|0|
|F-NOCONSUME|DESCENDANT_ALIVE|10|0|0|0|10|0|0|10|0|
|F-NOEXIT|N1K|10|0|0|0|10|0|0|0|0|
|F-NOEXIT|N64K|10|0|0|0|10|0|0|0|0|
|F-NOEXIT|N1M|10|0|0|0|10|0|0|0|0|
|F-NOEXIT|INPUT_DRIFT|10|0|0|0|0|0|10|10|0|
|F-NOEXIT|DUP_ACTIVE|10|0|0|0|10|0|0|10|0|
|F-NOEXIT|CRASH_AFTER_WORK|10|0|0|0|0|10|0|10|0|
|F-NOEXIT|RECEIPT_MISMATCH|10|0|0|0|0|0|10|10|0|
|F-NOEXIT|EARLY_SCORE|10|10|10|0|0|0|0|10|0|
|F-NOEXIT|DESCENDANT_ALIVE|10|10|10|0|0|0|0|10|10|

表中V为违反准入的格数/次数（本轮每格至多一次），Dup为额外实际工作次数，
L为合法完成，U为UNKNOWN终态；每行仍N=10。其余为明确REJECTED，不隐藏未送达或未运行。

## 真实注入与独立oracle

observer独立生成SHAKE原始payload/期望SHA；不调用F validator作为真值。
每worker独立写入口、完成oracle文件，准入逻辑不读取这些oracle文件。
早评分的OS状态在决策前取样，决策完成之后才释放barrier；后代还用真实进程句柄/Job成员关系核验。

|family|representative|actual evidence (full hashes/data in CSV)|delivery|outcome|
|---|---|---|---|---|
|INPUT_DRIFT|F/0|planned a2cf71def916; mutated/actual 87a18c68b37c; final PAYLOAD_MISMATCH|DELIVERED|REJECTED|
|DUP_ACTIVE|F/0|entry before second independent request=True; request2=CONSUMED|DELIVERED|RETURNED|
|CRASH_AFTER_WORK|F/0|actual exit17, completed=True, first receipt absent=True; recovery=CONSUMED|DELIVERED|UNKNOWN|
|RECEIPT_MISMATCH|B0/0|code a82810e4a590 -> 082810e4a590; numerical result unchanged; RECEIPT_CODE|DELIVERED|REJECTED|
|EARLY_SCORE|F-NOEXIT/0|direct alive before/after decision=True; admitted=True; group_active=2|DELIVERED|VIOLATION|
|DESCENDANT_ALIVE|B0/0|parent exit0, registered descendant own Job/alive=True; admitted=True; group_active=2|DELIVERED|VIOLATION|

完整[540行CSV](./benchmark-rows.csv)保留计划/实际请求、入口/完成、终态、注入、
每次评分请求/准入及独立OS快照、违规类别、退出/fallback、wall/CPU/commit/bytes及错误。
公开CSV在导出时仅从本轮已有oracle/收据补入无PID的原始绑定证据和独立复算结果；
没有改变原始正式测量、方案决策或再执行工作。可由公开seed和这些字段重算汇总。

崩溃家族全部60格都先完成了工作、缺少第一调用的正常收据且实际exit17。
B1/F/F-NOBIND/F-NOEXIT各10格已消费不可恢复、终态UNKNOWN；
B0/F-NOCONSUME各10格恢复后实际重复工作，后续准入违反不能冲销第一次不确定性。
“已消费但0次实际工作”的观测为0；本故障集未专门注入consume与dispatch之间断电/崩溃。
不宣称crash-safe exactly-once、断电安全或恶意worker可信执行。

## E：正常成本与组件归因

每种大小/配置n=10。逐格端到端包括输入准备/摘要、存储消费、OS启动、工作、等待、
方案持久化和最终准入；最终独立case-summary/CSV写出另属共享观察器。
共享oracle/平台层仍在case wall中，没有声称精确扣除了它的真实开销。
Job CPU是工作组user+kernel；调度CPU单列，不能把wall当CPU，也不能与包含它们的外层Job CPU相加。

|payload|profile|n|wall min s|wall median s|wall max s|empirical p95 s|work Job CPU median s|work peak commit max B|case bytes median|
|---|---|---|---|---|---|---|---|---|---|
|N1K|B0|10|0.330858|0.355160|0.389183|0.389183|0.117188|13639680|2222|
|N1K|B1|10|0.355532|0.379177|0.451329|0.451329|0.101562|13570048|2222|
|N1K|F|10|0.345713|0.381258|0.405968|0.405968|0.109375|13615104|2222|
|N1K|F-NOBIND|10|0.350906|0.373691|0.441997|0.441997|0.093750|13664256|2221|
|N1K|F-NOCONSUME|10|0.330647|0.361471|0.386967|0.386967|0.101562|13582336|2221|
|N1K|F-NOEXIT|10|0.335430|0.373470|0.387163|0.387163|0.093750|13680640|2222|
|N64K|B0|10|0.344883|0.360197|0.414827|0.414827|0.093750|13766656|66735|
|N64K|B1|10|0.372393|0.389410|0.436836|0.436836|0.117188|13725696|66735|
|N64K|F|10|0.355802|0.375474|0.447540|0.447540|0.093750|13680640|66736|
|N64K|F-NOBIND|10|0.344889|0.365269|0.410124|0.410124|0.109375|13676544|66735|
|N64K|F-NOCONSUME|10|0.341949|0.374386|0.402222|0.402222|0.117188|13688832|66736|
|N64K|F-NOEXIT|10|0.346584|0.387579|0.441343|0.441343|0.109375|13651968|66736|
|N1M|B0|10|0.377329|0.396064|0.415737|0.415737|0.140625|14704640|1049771|
|N1M|B1|10|0.396631|0.411017|0.433935|0.433935|0.132812|14671872|1049771|
|N1M|F|10|0.378652|0.410891|0.454992|0.454992|0.140625|14778368|1049770|
|N1M|F-NOBIND|10|0.383383|0.401887|0.475010|0.475010|0.132812|14696448|1049770|
|N1M|F-NOCONSUME|10|0.377596|0.401637|0.451349|0.451349|0.125000|14700544|1049771|
|N1M|F-NOEXIT|10|0.388065|0.407857|0.451630|0.451630|0.140625|14721024|1049771|

|payload|pair|n|diff min s|diff median s|diff max s|ratio min|ratio median|ratio max|
|---|---|---|---|---|---|---|---|---|
|N1K|F/B0|10|-0.042453|0.024375|0.052141|0.890917|1.071005|1.153008|
|N1K|F/B1|10|-0.079100|0.005121|0.029699|0.824740|1.013485|1.081769|
|N64K|F/B0|10|-0.024917|0.008835|0.091293|0.938028|1.025454|1.256264|
|N64K|F/B1|10|-0.039093|-0.013773|0.043520|0.910509|0.963456|1.107718|
|N1M|F/B0|10|-0.002139|0.014313|0.060633|0.994822|1.036921|1.160690|
|N1M|F/B1|10|-0.030747|-0.001318|0.048524|0.924897|0.996761|1.120131|

经验p95按nearest-rank：n=10时取第10个，即max；不足以估计生产尾延迟。
F/B1配对wall比值中位数分别约1.0135、0.9635、0.9968，三种大小方向并不一致，
每种差值范围均跨0。没有据此证实清晰、跨大小可重复的成本优势，也没有制造p值。
单独的payload绑定摘要成本不能由这些配置差唯一分解：所有worker都已产生共同实际摘要。

|profile|separate backend initialization seconds|
|---|---|
|B0|0.000147500|
|B1|0.020597800|
|F|0.000243200|
|F-NOBIND|0.000215300|
|F-NOCONSUME|0.000183400|
|F-NOEXIT|0.000266700|

|profile|persistent backend files after90 cells|backend logical bytes|
|---|---|---|
|B0|160|35540|
|B1|61|79758|
|F|300|189616|
|F-NOBIND|320|194335|
|F-NOCONSUME|230|188182|
|F-NOEXIT|300|177739|

CSV的output_bytes是逐case目录中最终summary写出前的逻辑文件字节，**不含共享后端**。
因此另列各profile实际后端总量与两根总量，不将该列当作完整磁盘开销排名。
SQLite共享页空间/短命journal的逐key分配与写放大量未测；表中不是NTFS物理分配字节。

消融的实际归因：去绑定在INPUT_DRIFT产生10格违规；去消费在DUP/CRASH各产生10次额外执行；
去整组退出在EARLY/DESC各产生10格违规。RECEIPT_MISMATCH所有配置均拒绝，
证明B0也有公共代码/manifest检查，不是无校验的稻草人。F优于B0仅说明这些已知组件在本合同中有用。

## F/H：复现、资源与结案

干净目录只复制三个已封存.py，-I -S -B并清除PYTHONPATH；实际3个help、1个F正常demo、
6配置×N1K/CRASH共12格复现，均保留结果。不是独立机器/研究者复现。
细节、命令与先例裁决见[复现及先例报告](./reproducibility-and-prior-art.md)。

|phase|outer supervised wall s|exit|active|Job user CPU s|Job kernel CPU s|outer peak commit B|outer termination requested|
|---|---|---|---|---|---|---|---|
|suite-1|3.656000|0|0|1.046875|1.156250|44675072|True|
|formal|241.219000|0|0|66.953125|93.328125|45867008|False|
|clean|7.250000|0|0|1.937500|2.500000|44064768|False|

Actual outer supervised wall total **252.125000s** /1500s. Reservations120+900+120s plus120s initialization margin =1260s. Smoke is inside the suite window, not added twice. Formal work-group user/kernel totals **30.640625/40.515625s**; scheduler CPU total **67.812500s**. Inclusive outer Job CPU is not summed with those child subtotals. OS total_processes fields are raw Job accounting/assignment counters, not unique worker counts.

两个新根最终总量7275文件/70,137,270B，无reparse；实际数量在报告阶段再次核对。
完整报告导出后的父时钟测点为1803.213s，距5400s上限仍有3596.787s；
该数含同步、实现、等待和执行，不把241s正式窗口冒充整个父任务时长。
初始化及报告控制脚本未逐PID计CPU；已报告的Job CPU仅对应实际受监督phase。
新suite/正式/clean均实测退出并无活动成员；正常/正式没有用外包络替B1/F作评分决定。
B0/F-NOEXIT各10个后代格需要外部生命周期收尾，已标fallback；正式工作组没有强杀。
覆盖缺口包括断电/磁盘损坏、真实外部副作用、专门SQLITE_BUSY/IO故障和正向成功缓存复用的完整工作流。
SQLite OperationalError在当前实现中保守统一报BUSY而不算成功，诊断不够细；正式未触发该分支。
本轮没有按这些缺口追加故障或修改已封存实现。

**G裁决：NO_DISTINCT_MECHANISM_EVIDENCE。** B1与F同为0违规、0重复，正常30/30及
安全可完成故障30/30，且都暴露10个崩溃后UNKNOWN。文件方案没有独立的新可靠性保证。
本轮留下可复核故障合同、负结果和三文件复现入口，可作为工程稿材料；
没有完成真实推理接入、现成工具公平实测或跨机验证，不能据此许诺核心期刊录用。
停止继续堆框架包装创新；任何后续方向由负责人另行决定，不自动041。

GPU/模型/Torch/Transformers/NumPy/processor、训练、真实QA/gold/原标注、旧帧/
旧预测/private helper、实验网络/下载/媒体解码/安装/永久系统修改均0。
仅七处allowlist交付和一个040父追加，一次普通安全push main后STOP。
