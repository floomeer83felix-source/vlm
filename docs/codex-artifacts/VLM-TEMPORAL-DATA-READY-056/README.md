# 056：真实事件数据就绪与时间问答小头实现

2026-10-30（北京时间）｜负责人ChatGPT；本地Codex执行。
父任务：**VLM-TEMPORAL-DATA-READY-056**。
状态：**READY / AWAIT_EXPLICIT_USER_START**。

本包由用户“给出下一指令”新立项，专门解决[055验收](../../research-decisions/post-055-input-stop-disposition-2026-10-29.md)的媒体打包/限额不匹配、原来源映射未实算及小头未实现三项问题。不是重跑055，不沿用旧预算，也不是已经通过数据准入的训练任务。**本轮GPU、Qwen权重加载、模型特征抽取及真实研究训练均0。** 用户发送第8节启动指令后，才激活本包具体下载、CPU解码和实现验证权限。

交付目标是可追溯的真实媒体/分组/12帧输入及可用的小头代码；不是再证明“接口toy能跑”。数据部分失败不应阻止独立的小头实现和必要软件验证，统一回报后停止。

## 1. 开始与读取范围

安全同步独立文档checkout main，完整读取AGENTS、本README、[055冻结方法](../../research-protocols/question-conditioned-temporal-learning-2026-10-29.md)、055验收及055执行回执。对next-steps/research-overview读取页首当前状态和056任务相关段；对results检索唯一056父ID、完整读取055结果。三大文件其余历史仅为背景，本包不要求全文重读它们；这是对055阅读负担的明确范围修订，不回写其历史记录。

确认唯一未交付READY为056；同ID已有completed/partial/blocked结果即不执行。干净文档checkout才可快进，不reset/rebase/强推或丢弃变更。公共文档仓库与原Windows实验目录保持分开。

沿当前会话已明确的私有输出父目录新建vlm-private-056，独占创建、不覆盖已有根。准确入口缺失时一次性说明缺项，不扫盘/猜路径/恢复回收站。只读准确已知的关闭055根中以下公共数据副本：dybench_annotations.body、dybench_revision.json、dybench_file_sizes.body、dybench_readme.body、timeblind_revision.json、qualification.json、network.jsonl。每文件≤2MiB、合计返回≤8MiB；timeblind仅沿用版本事实，不重开其QA。055原目录、账本和结果不改，不运行其脚本或重新发已完成的055请求。

055入口确实不可用时，可以在056新的元数据预算内从同固定revision各取一次所缺DyBench公共文件，记录为新父必要获取，不能冒称旧预算续用；不要求为找旧根停止所有独立实现工作。

## 2. 先闭合来源映射和候选划分

本次主数据候选限定DyBench的**Breakfast子类**。其余三子类只计排除规模，不凭未核实的名字混入主训练/测试，不自动切换其他数据集。

DyBench固定revision：`fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405`。允许的新增公开入口：

