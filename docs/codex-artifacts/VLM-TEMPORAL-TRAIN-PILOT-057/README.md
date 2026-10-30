> **负责人归档（2026-10-30）：057真实训练已完成、验收关闭，不重跑。** [验收](../../research-decisions/post-057-real-training-disposition-2026-10-30.md)：8配置/2000真实更新，I四格3/24、4/24低于A5/24、7/24，预设先导门FAIL；停止具体联合监督配方。加载前监督器失败/修复保留，当前0 READY，不自动058。以下READY/启动指令仅为历史合同。

# 057：首次真实时间关系小头训练先导

2026-10-30（北京时间）｜负责人ChatGPT；本地Codex执行。
父任务：**VLM-TEMPORAL-TRAIN-PILOT-057**。
状态：**READY / USER_REQUESTED_ACTUAL_TRAINING / LOCAL_START_REQUIRED**。

用户明确要求“尽快开始实际训练”。[056验收与先导决定](../../research-decisions/post-056-and-first-training-pilot-2026-10-30.md)接受已有实现，并在任何本路线模型/训练输出产生前，预注册本次25训练/2验证/24测试的小规模真实先导。本包连续完成获取、解码、冻结特征、8次真实训练及评分，不再单独下发准备任务。发布合同不代表本机已运行；用户将第9节发给本地Codex激活执行。

## 1. 范围与当前事实

056有51对政策合格候选、原参与者分配25/2/24，组数16/2/15；未达到其64/8/32最低量，因此媒体/模型/真实训练0。旧056的HOLD正确且保持，不修改其表格、门或输入文件。

057明确采用同51对、同source-table/candidate-split成员及原hash划分。**不重新挑样本、不放宽事件标准、不更换hash或混入其他子类。** 只将本轮科学范围改为小规模开发先导；它不证明原完整开发任务通过、不提供外部确认。验证2对禁止用于选参/早停/检查点选择。原055/056和053/054均关闭，不重跑、不转余额。

## 2. 同步、精确入口和新封存

在独立文档checkout安全同步main，完整读AGENTS、本README、上述验收、055冻结方法第5至7节、056执行回执/训练交接/实现检查及两份056源码。看板/总览读当前段落；results完整读056条目并搜索唯一057，其他历史仅背景。确认唯一未交付READY为057，既往同ID有任何已交付记录即停止，不清理/覆盖现有文件。

只用当前会话已明确的现有conda pytorch、Qwen3-VL-4B-Instruct准确模型根、关闭056准确根及私有输出父目录。缺准确入口一次性指出，不扫盘猜路径。新建vlm-private-057，独占创建，不覆盖已有根或改旧账本。若055/056有活动作业，先报告，不并发启动新模型。

只读056：training-handoff-local.json、source-summary.json、source-table.json、candidate-split.json、prior-copies.json、independent-review.json、implementation.json、additional-checks.json、breakfast-revision.json、acquisition-status.json及其明确列明的阶段receipt；单文件≤2MiB、合计≤16MiB。不读旧fixture目录、其他任务私有根或旧HourVideo QA/缓存/gold。数据准备角色可为本包绑定读取同51对的发布标签；训练角色只得到训练标签。

核51对及完整成员身份、25/2/24、参与者不交叉、原标注证据、公开源码LF SHA；本机CRLF原始字节和规范化SHA分开，不因换行误改旧文件。新pilot-input-seal明确记录任务057、旧056规模门未过、新先导范围、全部成员/来源/划分/标签绑定/代码配置身份。只在057新副本中设置本包media许可，不能把056原门改PASS。

## 3. 一次获取事件ZIP并准备真实输入

在本包新预算中，复用056媒体获取/安全提取/CPU缓存的纯函数或复制经核对的窄实现到新057模块；允许修改**新模块**以接收057先导seal。不得调用056 acquire/join/main/fixture、触发旧任务或改其源文件。旧工具的media_permitted检查必须由新的057明确先导许可满足，不能暗中移除来源检查。

固定对象：
`https://huggingface.co/datasets/ddz16/DyBench/resolve/fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405/video/event_sequence.zip`

先用固定版本官方对象元数据核精确大小2,783,546,023B及发布**内容SHA256**；不混用Git blob SHA、LFS内容SHA、Xet标识和ETag。元数据/说明新增累计正文≤16MiB；媒体累计正文≤3GiB，一个最终媒体GET尝试，无自动重试/Range/续传/下载其他ZIP/换revision。最多5跳官方固定对象响应链，HTTPS、不转发凭据；计全部重定向/失败正文。流式写盘，提前落STARTED，outer≤3600秒、connect≤30秒/read无进展≤60秒。最终大小和内容SHA均匹配才解压。

运行前磁盘free≥10GiB；新根输出≤8GiB/4096文件。ZIP目录≤16MiB/4096条，拒绝重名/加密/穿越/绝对路径/链接及异常压缩；只提取同51对的102个唯一成员，允许唯一的发布ZIP目录前缀对应，歧义保留失败，不猜同名对象。单成员≤64MiB、累计解压≤2GiB、解压/压缩比≤100，逐成员完整性/CRC通过。

