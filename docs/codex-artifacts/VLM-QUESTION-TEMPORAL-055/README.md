> **负责人归档（2026-10-29）：055已按输入门安全停止并验收关闭，不可重跑。** [验收](../../research-decisions/post-055-input-stop-disposition-2026-10-29.md)：事件ZIP超原对象/总媒体额度，来源映射未核实；模型/训练0，配方未测试。接受部分交付并保留全文阅读未完成的程序性说明，不签完整协议PASS。当前0 READY；以下READY及启动消息均为历史合同，不再授权执行。

# 055：问题条件化时间关系学习的完整开发对照

2026-10-29（北京时间）｜负责人ChatGPT；本地Windows Codex执行。
父任务：**VLM-QUESTION-TEMPORAL-055**。
状态：**READY / AWAIT_EXPLICIT_USER_START**，不是已授权后台运行。

用户已选定新路线。本包一次连续完成数据准备、实现、冻结特征抽取、8次真实小头训练、全部对照和外部诊断；**不再拆成连续的toy/空资格父任务**。机制、数据规则、公式、臂、seed及去留门以[冻结协议](../../research-protocols/question-conditioned-temporal-learning-2026-10-29.md)全文为准。

GitHub更新本身不启动模型或下载。用户将第6节完整启动指令发到当前**本地3090的Codex会话**，才激活本包具体数据/模型/训练权限。当前云端文档checkout不代表已连接本机实验目录。

## 1. 入口与执行顺序

安全同步独立文档checkout，重读AGENTS、next-steps、codex-results、research-overview、本README、冻结协议及[054关闭裁决](../../research-decisions/post-054-finite-view-disposition-2026-10-28.md)。确认唯一未回报READY为055；无同ID completed/partial/blocked结果，才执行。

只用本地会话已经明确的现有conda pytorch、Qwen3-VL-4B准确模型根和研究输出父目录；缺失时一次集中报告所缺入口，不扫盘、猜旧路径或恢复回收站。当前已经明确的模型根不重复索取。创建新vlm-private-055，已存在则不覆盖。

依次完成：

1. **数据与划分**：核公开固定revision、event_sequence配对/来源/权利说明、TimeBlind严格先后子集；先冻结不看模型分数的划分/候选清单。只取协议需要的媒体，不下载整库。原发布标注只在本父私有工作目录使用，不公开。
2. **实现与必要CPU验证**：实现协议的特征接口、一个公共小头、四种损失、同初始化/采样序列、单格推理、统计/失败传播及持久账本。用自有小型数值fixture核分组/损失不等同CE、S恰用每logit一次、推理不接配对键、参数量/主模型冻结、梯度/参数更新及来源不跨split。不导入/复跑019等旧main或旧suite；fixture通过不算科学收益。
3. **正式特征与基础模型**：CPU核已安装Qwen源代码及processor/tubelet映射；固定后只一次权重加载，在一个监督GPU阶段抽取正式视频/问题特征及B0测试/外部输出。基础模型预测单独封存，不给训练角色。首次真实forward计入预算并复用其结果，不设免费探针/预热。
4. **真实小头训练与推理**：主模型实际卸载、GPU Job active0后，CPU float32连续完成A/V/S/I×两个seed，每配置250次真实backward/optimizer.step；冻结最后一步及代码，逐条生成验证/测试/外部输出，不传四格配对元数据。训练过程中不得访问测试/外部答案或B0输出。
5. **评分、独立复核、交付**：所有臂/seed输出封存后打开评测标签，按完整分母评分；独立stdlib复核不导入被测聚合实现，从新派生整数表复建总数/纠正误伤/四格门及统计。不能把同一实现重调用当独立复核。报告真实资源、失败与未知，一次安全push后STOP。

最低开发样本不足、特征时间轴不能验证、权利/原来源分组不支持预定用途、主模型身份/现有环境不可用，均在正式GPU前停止并交付具体原因。TimeBlind子集不足或跨库来源未知不阻止合格DyBench开发实验；外部门按协议保留UNKNOWN/NOT_QUALIFIED。工程问题可在首正式抽取/首训练前于同父窗口内定点修复并保留失败；开始训练后不得换架构、输入、超参或重新开始已STARTED配置。

