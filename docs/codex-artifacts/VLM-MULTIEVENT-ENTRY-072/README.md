> **2026-11-01归档：072_CLOSED / ACCEPTED_BLOCKED_DELIVERY_WITH_CONNECT_DEADLINE_CAVEAT / SCIENTIFIC_NOT_RUN。** [9af6b12](https://github.com/floomeer83felix-source/vlm/commit/9af6b121b8253823469c93f3e9a7bcee3a81a662)首入口停于TCP连接，实际HTTP GET/响应/正文0，另两入口未运行；15秒socket timeout未落实整个连接阶段总deadline，不能认证完全资源合规。[负责人验收](../../research-decisions/post-072-connect-stop-and-offline-handoff-2026-11-01.md)106项公开检查通过，只验收阻断事实，未审查数据或构建清单。下文是原合同完整归档，不是当前许可；唯一条件READY转[073用户文件离线构建](../VLM-MULTIEVENT-OFFLINE-073/README.md)，文件未齐只等待，不重试下载器、不交空包。069继续暂停、070关闭。

# 072 固定多事件数据入口、构建多问题清单，停止两事件换头

2026-11-01（北京时间）｜ChatGPT研究负责人。**唯一条件READY：METADATA_ONLY_AWAIT_EXPLICIT_START。** 用户要求继续探索且不写论文，071已完整验收，070配方仍关闭。依据[071验收/下一步](../../research-decisions/post-071-review-and-multievent-entry-2026-11-01.md)。本包涉及一个新公开数据源，只有用户在本地Codex新消息明确072和**公开小元数据累计≤4MiB**后执行；原071下载0不转余额。未授权不发请求、不建研究根或消费父任务。这里无媒体/模型/GPU或训练权限。

## 1 同步与唯一候选

安全同步独立文档main，读AGENTS、最新看板/总览、本合同及071验收/科学结果；确认唯一尚未交付条件READY为072，results无本ID。069仍PAUSED_BY_USER，不写论文，不继续071或重问旧模型。本轮不需要读取任何旧私有研究根、预测、标签、模型/头/特征/训练计划/媒体。

只审计作者发布候选`anonymous-video-benchmark/toc_bench`，固定revision **da3065053d958c38151304e33a42e138b1899eaf**。匿名/尚未发表是来源范围，不当成公认基准或原创性保证。三个且仅三个逻辑HTTPS GET入口，每项最多一次，无重试/换版本/扫描替代数据：

1. `https://huggingface.co/api/datasets/anonymous-video-benchmark/toc_bench/revision/da3065053d958c38151304e33a42e138b1899eaf?blobs=true`（固定仓库身份/文件元数据）
2. `https://huggingface.co/datasets/anonymous-video-benchmark/toc_bench/resolve/da3065053d958c38151304e33a42e138b1899eaf/README.md`
3. `https://huggingface.co/datasets/anonymous-video-benchmark/toc_bench/resolve/da3065053d958c38151304e33a42e138b1899eaf/answer_final.json`

不取data/test.jsonl的重复全表、不用datasets.load_dataset、不运行远程dataset脚本、不取视频/图片/模型或对媒体发HEAD/Range，不取旧Breakfast/Charades/其他来源文件。仅以上元数据正常服务重定向链最多3跳/请求，失败与重定向正文也计预算，不带凭据/令牌、不绕过登录/许可。API体≤2MiB、JSON体≤2MiB、README≤32KiB，并共同受**累计4MiB**约束；流式读写、请求STARTED/字节/终态先行。network outer累计≤180秒，connect≤15秒、无进展read≤30秒，不能重置累计量。拒绝HTML错误页冒充JSON/归档。

先核API返回sha、目标文件真实size及blob/LFS内容身份，区分普通Git blob SHA1与LFS SHA256；JSON实际内容须匹配发布固定版本身份，不能只自算hash便称认证。保留原始metadata私有副本及请求账本。不解释API里video文件大小/oid为媒体已下载或已许可。缺身份、响应超限、gate/HTTP失败立刻具体停止，交已有观察，不补GET或换候选。

## 2 原始schema和资格核验

README目前声明2323 QA、ordering_3=52、ordering_4=53及events/correct_order等；这些是待核声明，不直接当实测。找原bundle中唯一具有qa_id/video_id/format的条目集合，保存实际根字段/schema，核总量/各题型/源类别/重复ID。只能按明确的原字段结构解析事件ID→原事件文本及correct_order；字段只有ID而无文本、多个冲突映射、未解决标签状态均不能用猜测/LLM补齐。README与bundle不一致分报实测和声明，不修原文件。

下载/预算/安全/日志代码先封存；允许一次有界schema观察（不公开QA/答案），随后在正式选择前封存完整解析/选择/构造/独立核验代码及源身份。规则如下预先固定，不按标签方向或模型分数改变；schema适配与失败成本如实报，不能说所有代码在首次元数据读取前已冻结。

候选只取原生ordering_3/ordering_4。资格需：原qa_id与发布video_id/路径绑定明确；事件ID/非空语义文本一一对应且至少三个不同事件；没有原发布者未决/不确定标签标记。事件文本只允许strip和空白折叠，禁止语义改写/翻译/从正确顺序造描述；不把event1/2/3当语义文本。原描述若含整词`before|after|first|second|third|fourth|then|earlier|later|finally`，记EXPLICIT_TEMPORAL_WORD_IN_EVENT排除，避免用文本自带排序作视觉证据。文本含引号/转义等必须通过原062严格tau的逐字解析/双交换回原串和事件绑定，失败排除，不放宽parser。

对每个原生条目，先按事件ID的UTF8字节序取前三个事件（四事件题也取前三，不用correct_order选事件）。构造观察投影：源命名空间、原video_id/qa_id/媒体路径、所选三事件ID与原文本；不含correct_order/答案/模型分数。每发布video_id仅保留一个候选，按`SHA256(b'VLM072/select/'+ canonical_JSON(observation).encode('utf-8'))`完整digest升序、再完整观察字节打破平局；canonical_JSON明确sort_keys=True,separators=(',',':'),ensure_ascii=False，先每video取最小，再全体排序取前24。先封观察名单/规则/排除表，再绑定正确顺序；不按文件大小、答案方向或后验有效数补样。24不足就取全部并报告不足，不重新选择。

之后核原correct_order是否是全部原事件ID的完整唯一排列、无缺项/未知。过滤到已选三个事件，得到其发布者原生次序。所选条目失败保留原计划位置/unknown，不用后排替代。每视频六个有向事件对全部生成：

`Does the event "<原事件文本A>" happen before the event "<原事件文本B>"? Answer Yes or No.`

标签仅由原排序中pos(A)<pos(B)机械派生；必须每视频3是/3否、反向问题互补、tau闭包且双交换回原串、与原event ID/text逐项绑定。模型问题不带ID/序号/完整事件列表/正确顺序/来源或原question中的排序提示。它是**PUBLISHER_ORDER_DERIVED**证据：不能把完整排列自动升级为动作非重叠、物理唯一发生或严格完成时间语义。若原排序含义不明确，六问标为条件性标签计划，不宣称正式可评分。

通过API文件元数据/原video_path或唯一明确原ID映射核媒体locator/发布size/内容identity，禁止凭相似名字猜路径。无明确映射就MEDIA_LOCATOR_UNKNOWN，不另发媒体HEAD/下载。记录源许可/混合源保留条款、旧数据潜在重叠可证层级和缺口；没有原录制/参与者或旧源映射就UNKNOWN，不能仅凭新video_id认定无污染。匿名数据集卡不能替代第三方媒体权限，未来须逐源确认并新授权。

## 3 实际构建与真实重排的边界

一轮必须生成完整私有manifest：固定成员/三事件/原order/六问题与标签、来源与file locator/size/identity、资格与排除理由、未决项/代码/输入封存及校验记录。不只交文献综述。若K≤24全部有效，原生清单6K个未运行问题；K=24即144个，媒体/模型均NOT_RUN，准确率NA。

同时为同三事件生成**仅符号的六排列×六问=36K格计划**，每排列3是3否；六排列的相邻位置交换有12条有向边，每边2问翻转/4问保持，共72K个边问题关系（24K翻转/48K保持）。K24时864格、1728关系，其中576翻转/1152保持。问题文本在各排列相同，不依照标签改问法。

这只验证构造逻辑，**不是已经生成六种真实视频或新科学准确率**。逐项核原metadata是否确有三个事件的明确非重叠边界、边界时间单位/媒体时钟、唯一发生及可剪接依据；缺任何一项，真实重排必须CONTROLLED_MEDIA_CONSTRUCTION_HOLD。不以六tubelet或整段DyBench二事件视频拼接替代三事件，也不凭原ordering label猜剪接点。原生多问题入口与受控重排入口分别报告，不用前者PASS掩盖后者HOLD。

输出状态最多为`FIXED_MULTIQUERY_LABEL_PLAN_READY / MEDIA_AND_COUNTERFACTUALS_HOLD`：要求原生标签/问题/绑定全合格、24唯一发布video IDs（不认证物理独立）及媒体locator/size可核。若不足/有未知则`PARTIAL_OR_NO_MULTIEVENT_ENTRY`，分列实际valid/invalid/unknown，不称新benchmark已就绪。若确有完整边界证据只列证据和条件，仍不取得本轮媒体/模型权限。

## 4 下一实际评估方案必须可审阅

`evaluation-plan.md`按本次实测K/文件字节/unique V与q列出未来原生多问题评估的精确数据/标签层级、与旧模型接口相容性、来源许可/重叠/clock/token等缺口和预算；不能直接安排训练或选择当前“冠军”。可提出一次冻结C/D及070四臂×六seed的36头比较：K24时24新V、至多144q（含tau闭包），最多168 Qwen特征高层调用、5184 CPU单项预测，全部native未知项保持分母。拟定上界GPU600秒/allocated16GiB、媒体总512MiB/新根3GiB/实际CPU解码10万帧及900秒，**这里只是待另审提案**；若所选实际元数据不合上界就具体HOLD，不换小视频补样、不申请整个15GB包。

不能把144问题当144独立来源，统计最高单位是K个发布video_id，原录制依赖未知；新生成问题未评分不等于原答案未公开/预训练无暴露。受控六排列的未来预算须另列缺失边界/媒体证据，不能用原生24视频的预算冒充144重排视频。没有新受限授权就不进入模型/媒体阶段。若入口不可行，一次说明决定性缺项，停止本候选，不自动再开另一个小数据检查父任务或改头。

## 5 独立核验、预算和交付

独立核验不import生产解析/构造器，从原封存metadata单独复算根/题型/源/重复分母、每个排除/固定观察排序、无标签选择、24/实际K名单与unknown保留、事件ID/text/order、六问/模板闭包/平衡、原生标签及仅符号36/72格、媒体路径/identity与计划预算，核网络实际/字节/阶段/资源/旧文件未改。只允许整数/文本构造软件fixture验证逻辑，训练/forward/准确率0。

新独占私有根≤32MiB/256文件、起始free≥128MiB；CPU准备+构造+独立核验监督累计≤300秒，parent≤3600秒含编辑/网络；Job RAM≤1GiB/active≤2/单线程。原始数据/派生问题/标签/成员/媒体映射留私有根，不能上传此公开仓库。不读旧私有研究文件、torch/模型/特征/视频/processor，GPU/nvidia-smi/媒体请求/下载/训练/推理/论文/安装/环境改变全0；仅列明三小元数据GET属于本新授权。只管自身Job，不清旧锁/账本或杀其他进程；不足/失败先落reason/actual/limit/阶段再停，不重试。

精确七处allowlist：

1. `prototypes/multievent_entry_072.py`（显式入口，导入无网络/数据或研究操作）
2. 本目录`execution-receipt.md`
3. `admission-report.md`
4. `admission-summary.csv`（原题型/源类别/互斥排除/已选valid-invalid-unknown等聚合，不含逐成员）
5. `construction-summary.json`（实际分母/选择规则/原生与仅符号计划/证据层级/映射许可未知/网络预算/核验/资源/code LF SHA）
6. `evaluation-plan.md`
7. `docs/codex-results.md`仅尾增一次本父记录

不得公开原QA/事件文本/答案/六问逐项标签/视频ID或路径/逐项hash/源映射/私人路径/媒体或模型；可列公开dataset revision/官网URL、代码hash和聚合计数。核精确暂存/脱敏/append-only，普通安全push main后STOP，不自动073/媒体/模型/训练或论文；负责人验收同回合给下一具体决定。
