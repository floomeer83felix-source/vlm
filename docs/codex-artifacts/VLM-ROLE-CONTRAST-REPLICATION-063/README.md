# 063：固定角色差分的种子复验与完整顺序2×2对照

2026-10-31（北京时间）｜ChatGPT研究负责人。**READY，唯一尚未交付新父任务；CPU_CACHED_TRAINING。**

一轮连续完成输入/完整代码封存、16配置4000真实CPU更新、预测、统一评分和独立核验。依据[062验收及下一步决策](../../research-decisions/post-062-role-signal-and-replication-2026-10-31.md)。不另拆准备轮、不改062配方/阈值或重跑旧模型；本地新启动消息只触发本父包，push后STOP。

## 1. 刷新与精确读取

安全同步独立文档仓库main，完整读AGENTS、本合同和062验收；next-steps/overview读最新页首及063/062段，results全文检索063并读唯一062条目。确认唯一READY为本ID且无既往交付。

仅从当前明确handoff取062及其old-assets登记中的060精确根，闭合登记/Job必须完整；不递归扫描。062只读old-assets、input/output seals、normalizer.pt、views.pt、train-views.pt、transform-bindings、feature-index、四split observations、train-labels、scoring-bindings、`plan-19.pt`/`plan-73.pt`、scoring-summary/全部输出及必要账本/闭合文件。060仅依062索引读取实际复用V/q和四split评分标签/原绑定以核身份；旧最终权重、主模型权重、ZIP/视频/RGB不读。旧19/73 C/D和B0只投影预测缓存，不载旧最终模型或重forward。

核062固定133＋50、68/11/54/50及25/4/20/25组、366V/220q、84去重train问题及原标签绑定；各split/源组完全不变。062三臂views文件可完整反序列化，但仅使用C_CENTER/D_ROLE，N不训练/预测；只读复核train-only mu/s/锚及原变换值，不重新拟合normalizer/换tau文本或更改尺度。来源50仍为已使用NO_EVENT_SEEN，PUBLISHER_COMPOSITE_QA、物理来源/预训练未知等边界保持。

准备可核原标签/成员身份，训练角色只读train68标签/所需V、固定C/D训练views/初始计划；不读评估标签、来源组、旧预测/正确性。其他旧原预测只在新输出封存后由评分角色读取。只核本次实际使用资产身份，不整根/模型/媒体重哈希；角色隔离不认证OS访问。

## 2. 固定实验矩阵与输入

| seed | C_NATIVE、D_NATIVE | C_HASH、D_HASH |
|---|---|---|
| 19、73 | 062已闭合预测直接缓存，更新/forward0 | 每臂新训250步，共4配置1000步 |
| 137、263、419、557、733、911 | 每臂新训250步，共12配置3000步 | NOT_PLANNED，不追加 |

C为062普通中心化/标量RMS，D为062角色差分/标量RMS；mu/s、84问题/锚规则、views直接冻结沿用。每次仍当前V与当前问题，D内部只用派生交换文本特征，不读其他格预测/标签或硬翻答案。本次不再比较N、换差分系数/损失/层/模型。D冷启动的额外文本编码成本不因缓存消失。

NATIVE原V[6,2560]不变。HASH严格采用058定义：每行转连续、小端float32字节b，按`(SHA256(b).digest(), b)`字节升序排序六行，原数值逐字节保留。键不得含时间索引、时间戳、q、标签或源ID；相同行可交换。对全部366 V核形状/有限性/行多重集合、幂等及四个固定置换[5,4,3,2,1,0]、[1,2,3,4,5,0]、[2,5,1,4,0,3]、[0,2,4,1,3,5]下结果完全相同，报实际改变顺序数量；全无变化则H_NO_EFFECT/BLOCKED，不换键。

HASH在训练与所有评估均使用同一视图，不只在测试打乱。它删除显式跨单元排列，但保留六行全部内容、单元内部运动/编码器上下文或隐含位置，不能叫完全无时间模型或纯时间信息量。相同变换同时作用C与D，完整2×2用于控制通用顺序收益。

## 3. 初始化、计划与4000步

每配置仍为056 TemporalHead(2560,2560)，356673参数、同pack/BCE/AdamW/clip，旧源码不改。原19/73 HASH直接使用062实际A初始state及[250,8] sequence，逐张量核相同。

