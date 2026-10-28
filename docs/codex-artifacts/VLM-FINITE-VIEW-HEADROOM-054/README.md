> **负责人归档（2026-10-28）：054已完整交付并验收关闭，不可重跑。** [验收](../../research-decisions/post-054-finite-view-disposition-2026-10-28.md)：SIMPLE_CONFIDENCE_USES_MOST_HEADROOM，恢复3/误伤2/漏1；当前0 READY。以下原READY/启动消息保留为历史，不再授权执行。

# 054：闭合16组合的有限可恢复性与排序缺口
2026-10-28（北京时间）｜ChatGPT负责人；本地Codex执行。
父任务 **VLM-FINITE-VIEW-HEADROOM-054**。
**唯一READY / CPU_ONLY / AWAIT_USER_START。** 不是053重跑或新算法验证；核心创新保留数仍0。
研究理由与近邻见[负责人决定](../../research-decisions/post-053-finite-view-direction-2026-10-28.md)，本README完整执行合同优先。

## 1. 本轮只回答三个问题
053固定24题/四source各6的填128完整16组合中：
- 15个非空集合的有限答案知情oracle覆盖O15，相对F有多少可恢复题？
- 事前固定的精确置信度选择E15能恢复多少、误伤多少、漏多少？
- I/A的估计候选与其被选状态的实测top1/标准答案分别怎样对应？
全N24、052时间范围标志1保留；不挑来源、不改题/输入、不改053原结果/投入门，不启动模型或新数据收集。

## 2. 同步、准确入口、旧输入范围
在独立文档checkout安全同步main，读AGENTS、看板/results/总览、本README、负责人决定及053验收。确认054是唯一未回报READY。旧053模型及CPU相关进程必须实际active0；053父已消费不可启动。
只用当前本地已明确的准确053关闭根，不扫盘、猜路径、访问旧049/051/052根或回收站。缺精确入口时先集中一次交接，不创建空HOLD运行。入口明确后创建同一指定父目录新根vlm-private-054；已存在不覆盖/删除，停止准确交接。父≤3600秒从入口明确开始，包含实现/等待/清理，不重置。
只读旧053以下文件，普通文件/无reparse祖先，单文件≤2MiB，累计实际Python返回≤8MiB：
第一阶段：coordinator-config.json（协调者仅取得同版原标注路径/SHA和既有Python）、nongold.json、source-selection.json、scoring-map-private.json（协调者）、binding-receipt.json、initial-input-seal.json、scores-private.json、selection-seal.json、output-seal.json、infer-phase.json、inference-complete.json、independent-review.json、verify-phase.json。
第二阶段才可：outputs-private.json、scored-derived-private.json、scoring-receipt.json。它们的读取不得早于第三节E15选择与代码封存、nongold进程实际退出。
不读旧原始ledger/完整日志、runtime-config中的其他资产、目录其他文件或任何cache、vision tensor/NumPy数组、图片/视频/模型权重。scores-private内5维JSON标量得分不属于许可外的视觉数组payload。
核代码实际LF SHA为d83f2d1f0e64039f16d973b6dbc2d50943bded8b5a31b40577102f055f51d6f5，并与各seal code_sha一致；053来源仅作为只读源码，不导入其实现或调用旧main。核nongold/score/输出SHA与旧seal一致、selection绑定初始队列、24索引/每源6/原ordinal与scoring-map一致、初始384格每题mask0..15恰一次、初始384身份唯一，五分数均有限且对应RETURNED/一步。旧闭合attempts=returns=steps437/一次模型、相关进程exit0/no kill和独立reviewPASS均核；不冒充从公开记录认证本地数组字节。
scores文件可能包含已选零填充结果；主分析只取initial seal指定的384状态（其中24空白），不把53个选择性零填充混入固定全集。无法验证必要身份或完整性则INPUT_OR_COUNT_UNKNOWN，保留原因，不通过读新目录/重算模型补齐。
可只读049 projected_json、负责人051 binder及040 Job/Process的窄纯实现；不执行旧main/runtime/score，不改旧模块。加载纯helper后须核sys.modules没有torch/transformers/numpy/PIL/cv2。

