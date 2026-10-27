# 049：选帧内容与坐标通道的完整开发比较

2026-10-27（北京时间）｜ChatGPT研究负责人下达，本地Windows Codex执行。  
父任务：**VLM-SELECTION-CHANNEL-049**。  
**唯一READY / USER_APPROVED_BOUNDED_INPUT_RECOVERY / RESEARCH_NOT_STARTED**。这是实质研究任务；2026-10-27用户在当前私人聊天明确要求执行整包，并批准第10节有限入口恢复及必要CPU候选重建。科研运行尚未开始；不是另建任务或恢复旧父任务。

依据：[路线复盘](../../research-decisions/portfolio-reset-and-core-innovation-roadmap-2026-10-27.md)、[候选设计](../../research-proposals/selection-content-coordinate-study-2026-10-27.md)、[同题跨源修订](../../research-proposals/selection-channel-identifiability-revision-2026-10-24.md)。本README冻结本轮操作；旧设计的NOT_READY说明是历史阶段，不覆盖本合同。017/018只作历史和API参考，不复用其GPU额度或评分作新对照。

## 1. 唯一目标、开工条件与交付方式

一次研究包回答两件事：

- H1：同题在原源视频上产生的选帧位置表，是否比同题在其他源上产生的位置表，更有利于预测原源的既有标签？
- H2：在自然画面不变的情况下，坐标呈现改变是否实质影响Top12相对Uniform12的结果？

本轮是开发诊断，允许已有来源与先前曝光，不是独立确认或新算法认证；NOVELTY仍RETAIN0。

先在**当前本地聊天**完成一次准确入口交接。若路径/缓存未给齐，集中索取第2节全部缺项并等待，不搜索、不创建run/调用账本、不上传空HOLD结果、不领取第二任务。等待用户输入不计执行父时钟。不得仅凭本README或“继续”调用模型；**第9节完整启动消息实际由用户发送**才提供本轮具体数据/模型范围。

输入表完整后，声明领取本父、启动新的不可重置父时钟与独立run。资格、必要预检、全部可执行对照、评分和统一交付连续完成，无需中途再请求子步骤批准。开始内容检查后若资格不满足或运行失败，保留事实统一交付一次PARTIAL/INPUT_NOT_QUALIFIED；这结束本父，不改任务号继续修补。既有任务不复活。

## 2. 一次本地输入交接：只用已存在的缓存

用户在本地指定一份新049输入表，列出确切普通文件/固定目录及其用途；可在聊天提供，不要求上传。需要：

1. **R1–R6中可用的既有候选缓存**及其精确清单。每源48个有序候选RGB；来源、候选顺序和问题源映射有当前可核的私有对应。可用单个数组容器或明确列出的48张图片；不得枚举缓存目录补齐。只接收已存在的48候选，不打开MP4/WebM、不解码原视频、不下载。
2. 已有nongold问题/五个选项/原题ordinal/来源对应文件，或能一次投影这些字段的准确原HourVideo dev JSON入口。只处理R1–R6范围、每源至多50题，共≤300题；不读其余研究资产。原JSON在隔离投影器中读取，不取gold值给选择器或推理进程；若原文件物理上同时含gold，须如实报告该文件被投影器打开，不能声称gold文件零open。
3. 相应原标签的准确评分入口，及题目/source映射。其原标签只由最后独立scorer读取，最多本轮冻结的24题；不读历史分数挑题。若JSON同时含nongold和gold，投影与评分由不同进程执行，原路径不传模型worker。
4. 可用的**完整同配置SigLIP图像/文本特征**及内容/模型/预处理绑定；没有完整特征可提供当前既有SigLIP本地模型目录。只有self-score或top12清单不足以跨源重打分。
5. 当前已明确的Qwen3-VL-4B-Instruct模型/processor目录、既有conda pytorch解释器、现有成功的本地推理入口（如果需要参考，给其准确源码文件）。
6. 原全局GPU锁、相关已STARTED调用索引/账本的准确文件及既有关闭结果索引、用户指定的新049输出父目录。只读指定账本中身份/配置/状态必要字段，不搜索旧run或凭旧日志推断路径。

