> **ARCHIVED / 060_CLOSED / 不可执行（2026-10-31）。** [876eded交付](https://github.com/floomeer83felix-source/vlm/commit/876ededdcaa4038363fc92f9761462c42435e41c)已由[负责人验收](../../research-decisions/post-060-pool-transfer-disposition-2026-10-31.md)：带两次调用前软件检查修复的完整比较，1000真实更新、6056项均有效；来源A25=3/2、A68=3/0、P1_68=5/4、B0单次7，各N50，主门FAIL。停止此扩展配置，当前0 READY；不重跑、续额度或自动061。以下原合同和启动文字仅作历史保留，不构成新授权。

# 060：训练池扩展与50Salads来源留出基线

2026-10-31（北京时间）｜ChatGPT研究负责人。**READY，唯一新父任务；尚未执行。**

新指令下的一体任务：输入/媒体/冻结特征、4个CPU训练、缓存基线与新来源评分连续做完再交付。不拆准备父任务，不恢复057/059机制，不新增模型结构或环境。GPU仅在用户本轮明确授权本包后运行。

## 1. 问题、证据等级和读取

检验**扩展后的发布者标签训练池，能否改善普通基线的来源留出表现**。主模型为原普通A，P1为已知一阶对照，均不作新算法贡献。旧25训练与新68训练包含关系固定，更新数相同；训练量/覆盖/验标策略同时改变，结果不是数据量单因果效应或旧机制复活。方法/证据变更说明见[重置决策](../../research-decisions/post-059-data-regime-reset-2026-10-31.md)。

安全同步独立文档仓库main，完整读AGENTS、本README及重置决策；next-steps/overview仅读最新页首与060/059段，results全文检索060并读056/057/059唯一条目。确认唯一READY且父ID未交付。读旧056数据/小头、057运行/抽特征与059 PairHead/P1的相关实现，旧源码和合同不改。

只从既有运行登记/handoff取得精确056/057/059私有根、现有本地Qwen3-VL-4B-Instruct及conda pytorch路径，不递归扫无关目录。旧根只读；读取已闭合的元数据、原身份join、输入/特征/初始计划/最后权重/预测及各seal。文本I/O显式UTF-8（旧带BOM登记可utf-8-sig）。缺关键旧资产或STARTED未闭合则BLOCKED，不重新下载、重训旧模型或通过新ID重试历史调用。

## 2. 固定133+50数据配置

固定DyBench revision `fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405`的原事件JSON（388049B/814行），从旧055/056已闭合副本读取，研究数据网络请求0。对Breakfast/50Salads按原文件名original/reversed配对，原问题相同、事件解析同056，以下条件全部满足：两事件经仅下划线转空格/折叠空格后不同；固定两个选项、互补发布答案、两视频各唯一；记录名/来源字段匹配。

Breakfast须133对，排除名义147中的9对同事件及5对记录编号不合格；**逐项**与旧056 source-table的133条原记录join对齐，包括原记录、participant、camera与group_key，不能只对数量。使用原`SHA256('VLM055/'+group_key)`首8hex mod10：0..5训练、6验证、7..9开发，**本轮取全部133，不沿用旧48开发cap裁样**。必须得到68/11/54及25/4/20组。原057的25/2/24及所有视频、问题、四格标签须分别是这三池的精确子集，旧训练25全部进入新训练68；参与者组跨池无交叉。

50Salads固定全部50对/100视频，匹配`rgb-NN-[12].mp4`与反事实版本，25个NN family各两试次。全部只作`source_holdout`，不训练/选参/改配方。此分组证据为`FILE_FAMILY_CLUSTER`；官方页说明25人各两次，但未取逐项编号说明，不写成已验证participant join。不得因媒体/模型失败删实例或改变50的分母，任何资格/成员/身份不一致报告UNKNOWN/BLOCKED。

q0/q1严格用056原模板和**原始事件字符串**（归一化只用于事件不同检查）：`Does the event "A" happen before the event "B"? Answer Yes or No.`及交换A/B。标签取发布者original顺序并按视频/问题各交换一次翻转，四格绑定在任何新模型调用/更新前封存；不按模型分数选样，不看TimeBlind。

新QA证据级别为`PUBLISHER_COMPOSITE_QA`，来源身份与QA真值分开记。[作者论文v2 Appendix A.2](https://arxiv.org/pdf/2605.21988v2)给出两动作片段拼接及人工检查说明；不再要求动作在未剪辑原长记录中只出现一次。没有逐成员剪接manifest或本项目逐帧复核，不把其等同旧51对的逐事件验证，也不改055/056历史门。50Salads是同一DyBench管线内的来源留出，不是独立新benchmark、物理来源独立证明或未见预训练数据。

准备角色可读发布答案做绑定及投影来源；训练角色只读train68标签、无标签输入/原计划，不读任何验证/开发/50Salads标签、旧或新B0预测/正确性或源组。评分在所有输出封存及训练Job actualactive0之后。程序/文件角色分离不认证OS无访问。

## 3. 媒体与已有缓存复用

只用057已下载`event_sequence_zip.body`（2,783,546,023B），允许本轮一次流式SHA核对旧发布内容SHA；不发新GET/HEAD/Range/续传。旧媒体/帧/特征不覆盖。ZIP全局安全目录检查≤4096条/16MiB、无路径穿越/链接/加密/重复路径，压缩类型及ratio沿用056；按封存183对的366个唯一视频名映射实际成员。

旧51对的102份V、54份q与对应RGB/processor/model identity闭合复用；这些输入不重新解码、抽特征或生成B0。只提取/解码新增**264个成员上限**，单成员≤64MiB、额外解压总≤2GiB、ratio≤100。成员唯一、完整大小/CRC一致；缺失/冲突不换样。所有路径及身份hash私有。

CPU解码沿用057的12个全时域均匀目标、最近PTS、uint8[12,224,224,3]及CFR/index-clock一致性规则；动作标注边界不作采样输入。总解码≤500000帧、外层≤1800秒，已有旧帧不重跑。使用现有PyAV/NumPy/processor，不装ffmpeg/新依赖，不作新剪接或手工标注。新输入准备要在GPU前完成，不能用模型重试探测帧格式。

在新Qwen调用前，将全部Breakfast/50Salads媒体内容SHA和完整12帧RGB身份作跨来源碰撞检查；旧102项用已闭合身份，不重复解码。若有跨来源完全相同内容/模型RGB输入，记`SOURCE_INPUT_COLLISION/UNKNOWN`并停止本队列，不删冲突项后改分母或把旧输入当新来源。未发现精确碰撞不证明没有转码/裁剪同源。来源内部的相同输入可复用特征，逐对重复/退化数量照实报告且保留分母，不以此清洗难例。

CPU processor/local tokenizer核12帧→grid[6,14,14]、pixels[1176,1536]、文本≤128有效token及原模型/配置/权重/tokenizer/代码身份。必要的原权重文件哈希核对计入其他CPU预算，不作完整旧目录复制。新root≤8GiB/4096文件，初始free≥10GiB。

## 4. 单次冻结Qwen GPU阶段

仅用户在本轮明确授权本包时执行：**一次真实Qwen加载、GPU外层≤1800秒、allocated峰≤18GiB、JobRAM≤32GiB、active-process限4、单块3090且free≥18GiB**。用既有互斥锁/持久调用账本和监督器，留出卸载时间；不删旧锁、杀他人进程或重置包络。原057模型/config/tokenizer及抽特征定义必须一致，不允许新模型替代或环境修改。

高层调用最大**776=264新V+312新q+200 B0**，分别也受该子上限约束；任何重复的RGB/纯文本实际输入先查闭合cache并复用，历史STARTED未闭合不重试。不能仅改模式名/ID包装同一旧输入为新调用。旧54问题是183对×2＝366个问题槽（去重前）的字符串集合子集，新去重纯文本问题≤312。记录实际调用数、缓存/alias、根forward/视觉encoder/decoder层计数，不相加混淆。

torch.no_grad/eval/全部Qwen参数冻结，主模型backward/optimizer0。新V仍取主视觉merger、decoder前、6×49×2560仅空间均值为[6,2560]，不新取层/deepstack/更高分辨率；新q取纯文本最后有效token的最终hidden[2560]，CPU float32落盘。形状/有限性失败不退化或另找层重试。

B0只评估50Salads的200个视频×问题cell，每项greedy/max_new_tokens8，严格完整Yes/No可带句点；INVALID原样保留分母且按错计，不能改prompt重生成。沿用057 native video/time metadata、12帧原输入；B0 key含RGB、q、fps/indices/duration/total_num_frames及模型/processor身份。输出私有封存，CPU训练角色不得读取。一次B0不因两个seed重复；不重跑旧Breakfast B0。结束核主模型无grad、卸载/active0后才CPU训练。

## 5. 4个新训练与冻结旧基线

四个方法各两个seed19/73：A25为057普通A末期权重，P1_25为059 P1末期权重，只冻结复用；**A68/P1_68**为本轮新训练，均356673参数、原架构不变、BCE only。

A68实际初始state取原057 pretrain，P1_68实际初始state取原059的映射初始state并核其等于原conv切片/MLP映射；分别必须与A25/P1_25训练时使用的初始state逐项一致。不得从旧最终权重继续训。每seed新sequence固定为`torch.randint(68,(250,8),generator=torch.Generator().manual_seed(seed))`，两架构共享；不把旧n25索引误作n68计划，不重抽计划。封存新sequence和初始化、核68均被覆盖，无依据结果重采样。

顺序seed19 A68/P1_68，再seed73 A68/P1_68，各250真实forward/BCE/backward/AdamW step，合计**1000**；每配置8四格/32cell、2000组/8000cell曝光。AdamW lr0.001/wd0.01/betas(0.9,0.999)/eps1e-8，clip1、CPU float32/线程4，最后checkpoint。每步STARTED→有限loss/每个参数grad非None且有限→step→CLOSED；不调参/早停/挑seed/增加更新。旧056可复用A/pack/optimizer；059只复用PairHead('P1')/predict，不运行旧main/训练或R臂，也不修改旧源码。

旧A25/P1_25 checkpoint及其实现哈希前后不变，旧模型research updates0。没有新软件fixture优化/暖机forward/额外反转检查；复用原已验实现，只做数据/状态/映射静态核对，实际新头forward只用于250步和正式预测。新Qwen调用前应完成必要的无模型/无优化输入、状态、计数和封存检查；可用不含真实QA的整型fixture核33/10表及6056守恒，不计成研究结果。新训练模型变化/loss为执行证据，不能替代来源留出收益。

## 6. 缓存预测、统一评分和固定门

8个训练后头在所有133 Breakfast及50 Salads上各独立单V/q预测：各183×4=732cell。旧A25/P1_25对原51的**816个**闭合预测按视频/q/参数/特征身份精确映射复用，不以新索引名重forward；其余**5040个**小头cell为新预测。加单次B0 200，正式总**6056=816缓存+5040新小头+200新B0**。没有配对答案修复，推理只接受当前V、q和固定已训练模型。

输出/所有旧新checkpoint/特征/代码身份全部封存，训练Job actualactive0之后评分。33条件行：4方法(A25/P1_25/A68/P1_68)×2seed×4split(train_pool68/validation11/development54/source_holdout50)=32，另B0/NA source_holdout1。每行有training_pool_n（25或68；B0 NA）、原N/cell、cached/new计数、正确/视频对/问题对/四格全对及INVALID/FAILED/NOT_RUN/unknown。

`train_pool68`是统一评估池，旧25模型对新增43例没有训练过，不能把此行都叫旧模型训练准确率。development54含已使用的旧24，不称新确认集。JSON另核原51的旧缓存子集所有指标复现057 A及059 P1；原新25/68评价差异不挪改历史表。

B0 INVALID为已生成但严格格式不合格、按错计并留分母；complete_cells包括有效和INVALID，valid_cells另列。FAILED/NOT_RUN/无法判断为未知、保留计划分母、科学门UNKNOWN，不把未知当错抬高对照收益；完整但有B0 INVALID可评分，披露其数量与解释限制。没有按预测结果删题。

10行source_holdout配对：每seed下A68−A25（主）、P1_68−P1_25、A68−B0、P1_68−B0、P1_68−A68（后四均次要）。列左右独对/都对/都错/unknown及净实例、百分点、组bootstrap区间。单次B0对两个seed共享，不扩大独立N。

**完整主投入门**：A68两seed各四格≥10/50，且对A25各净增≥4/50（8个百分点），两seed A68对单次B0的平均差>0。全满足记`A_POOL_EXPANSION_TRANSFER_SIGNAL`，否则完整比较为`NO_PRIMARY_A_TRANSFER_SIGNAL`，不完整为`INCOMPLETE/UNKNOWN`。P1次要好结果不替代预先指定A主门，也不作新贡献；如实保留，不据此重选主方法/seed/超参。

每配对按25个编号family有放回等概率抽25组，组内两个实例全取，以实际抽样N为分母；10000次、每比较重置`random.Random(55060)`，原family key字典序，2.5/97.5%线性分位。公开250行匿名来源family×2seed×5比较的n、左右独对/都对/都错/unknown/net，便于负责人复算。此为文件family聚类，不冒认官方participant/厨房独立。该门在新来源结果出现前固定，但只有一个原始来源留出、共享DyBench构造，不能作大样本/独立benchmark或样本量单因果证明。

无论门结果，不恢复I/R1、调损失或换头续搜。未过停止这次普通A扩展配置，不宣称所有特征无时间信息，也不掩盖P1的预定次要结果；通过只说明此配置值得进一步确认，后续新机制仍须胜普通基线及新数据验证。TimeBlind保持NOT_RUN，不自动061。

## 7. 预算、封存和失败

父elapsed≤10800秒；CPU解码≤1800秒/500000帧、其他准备/身份/静态/独立核验CPU外层累计≤900秒、CPU训练＋小头预测＋评分≤1200秒/JobRAM≤8GiB/线程4；GPU限额见§4。checkpoint/初始计划副本≤32MiB，新root≤8GiB/4096文件、起始free≥10GiB。网络研究数据请求0，只有Git文档同步；无环境安装/升级/新模型/手工标签/付费API/云GPU。

首个新Qwen调用或研究配置STARTED（较早者）前封存全部输入/代码/计划/门；后续不得改采样/特征定义/模型/训练或评分公式来适应结果。修复仅限这个首次消耗前，修后重封代码；已开始配置/输入失败或中断不恢复/改名重试。持久账本、累计计时和进程监督先行，所有自有Job收尾核actualactive0/no kill，不动他人锁/进程；不隐藏准入/解码/输入失败，不自动续父任务。

输入身份/133↔旧join/68嵌套关系/50成员/磁盘/锁条件不满足即BLOCKED，输出完整计划33/10表且准确率NA/UNKNOWN，不发起GPU。正式阶段失败也保留完整计划分母/NOT_RUN，不能因合同允许批量而另开替代训练或下载。

## 8. 八处交付并停止

1. 新`prototypes/temporal_pool_transfer_060.py`，显式准备/训练/评分入口，导入无I/O或训练。
2. 新`prototypes/temporal_pool_runtime_060.py`，显式CPU/GPU运行入口，导入不加载模型/初始化CUDA。
3. 本目录新`execution-receipt.md`。
4. 本目录新`scientific-results.md`。
5. 本目录新`condition-summary.csv`（33行）。
6. 本目录新`paired-summary.csv`（10行）。
7. 本目录新`execution-summary.json`（数据证据/身份范围、表/250来源行、缓存/新输入/1000步/资源/代码SHA及限制）。
8. `docs/codex-results.md`仅追加一次`### VLM-POOL-TRANSFER-060`。

独立复核从新封存文件核133成员对旧join、所有四格/68嵌套/来源分组/标签绑定、旧输入/预测/权重闭合身份、初始化和新计划/1000步、各缓存/新调用数、6056守恒、33/10表和250组bootstrap、资源/失败。可以只读CPU torch状态但不重复forward/训练、解码或调用Qwen，不靠执行被测scorer算独立；未重做的项目写UNKNOWN。短复核代码可内嵌回执。

不公开媒体/帧/特征/权重/checkpoint、QA/答案/逐题预测或正确性、真实源映射/数据身份hash/私人路径。只传代码hash和聚合匿名统计。README、AGENTS、负责人规划/决策/旧协议、历史代码/报告不改。只stage八处允许文件，一次普通安全push后STOP，不自动061或后台继续。

## 9. 发给本地Codex

```text
执行VLM-POOL-TRANSFER-060。安全同步main，读AGENTS和060 README，确认唯一READY且未交付。
按新发布者拼接QA证据配置，核Breakfast68/11/54及旧25训练嵌套，留出50Salads50对；复用已有ZIP/特征/旧模型，不新增媒体下载。
授权本包一次冻结Qwen GPU阶段≤1800秒/allocated≤18GiB/高层调用≤776，只处理新增输入；随后A68/P1_68×seed19、73各250次真实CPU更新，共1000步。旧A25/P1_25冻结复用，完整比较新来源四格收益。
输入、特征、训练、封存评分和复核一轮做完，不调参/重跑旧输入或恢复I/R1。按README八处脱敏交付并推送main后停止。
```
