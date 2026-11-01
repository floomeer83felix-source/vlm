# 071 冻结选择器干预：答题收益是否依赖问题变化的时间权重

2026-11-01（北京时间）｜ChatGPT研究负责人。**READY，唯一尚未交付父任务；CPU_FROZEN_DIAGNOSTIC / TRAINING_ZERO。** 依据[070验收](../../research-decisions/post-070-review-and-selector-intervention-2026-11-01.md)，一包完成冻结模块干预、封存输出、配对评分和独立核验。070配方关闭，069继续暂停；不是新头搜索、三事件实验或论文内容。

## 1 范围和来源

安全同步独立文档main，读AGENTS/最新看板总览/本合同/070验收、070公开源码及原合同。确认本ID未交付且唯一READY。仅由明确handoff定位070闭合根及其登记来源，核push/Job实际active0/exit0、科学代码/输入/训练/output seal链。禁止扫私有目录、修改旧根、重训/恢复070或069。

只复用070 **四臂CONCAT/FACTOR/REVERSE/ANCHOR×六seed137/263/419/557/733/911的24个final state**，原两已用50池(source_holdout50/item_transfer50)的固定无标签observations、V/S/R、原anchors及原train84文本名单。参数/代码/float32/阈值/V六时间单元等与070一致。原input-seal只核本次实际所需的video.pt/views.pt/observations.json/transform-bindings.json/sources.json，不能为全表hash去读train.pt或训练标签。无需h、原初始计划、旧C/D state、图像/ZIP/processor/model配置。

video.pt/views.pt是原多split容器，允许有界读取容器并只投影上述两池和训练均值所需84问题的键，其余成员不分析；完整容器字节计入读预算，不伪称只读了所需切片。

最后评分角色才读取070封存new-outputs.json，投影两50池四臂原9600个答案；其余split/旧C-D不另分析、不forward。仅评分/独立核验按070已登记原060标签与原publisher内容身份/selected_positions重建两池真值和25×2文件family；继承070派生标签历史seal范围限制，不能倒填。只读精确旧来源，不换版本/名单，不联网补数据。

## 2 精确内部干预，零训练

每头均冻结/eval/no_grad。原070计算逐字保持：H=原video/PE/LN/conv/GELU，a/b的32+32投影、锚和g_read按原臂。独立计算以下三个条件，**只改alpha的来源**：

| 条件 | 时间权重 | 答案来源 |
|---|---|---|
| ORIGINAL_CACHED | 原g_select(q)的alpha，071仅测中间量 | 070原预测，只复用 |
| TRAIN_MEAN | alpha=softmax(H·mean_select/8) | 新干预输出或精确别名 |
| UNIFORM | 六个alpha直接各为float32的1/6 | 新干预输出或精确别名 |

mean_select为**每个已训练final头**在原84去重训练问题上的原g_select(q)均值：先按070逐问题float32 linear/GELU/cat得到64维向量，再按原UTF-8排序转float64求均值，最后float32。ANCHOR用原a(anchor(q))，其他按原路由；无验证/测试拟合、标签、重标准化/裁剪/温度。它是学得投影后的训练均值，不是S均值，也不能先平均S/R再过非线性。均值一经生成先封存，每头仅一个向量，所有评估问题/视频共享。

三条件**同一H和同一原g_read(q)**，仍u=sum alpha H、o=sum alpha xi H、z=原MLP(concat(u,o,g_read,u*g_read))，strict z>0。MEAN仍依赖视频内容/位置；UNIFORM仍保留H内的时间/卷积信息，二者都不叫无视觉/无时间模型。CONCAT/REVERSE的原读出也含共享分量，保留该差异，不能称所有模型都只有R读出。

允许为本次几何诊断新计算原H/g_select/g_read/alpha和MLP输入，**不计算原未干预MLP答案或logit，不调用原head.forward重问旧QA**。这些原注意中间量标为071_NOW_MEASURED，不冒称070已保存。V→H可每head/video复用，问题投影可每head/q复用，但每个实际子模块调用及中间量用途须分报，不能用“零原完整答题forward”掩盖有部分重算。原logit没有历史证据，不报logit变化。

**精确别名避免重复调用。** 在固定final state下，以最终256维float32 MLP输入的字节身份＋逐元素相等核对原条件及两个干预。若与原070某个已执行单元完全相同，不重做MLP，输出封存为指向该原键的deferred alias，评分阶段才解析原二值；若与本轮已封存新单元相同，可指向最早合法新键。别名无环/有唯一终点、同state/精确相等，不因“很接近”或分数选缓存。预测阶段不读旧答案、答案标签或正确性，不用标签推断相同输入。若同输入多个原键，最后核原答案一致，否则STOP_IDENTITY_CONFLICT。没有精确别名时每干预cell一次新MLP输出，不重复原完整头。

矩阵：24头×两池×两个新条件×200cell，**最多19200个新CPU干预答案调用**；原9600缓存，加干预19200逻辑项=**28800计划cell**。别名减少实际调用但不减计划分母；报告new_actual/original_alias/new_alias/failed/notrun/unknown守恒，不能把别名伪称新forward。三条件×四臂×六seed×两池=**144条件**。只对两个已用50，不加train/val/dev的答题运行。

## 3 运行顺序与封存

全部科学/依赖/预算/supervisor/别名与独立核验代码、矩阵/统计和上限在首次071研究tensor读取前封存。先做静态schema/接口审查；最多6次纯合成CPU小头forward、0更新，核显式override与同一个合成select的原计算一致、UNIFORM和训练均值算法/读出保持，纯软件检查不算科研样本。不能使用真实输入作warmup或挑干预强度。