research输入表/小型元数据合计≤32MiB、指定历史调用索引合计≤128MiB；RGB/特征缓存从精确清单读取，累计输入字节≤12GiB，单缓存≤4GiB。超限或链接/reparse只报告，不自动扩大。正常本地模型加载不计入research小文件限额。允许正常本地配置/权重/分词文件加载，不枚举其他模型目录。

**数据源与题目在任何新输出前冻结：** 按R1→R6固定顺序，选择最前四个同时具有完整RGB、可靠源对应及≥3道合格题的来源。不得按旧/新成绩换源。每源按原ordinal取最前min(6,合格题数)，总N在12–24之间。少于四源时，不做不完整H1的模型试验，也不把缺源当0或借用另一片。

这是对“4×6”规划的前瞻细化：四源不变，每源3–6题，规则只看输入资格；不保证一定凑满24题。完整筛选表、最终n_s与排除数在推理前封存。不同n_s仍按源等权，不能按题数混权。

## 3. 冻结资格、选择规则与模型接口

### 3.1 nongold资格

沿用017公开约束：题干与A–E五个选项均非空、无辅助图片/外部资源依赖，能与指定视频/source及原题一一对应。资格不看答案内容或任何历史/新模型输出。

本任务限不依赖时间坐标的视觉语义问题。对题干**及全部选项**作Unicode NFKC+casefold后，以词边界/等价中文规则排除：
`when; before; after; during; first; last; next; previous; earlier; later; begin/beginning; end/ending; start/starting; finish/finished; order; sequence; duration; timestamp; timecode; elapsed; second(s); minute(s); hour(s); millisecond(s); fps; speed; frequency; pace; how long; how much time; how fast; how often; what time; which time`，以及数字时钟模式`数字:数字`；
中文对应“何时/什么时候/之前/之后/期间/首先/最后/接着/此前/随后/开始/结束/顺序/时序/时长/时间戳/秒/分钟/小时/多久/多快/频率”。
采用英文整词/列明词形，不能把before/after当子串误排其他单词。不事后放宽这些规则来补样本。

如果现有task type或nongold正文仍明确依赖时间而不被词表覆盖，以TIME_DEPENDENT额外保守排除并记录所依赖的字段/规则，不用临场改写问题。语义不确定记SEMANTIC_UNKNOWN并排除，不伪签“标签已认证”。本轮是题目资格判断，不新增视频证据/事件标注。

输入长度在CPU预处理检查≤2048 tokens（含视觉占位）；超限在冻结前排除，不截断原题或选项。若最终不足四源≥3题则结束资格阶段，模型0。所有决定必须在任何Qwen输出前封存。

### 3.2 同题跨源分数

同一SigLIP模型/预处理，新增提特征用float32、eval/inference_mode。图像特征与question-only文本特征转为有限float32输入，再在CPU用float64计算L2归一化和cosine；零范数或非有限值不得填0。对每个q_i与四源各48帧分别打分。按分数降序、候选下标升序稳定取12，恢复候选时间顺序；问题文本不拼选项、答案、时间标签或source ID。

完整同配置缓存优先；若所选四源/题目特征不完整，则在明确本地SigLIP范围内**全部重新提取本轮所需特征一次**，不把不明来源缓存混入。同一192张候选图只编码一次、≤24张题干只编码一次；不做query改写或额外候选。SigLIP推理也计本轮GPU阶段/额度，不是CPU元数据操作。

### 3.3 坐标、RGB与原生processor

统一48槽序数载体：fps=1、total_num_frames=48、duration=48；槽0…47。**不是原片物理秒数**。固定Uniform槽：
`U[j] = floor((47*j+5)/11), j=0…11`，
即`[0,4,9,13,17,21,26,30,34,38,43,47]`。

O用真实所选候选槽号；R保留同样RGB/顺序，把frames_indices替换为U。所有视频条件恰12帧、192×288、RGB uint8。按固定PIL BICUBIC整帧缩放到该尺寸，无裁剪、字幕或叠字；记录库版本。SigLIP仅看既有候选的同一确定性192×288版本，缓存路线须能证明相同版本，否则用一次授权的重提特征路线。

