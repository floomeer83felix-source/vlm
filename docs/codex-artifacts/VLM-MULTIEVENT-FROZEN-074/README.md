# 074 修正版24视频原生六问：一次冻结模型评估

2026-11-01（北京时间）｜ChatGPT研究负责人。**唯一条件READY：AWAITING_074_MEDIA_AND_GPU_AUTHORIZATION_AND_PACKAGE。** [073验收](../../research-decisions/post-073-review-and-native-multievent-evaluation-2026-11-01.md)接受部分交付但原清单准入FAIL；新任务修复已知根资格漏项并直接评估，不修跑073、不再单独交一轮准备报告。070继续关闭、069继续暂停。

## 1 先取得明确授权和完整本地包，不空转

本轮是新的原生媒体/模型范围：[AGENTS](../../../AGENTS.md)要求data download及GPU/model operations明确授权，历史额度不继承。用户需明确批准**074固定24段原视频获取≤512MiB，以及本地冻结Qwen3-VL单次GPU≤600秒/allocated16GiB、最多52高层特征调用和36旧头5184逻辑预测**。一般“继续”或073交付不等于批准。尚未批准只报NEEDS_074_MEDIA_AND_GPU_AUTHORIZATION，不读媒体/模型、不建实验根/消费任务/append结果。

批准后由ChatGPT负责人按已冻结修正清单取得并交接一个私有ZIP，不让本地Codex再运行072失败下载器。负责人获取范围仅固定revision `da3065053d958c38151304e33a42e138b1899eaf` 的24个已选原生媒体：每文件一个逻辑GET、最多3跳重定向、无重试/Range/HEAD/替代host/version/来源；所有响应正文累计≤512MiB、累计外层≤900秒，逻辑连接总阶段≤15秒/无进展read≤30秒，必须有外层监督而非仅socket timeout。按固定API普通Git blob/LFS内容身份和size验证，失败不伪造完整包。研究下载和Git文档同步分开计量。公开不存储媒体、成员IDs/路径/hash或逐项映射；仅向本用户交接本地评估包，不公开再分发。

本地Codex只有在收到**当前新消息明确授权+具体ZIP路径**且输入门通过后才正式执行。ZIP应有三原元数据、修正规则/无标签观察/评分专用标签和仅24段匹配媒体；三原文件仍1847197B，视频发布总103041283B，不能多取整库。包未齐/路径缺失/版本错，只报告具体所缺并等待，不建074根、不交空阻断包、不联网或轮询。

## 2 同步、封存和修正版资格

安全同步独立文档main，读AGENTS/最新看板/总览/results、本合同、073验收及073原合同、[068原媒体接口](../VLM-FROZEN-TRANSFER-READMISSION-068/README.md)和[070四头定义](../VLM-SEMANTIC-ROLE-FACTOR-070/README.md)。确认074唯一尚未交付条件READY，073已闭合。没有丢弃Git改动/重置/重写历史或修改073原代码与清单的权限。

在首次包/研究资产读之前封本轮科学、独立核验、输入门/预算/Job/ledger代码与限额；不得先看旧分数设计新方法。一次有界ZIP目录/三元数据输入门可在正式根外执行，CPU≤30秒计入准备300秒；目录≤256项/8MiB、容器≤516MiB，拒绝链接/路径越界/加密/重复或歧义、超出固定成员/异常压缩比>100，不全目录解压。三元数据原字节与API sha、登记size及普通Git blob/LFS身份逐一核，不把签名/上游HTTPS认证强加给执行者用户副本。

根`repair_summary.a3_kept_invalid_qa_ids`须为无重复字符串列表、每ID唯一绑定原items；实际2条，两条均在ordering。**NOT_ORDERING之后、其余资格/排名之前，先按这份发布者清单整条排除。** 缺键/歧义/未知标记不得默认为空；独立核验必须从原根重新读该键并验证其影响，不能只复现生产分支。原已删除/其他repair统计如实审计，不按不理解的修复字段改答案。

除此之外逐字保持073/072科学规则：唯一items/qa-video-format、ordering_3/4及明确事件ID→非空语义文本/原未决标记、相同时间词黑名单、严格062 before模板/tau与精确绑定；四事件按ID UTF8前三。只使用无答案观察投影，canonical JSON sort_keys=True/separators=(',',':')/ensure_ascii=False，`SHA256(b'VLM072/select/'+observation_bytes)`全digest再观察UTF8平局，每发布video取最小、再全体前24。不得将correct_order有效性加入筛选、按073失败组位置临时补位或看模型结果选样。

预期修正版互斥分区：2218非ordering/2根无效/12时间词/91eligible；K24（6三/18四），与073保留23组、按统一规则改变1组。先封新选择/排除，再绑定完整原order并生成每组6问/3Yes3No：预期144有效标签、0unknown、28精确问题文本（含tau）、24媒体/103041283B/max10989839B。这是负责人事后元数据预览，**不是首次盲选/预注册或074本地已执行事实**；本地须独立重建核同一清单，任何差异持久化后STOP，不调规则凑聚合。

