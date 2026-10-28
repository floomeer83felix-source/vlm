> **负责人归档（2026-10-28）：052已交付并验收关闭，不可重跑。** 结论为ONE_SCOPE_CAVEAT，见[验收](../../research-decisions/post-052-protocol-disposition-2026-10-28.md)。以下README保留原立项/资源/启动消息的历史内容，原READY状态不再有效；当前任务只看最新看板。

# 052：官方任务协议与持续失败结构的一次CPU审查

2026-10-28（北京时间）｜ChatGPT研究负责人；本地Codex执行。  
父任务：**VLM-QUESTION-PROTOCOL-AUDIT-052**。  
**唯一READY / CPU_ONLY / AWAIT_USER_START。** 本包是有具体源码依据的研究诊断，不是新算法或GPU实验；NOVELTY=RETAIN0。

## 1. 本轮要解决的问题

051同24题完成后，F48=SO9/24、V4=10/24，12题在F48及四P全部答错。总分不能区分题目输入要求未满足、视觉观察不足或模型推理错误。

负责人进一步检查到：049的原元数据投影只列task_type/question_type/category和部分image字段，**没有官方task**，见[049源码](../../../prototypes/selection_channel_049.py)第294、309–311行。官方[数据卡Annotation Format](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)声明task；作者按task分派不同协议，而非所有题都是视频＋文本选项：
- navigation/room_to_room_image、navigation/object_retrieval_image、reasoning/spatial/layout：需要五个图像选项。
- reasoning/predictive：需要按题目指定时点限制可见视频前缀。
- 原049自己的范围排除了时间依赖题，官方task若含相应类别，也应与该范围核对。

**这只是已证实的字段覆盖缺口，尚未证实24题实际含受影响题。** 051严格题干/选项/标签join及原得分不因该静态发现自动作废。052要一次回答：是否存在特殊协议或范围冲突？已有持续失败分布在哪些官方任务类别？现有结果能支持哪些有限解释？