## 2. 本包数据范围与额度

只允许以下官方公开入口的选择性元数据和媒体，不引入新服务账户、付费API或云GPU：

- [DyBench](https://huggingface.co/datasets/ddz16/DyBench)：README、仓库revision/文件清单、json/event_sequence.json及其直接引用的选中video文件。
- [TimeBlind数据](https://huggingface.co/datasets/BaiqiL/TimeBlind)：README、revision/文件清单、data.jsonl及选中video文件；[评测代码](https://github.com/Baiqi-Li/TimeBlind)的README、utils.py、tags.json，仅只读核协议。
- 上述资源明确链接的原数据集公开许可/来源说明；仅网页小文本，不追踪其他媒体、旧QA或私人目录。

版本固定后按完整来源组冻结媒体清单；上限DyBench160四格/320视频、TimeBlind32四格/64视频，实际只取满足协议的数量。元数据/公开说明累计正文≤16MiB；媒体累计实际下载≤1536MiB、单对象≤64MiB。下载计数包含失败/重定向实际收到的正文，先核清单大小，流式计量，不能用自动snapshot下载全库或隐藏重试。若官方签名CDN跳转，核实它确为该固定对象的响应链，不转发凭据；不绕过登录/许可要求。

无需为换revision重下同对象。已完成且内容身份匹配的本父对象可复用；未完整文件不冒充可解码成功。预算不足即停止未开始下载，封存后的缺失保留NOT_RUN，不按文件大小/可用性换源补齐。

主机始终保持Windows3090/64GiB和当前conda pytorch；不安装/升级依赖、不迁移环境。不使用Charades、旧HourVideo/049–054的QA/缓存/gold；没有新增人工标注或教师模型。原数据/权重只读，所有新媒体、帧、特征、标签和checkpoint留本父私有目录，不上传。

## 3. 模型与训练限额

仅现有Qwen3-VL-4B-Instruct，local_files_only=True、trust_remote_code=False、BF16/SDPA、batch1；主模型eval/no_grad，模型权重梯度和更新0。模型阶段max_new_tokens=8，只执行B0所需生成，不加解释、反思或重问。

按最高输入量：视频特征调用≤384，纯文本问题特征调用≤384，B0对开发测试和外部的单项回答≤320；模型调用合计≤1088。`generate`内部实际forward步数另报，不能把一次generate称一次forward。按完整输入/模型/模式身份去重，正式调用STARTED前落持久账本；异常不重试，已有闭合结果复用，STARTED未闭合留失败。不从旧父继承调用或预算。

只有一次受监督GPU阶段，outer≤3600秒，包含加载、实际调用、缓存落盘及实际卸载；内部预留120秒清理。PyTorch peak allocated≤18GiB，Job RAM≤32GiB。沿现有非阻塞GPU锁/mutex，取得后两次nvidia-smi检查同3090、free≥18GiB（监督器/worker各一次）；锁忙或不足即GPU_BUSY，不等待、不杀peer、不删除他人锁，实际active0后释放自有锁。

小头训练在CPU，≤1M真实参与参数；4臂×2seed各250步，累计≤2000次optimizer.step，严格同初始化/样本曝光/更新数。仅CPU小头可backward，禁止Qwen、视觉编码器、LoRA或其他模块训练。CPU训练/评估Job outer累计≤1800秒、RAM≤16GiB、线程≤4；其余数据准备/必要测试/CPU解码累计≤7200秒、RAM≤16GiB。每视频12帧，禁止保存全帧流、无界解码或后台worker；有界PyAV随机定位/解码并记录真实帧数/耗时。

全父wall≤14400秒，包括实现、准备、下载、GPU/CPU及清理；不是预计耗时或完成保证。输出根≤3GiB/2048文件，运行前磁盘free≥4GiB；媒体上限及checkpoint合计≤64MiB分别计量。输出快照不是文件系统硬配额；报告控制实际实现，不伪造OS审计证书。只清理/终止本父自有Job，记录active0、exit和所有失败；不修删旧账本/锁，不重跑已消费配置，不自动重开父。

## 4. 科学结论和完整分母

按冻结协议报告五臂、两个训练seed、三个split的全分母/四格全对率、I对各对照的配对纠正误伤与来源组区间，逐臂参数/训练步/曝光/耗时/内存。B0是单次基础模型锚点，不能复制成两个独立样本；四格、重复seed也不增加独立来源数。

完整开发门失败则STOP_THIS_JOINT_SUPERVISION_RECIPE；只赢B0但不赢A也停止。外部数据不足或来源不明不能叫独立泛化通过。只有输出/表示差异、loss下降或成功更新参数，不等于答题收益。首次结果不自动构成论文核心创新，所有状态NOVELTY_UNRESOLVED，既往已证实核心创新仍0。

## 5. 八处允许交付

1. prototypes/question_temporal_055.py：本父小头/冻结损失/训练及单格推理实现，不导入时自动执行模型/下载。
2. prototypes/question_temporal_data_055.py：本父选择性数据、特征抽取/封存和评分入口；不修改旧代码。
3. 本目录execution-receipt.md：实际步骤、版本/参数/调用/训练变化、预算、失败和独立复核边界。
4. 本目录scientific-results.md：协议门、各对照/来源/外部局限及明确去留。
5. 本目录condition-summary.csv：dataset,split,arm,seed,n_instances,n_cells,complete_cells,correct_cells,video_pair_correct,question_pair_correct,four_way_correct,failed_cells,invalid_cells,not_run_cells。B0 seed写NA；包括未完成臂的计划行，非适格外部明确n=0/status说明。
6. 本目录paired-summary.csv：dataset,split,seed,comparator,n_instances,i_only,comparator_only,both_correct,both_wrong,unknown,delta_four_way_pp,bootstrap_low_pp,bootstrap_high_pp。B0共享一次预测，不复制扩大N；所有分母/unknown可复建。
7. 本目录execution-summary.json：冻结输入的匿名规模/来源证据等级、所有臂/门、参数/步/损失聚合/资源与未知，不上传可重识别文件hash。
8. docs/codex-results.md只尾增一条`### VLM-QUESTION-TEMPORAL-055`，链接以上结果。

必要fixture可包含于新实现并显式调用，不能形成无关测试工程。独立复核源码随execution-receipt以短代码块给出。原QA/答案、逐题预测/正确性/logit、数据行/源ID映射、精确私人路径、媒体/帧/特征/权重、checkpoint及原始日志不公开；原公共任务文件不覆盖。README、协议、AGENTS、看板/总览由负责人维护，执行者不改。

统一stage仅八路径、核diff及敏感信息、普通push main后停止；失败如实报告，不强推/重置/rebase或静默重试。不自动056、扩样、调参、再训练、重做旧任务或开启后台监控。

## 6. 发给本地Codex的一次完整启动指令

```text
批准并执行055完整开发实验：安全同步独立GitHub文档仓库main，重读AGENTS、next-steps、codex-results、research-overview、VLM-QUESTION-TEMPORAL-055/README和冻结时间关系学习协议，确认唯一READY且没有同ID交付。

我明确授权本包按README选择性获取DyBench event_sequence开发数据及TimeBlind严格先后外部评测子集：元数据正文合计≤16MiB、媒体合计≤1536MiB，不下载全库。按固定来源划分、仅用训练标签；TimeBlind不训练、不选超参或检查点。

我明确授权在现有3090/conda pytorch上只一次加载本地Qwen3-VL-4B，冻结主模型，完成协议内正式特征抽取和B0输出：GPU监督outer≤3600秒/peak allocated≤18GiB；视频/问题特征及B0调用合计≤1088，实际generate步数另记，无免费探针/重试。主模型卸载后，在CPU训练同一≤1M参数小头，A/V/S/I×seed19、73，每配置250步，共≤2000次真实optimizer.step；不训练Qwen/LoRA、不改环境。

在同一父窗口连续完成实现、必要CPU验证、合格开发实验、外部诊断、封存后评分与独立复核，严格执行完整分母/固定门和所有预算。若外部不足，完成合格开发部分并保留外部UNKNOWN。统一八处脱敏交付，一次普通安全推送main后停止；不重跑旧任务、不调参/扩样/自动056。
```
