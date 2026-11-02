# 078 真实RGB三事件：完整基线、冻结特征与匹配监督训练

2026-11-02（北京时间）｜ChatGPT研究负责人。
**唯一条件READY：AWAIT_EXPLICIT_078_MEDIA_GPU_TRAIN_APPROVAL。** [077验收](../../research-decisions/post-077-stop-review-and-integrated-training-2026-11-02.md)后的一次完整新父包；077关闭不续跑，076本入口停止、D/070关闭、069暂停。**用户本次仅反馈077交付，尚未批准078新范围。** 同意后负责人登记授权，本地新消息明确078即可一包执行，不在相同范围再请示。

## 1 启动、范围与来源

按AGENTS安全同步独立文档main，核唯一未交付条件READY及书面新授权。未授权只等，不开研究根/媒体请求/模型payload，不交空阻断报告。唯一输入仍为用户已交接`PT_077_timestamp_metadata.zip`390919B、SHA256 `950ae2f6766179743f27e512948730682e444eb1c235393d034e508081224cd2`；本地路径可沿本轮明确handoff登记，不扫盘。无路径只等待输入。原077根仅精确读inputgate/失败Job/父闭合/代码seals以核未消费科学输入，不改其文件/失败/锁/结果。旧076仅登记的模型identity/catalog/安装源码hash、输入去重账本/必要token身份，不读旧QA正确性/旧小头/逐项答案作训练或选择。若旧catalog需精确回指已登记模型身份文件，仅那个文件。旧metadata累计≤32MiB，无其它私有根扫描。

使用只读[已负责人实际验证的078 metadata组件](../../../prototypes/timestamped_triples_078_metadata.py)，LF SHA256 `c10f863190a6ccc3f4d961d173dade99c80f35453548e8d523704b9b232bbe34`。完整原包/ZIP64/metadata构建/独立有理数oracle/有序owner比对在新CPU Job内执行一次；`code-seal.json.science_lf_sha256`对应此组件，父级另有完整代码seal清单，不混为全pipeline hash。不得直接import未运行077生产器，原动作字段`id`明确映射内部annotation_id，原JSON不改。程序fixture与所有schema/code修正须在本父正式payload前完成，源规则/选中32/20-4-8不改。

资格要求原2135视频/13644动作、2678合格段、1376候选/280eligible，32选中有序观察/digest匹配owner参考、29动作文本/138精确问题/1152符号答案/2304关系（768FLIP/1536HOLD）、28139 metadata帧。生产与独立代码各自重建，不能只复制负责人结果。32先按原hash排名20train/4dev/8test，再全部六排列×六问；变体不跨split。每同问六排列3是3否。压缩581426975B、解压579702574B、最大压缩71166131B/最大解压70872100B，必须明确两口径。资格不符一次STOP，不换源/补数/改阈值。

