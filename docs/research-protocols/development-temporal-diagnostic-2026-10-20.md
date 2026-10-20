# 开发集双事件时间间隔四臂诊断 — 2026-10-20

**新研究口径：DEV_DIAGNOSTIC / SOURCE_OVERLAP_ALLOWED / PRIOR_EXPOSURE_POSSIBLE。**
用户在029来源路线停止后，对“允许来源可能重合的开发集机制诊断”答复“好的”，
接受本科学口径。该答复不是新GPU/下载/gold的无限许可；真实操作限
[VLM-DEV-TEMPORAL-PILOT-030合同](../codex-artifacts/VLM-DEV-TEMPORAL-PILOT-030/README.md)
及用户实际发送的明确启动消息。当前尚无030执行结果。

## 研究问题与继承关系

在相同48个实际PTS候选、12帧和两个事件锚点下，把题目已经给出的A先B后约束
施加于pair检索，相对不限制pair次序，是否改变选帧及描述性答题结果？

四臂定义、窄语法、tie、补齐、分母和解析全部继承
[025协议第2–5节](./temporal-distance-diagnostic-2026-10-20.md)及已交付025实现。
本协议只明确替换其第7节对新研究的来源分离入门条件；原025/024等历史合同不改、不重开。
SKIP_NONFINITE_028 / PROJECTOR_028_V1显式沿用，默认严格解析仍保留。

原028固定四个来源/原题索引、20选项和ABCD/BCDA/CDAB/DABC的16文字槽位不变。
不换题、不再筛选、不补来源登记、不以不同UID、时长或P3缺参与者推断独立。
本轮正面声明旧源重合及以往题目暴露可能；不再要求排除013/014或R1–R6才能做本诊断。

如030的新用户消息明确授权，可对这四个固定题每臂新回答一次，即使旧实验答过同题。
这是030独立新run的16个槽位，不重放原013–029父任务，不读取旧预测/金标来调参，
旧任务/锁/账本/预算不迁移。现有AGENTS对历史前向的禁令在其他任务仍有效。

## 唯一预定的主要对比

- A：Uniform12；B：question-only GlobalTop12。
- C：i≠j最大a[i]+b[j]双锚点；D：同目标限制i<j。
- C/D共享事件A/B词句、图像编码、原始cosine、恰好两个不同锚点、
  question-score Top12补齐、tie及按实际时间呈现。只改变pair可行域。
- 报告C/D同帧集合率、锚点pair次序、两组原始目标值、12帧跨度及bin覆盖proxy、
  C/D正确性配对及各组成本。六对表均为描述；不按观察结果换主要对比。
- 若所有实际执行题C=D，报告NO_REALIZED_SELECTION_CHANGE；相同帧/prompt/tensor却不同回答应核为实现/可复现性问题，不能当顺序约束效应。
- 48候选按现有真实runner的全片均匀target、0.10秒尾边距、seek-backward后取
  首个>=target的解码帧，保存实际PTS；不足48或非有限/不严格递增则该源NOT_RUN。
  所有臂同一pool，不补帧、不clip分数、不加tau/间距阈值或搜索超参。
- 现有输入helper的12源帧、grid[6,12,18]、实际324 visual tokens必须由本轮processor测得，
  同题四臂匹配；不是凭旧回执填数。插入的时间戳token可因选帧不同而变，
  记录总输入长度，不以此要求所有text+timestamp token数相同。
- SigLIP检索仅用问题/事件文本；五选项仅进Qwen prompt。
  原tokenizer截断规则不变，额外记录未截断长度/实际长度与截断标志，不按截断调参或剔题。

## 完整分母与实施失败

本轮在任何模型加载前冻结完整N=4、16槽位，保持原全局索引轮转。
来源权利/媒体/解码失败或资源不足不换候选；相应四槽NOT_RUN并写明事前原因。
至少1源媒体及隔离门通过才启动模型；完全无可执行源则实际GPU0/gold0并如实STOP。

所有计划槽位终态且所有模型PID实际退出后，最多一次独立CPU scorer；
只读取原标注中这四题gold，profile/version与原028完整快照一致。
有效gold下INVALID/FAILED/NOT_RUN在每臂完整N4中计错，另报完成率；
gold缺失/坏值/快照不匹配时完整准确率和pair表UNKNOWN，不缩N或重开。
按源列是否真正执行，避免将实施失败当成选帧机制的负结果。
至少实际调用过一次Qwen.generate才允许本轮gold访问；纯准备失败不消费gold来填报告。

## 可作与不可作的结论

最多4个已暴露可能、来源依赖未知的开发题，只用于检查真实集成与寻找值得扩大检验的
现象。正结果不证明稳定提升、独立泛化、显著优势、正式HourVideo榜分或算法新颖性；
负结果也不能推出所有顺序约束无效。相似度和选帧跨度不认证事件实例、存在性或证据召回。
48候选可能漏掉短事件；未获独立实例时间标注，不能把错误定位为召回或推理原因。

媒体采用名义完整视频PTS；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED，发布/crop/实例仍未独立认证。
许可必须在本轮有用户有效许可声明及既有批准依据，下载/HEAD本身不替代权利。
NOVELTY=RETAIN0；TRAIN-GPU HOLD；Charades FINAL_MEDIA_STOP。