作者代码固定在1ac83c260c315545c571f78dea5bf913f36595a5：
- [gpt4_qa.py](https://github.com/keshik6/HourVideo/blob/1ac83c260c315545c571f78dea5bf913f36595a5/hourvideo/gpt4_qa.py#L81)，blob66751c01ba5f3e01581bd9376b33cdbc0705daf6。
- [gpt4_utils.py](https://github.com/keshik6/HourVideo/blob/1ac83c260c315545c571f78dea5bf913f36595a5/hourvideo/gpt4_utils.py#L297)，bloba49991caf2f8bb300e9f8d9b6ae3ea40f1becd3c，预测前缀/图像分支及answer_N图像加载。
- [gemini_utils.py](https://github.com/keshik6/HourVideo/blob/1ac83c260c315545c571f78dea5bf913f36595a5/hourvideo/gemini_utils.py#L327)，blob68d15dee4bb7902daf93b7353f8939224f164f16，独立对应分支。
只读这些公开源码，不运行作者API、安装环境或获取示例数据。负责人已取得上述固定源码并阅读相关分派/输入构造分支及官方论文§2.1；不是只凭搜索摘要下合同。

## 2. 准确输入与闭合身份

安全同步独立文档checkout，重读AGENTS、看板/results/总览、本README及[051验收](../../research-decisions/post-051-coverage-aggregation-disposition-2026-10-28.md)。052须是唯一未回报READY。只用当前本地051执行已明确的准确根；缺入口一次集中核对，不扫盘/猜路径/恢复回收站。不创建空HOLD运行来代替入口交接。

允许只读该051根的以下准确文件，单文件≤2MiB、合计实际Python返回字节≤8MiB：
1. coordinator-config.json：只为取得同一原标注路径/SHA和指定本地Python入口；不访问其中其他资产。
2. nongold.json、source-selection.json、source-map-private.json、binding-receipt.json。
3. input-queue-seal.json、infer-phase.json、inference-complete.json、independent-review.json。
4. score-private.json：**只允许在第3节分类封存后**读，用其既有派生correct/state及diagnostics；无需读取旧预测字母、原始账本或旧049根。

闭合检查：模型Job active0/exit0/no kill、120新attempts=returns、24题/四alias各6、Q01…Q24与旧ordinal/source次序、nongold字节SHA与051队列一致、原标注SHA与051绑定收据/配置一致、独立review PASS。baseline_mismatch_count0在第4节允许读score后再核，不提前读逐题分数。公开[051 execution-summary.json](../VLM-COVERAGE-AGGREGATION-051/execution-summary.json)固定执行提交2afac5e用于核汇总，不能替代本地逐项join。

旧源/原文件均普通文件、无reparse祖先；不写旧根。输入/闭合身份不符则INPUT_IDENTITY_UNKNOWN，保留原因，不打开新原文件追查。代码可只读公开049的projected_json/qualify纯函数、负责人hourvideo_mcq_schema_051.py及既有040 Job类；不运行旧main/模型路径、不改任何旧代码。应核对Git blob或明确LF/CRLF转换身份，不把文本等价说成字节SHA相同。

入口明确后创建同一指定父目录下新根vlm-private-052；已存在不覆盖/删除，等待准确交接。父执行≤3600秒，从入口明确开始，包含实现/等待/清理；不重开时钟。

## 3. 先封存nongold任务分类，后看逐题错误

在独立CPU进程中，对与051相同的原文件**只打开一次，≤4MiB**，纯字节SHA必须与冻结记录相同。物理文件包含保护答案，须报告这次混合文件读取，不能称gold文件零open。

用049既有词法投影器，仅投影同四UID/24个ordinal的**question、mcq_test、task**。保护答案值解码0；其他题及correct_answer_label、answer_N、relevant_timestamps、canary等未保留值词法跳过。不得整文件json.loads、再开原文件/其他版本、读取图像文件或额外探字段。task缺失记UNKNOWN，不用task_type等回填。

每题以负责人051显示绑定器再次核question/mcq_test与冻结题干/五选项。绑定失败不依据旧分数修正；交付INPUT_BINDING_UNKNOWN，原分母24保留。不能换题、删题或补推理。原始混合字节不保存；可保存同24题允许的nongold投影、绑定收据与代码/投影SHA于新私有根。其后全部工作复用封存投影，不重开原文件。已有投影器/自己的CPU实现可在预算内定位修正，保留初失败；不得放宽字段、显示比较或追加原文件打开。

任务分类规则在读取score-private.json前冻结；只使用原task及原049不变的qualify(q)，不做人工视频/证据标注。task须为非空≤160字符且满足[a-z0-9_]+(/[a-z0-9_]+)*的原始字符串；不修改大小写/拼写。按以下顺序产生唯一protocol_class：

| 条件 | protocol_class |
|---|---|
| task缺失/类型不符/非上述规范路径，或首段非summarization/perception/reasoning/navigation | TASK_UNKNOWN |
| 恰为上述三个图像选项路径之一 | AUXILIARY_IMAGE_REQUIRED |
| 恰为reasoning/predictive | PREDICTIVE_PREFIX_REQUIRED |
| task含temporal、ordering、duration、timestamp、timecode或chronolog任一字串 | OUTSIDE_049_TIME_SCOPE |
| 其余规范路径，但原049纯qualify(q)不为ELIGIBLE_NONGOLD | TEXT_SCOPE_CONFLICT |
| 其余 | NO_LISTED_SPECIAL_BRANCH |

NO_LISTED_SPECIAL_BRANCH只表示未命中本包已知分支，**不认证问题的全部语义、必要证据、时钟或视频可答性**。已知特殊task标志和原qualify结果都保留私有，即使前者优先分类。预测题只有PREFIX_REQUIRED标志，不能凭没有物理钟证书直接断言实际看到了未来。图像题核051封存完整输入字段是否只有video而无图像选项；不得为了核对加载processor或图像payload。

正式task类别在私有表保留原值。公开只用task_alias（原规范task按字典序固定T01…，缺失/非规范统一T_UNKNOWN）、四个已公开大类family及protocol_class；raw task→alias映射、逐题ID/ordinal/UID/题干/选项均留私有。三条图像路径与predictive路径可在报告方法中作为已公开规则列出，不能带出本地逐题对应。

将24题类型/分类/绑定封存并记时间与SHA。分类进程无score文件入口、不读取已有逐题correct、模型预测或gold；随后退出。不能在看到错误分布后改变分类/别名/规则。

## 4. 既有派生正确性的一次分析

分类进程实际退出后，另一CPU进程读取封存分类和051 score-private.json。该文件由051源码生成，只含既有派生correct/state等，不需再次解析原标签。只提取同24题的SO、F48、P0…P3、V4（共168个逻辑格）；拒绝重复/缺失/未知state及非0/1正确性。其余内容不复制到报告，不读原始答案或预测字母，不打开原标注。

独立重建：SO9、F489、各P8、V410；每源各6的对应总数与公开051JSON一致。新私有二维表只联接固定question index，核一对一，不能以相似题文或答案猜join。

统一报告：
- 原24题总体及每源的protocol_class分布，类别合计恰24，未知单列。
- 每个family/task_alias/protocol_class的题数及来源覆盖；SO/F48/V4的correct/N、F48/SO与V4/SO纠正/误伤/双对/双错。
- 按同一分组重算all-five-wrong、full-only、split-only及split-only被V4恢复、vote-missed；全24计数应仍为12/1/3/3/1。
- 特殊协议/范围冲突涉及多少题，和持续失败有多少交集。已知别名和组别来自先封存的nongold分类；这些是**事后描述**，不当新假设检验。
- 各组来源数/逐源n_s必须公开。某源该组n=0写0，无分母不填0%或伪装四源等权；不另算可挑选的“清洗后主分数”，不在子组重新跑051投入门，不从高增益组挑新样本。

建议CSV字段：group_kind,group_id,source,n,SO_correct,F48_correct,V4_correct,F48_correction,F48_harm,F48_both_correct,F48_both_wrong,V4_correction,V4_harm,V4_both_correct,V4_both_wrong,all_five_wrong,full_only,split_only,split_recovered,vote_missed。group_kind限overall/family/task/protocol；source为ALL或原四匿名alias。零n计数全0、比率不生成。复核分组和时固定group_kind/source，ALL行是四源汇总，不能把ALL再与四源相加；family/task/protocol是同24题的不同分组，不累加为新样本。

独立复核进程不导入本包聚合实现、不重开原标注；从私有分类/派生正确性表重新计数，核一对一join、分母、配对恒等式、组间合计和051公开汇总。必要自有CPU夹具仅验证实际用到的分支、遗漏/重复join拒绝、gold未投影及合计；不新建评测框架或以测试数作科研结论。报告初失败/修复和最终核验状态。

## 5. 科学处置与明确止损

以下状态互斥：
- JOIN_OR_COUNT_UNKNOWN：身份/绑定/闭合/复算未通过，不给新的科学解释。
- TASK_PROTOCOL_REVIEW_REQUIRED：完整复算，但至少一题AUXILIARY_IMAGE_REQUIRED/PREDICTIVE_PREFIX_REQUIRED/OUTSIDE_049_TIME_SCOPE/TEXT_SCOPE_CONFLICT；仅交已发生偏离/未认证的数量与依据，交负责人决定历史解释是否需补充。不得自动将任何题重新判对/错或整轮作废。
- TASK_METADATA_INCOMPLETE：无上述已知冲突，但存在TASK_UNKNOWN；资格不能认证。
- NO_LISTED_PROTOCOL_GAP_FOUND：完整核对、无未知/列明冲突；保留051现有阴性判断，提供错误结构。不是证明所有输入要求都满足或存在新算法空间。

可同时在JSON用单独flags完整披露未知与已知冲突，主状态按上述顺序。任何状态都不自动触发修图、切片、再采帧、原生处理器、旧模型重跑、改提示/投票/阈值、换题/扩样、第二模型或训练。052不提供新准确率，不宣称核心创新，不把错误簇当必要证据标签。若特殊协议0题，这个答案本身结束该核查，不继续猜新字段。若有冲突，历史实测记录原样保存，负责人负责另作解释修订。

## 6. 本轮资源、交付与停止

仅当前既有conda Python/stdlib；torch/transformers/numpy/SigLIP/processor导入与模型/GPU使用0，nvidia-smi/peer检查/旧锁操作0。原视频/数组payload/图像/权重读取、decode、网络数据下载、训练、新人工证据标注/安装/环境或永久配置修改0；公开参考/文档Git同步发布单列，不计实验联网。

全部CPU子进程使用已核的自有Windows Job监督入口，≤1GiB RAM、单线程，累计outer≤300秒；父≤3600秒。不得以换clock域规避包含成本，先Job assign后执行；只结束自有子进程，实际active0后交下一阶段。新根≤8MiB/128文件，首输出前可用磁盘≥输出配额+128MiB；按阶段报告实际读字节、wall、峰Job与输出快照，快照不称硬配额。输入读取上限按第2/3节分别记，不复制数组/旧目录。超限/失败统一保留已发生事实并交付，不重开父任务。

六处allowlist：
1. prototypes/question_protocol_audit_052.py：本包stdlib脚本及必要自有夹具；无旧main调用。
2. 本目录execution-receipt.md。
3. 本目录scientific-results.md：直接回答三项研究问题及局限。
4. 本目录protocol-and-error-profile.csv。
5. 本目录execution-summary.json：脱敏计数/身份结论/资源/初失败/未知。
6. docs/codex-results.md仅尾增一条“### VLM-QUESTION-PROTOCOL-AUDIT-052”。

旧源码、负责人模块、051原证据、049/051结果、原始历史、看板/总览/README不由执行者修改。公开不含QA/选项/标准答案/逐题预测或correct表、真实路径/UID/原task逐题映射、输入重识别hash。代码哈希和通用规则可公开。一次普通安全push后STOP，不自动053。完整审查由负责人接收后再选择一个具体机制；不承诺一定能从这24题得出可发表新意。

## 7. 用户发给当前本地Codex的启动消息

```text
执行052完整CPU审查：安全同步GitHub文档仓库main，重读AGENTS.md、看板/results/总览及docs/codex-artifacts/VLM-QUESTION-PROTOCOL-AUDIT-052/README.md，确认唯一READY且未回报。

我授权在本包范围内，只读051准确关闭根的列明元数据，按同一原标注冻结SHA做一次≤4MiB的question/mcq_test/task词法投影（保护答案值解码0），先封存24题官方任务/协议分类；分类进程退出后，只读051既有派生correct/state做完整错误结构和独立复算。不得重开原标签、换题、修改旧结果或启动模型。

连续完成实现、必要CPU验证、正式核对、分析、独立复核、脱敏六处交付；累计CPU≤300秒、Job RAM≤1GiB/单线程、父≤3600秒、新根≤8MiB/128文件。GPU/模型/processor/特征/视频或数组payload/图像读取/解码/下载/训练/环境修改均0。一次普通安全push后停止，不自动053。
```