准备只读必要的原seals/24 final/视图/anchors，生成并封存24 mean_select。按seed、臂CONCAT→FACTOR→REVERSE→ANCHOR、split原固定顺序、TRAIN_MEAN→UNIFORM完成所有干预；新单元/别名STARTED/CLOSED及输入/模型身份耐久记录。输入/均值/代码完整性检查先行。某输入或配置失败不得改精度/batch/模型/统计再跑，先持久化reason_code、actual/limit/阶段/已完成/剩余，保留UNKNOWN。

封存新输出/别名及中间量、所有键集，预测Job实际active0/exit0后才评分。评分独立解析070原9600缓存并解别名；原48条件必须逐字段复现070公开两池四臂分数/响应。真实答案只进评分，不影响投影均值、别名、原始alpha或任何运行选择。全部旧文件只读，过程角色不是OS访问审计。

## 4 公开统计和解释

144条件逐行报告head_arm/seed/split/condition、N50/cell200、实际新调用/别名/原缓存/状态/两类unknown、单项/视频对/问题对/四格/不敏感/K0..K4/五分类与百分比；不完整相关指标NA，不删题或充0。**96配对行**＝四臂×六seed×两池×两干预，各干预−原条件，列独对/对方独对/都对/都错/unknown/net/pp、不敏感差和预测改变cell数。

**96注意汇总行**，每个同样的arm/seed/split/干预：N50/cell200，原与干预alpha的L1距离mean/median/p95、各自平均熵(自然log，0log0=0)、预测改变数/比例。分位按(n−1)p线性；L1∈[0,2]、熵∈[0,log6]。在全部计划成员上汇总，不按正确性筛选。热图/权重变化不代替答题影响、事件定位或因果语义证据；无逐成员向量/热图公开。

固定**32个四格均值差95%区间**：四臂×两干预×两池×文件/seed两轴。文件轴50Salads仍25family×2，VIDHALLUC50文件对；每单位合计六seed的(干预四格正确−原四格正确)，分别−12..12的25箱/−6..6的13箱。**304箱**＝四臂×两干预×(25+13)，包含零频数，各频数和G、加权和等于六seed总净。不同对照分别边际规范展开，不保持真实跨干预/臂对齐，不做联合交互或混合两池。

每池独立重置Random55072一次，10000次choices(range(G),k=G)，四臂×两干预共享该池索引；文件轴样本差=100*sample_sum/300。每池Random55073一次，10000次choices(range(6),k=6)，固定seed顺序，各干预取六seed净值样本和/300×100。两轴点=原六seed总净/300×100，2.5/97.5%线性position=(10000−1)p。文件轴固定六头，seed轴固定该50条目；无p值/子组/响应或逐seedCI。阻断仍交144/96/96/32/304计划行，未执行频数/指标NA、draws0/planned10000。

完整记`COMPLETE_FROZEN_SELECTOR_INTERVENTION / RETROSPECTIVE_DIAGNOSTIC`，不完整`INCOMPLETE / SCIENTIFIC_UNKNOWN`。**无新配方PASS/排行榜/最佳模型选择门**：完整报告每头/每池/每干预的影响、全部正负零值与区间。区间含0不证明等效；分数保留不证明从未用语义，分数下降也不证明定位正确。固定内部模块干预不等于真实视频反事实，更非三事件选择性/原创性确认。070停止结论不改，不把ANCHOR升级新方法，不恢复训练或论文。

## 5 核验、预算和交付

独立核验不import被测scorer、不forward/训练模型，不重算MLP/conv/learned投影/原答案。核24 state/seals/冻结性和原视图/映射、mean_select等于封存84选择向量float64均值、各干预常量/均匀性、三条件H/g_read共享、别名精确输入/同state/无环及原答案一致、新输出阈值/键/账本、144条件/96配对/96注意/304箱/32区间与原48条件；从封存alpha重算归一化/L1/熵及评分、独立bootstrap。静态源审查/中间量恒等式不冒充独立重做全部learned forward；所有未独立证实项明确限度。

既有CPU/pytorch，CUDA_VISIBLE_DEVICES=''，线程≤4/interop1、CUDA不初始化。干预准备/部分图重算/新输出/评分监督累计≤900秒，其他静态/fixture/独立核验≤600秒，父≤10800秒；Job RAM≤8GiB/active≤4。新根≤256MiB/1024文件、起始free≥1GiB；原特征/views逻辑读≤256MiB、24state逻辑读≤128MiB、旧metadata/输出/标签≤64MiB（含核验/hash），复用同角色闭合缓冲可分列。计量模型子图/新MLP/别名与fixture调用，不伪精确物理IO/硬配额；不得安装/迁移环境、删旧锁账本或杀他人Job。

研究优化/backward、新训练/新state选择、旧C/D forward、原070未干预完整答案重算、Qwen/encoder/processor/GPU命令/媒体/下载/研究网络/论文内容全0。不读取训练答案；不复制旧完整根。所有失败有事实落盘并安全关自身Job，不能以新ID隐藏重试。

精确十处allowlist：

1. `prototypes/frozen_selector_intervention_071.py`（显式入口，导入无研究操作）
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（144行）
5. `paired-summary.csv`（96行）
6. `attention-summary.csv`（96行）
7. `mean-intervals.csv`（32行）
8. `difference-histogram.csv`（304行）
9. `execution-summary.json`（矩阵/原和新/别名/子图调用/实际预算/全部公开表/核验范围/失败/未知及code LF SHA）
10. `docs/codex-results.md`仅尾增一次本父结果

不改070/其他历史代码、结果、论文、规划或本README。不公开原QA/标签/逐例预测或正确性/中间向量、真实成员/源映射/私有路径/资产hash/特征/权重；只交科学代码hash和聚合。核精确暂存和append-only，普通安全push main后STOP。无自动072/新头训练/论文；负责人验收后另定有证据支持的下一步。