现有PyAV有界CPU解码：102视频各在整片段12个等时间bin取中点最近合法帧，224×224 RGB、唯一帧索引，保存uint8[12,224,224,3]及采样/容器时间基/身份。不得用原标注时间裁事件、按标签/预测挑画面或复制帧补12。累计CPU解码outer≤1800秒、解码帧≤500000、RAM≤16GiB/线程≤4。已有本父闭合对象按完整内容身份复用，STARTED未闭合不重试；缺失/失败保留计划分母，不换组补齐。

完整102媒体/缓存及51四格都核齐后才进入模型阶段。未齐则REAL_INPUT_INCOMPLETE，保留全部计划和实际失败；不靠缩小分母启动另一个未注册子集。准备阶段的问题可在首正式媒体/模型/训练之前定点修复并留记录；已STARTED下载、模型输入或训练配置不重跑。

## 4. 一次冻结Qwen阶段：真实特征与B0

现有本地Qwen3-VL-4B-Instruct，local_files_only=True、trust_remote_code=False，BF16/SDPA/batch1，全部eval/requires_grad=False/no_grad；主模型更新0，不调用SigLIP/第二模型/付费API。

先在CPU阅读本机已安装实现/配置及processor格式，确定12帧→真实grid/tubelet→时间单元/空间token对应。实际返回结构/shape必须核实，禁止按元素总量猜reshape、把空间token当时间。首次真实抽取就是正式输入，计入持久账本并复用结果，不设免费GPU探针或预热。

按055固定特征定义：V为Qwen主视觉输出、进入语言解码器前的表示，按实际时间单元仅空间平均；q为同模型纯文本forward中问题最后有效token的最终隐状态。保留词序，不用输入词嵌入的无序平均替代。量测实际Dv/Dq，转float32 CPU缓存；全部臂共享同一份特征。不因抽取失败切换SigLIP/特征层或第二模型。接口不能成立时报告FEATURE_RUNTIME_NOT_QUALIFIED，不虚构训练。

所有问题模板、采样RGB和时序配置在首正式调用前封存；B0只对固定24测试四格共96项生成回答，使用同12帧与当前问题、greedy、max_new_tokens=8，确定的完整Yes/No及可选句点解析；其他INVALID，不重问。B0结果单独封存，训练角色不可读取。

上限直接视频特征调用102、不同当前问题文本特征调用102、B0生成96，高层模型调用合计≤300；完全相同文本/视觉输入可去重复用，不借task别名重新调用。generate内部实际forward步数及其视觉编码调用另报，不能把B0内部96次可能的视觉编码当作免费或遗漏在实测中，也不称只有300个底层forward。每次正式调用先持久STARTED；失败/NaN留状态，无重试。

一个监督GPU阶段outer≤3600秒，包含加载、正式准备/调用/缓存和实际卸载，内部预留120秒清理；allocated峰≤18GiB，Job RAM≤32GiB。沿既有非阻塞锁，取得后监督器/worker各一次nvidia-smi核同3090/free≥18GiB；忙则GPU_BUSY，不等候、不杀peer或删除旧锁。锁保留至实际active0。GPU预算不分阶段重开，模型不能二次加载。

## 5. 8次真实CPU小头训练

主模型Job实际退出并卸载后，使用056公开小头的TemporalHead、objective、shared_plan、train、predict纯接口（源码身份核齐），或在新057模块中作等价的必要编排。禁止改旧源码、重跑056 fixture或使用旧fixture权重/合成特征作为训练数据。

四臂A/V/S/I、seed19和73，均从同seed全新公共初始化开始，使用同25训练实例、同250×8有放回采样序列、同真实参数数和曝光。r64架构及损失完全沿用055/056；若实际Dv=Dq=2560参数为356673，最终以实际计数为准且≤1M，无虚假补齐。

AdamW lr=.001、weight_decay=.01、betas=(.9,.999)、eps=1e-8、clip_norm1、float32、batch8四格、每配置250步。累计≤2000次**真实研究optimizer.step**，不把056的8个fixture更新计入。训练进程不接验证/测试标签或B0结果；验证2对不得选参、早停或选检查点。只保存最后一步，不扫步数/超参/损失权重，不选有利seed。

CPU训练/评估累计outer≤1800秒、RAM≤16GiB/线程≤4，进程内CUDA_VISIBLE_DEVICES为空、不永久改环境。每配置独占新目录，STARTED/STEP_STARTED/STEP_CLOSED/CLOSED或FAILED持久落盘；250次实际更新、有限loss/梯度、真实参数变化、最终checkpoint都要报告。不重启/恢复已STARTED配置；失败的臂不省略，不把已发生步数清零。

首optimizer.step前可核真实特征/标签shape、初始化和计划，作无更新的数值检查；不另加合成训练或未注册真实优化步骤。仅原训练集可提供标签梯度。CPU预算不足保留状态和全计划分母，不用减少对照或只保留一个seed凑完成。

## 6. 单格评估、封存后评分与先导门

