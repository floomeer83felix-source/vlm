> **2026-11-02已按真实启动阻断验收关闭，不续跑。** [0dc7267](https://github.com/floomeer83felix-source/vlm/commit/0dc7267e90713e53494862a7390bfac2e4f6426a)在native线程4>1时自身Job停止，fixture/构建/数据oracle/训练NOT_RUN。[验收](../../research-decisions/post-077-stop-review-and-integrated-training-2026-11-02.md)65公开检查保留资源覆盖缺口；未执行字段/大小guard问题另建078组件修正，不回写077。唯一下一[078完整RGB训练包](../VLM-TIMESTAMPED-TRIPLES-TRAIN-078/README.md)待新媒体/GPU/训练明确批准。以下原合同按当时状态逐字保留，旧READY不构成新授权。

# 077 时间段标注三事件：离线构建与后续训练方案

2026-11-02（北京时间）｜ChatGPT研究负责人。
**唯一READY：CPU_METADATA_CONSTRUCTION / AWAIT_LOCAL_ZIP。** [076验收](../../research-decisions/post-076-review-and-timestamped-triples-2026-11-02.md)已关闭当前TOC-Bench入口的新适配器训练。这里换为带时间段标注的新开发构造，不改prompt/头继续试076。069仍暂停。

## 1 一次范围与输入

按AGENTS安全同步独立文档main，核本ID无已有完成/部分/阻断结果。用户交接本地`PT_077_timestamp_metadata.zip`：**390919B，SHA256 `950ae2f6766179743f27e512948730682e444eb1c235393d034e508081224cd2`**。完整包12成员、总解压1104895B；唯一`package-manifest.json`列其余11文件size/SHA。校验无重复、路径穿越、绝对路径、链接、加密，CRC全部通过；只在新私有根抽取。未给本地路径或包不可达只等待输入，不扫盘、不建根/append/交空阻断包。实际读到身份/预算/内容失败则记录实际、阶段、限额，按一次父包完整回报失败，不修换输入再跑。

包包含原`action_localisation_train_annotations.zip`、`source-README.md`、`source-receipt.json`、`archive-tail.bin`、`central-directory.bin`、`archive-directory.json`、`source-registration.json`、`owner-rule.json`、`owner-preview-summary.json`、`owner-selection-frozen.json`、`DATA-LICENSE-NOTICE.txt`和manifest。内部原标注ZIP唯一JSON为2692679B、原ZIP222956B，SHA256 `5b27beaa97df0a1ea258437b179ed17092981a93501a22a572d64dd46fb12575`。两层ZIP都核固定allowlist和解压上限；禁止递归扫描其它档案。

源码/来源固定官方[Perception Test](https://github.com/google-deepmind/perception_test/tree/3938d2f1ba3a6b502025741cea4cd73c7b3bdfaf)，README Git blob505cd675d6759962202747c2fd4970074a027df4；数据CC-BY-4.0/软件Apache-2.0，保留归属/修改说明。annotation generation1686575055001154；视频archive generation1685446268139925、ETag `"-CJXz5tD4nP8CEAE="`、总28404087974B。目录171100B、SHA256 `505019446df7a796909c8f00a63bd55a2e214d3ba533de00104001f0a30aac82`，2184记录。负责人只取了标注和目录metadata，没有媒体内容；目录/ETag不等于整个archive或视频内容hash认证。

本轮研究HTTP/HEAD/GET/Range、媒体成员读/下载/解码、processor/Torch/Qwen/头forward、GPU/训练、环境变更/安装、手工标签、旧私有根/QA读取及论文全部**0**。Git文档同步不计研究网络。不能把包内URL视为联网授权。

## 2 本轮一次完成的实际构造

用Python标准库写可运行的`prototypes/timestamped_triples_077.py`；数据清单、标注、实际问题/源ID/时间戳/ZIP映射仅存在用户新私有根，不上传GitHub。不只交schema/复制负责人统计。

原JSON顶层2135视频，13644动作；逐条验证metadata.video_id/官方train、有效fps/num_frames、每视频annotation_id唯一。所有行均入准入计数，失败不得消失。整视频label做strip+空白折叠，归一化后计数；只允许非空且全视频恰一次的文本，排除whole-word before/after/first/second/third/fourth/then/earlier/later/finally（大小写不敏感）。保留原label_id/文本/annotation_id/边界，不用LLM改写/新标注。

每段timestamps微秒和frame_ids均为两个有限数、0≤start<end、duration∈[0.5,8]秒；timestamp end≤(num_frames+1)/fps，frame0≤start<end<num_frames。两个端点timestamp与frame/fps误差≤一源帧+1e-6秒。段内12个均匀中点，元数据最近索引`floor(t*fps+0.5)`须12个互异且在标注frame区间内；这只是metadata计划，不声称真实PTS已核。时间排序选所有三段组合，相邻结束到开始gap≥100000微秒，三文本互异；只认动作**标注段出现顺序**，不认证动作原子完成/唯一实际发生。

事件槽按numeric annotation_id升序，问题模板严格为`Does the event "{}" happen before the event "{}"? Answer Yes or No.`，六有向问题严格regex回读恰绑定两原文本；特殊文本导致歧义必须拒绝并计数。观察结构固定：`{source:"PerceptionTest/action_localisation/train",video_id,events:[{annotation_id,label_id,text,timestamps_us,frame_ids}]}`；canonical JSON `sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False`，UTF8；digest=SHA256(`VLM077/pt-triple-v1/`字节+canonical观察字节)。每video选digest、canonical字节最小候选；该video在官方目录必须有唯一filename stem匹配，核完整安全member路径。所有video-best再同规则排名取前32，不挑文本/模型得分/更易媒体。目录必须独立解析ZIP64 extra/offset，不能拿owner解析JSON当唯一证据。

按固定排名0–19 train20，20–23 development4，24–31 test8。先固定source group split，再枚举六事件排列（itertools.permutations(0,1,2)顺序）×六有向问题同顺序；六种变体不能跨split。实际私有manifest包含全部32组、源边界/12计划采样点和索引/媒体size CRC method offset/6问/6RGB拼接计划；公开只汇总。未来每段12真实RGB帧、三段共36帧，6种block拼接、统一12fps/3秒运行时钟，192变体；**本轮不读帧、不输出视频、不做latent特征重排。**

构造1152符号答案，每排列每问按两个槽位置先后定Yes/No。相邻位置交换两种×6排列=每组12有向边，每边对六问判FLIP/HOLD，共2304关系（768FLIP/1536HOLD）；存label difference及关系，不混为2304独立视频。每同问跨六排列3是3否；固定q-only分类器单项恰50%、每组36项全对上界0，逐组逐问证明。训练只可读train20监督；dev4用于未来预先规定选择；test8禁止未来调参回流。本轮数据构建必须读取公开GT，故不称新盲测。

负责人preview参考为1376候选/280eligible/32选中/29动作文本；压缩581426975B、解压579702574B、最大70872100B。**独立计算所有数和选中digest/观察后才比owner-preview与selection**；不同则停止资格、不以参考覆盖实际。保留根JSON所有行/拒绝原因/身份异常计数。32不够不能换规则填数。

## 3 独立核验和一次可执行后续方案

构造及独立review完整源码须在正式读取annotation/selection之前封存SHA；先核输入ZIP身份/成员允许。review不得调用生产筛选/排序/标签函数，用原metadata独立筛选（边界采用有理数/整数微秒交叉核浮点阈值）、解析目录、重建排名/split/1152键与标签/2304关系、计数/不交叉split、q-only恒等式。预写完整核验，不能看结果后再增加检查并追称全部事前。对owner-preview只做最后比对，不视为数据标签/独立核验的替代。

同时写`training-plan.md`：下一父包应一次完成**实际RGB构建+同冻结主干特征+匹配小规模训练/评估**，不要继续拆成几个无模型审计。这里只拟具体方案，不执行也不授权它。至少写清：

1. 精确32成员目录身份、method12/BZIP2和ZIP64、本地header/必要Range计划、固定generation/ETag、CRC/size/内容hash、失败不重试及**不下26.5GB整包**；明确未来32媒体压缩581426975B已超旧512MiB。按实际有界成员Range/header开销给新的完整预算、预计存储、frame/CPU/GPU秒数及峰值，不借旧许可。实际PTS/边界/帧数/相邻段不重叠和固定时钟验证如何在模型前完成；视频不足/坏帧保留分母并停，不换样。future budget必须可执行、过紧或不能从metadata确定之处显式UNKNOWN，不伪造运行测量。
2. 全部新变体必须从真实源RGB采样再拼接，实际相同段帧字节跨排列复用，音频不入模型；输入只当前视频+当前问题，不喂annotation_id/source/permutation/GT边界、label_id/另一个问题输出。分组辅助信息只可供train监督，推理不做强制互补/按组修复。新数据不代表新来源：Perception Test也是TOC-Bench来源，旧录制/参与者/像素/预训练重叠UNKNOWN；未来去重只在另立精确范围后，不能在077扫描旧根。
3. 同一冻结Qwen、本地现有环境；明确新特征接口/视觉token预算与构图，不沿旧失败小头反复调参。比较基础模型、相同参数普通适配器（仅答案监督）、**相同架构/参数/数据/seed/更新/优化器**的联合FLIP/HOLD监督，以及同训练图的**question-relevance关系打乱控制**。打乱须真正破坏“该相邻变化与当前问题的相关性”，不能只是把仍等价的问句方向交换；答案监督不打乱。明确CE与联合损失、权重、架构参数数、seed/步数/采样、唯一开发选择规则、测试封存/一次评分、所有逻辑和真实新调用/精确别名。训练计划应小而完整，时间预算诚实估计，未运行就标ESTIMATED。
4. 评价单项、36项整组、相邻交换四格、问相关FLIP和无关HOLD分别答对（只变表示不算收益），保持源组分母、配对源组不确定性和小样本限制。联合机制须胜过同预算普通适配器及打乱控制才保留，不能仅胜基础模型；给预先可计算的整数/均值投入门，不按结果换门，不把20训练组试点当可发表证明。后续换数据验证仍待安排，不能把官方train中切出的test8称外部确认。

现成反转/时间适配器/反事实训练本身不算创新；077不证明新机制，不恢复070，不写论文。若metadata通过但未来媒体/GPU预算未批，正常交付资格与具体提案，不为缺未来授权将本轮空置。

## 4 独立资源与完整交付

| 本轮资源 | 上限 |
|---|---|
| 研究网络/媒体成员/模型/GPU/训练/论文 | 0 |
| CPU构造+独立核验累计 | 300秒；标准库，无安装/新环境 |
| CPU Job峰值/同时active/每进程线程 | 1GiB / 2 / 1；不import多线程数值库或codec |
| 明确交接的输入/新中间件累计逻辑读取 | 32MiB，含hash/解压/核验；共享cache按实际计，不把逻辑读称物理I/O |
| 新独占私有根/文件数 | 32MiB / 256文件；输出manifest/监督/关系/代码/账本均计入 |
| 初始free/父总时间 | ≥128MiB / ≤3600秒，从同步前持久起点 |

按现有有界Job/累计deadline框架，先持久父起点、初始free、预算/锁/代码seals；准入前允许只读明确ZIP路径size及hash/目录。禁止杀其它进程/删旧锁/回写旧根。留完整actual/limit/coverage/STOP阶段、已完成与剩余、自己Job退出闭合；全面OS/物理I/O/硬磁盘覆盖未知就如实写UNKNOWN，不以计数代替认证。一次程序软件fixture及正式完整构建/独立核验均计300秒，失败不改规则再构建同父。

精确**七处**Git交付：

- `prototypes/timestamped_triples_077.py`
- 本目录`execution-receipt.md`、`admission-report.md`、`admission-summary.csv`、`construction-summary.json`、`training-plan.md`
- `docs/codex-results.md`仅一次本父追加

CSV按train20/development4/test8/total四行，planned/actual source groups、variants、questions/answers、FLIP/HOLD、媒体compressed/uncompressed、资格/unknown；JSON含全部来源/选择规则/预览比对/不交叉split/q-only证明/独立核验/资源/后续状态。私有JSON/逐项标签/文本映射/媒体成员和时间戳表不得上传。公开可含官方source URL/revision/全局hash/汇总；不含私有路径/凭据/原始QA或reidentification map。README/负责人看板/决策/历史和其它父只读。

最高成功状态`TIMESTAMPED_TRIPLE_SUPERVISION_READY / RGB_NOT_CONSTRUCTED / TRAINING_NOT_RUN`，未来模型成绩均NA。失败也交实际分母和完整原因，禁止符号答案被说成模型准确率。安全审查、只stage七处、一次push main后**STOP**；不自动078、不下载/训练、不后台等待。负责人验收后给下一指令。
