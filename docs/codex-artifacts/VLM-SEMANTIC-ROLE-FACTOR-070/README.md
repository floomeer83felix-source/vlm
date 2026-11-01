> **归档：070已完整交付并验收关闭，不再READY。** [82d6db9](https://github.com/floomeer83felix-source/vlm/commit/82d6db9775ce7d3b3778d08b37c58ef7ff855692)6000更新/33552有效项，FACTOR均值27.67%/23.33%但未过原全对照门，STOP_THIS_RECIPE。[验收](../../research-decisions/post-070-review-and-selector-intervention-2026-11-01.md)10220公开检查/16区间独立复现。下一唯一READY为[071冻结选择器干预](../VLM-FROZEN-SELECTOR-INTERVENTION-071/README.md)，不训练/调参，不把锚对照升级新方法；069继续暂停。以下原合同逐字保留，原READY/额度不再生效。

# 070 交换不变分量选片、角色差分读出的受控CPU实验

2026-11-01（北京时间）｜ChatGPT研究负责人。**READY，唯一尚未交付父任务；BOUNDED_CPU_MECHANISM_PILOT。** 用户已要求继续机制探索、暂停论文。[方向与边界](../../research-decisions/post-068-exploration-priority-and-semantic-role-pilot-2026-11-01.md)。本地收到含本ID及本合同CPU范围的用户新启动指令后，一包完成实现、24配置实际训练、预测/封存评分/独立核验并统一push；不拆准备父任务，不继续069或写论文，不自动071。

## 1 同步与只读资产

安全同步独立文档main，读AGENTS、最新看板/总览页首、本合同、方向决策、068验收和063/062/056公开实现。确认070是唯一尚未交付READY，results无本ID；069为PAUSED_BY_USER，不消费它或补完成记录。如069已在本地进行，先停止新增写作、正常关闭自身文档Job并保留草稿；不得丢弃Git改动或杀其他进程。文档checkout不干净/不能快进即停止报告。

仅由既有handoff/明确登记定位063、068及其062/060来源链，不递归扫私有目录。父闭合/push、实际Job active0、代码/输入/feature/outputs/seals必须核齐，不倒填历史缺口。允许只读：

- 063保留的原六`plan-<seed>.pt`，其中实际`state`与250×8 `sequence`，**不得新生成初始化或计划替代**；原062 C/D normalizer，060/062/063原feature-index和所需缓存V[6,2560]/h[2560]。
- 原四split无标签observations，固定train68标签；评分专用旧val11/dev54/source50标签和文件family绑定。注册/训练角色不解析评估答案或旧预测。
- 068原100V/100h的feature-index/seal/特征、同50无标签observations及评分专用已封存labels/outputs、prediction-seal和闭合记录；**不读其ZIP/视频/RGB/processor cache、主模型权重或配置**。
- 评分角色最后才投影063已封存`new-outputs.json`中的六seed C_NATIVE/D_NATIVE共8784条、068原输出2400条；其他旧臂不重新分析，B0不读。基线总11184条，所有条件必须原样复现063/068公开聚合，不重跑旧头。

VIDHALLUC标签优先核068派生labels的原闭合seal。若派生labels没有独立历史seal，评分角色最后可按**068原catalog已登记**的066 `dy.body`原内容身份及原selected_positions重建同50标签，并逐项核对068派生labels；不是读新版本或重选名单，不倒填历史seal。只允许该精确登记的旧publisher元数据，计64MiB旧metadata/预测/标签总读量；原来源身份/positions缺失即停止，训练/预测角色不得读取它。

原划分N68/11/54/50/50、原事件/问题/tau/label绑定与六seed137/263/419/557/733/911不变。V/h合并只取这些精确成员，最多466V/320h，缺失/歧义或相同键身份冲突即停，不补编码。两个50集合均已用分数，本轮不是盲测/独立原始来源。

## 2 固定文本分量与训练统计

tau逐字沿用062严格模板，当前问题派生其角色交换文本；无改写、另问LLM或依赖另一格预测。float64定义：

```text
c_raw(q) = (h(q)+h(tau(q)))/2
r_raw(q) = (h(q)-h(tau(q)))/2
```

R(q)精确使用旧062 D_ROLE的train84 mu/标量RMS变换，先核其旧seal/值/有限性，不重新拟合D。仅新c_raw在**原84个去重训练问题**上拟合mu_c与标量RMS_c，算法和062相同；S(q)=float32((c_raw(q)-mu_c)/RMS_c)，要求scale>1e-8/有限，不加epsilon/白化/单位化/数据选择。R转float32的顺序也与旧D一致。所有split只应用这些固定统计，评估不参与拟合。c是交换不变分量，尚未证明是纯语义；不假定经旧中心化的R严格变号，更不强制logit互补。

ANCHOR固定训练事件对：将每个q与tau(q)的UTF-8字节较小者作为canonical，原84问题得到42个canonical文本，按UTF-8排序。事件名按062规则（下划线改空格、折叠空格、casefold）生成无序事件对。对当前canonical q，用`SHA256(b'VLM070/c-anchor/'+canonical_q.encode('utf-8'))`前8字节大端整数mod42作起点，循环选择第一个**规范化无序事件对不同**的训练canonical a(q)；无合法锚即停止。q/tau共享锚，只用已有h与S(a)，不生成新文本。锚可能与问题共享一个事件，准确称“不同事件对训练锚”，不宣称完全无关语义。规则/映射在训练前固定，不读答案/分数。

## 3 同参数路由，精确四新臂

视频支路逐字复用056 TemporalHead：r64、video Linear2560→64，原固定sin/cos位置编码、无仿射LN(eps1e-5)、Conv1d64→64核3/padding1、默认exact GELU，得到H_t。输出仍原MLP256→64→1（含原bias/GELU），无新损失/位置/卷积/二阶乘积/温度。

保留原`question.weight[64,2560]`和`question.bias[64]`两个参数张量，以前32行为A/b_A、后32行为B/b_B：

```text
a = GELU(A S(q)+b_A)             # 32维
b = GELU(B R(q)+b_B)             # 32维
a_anchor = GELU(A S(a(q))+b_A)   # 只在ANCHOR，用它替代a，不计算未用a
dup(x) = concat(x,x)             # 固定重复，无新增参数/缩放
```

| 新臂 | 时间权重向量g_select | 最终读出向量g_read |
|---|---|---|
| CONCAT | concat(a,b) | concat(a,b) |
| FACTOR（候选） | dup(a) | dup(b) |
| REVERSE（职责反向对照） | dup(b) | dup(a) |
| ANCHOR（不同事件对语义对照） | dup(a_anchor) | dup(b) |

```text
alpha_t = softmax_t(dot(H_t,g_select)/8)
u = sum_t alpha_t H_t
o = sum_t alpha_t xi_t H_t, xi=linspace(-1,1,6)
z = old_MLP(concat(u,o,g_read,u* g_read))
prediction = int(z>0)             # z==0为No；非有限值是失败
```

CONCAT是**参数匹配的32+32分块投影拼接**，不是5120→64无约束全连接；该限制必须在结果解释中保留。后三臂相同固定重复/分支宽度，REVERSE和ANCHOR控制这种架构约束及事件对信息本身。所有参数参与真实计算，不加未用参数凑数。

四新头每个参数总数仍356673：video163904＋question163904＋conv12352＋MLP16513；参数键/形状完全兼容原056/063初始state，无新随机映射。相同seed四头从原063 plan的同一完整state克隆、原sequence逐项相同。C/D只复用原预测，不新训/forward。新四臂均无强制互补/翻转答案/配对修复，推理只当前V、当前q的S/R或其固定训练锚，不查另一个视频/问题的输出、标签、来源或组ID。

## 4 一次真实训练和封存预测

先完成静态schema/参数/整数公式审查，最多8次**纯合成CPU小头forward，0优化**：核四路由/形状/有限输出、所有参数真实使用，及CONCAT在S=R=x时与同state的056头在q=x上的输出相符（容差abs≤1e-6+1e-5*abs(reference)）。不使用真实特征/标签或旧final头作fixture，不检查本来不存在的logit奇对称。仅用于软件正确性，不算科研效果。

全部科学/依赖、私有supervisor/budget/ledger和独立核验代码、矩阵/锚规则/判据/新预算在首次070研究tensor/标签读取前封存；所需无标签来源登记可先定位，禁止为读分数设计公式。准备后再封实际输入/新统计/映射/计划，首配置STARTED前核所有代码和输入身份。研究输入消费后不改科学公式或以不同ID重试；任何错误具体actual/limit/reason/阶段先落盘再停。

按seed顺序137/263/419/557/733/911，每seed CONCAT→FACTOR→REVERSE→ANCHOR，24配置，各250真实CPU backward/optimizer.step，共**6000更新**。同seed原250×8四格采样，每步32cell；各配置8000 cell曝光，共192000。不早停/选checkpoint/调通道/系数/学习率/seed，不按验证/开发/两来源结果选择。float32、4线程、无dropout/新增强；BCE=`mean(softplus(-(2y-1)*z))`，AdamW lr0.001/wd0.01/betas(0.9,0.999)/eps1e-8，clip全参数norm1。每步grad均非None/有限，记录实际初始相同、loss/参数变化/更新数，只有末步checkpoint。这些执行事实不当作收益。

训练角色仅train68标签/训练特征与计划，评估答案/旧预测/来源组0。所有新final头按当前单V/q评估五split，24×(68+11+54+50+50)×4=**22368新cell**；封存新输出、checkpoint、code/input/view/anchor/normalizer及每cell STARTED/CLOSED账本。训练/预测Job实际active0且exit0、输入/输出完整键集与seal都通过后，评分角色才读旧预测11184和评估标签。合计**33552正式cell，180条件**＝六方法(C_CACHED/D_CACHED/四新臂)×六seed×五split。基线不是新推理；无B0/N/HASH新增分析。

条件表逐行保留原计划分母、new/cached/CLOSED/INVALID/FAILED/NOT_RUN/execution_unknown/scoring_unknown、单项/视频对/问题对/四格、不敏感、K0..K4/五响应模式和百分比。软件错误不伪造二值或删题，不完整条件相关指标NA、不判门。所有负/零结果/失效均保留。

## 5 固定配对、统计与停止门

仅两已用50集合做主比较。每seed FACTOR分别对C_CACHED、D_CACHED、CONCAT、REVERSE、ANCHOR，共60配对行（6×5×2）；列split/seed/left/right/N50/evaluated/独对/对方独对/都对/都错/unknown、四格净例数/pp及不敏感差。dev54/val11/train68全部条件完整报告，不新增子层/交互/p值或按子层选配方。

**仅完整时，两份50集合各自同时满足以下全部要求，才保留PILOT_SIGNAL：**

- FACTOR对D_CACHED、CONCAT分别至少5/6正差，平均净增各≥3/50（6pp）。
- FACTOR对REVERSE、ANCHOR分别至少4/6正差，平均净增各≥1.5/50（3pp）。
- FACTOR自身六seed平均四格正确数≥10/50（20%）。

用整数比较：对D/CONCAT六seed净值之和各≥18，对REVERSE/ANCHOR各≥9，FACTOR六seed正确数之和≥60；正差计数以net>0判，不能对舍入后的百分比判门。

均通过记`SEMANTIC_ROLE_FACTOR_PILOT_SIGNAL / SELECTIVITY_AND_NOVELTY_UNCONFIRMED`。完整但任一失败记`NO_SUPPORT_FOR_THIS_FACTORED_ROUTING / STOP_THIS_RECIPE`，不挑某对照或较好seed改名贡献、不修改门/补seed。未完整为`INCOMPLETE / SCIENTIFIC_UNKNOWN`，失败/未知不充零分。新门是看过旧C/D后、070新输出前设的投入门，不是显著性/发表要求，不改063原20%失败。

固定16个95%均值区间只针对**四格答题差**：FACTOR对D_CACHED/CONCAT/REVERSE/ANCHOR×两池×两轴；C只作上下文配对，不算C区间；不敏感只作描述，无响应区间。无其他检验。公开聚合直方图支持重算，不公开逐成员正确性/排序：

- 50Salads：沿原25个文件family（每family两实例），每簇合计六seed差，取值−12..12，25箱；每对照箱频数和25，加权和等于六seed总净值。
- VIDHALLUC：原50文件视频对单位，每单位合计六seed差，−6..6，13箱，频数和50。
- 四对照×(25+13)=**152箱**，每行split/right/seed_sum/count/status。各直方图按值从小到大规范展开各自边际，不保持跨对照/指标真实成员对齐，不能做联合bootstrap/差分中的差分。family是文件簇，不认证原录制/参与者独立。

按split固定顺序source_holdout50→item_transfer50，对每池重置`random.Random(55070)`一次，10000次`choices(range(G),k=G)`，G=25/50；该池四对照共享规范索引，用各自向量得`100*sample_sum/(6*50)`。seed轴每池重置`Random(55071)`一次，10000次`choices(range(6),k=6)`，固定seed顺序，对每对照以所抽六seed净值之和除300再乘100。两轴点估计均六seed总净/300×100；2.5/97.5%线性分位position=(10000−1)p。文件/簇轴固定六头，seed轴固定同50条目，不是联合泛化认证。阻断仍交180/60/16/152计划行，未观测指标/频数NA，draws0/planned_draws10000，不能以0掩盖未执行。

## 6 CPU预算、核验与一次交付

既有conda/pytorch，`CUDA_VISIBLE_DEVICES=''`，torch CPU可用且各Job前后CUDA未初始化。CPU训练/预测/评分监督外层累计≤1800秒；其他准备/软件检查/独立核验累计≤900秒；父≤10800秒；线程≤4，Job RAM≤8GiB/active≤4。新独占根≤512MiB/2048文件、起始free≥1GiB；新checkpoint/初始计划≤64MiB，每seed仅保留一份共享initial/plan，四臂记录相同身份，不复制24份initial。缓存feature/views全部实际逻辑读取（含核验/hash）≤512MiB，旧初始化/计划/normalizer≤128MiB，旧metadata/预测/标签≤64MiB，分项实际计量；未知物理I/O不伪精确。只读既有精确资产，不复制整个旧根，不清旧锁/账本，不杀他人进程。GPU/nvidia-smi/Qwen权重/encoder/processor/媒体/下载/研究网络/环境改变/论文内容全0。

配置/步骤/cell持久STARTED与deadline先行，失败不恢复已STARTED配置，预算不重置；只关闭自身Job并核实际active0。资料/shape/统计/参数/identity/budget不合先持久化reason_code、actual/limit、已完成/剩余及阶段，再STOP，所有计划分母和失败保留。旧资产前后身份不变，旧C/D所有180表中其60条件原样复现063/068公开数值；未证实项写UNKNOWN，不为通过门改输入/对照。

独立核验代码不得import被测scorer或重新forward/优化，torch只用于只读张量/state核对：原六初始化/采样与四头共享、train84统计/锚/角色隔离、24末state和6000实际步骤/grad/loss/192000曝光、22368新＋11184旧/33552键、五split标签与基线精确一致、180条件/60配对/152箱/16区间和各门，代码/input/output/seal链及资源/Job闭合。输出和标签重建统计，bootstrap独立实现，不能调用生产scorer冒充独立复算；角色隔离不等于OS访问审计。

精确九处allowlist，其他旧文件/论文/规划/本README不改：

1. `prototypes/semantic_role_factor_070.py`（显式入口，导入无研究I/O/forward/训练）
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（180行）
5. `paired-summary.csv`（60行）
6. `mean-intervals.csv`（16行）
7. `difference-histogram.csv`（152行）
8. `execution-summary.json`（矩阵/实际消耗/静态检查/源code LF SHA、五split/两主比较池范围、锚/数据证据层、独立核验/失败/预算/未知；不公开资产hash）
9. `docs/codex-results.md`仅尾增一次本父记录

不得公开原QA/答案/逐题logit预测或正确性、真实成员/源映射/私有路径/资产hash、特征/媒体/权重；仅聚合频数/统计与科学代码自身hash。暂存核精确allowlist与results前缀，普通安全push main后STOP，无后台/自动071/重问旧模型。

即使通过，本轮仍未建立三事件选择性、严格事件定位/因果机制或算法原创性。至少三事件、同视频不同目标对、相关/无关顺序干预的数据和媒体/模型预算尚未建立，不在本包生成；六tubelet不冒充六事件。先用本轮强对照筛选是否值得投入那项决定性验证。未通过就关闭本具体机制，069继续暂停，不能擅自回到论文或另一新头。
