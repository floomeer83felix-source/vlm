> **2026-11-03已验收关闭，不重跑。** [55e138f](https://github.com/floomeer83felix-source/vlm/commit/55e138f670bbcc690c0b86c53e680dffb609cdf3)完成限定缓存诊断，`CACHE_INTEGRITY_PASS / CAUSE_UNRESOLVED`；负责人2604公开检查，非私有cache独立重跑。开发/test头六排列二元答案不变，严格位置对称条件未满足，不归因。081暂停排除依据未证/raw超限、082首次fetch前父钟未登记及资源覆盖缺口保留。[验收](../../research-decisions/post-082-cache-diagnosis-and-mechanism-reset-2026-11-03.md)；唯一新[083](../VLM-TEMPORAL-MECHANISM-RESET-083/README.md)只做公开机制/文献复核和可否证实验设计，训练/forward/GPU/私有cache/论文0。以下原082合同逐字归档，不继承READY或剩余预算。

# 082 只读081缓存：核查未拟合原因，不做新预测/训练

2026-11-03（北京时间）｜ChatGPT研究负责人。
**唯一READY：CPU_CACHE_LEARNABILITY_AUDIT / NO_NEW_MODEL_PREDICTION_OR_TRAINING。** [081验收](../../research-decisions/post-081-negative-gate-and-cache-learnability-audit-2026-11-03.md)已完整跑完并按原门关闭当前配方；这次一次性诊断训练集358–360/720、全部REAL头FLIP0的原因。不是继承剩余GPU预算，不自动修复重训，也不恢复069论文。

## 1 一次只读范围

按AGENTS安全同步独立文档main，读最新看板/results/081验收/本合同，核唯一未交付READY。沿081明确handoff准确根读取closed records，原076–081及Job/失败/时钟/锁只读；不得全盘/其它研究目录扫描。缺根地址只等待，不交空包。允许登记的文件必须由manifest/seal明确定位，缺证不能猜路径并扩读。

白名单：081 parent/code/input/output/feature/training/prediction/aggregate seals、observations/truth/relations、prepared-index和inference-plan**仅JSON元数据**、feature-index及其193V/138q小张量、feature-pack-seal/prediction-input-index、prediction-inputs tensor、train/manifest及training tensor、六initial/18final head state、4500步training ledger、baseline/head CLOSED逐项输出及对应unique-root两logit/aggregate/source-statistics、必要IO/Job/父闭合和v1/v2代码seals。时钟只读parent-clock、infra-repair-v2、train/predict started/job、第一次预测supervisor失败控制记录、原封存pause/启动/闭合证据与registered v1/v2源码。总≤512个精确登记source文件/256MiB，shared bytecache一次hash后torch.load同buffer，不为核验重读整文件。

**禁止**媒体/帧/RGB/原ZIP/大prepared pixel张量、Qwen权重/processor/tokenizer payload、原新protected benchmark、其它私有数据/聊天全文。无network/decode/processor/Qwen/GPU/头forward/partial-forward/backward/optimizer/新预测/新阈值/种子或训练。torch仅CPU weights_only/map_location=cpu载入既有tensor及做stat；CUDA_VISIBLE_DEVICES为空、CPU4/interop1，前后cuda.is_initialized须false，不NVML/nvidia-smi。不得实例化Head/Linear模型或把学得的Wv/Wq等乘真实features来补算logits/梯度；不import执行旧训练/scorer。已存连续head margins/梯度若不存在就`NOT_STORED`，不补证重放。

## 2 必须一次完成的缓存绑定与响应复核

用只读[纯算术082组件](../../../prototypes/temporal_cache_response_082.py)，LF SHA256 `f136b16bc0053e28bd5efe308d431e9dd8e5358eafd0fb098280c4f5b1b9a1f9`。它不含模型/IO，已12合成检查；正式诊断和独立计数源代码须先封存，独立核验不得调用该生产helper/旧scorer来证明自身。

1. 核3456 B0/62208头逐项keys、CLOSED/alias和原唯一output/state identity；所有缓存分母/原9-162-42汇总对应，原1152 GT按三槽六排列六方向独立重建、q/tau互补。复核train bundle确是源0–19的V/Q/Y与prediction bundle对应子集，feature_pack中的V按pixel key/Q按严格原q token key回指原captured文件，避免group/permutation/question轴或q方向错位。只读index，不读像素。相同字面q跨源应绑定同一q feature；group source先split再perm不交叉，公开仅计数不列真实q/source。
2. 从原CLOSED预测计每源每问六排列答案是否变化：source-question view数为6×源数；固定答案view必恰3/6正确，直接验证。按train20/dev4/test8、B0及A/I/S六seed输出**57行**cache-diagnostics.csv：源/项/view计划与actual、correct item/source36、原FLIP/HOLD四格正确数、permutation-sensitive/invariant views、invariant/sensitive各correct数、REAL对BLACK和第2固定控制（B0 TEXT/头TRAIN_MEAN）逐项agreement。另在JSON报同seed I−A/I−S/A−S原REAL逐项disagreement计数。
3. 同分数不等于同pred/权重/logits；只根据实际cache判二元决策敏感性，不能由agreement推出logit不变或完全不使用V。复核原指标是审计原冻结输出，不引入新科学条件、不修改答案、阈值或门；不按结果筛源/seed。

## 3 特征和参数：精确矛盾与可检验结构，禁止编因果

V真实32×6×18×2560、q当前138个2560float32。核shape/dtype/finite、原file SHA/回指和新包raw tensor bytes对应；与train/predict bundle逐字节一致。报告各split和全32的：

- ordered V精确不同数量、6排列之V按**已知PERMS逆置3个6-unit块**对齐canonical后的exact equality/最大abs和相对L2；均值V作为独立统计参照是否相同。不可排序内容制造“等价”，不把近似相同当bit-exact，不把mean参照碰撞套到真实ordered V上。
- 字面q与raw q feature的唯一数量、q/tau exact collisions、原q/tau相对L2/cosine区间、跨源同q一致性与train/dev/test字面覆盖汇总；不公开具体事件文字/ID，不凭cosine接近断言模型看不懂问题。
- 真实当前输入**(ordered V bytes,q bytes)**带dtype/shape的精确类/相反GT冲突；helper确定性item最大正确数与within-source冲突给的source36保守上界。100%上界只表示未被此精确冲突排除，不能证明架构能学；源上界只排除组内矛盾，跨源约束可能进一步收紧。若仅统计hash相同，必须原bytes直接核相等，不能依赖近似/rounding。

从6initial/18final **直接读state tensors**，不构建/执行网络：核各341633参数、same-seed三臂initial/batch流、final确更新；每参数族的Δ范数、精确未变/变计数，三臂final之间tensor equality/差值范数。重点P[18,64]：initial零、final变化/非finite、18行全同与reshape[3,6,64]块间重复的exact条件、各block差异量。不得用raw学得的权重投影真实V/q。

写清代数条件：理想实数运算下，若P对三块位置重复（包含全零/全常量），且视觉序列只按三块置换，当前query-attention pool对块顺序不变；这只是条件性函数对称性。结合cache/state只能在条件确实满足时报告证据，FP微差/近似重复不能自动当实际预测严格不变，不将此条件推广到所有时序adapter。若P不满足或V不等变，就如实反证该特定解释。

training ledger只取原18配置每步已记录BCE/relation/total loss，核4500 STARTED/CLOSED，不产生新梯度；固定报告step1/10/50/100/250及前10/后10均值、有限性和参数更新对应。loss下降/参数改变不是答对收益，没存梯度就不能说“梯度有效/为零/收敛”。普通头训练近50%可能由不同原因产生，不能仅据最终accuracy选择优化器/学习率/新结构。

## 4 时钟小范围核对和结论边界

原报告剔除26054.403秒、raw081父30640.472秒，原new-parent12000/四父14400上限在raw口径均超；v2 charged口径另列。只读封存clock/train-close/首次predict拒绝/repair/v1-v2 source、下一次predict STARTED和闭合，核区间确在已结束训练active0之后/首次真正预测之前、排除量/保留60秒/阶段预算无清零、六科学AST不变和预测只执行一次。

**active0不等于有权剔除用户暂停。** 只承认原已存在、能绑定该间隔的明确用户暂停/恢复或handoff证据，不读取/上传聊天全文、不要求补做证明，不以新造posthoc receipt倒填授权。若没有，只记`IDLE_EXCLUSION_UNVERIFIED / RAW_PARENT_CAP_EXCEEDED / CHARGED_ARITHMETIC_REPORTED`，不能因“没有算GPU”就认证父限额满足。保留真实科学结果与FAIL，时钟问题不授权任何重跑。

诊断按证据输出可并存的BINDING_DEFECT_CONFIRMED、EXACT_FEATURE_CONTRADICTION、POSITION_SYMMETRY_CONDITION_MET或`CACHE_INTEGRITY_PASS / CAUSE_UNRESOLVED`。后三者都不等于已建立新方法。若无确定原因，明确缺失证据，停止此配方的调参而不是随便归因“模型能力差”。新机制/未来训练须另有可检验设计和完整授权，本082不写新头/训练proposal或论文内容，不自动083。

## 5 资源与七处交付

新独占082根，081以前所有资产只读，不用旧未用GPU/调用/训练额度。CPU数据处理+独立统计复核累计≤300秒、Job RAM≤4GiB；source文件总≤512个/显式读取256MiB、内存cache复用，new root≤64MiB/256文件、起始free≥512MiB。一个科学统计worker、owned active≤8/native采样256、Torch/BLAS4/interop1，同既有环境，无安装。CPU-only fake helper fixture成本包含，不访问真实模型；源码/所有统计与独立核验预封，不在结果后补选阈值/方向。

父≤3600秒，从首次同步前持久时钟；代码生成/助手空闲/报告/同步均计入。只有**事前明确用户暂停**且所有自有Job已active0的区间才可剔除，单纯没有Job不自动减时；raw/charged/证据各列。Job/read-limit实际和UNKNOWN/coverage如实留存，不把快照当全OS认证；新统计完整后一次独立重计，不能import生产helper或重放任何predictor。超预算/identity冲突保留actual/limit/剩余并STOP，不改历史。

精确七处：`prototypes/temporal_learnability_audit_082.py`；本目录`execution-receipt.md`、`cache-diagnostics.csv`（57行）、`diagnostic-summary.json`（binding/features/loss/parameter/clock/independent证据）、`scientific-diagnosis.md`、`execution-summary.json`；`docs/codex-results.md`一次append。公开只有汇总/通用参数名/全局code/资产seal identity，不上传每源/每q预测、GT/事件文字、原特征/参数值/文件或个人路径、原聊天/凭据。raw中间诊断留私有根，必要旧code只AST解析，不执行旧科学入口。

成功最高`CACHE_DIAGNOSTIC_COMPLETE / NO_NEW_PREDICTION_OR_TRAINING / ORIGINAL_RECIPE_CLOSED`；不能把表征统计说成答题收益，不能将posthoc诊断冒充新盲测。七处安全审查、一次普通push main后STOP，不自动083/新训练/新GPU/论文。负责人验收同回合给下一步。