## 3. 先封存nongold控制，再看正确性
独立stdlib进程只接第一阶段nongold配置，无原标注和旧逐题correct路径。从initial seal取同384状态；给出每题候选top1、margin、mask和E15选择，结果留私有。
top1按最大L_a，精确同分按ABCDE更早。margin=L_top−max其他L；不用标准答案、不重新归一/温度/阈值、不学习来源/题型规则。
**E15**只看mask1..15，选择实测top1 margin最大状态；精确同分按保留块数更多、mask整数更小、ABCDE更早，和053 best相同。这是事后规定的已知置信度控制，未经过独立确认，也没有第二填充复核；不得冒称“053同门控方法的改进”。
mask0是全128遮挡控制，作为独立描述B0；它不是无视频输入、不加入O15/E15或新主分母。
同时只读旧selection-seal，封存I/A所选(a,mask)与该mask的实测top1是否一致；不得依据此改变选择。原选择无三块访问记录保留，054现在读取完整旧表不回溯授权053策略看到全部表。
封存本包代码、输入对应关系/得分SHA、E15全部选择和分析计划，记录时间并退出，实际Job active0后才向第二角色交原文件/旧correct入口。

## 4. 一次隔离评分与旧结果核齐
评分角色复核前阶段实际exit0/active0及代码/封存未变。
对053配置中同一个原mixed annotation打开**一次≤4MiB**，核冻结SHA；仅词法投影固定24 question/mcq_test/correct_answer_label。题/五选项以负责人051 binder严格核齐。原保护标签值解码恰24；不得整文件json.loads、重开/换版/读取task/answer_N/图片。物理mixed读取与保护值解码分别记，原mixed字节不保存。
用同24标签重建旧outputs-private的144个方法correct/state，须与旧scored-derived逐项一致，并复现F9/M7/A10/I8/C10/R11及四源各6。重复/遗漏/非法label/state/任何差异一律INPUT_OR_COUNT_UNKNOWN，不修旧记录、不改标注、不给新的科学结论。
之后从冻结E15与旧384得分计算本包指标。新的标准答案数字映射可封存在新私有评分文件，供独立review重新算；不传回已退出的nongold角色、不进任何未来策略或训练数据，不公开。
没有新模型答案；本次新增的是对旧得分状态的派生正确性分析，不称新实验证实/新泛化成绩。

## 5. 固定指标与分母
单题始终是统计单位，共24、四源各6；360个非空状态/480个三块score分量均不是独立题数。
报告F/M/A/I/C/R的旧完整输出计数（FROZEN_053_METHOD）；E15为POSTHOC_UNGATED_CONFIDENCE_CONTROL；B0为MASKED_CONTROL；O15/O1/O2/O3为FINITE_GOLD_ORACLE_NOT_DEPLOYABLE：
- O15：mask1..15中任一个实测top1等于标准答案。
- O1、O2、O3：分别在保留1、2、3块的所有集合中任一个top1正确；它们不必单调，不能按组相加为样本量。4块唯一状态就是F。
- B0：mask0 top1正确。不可叫“没有视频也能答对”，它仍有48槽/1296视觉tokens及同位置载体。
- 最小成功保留块数K∈{1,2,3,4,NONE}，在所有非空集合中按是否top1正确取最小；它不是MRFS/真实必要证据或普适最少帧数。
同一题各集合正确性可以偶然或依语言先验变化；O15不是未来模型/新观察上界，不证明存在可识别视觉依据。
每源及ALL计算：
H=O15_correct−F_correct（F错而O15至少一个成功），必须>=0。
E15_recovered=F错且E15对；E15_harm=F对且E15错；missed=H−E15_recovered；核E15−F=recovered−harm及missed>=0。
来源覆盖：H>0的来源数；ALL是四源之和，不新增样本。保留全24，不单列“适格23题主分数”，不以子组重跑053门。
I/A各自把24题分为：候选a不等于所选状态实测top1；候选等于实测top1但答案错；候选等于实测top1且答案对。三类互斥合计24，只是旧表对应关系，不能声称已做因果错误分解。另原样报告旧最终correct与是否改答，避免把候选错和最终错混为一件事。
对已测灰色状态，汇总目标答案的rank1..5（log score降序，精确同分ABCDE优先）及目标margin=L_gold−max其他，报告范围/分位等描述，不寻找新阈值、不把E15/目标rank反向做选择器。
所有图表/CSV只含源alias与聚合，不公开逐题ID/ordinal、mask→逐题答案、scores/目标rank/correct逐题表、真实路径/UID/输入重识别hash。