灰色条件12帧恒为RGB(128,128,128)。每个请求走本地原生Qwen processor、`do_sample_frames=False,do_resize=False`与VideoMetadata；参考[045公开原生调用写法](../../../prototypes/native_pts_adapter_045.py)，**不调用045的PTS适配分支**、不手改时间token/position_ids、不全局patch安装库。

预期grid[6,12,18]、324视觉tokens及六个原生temporal-patch时间码须实际核对；U的六个双帧均值为[2,11,19,28,36,45]。CPU processor进程隐藏CUDA，不加载Qwen权重；text-only无视觉输入。O/R不同不保证最终输入不同，不能只看列表断言处理成功。所有source时长、alias、文件名/UID均不传入模型。

### 3.4 唯一prompt、解码与解析

system固定：`You are a helpful assistant.`
user视频块先于下列文本；Q条件只有同样文本：
```text
Answer the multiple-choice question using the video when available.
Time labels, when present, are ordinal positions, not real elapsed seconds.
Question: {原题}
Options:
A. {原选项A}
B. {原选项B}
C. {原选项C}
D. {原选项D}
E. {原选项E}
Return exactly one uppercase letter: A, B, C, D, or E.
```
不改原题/选项次序、不加别名或本题条件名称。此新prompt在所有条件一致，不能为绕过旧输入禁重放而临场加标记。

Qwen3-VL-4B-Instruct BF16、SDPA、eval/inference_mode、seed19、batch1、greedy/do_sample=False、max_new_tokens64、fresh context、无warmup/额外forward。仅解码新生成部分；strip后严格全文等于A/B/C/D/E之一才有效。解释、多字母、空输出均INVALID；未自然EOS的cap输出另列，即使恰为字母也不算有效答案。无重问/纠格式/调prompt。

## 4. 固定逻辑表与完整输入封存

每题10个逻辑条件：

| 条件 | 每题格数 | 含义 |
|---|---:|---|
| G1/G2/G3/G4 | 4 | 同题对四源各算Top12，只把位置表送入固定灰色视频 |
| GU | 1 | 灰色＋Uniform位置 |
| Q | 1 | 纯文字 |
| UO/UR | 2 | 原源Uniform真实RGB，O或R坐标 |
| SO/SR | 2 | 原源Top12真实RGB，O或R坐标 |
| 合计 | 10 | N≤24，共≤240逻辑格 |

UO=UR必须为完全相同模型输入，故**新增Qwen generate上限9N≤216**，不是240；进一步等价再合并。G和自然条件只比较本轮数据，不拿017/018分数填表。

先封存完整CPU最终输入：所有kwargs键、dtype/shape/content及token/grid/position/time相关信息，模型/processor/生成配置与上下文；浮点按最终BF16、整数不改。**对共享pixel_values可去重存内存，身份封存不能漏键**。推理前CPU预检并重新比较：

- UO与UR全输入相等。
- 分别核对SO/SR组内部、同题G1–G4/GU组内部的视觉tensor/grid逐字节相等；各组内只有预声明坐标文本及由原生实现派生的位置相关字段允许不同。
- G在相同q下除坐标链外没有source身份变化；Q无视觉。
- 同输入只保留一次输出，其余逻辑格保留别名与分母。
- 若所有q的四个G实际输入均同，则H1当前接口无可用干预，Qwen generate0；结束本包，不为凑配额继续。

CPU预检可用自有灰色数据做≤2次小探针，随后封存所有正式输入一次；允许在首次Qwen generate前**一次**有确切源码依据的本包兼容修复与必要回归，保留初始失败。不得改科学条件、改安装库或恢复048；已经生成后不修复后重跑。

固定逻辑队列：按题目在各源选中列表的第1…6位轮转、每位按所选四源顺序；每题条件基序G1,G2,G3,G4,GU,Q,UO,UR,SO,SR按全局题号mod10左旋。封存后按首次出现的独特输入顺序执行，重复条件只建别名，不临场重排。

