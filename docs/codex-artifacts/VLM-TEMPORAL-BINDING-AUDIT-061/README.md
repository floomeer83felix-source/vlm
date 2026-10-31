> **ARCHIVED / 061_CLOSED / 不可执行（2026-10-31）。** [e5e479d交付](https://github.com/floomeer83felix-source/vlm/commit/e5e479d27a5ac4f9b05f931e0602340ea6d006a7)已由[负责人验收](../../research-decisions/post-061-response-audit-disposition-2026-10-31.md)：6056缓存项/1514四格完整，33条件、225标签盲来源行和26区间复核通过；来源小头问题不敏感60–92%，B0单次22%，50/50来源对两事件名称均未见于train68。7837公开检查PASS，因果成因仍未定，无新机制/收益。当前0 READY；不重跑或自动062。以下原合同/启动文字仅作历史保留。

# 061：缓存中的视频—问题响应与迁移缺口分解

2026-10-31（北京时间）｜ChatGPT研究负责人。**READY，唯一尚未交付的新父任务；CPU_ONLY / CACHED_DATA_DIAGNOSTIC。**

一轮完成输入核验、6056项响应分解、缓存几何/词汇覆盖、独立核验和统一交付。不训练，不运行任何新/旧模型forward，不另派准备轮。研究依据及直接近邻见[探索决策](../../research-decisions/post-060-bottleneck-exploration-2026-10-31.md)。

## 1. 固定问题与读取范围

问题：060四格失败主要表现为不随视频变、不随问题变，还是双轴一致但方向错误？缓存精确碰撞与训练事件字符串覆盖能否进一步约束解释？输出模式是行为诊断，不能独自定位因果瓶颈或证明新机制。

安全同步独立Git文档仓库main，完整读AGENTS、本合同、探索决策与[060验收](../../research-decisions/post-060-pool-transfer-disposition-2026-10-31.md)；next-steps/overview只读最新页首及061/060段，results全文检索061并读唯一060条目。确认唯一READY为本ID且无既往结果，旧任务全部不重跑。

从当前本地运行登记/明确handoff取精确060私有根，不递归扫描。只读其parent-closed、训练/预测/GPU闭合记录、data-bindings、四split标签/observations、feature-index、all-outputs-sealed、pre-consumption-seal及outputs-identity-seal。通过这些已知索引只读实际复用的366V/220q；旧057特征路径仅按060索引解析，不遍历旧根。仅核本次实际读入文件的seal及哈希，不重读模型权重/checkpoint、ZIP、视频、RGB或整套旧资产。元数据/旧预测读取≤32MiB；缓存tensor读取≤64MiB，每文件≤2MiB。UTF-8，旧BOM可utf-8-sig。

只可先查看路径登记、闭合记录及文件存在/大小；首次读取data-bindings、旧预测/评分标签的实际值或开始正式诊断（较早者）前，封存061代码、公式、输出schema、全部阈值和计划，再按以下规则一次分析。

核060提交876eded对应代码/输出封存、133/50与68/11/54/50、25/4/20/25组、原816缓存＋5040新头＋200 B0＝6056。8头配置A25/P1_25/A68/P1_68×seed19/73各183个四格，另B0/NA仅50来源实例，共1514四格、33条件。B0只读单次结果，不按seed复制。标签必须满足y00=y11、y01=y10、y00+y01=1；全部6056输入预测必须CLOSED且严格二值。身份/闭合/成员/标签关系不符即BLOCKED，不修旧封存、补forward、删样本或将未知当错。

核验/审计角色可依此合同读取明确旧标签/预测；没有训练或根据得分挑条件。程序角色与seal不等于OS访问审计。

## 2. 16种输出的精确分解

每实例取p00,p01,p10,p11，第一索引为视频、第二为问题。按以下互斥顺序分类：

| 类别 | 精确定义 | 模式数 |
|---|---|---:|
| CONSTANT | 四项相同 | 2 |
| VIDEO_ONLY | p00=p01，p10=p11且p00≠p10 | 2 |
| QUESTION_ONLY | p00=p10，p01=p11且p00≠p01 | 2 |
| CHECKERBOARD | p00=p11，p01=p10且p00≠p01 | 2 |
| MIXED | 其余；恰有一个或三个1 | 8 |

CHECKERBOARD按旧标签拆为全对/全反；其余不改预测。每33条件行保留原N、n_cells/complete/valid/unknown/status、原单项与四格全对数，五类数、checkerboard_correct/inverted及K0..K4（每实例正确单项数直方图）。须逐项复现060公开33行原正确数与分母，不重写历史结果。

同时报告question_invariant=CONSTANT+VIDEO_ONLY、video_invariant=CONSTANT+QUESTION_ONLY，各除完整N；qflip_edges=2×(QUESTION_ONLY+CHECKERBOARD)+MIXED，vflip_edges=2×(VIDEO_ONLY+CHECKERBOARD)+MIXED，各以2N为分母。核K0=全反棋盘、K4=全对棋盘、K2=前三类和、K1+K3=MIXED及sum(k×Kk)=原单项正确数。它们是同一模式的不同表达，不宣称多项独立发现。不做配对投票、互补修复、测试标签翻转、置信度排序、最优模式投影或oracle纠错得分。

公开source-profile.csv恰225行：9个来源条件×25个字典序family（匿名F01..F25，所有方法相同对应），仅method/seed/family/n=2与五个**不读标签**的类型计数。不公布每项预测、K、标签、各family正确数或可反查源名/身份hash。五类全表允许从此表独立复算来源响应率。

## 3. 固定来源组区间

来源N50已使用，以下全为描述性诊断。对9条件各question_invariant、video_invariant两率，得到18个边际区间；再对每seed的A68−A25及P1_68−P1_25，各上述两率得到8个配对差区间，共26条。正差表示不变比例增加，不叫准确率提高或新的胜负门。

25个文件family有放回等概率抽25簇，保留每簇两个实例、按实际N计算，10000次；`random.Random(55061)`只初始化一次，以`choices(range(25),k=25)`生成每次公共索引序列，所有26统计量使用同一次抽样。配对差在共同簇上联合计算。2.5/97.5%分位用position=(10000−1)×p的线性插值；记录点估计/区间/来源N。不将四格、两seed或文件family当新增独立原始来源/已验证participant。

## 4. 缓存几何和词汇覆盖

CPU tensor只用torch.load(map_location='cpu',weights_only=True)读索引中有限float32 V[6,2560]/q[2560]；不导入057—060被测模块、加载头状态或调用nn.Module/processor/tokenizer。CUDA_VISIBLE_DEVICES在import torch前置空，torch线程≤4、interop1，确认CUDA未初始化。数值诊断用float64；主分析对重复路径/相同输入tensor只读一次，独立核验可再读一次，累计仍≤64MiB。

对四split分别汇总，所有分位采用排序后position=(n−1)×p线性插值、p=0,.25,.5,.75,1：

- q交换相对距离||q0−q1||/(||q0||+||q1||+1e−12)，另计逐元素精确相同及距离≤1e−4。后者只叫小数值差，不当成语义丢失证据。
- V有序相对Frobenius距离||V0−V1||/(||V0||+||V1||+1e−12)，及遍历六行全部720置换所得最小相对距离；这不是动作定位，视频段交换也不等于逐帧反转。
- 每V时间变化比例sum_t||Vt−mean_t V||²/(sum_t||Vt||²+1e−12)，汇总2N个视频槽并报唯一数，不称独立样本。
- 每split精确q碰撞或精确有序V碰撞实例的并集数，以及必要上限N−并集数。该上限仅约束读取此V/q的确定性小头，不约束直接读RGB/原问题的B0或其他表征。仅精确碰撞能给这一确定性输入约束；上限高不证明可学习性、近距离不作不可恢复判定。

只从封存问题原字符串解析两事件，不读标签作筛选。统一`' '.join(event.replace('_',' ').split()).casefold()`，不做同义词/词干/LLM重写。始终保留两个事件位置，无序对为长度2排序tuple；若归一化后二者相同，只另计碰撞，不删实例/改标签。以train68事件集与无序事件对集为唯一参照，四split各报告PAIR_SEEN、BOTH_EVENTS_SEEN_PAIR_NEW、ONE_EVENT_SEEN、NO_EVENT_SEEN四互斥计数，合计原N；另报原/去重q数量。只发布覆盖计数，不作小分层准确率表或按模型效果再排样。未见字符串不等于未见动作语义、Qwen预训练未见或已证明域迁移成因。

## 5. 核验、预算和失败处理

先用不含真实QA的16种二值枚举独立验证类别互斥穷尽、2/2/2/2/8基数及边/正确数恒等式。独立核验不得导入本次分析模块：从旧封存预测/标签重建33行、6056守恒和五类，重新读取公开225行复算26区间；核366V/220q、4个覆盖/几何汇总与公式、所有实际读取seal/前后旧文件不变。geometry可用原缓存只读复核，仍计CPU预算；不得借核验重复模型/头forward或更新。

父elapsed≤3600秒，全部受监督CPU分析/独立核验外层累计≤300秒，JobRAM≤2GiB/active-process≤4、线程≤4；新根≤32MiB/256文件、起始free≥256MiB。现有conda pytorch，不装依赖/改环境；新模型、主模型权重读取、Qwen/小头forward、optimizer/update、GPU/nvidia-smi、媒体/数组RGB读取、解码、研究数据网络和TimeBlind访问均0。纯特征数学运算不算模型forward，但如实记录tensor读取与分析耗时。

独占新061根、持久STARTED/CLOSED及计时、既有自有Job监督/actualactive0/no kill；不动旧锁/账本或他人进程。正式诊断开始后不改变成员、公式、阈值/预算重试；失败保留33计划行和NA/UNKNOWN，不把缺测当0。输入/预算不合格提交有界BLOCKED回执，不新建替代任务。必要软件修复仅首次正式诊断STARTED前，修复/成本保留并重封。

## 6. 七处交付，推送后停止

只新增下列六文件及向results追加一次061父结果：

1. `prototypes/temporal_binding_audit_061.py`
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（33行）
5. `source-profile.csv`（225行）
6. `execution-summary.json`（含26区间、4个词汇覆盖/几何汇总、全部实际成本/未知）
7. `docs/codex-results.md`仅一条append

科学回执要回答三项诊断，并对A25/A68/P1_25/P1_68两seed和单次B0完整比较。若完整则`COMPLETE_CACHED_RESPONSE_AUDIT / CAUSAL_BOTTLENECK_UNRESOLVED / NO_NEW_METHOD_CLAIM`；可指出主要行为模式，但不得改成已查明某层/语义成因。精确碰撞是输入限制，不等于整体因果归因；若无突出模式也如实报告，不能强造下一机制。

禁止原QA/事件文本、标签、逐项输出/正确性、模型/数据身份hash、私有路径/源映射、特征/媒体/权重上传；公共源代码自身LF SHA可报。README、规划、AGENTS、旧源码/结果不改。检查七处allowlist，普通安全commit/push main后STOP；不自动062、不继续架构/损失搜索或申请消耗旧GPU余额。
