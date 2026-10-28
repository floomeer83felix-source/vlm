# 053：证据交互路由的一次完整开发比较
2026-10-28（北京时间）｜负责人ChatGPT；本地Codex执行。父任务 **VLM-BLOCK-INTERACTION-053**。
**唯一READY / AWAIT_EXPLICIT_USER_START。** 本README下列启动消息被用户发到当前本地Codex后，才激活这一新父包的具体模型/缓存/评分权限；GitHub更新本身不启动。
科学算法、平局、复核门、六方法、480次上限及投入门以[冻结设计](../../research-proposals/answer-conditioned-block-interaction-2026-10-28.md)全文为合同组成部分。不是核心创新认证，不继承任何旧预算。

## 1. 开始、身份与准确入口
安全同步独立文档checkout并重读AGENTS、看板、results、总览、本README、冻结设计及[052验收](../../research-decisions/post-052-protocol-disposition-2026-10-28.md)。确认唯一未回报READY053；所有旧父均已消费，不修改/重跑。
只用当前已明确的052、051准确关闭根，不扫盘、猜父路径、恢复回收站或读取旧049根。入口确有缺失，先一次集中交接准确入口，不创建占位HOLD运行。明确入口后，在同一指定父目录新建vlm-private-053，不覆盖/删除已有根；父窗口从入口明确开始≤7200秒，含实现、准备、等待、核验、清理，不重置。

只读列明旧元数据，单文件≤2MiB、合计实际Python返回≤16MiB：
- 052：coordinator-config.json（仅原文件身份/准确已知入口）、classification-private.json、classification-seal.json、nongold-projection-private.json、analysis-receipt.json、classify-phase.json、analyze-phase.json、verify-phase.json。若准确闭合核验文件命名在052本地记录不同，只一次交接精确已有名称，不猜文件/改读整个目录。
- 051：coordinator-config.json、runtime-config.json、nongold.json、source-selection.json、source-map-private.json、worker-input.json、input-queue-seal.json、inference-complete.json、infer-phase.json。只为同24题/源/缓存/配置/旧完整输入身份；不读其中其他资产。
- 051 old-natural-worker.json：词法投影closed_hashes，其他字段值跳过，不保留旧预测。只用上述闭合索引作局部重复检查，不回读旧账本；全历史完整输入身份覆盖仍UNKNOWN，不把局部去重称全历史exactly-once。
不读051/052逐题派生correct、旧score-private/predictions、旧049目录、原视频/图像/新数据或模型权重以外资产。公开参考/文档Git单列。

封存前核同24 Q01..Q24、四source各6、原ordinal/UID私有映射、052分类/投影SHA、原annotation冻结SHA、051同数组shape/dtype/内容SHA与同一模型processor/tokenizer配置身份、051和052相关进程实际active0/exit0（051初bind曾失败并已定点修复，不能错误要求其初bind exit0）。原052源脚本身份为仓库LF SHA256 7825e6e0b4b34c2b9ae2d4d6fd5326a63b3059f1dc92c79b81954c1e78758612；不要套用051 CRLF关系。
保留全24；明确052一题time-scope标志不在原049宣称范围内。新比较不宣称时间无关资格、物理时间能力或已找到必要证据；不据类型/来源/分数筛题。分类原task和UID映射不进模型角色，模型只得冻结题文/选项/source alias及准确缓存入口。

## 2. 准备、代码与读出门
仅当前既有conda pytorch，不安装/升级/新环境。可只读049 template/cpu_boundary、051 native_input/缓存读计量及040 Job/Process纯实现以复用实际接口；复制必要窄函数到本包或受控加载纯helpers，不执行旧main/旧infer/旧score，不改旧代码。
先实现冻结算子/消融/共同门/精确平局与完整分母，必要自有CPU夹具验证单项/二阶恢复、路由不看三块实测或gold、复核失败回退、输入去重/计数与失败保留。夹具只是软件验证，不作机制科研证据。分析过程不新增主观阈值。
两个CPU processor探针，均为自有合成48帧阵列（全128、全0）和自有非基准问题；**模型forward0/CUDA初始化0**。核原生48槽grid[24,12,18]/1296视觉tokens、完整字段/整数及BF16类型、原序数metadata回调、时间码与token roundtrip、全部五续写恰单token的完整上下文边界（正式CPU准备时再核同24题的真实上下文）、前缀真实进入input_ids、长度≤4096。不把序数载体的seconds文本认证为自然媒体物理秒。
若读出/原生结构不成立，CPU侧READOUT_NOT_QUALIFIED或INPUT_NOT_QUALIFIED完整回报后停止，不调prompt/回退多token评分/启动模型。
CPU实现问题可在同父累计预算内修正、保留初失败和源码；允许正式forward前定点修复。首正式forward后策略/模板/算子/阈值/分母/评分代码冻结，不调参、不重启模型、不重跑已STARTED状态。

