# 补充材料

## S1 固定项目判据及其解释

这些要求在相应后续结果产生前固定，作用是项目投入决策，不是社区科学有效性阈值、显著性检验或统一效应判定。原两seed19、73的开发比较要求D各至少10/50、D−C各至少3例、D−N各至少2例，且C−D问题不敏感数各至少10例。原结果D15/13、C2/8、N6/4，答题与响应要求均满足，第二seed的D−C区间仍含0。

后续六新seed137、263、419、557、733、911的稳定性要求为正净增至少5/6、平均D−C至少4/50、D平均至少10/50及问题不敏感平均减少至少10/50，四项共同满足才继续。实际正差6/6、净增38/6例、D53/6例、响应减少101/6例；唯独53/6<10，完整稳定性要求未满足。合八D平均10.125例只是描述，不能替换事前新六样本。

原两seed另外要求D_NATIVE−D_HASH各至少2例、交互Δ=(D−C)_NATIVE−(D−C)_HASH各至少1例。实际顺序净9/8、交互9/2，两个计数要求满足；第二交互区间[-14,22]pp含0。三项联合顺序信号须连同稳定性一起满足，现不能保留。没有修改门、追加种子、调参或因区间有利而重定判据。

## S2 实验阶段与公开证据

所有阶段重复使用的缓存只算同一数据。正文的“来源留出”指已多轮查看的50Salads50实例，不是此次首次揭盲。六新seed增加的是初始化与采样变化，没有增加原始来源。

| 原任务 | 公开证据定位 | 正文用途和边界 |
|---|---|---|
| 056 | 原严格51对的准备记录及通用小头代码 | 严格事件联接层不等同后来的133发布者QA层 |
| 060 | 133 Breakfast68/11/54、来源50、冻结特征与B0、普通扩池结果 | PUBLISHER_COMPOSITE_QA；A25来源3/2与A68的3/0为保留的负结果 |
| 061 | 输出响应、输入碰撞及字面覆盖 | 小头来源问题不敏感60%–92%；B0为22%；不是理解准确率或因果解释 |
| 062 | C/D/N×19/73，1500次真实更新 | 无关锚仅这两个seed；19例新组合子层C4/3、D5/2，非两seed均改善；0例子层EMPTY/NA |
| 063 | 六新C/D及原两seed完整顺序交叉，4000次真实更新 | 固定配方优化复验；开发seed733的C13/D11保留；81条件、14配对、2交互 |
| 064 | 公开表与三图的整理及B0回溯相等核对 | 没有新训练或评分；不追认旧封存，不增加独立来源 |

原阶段不可变公开入口：