## 6. 预先冻结的研究处置
完整核齐后，按优先次序：
1. 若H<4或H>0的来源数<3：FINITE_VIEW_HEADROOM_TOO_SMALL，停止为原目标尺度继续在这些固定状态之间设计选择规则。
2. 否则若missed>=2：RANKING_GAP_OBSERVED。仅说明这张有限表中置信度控制漏掉部分可恢复题，交负责人研究近邻与不同机制；不宣称新颖/可部署，原I停止不撤销。
3. 否则：SIMPLE_CONFIDENCE_USES_MOST_HEADROOM，当前控制已覆盖大部分有限纠正空间；不是把E15立为新核心。
H门借用053已冻结的>=4题/至少3源机会尺度，不是统计显著性或全领域通用标准。若复核缺失/失败/预算超限，则INPUT_OR_COUNT_UNKNOWN而非上述三种科学处置。
所有状态最后均STOP；不自动055、改margin/置信度/选项顺序、训练、二模型、扩样、下载或再获取画面。没有必要证据标签时，15状态全错不等于没有自然证据或推理能力达到上限。

## 7. 监督、成本与七处交付
仅当前既有Python/stdlib；CPU累计监督outer≤300秒、每Job≤1GiB RAM/单CPU/单线程、父≤3600秒。既有Windows Job/Process先assign后执行，每阶段实际active0后交下一阶段；只结束自有Job。代码定位修正可在同父累计预算内进行，保留初失败，不新增原文件打开、不改冻结分析规则。
旧metadata≤8MiB/单≤2MiB，原文件一次≤4MiB；新根≤8MiB/128文件，开输出前free≥8MiB+128MiB。实际Python返回字节/资源wall/峰Job/输出快照与未知分别报告，快照不冒充硬配额，OS/import/control IO不声称穷尽。
模型/processor/tokenizer/torch/transformers/numpy/PIL、GPU/nvidia-smi/peer/旧锁操作、weights/视频或图像/视觉数组payload、decode/特征/下载/训练/安装/永久环境修改均0。公开文档Git访问单列。
自有必要fixtures只验证实际用到的top/tie、mask排除0、oracle覆盖、失败/重复join拒绝及守恒，不创建新框架或以断言数作科学价值。
独立stdlib reviewer不导入被测聚合/E15实现，不重开原文件或旧数据，使用新封存得分/选择/标签私有表重新计算360状态正确性、144旧输出一致性、所有聚合/门与成本。公开review源码可内嵌本包模块，明确它是新封存表的复建而非独立像素/OS认证。
七处allowlist：
1. prototypes/finite_view_audit_054.py（含必要自有fixtures/独立review源码）。
2. 本目录execution-receipt.md。
3. 本目录scientific-results.md（直接回答三问题与主状态）。
4. 本目录finite-view-summary.csv：12种条件×ALL/S01..04=60行；条件F/M/A/I/C/R/E15/B0/O15/O1/O2/O3，带kind、N与correct/unknown。
5. 本目录headroom-and-ranking.csv：ALL/S01..04五行，含N、F/O15/E15正确、H、recovered/harm/missed、K1/K2/K3/K4/NONE及I/A三类计数。ALL可另JSON记来源覆盖，不能把来源数相加。
6. 本目录execution-summary.json（完整计数、输入/封存/旧144一致性、分类状态、资源与初失败/未知）。
7. docs/codex-results.md仅尾增“### VLM-FINITE-VIEW-HEADROOM-054”一条。
不修改README/看板/总览/负责人设计/旧模块/旧科学记录。公开不得含QA/选项/标准答案/逐题预测、correct或logit、原日志/路径/UID/重识别hash。一次普通安全push后STOP，不自动055。

## 8. 用户发给当前本地Codex的启动消息
```text
执行054完整CPU科学分析：安全同步GitHub文档仓库main，重读AGENTS、看板/results/总览、VLM-FINITE-VIEW-HEADROOM-054/README，确认唯一READY且未交付。

我授权按README只读053列明闭合元数据和标量得分，先封存nongold E15选择，再隔离读取同版原标注一次，仅对固定24题分析并核齐旧144个正确性格。保护标签不进选择规则、不修改旧结果。

连续完成七处脱敏交付和独立复核。CPU监督累计≤300秒/Job≤1GiB单线程、父≤3600秒；模型/processor/GPU/视觉数组或媒体payload/下载/训练均0。一次安全推送后停止，不自动055。
```