## 3. 私有输入准备与一次模型阶段
四个准确既有uint8[48,192,288,3]数组只读，各打开一次，使用可计量np.load allow_pickle=False，合计Python读返回/预留≤64MiB；旧内容SHA全部匹配。原数据只读，遮挡在内存新副本上，原槽保留字节匹配；不复制旧缓存到新根、不写媒体/数组payload。无媒体decode/SigLIP/新增高分辨率。
CPU准备填128的16状态/题共384逻辑状态，构造最终CPU输入/封存真实张量与文本身份。路由观测只是12项；额外4三块结果只供选择后验证和误差分析。队列确定顺序按qi、mask整数；每题16状态起点按qi mod16循环（不据答案/时长改变）。
完整输入身份必须含实际input_ids/attention/视觉值/shape/dtype/grid及执行模型配置；同一底层完整输入不能因为标签053、forward模式、读出字段或填充名字不同就重新调用。与051及其闭合旧索引核对；旧STARTED且缺所需闭合5-logit者记HISTORIC_INPUT_UNAVAILABLE，不重跑。首formal forward前所有初始输入的边界/去重检查通过。第二填充按冻结选择生成时同样核完整身份，重复直接映射同一闭合结果。
最多一次权重加载，Qwen3-VL-4B-Instruct既有本地权重，BF16/SDPA、batch1、eval/inference_mode、seed19、local_files_only=True/trust_remote_code=False。不训练、不反传、不加detector/第二模型/API。
一个新逻辑视频状态仅一次model forward，use_cache=False，取最后位置五候选logit；float32 log_softmax归一化。禁generate、warmup、模型探针、重试、额外解释/反思。用forward钩子核实际调用steps；forward到RETURNED前持久STARTED，成功后封存得分/成本；NaN/异常不补调用。model只有nongold配置，没有原标注/正确性文件入口。
先收集填128，I/A/C调用只传12项；选择封存后才能查询三块实测验证。R的13项观测集合由qi预先固定，只接收其声明观测后才选择；I/A/C不接触未允许的三块真值。I/A/C/R的不同所选集合在填0上至多4个/题；S=full复用，完整输入去重；全父最多480实际forward（非480×5），不得用稀疏失败/预算余额扩状态。GPU时间不足或异常时保留已发生STARTED/RETURNED/未执行格，清理自有Job并交付完整失败分母，不重开父任务。
禁止按已知S04成功模式、task alias、旧逐题正确性进行路由。没有必要证据标签，不作真实干扰/检索融合归因。

## 4. 窗口、监督与硬停止
单模型监督Job的outer wall≤1200秒，包含权重装载、正式输入在模型阶段的准备/迁移、所有forward和实际退出；内层权重意图计时须被其包含，GPU诊断不得另开免费窗口。监督器提前保留≥60秒完成卸载/退出；达到内部停止点后不再发新forward。
GPU PyTorch peak allocated≤18GiB；Job RAM≤32GiB；单进程单batch，不并发模型。CPU-only监督Jobs outer累计≤1800秒（模型Job中的准备已计GPUouter，不相加双计），其余Job也RAM≤32GiB、线程1。既有Job/Process先assign后运行，所有下阶段只在本阶段真实active0后开始；只结束自有Job。
沿既有非阻塞GPU锁/mutex，仅在取得后用两次nvidia-smi核同3090 UUID/bus与free≥18GiB（父/worker各一次）；锁持续到模型Job真实active0。锁忙或free不足即GPU_BUSY无模型尝试；不等候占用者、不杀peer/清旧锁、不用第三次查询追查。
新根≤128MiB/1024文件；开输出前磁盘free≥128MiB+1GiB。阶段记录实际元数据/数组返回字节、墙钟/峰Job/torch峰值、实际active0和输出快照；快照不冒充硬文件系统配额。父≤7200秒。已实际开始的parent不复跑，未用余额不转给054。
上述上限是止损合同，**不是预计实测耗时/保证完成**。资源不达则报告不完整，不靠省略对照或放宽门完成。

