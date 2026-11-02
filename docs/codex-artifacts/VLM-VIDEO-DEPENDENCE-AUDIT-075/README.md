> **2026-11-02归档：075_CLOSED / ACCEPTED_COMPLETE_CPU_AUDIT_WITH_RESOURCE_COVERAGE_LIMITS。** [35643e6](https://github.com/floomeer83felix-source/vlm/commit/35643e6868f9bd9a97a4dddf4a2037c765a7abf4)完整15552逻辑项/2016新CPU头forward及720整数基线；FACTOR原/均值/全零六问11.1111/17.3611/10.4167%，72个配对均改变预测，当前视频特定答题优势未证。负责人3670公开/交接元数据检查通过；宿主/新派生I/O下界/磁盘监视覆盖边界保留。[验收及下一步](../../research-decisions/post-075-review-and-full-model-visual-screen-2026-11-02.md)停止当前冻结特征/小头继续调参，唯一条件READY转[076完整Qwen视觉证据基线](../VLM-FULL-MODEL-VISUAL-SCREEN-076/README.md)，须明确新GPU授权；070关闭/069暂停。下文原合同完整保留，不继承CPU或GPU额度。

# 075 缓存CPU：移除当前视频并校准结构一致性基线

2026-11-01（北京时间）｜ChatGPT研究负责人。**唯一READY：BOUNDED_CPU_VIDEO_DEPENDENCE_AUDIT / AWAIT_FRESH_075_CPU_START。** [074验收与数学基线](../../research-decisions/post-074-review-and-video-dependence-audit-2026-11-01.md)确认全部5184项完整，但D门失败；070保持关闭、069继续暂停。本任务是074已见结果后的事后诊断，不是新机制或盲测。用户本地新消息明确075、仅CPU及下列上限后一包执行；不需也不产生新GPU/媒体权限。

## 1 同步和唯一输入

安全同步独立文档main，读AGENTS/最新看板总览/results、本合同、074验收及074原合同/科学结果/代码。确认075唯一尚未交付READY；原074完整push/实际Job active0/输入输出闭合，不能重跑原5184头预测或任何特征/解码。

只沿已明确handoff登记读取**074私有根**：parent/code/asset/input/feature/prediction seals与必要闭合账本、24V[6,2560]/28h[2560]、36个原state副本和frozen-statistics.pt（C_CENTER/D_ROLE/S_normalizer、42canonical/anchor_S）、observations、评分专用scoring-labels和原outputs。核全部内容身份/shape/finite/相同六seed137/263/419/557/733/911与六方法C_NATIVE/D_NATIVE/CONCAT/FACTOR/REVERSE/ANCHOR；只读、无递归搜索。无需旧063/070根、原metadata/ZIP/媒体/模型权重或processor/配置，也不读任何旧训练/开发答案。

科学/独立核验/预算/Job/ledger代码和全矩阵先封，再首次读074研究payload。首次同步前持久父起点；初始free实际值、所有阶段/限额/实际读量先记录。代码/输入/state/normalizer/锚固定，研究输入STARTED后不改公式或恢复失败单项。可以核必要结构而不生成旧预测，最多一个纯整数/文本fixture，真实旧头/特征不作探针。

## 2 两种固定视频参照，无新训练

文本逐字原074的严格模板/tau、C/S/R变换、float64统计→float32顺序、42训练锚和logit>0（0=No）不变；36旧头eval/frozen、参数356673/无梯度。仅V替换：

- `GLOBAL_MEAN_V`：以原074视频索引0..23固定顺序，float64累加每个原V[6,2560]，除24后一次转float32。**不沿6时间位置取平均**。全24视频使用同一逐位置参照，不按问题/来源/标签/分数/当前视频选择，不重新拟合normalizer。该参照来自同一未标签评估批次，准确称转导输入干预。
- `ZERO_V`：float32全零[6,2560]，同样全组共享。它可能分布外；失分不能直接证明原头读取了正确时间证据。

原`ORIGINAL_CACHED`只读取074封存5184项输出，不forward。模型角色只收到固定V参照和当前问题变换（ANCHOR保留原固定训练锚），无当前video ID/组号、评分标签、另一个问题预测；不得“修复”互补/传递/答案。`GLOBAL_MEAN_V`不随当前样本变化，不把平均参照中的总体信息称为当前视频信息。

## 3 精确去重、封存预测与逻辑分母

原36×24×6=5184缓存项；两参照各5184新计划逻辑项，共**10368干预逻辑项**，与原缓存合**15552 learned-head逻辑项**。六方法六seed和28精确问题固定，完整输入相同就复用，理论新头forward上界**2×36×28=2016**；实际重复还可能更少，不以2016填实测。

键含控制/方法/seed/原视频索引/问题索引；另按完整state+计算图/方法、实际V及所需C或S/R/anchor字节确定执行身份。重复text只是原始键，不能取代真实tensor核对；hash命中还比较完整输入字节。跨视频同问题在固定参照下必须完全同logit/预测。相同原074完整模型输入如已有CLOSED且身份闭合，允许原输出精确复用，不能再问；未决STARTED或身份冲突STOP。别名不等于新forward，5184原输出不计新调用。

每个实际唯一新调用STARTED/CLOSED先行，finite/预测/来源与全部逻辑别名绑定落盘；新根ledger不覆盖原074。全部输出/键集/代码/input/state/参照seals及Job实际active0、exit0通过后，评分角色才解析074标签。失败/未知保留分母，不能按已完成子集打分或把未知填0；无法完整时相关指标NA。

## 4 无视频的720全局文本顺序基线

只从无答案当前问题按原strict regex解析两个事件原文本，保持原字节，不改写/casefold/添加第三事件问题；去重后应为**6种文本、12种无序三元组、28问题**。固定按UTF8排序枚举全部6!＝720个全局文本排列，每排列给六文本固定rank；当前问题A-before-B的预测仅`rank(A)<rank(B)`。不读取视频、原correct_order、第三事件/组ID或另一个问题预测，不选择最佳/最差排列、按标签拟合/重加权、挑seed或声称新算法。

先封720规则/按每排列28文本问题的20160个纯整数预测，映射到720×144=**103680结构基线逻辑答案**；共享文本对应的别名另计，不是103680次模型调用。评分角色随后用同一144标签核：每视频恰120个排列六问全对，合2880/17280组格；单项正确51840/103680。全720等权平均六问16.6667%、单项50%、反向互补100%、恒定视频0。输出正确组数0..24的**25箱**，计数和720、加权和2880。不得公开词表/排列/成员答案或从这些结果选一个最优排序当方法。

该数学期望不等于某一次随机输出的成绩，不是p值/显著性/物理独立认证。可解释六独立随机位1/64、三独立互补位1/8、完整顺序1/6的差异，不额外采样/bootstrap。720排序共享同六文本并非720独立模型seed/数据源。

## 5 答题指标与视频依赖事实

learned-head条件表固定**108行**：ORIGINAL_CACHED/GLOBAL_MEAN_V/ZERO_V ×六方法×六seed。每条件分母24视频/144问/72反向对，保留原074六问全对/单项/互补/恒定视频整数与百分比；原36条件必须原样复现074公开表。原始缓存新增结构计数为事后重算，不称074当时已测。

按每组六位预测是否等于其三事件某个完整顺序，分为`coherent_and_correct`、`coherent_but_wrong`、`incoherent`，三者和24，第一项恰六问全对数。互补但成环算不一致。不得把分母改成只评分一致组/只保留成功组或强制修复预测。

配对表**72行**：两参照各对同方法/seed原缓存；left=参照/right=ORIGINAL_CACHED。记录24分母、两边独对/都对/都错/unknown/net、六问全对pp变化、144单项中变化数、24组六位有任一变化数。另12行方法×参照聚合mean-sixway差/正负零seed/changed-cells/完整预测相同的seed数；原6seed全部报告，不选冠军，不再增bootstrap/区间/p值/子层或比较不同方法的新门。

“分数接近”不等于预测等效，“删除当前视频后完全相同”只对这些已观察输入成立；不能推广为函数完全不依赖视频。恒定参照下掉分有分布外风险，不能据此证明正确时间定位/问题相关交互。参照仍保留原锚/问题先验，任何答题收益保留与结构一致性/视频依赖分开陈述。**不恢复D迁移或070，不以本诊断创作新头/训练/重排/论文。**

独立核验不得import生产预测器/scorer或做真实头forward，从原074封存输出/labels重算原36条件、所有108条件/72配对/12汇总、coherence和720整数基线/25箱；核两个参照的float64→float32公式、state/固定统计/锚未变、完整实际输入绑定、去重/ledger/输出seal/Job闭合/资源。只读torch可核tensor状态，不加载大模型/processor、不重新forward或补旧输入。输入/代码/预算错误先持久actual/limit/reason/阶段/已完成与剩余，再STOP。

## 6 CPU预算、一次完整交付

既有环境，CPU worker用正常site-packages，不重复074的−S启动错误。CUDA不可见、各Job前后torch.cuda未初始化；无GPU/nvidia-smi/模型权重/encoder/processor/媒体/解码/研究网络/安装环境变化/训练/backward/optimizer/新标签/论文。公开Git文档fetch/push另计，不作为数据下载。

CPU新头/结构预测/评分累计监督≤600秒；准备/独立核验≤300秒，父≤3600秒；CPU Job RAM≤8GiB/同时active≤4/线程≤4。新独占根≤128MiB/256文件、起始free≥512MiB；不复制整个074根或旧权重包。旧074feature/views逻辑读累计≤64MiB、36小头/统计state≤128MiB、必要metadata/outputs/labels/账本≤32MiB，核验与hash读都计；新派生产物读另列，物理I/O/宿主未覆盖范围如实披露，快照不冒称硬配额。

精确10处统一交付，成功/部分/阻断均保留计划分母和实际未知：

1. `prototypes/video_dependence_audit_075.py`
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（108行）
5. `paired-summary.csv`（72行）
6. `method-control-summary.csv`（12行）
7. `structural-baseline-summary.json`
8. `structural-baseline-histogram.csv`（25行）
9. `execution-summary.json`
10. `docs/codex-results.md`只尾增一次本父记录

不改074/历史代码或回执/规划/本README/论文；不公开原事件文本/QA/答案/逐项logit预测或正确性、排列/词表/成员IDs/hash/路径/映射、私有目录/特征/state。只允许上述聚合、固定数据revision/科学代码LF SHA和已公开定义。精确暂存与results历史前缀核对，一次普通安全push main后STOP，不自动076/补seed/改方法或消耗GPU。