分别保存无答案observations和评分专用labels，不让GPU/旧头角色读correct_order、原question/answers、来源/组ID或另一个问题的预测。标签仅PUBLISHER_ORDER_DERIVED/exact-complete-order；非重叠/唯一发生/严格完成语义未认证。六排列仅原符号计划，真实重排继续HOLD，不构造新视频。

## 3 媒体、旧资产与输入接口

完整包门与元数据重建通过后建独占新074根。只对上述24成员流式读/写及校验登记size、普通blob/LFS内容identity，保存私有输入/路径/时间/代码seal，原metadata和媒体只读。视频大小是已知发布值，实际字节/解码成功仍待测；不缺省CRC/hash/碰撞检查、不转码/裁剪/改选更小文件。

仅沿既有精确handoff/asset catalog读取063/062/060/057及070/068的必要封存链：六seed137/263/419/557/733/911，063原C_NATIVE/D_NATIVE12个final头、070 CONCAT/FACTOR/REVERSE/ANCHOR24个final头，原C_CENTER/D_ROLE及070交换不变分量的train84 mu/标量RMS，原42canonical训练文本/锚及所需已封存S或h/h(tau)。不读旧训练/验证/开发答案、旧逐项正确性或分数来选配置，不生成新初始化/训练计划/统计/锚规则。资产身份/shape/finite/seal缺失即STOP，不递归搜索旧私有盘或重新训练。

原Qwen3-VL本地权重/配置/processor/库环境不变：bf16/SDPA，12真实帧/6tubelets、224RGB、原均匀中点/最近PTS和原068允许的clock条件；主visual merger输出空间池化V[6,2560]、纯文本最终decoder最后有效token h[2560]。严格复用原接口/层/统计/精度；不换32帧、动态分辨率/池化层或隐式CFR时间定义。静态审查完整未执行路径，最多一次CPU processor-only合成12帧fixture（无模型权重/真实feature/旧头forward），不把软件预检当科学效果。

旧metadata/ledger仅允许必要身份/闭合/输入碰撞/精确缓存索引。逐层核实际可得旧媒体内容/RGB/prepared pixels/文本tokens/model identity；未存层写UNKNOWN，不重跑旧输入补证。相同模型输入若有完整CLOSED且身份闭合的feature，直接复用并计REUSED；未决STARTED或身份冲突停止，不换父ID再问。文本精确去重，锚只复用旧缓存；缺锚不能追加Qwen调用。实际准备输入与完整code seal均须在首次真实解码或模型STARTED较早者之前封存，之后不改科学代码/重新解码或恢复失败输入。

## 4 一包直接跑完，不训练

媒体/资产/processor/输入身份通过即同包进入：解码封存→一次GPU冻结提取→CPU冻结旧头→完整输出seal→评分及独立核验。不得只交准备统计后再申请一轮。

- 模型只当前原生视频与当前问题的分离特征；高层V≤24、q≤28、合≤52，新调用扣除合格旧缓存；逻辑输入与实际调用、内部visual/decoder/root hooks和别名分开计。没有B0/generate/预热/探针/backward/optimizer；基础模型直接答题本轮NOT_RUN，不声称完整基准leaderboard。
- 六方法六seed共36旧头，每头原356673参数和固定末步state，全部eval/frozen。C按原C_CENTER，D按原D_ROLE；070四臂逐字用原S/R、两32维投影/dup/attention/读出及ANCHOR规则，不换平均/均匀权重。logit>0为Yes、0为No，非有限为失败，不强制互补/改答案。
- 36×24×6=**5184计划逻辑单项**，不把重复文本合并预测或把同视频重复六次编码。精确旧已CLOSED的同state/同V/q输出只能身份闭合复用，不重新forward；报告实际新forward/缓存/别名及逻辑守恒。没有任何重新训练/微调/选seed/checkpoint/阈值/层/normalizer。
- 首次GPU前非阻塞共享锁/free≥18GiB，最多一次GPU信息命令；忙则GPU_BUSY，不等/轮询/杀其他进程。持久化每调用/头单项STARTED/CLOSED与累计deadline；所有Job闭合/exit0/actualactive0和feature/output seal完整后，评分角色才解析原order/派生labels。

## 5 固定指标、配对和独立核验

主指标**每视频6问全部答对率**，计划分母始终24；次指标单项准确率（144）、每视频3个反向问题对互补率（72对）、六问预测恒定视频数（24）。响应/互补变化不代替答题收益。未知执行/未知标签分别列；不完整条件指标NA，不能仅按已完成子集算分或将未执行填0。不是旧四格分数的同分母比较。