- [060原公开摘要](https://github.com/floomeer83felix-source/vlm/blob/876ededdcaa4038363fc92f9761462c42435e41c/docs/codex-artifacts/VLM-POOL-TRANSFER-060/execution-summary.json)
- [062原公开摘要](https://github.com/floomeer83felix-source/vlm/blob/be8076782d2a813af131eff6d8dddb9fc0450e9d/docs/codex-artifacts/VLM-QUESTION-ROLE-CONTRAST-062/execution-summary.json)
- [063原公开摘要](https://github.com/floomeer83felix-source/vlm/blob/e91a6951a610c21453fac3723ef135afd603aeae/docs/codex-artifacts/VLM-ROLE-CONTRAST-REPLICATION-063/execution-summary.json)
- [064原公开摘要](https://github.com/floomeer83felix-source/vlm/blob/df50bf1c8389d20418bc56b5641f13f8f8392bfa/docs/codex-artifacts/VLM-EMPIRICAL-PAPER-DRAFT-064/execution-summary.json)

## S3 全部34个既有区间索引

以下逐条引用已验收的公开区间，未重新抽样、重新检验或选择正结果。I01–I28为14配对的答题与问题不敏感差；I29–I30为四头交互；I31–I34为六新平均差的family/seed两类条件区间。单位均为百分点，点估计及上下界保留JSON浮点原精度，不以主文两位小数替换源值。family25簇每簇2实例；单seed区间固定该优化结果；新六family区间固定六seed，seed区间固定同50实例。两轴不是联合泛化认证。

[完整聚合附件](https://github.com/floomeer83felix-source/vlm/blob/df50bf1c8389d20418bc56b5641f13f8f8392bfa/docs/papers/frozen-role-order-study/tables.json)：`replication063.intervals[0..33]`；[原始区间来源](https://github.com/floomeer83felix-source/vlm/blob/e91a6951a610c21453fac3723ef135afd603aeae/docs/codex-artifacts/VLM-ROLE-CONTRAST-REPLICATION-063/execution-summary.json)：`paired`、`interactions`和`extra_intervals`。

| 索引/JSON下标 | 条件 | 指标 | 点估计pp | 下界pp | 上界pp |
|---|---|---|---:|---:|---:|
| I01/0 | 19 D_NATIVE−C_NATIVE | answer | 26 | 12.0 | 40.0 |
| I02/1 | 19 D_NATIVE−C_NATIVE | question_invariant | -32 | -54.0 | -8.0 |
| I03/2 | 73 D_NATIVE−C_NATIVE | answer | 10 | -8.0 | 28.0 |
| I04/3 | 73 D_NATIVE−C_NATIVE | question_invariant | -22 | -32.0 | -10.0 |
| I05/4 | 137 D_NATIVE−C_NATIVE | answer | 14 | 4.0 | 24.0 |
| I06/5 | 137 D_NATIVE−C_NATIVE | question_invariant | -48 | -60.0 | -36.0 |
| I07/6 | 263 D_NATIVE−C_NATIVE | answer | 8 | -4.0 | 20.0 |
| I08/7 | 263 D_NATIVE−C_NATIVE | question_invariant | -44 | -58.0 | -28.0 |
| I09/8 | 419 D_NATIVE−C_NATIVE | answer | 18 | 6.0 | 30.0 |
| I10/9 | 419 D_NATIVE−C_NATIVE | question_invariant | -10 | -30.0 | 10.0 |
| I11/10 | 557 D_NATIVE−C_NATIVE | answer | 10 | 2.0 | 18.0 |
| I12/11 | 557 D_NATIVE−C_NATIVE | question_invariant | -30 | -46.0 | -14.0 |
| I13/12 | 733 D_NATIVE−C_NATIVE | answer | 12 | 0.0 | 26.0 |
| I14/13 | 733 D_NATIVE−C_NATIVE | question_invariant | -34 | -52.0 | -14.0 |
| I15/14 | 911 D_NATIVE−C_NATIVE | answer | 14 | 2.0 | 26.0 |
| I16/15 | 911 D_NATIVE−C_NATIVE | question_invariant | -36 | -50.0 | -20.0 |
| I17/16 | 19 D_HASH−C_HASH | answer | 8 | -2.0 | 18.0 |
| I18/17 | 19 D_HASH−C_HASH | question_invariant | -18 | -34.0 | -2.0 |
| I19/18 | 19 D_NATIVE−D_HASH | answer | 18 | 4.0 | 32.0 |
| I20/19 | 19 D_NATIVE−D_HASH | question_invariant | 8 | -6.0 | 22.0 |
| I21/20 | 19 C_NATIVE−C_HASH | answer | 0 | -8.0 | 8.0 |
| I22/21 | 19 C_NATIVE−C_HASH | question_invariant | 22 | 2.0 | 42.0 |
| I23/22 | 73 D_HASH−C_HASH | answer | 6 | -2.0 | 14.0 |
| I24/23 | 73 D_HASH−C_HASH | question_invariant | -22 | -40.0 | -4.0 |
| I25/24 | 73 D_NATIVE−D_HASH | answer | 16 | 4.0 | 30.0 |
| I26/25 | 73 D_NATIVE−D_HASH | question_invariant | -16 | -32.0 | 0.0 |
| I27/26 | 73 C_NATIVE−C_HASH | answer | 12 | 0.0 | 24.049999999999272 |
| I28/27 | 73 C_NATIVE−C_HASH | question_invariant | -16 | -32.0 | 0.0 |
| I29/28 | 19 Delta− | answer | 18 | 2.0 | 36.0 |
| I30/29 | 73 Delta− | answer | 4 | -14.0 | 22.0 |
| I31/30 | new_six_family | answer | 12.666666666666666 | 5.666666666666667 | 20.333333333333332 |
| I32/31 | new_six_seed | answer | 12.666666666666666 | 10.333333333333334 | 15.333333333333334 |
| I33/32 | new_six_family | question_invariant | -33.666666666666664 | -42.0 | -25.666666666666668 |
| I34/33 | new_six_seed | question_invariant | -33.666666666666664 | -42.333333333333336 | -23.333333333333332 |

公共随机流为Random55063的10000次共同family抽样，及Random55064的10000次seed抽样，分位数线性插值。原062区间采用其自己的Random55062流，不以063流替换旧结果。正文图2沿用原图，旧seed区间按图的源表解释；其旧两seed答题区间与原062显示值相同不意味着所有重采流可互换。

## S4 模型接口、问题视图与计算成本

每段视频12个均匀中点目标、最近时间戳帧、224RGB，处理器双帧tubelet给出6时间单元。主merger的每单元49空间token均值形成6×2560矩阵；不是DeepStack。h(q)为纯文本decoder末层最后有效位置2560维hidden，不是专门的共同检索embedding。

C原始h(q)，D原始[h(q)−h(τ(q))]/2，N原始[h(q)−h(a(q))]/2，分别以训练84条的均值向量和全条目标量RMS标准化。float64统计、float32读出，尺度>1e-8，无epsilon。τ仅从当前文本解析事件并交换；无另一格预测或标签输入。锚训练名单按UTF-8字节序去重排序；k=int.from_bytes(SHA256(b'VLM062/anchor/'+q.encode('utf-8')).digest()[:8],'big')%84，从k循环找首个非q、非τ(q)文本。这个规则不取测试标签或来源信息。

共同头356673参数：视频及问题投影64维，正弦位置、无仿射LayerNorm、核宽3残差卷积/GELU，点积注意力除以8，内容/方向/问题/乘积四项拼接MLP。BCE/AdamW，lr0.001、wd0.01、betas0.9/0.999、eps1e-8、clip1，batch8四格、250步、CPU4线程。相同seed共享真实初始state和采样；固定最后checkpoint，无验证选模。

小头缓存训练预算相同，只控制读出阶段容量和优化资源。D原始文本部署需额外τ编码，N需训练锚缓存；没有端到端等FLOPs或等时延测量。B0是完整冻结Qwen单次生成，与小头监督和输入处理不同，不是同容量对照。D seed557的6/50低于B0的7/50，不据平均数宣称全部胜出。

HASH按连续小端float32行字节的SHA256摘要和行字节本身排序，键中无问题、答案或时间编号。366个V中365个改变显式顺序；行多重集合、幂等性和4个固定置换检查已完成。该控制保留行内容、单元内运动和编码器上下文/潜在位置，不能证明所有时间信息被移除。交互只覆盖原19/73，不能外推六新seed也有同样顺序交互。

## S5 B0回溯及复现范围

064新增回溯只读核对，原060封存输出与063当前缓存计划/实际各200，逐键相等200、不等/缺失/未知0，视频/问题/索引绑定一致，原输出seal验证通过。逻辑读取9821092字节；没有读gold标签或重新评分，7/50沿用原060公开分数。本修订仅引用公开报告，未再次读取任何私有文件。回溯相等不能追认062/063原封存或认证物理来源、OS访问和预训练独立。

062科研模块和输入有事前封存，但私有监督/核验helper未全纳最初seal；063补齐科研、依赖、监督、核验代码的首次训练前封存。后期改进不填补早期历史。公开聚合和匿名family统计支持算术复核，不公开原媒体、特征或逐项预测，不能宣称完整端到端公开复现。

## S6 分版本评分与未知状态

060评分循环固定原计划N，缺项默认NOT_RUN。CLOSED且预测0/1记有效，INVALID记完成但不正确，均保留4N、2N或N分母；FAILED/NOT_RUN及其他未知增加unknown。只要条件含unknown，correct_cells、video_pair_correct、question_pair_correct、four_way_correct和相应率置NA/INCOMPLETE。配对实例若任一边unknown记unknown而非both_wrong；配对净值/区间不计算，条件不完整时主门不判。中间循环的临时correct=0并非最终unknown得分，不能脱离最后NA覆盖解释。

062/063评分实现更窄：明确要求固定键集、各格CLOSED且预测二元后才构造完整统计，碰到其他状态会停止/不能形成完整结果；它们没有定义将INVALID或未知统一转零的容错成功路径。不把060的INVALID处理反向当成所有历史版本通则。此处仅静态说明原实现，没有运行坏输入夹具或改变评分器。当前已验条件均有效，原主数值与既有区间不变。

- [060评分原源码](https://github.com/floomeer83felix-source/vlm/blob/876ededdcaa4038363fc92f9761462c42435e41c/prototypes/temporal_pool_transfer_060.py)：score/metrics中的状态检查与汇总。
- [062评分原源码](https://github.com/floomeer83felix-source/vlm/blob/be8076782d2a813af131eff6d8dddb9fc0450e9d/prototypes/question_role_contrast_062.py)：score/metrics中的状态检查与汇总。
- [063评分原源码](https://github.com/floomeer83felix-source/vlm/blob/e91a6951a610c21453fac3723ef135afd603aeae/prototypes/role_contrast_replication_063.py)：score/metrics中的状态检查与汇总。

## S7 文献与表达边界

主文使用原八条已核文献，没有新增文献网络或复现外部方法。原书目核实中七个一手入口返回摘要/元数据，Winoground的CVF入口403，沿用负责人已核简表，不声称重新读全文。正文提供完整作者简表、题目、arXiv编号或会议年份及URL，可脱离仓库阅读。未提供未核DOI，未用CRPO/EIGV/TimeBlind外部成绩作不等协议比较。

正文性能小数有意保留两位；计数、样本量和固定超参数保持原值。证据CSV保留原估计/区间并链接完整精度原JSON。三张图原样引用，图中旧标签C: centered只是标准化C的简写，不表示本稿删除RMS；原20%线和所有负区间不改。
