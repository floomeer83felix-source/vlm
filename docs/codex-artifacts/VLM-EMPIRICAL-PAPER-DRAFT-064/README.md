# 064：整理证据并完成时间问答实证论文初稿

2026-10-31（北京时间）｜ChatGPT研究负责人。**READY，唯一尚未交付新父任务；CPU_READ_ONLY_PAPER_DRAFT。** 依据[063验收与写作决策](../../research-decisions/post-063-disposition-and-paper-plan-2026-10-31.md)。安全同步文档main后，一轮完成允许的只读核对、复算/图表、完整论文正文和交付；push后STOP。无新训练/模型推理。

## 1. 读取与材料范围

完整读AGENTS、本合同、063验收和本目录[reference-brief.md](./reference-brief.md)；next-steps/overview读当前页首及064/063段，results检索本ID并读唯一060/061/062/063结果及其公开附件。确认唯一READY是本ID且无既往交付。只读056/060/061/062/063公开科学代码、科学报告/表/receipt/summary及其相关决策，补齐方法细节；必要时读057/058/059原报告说明历史停止，不重写旧证据。

公共材料以063交付e91a695及其引用的原始提交为冻结依据。正文不依赖私有特征，复算可从公开JSON/CSV和匿名family行完成。不得扫描实验根或Library，不寻找其他旧聊天/文件，不改旧表/阈值。060/061/062/063的重复缓存只算同一数据；TimeBlind未运行。

## 2. 一次窄范围B0缓存桥接，可独立失败

仅从当前明确handoff定位**063已闭合精确根**及其old-assets登记的**060精确根**，不递归扫描/猜路径。允许读取这两根必要的闭合/索引、063 cache-read/output seals、063 `all-outputs.json`与`source_holdout50-observations.json`，以及060 `pre-consumption-seal.json`、`outputs-identity-seal.json`、`all-outputs-sealed.json`、同名source observations。只核这些实际使用文件在原seal中的身份，不沿seal全表重哈希/读取。只跟随其中实际用于这次比较的精确引用，不读模型、特征、views、normalizer、头权重、计划、RGB/ZIP、标签文件。

先核原060 outputs seal登记的原输出SHA和闭合，再取其中单次B0/NA/source_holdout50的200项，与063当前缓存比较：split/index/video/question完整键、CLOSED状态和二元prediction一一相同，source observations的两视频/两问题绑定及索引对应也一致；不比较字符串显示顺序来替代实际绑定。记录本次所读文件当前身份和前后相同，仅在私有新064根保留。精确schema以旧源码/实际索引为准，禁止为了得到PASS补写历史seal。比较只需旧预测与绑定，无需gold标签或任何模型。

输出公开`b0-cache-bridge.md`仅含计划/实际200、相等/不等/缺失/未知计数、绑定检查/原seal验证状态和PASS/UNVERIFIED/MISMATCH，说明这是**064新增的回溯只读相等核对，不追认062/063原seal**。不公开逐项结果、路径/资产hash/问题文本。若原文件/注册/身份/预算不支持，明确UNVERIFIED并停止这一子项，**继续公共表和论文**；不修复/重跑旧B0。MISMATCH不挑选200项或写回旧文件。只有PASS才可把B0单次7/50作为已核缓存锚；否则主图不画B0线，正文将其移至带限制的历史说明或省略。主C/D结论不随此改变。

## 3. 公开复算、关键表和三张图

写可独立运行的`prototypes/empirical_paper_064.py`，公共模式只读公开材料、stdlib和可选现有Matplotlib，不导入torch或被测模块。桥接模式只接受显式精确旧根，单独入口，不自动由公共模式触发。公共模式重建63的81条件/14配对/2交互/34区间，核350family边际、固定六新/八合并汇总及原门；分别Random55063/55064、10000公共抽样、线性分位数与063一致，不能重写历史062的随机流。另将060/061/062必要聚合锚、062开发54的覆盖子层和8seed开发54结果纳入`tables.json`。没有新增显著性检验或事后子层搜索。

所有论文数值必须由这些源表/公式定位；每张表标明来源、实例分母、seed阶段与缓存。新六source C均值2.5/50＝5%，D53/6/50＝17.6667%，配对差12.6667pp，6/6正；**未过20%绝对目标是摘要、结果、讨论、结论共同保留的主结论**。合八D10.125/50不可救门。两个mean区间分别固定seed重采family、固定实例重采seed，不宣称联合认证或N300独立。所有14/2/34正负结果在附件表保留。