六个新seed固定为137、263、419、557、733、911，不能替换。每seed `torch.manual_seed(seed)`后仅实例化一次056头取得初始state；独立`torch.Generator().manual_seed(seed)`生成`torch.randint(68,(250,8),generator=...)`。该seed C/D共享克隆的实际初始state与sequence，核68成员全覆盖；若未覆盖则BLOCKED而非重抽。不要调用056限定旧seed的shared_plan或修改其SEEDS；新计划在063自己的实现中按上述原生成规则建立。

固定训练顺序：19 C_HASH/D_HASH、73 C_HASH/D_HASH，再六新seed各C_NATIVE/D_NATIVE，共16配置×250＝4000真实forward/backward/optimizer step，batch8四格/32cell、128000训练cell曝光。CPU float32/线程4/interop1，AdamW lr.001/wd.01/betas(.9,.999)/eps1e−8、clip1，仅250步末期checkpoint；全部参数grad非None且有限，保留有限loss/初始末期state及实际参数变化。不得warmup头forward/软件优化、加步数/早停/挑seed/验证选择；数学HASH/索引fixture不是头forward。

CUDA_VISIBLE_DEVICES在torch import前置空，CUDA不初始化。训练Job actualactive0后才独立预测；所有新预测/代码/checkpoint/变换封存且预测Job actualactive0后才评分。种子同时改变初始化和批采样，不把差异单独归因某一者。

## 4. 14840正式项与完整表

新16头×183实例×4＝**11712新单V/当前q预测**。随后精确映射062的原19/73 C/D共2928项＋B0单次200＝**3128缓存**，不重forward。总**14840**、3710四格；无投票、模型ensemble、互补修复或按组翻预测。不同seed准确率均值仅为分析，不是新的部署答案。

**81条件行**：C_NATIVE/D_NATIVE×8seeds×4split＝64，C_HASH/D_HASH×19/73×4split＝16，B0/NA source_holdout50＝1。标记phase=CACHED_062或NEW_063，完整N/缓存新项/valid/INVALID/FAILED/NOT_RUN/unknown及单项/视频对/问题对/四格正确数与率，另061五类响应、K0..K4、question_invariant/率。17缓存行所有数字复现062，B0仍一套，不增独立N。缺测保留计划分母，unknown不当错；EMPTY未计划矩阵不造为失败配置。

新六seed的来源及开发54 C/D逐seed完整报告，包括均值/中位数/范围，不能只列好seed。原19/73及合并8seed仅描述，不进入新seed主门。不重复062覆盖分层搜索、无新标签或筛选。

## 5. 配对、交互与34区间

source_holdout50固定**14配对行**：8seed的D_NATIVE−C_NATIVE各一；原19/73另有D_HASH−C_HASH、D_NATIVE−D_HASH、C_NATIVE−C_HASH各一。每行n50、四格左右独对/都对/都错/unknown/净例数/pp及95%区间，问题不敏感左右数/差pp及区间；正的不敏感差表示更差。

JSON公开**350个匿名family配对行**（14×25），一致F01..F25、每行n2，包含上述配对计数/unknown及left/right_question_invariant，不含逐项预测/标签/正确性或反查源映射。足以独立重建所有配对边际与区间。

原19/73另各一交互行：`Delta=(D_NATIVE−C_NATIVE)−(D_HASH−C_HASH)`，这里差为四格正确例数差；报净例数/pp及95%来源组区间。Delta每次用相同抽样family联合求四头差，不把独立区间相减。正确性与问题不敏感仍分别解释，不以交互/响应变化代替答题。

Random55063一次初始化，10000次choices(range(25),k=25)，各簇两个实例全保留、实际抽样N。全部28个配对区间（14×答案/不敏感）、2个Delta、2个**新六seed平均差的来源组区间**共32区间用同一族抽样。新六均值对每个抽样先分别求6个配对差，再等权平均；不能把6×50当300独立视频。

另外Random55064一次初始化，10000次choices(range(6),k=6)，从**新六seed的整套50实例配对差**等权有放回抽seed，得到平均答案差及平均不敏感差的2个seed区间。它只描述固定50实例下观察到的优化种子变动；前述来源组区间固定6seed，二者不是联合新来源置信认证。全部共34区间，2.5/97.5%分位用position=(10000−1)×p线性插值。原19/73当前区间使用063公共流，注明与062历史区间不是同次重采样、不覆写旧表。