旧已STARTED完全相同输入不重复。只在用户指定索引中查身份；可用关闭结果且完整配置/输入相同则只读取该精确关闭结果行复用，不读其余旧预测，否则标LEGACY_STARTED_UNAVAILABLE。不能通过新run、seed或提示装饰绕过。若影响主要比较，最终只报告不完整，不计算GO。

## 5. 连续执行、预算与信息隔离

**执行阶段次序：** 精确入口→CPU资格与实现/必要数学检查→CPU processor启动→必要SigLIP提取→全队列/等价类冻结→Qwen一次加载与全部新独特输入→模型退出→独立评分→复核/一次push。

输入齐备后父墙钟≤7200秒（含实现/等待/修复/清理/同步，不跨run重置）；首个模型加载前优先验证processor能启动，不先做昂贵读取。一次SigLIP及一次Qwen加载；SigLIP结束后卸载再加载Qwen。全部GPU阶段从首个权重加载意图到最后模型退出累计≤1800秒，包括中间CPU准备/等待；不只计generate。

- Qwen generate≤9N≤216，失败/异常也预扣，每独特输入至多一次；无额外forward/warmup或第二模型。
- 无完整特征时SigLIP最多192张image、24条question文本，batch≤8，image batches≤24、text batches≤3；一次提取，不重试。
- 只用当前pytorch环境/本地权重；local_files_only=True、trust_remote_code=False、HF/Transformers离线与telemetry关闭。实验应用联网/下载/环境修改/训练0。
- 沿用既有全局非阻塞GPU锁/协作mutex；未取得则不加载模型。首个模型前一次当前telemetry、Qwen加载前再复核：free VRAM≥12GiB、util记录、已知冲突则STOP，不轮询等空闲、不动他人进程/锁。18GiB torch allocated上限、32GiB任务RAM包络、CPU threads≤4；峰值不是总物理显存保证。
- 每次模型/encode/generate前私有持久账本fsync预扣，记录parent与单调时间相对值。父只传“剩余时长”，child用本进程起点；不跨runtime相减绝对perf_counter。
- 自己启动的进程使用既有可靠监督机制；超时/OOM/模型异常安全结束本轮，余格NOT_RUN。不得kill未知进程或重新启动模型补跑。
- 新049根≤256MiB/4096文件，首输出前free≥配额+2GiB；不保存RGB/整块视觉tensor或复制权重。读取指定缓存的字节与共享准备成本实记，不把重复引用当重复文件读取。
- 不引入新的全局文件audit猴补丁。依靠精确输入表、角色分离、local-only调用及代码/输入清单复核，避免旧bytes/str审计启动问题。正常模型配置/库读取允许；此条不允许拓展研究数据访问。

推理worker仅接收已投影nongold输入/封存tensor，不接收gold文件路径、旧评分或source真身份。完整推理进程退出后，scorer才从精确评分入口读取冻结题对应原标签。标签编码/题目join无效→SCORING_UNKNOWN，不能删除题或当0；合法真值下wrong/INVALID/FAILED/NOT_RUN按原分母计0。模型输出内容只供解析评分，不用于改选择或停止规则。

## 6. 核心量、判定与退出

逐源n_s分别报告，不以N=24假装齐全。b_iv为G_v输出命中原题标签的指示：
`D_i=b_i,r(i)−sum(v≠r(i),b_iv)/3`；
先按各源题平均再四源等权。灰色命中是对原标签的预测关系，不是灰色视频具有有效视觉真值。

每源`I_s=[Acc(SO)−Acc(UO)]−[Acc(SR)−Acc(UR)]`，再四源等权。报告每臂correct/N、valid_wrong/INVALID/FAILED/NOT_RUN、SO/SR纠错/误伤、完整输入等价数及全部来源方向。

来源等权D≥0.08且≥3/4源D>0；同时|I|≥0.05且≥3/4源I与总方向一致，才记DEVELOPMENT_GO_TO_OWNER_REVIEW；否则分别记CHANNEL_ONLY / REPRESENTATION_SENSITIVITY_ONLY / STOP_CURRENT_HYPOTHESIS。不完整/评分未知只能INCOMPLETE_OR_UNKNOWN，不替代为负结果。此门是开发投入门，不是显著性、出版门槛、贡献认证或自动扩样许可。

