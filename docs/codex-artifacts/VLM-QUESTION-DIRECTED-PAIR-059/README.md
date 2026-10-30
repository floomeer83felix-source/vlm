> **负责人归档（2026-10-30）：ACCEPTED_COMPLETE_CPU_2X2_EXPERIMENT / STOP_THIS_MECHANISM / CLOSED，不重跑。** [验收](../../research-decisions/post-059-directed-pair-disposition-2026-10-30.md)：8配置2000真实更新，R1四格7/24、9/24，A5/24、7/24，P1为6/24、12/24；R1−P1 +1/−3，Delta +9/−3，预设开发门FAIL。2004公开检查及8配对/2交互区间独立复算PASS；低分对照原样保留，不调参/修对照/改称P1贡献，当前0 READY。以下原合同完整保留为历史，不是新的执行授权。

# 059：问题条件化的有向特征对交互

2026-10-30（北京时间）｜ChatGPT研究负责人。**READY，唯一新父任务；尚未执行。**

用户在058交付后要求下一步；本任务是新的表示机制开发实验。复用闭合缓存，一轮完成实现、8个真实CPU训练、封存评分与脱敏交付，不拆准备父任务，不恢复057联合损失。收到用户在本地Codex发出的本轮执行指令后才运行。

## 1. 可否证主张与边界

**问题在时间特征两端发生交互之前调制特征，配合有向二阶关系，能否超出同参数的一阶顺序池化，以及关系汇总后才接入问题的对照？**

057已否定该次四格联合损失配方；058仅保留原顺序A优于指定内容排序H的开发信号。059改变表示的计算，不增加联合损失。采用完整2×2：一阶池化P/二阶关系R×关系支路晚期0/早期1接入问题；四头均用逐cell BCE、同参数/初始化/样本计划。R1为候选，P1控制二阶交互，R0控制关系支路的问题注入位置，P0补足差分中的差分；另复用原A为实际性能基线。

这里的节点是冻结模型的六个时间特征单元，不是已定位并命名的事件。二阶反对称乘积表示有向特征对关系，不能直接叫作事件定位或因果发现。最终推理只接受当前V和q，不读配对视频、另一问题/预测、标注时间或来源。不对四格强制互补、翻转答案或修复预测。