用现有Matplotlib/Agg生成三张标准科研图，各SVG＋PNG，英文图内标签可避免字体安装，中文完整图注写正文：

1. `fig1-seed-accuracy`：全部8seed C/D四格全对率，标旧2缓存/新6；标20%固定目标与新六均值17.6667%。B0仅桥接PASS时作单次14%参考，不给其多seed误差条。
2. `fig2-paired-intervals`：全部8seed来源D−C点估计及各family95%区间；另外明确分组标新六均值的family区间和seed区间、0线和pp单位，保留含0/负下界，不把两类不确定性混在一根误差条。
3. `fig3-role-order`：原19/73完整C/D×NATIVE/HASH四柱及各Delta/95%区间，展示seed73含0。HASH保留内容/内部时间线索写入图注。

图由聚合值程序生成，不用imagegen、不手写数据、不造误差条。检查SVG可解析、PNG尺寸和标签/轴/图例/截断，能用现有工具打开就逐图目视；若没有图形查看能力，明确只完成结构检查，不能写已目视。Matplotlib缺失不得安装，完成表/正文并报告FIGURES_NOT_GENERATED及PARTIAL，不让图形依赖阻断其他写作。路径须可从manuscript相对打开。

## 4. 交付完整正文，不交提纲

`docs/papers/frozen-role-order-study/manuscript.md`暂题**《冻结特征时间问答的角色差分与顺序效应》**。目标正文约6000–8000中文字符（不含表/参考文献，报告实际计数，不为凑字重复），中英文摘要和关键词、引言、相关工作、方法与数据/统计、结果、讨论/局限、结论、参考文献齐全，有连贯论证和公式/表/图引用。作者单位/基金只可标“待作者填写”，不得编造；主体不可用待实验/TODO代替实际结果。普通实证稿定位，不能保证任何期刊录用，未经用户授权不选刊投稿/联系编辑。

必须讲清以下细节与边界：

- 冻结Qwen3-VL-4B-Instruct，12帧均匀中点224RGB形成6tubelet、每49空间token均值的predecoder主merger特征V[6,2560]；q是纯文本decoder最后有效位置末层hidden[2560]，不是专用多模态embedding，同维不等于天然对齐，不用DeepStack替代。
- DyBench固定revision `fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405`的**自建开发划分**；PUBLISHER_COMPOSITE_QA：133Breakfast→68/11/54（25/4/20组）＋50Salads50（25文件family×2），不是官方零样本测试/两个独立新基准。不能把文件family当已验证参与者/厨房，物理/转码独立及预训练未知；旧51严格事件核验层与133发布者QA层不同。50来源已多轮查看，六新优化种子不是新来源确认。
- 清楚定义四格/单项/视频对/问题对/四格全对和问题不敏感；CONSTANT与VIDEO_ONLY的合并不是理解正确。四格指标与配对构造已有先例，不申报原创。主推理每次当前V/q，无读另一格预测/标签或强制互补。
- C与D的原始视图分别h(q)、(h(q)−h(tau(q)))/2，再各自train84的mu与标量RMS；tau由当前文本交换角色，normalizer固定。N无关训练锚差分仅062两seed作负对照；不是新六也跑了N。D冷启动需额外文本编码，不把CPU缓存训练等价于端到端同成本。
- 同356673参数A头、BCE/AdamW、batch8四格/250步、lr.001/wd.01/clip1/CPU4线程、同seed共享实际初始state/采样序列，固定最后checkpoint。种子同时改变初始化/采样，不把效果只归一者。062/063分别1500/4000实际更新，不把旧缓存当新训练。
- 061来源问题交换不敏感、字面事件名称未见为背景；062开发新组合19例不是两seed均改善，063开发54有seed733负值，不能仅报来源最强结果。062两门通过与063新门绝对项失败并列，事前目标是项目投入阈值，不是社区通用有效性/显著性标准。
- 原2×2 D顺序净+9/+8、Delta+9/+2，各N50，第二Delta区间[−14,+22]pp；不能证明纯时间编码量、问题定位、一般机制或因果层。结构/差分本身无新算法认定，不用已有方法CRPO/EIGV/TimeBlind的公开分数作不等协议比较。
- 公开代码与聚合量/匿名family统计可复算；原媒体、特征和逐项预测未公开，不宣称完整端到端公开复现或新增人工核验。062私有helper初始seal缺口、063补齐范围、B0当前桥接结果如实写入可复现性/局限简段，不让操作审计淹没科研主线。

