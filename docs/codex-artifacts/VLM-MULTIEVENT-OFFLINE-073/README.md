> **2026-11-01归档：073_CLOSED / ACCEPTED_PARTIAL_DELIVERY_WITH_IMPLEMENTATION_FAILURE / ADMISSION_FAIL / SCIENTIFIC_NOT_RUN。** [bb2adae](https://github.com/floomeer83felix-source/vlm/commit/bb2adae8dd640916a3903ebad07cec12b8fe339d)真实构建24组/144问，但漏读发布者根无效清单，选入1个无效组/6未知标签，原清单不得评估。负责人1952项原副本/公开检查确认失败；不追认963项复现为全合同合格，不修跑本ID。下文原合同完整归档，唯一条件READY转[074修正版原生六问实际评估](../VLM-MULTIEVENT-FROZEN-074/README.md)，须新媒体/GPU明确授权及完整本地包；070保持关闭、069暂停。[完整验收/明确的新版本](../../research-decisions/post-073-review-and-native-multievent-evaluation-2026-11-01.md)。

# 073 本地元数据离线核验与多事件清单完整构建

2026-11-01（北京时间）｜ChatGPT研究负责人。**唯一条件READY：WAITING_USER_METADATA_FILES / OFFLINE_INPUT_GATE。** [072验收](../../research-decisions/post-072-connect-stop-and-offline-handoff-2026-11-01.md)确认无源正文、连接总deadline有缺口；072关闭。本包不修下载器、不发任何网络请求。用户提供输入后，一包实现完整构造器、固定清单和标签、独立核验及未来方案，push后STOP；069继续暂停、070/071不恢复。

## 1 用户交接的三个原文件

固定候选`anonymous-video-benchmark/toc_bench`，revision **da3065053d958c38151304e33a42e138b1899eaf**。用户用浏览器下载同固定版三份原文件到一个文件夹，并向Codex明确交接该文件夹；不要求或尝试自动控制浏览器：

- [API元数据，保存为api.json](https://huggingface.co/api/datasets/anonymous-video-benchmark/toc_bench/revision/da3065053d958c38151304e33a42e138b1899eaf?blobs=true)
- [README.md](https://huggingface.co/datasets/anonymous-video-benchmark/toc_bench/resolve/da3065053d958c38151304e33a42e138b1899eaf/README.md)
- [answer_final.json](https://huggingface.co/datasets/anonymous-video-benchmark/toc_bench/resolve/da3065053d958c38151304e33a42e138b1899eaf/answer_final.json)

下载原内容，不复制网页渲染文字/另存HTML；API需带blobs=true的文件元数据。三文件总≤4MiB，API≤2MiB、README≤32KiB、answer_final≤2MiB。**不得将文件、原QA/答案、路径或逐项来源映射推送公共仓库。** 浏览器取得文件是用户操作，073不认证其实际请求/流量或宣称旧072已取得正文。用户无需提供任何凭据。

## 2 输入门：未齐只等待，不交空包

安全同步独立文档main，读AGENTS/最新看板总览/本合同/072验收及[072原合同](../VLM-MULTIEVENT-ENTRY-072/README.md)科学规则。确认本ID无交付、唯一条件READY。只读用户明确目录中的上述三文件，不猜D盘路径、不递归找文件/旧根、不从072缺失源“恢复”数据。

每条用户启动消息只做一次有界输入预检：目录/文件存在、尺寸/总量、非HTML、API可解析且sha=固定revision/非private或gated，README/answer_final各有唯一登记、size与普通Git blob SHA1或LFS SHA256匹配实际原文件。输入预检只解析API文件和校验另外两文件字节，不先做QA/schema/选样。预检本次CPU≤15秒、只读源≤4MiB，可同缓冲复用。不修改原文件/格式来凑hash。

**任一缺失/错格式/版本或身份不符：只回复具体缺项和所需原文件，WAITING_USER_METADATA_FILES，不新建073研究根、不做schema观察/选择、不消费正式构建、不append或push阻断结果，不重试网络/轮询。** 用户纠正输入后可由新消息再次触发输入门，这是正式构建前的输入交接，不恢复已STARTED研究配置。输入门成本如实记入通过后回执，失败预检不能冒充科学执行。

输入门通过才建立独占073私有根，保存用户提供来源/文件身份/本次预检事实并封存只读副本。来源等级为`USER_SUPPLIED_FIXED_REVISION_COPY / OFFLINE_CROSS_FILE_IDENTITIES_MATCH`，不是执行者观测的上游HTTPS/签名/可信时间戳；API与内容的一致性不证明上游或媒体完全可信。不要使用AUTHENTICATED_REMOTE_DOWNLOAD或把用户浏览器流量记为073测得0B。执行者网络请求本身必须为0。

## 3 固定科学规则，不因离线改变任务

完整继承072§2–4的候选/科学定义和待审方案，072原说明已按当前归档标记保留。重点如下：

1. 原bundle实际根/唯一qa_id-video_id-format集合、总/题型/源/重复数量须实算；2323/52/53只作为待核声明。只用ordering_3/4，有明确事件ID→非空原语义文本/无冲突及原发布者未决标记筛查；不猜字段含义、用LLM改写或从order造事件描述。匿名审稿源只是候选，不称公认基准。
2. 事件文本只strip/折叠空白；含整词before/after/first/second/third/fourth/then/earlier/later/finally按原规则排除；原062严格tau解析、双交换、事件文本绑定不放宽。四事件题按ID UTF8取前三个，不按正确次序挑目标。
3. 选择仅观察投影（原源命名空间、video_id/qa_id/媒体路径、所选ID和原文本），不得含correct_order/答案/分数。canonical_JSON为sort_keys=True,separators=(',',':'),ensure_ascii=False；原`SHA256(b'VLM072/select/'+canonical_JSON(observation).encode('utf-8'))`完整digest排序规则**保留VLM072域**，不因新父ID改变既定选择。先每发布video取最小、再全体前24，digest平局再观察字节；先封规则/名单/排除，再绑定原correct_order，不足不补样。
4. 核原correct_order是全部原事件ID的唯一完整排列，过滤到已选三事件；原选中标签失败保持unknown/invalid和原计划位置，不用后排替代。生成每视频六个有向before原模板问题，每组3是3否、反向互补、tau闭包，问题不带ID/原顺序/来源/完整列表或原question排序提示。
5. 原排序派生关系仅`PUBLISHER_ORDER_DERIVED`，不认证物理唯一发生、非重叠/完成时间/媒体时钟。若排序含义不明保留条件性标签，不宣布正式可评分；ID文本/映射不明确就UNKNOWN，不从名称相似猜媒体。
6. 从api.json原文件元数据和原显式locator/唯一确定映射核发布媒体大小/identity；无映射就MEDIA_LOCATOR_UNKNOWN，**绝不HEAD/下载视频**。mixed-source/用户文件副本不授予第三方媒体权利；参与者/原录制/旧数据或预训练重叠无证则UNKNOWN，不仅凭新ID宣称独立。

先封输入门/文件只读/预算/日志代码；输入门通过后允许一次私有schema观察，代码适配实际原字段但不得改上述规则。只记录字段/类型/计数，样本QA和答案不打印到公开报告/控制台。正式选择前封完整解析/选择/标签/符号构造/独立核验代码及输入；选择STARTED后不改公式、名单或重做已STARTED构建。

## 4 本轮要交真正的清单，不仅是设计

新`prototypes/multievent_offline_073.py`必须实现显式输入门/一次私有观察/正式构建与独立核验入口；导入无网络/私有I/O/模型操作。**不调用072下载或observe入口，不把其90行脚本声称为已完成构造器。** 原文件不改；旧源码只静态参考。

私有完整manifest保留源/固定观察/三事件/原order/六问/标签/媒体登记/排除和未决状态/代码与数据封存；原生6K问真实生成后才计数，K≤24，K24时144问。没有模型运行，准确率NA。只执行必要的整数/文本fixture，不训练、不用虚构特征成绩当科研结果。

另生成仅符号6排列×6问题=36K格，每排列3是3否；相邻位置交换12有向边×6问题=72K关系，其中24K翻转/48K保持。K24时864格/1728关系，576翻转/1152保持。逐组核同问题文本、变/不变标签，**这些不是已经生成的真实视频或已评分反事实**。

原metadata有无明确边界/非重叠/唯一发生/时间单位/源媒体时钟及剪接许可分别列证据。缺任一真实重排条件就CONTROLLED_MEDIA_CONSTRUCTION_HOLD，未观察不能写成不存在，不凭六tubelet/二事件拼接或原顺序猜切点。原生多问题和受控重排入口分开，不用前者PASS掩盖后者缺项。

K24、所有原生标签/模板/绑定及locator/size可核，最多记`OFFLINE_FIXED_MULTIQUERY_LABEL_PLAN_READY / USER_SUPPLIED_SOURCE_PROVENANCE / MEDIA_HOLD`；不足/不明确则`PARTIAL_OR_NO_MULTIEVENT_ENTRY`，实际valid/invalid/unknown分列。不把输入门PASS当数据资格PASS。正式构建开始后遇到真正内容不合格，交完整事实/排除与现有产物并关闭该候选，不补样/换源或自动再开准备微批。

## 5 待审实际评估方案与边界

按实测K/原native V/q去重（含tau）/所选文件实际发布字节，完成evaluation-plan.md；不要重复纯声明上界。沿原072提案，K24时native最多24V+144q=168次Qwen特征、C/D及070四臂×六seed=36冻结头/5184单项；未来若维持旧接口须仍12帧/6tubelet、原层/统计/阈值，不选择冠军或训练新头。拟上界GPU600秒/16GiB、媒体512MiB/新根3GiB、CPU解码10万帧/900秒均只是后续待审提案，实际所选不合即HOLD，不换小文件或取整包。

K发布video IDs不是6K独立问题来源，原录制依赖仍未知；新派生问题未评分不表示原答案未公开或预训练无暴露。受控六排列媒体的144变体与native24分开，不借native预算冒充全重排；边界/许可/时钟不清就不给执行方案。073本身不产生媒体/模型/GPU/训练/论文权限。

## 6 核验、资源和一次交付

独立核验不得import生产构造器，从原用户提供三副本独立复算API revision/两内容身份、schema/题型/源/重复与各排除、观察选择和原封存名单、event ID/text/order/tau/六问标签与平衡、原生/符号规模及翻转保持、locator/size/许可未知、待审预算和全部状态。输入真实资格结果未知，不靠schemafixture或断言数冒充数据验证。

通过输入门后，CPU准备/构造/独立核验监督累计≤300秒，父≤3600秒，Job RAM≤1GiB/active≤2/单线程；新根≤32MiB/256文件、初始free≥128MiB。三原文件逻辑读（包括成功输入门/hash及独立核验）累计≤24MiB，私有源副本至多一套，记录实际读量与未计静态/闭合范围；不假称物理I/O/OS访问或硬配额证明。

本包网络请求/媒体GET-HEAD-Range/GPU/nvidia-smi/模型/torch/processor/特征/训练forward/论文/安装环境改变全部0，不修代理或证书、不清旧根/锁账本、不杀他人进程。只读用户精确交接三文件，不需要旧私有根或标签。只有正式构建启动后才执行以下七处统一交付：

1. `prototypes/multievent_offline_073.py`
2. 本目录`execution-receipt.md`
3. `admission-report.md`
4. `admission-summary.csv`（纯聚合资格/排除/已选状态）
5. `construction-summary.json`（实测身份一致/用户副本来源边界/分母/选择/原生与仅符号/证据/预算/独立核验/失败及code LF SHA）
6. `evaluation-plan.md`
7. `docs/codex-results.md`只尾增一次本父结果

不改072/其他历史、论文、规划或本README。不上传原三副本、QA/事件/答案/逐项标签、video IDs/真实路径/成员hash/源映射、私有路径或媒体模型。允许公开固定dataset revision/官网URL、代码hash与聚合。核精确暂存/append-only，普通安全push main后STOP，无后台/自动074/网络取数/媒体模型或写论文；负责人验收后给下一具体决定。