只有H1没有自然应用影响，不立核心；普通rank归一化/编号不是新算法；I不是“总收益中坐标通道占比”。所有相似输入、灰色分布外性、已见来源、题目过滤及残余source/答案位置关联须披露。

共享特征、processor、模型load、prefill/generate、总wall、GPU包络/峰值、读字节分别报告；完整成本单计，不叠加父与子包含阶段。不因表现差更换题/选项顺序、模型、坐标或阈值。

## 7. 必要验证与允许的公开交付

只写能检验科学比较的必要测试：跨源矩阵不可用self-score代替、稳定tie、UO=UR去重但逻辑格仍计、失败分母、不同n_s的来源等权、UNKNOWN传播与独立成本。至少用手算例核D=2/3（原源命中1、三错源仅1命中）及I=1/4（UO=UR=1/2、SO=3/4、SR=1/2）；不能仅调用被测函数生成自己的期望。

允许新增/修改恰下列7处；README属于负责人，不由执行者覆盖：

1. `prototypes/selection_channel_049.py`：本包入口/准备/执行/评分，科学常量在此可查。
2. `prototypes/test_selection_channel_049.py`：必要验证及独立聚合检查。
3. 本目录`execution-receipt.md`：范围、入口资格、CPU/模型阶段、初始失败、预算与状态。
4. 本目录`scientific-results.md`：按源配对结果、D/I、GO/STOP及解释边界。
5. 本目录`condition-summary.csv`：每源×条件聚合，不含逐题原标签/预测；G各列均保留。
6. 本目录`execution-summary.json`：匿名计数、配置版本、类数量、成本/封存与退出检查。
7. `docs/codex-results.md`：末尾追加恰一条`### VLM-SELECTION-CHANNEL-049`父结果；旧正文不改。

本轮代码可以参考公开045原生链及当前用户给出的成功本地入口，但不改旧代码/模型环境。参考旧本地入口只读其明确源码，不直接执行旧主程序、不导入有研究文件读取/推理副作用的helper。所有运行时私有文件留本地；公共文件只有匿名source alias、聚合、通用代码与资源证据。不上载QA/选项/原标签/逐题预测、真实路径/UID、帧/特征/权重、原始账本或可反查来源的内容hash。

只有完成实际全队列、评分与独立复核才可写FULL_DEVELOPMENT_COMPARISON；CPU通过、exit0或输入资格报告不能冒充科学完成。部分失败如实统一交付，不新增子任务号。安全普通push main一次后STOP，ChatGPT验收；不自动050、扩样、第二模型、修复、下载或训练。

## 8. 本轮负责人已做与仍未知

负责人已核main 60cf1ed、AGENTS/看板/results/总览及候选设计，049无历史结果；正式冻结Uniform槽、prompt、选择/聚合规则、3–6题资格细化、调用上限及完整交付范围。尚未访问Windows或取得输入，不声称缓存/模型/锁可用。

原048本片停止、C/D和040/041关闭、Charades FINAL_MEDIA_STOP、旧PTS获取停止保持。新实验仅处理明确交接的已有48帧缓存；许可通过第9节新消息激活，不继承历史额度。

## 9. 用户发给当前本地Codex的完整启动消息

下面消息用于在用户自己的本地Codex聊天激活具体操作；GitHub更新本身不唤醒Codex。用户实际发送前，研究数据读取/模型仍未激活。