## 6. 三个预先固定判据

**新seed稳定性门（仅6个新seed，完整时判断）**：D_NATIVE−C_NATIVE严格正净值的seed≥5/6；平均净增≥4/50例；D平均四格全对≥10/50；C−D平均问题不敏感减少≥10/50（20pp）。平均以6seed等权，每seed分母仍50。全部满足才ROLE_CONTRAST_MULTI_SEED_DEVELOPMENT_SIGNAL，否则NOT_ROBUST_UNDER_FIXED_REPLICATION_GATE；旧19/73和合并8seed不得救门。

**D顺序门**：原19与73各D_NATIVE−D_HASH≥2四格例。**角色×顺序交互门**：两原seed的Delta各≥1例。三个门分开列出；只有三门均过才额外保留EXPLICIT_ORDER_INTERACTION_DEVELOPMENT_SIGNAL，仍非问题定位/纯时间信息/新算法或独立确认。

稳定性过但D顺序门未过：保留角色差分复验信号，未支持所要求的显式顺序收益。D顺序过但交互未过：仅通用顺序收益，未支持角色差分专有交互。稳定性未过：停止扩张当前差分收益主张。任何结果不修换低分H/C或补其他seed，不把单个正区间当门；如实保留全部loss/拟合/正负效果。H低分也可能涉及优化/表示可读性，正交互不自动定位因果成因。

## 7. 完整封存、预算和核验

针对062的代码来源限制，首个新配置STARTED/研究forward之前，封存**科学脚本/依赖、私有监督器、预算/账本辅助、独立核验脚本**及全部参数、成员、HASH索引、旧冻结views、初始化/计划、门/评分公式。报告排版代码可后写但单独留记录，不得改研究输入/运算；不追认062私有helper缺口。修复仅限首次消耗前，保留失败/成本并重封；研究开始后失败不重试/改名/续步。

父≤10800秒；训练＋预测＋评分CPU监督外层累计≤1800秒，其他准备/数学核验/只读独立复核≤900秒，JobRAM≤8GiB/active-process≤4、线程4。新根≤128MiB/512文件，initial/final/plan副本≤64MiB、起始free≥256MiB；固定几份append-only JSONL记步/预测，非每格建文件。特征/冻结views逻辑读量累计≤512MiB，元数据/旧预测≤64MiB，初始计划/头状态另计；区分字节计数、保守逻辑估算与未知物理I/O，不伪称硬配额。只哈希实际使用资产，不整根或模型/媒体重读。

既有conda pytorch与CPU，不安装/改环境；主模型/Qwen/视觉encoder/processor/tokenizer/new text encoding、GPU/nvidia-smi、媒体RGB/ZIP读取/解码、研究数据网络/TimeBlind访问0。新建独占063根、持久STARTED/CLOSED/计时与自有Job监督，核actualactive0/no kill，不动旧锁/账本或他人进程。缺资产/身份/锁/预算则BLOCKED并完整计划NA，不加来源或清洗难例。

独立核验不导入被测实现/评分器，不重复头/Qwen forward或optimizer；可只读CPU torch比较冻结062 views/normalizer、原19/73计划、新六实际初始/序列及每个初始末期state、4000步/11712预测账本、3128缓存投影、HASH数学性质和实际成员。由原标签/预测重建81/14/2表、350来源行、34区间及三门，核全部实际成本/代码seal/旧资产前后身份。无私有取证能力的公开负责人复核须明确限于聚合算术，不替代OS审计或物理来源认证。

## 8. 七处交付并停止

仅新增以下六文件并向results追加一次063父结果：

1. `prototypes/role_contrast_replication_063.py`
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（81行）
5. `paired-summary.csv`（14行）
6. `execution-summary.json`（含2交互/16配置/新六和合并八seed汇总/350来源行/34区间/三门/全部成本与未知）
7. `docs/codex-results.md`仅一次append

不上传原QA/事件文本/标签/逐项预测或正确性、数据/模型身份hash、路径/源映射、特征/views/normalizer/头权重或媒体；公共源码自身LF SHA可报。README/规划/AGENTS/旧代码/原结果不改。核七处allowlist，普通安全commit/push main后STOP；不自动本地064。负责人验收同时给出下一指令，新的数据/GPU仍需明确范围，不能继承旧余额。
