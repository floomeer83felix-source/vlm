# 051：按官方mcq_test绑定后的完整覆盖/读出实验

2026-10-27（北京时间）｜ChatGPT研究负责人；本地Windows Codex执行。  
父任务：**VLM-COVERAGE-AGGREGATION-051**。  
**CLOSED / ACCEPTED_DEVELOPMENT_COMPARISON / NO_MATERIAL_DEPLOYABLE_GAIN（2026-10-28；不可再次领取）。**

已按[2afac5e](https://github.com/floomeer83felix-source/vlm/commit/2afac5e4769a6ea0cc3a22fbcea42377f4692d1d)交付并由负责人[验收关闭](../../research-decisions/post-051-coverage-aggregation-disposition-2026-10-28.md)。当前0 READY；下方原合同与启动消息仅保留历史，不授权重跑本父或转移预算。

依据：[050验收与纠正](../../research-decisions/post-050-input-binding-disposition-2026-10-27.md)；[050原完整设计](../VLM-COVERAGE-AGGREGATION-050/README.md)。本包以官方字段修正未运行的科学比较，不重新启动已消费的050/049。

## 1. 目的与不变的实验

沿用050第3–7节的科学条件、实际输入/去重/票数规则、部署成本口径、来源权重、H_F/H_V、oracle界限和原约束；本README在字段绑定、父ID/根/账本/上传路径及明确的新预算上优先。禁止借修正schema换题、改prompt/投票/模型/门槛。

固定049同24题、四源各6题及四个uint8[48,192,288,3]规范化数组。统一ordinal载体fps1/total48/duration48，不宣称原片秒数。

| 条件 | 候选槽 | 每题generate | 实测预期grid/视觉tokens |
|---|---|---:|---|
| F48 | 全部0…47 | 1 | [24,12,18] /1296 |
| Pj，j=0,1,2,3 | 4k+j，k=0…11 | 各1 | [6,12,18] /324 |
| V4 | 四P固定plurality；同票取P0→P3中最早出现的并列答案，全无有效票INVALID | 0 | 4×324总1296 |
| SO/UO/UR/SR | 049关闭的同题自然结果 | 0新增 | 严格重绑定/评分 |

五新条件×24=120逻辑格，新增独特generate≤120；相同完整输入按049旧队列复用可核关闭结果，不重跑。F48与四P使用同48候选像素集合/总visual tokens，但语言前缀、生成次数、tubelet配对/布局和真实成本不同，不说同FLOPs或唯一神经原因。所有原问题/选项/提示逐字沿用049，greedy/max_new_tokens64、BF16/SDPA、seed19、batch1、fresh context。

## 2. 精确输入与新父包

用户在当前本地Codex聊天发送第7节后，允许只读050第2节列明的**同一049准确根与原标注/模型/锁/监督入口**。缺精确入口一次集中核对，不扫盘/猜路径/恢复回收站/重新解码，不产空HOLD。可另外只读当前050准确根的execution/input-failure闭合收据、bind日志及四份阶段收据，总≤128KiB；只为证明050模型未运行，不执行旧代码主程序。对050-call-ledger.jsonl、input-queue-seal.json、infer-phase.json的存在性定点核对，若发现真实STARTED则不得按0假设重放。

其余旧元数据/关闭规范预测总≤32MiB，四数组总payload≤64MiB；原文件≤4MiB，均普通文件/无reparse祖先、身份与049冻结记录相符。050新输入投影失败不能代替049原绑定，也不需要复用050残缺中间产物。

创建准确新根vlm-private-051（当前指定同父目录可用）；存在或有歧义则等待，不覆盖/删除。父7200s时钟从入口明确开始，一次启动，包含实现/等待/清理/全部子步骤。研究/账本前缀均051，不写任何旧根或继续050账本。

## 3. 官方字段修正：模型前一次核齐全部24题

官方来源：
- [发布者数据卡Annotation Format](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)：mcq_test为展示的A–E测试文本。
- [作者hv_utils.py固定提交](https://github.com/keshik6/HourVideo/blob/1ac83c260c315545c571f78dea5bf913f36595a5/hourvideo/hv_utils.py#L303)：用question与mcq_test构造题目，blob0b243332edddb518f0db7ee06921817cf8c5a605。
这只提供schema依据，不认证本地私有24题已匹配。

本轮替换050“三种options字段”的门：允许原文件在隔离CPU nongold投影器中打开一次≤4MiB，只对已冻结四源UID/24个ordinal投影**question、mcq_test**。保留JSON重复键/非有限保留值拒绝；不解析correct_answer_label、canary、其他题目或保护字段值。其他未保留值只作词法跳过。原文件物理含gold并被读取须如实记录，不说gold文件0open。

使用已发布的纯stdlib：
- prototypes/hourvideo_mcq_schema_051.py。
- prototypes/test_hourvideo_mcq_schema_051.py（负责人已在自有夹具CPU实跑16例通过，不是原数据认证）。

绑定规则已经写成代码：
- question必须存在并与049冻结题干全文相同。
- mcq_test必须存在，提取恰好一次、按A–E顺序的显示标签。优先行首标签，完整时不把选项正文内的偶然标签当边界；否则使用受限同行标签。
- 只接受A. / A) / (A) / A: 等已声明形式和空白或Answers:/Options:/Choices:前缀；行结束符CRLF/CR统一LF，去标签后的首尾结构空白可剥离。禁止大小写/标点/内部空白折叠、语义改写、选项重排。
- 提取结果逐项等于冻结五选项（仅上述边界空白/换行比较规范化）；**交给模型的仍为原冻结文本**。公开汇总边界空白规范化次数，不能把规范化比较称输入字节逐字相同。
- answer_1…5或旧options/A–E键不作为替代/回填，也不覆盖mcq_test显示顺序；不要求不用于评测的其他表示必须与它同序。此优先级来自作者实际评测代码。
- 无mcq_test、解析歧义、缺标签/重复标签、题干/选项错配均INPUT_BINDING_UNKNOWN，不能猜原格式、看gold选解析分支或替换题目。

必须将全部24题映射/源/ordinal与同一SHA一次核齐，并封存解析模式、A–E顺序/文本绑定和代码身份，**之后才允许读取数组payload、加载processor或权重**。绑定失败只可在本地记录已允许的question/mcq_test是否存在/类型与错误码，不额外探其他字段/开原文件。不能把一题失败写全部24题格式无效。

两份负责人纯模块只读使用。可在自己的新执行模块修正调用/运行时接入一次（有确切依据、首generate前），不得放宽此语法/比较标准或修改安装库/旧代码/负责人模块；超出声明格式则如实交付并结束。

## 4. 代码、实际CPU输入与GPU执行

在新prototypes/coverage_aggregation_051.py中复用050已公开、科学上未改变的分区/投票/聚合/原生输入思路；将绑定器与所有私有路径/账本/完成标记改为051。不得直接执行050主入口或其未验证的完整推理路径后声称已过门；不改050/049源码。可以调用无副作用纯函数，实际新接口均需本包验证。

依次完成：负责人16例自有parser测试与本包必要数学检查→24题官方显示字段绑定→两种实际CPU形状探针（至多2个）→120正式输入/队列封存→一次新Qwen加载→全部可执行独特输入→实际模型Job退出→独立评分与复核→一次push。部分失败仍统一保留原分母，不新建子任务号。

其余CPU/模型规则完全沿用050§3–4：
- 原生processor、do_sample_frames=False、do_resize=False，P时码j+2+8m(m0…5)，F48时码0.5+2m(m0…23)，全部真实暴露并核grid/token/完整kwargs/BF16/roundtrip。输入≤4096 tokens，不截断/换题。
- 使用049同模型/processor/tokenizer/生成声明身份，最终全部字段指纹与旧STARTED查重；可核关闭结果只读复用，否则LEGACY_STARTED_UNAVAILABLE、不得重跑。
- 条件基序F48,P0,P1,P2,P3按全局题号mod5左旋，题顺序同049。每调用前fsync预扣，失败也算；无warmup/额外forward/重问/纠格式。
- 所有权重前已封存新科学代码/解析器/nongold/数组身份。模型worker只见匿名nongold和数组，不见原标注路径或UID。
- OOM/timeout/模型异常安全结束，余格NOT_RUN；开始生成后不得修复重跑或更改程序。

050模块本轮尚未实测的native/模型路径不能以既有suite通过替代真实验证。实现兼容修复、必要回归和实验都在同一051内进行，无需再逐项征求批准；允许的修复不扩大字段/科学范围和预算。

## 5. 退出后严格评分与科学判定

模型进程实际active0后，scorer可第二次打开同原文件≤4MiB；只投影同24题question/mcq_test/correct_answer_label，用同一个官方展示绑定器再次核题和选项，再解析原标签。标签值只在此角色读取，总≤24；原SHA必须一致。

重算049 SO/UO/UR/SR规范关闭输出的正确性，逐题与049派生正确性表核齐。任何差异BASELINE_SCORING_MISMATCH→INCOMPLETE_OR_UNKNOWN，保留差异计数供负责人追溯，不修改049旧标签/结果，不先断言049已被推翻。

固定049 SO作主参照。每源6题、四源等权：
- F48−SO净收益≥1/6且至少3/4正源，或V4−SO同门通过→OBSERVED_HEADROOM / OWNER_REVIEW_REQUIRED。
- 两门均不通过→NO_MATERIAL_DEPLOYABLE_GAIN。
- 输入/评分/执行不完整→INCOMPLETE_OR_UNKNOWN，不写科研阴性。

逐源各臂correct/N、valid_wrong/INVALID/FAILED/NOT_RUN/SCORING_UNKNOWN、F48−SO/V4−SO/V4−F48四格与全部成本都交。V4按固定plurality/最早并列票规则，不加入裁判推理。O4/O5、full-only/split-only、vote-missed/all-five-wrong按050定义，仍是gold事后有限程序诊断，不是可部署方法、真实证据标签或未来方法上界；不据此训练selector。

同一24题四个已见记录来源不是独立确认集；低分辨率/序数时间/物理独立未知等边界保留。研究机会GO不是核心创新或论文认证，049坐标候选不恢复。

## 6. 独立新预算与七处交付

新预算不是050余额结转：
- 新generate≤120，一次Qwen4B BF16/SDPA加载，greedy/max_new_tokens64；GPU从权重意图到进程退出≤1200s。
- allocated≤18GiB、Job RAM≤32GiB、CPU threads≤4；加载前两次明确时点free≥18GiB，设备身份/全局非阻塞锁/mutex与自有Job监督沿用已核入口，不轮询等空闲、不kill peer。
- 父≤7200s，CPU监督累计≤1800s；新根≤128MiB/2048文件，首输出前free≥配额+2GiB。四候选数组不复制，不保存完整视觉tensor/logits。
- local-only/trust_remote_code=False/离线，原视频读取/解码、SigLIP/新特征、下载/训练/环境与永久配置修改0。原文件读取仅上述两次两个角色；输入缺失不扫描/恢复。
- 首generate前最多一次有依据的本包兼容修复，保留初失败；耗尽/失败不重开parent。阶段wall与包含成本不叠加，V4四前缀/四生成和F48总成本分别报告。

执行者只允许新增以下6文件、另向results尾增一个051父记录，共7处：
1. prototypes/coverage_aggregation_051.py。
2. prototypes/test_coverage_aggregation_051.py。
3. 本目录execution-receipt.md。
4. 本目录scientific-results.md。
5. 本目录condition-summary.csv。
6. 本目录execution-summary.json。
7. docs/codex-results.md只追加“### VLM-COVERAGE-AGGREGATION-051”。

负责人两个schema模块、050旧产物、README/看板/总览不由执行者修改。所有QA/原选项/gold/逐题预测、真实路径/UID/数组/权重、原始账本/可反查输入hash留本地；公开只汇总和通用代码。一次普通安全push后STOP，不自动052/扩样/换视图/第二模型或训练。

## 7. 用户发给当前本地Codex的完整启动消息

```text
执行051完整纠正版：安全同步GitHub文档仓库main，重读AGENTS.md、看板/results/总览、050负责人验收及docs/codex-artifacts/VLM-COVERAGE-AGGREGATION-051/README.md，确认唯一READY且未回报。050已消费，不重启其根或账本。

我授权按051完整合同只读同一049准确根、四源48帧缓存/同24题/自然关闭结果及必要配置；从同一冻结原标注的question/mcq_test按作者格式严格核齐全部24题，再连续完成F48、四互补12帧及固定投票/完整评分。使用已发布的hourvideo_mcq_schema_051.py和16例自有测试，保留原题/选项/提示/模型/门槛，不回填或改写。准确入口不明一次集中核对，不扫盘或恢复文件。

新Qwen generate≤120、greedy/max_new_tokens64、一次加载、GPU整包络≤1200秒、allocated≤18GiB、RAM≤32GiB、父≤7200秒。无原视频解码/SigLIP/下载/训练/环境修改。原标签值只在模型实际退出后由隔离scorer读取同24题；050未用预算不结转，旧STARTED输入不重跑。

按051七处allowlist统一脱敏交付，完整逐源结果/未知/成本均保留；一次安全push main后停止，等待ChatGPT验收，不自动下一任务。
```


## 8. 负责人验收（执行后追加）

2026-10-28：[完整验收](../../research-decisions/post-051-coverage-aggregation-disposition-2026-10-28.md)。120/120新generate有效，严格显示字段/标签和旧96正确性一致；F48=SO9/24、V4=10/24，两预设门均FAIL。ACCEPTED_DEVELOPMENT_COMPARISON / NO_MATERIAL_DEPLOYABLE_GAIN / CLOSED。当前0 READY；原合同已消费，不重启、不自动052。执行者七处原产物/results保持原样，560项公开一致性复核不等于私有实验独立复现。