```text
执行049完整研究任务包：安全同步GitHub文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md及docs/codex-artifacts/VLM-SELECTION-CHANNEL-049/README.md，确认唯一READY且049尚未回报。

按README在当前聊天集中向我核对/索取全部准确本地入口：R1–R6已有48候选RGB缓存及完整特征或SigLIP目录、nongold/原标签与来源对应、Qwen4B/processor与pytorch解释器、调用索引/全局锁及新输出位置。缺项先等待我提供，不扫盘、不猜旧路径、不创建run或上传空HOLD。我提供/确认的输入表是本轮唯一研究读取清单。

我明确授权：输入齐备后，在同一个049父包中只读上述清单，按合同冻结四源各3–6题，完成CPU准备、条件SigLIP一次提取、固定问题跨源对照与自然画面配对、独立评分和统一脱敏交付。最多24题/240逻辑格；相同输入合并，新增Qwen3-VL-4B generate≤216、每独特输入一次、greedy/max_new_tokens64；必要SigLIP≤192图/24题，全部GPU阶段≤1800秒、torch allocated≤18GiB、任务RAM≤32GiB、父执行墙钟≤7200秒。只用现有环境和本地模型，不下载/解码原视频、不训练、不重跑旧STARTED输入、不修改系统环境。输入资格不足或异常按合同结束，不自行换方案或补额度。

原标签仅由模型退出后的隔离scorer读取本轮冻结题；问题/答案/路径/帧/特征/原始账本不上GitHub。按README七处allowlist一次安全push main后停止，等待ChatGPT审查。
```

## 10. 2026-10-27用户批准的同包入口恢复补充

用户已在当前本地私人聊天实际发送049完整启动授权，随后要求执行者自行确认入口、继续完成且无需逐项询问。
执行者提出“有限定位原标注；必要时按017/018原48候选规则一次CPU提取；先验processor再做昂贵准备；GPU预算不扩大、沿用049”，用户明确回复“那你就这么做”。
本节登记该新授权，覆盖前文与此冲突的“完全不查找入口、只用已有RGB、原视频零解码、不得修改负责人文档”限制。
**第3–7节科学问题、非时间题过滤、源/题排序、Uniform12、ordinal载体、prompt、模型、去重、D/I、阈值、gold隔离及GPU/生成上限全部不变。**
本节不是048/017/018重跑授权，不授权下载、旧预测/旧gold产物读取、训练、安装或更换研究方案。

### 10.1 有限入口恢复与当前文件绑定

- 文件名定位只限当前聊天早已给出的两个下载/模型父目录，深度至多2层子目录；每父目录最多4096个目录项、64个子目录，合计最多300秒。达到任何上限即停止对应分支，不扩目录、不扫其他盘/用户目录。
- 只筛公开HourVideo原dev标注文件名及其明确备份变体（名称包含`dev_v1.0_annotations`或同时包含`hourvideo`与`annotation`，扩展限JSON/JSON.BAK/JSON.OLD）；不打开其他QA/标签/预测文件。最多8个候选，仅lstat/type/size/祖先检查；必要时对至多一个无歧义、≤4MiB的候选做一次纯字节SHA核对现有冻结引用，不decode/JSON解析或提取gold。
- 文件名发现和内容身份核对分开记录。缺失/有歧义不从旧预测或标签产物补造评分入口、不下载替代文件；输入表仍不完整时保持入口等待，不提交空HOLD父结果、不创建调用run。
- 已明确017/018根及R1–R6子目录可作有界非递归清单恢复；仅定点只读已定位的manifest、nongold路径交接、原候选PTS元数据及必要runner源码。不得打开旧预测/答案/评分正文。只读指定旧账本的身份/配置/状态字段仍沿用第2节上限。
- 所有真实路径、source UID、文件/帧/输入身份摘要只留当前私人交接；公开使用匿名角色。冻结恢复后的准确输入表，保留旧引用与缺失事实，不修改旧私有文件。

### 10.2 必要的现有媒体CPU候选重建