`evidence-map.csv`逐条列论文主要主张的claim_id/段落、原提交+相对路径+JSON字段/CSV行条件、分母、旧/新阶段、估计/区间、允许措辞及不得外推内容。覆盖摘要所有数值和每张表/图；无原始逐项数据。

`references.md`按reference-brief的一手来源形成编号一致的核实文献表，记录作者/题目/年/会议或预印本/URL/支持范围与未运行对照。可只使用已核材料，不新增查新任务；如能只读公开一手页面核元数据允许，总≤12页，不下载PDF/数据或调LLM/API。不编DOI/页码/会议信息，文内引用与表逐一对应。相关研究不是本项目实际复现过的对照。

`submission-readiness.md`给出可支持的最窄贡献、尚欠的独立验证/有限数据/方法新意等主要缺口、正文/图/文献自检结论及下一篇幅修订重点；只提具体缺口和后续可选研究设计，不实际运行新实验或为了达标继续调当前配方。

## 5. 边界、核验和成本

公共复算/图形生成累计监督外层≤300秒；B0旧元数据/输出逻辑读取≤16MiB、监督≤60秒，达到边界则桥接UNVERIFIED。新的064私有输出根≤64MiB/128文件，RAM≤4GiB/active-process≤4/CPU线程≤4，起始free≥128MiB；父≤10800秒含写作。只监督自有进程/现有040 runner，不杀其他Job、不删旧锁/账本。无torch/测试头导入、特征重算、训练或LLM/Qwen/encoder/processor/tokenizer、GPU/nvidia-smi、媒体/RGB/ZIP、研究数据网络、安装/环境变化。原表/schema差异用静态核对，禁止重跑闭合实验。

新代码/图生成与桥接核验代码及预算在首次相应读取/运行前记录身份，闭合后核前后；报告排版修改独立记录。写作编辑不算研究重试；桥接发生MISMATCH/缺失不重新生成旧预测。私有精确根只经handoff登记，无合法根则不找。保留逻辑读量/外层时间/OS或物理I/O未知的区别。

独立复核不得import公共生成脚本或被测模块，只从原公开源另算所有摘要/图数据/门/34区间，核表与正文/英文摘要/证据表逐数一致、图文件/链接/文献对应、负结果与限制齐全；B0桥接私有核验仅比较旧输出与绑定，公开仅汇总。工具能力不足如实PARTIAL，不伪称视觉或私有审计完成。提交前准确统计公共文件大小和allowlist，敏感内容检查不靠某个关键词PASS代替人工审阅。

## 6. 精确16处交付并停止

仅新增以下15处文件并向results追加一次本父结果（图形依赖不足时缺图须明确列NOT_GENERATED；不建伪图）：

1. `prototypes/empirical_paper_064.py`
2. `docs/papers/frozen-role-order-study/manuscript.md`
3. 同论文目录`evidence-map.csv`
4. 同目录`references.md`
5. 同目录`tables.json`
6. 同目录`submission-readiness.md`
7. 同目录`figures/fig1-seed-accuracy.svg`
8. 同目录`figures/fig1-seed-accuracy.png`
9. 同目录`figures/fig2-paired-intervals.svg`
10. 同目录`figures/fig2-paired-intervals.png`
11. 同目录`figures/fig3-role-order.svg`
12. 同目录`figures/fig3-role-order.png`
13. 本任务目录`b0-cache-bridge.md`
14. 本任务目录`execution-receipt.md`
15. 本任务目录`execution-summary.json`（复算/桥接/图形/正文状态、数值/门一致性、独立核验、字符数、计时/读取量和未知）
16. `docs/codex-results.md`仅一次append

不得改本README/reference-brief、AGENTS、规划、旧代码/交付，不上传原QA/事件文本/标签/逐项预测或正确性、资产hash/私有路径/源映射/特征/权重/媒体。原公共科学源码自身LF SHA可报告。普通安全commit/push main后STOP，不自动065或提交期刊。负责人验收同回合下达下一具体工作。