- [DyBench](https://huggingface.co/datasets/ddz16/DyBench)该revision的README、json/event_sequence.json、固定对象文件元数据/大小/发布SHA256及video/event_sequence.zip。
- [Breakfast官方说明](https://serre.lab.brown.edu/breakfast-actions-dataset.html)及其链接的[官方分发页](https://huggingface.co/datasets/Serrelab/breakfast-actions)：先固定仓库revision，只读README、SHA256SUMS、provenance说明和segmentation_coarse.tar.gz/segmentation_fine.tar.gz。
- 官方页面直接链接的[HTK仓库](https://github.com/hildekuehne/HTK_actionRecognition)中README及明确用于命名/参与者划分的短文本/列表；不运行其代码、不安装HTK或访问其特征/原视频外链。
- [CRPO论文附录A.2](https://arxiv.org/html/2605.21988v2)的Breakfast两片段交换构造说明；仅公开文本。

本包不下载breakfast_data.tar.gz（它是Fisher特征，不是RGB视频），不取原Breakfast视频、不访问Google Drive/Dropbox，不取DyBench其余两个ZIP或TimeBlind媒体。

先校验055公共标注副本的固定版本/结构计数，保存只属于056的新身份封存。379/28是旧结构检查结果，不直接当合格/不合格训练数。保留固定二事件解析规则；在新映射中逐项列出可追溯、歧义、无匹配等原因，不在看到模型效果后修解析。

从官方原标注/列表建立“DyBench Breakfast成员→原录制记录→参与者及机位”的可审计对应：仅用公开有依据的命名规范和唯一对应，不只截取一个P前缀便宣布认证。允许机械地去交换后缀、标准化扩展名/相对路径分隔符，以及按官方约定转换机位/动作名；任何有歧义的对应保留UNKNOWN，不凭语义猜测或人工新标注补齐。原事件标签存在性、重复实例、时间单位与严格非重叠资格也要核实；不能从相同单词推断准确的事件边界。

可接受的证据等级为**官方原标注唯一对应＋发布构造说明（ANNOTATION_JOIN）**，报告归因边界；它不是逐像素鉴定或世界范围物理独立证明。按参与者合并其全部活动/机位/交换版本，至少防止同一原录制及已知多机位跨split。厨房是否独立若未知单列，不冒充跨厨房独立评估。

组键固定为`Breakfast/participant=<官方参与者标识>`，哈希`SHA256("VLM055/" + group_key)`，取首8个十六进制转整数mod10：0..5训练、6验证、7..9开发测试。各split按完整hash升序纳入整组，加入将超过上限则跳过整组并记录；不拆组凑数。上限train96/validation16/test48四格实例，最低64/8/32，test至少8个参与者组；不换seed/比例或借其他子类凑门。

在申请大ZIP正文前先实算映射及上述候选数量。若来源/最低量不成立，不为形式进展下载2.78GB；数据记SOURCE_OR_SIZE_HOLD，继续独立的第5节实现。若成立，封存候选/版本/来源/排除和下载计划，再执行第3节。该候选还不代表正式训练输入已合格。

## 3. 一次获取实际存在的事件ZIP

**本包特许整包获取这一个已知事件对象**，替代055不兼容的单对象64MiB限制；不是下载整个DyBench三任务库。对象地址：

`https://huggingface.co/datasets/ddz16/DyBench/resolve/fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405/video/event_sequence.zip`

055记录大小2,783,546,023B，约2.59GiB。正文GET前必须从固定版本官方对象元数据取得并封存精确大小和**内容SHA256**；区分LFS内容SHA、Git blob SHA、Xet文件标识及ETag，不把它们混用。身份或大小与已知对象不符先停止媒体获取，不换revision。不能只有本地自算SHA便宣称与发布者内容相符。

- 新元数据/说明/两个小标注包的累计下载正文≤16MiB，包含重定向/失败正文；小标注包解压总量≤64MiB。
- 事件ZIP媒体传输正文累计≤3GiB，包含失败/重定向正文；最终成功对象正文必须恰为2,783,546,023B并匹配发布内容SHA256。
- 一个最终媒体正文GET尝试，不自动重试、断点续传、Range或200/206回退；HTTP重定向最多5跳，只跟随固定官方对象响应链，不转发凭据、不绕过登录/许可。
- 传输outer≤3600秒、connect≤30秒、单次无进展read≤60秒，流式读取/写盘，禁止全ZIP驻留内存。提前持久STARTED、实际正文计量及终态；异常保留partial和实际已耗量，不另开任务花余额续传。
- 新根写入前磁盘free≥10GiB；整个056输出≤8GiB/4096文件，不复制多份大ZIP。此额度覆盖ZIP、选中成员、帧和小文件；不再沿用055的3GiB总输出上限。

用既有stdlib zipfile只读检查中央目录、压缩方式、重名、加密、路径穿越/绝对路径/链接风险、声明大小及CRC；目录≤16MiB、条目≤4096。不直接extractall；只提取候选清单的成员，精确唯一匹配，单成员解压≤64MiB、选中成员累计≤2GiB、解压/压缩字节比≤100。压缩/解压计量同时受限；选中对象必须完整读取并通过CRC。不能把ZIP目录可读当媒体正确，也不要求解压未选中的三百余对。

若候选成员缺失、超限或不唯一，保留完整计划/失败，不按文件大小换组补齐。完整性失败不启动CPU解码；仍继续独立小头实现并交付已有数据状态。

## 4. 真实输入准备与交接

通过媒体完整性后，用现有PyAV进行有界CPU解码；不安装ffmpeg/新依赖。每视频完整已发布片段分12个等时间bin，取各中点最近的合法帧，统一224×224 RGB。保留真实时序，不借标准答案/原标注截取事件或选择画面，不复制一个帧索引补成12个时点。单视频失败保留状态，不换题。

CPU解码累计outer≤1800秒，单Job RAM≤16GiB/线程≤4，累计实际解码帧≤500000；不保存全帧流。每个视频保存一份uint8[12,224,224,3]数组（单份payload1,806,336B）及采样时点/原索引/容器时间基/内容SHA。重复请求复用本父闭合缓存，所有新文件只在056私有根。

冻结四格问题、原标签绑定、来源组、划分、成员和缓存身份；训练标签与验证/测试标签分文件，后续训练角色仅得到训练标签。准备者本轮可为完整性核验读发布标签，但不接触模型效果；角色隔离不是OS审计证明。原标注时间、参与者/来源ID、文件名及original/reversed标记不进入模型输入。

公开只报匿名规模及各类失败，不上传原始QA/标准答案/逐成员身份或缓存内容。交接分别列明SOURCE_MAPPING、SPLIT、MEDIA_HASH_CRC、FRAME_CACHE、HEAD_IMPLEMENTATION、FEATURE_RUNTIME，不能用一个PASS掩盖未验证项。

只有候选最低量、完整来源隔离、全部选中媒体/缓存、HEAD_IMPLEMENTATION及独立复核都通过，才标DATA_AND_HEAD_READY；Qwen特征/tubelet/实际forward仍**FEATURE_RUNTIME_UNVERIFIED**。有失败则DATA_PARTIAL_OR_HOLD，不清洗后冒称完整数据通过。此状态不授权下一GPU任务。

## 5. 独立完成A/V/S/I小头代码

无论第2至4节数据是否成功，本节在本父剩余CPU预算内继续。实现新prototypes/question_temporal_056.py，完整复用[055冻结方法第5至7节](../../research-protocols/question-conditioned-temporal-learning-2026-10-29.md)的r=64架构、L_BCE/L_video/L_joint、S分组方式、seed19/73、共享初始化/采样、固定AdamW及每配置250步设置；不改原文件或用不同参数填充同参。

训练/评估入口必须可显式调用，支持未来真实冻结特征、持久步骤/失败、最后检查点和单格推理；`import`不得自动下载、加载模型、训练或访问数据。推理函数只接当前(V,q)，不接配对键、其他格预测、源ID或标签。未被真实模型验证的Qwen接口必须标明，禁止靠合成feature验证声称实际抽取可用。

实现新prototypes/question_temporal_data_056.py用于本父来源join、固定划分、单对象获取/封存、受限提取、CPU采样、分文件handoff及独立核验入口；不能调用055主程序或修改旧脚本。必要时只读现有040平台Job/Process纯helpers以沿用Windows监督，不执行其main/tests。

在现有conda pytorch的CPU进程，以自有数值fixture验证参数数、A/V/S/I初始化/曝光一致、S每logit恰用一次且不改标签、联合损失不等同CE、梯度有限/真实参与参数可更新、单格推理接口及失败保留。**只允许软件fixture累计≤12次optimizer.step，真实研究训练0**；结果/临时权重不作科研证据，不运行旧019等toy suite。CUDA不可初始化、模型权重不可打开，进程内CUDA_VISIBLE_DEVICES为空，不永久改环境。

本节CPU Job outer累计≤900秒、RAM≤4GiB/线程≤4。HEAD_IMPLEMENTATION只能根据实际完成情况给PASS/PARTIAL，不因数据失败就省略代码或伪造未做的检查。

## 6. 全局限额、复核与状态

全父wall≤10800秒，包含实现、网络、等待、解压、解码和清理；其余CPU准备/解压/复核Job outer累计≤2700秒、RAM≤16GiB/线程≤4。下载3600、解码1800、实现验证900及其余2700均受父总量约束，不能阶段重置。仅管理自有Job，记录active0/exit及真实成本；只读数据和输出快照不冒充硬文件系统配额/OS全量审计。

不安装/升级环境、不打开Qwen权重、不初始化CUDA、不用GPU/nvidia-smi、不动旧GPU锁或peer、不训练真实小头/Qwen/LoRA、不运行B0或任何QA推断。本包不给057及旧055权限。

独立stdlib核验不得导入被测join/split/聚合代码；从新的封存成员/标签绑定/采样元数据/来源表逐项复建来源不交叉、数量/排除、路径唯一性/完整性、hash及缓存shape/采样关系。可使用同一已完整验证的ZIP/本父对象，不再次下载/解码。独立核验和实现验证分别报告，不能将fixture计为真实数据独立性证据。

## 7. 八处脱敏交付

1. prototypes/question_temporal_056.py。
2. prototypes/question_temporal_data_056.py。
3. 本目录execution-receipt.md：版本/实际阶段/字节/文件/耗时/失败及监督边界。
4. 本目录training-handoff.md：逐项证据等级、私有精确入口在本地何处交接、未来正式GPU阶段尚缺什么；公开不写私人路径。
5. 本目录split-summary.csv：split,planned_instances,source_groups,qualified_instances,media_complete,frame_cache_complete,failed_instances,unknown_instances；train/validation/development_test三行，未冻结时明确NOT_FROZEN而非0%准确率。
6. 本目录readiness-summary.json：来源/划分/媒体/缓存/代码各门、资源、调用0/研究训练0、fixture更新单列及所有未知。
7. 本目录implementation-check.md：实际代码/梯度/损失/接口验证及独立复核的范围和结果，必要短核验源码可内嵌。
8. docs/codex-results.md仅尾增一条`### VLM-TEMPORAL-DATA-READY-056`。

只提交以上路径；QA/答案、源与成员映射、原身份hash、视频/ZIP/帧/数组、模型/临时checkpoint及原始日志不公开。AGENTS、负责人README/协议/看板/总览和历史证据不改。统一核暂存/脱敏，一次普通安全push main后STOP，失败如实报告，不强推或静默重试。

## 8. 用户发送到本地Codex的启动指令

```text
批准并执行VLM-TEMPORAL-DATA-READY-056。先安全同步独立GitHub文档仓库main，按056 README读取当前合同和相关结果，确认唯一READY且未交付。055已关闭，不重跑、不改旧根或转余额。

我明确授权本包只读列明055公共元数据副本，并在≤16MiB新下载正文内获取固定版本的官方来源说明、对象内容SHA256及Breakfast两个小标注包。先完成原记录/参与者/多机位对应和固定候选划分，禁止只靠basename猜物理独立。

候选来源与最低量通过后，我授权一次整包获取固定DyBench revision的video/event_sequence.zip，已知大小2,783,546,023B；单对象/媒体累计上限为3GiB，不沿用055的64MiB/1536MiB限制。不取另外两个ZIP、不Range/续传/重试；传输outer≤3600秒，内容SHA256和大小必须与发布对象一致。运行前磁盘free≥10GiB，新根总输出≤8GiB。

允许受限提取选中成员（单份≤64MiB/合计≤2GiB）并用现有PyAV做协议内12帧CPU准备。完整执行来源/划分/媒体/缓存独立核验。数据部分若HOLD，继续独立完成056 A/V/S/I小头和数据入口代码及≤12次CPU软件fixture更新，不能只交同一份缺数据报告。

本轮禁止Qwen权重加载、CUDA/GPU、真实研究训练、B0/QA推断和环境变更。严格执行所有阶段/父预算，统一八处脱敏交付、追加一条结果，一次普通安全推送main后停止，不自动057。
```