- 优先使用能绑定对应R源的已有完整48帧缓存。确实缺缓存时，只允许使用上述R目录已存在的`media-entry-private.txt`所指单个准确文件及其`frozen-manifest-private.json`/`source-pts-private.json`；不猜同名、不搜其他视频、不打开048单影片。
- 来源仍按R1→R6固定顺序，结合原第2/3节的nongold题资格和现有媒体/缓存可用性，**在任何新解码前**冻结最前四个合格来源。原媒体size/mtime及同一runtime的文件identity、普通文件/无reparse祖先须符合旧冻结声明；不通过则按资格表排除，不改expected。冻结四源后的提取失败即停止本父，不换第五个来源补跑。
- 缺缓存的所选来源每源只做一次候选提取，共至多4源。按实际017/018源码规则：48个目标为`numpy.linspace(min_packet_pts_s, max_packet_pts_s-0.10, 48)`；每目标至多一次向后keyframe seek，选第一张实际显示PTS满足`ts+1e-6>=target`的解码帧，48个实际PTS须严格递增。不改为索引均匀抽样，不复跑旧主程序或旧问题生成。
- 仅CPU PyAV、video流、hwaccel禁用、线程≤4；不解音频。每源≤600秒，总提取≤1800秒，单源≤16GiB、四源原文件size合计≤32GiB、Python媒体read返回/保守预扣合计≤48GiB。媒体读取与缓存读取分别记账；不得称物理磁盘I/O精确值。父7200秒预算内收紧，无重试、补帧或额外完整遍历。
- 原媒体原地只读，前后stat同runtime一致；尺寸≤4096×2160。选中48帧依原第3.3节PIL BICUBIC整帧缩放为192×288 RGB uint8，不裁剪/叠字。仅允许在本轮新根保存这四个必要规范化候选数组，合计≤32MiB；不存完整视频、原尺寸帧或模型视觉tensor正文。这是对原“禁止保存RGB”的唯一限定例外，仍计新根256MiB/4096文件，不上GitHub。
- 目标/PTS/候选顺序、版本、原媒体identity与新数组绑定在推理前私有封存。重建是本轮CPU准备，不是已存在缓存、历史字节连续性证明或科学独立来源认证，不替换原来源/题目规则。

### 10.3 先验证输入链，再连续执行研究

- 原标注评分入口与四源候选/媒体引用恢复完整后，才开始不可重置父7200秒时钟并建立独立049根；本轮输出父目录取独立文档checkout同级的新`vlm-private-049`，存在/链接/reparse即停，不另找位置。
- 首先在同一现有pytorch环境以CPU、隐藏CUDA/local-only/trust_remote_code=False启动原生processor，至多2次自有灰色小探针，实际核grid[6,12,18]/324tokens及原生回调。权重/forward/generate0，禁止引入全局file-audit猴补丁。先过此门，才读取/重建昂贵RGB或启动SigLIP。
- 隔离nongold投影与CPU资格、候选准备、必要SigLIP、全输入封存/去重、Qwen、退出后隔离评分和成本复核仍在同一个049包连续执行。最多一次首次Qwen generate前、有确切依据的本包兼容修复；保留初始失败，不修安装库，不放宽科学门。
- 新CPU准备/候选/必要测试/后验核查总计≤3000秒，纯有限入口定位≤300秒；均不扩父执行7200秒或全部GPU1800秒。Qwen≤9N≤216、SigLIP≤192图/24题、allocated18GiB、任务RAM32GiB等原上限不变。不得用CPU重建名义加载/推理模型。
- 用户另明确授权本轮同步本README、任务板和总览以登记这份同包范围修订。公开修改上限为这3份规划文件加原第7节7处；实际研究交付仍恰7处。输入尚缺则只交付范围修订，不追加虚构049结果或宣称已开始科研。最终一次普通安全push后停止，不自动050/扩样/修复/下载/训练。

### 10.4 本次有限入口核对后的待恢复状态

2026-10-27，执行者按10.1检查当前聊天指定的两个父目录：共371个目录项，59个子目录入队，深度未超过2层；无错误/上限触发，匹配候选0，文件正文读取0。
该结论只覆盖这两个父目录、固定文件名规则及深度，不声称全盘没有文件或不存在其他备份。
原标注的已知精确引用仍缺失，当前未恢复可供最后隔离评分的入口；不得以旧预测/旧答案代替。
因此本次只发布第10节范围修订，049仍为唯一READY、等待数据入口，不创建研究run/调用账本，不启动processor/媒体重建/GPU，不追加空HOLD父结果。
原文件或其合法同版备份取得准确入口后，可继续同一049的完整流程；既有模型授权和数值上限不扩张，也不转为自动下载许可。