每个最终小头逐条预测train25/validation2/test24，共每配置204项，八配置1632项；接口只接当前V与q，不传来源/文件名/配对ID/标签或其他格结果，不按四格翻转、投票或强制互补。z>0为是，否则否；z=0固定否。B0仅test96项，train/validation没有B0计划行。

全部8配置最终输出、代码/checkpoint/特征/索引身份及B0输出封存后，评分角色读取本父分离的标签文件并逐项严格绑定。不重新读旧原混合文件/旧QA，不把测试标签或输出返回训练角色。文件/角色隔离按真实实现说明，不冒充OS级访问审计。

公开condition-summary固定25行：train/validation/test各8个小头配置，共24行，另1行test B0(seed=NA)。字段dataset,split,arm,seed,n_instances,n_cells,complete_cells,correct_cells,video_pair_correct,question_pair_correct,four_way_correct,failed_cells,invalid_cells,not_run_cells,status。train100格、validation8格、test96格/方法；失败/未运行保留计划分母，完整率另报。

paired-summary固定8行：test×两个seed×(A,V,S,B0)，字段seed,comparator,n_instances,i_only,comparator_only,both_correct,both_wrong,unknown,delta_four_way_pp,bootstrap_low_pp,bootstrap_high_pp。四格实例是主单位，B0共享一次预测，两个seed不翻倍样本数。按原15参与者组配对bootstrap10000次、seed55057给95%区间；小样本及厨房未知单列，不以区间包装独立确认。

先导投入门在首次模型/训练前冻结：所有必要状态完整且评分无未知；两seed各自I对A≥5个百分点且至少净多2个四格实例全对，I对V、S均>0，两seed平均I对B0>0。测试24例时“净多2个”实际为8.33个百分点，不能把2次seed当48例。来源分层差异、loss及参数变化单列，不能代替答题门。

完整过门仅PILOT_DEVELOPMENT_SIGNAL / OWNER_REVIEW_REQUIRED，未过为NO_PILOT_SUPPORT_FOR_THIS_RECIPE，必要状态不全为INCOMPLETE。本包没有外部评测，外部确认明确NOT_RUN；即使过门也不是原055完整门通过或核心创新认证，不自动调参/扩样/训练058。四格评测不能单独证明问题相关时间定位。

## 7. 总预算与独立复核

全父wall≤21600秒，下载/解码/GPU/CPU训练均计入；其他实现/CPU准备/复核累计outer≤3600秒、RAM≤16GiB/线程≤4。8GiB/4096文件输出覆盖ZIP、选中媒体、帧、特征及checkpoint；最终checkpoint合计≤64MiB。只管理自有Job，不安装/升级/迁移环境，不开云GPU/后台监控，不动旧账本/锁/数据。

独立stdlib复核不得导入被测损失/聚合/评分实现，从新sealed输出和标签派生整数表重建每格状态、25/8行、配对纠正误伤/门及组bootstrap输入；训练步数从各配置日志复建，明确STEP_STARTED未闭合不等于已完成更新。不得再次运行模型/训练/下载/解码，不能把执行者自报计数或同函数重调用当独立复核。

## 8. 八处脱敏交付

1. prototypes/question_temporal_train_057.py：新父编排/训练/评分和必要纯helpers。
2. prototypes/question_temporal_runtime_057.py：实际Qwen特征/B0运行及边界实现，import无自动模型/网络动作。
3. 本目录execution-receipt.md。
4. 本目录scientific-results.md。
5. 本目录condition-summary.csv（25行）。
6. 本目录paired-summary.csv（8行）。
7. 本目录execution-summary.json：所有实际步数/研究vs软件更新、参数变化/损失聚合、预算/未知、试验门和无外部确认。
8. docs/codex-results.md只尾增一条`### VLM-TEMPORAL-TRAIN-PILOT-057`。

独立复核短源码可内嵌回执。所有媒体/帧/特征/权重/checkpoint、原QA/答案、逐题logit/预测/正确性、源映射/原身份hash及私人路径不上载。README/冻结协议/看板/总览/AGENTS和历史代码不改。只stage八处并核敏感内容，一次普通安全push后STOP；不强推、不静默重试、不自动058。

## 9. 发给本地Codex的简短执行指令

```text
执行VLM-TEMPORAL-TRAIN-PILOT-057实际训练先导。安全同步main，读取AGENTS和057 README，确认唯一READY且未交付。

按新先导合同固定使用056的51对及25训练/2验证/24测试原划分，不重跑056、不改事件标准或旧文件。授权本包一次获取事件ZIP（媒体≤3GiB/元数据≤16MiB），完成CPU解码和真实特征准备。

授权一次冻结Qwen GPU阶段outer≤3600秒/allocated≤18GiB/高层调用≤300，随后CPU完成A/V/S/I×seed19、73各250次真实更新，共≤2000步，并完成B0与小头对照评分。主模型不训练，不调参、不改环境，其他限额按README。

下载、抽特征、8次真实训练、封存后评分和独立复核连续做完，统一八处脱敏交付，安全推送main后停止，不自动058。
```