文献约束：时序关系网络已有[TRN](https://arxiv.org/abs/1711.08496v2)，问题引导时间注意已有[QueST](https://ojs.aaai.org/index.php/AAAI/article/view/6766)，先于定位的问题条件化已有[GroundFormer](https://arxiv.org/abs/2608.15708)。后者目前核对到作者摘要，正文抓取不可用，不据此声称逐层实现不同。反对称、时序关系和问题条件化这些概念都不单独算创新；059是上述明确计算及强对照的候选实验，`NOVELTY_UNRESOLVED`。

同51实例/25训练2验证24开发测试已在057/058使用。059不是新盲测；即使通过门，也仅为`DIRECTED_PAIR_DEVELOPMENT_SIGNAL`，后续仍需与相关方法实质区分及新数据确认。验证2例不调参/选seed/早停。058两个区间包含0的限制不变，不扩大原055数据规模门或宣称改善冻结LLM内部推理。

## 2. 输入、读取和身份

安全同步独立文档仓库main，完整读AGENTS、本README、[058验收](../../research-decisions/post-058-order-control-disposition-2026-10-30.md)；next-steps/overview只需最新页首及059/058相关段，results全文检索本父ID并读057/058唯一条目。确认唯一READY及059无既往交付。读[056小头](../../../prototypes/question_temporal_056.py)、[057训练](../../../prototypes/question_temporal_train_057.py)、[058实现](../../../prototypes/question_temporal_order_control_058.py)的缓存/初始计划/分角色交付逻辑；旧源码/合同/结果不改。

只从既有057运行登记/handoff定位其精确私有根，禁止递归搜无关目录。057根只读、运行闭合/active0。复用原102份有限CPU float32 V[6,2560]、54份q[2560]、三份无标签observations、原训练标签、两个实际pretrain-seed*.pt及training/plan-*.pt；原25/2/24顺序、cell索引、16/2/15参与者组和原标签绑定均不变。058的H排序视图不进入059训练。

核原特征/index/代码/原初始计划/输出与闭合seal，前后仅哈希本轮实际复用文件；旧计划须张量逐项匹配，不能用新生成计划替代缺失旧资产。原A两seed三split408个闭合输出必须通过057 seal，基线计数须原样恢复。核验角色可投影旧A及带标签seal中的来源分组；训练角色仅读train标签、独立无标签observations、特征和初始计划，不读A/B0/H预测、验证/开发测试标签、来源组或带答案的pilot seal。角色分离不是OS级无访问证明。

资产缺失、身份冲突、旧任务未闭合或本任务STARTED已存在则有界报告BLOCKED，不下载、重抽特征、重训A或修旧账补齐。不读媒体/帧/主模型权重，不重哈希ZIP或复制旧根。

## 3. 固定模型：公共编码、2×2关系支路

所有新头r=64、float32，GELU采用PyTorch默认exact，LN为无仿射LayerNorm、eps=1e-5。仅以下可训练参数：Wv/bv：2560→64；Wq/bq：2560→64；Wh/bh：64→64；Wa、Wb：64→64、均无bias；Wf/bf：256→64；wo：64→1、无bias；标量tau。四头总参数各`64*(Dv+Dq)+7*64^2+5*64+1 = 356673`，与原A相同。所有参数必须进入实际计算，不加未用参数凑数。

对t=0..5：

```text
x_t = Wv V_t + bv
h_t = LN(GELU(x_t + Wh LN(x_t) + bh))
g   = LN(GELU(Wq q + bq))
alpha_t = softmax_t(dot(h_t,g)/8)
u = sum_t alpha_t h_t
```

无正弦/绝对时间位置编码、跨t卷积或其他时序编码。h的处理逐单元共享；四头只在下表指定之处不同。`⊙`为逐通道乘积，所有t<s的15对全部使用，不采样对或读拼接点。

| 计算 | P0：一阶/晚期 | P1：一阶/早期 | R0：二阶/晚期 | R1：二阶/早期候选 |
|---|---|---|---|---|
| a_t | GELU(Wa h_t) | GELU(Wa h_t + g) | GELU(Wa h_t) | GELU(Wa h_t + g) |
| b_t | GELU(Wb h_t) | GELU(Wb h_t − g) | GELU(Wb h_t) | GELU(Wb h_t − g) |
| w_ts | 1/15 | (alpha_t+alpha_s)/5 | 1/15 | (alpha_t+alpha_s)/5 |
| d_ts | ((a_s−a_t)+(b_s−b_t))/2 | ((a_s−a_t)+(b_s−b_t))/2 | a_t⊙b_s−a_s⊙b_t | a_t⊙b_s−a_s⊙b_t |

`o_raw=sum_{t<s} w_ts d_ts`；固定`o=o_raw/sqrt(mean_channels(o_raw^2)+1e-6)`，不尝试其他缩放。四头权重总和均1。P是经逐点非线性后的线性有符号顺序池化，可代数化为各t向量的加权和，没有两时刻特征乘积。Wa/Wb两条非线性支路均真实使用。P0/R0仍在公共alpha/u及最终输出读取当前问题，不是问题盲模型；0仅从时间关系支路的a/b和权重中移除问题，因此因子控制的是该支路的早期条件化整体，不能把差异细分为某一个注入点的独立因果效应。

所有头共用相同的方向读出：

```text
f(o) = dot(wo, GELU(Wf concat(u,o,g,u⊙g) + bf))
z = exp(clamp(tau,-2,2)) * (f(o)-f(-o))/2
prediction = int(z > 0)  # z==0为No；非有限值为失败，不能修复
```

tau是实际使用的正温度参数，不是被相减抵消的输出bias。四头都具有同一反转奇对称结构：在固定当前q下，**倒置六个特征向量**理论上使z变号；因此R1若赢，不能仅归因于它独有这种结构。该代数约束不是配对输出修复；不把特征倒序当作真实视频反事实标签，也不认证事件片段交换等于帧倒放。

## 4. 初始权重及一次真实训练

从057每seed原state确定映射：video和question权重/bias不变；`Wh=conv.weight[:,:,0]`、`bh=conv.bias`；`Wa=conv.weight[:,:,1]`、`Wb=conv.weight[:,:,2]`；`Wf/bf=mlp.0.weight/bias`；`wo=mlp.2.weight`；`tau=mlp.2.bias[0]`。切片数值直接复制，无转置/重新初始化；同seed四个新头的全部初始参数必须逐项相同，原A与新头计算不同而参数数目相同。封存映射后的初始state和原250×8样本sequence；不修改旧state或调用旧056 train去构造错误架构。

8配置：每seed19、73按P0→P1→R0→R1，各250步，共**2000次真实backward/optimizer.step**。同seed共享原实际sequence，每步8四格/32cell。仅均值BCE `mean(softplus(-(2y-1)*z))`；AdamW lr0.001/wd0.01/betas(0.9,0.999)/eps1e-8，clip全参数norm1，CPU线程4，模型float32，无dropout/新数据增强/验证选择/额外损失。每配置2000四格/8000cell曝光。可复用056的pack和optimizer，旧源码不改。

首个研究配置STARTED前完成代码/输入/公式/初始映射封存。每配置先持久登记唯一059/arm/seed STARTED，再用其初始化模型对**固定训练第0个四格**做三次batch4软件forward：原V、倒序V、重复首向量6次。核有限输出、倒序`abs(z_rev+z)<=1e-5+1e-5*abs(z)`、重复输入abs(z)<=1e-6。合计24次新头软件forward/96cell，不读/评分这些标签，优化0；单列计数，不作正式评估或Qwen调用。失败不改公式重试，停止并保留已启动状态。

每步先登记STEP_STARTED，再forward/BCE/backward，核loss/每个参数grad有限且非None，clip/step后STEP_CLOSED。所有新头无未使用/冻结凑数参数。记录实际参数数、初始化相等、loss首末/范围、参数L1变化、原采样计划和曝光；这些只是执行证据。仅最后一步checkpoint；不得挑seed、早停、增步、修STARTED配置或在结果后调整公式。

## 5. 封存评分与固定去留门

训练角色对8个最后checkpoint各自按当前单V/q输出三split预测：8×51×4=**1632新cell**；原A复用408，合计2040个正式评估cell。禁止重训或重新forward A/B0/I/V/S/H。单cell `predict(model,V,q)`，不查另一格或强制互补。封存新预测/checkpoint/代码/初始state等身份，全部训练Job actualactive0后，独立评分角色才读原验证/开发测试标签及A缓存。

30行条件表＝5方法（A_CACHED/P0/P1/R0/R1）×2seed×3split；每行报告原N/cell分母、单项/视频对/问题对/四格全对及失败/INVALID/NOT_RUN/unknown、新/旧预测来源。A所有指标必须与057六行一致，四格train24/20、validation2/2、test5/7，否则绑定失败而不是新基线。错误/无效不剔除；缺项/无法判断保持UNKNOWN，不能输出完整实验收益门。

8行配对表＝R1对A_CACHED/P0/P1/R0×2seed，开发测试N24、15参与者组；列R1独对/对照独对/都对/都错/unknown及净增/百分点、来源组区间。另在JSON固定报告每seed的2×2交互量：`Delta=(four_R1-four_R0)-(four_P1-four_P0)`及百分点/组bootstrap区间，不能把普通问题注入收益归给二阶关系。**仅在完整评估下，两seed均满足R1−A≥2例、R1−P1≥2例、R1−R0≥1例、Delta≥1例**才记`DIRECTED_PAIR_DEVELOPMENT_SIGNAL`。否则完整比较记`NO_SUPPORT_FOR_THIS_DIRECTED_PAIR_RECIPE / STOP_THIS_MECHANISM`；不完整为`INCOMPLETE / SCIENTIFIC_UNKNOWN`。R1超过A但不胜强对照或无正交互不保留中心机制；不因某个对照/seed较好就把它改名新贡献。

这是已知A和058结果后、059新模型执行前固定的开发投入门，不是独立确认或显著性阈值。Delta是这项答题指标上的设计交互，不认证因果关系或问题相关定位。无论门结果，不恢复057联合损失；若通过，只保留候选，下一轮另定新确认数据、来源重叠核查和最近相关方法强对照。若未过，停止此具体结构，不继续调注入位置/通道/损失/seed/步数。

每配对及每seed Delta均按15组等概率有放回抽15组、组内全取，实际抽样N作分母，10000次、每seed/对照或Delta独立重置`random.Random(55059)`，原group_key排序，2.5/97.5%线性分位。公开120行匿名S01..S15×2seed×4对照的n、双方独对/都对/都错/unknown/net，支持独立复算。每组交互净值可由三行净值`net(R1,R0)-net(R1,P0)+net(R1,P1)`重建，Delta区间用该组净值/实际抽样N，不将不同对照独立抽样。区间是开发不确定性描述，不增加独立N、推断厨房独立或测TimeBlind。

## 6. 新预算与失败策略

使用现有conda pytorch，无安装/环境修改。GPU/主模型权重加载/encoder/特征抽取/媒体解码/nvidia-smi/研究数据网络请求均0；允许新小头实例化、旧小头初始state加载及本轮CPU forward/训练。`CUDA_VISIBLE_DEVICES=''`，torch导入及各Job结束核CUDA未初始化。

父elapsed≤5400秒；CPU训练＋预测＋评分外层累计≤1200秒，其他准备/软件检查/独立核验CPU外层累计≤600秒，线程≤4、JobRAM≤8GiB、active-process上限4。新根≤512MiB/1024文件、起始free≥1GiB；checkpoint＋初始计划副本≤32MiB，不复制媒体/模型/完整旧根。最多2000研究更新；24软件forward单列，不得新增合成优化、搜索臂、暖机更新、补跑或重置预算。

只写独立059根，配置/步骤持久账本及deadline先行。所有公式/训练代码修复仅允许在首个配置STARTED之前，修改后重新封代码；此后发生改变计算的错误则停止，不重命名或恢复配置。缺少既定资产/计时/预算/锁条件则BLOCKED；只关闭自有Job并核actualactive0，不删旧锁/杀他人进程。失败项保留计划分母及状态，不把loss改善/结构不变性检查当作答案收益。

## 7. 一次七处脱敏交付

1. 新`prototypes/question_directed_pair_059.py`，显式入口，导入无I/O、模型forward或训练。
2. 本目录新`execution-receipt.md`，含映射/封存/步骤/软件检查/角色/资源/失败及独立复核说明。
3. 本目录新`scientific-results.md`。
4. 本目录新`condition-summary.csv`（30行；BLOCKED仍列计划N和NOT_RUN）。
5. 本目录新`paired-summary.csv`（8行）。
6. 本目录新`execution-summary.json`（含表、两seed交互量与区间、120匿名来源行、2000更新/24软件forward/参数/代码SHA/资源证据及限制）。
7. `docs/codex-results.md`仅追加一次`### VLM-QUESTION-DIRECTED-PAIR-059`。

独立复核应从新封存文件核原初始切片映射及八配置相同初始化/实际参数、原计划曝光、2000步、1632新＋408缓存预测/原标签绑定、30/8表、两个交互量和120分层/bootstrap、软件不变性及预算/旧文件只读。可用torch做只读小头state核对但不forward/训练，或stdlib读张量存储；若某项未独立复核须写UNKNOWN，不靠调用被测scorer充当独立复算。短复核源码可内嵌回执，无额外public文件。

不公开QA/答案/逐题logit预测或正确性、真实源映射/数据身份hash/私人路径、特征/媒体/帧/权重/checkpoint。只上传代码hash和聚合匿名计数。README/AGENTS/看板/总览/旧协议、代码和报告不改；只stage七处allowlist，普通安全push后STOP，不自动060或后台继续。

## 8. 给本地Codex的简短指令

```text
执行VLM-QUESTION-DIRECTED-PAIR-059。安全同步main，读AGENTS和059 README，确认唯一READY且未交付。
复用057原缓存/划分/初始计划，按README实现一阶池化P/二阶关系R×关系支路晚期0/早期1接入问题的2×2对照，四头均356673参数、只用BCE；seed19/73各250步，共8配置2000次真实CPU更新。
候选R1须与原A缓存及P1/R0比较四格全对率，并报告2×2交互量；一轮完成实现、训练、封存评分和独立复核。不调参、不重跑旧模型；不下载、不用GPU或重抽特征。七处脱敏交付并推送main后停止。
```