官方[Perception Test revision3938d2f1ba3a6b502025741cea4cd73c7b3bdfaf](https://github.com/google-deepmind/perception_test/tree/3938d2f1ba3a6b502025741cea4cd73c7b3bdfaf)动作定位train，原annotation generation1686575055001154/ZIP SHA2565b27beaa97df0a1ea258437b179ed17092981a93501a22a572d64dd46fb12575。保留Google DeepMind归属、数据CC-BY-4.0/软件Apache-2.0、derived裁剪/拼接修改说明。所有官方train中切的test8只是开发留出，owner已见标签，非新盲测/外部确认；原来源与TOC-Bench重叠可能，录制/参与者/像素/预训练重叠UNKNOWN，不声称已排除。标注段出现顺序不认证原子动作严格完成、唯一实际发生、全部动作内容可见。

## 2 只获取固定32媒体，随后真正RGB重排

仅允许`https://storage.googleapis.com/dm-perception-test/zip_data/train_videos.zip`，固定generation1685446268139925、ETag `"-CJXz5tD4nP8CEAE="`、total28404087974B。原central目录171100B/SHA256505019446df7a796909c8f00a63bd55a2e214d3ba533de00104001f0a30aac82已在包内，不额外下载/HEAD/枚举。**不下载整28.4GB archive。** 新构建manifest完整安全路径/ZIP64offset/flags0/method12/CRC/两size先封存。32视频只做30B local header、确切filename+extra、确切compressed body三个Range，≤96请求，无redirect/retry/resume/换源。每次If-Match原ETag，返回必须206/精确Content-Range、identity编码、总长度及generation一致。200或身份不符在应用读取body前拒绝，已实际读到字节仍入账。

每body≤80MiB、总网络response正文≤768MiB；已知compressed+保守local字段上界585622175B，余量不是追加成员许可。bounded BZIP2严格end-of-stream/无多余流/解压size/CRC，记录新收到内容SHA而不假称历史已知hash；解压aggregate≤640MiB、每member≤80MiB。连接阶段总≤15秒；header区域单响应outer≤30秒、视频body响应outer≤240秒、read inactivity≤60秒、整个获取≤1800秒；使用supervisor累计deadline覆盖DNS/代理/TLS/headers/body/清理，不能只用socket timeout冒充连接/outer硬上限。网络Job及字节/失败阶段持久化，超限只终止自己Job。授权不含重复GET。

每源视频只解码一次，无音频，PyAV `codec_context.thread_count=1`在open codec/首次decode前显式设置并核实际配置；线程自动并行禁止。累计≤1800秒/100000遍历帧。保存实际PTS/timebase/实际帧数/fps，finite单调展示顺序，relative-first-PTS时钟与源frame/timestamp端点误差≤一实际源帧+1微秒，帧数误差≤1；三段原时间间隔≥0.1秒。按原12段内中点采样最近真实PTS（平局早者），段内12个不同索引、帧在该标注区间；不足/坏帧/不支持时钟就持久实际/限额、保留32计划分母STOP，不复制/补帧/换样/重decode。未知视觉可见性不转为人工标签。

保存96个12×224×224真实RGB block，每块bytes/hash固定。每组三段真实RGB按全部6种顺序组装为36帧，统一runtime frame0..35、fps12、duration3秒，192变体；原PTS/sourceID/annotation/permutation/标签/原切点不进入模型字段，只有当前视频+当前问题。不是latent块置换。CPU processor-only一次合成fixture，禁止额外模型probe；实际native36帧grid[18,14,14]/pixels[3528,1536]/882占位token、temporal patch2/merge2及每单元49 token的flatten顺序必须从封存本地安装代码和真实prepared结构核对。禁止processor再采样丢帧。所有来源/排列同时钟；BLACK所有非pixel字段对同q的REAL逐字节一致。

prepared按pixels内容寻址，一变体一份bf16、BLACK全局一份，q-token/metadata小引用分开。GT注册角色在model前核精确相同输入若有相反答案则停止资格，不按图像质量/预测选择；原计划分母保留。pixel/hash/GT不进入模型权重或问题文本。不能给六问复制六份pixels。

## 3 一次完整Qwen推理，同时只读取训练特征

同原本地Qwen3-VL-4B-Instruct、本地环境、bf16/SDPA、batch1、eval/requires_gradFalse/inference_mode、use_cacheFalse/logits_to_keep1、local_files_onlyTrue/trust_remote_codeFalse。默认同076native chat template，唯一用户文本为严格原q；assistant首续写位置字面Yes/No均单token且不同，marginYes−No>0为Yes，tieNo，所有值finite。无generate/提示词候选/温度/LoRA/主干梯度/安装/新环境。

GPU前全部完整源码/fixture/模型identity、prepared输入、planned output键、输入与代码seals、独立完整oracle封存；不等结果后补审。持久共享锁/精确input ledger，非阻塞GPU锁忙或free<18GiB→GPU_BUSY，不等/轮询/杀其它进程。同模型图/权重/完整input与历史或本轮CLOSED相同则只精确复用；有未决STARTED/身份冲突或必要feature缺失则停止，不能借新ID/改prompt重问。新旧q字符串交集0只作owner预检，不代替token/input身份核对。允许读取登记的调用hash/状态，禁止旧QA重放。

固定顺序REAL（source排名→permutation→q）→BLACK→TEXT，后两条件按精确q UTF8排序并按完整实际输入去重。B0为三条件各1152逻辑项，共3456；最多新完整root=1152+138+138=**1428**，预计精确别名2028，若实际更多重复则如实减少；不能用预算补调用。最多一次load，GPU累计≤3600秒含load/复制/forward/save/unload，3480秒停止新调用/预留120秒闭合；allocated≤16GiB、GPU Job RAM≤32GiB。每input先持久STARTED再dispatch，CLOSED绑定两logits、margin/pred及必要feature；失败不重载/重试。hooks实际root/visual/decoder/layer/lm_head单列，不将1428叫全部底层调用。无别名时预期root1428/visual1290/decoder1428/36层51408/lm_head1428，核实际模型层数。

**无单独视觉或文字特征forward。** 在这些B0 root中注册不修改输出的只读hook：每REAL变体第一次调用捕获visual原主merger输出[882,2560]，按本地原顺序reshape[18,49,2560]空间均值→[18,2560]float32；忽略deepstack支路，不能猜返回类型或截取解码器视觉token代替。BLACK第一次调用同样捕获唯一[18,2560]。每TEXT root捕获language_model返回的最后有效位置last_hidden_state→当前q的[2560]float32。捕获点/主tensor语义从封存安装源码静态绑定；必要hook缺失/shape不符STOP，不追加probe/feature forward。固定视觉特征的读取不访问当前q/标签。所有feature新文件与模型输入/seals精确绑定；这类特征小头与完整B0接口不同，报告限制，不声称连接器归因。

REAL每variant的pixels只加载一次GPU，连续供其6问复用后释放；BLACK pixels全局只读一次复用所有q；不要重复读prepared使预算爆掉。仅存192个V、138个q和1个BLACK V及必要别名/两logits，不落全词表或完整decoder层序列。所有B0/feature结果封存、GPU卸载/Job实际active0之后，才能CPU训练；B0预测和dev/test答案不供trainer读取。

## 4 同参数/同图的A、I、S真实训练

三臂当前输入函数完全相同：V[18,2560]、q[2560]，两biased Linear2560→64；各LayerNorm64。`v_t=LN(Wv V_t+bv)+P_t`，P[18,64]零初始化可学习；`q64=LN(Wq q+bq)`；softmax(v_t·q64/√64)得权重，z=加权v；concat[z,q64,z*q64]→biased Linear192→64→GELU→biased Linear64→1。无dropout/其它normalizer/额外边界输入。精确参数327808+1152+256+12352+65=**341633**；其余Linear和LN用现有PyTorch默认初始化，顺序封存。

六seed固定19/73/101/137/181/229，各初始化一次，三臂load同一字节state。每seed `random.Random(seed)`预生成250步，每步4个train源组有放回采样，三臂同batch序列/hash。每组全部6排列×6问，144项/batch；trainer只读20源train的720标签/特征及相邻关系；不读dev/test标签、B0答案、其它臂状态。完整18配置顺序seed升序、每seed A→I→S，各250次backward+optimizer=**4500真实更新**。单进程CPU float32，Torch intra/BLAS4、interop1、无workers；GPU训练0。

各臂都计算相同144 logits、BCE均值和关系图，无额外配对forward：p=sigmoid(logit)，每组12有向相邻交换边×6问，delta=y_right−y_left，`L_rel=mean((p_right−p_left−delta)^2)`；A=CE+0×L_rel，I=CE+0.25×L_rel；S=CE+0.25×相同图L_rel，其delta target取当前q的(q+1)mod6，答案CE不改。q顺序[(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]；独立fixture证明每交换对原FLIP question support与S目标FLIP support不相交、计数/符号匹配，不能仅交换等价逆问。冗余关系不是新增独立训练数据/新标签或已证创新。

AdamW lr1e-3,betas(0.9,0.999),eps1e-8,weight_decay0.01，全部参数参与；无scheduler/clip/early stop/中途评估。最终step250唯一checkpoint，不选seed或dev赢家；dev4只在全部最终输出封存后报告。预写CPU软件fixture核参数、forward/backward/loss/打乱支持及隔离，synthetic不用真实QA；其成本入CPU预算，不能跑真实输入试调学习率。每真实optimizer STARTED/CLOSED ledger步数，失败不续训/补seed/改loss。

## 5 一次预测、独立评估与决定门

全部18最终state封存后一次CPU读出，单条推理只当前V/q，不输入group/swap/其它预测/GT/答案池，不强制互补或排序修复。每头三条件REAL、BLACK、TRAIN_MEAN；后者用train20×6=120个V逐位置float64均值转float32，同一固定V供全部q，不能用dev/test。BLACK用前述实际主干black V，无新GPU。每头每条件1152逻辑项；合计**62208**，精确input/state去重后实际eval logits上界20736 REAL+2×18×138=**25704**；训练4500个batch forward另外计，不混为评估调用。所有固定V控制sameq必同预测，三条件不可根据输出切换。

模型和头全部输出/keys/seals闭合后，隔离scorer才接dev/test真值；trainer保留train监督合法，不宣称全数据标签盲。按train20/dev4/test8分别保留720/144/288 item、120/24/48 native变体、20/4/8源组。报单项、每变体六问全对、每源36项全对、相邻交换四格及FLIP/HOLD四格分别正确数。去重为每源6条无向swap edge×3 canonical q/tau=18四格（6FLIP/12HOLD），test144=48FLIP+96HOLD；有向反边只描述，不作新独立证据。给来源组修正/伤害及六seed完整值，私有保存8源差值；公开只汇总。

B0 BLACK/TEXT及每头BLACK/TRAIN_MEAN单项在全六排列中必须精确50%、源36全对0，否则实现/绑定软件FAIL，不判科学收益。独立review不能import生产scorer/训练函数或重放任何Qwen/头/视频decode；从原固定输入/标签/输出/state+steps账本独立重建所有分母/alias/3456基线/62208头逻辑键、native/全36/四格、FLIP/HOLD、参数初始化/batch/步数/只读hook/模型freeze、资源/STOP和门。每源先平均六seed，对I−A、I−S的8个test源差值枚举256符号翻转，给描述性零参照tail与修正/伤害计数，不能视seed或四格为独立源；无事后subgroup/prompt/门阈值搜索。

完整且软件守卫通过时，**所有条件同时满足**才记`QUESTION_RELEVANT_RELATION_PILOT_SIGNAL / NEW_MECHANISM_UNCONFIRMED`：

1. 至少5/6 seed中，I的test源36全对数同时严格高于A、S。
2. 六seed I源全对总数≥12（均值≥2/8=25%），且I−A和I−S总净增各≥6（均值至少1/8=12.5pp）。
3. 六seed I的test单项、FLIP无向四格、HOLD无向四格正确总数各不低于A和S；I源全对与单项均值均不低于B0 REAL且源全对严格高于B0 REAL。
4. I REAL源全对均值严格高于自身BLACK与TRAIN_MEAN，test单项均值≥50%。

关键unknown→`INCOMPLETE_NO_SCIENTIFIC_GATE`；完整但任一不满足→`NO_SATISFYING_JOINT_SUPERVISION_SIGNAL / STOP_THIS_RECIPE`。不要求B0自己先在源全对上胜控制，不因其失败否定已满足I对照的学习收益；B0始终报告。新门在078模型前审定，不改076/077历史门。未过不换控制/补seed/改阈值/升级A为新方法；过了也只是小开发试点，须后续未调参数据验证和原创性查新才谈方法论文。不以loss/表示差异代替答题收益，不写069论文。

## 6 一次新资源合同与交付

| 阶段/资源 | 新上限 |
|---|---|
| 本地metadata/processor/软件准入累计 | CPU600秒；metadata标准库，无环境变更 |
| 新32媒体网络 | 正文768MiB、compressed单member80MiB、≤96精确Range、累计1800秒；连接15秒/header30秒/body240秒，read inactivity60秒 |
| 解压/实际媒体 | aggregate640MiB/每个80MiB；media逻辑读累计4GiB，解码1800秒/100000帧/每源1次 |
| GPU冻结load/infer/unload | 1次load、3600秒、allocated16GiB、GPU Job RAM32GiB、≤1428完整root，独立特征/训练forward0 |
| CPU三臂六seed训练 | 累计1800秒/4500更新，RAM16GiB；stage软件fixture成本计入 |
| CPU最终预测/评分/独立核验 | 累计600秒，RAM16GiB，无模型/头重放审计 |
| 必要旧metadata / 新prepared+中间件读 / model hash | 32MiB / 12GiB / 12GiB（同一既有模型hash一次）分别累计，框架native覆盖如实单列 |
| 根/文件/最终与初始state | 新独占8GiB / 4096文件；全部checkpoint合计64MiB，流水账可append+fsync不每状态建文件 |
| 起始free / pre-sync父总时间 | ≥12GiB / ≤14400秒，所有阶段合计及cleanup/Git等待均计父 |
| CPU科学compute / native线程 / active | metadata单计算线程，Torch/BLAS intra≤4/interop1，codec显式1；**OS原生线程采样停止阈值256/owned进程**，同时active≤2 |

原生startup/CUDA/驱动辅助线程与compute/codec分开列数；native≤256为20ms own-Job快照约束，不声称连续硬线程quota。不得再将Windows启动4线程误按单科学计算线程超限杀掉。单阶段可用两个自己的进程落实Job supervisor；host/UI/Git/隐式native/物理IO/周期文件quota覆盖未知显式UNKNOWN，不将快照/逻辑读计数说成全OS认证。只关闭自己Job，禁止其它进程kill/锁删除/环境安装/CPU或GPU超预算后再修跑。

全部科学/下载/解码/prepare/推理/训练/评分/独立核验/监督器源码与参数矩阵在首次正式研究payload前完整封存；准入ZIPsize/hash/目录和必要安装身份只允许精确路径。尽可能用原源metadata预写fixture，已验证metadata组件不临时改数据规则。预执行代码准备失败可在正式payload前修语法/公开fixture并记录，不可用该例外重放正式媒体/model/训练输入。持久pre-sync父起点/free/新锁/预算及代码seals，阶段超限先记actual/limit/剩余/FAILED then STOP，全部planned分母保留；不为赶门删例。一次父包准入通过后连续做所有已授权阶段，不再拆成独立审计任务。

精确**九处**脱敏Git交付：

- `prototypes/timestamped_triples_train_078.py`（完整实际pipeline/独立review源码，已提供metadata组件只读）
- 本目录`execution-receipt.md`、`admission-summary.json`、`baseline-summary.csv`、`head-summary.csv`、`paired-summary.csv`、`scientific-results.md`、`execution-summary.json`
- `docs/codex-results.md`一次本父append

基线CSV固定9行（三split×三条件）；头CSV固定162行（三split×三条件×三臂×六seed）；配对CSV固定42行（三split×I对A/S×六seed及mean）；计划/有效/未知/整数与比例、actualnew/alias守恒，未执行全部NA，实际0输出与科学0正确分开。JSON保留schema/输入/Job/source/clock/模型/参数/4500steps/alias/独立核验/门与资源实际覆盖。不得上传原标注、实际问句/GT/源ID/时间戳/媒体成员映射、视频/帧/特征/weights/路径/凭据；官方source URLs/revision/全局hash/汇总可公开。owner README/看板/决策/metadata已验证组件/历史均只读。

安全审查、只stage九处，一次普通push main后STOP，不自动079/后台轮询，不写论文/追加训练。用户批准此整包后，同范围不用再次确认；若未来需要超此范围，仅先持久实际并停回报。负责人验收同回合给下一步。