## 5. 先输出封存，再隔离评分
实际模型Job active0/exit状态明确后，stdlib角色从闭合5-logit表/冻结策略重建六方法选择、门与输出，并封存完整24×6=144个逻辑输出状态；任何必要输入缺失/非有限等向受影响方法传播FAILED/NOT_RUN/SCORING_UNKNOWN，不把它们隐式当F回退。合法拒绝改答才可回退F。
之后独立stdlib scorer打开与052/051同SHA的原mixed annotation**一次≤4MiB**，词法投影仅同24 question/mcq_test/correct_answer_label，使用负责人051 binder严格核冻结题/选项，保护答案值最多24个。不重开、不试其他版本、不碰task/answer_N/图片；原物理mixed open与保护值解码分开报告。不得整文件json.loads，不保存原始混合字节或公开gold。若本轮实际返回0个新模型结果，不打开原答案，全部新评分UNKNOWN。
原标签不进入模型/路由配置；独立评分必须后于模型退出和所有方法输出封存。使用同一标准答案评估六个新读出方法；旧SO/F48/V4历史分数原样保留、不可当新读出基线或补全失败状态。
公开：全24固定分母，6方法×(ALL+4源)=30条件行；I对F/A/C/R/M×(ALL+4源)=25配对行，包含纠正/误伤/双对/双错/unknown；完整失败状态、改答与回退/填充冲突/估计残差、GPU/CPU/正式调用和各policy实际组件成本。
单个门仅在所有必要状态完整/评分无未知时判PASS/FAIL。按冻结设计预设门，不修改049/051的历史门或用子组过门。单源/任务类仅事后描述，不新增“清洗后主分数”。
另一独立stdlib复核者不导入本包聚合/策略实现、不再开原文件/旧分数，从新sealed nongold5-score/输出/score派生表逐项重建选择、平局、复核门、144格、30/25行、配对/来源分母和成本。独立复核也不接触原标签文件；公开清楚其证据边界而非OS访问审计认证。
真实收益若符合开发门，仅OBSERVED_DEVELOPMENT_GAIN/OWNER_REVIEW_REQUIRED；否则STOP_CURRENT_ROUTER；不完整则INCOMPLETE_OR_UNKNOWN。NOVELTY=UNRESOLVED，任何状态不自动产出核心创新/论文结论。

## 6. 七处交付与停止
1. prototypes/block_interaction_053.py：仅本包冻结实现/必要自有fixtures；不得修改旧模块。
2. 本目录execution-receipt.md。
3. 本目录scientific-results.md。
4. 本目录condition-summary.csv（30行）。
5. 本目录paired-summary.csv（25行）。
6. 本目录execution-summary.json（完整脱敏计数、所有方法门、来源/成本/失败、独立复核与未知）。
7. docs/codex-results.md只追加一条“### VLM-BLOCK-INTERACTION-053”。
README、proposal、AGENTS、看板/总览和旧代码/历史证据由负责人维护，执行者不改。公开不含真实路径/UID/原task映射、QA/选项/答案、逐题logit/预测/correct、可重识别输入hash、媒体/缓存/权重/原始日志；源码hash和匿名聚合可公开。
同一轮连续完成允许的实现/CPU门/一次模型/隔离评分/独立复核/脱敏报告，一次普通安全push后STOP。不自动054、扩样、更多块/填充/前缀/阈值/第二模型、下载或训练。

## 7. 用户发给当前本地Codex的启动消息
```text
批准并执行053完整开发比较：安全同步GitHub文档仓库main，重读AGENTS、看板/results/总览、VLM-BLOCK-INTERACTION-053/README及冻结机制设计，确认唯一READY且未交付。

我授权本包内只读列明051/052元数据与四个既有48帧缓存，完成CPU读出/原生输入门后，一次加载既有本地Qwen3-VL-4B，按冻结六方法最多480次新完整输入forward。模型退出、全部输出封存后，隔离读取同版原标注一次，只对同24题评分；不重跑历史完整输入、不换题或调参。

严格遵守GPU监督outer≤1200秒/allocated≤18GiB、CPU-only累计≤1800秒/Job≤32GiB、父≤7200秒和全部读取/输出上限。连续完成七处脱敏交付，一次安全推送后停止，不自动054；不下载/解码媒体、不训练或改环境。
```