36条件行，方法按C_NATIVE/D_NATIVE/CONCAT/FACTOR/REVERSE/ANCHOR，seed固定原顺序；保留计划/new/reused/CLOSED/INVALID/FAILED/NOT_RUN/execution_unknown/scoring_unknown及各整数分子。五个固定六问全对差：**D−C（主）**，FACTOR−D/CONCAT/REVERSE/ANCHOR（对照），各六seed，共30paired行；记录独对/对方独对/都对/都错/unknown/net和pp，不选冠军或临时加子层/对照。

只做五差×两轴=10个95%均值区间，无p值/等效检验/其他bootstrap：每个比较公开seed-sum差−6..6的13箱（计数和24/加权和=六seed净值），共65箱；每个边际按值升序规范展开。视频轴每比较重置random.Random(55074)，10000次choices(range(24),k=24)，`100*sample_sum/(6*24)`；seed轴每比较重置Random(55075)，10000次从固定六seed抽6个净值，同样除144乘100。分位为(10000−1)p线性插值。边际直方图不保留真实跨比较成员对齐，不做差分中的差分/联合推断。阻断时仍交36/30/10/65计划行，频数/指标NA、draws0/planned_draws10000。

发布video ID是最高可识别采样单位，原录制/参与者/旧源与预训练重叠UNKNOWN；24不是物理独立认证，144/5184不能当独立n。完整时若D−C均值≤0或正差不足5/6seed，关闭当前D多事件迁移投入；其余只记`NATIVE_MULTIQUERY_TRANSFER_PILOT_SIGNAL / SELECTIVITY_AND_NOVELTY_UNCONFIRMED`，不补认063原20%门、不恢复070失败配方。原生六问没有相关/无关时间交换的视频干预，不能称已学得问题相关时间交互或核心创新。

独立核验不import生产selector/scorer，不解码/重跑模型或头；从原三副本重新读根无效清单及全部资格/排名/新24绑定，核旧state/normalizer/anchors、封存/调用/5184键、标签/36条件/30配对/65箱/10区间及全部预算/失败/Job闭合。只读torch可核状态和seals，无真实forward。若资源/身份/形状不合，先持久actual/limit/reason/阶段/已完成与剩余，正常闭合自身Job并STOP，不恢复已STARTED输入。

## 6 新预算与精确交付

| 范围 | 上限 |
|---|---|
| 负责人新媒体获取（明确批准后） | 固定24逻辑GET/累计正文512MiB/网络外层900秒；真实发布总103041283B |
| 本地Codex研究网络 | 0；仅用户交接包，Git文档fetch/push另计 |
| 本地包读取/解出 | ZIP整体身份hash≤516MiB一次；所选压缩载荷≤512MiB、媒体解出≤512MiB各一次；三metadata逻辑读累计24MiB |
| 解码 | 遍历≤100000实际帧/监督≤900秒；每视频只一次，输出仍12帧 |
| CPU准备/身份/软件预检 | 累计监督≤300秒；模型身份hash另≤12GiB一次，记录真实耗时；输入门/宿主操作计入闭合说明 |
| GPU | 单次冻结加载/累计≤600秒/allocated≤16GiB，V24+q28≤52高层调用；GPU Job RAM≤32GiB |
| CPU旧头/评分/独立核验 | 累计监督≤600秒；计划5184单项，训练0 |
| 旧feature/views、旧state、旧metadata/ledgers | 分别累计逻辑读≤128MiB/64MiB/64MiB；必要旧模型权重读取单列，不复制模型 |
| 新独占根/起始free/父wall | ≤3GiB/2048文件、free≥4GiB、父≤10800秒；首次同步前持久起点，不回溯补造 |
| CPU Job/同时active/线程 | RAM≤8GiB/active≤4/线程≤4；计累计实际，进程总数不充同时活跃数 |

完整监督代码/父时钟/初始free实际值/阶段和读量先落盘，不能再只留predicate而认证全预算。文件快照不等于硬配额，逻辑读不等于物理OS I/O；未覆盖宿主操作如实列。环境/安装/付费API/新训练/旧媒体/新手工标签/剪接或符号媒体/论文0，旧根/锁/账本不改，不杀其他进程。

精确10处统一交付，研究开始后成功/部分/阻断均保留分母和失败：

1. `prototypes/multievent_frozen_transfer_074.py`
2. 本目录`execution-receipt.md`
3. `admission-summary.json`
4. `scientific-results.md`
5. `condition-summary.csv`（36行）
6. `paired-summary.csv`（30行）
7. `mean-intervals.csv`（10行）
8. `difference-histogram.csv`（65行）
9. `execution-summary.json`
10. `docs/codex-results.md`只尾增一次本父记录

不改073/任何历史代码与失败、论文、规划或本README。不公开原元数据/QA/事件/答案/逐项logit预测或正确性、成员IDs/路径/hash/来源映射、私有路径、特征/权重/媒体；仅聚合统计和科学代码自身LF SHA。核精确暂存/results历史前缀，普通安全push main后STOP，无后台/自动075/调参/续下载或扩预算。
