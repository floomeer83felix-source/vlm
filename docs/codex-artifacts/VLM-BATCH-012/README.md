# VLM-BATCH-012｜Charades官方评测对齐与时间质量分层修复（10项、只读）

**2026-10-09｜唯一父任务须在 `docs/next-steps.md` 显式READY，用户已明确选择修复现有Charades标准、暂不换数据集。**
本批目标不是人工修改19,625条“异常标注”，而是检验原来`0≤start<end≤length`的**自加严格筛选**与官方25时点定位评测语义是否兼容，形成可复算的`OFFICIAL_FRAME_COMPATIBILITY`、`TIME_BOUNDARY_QUALITY`、`P1/P2_SCIENCE_TRUTH`三层状态，且所有层独立定论。单批一次完成最多10项，至少1项关键证据缺失则`HOLD`而非编造修复；完后STOP，不自动开013。此前BATCH010一次授权获取的原ZIP仍在隔离目录，**严禁再次下载**。

**核心依据**：[Charades官方README](https://prior.allenai.org/projects/data/charades/README.txt)写`length`为视频秒数、`actions`为`class start end`三元组、frame localization在`j=0…24`的`j*length/25`评价。它**没有**提供`end>length`一律丢弃动作的判别式；但README单独不充分证明现有ZIP里的`Charades_v1_localize.m`究竟如何实现inclusive/exclusive比较、合并同类动作及处理越界。因此**先取固定ZIP里的真实评测器文本只读校验、再建模拟器**。历史[010真实数据质量报告](../VLM-BATCH-010/download-and-schema.md)、[011独立合同诊断](../VLM-BATCH-011/aggregate-range-diagnostics-and-decision.md)：66,500原token、19,625未过旧数值规则、P1=347同类分离组、P2=97,723异类区间相交对均属旧规则下**记录级**候选；不能据此证实数据损坏或媒体事件真值。补充已知[AGQA/CVPR2021补充材料](https://openaccess.thecvf.com/content/CVPR2021/supplemental/Grunde-McLaughlin_AGQA_A_Benchmark_CVPR_2021_supplemental.pdf)承认部分Charades动作时间区间有误，不能因“官方采样可兼容”就宣布事件精确边界全部正确。

## 启动/资源硬边界

**仅由用户在原有Codex聊天显式发送“执行唯一READY VLM-BATCH-012”才运行。** 安全只对公共**文档Git checkout** fast-forward main，重新读`AGENTS.md`, `docs/next-steps.md`, `docs/codex-results.md`, 本README、[旧用户授权/路径协议](../../charades-metadata-safety-protocol-2026-10-09.md)及010/011报告；如果任务已回报或多个READY/checkout脏/冲突，STOP。

**只读数据位置（绝不能换）**：
`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`
`incoming/Charades.zip`、`extracted/Charades_v1_train.csv`、`Charades_v1_test.csv`、`Charades_v1_classes.txt`。先按原路径身份+无reparse检查和所有固定SHA校验：
- ZIP `c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`；
- train `59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`；
- test `8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`；
- 类表源于固定ZIP、原有校验记录`7b95127e60300d6a69849d161869eb3e9657fa320fc9e92b6f2c9403b49c1887`。
SHA不一致/任何已授权包缺失→`BLOCKED_SOURCE`，STOP，禁止重新获取、重新提取或修改数据。

**官方评测器取得方式限定**：只用现有标准库`zipfile.ZipFile`检查中央目录后，按**唯一且严格匹配basename** `Charades_v1_localize.m` 找到安全成员对象（可位于ZIP安全子目录），再通过 `z.open(member)` 在内存中只读原已授权ZIP内的这份文本。若同名多份、存在路径逃逸/特殊成员或无法确定唯一来源，立即STOP；不得因为文件位于ZIP子目录就改从网络镜像获取。必须先安全验证ZIP central directory、路径/加密/链接/文件名冲突/CRC，禁止遍历或打开其他脚本/视频/图像；仅允许该评测器文本≤256KiB、UTF-8/ASCII解码，且**不写出到磁盘、不导入/执行MATLAB、不上传完整脚本或样本**。ZIP没有目标脚本、格式不明、逻辑不能确定→`OFFICIAL_EVALUATOR_UNKNOWN`并STOP对齐宣称，可继续不涉及实际文件的安全合成对照与总结。可以对公开README做链接和短引证，不能拿网络镜像假装本ZIP源码。

## 10项独立可审查工作（全程不改源CSV）

**1. 权限、来源完整性、安全入口**：确认上面SHA、路径物理身份和用户非商业研究权限、旧GET已消耗；本轮0HTTP数据/媒体请求、0原工作区修改。只披露SHA和相对类别，不打印真实绝对路径、任何原始行。

**2. 从ZIP只读核“官方算法”而非凭印象**：检查`Charades_v1_localize.m`函数/依赖、25个时点的计算、CSV`length`取值及时间判断`start≤t≤end`还是其他、相同`class`多动作如何合并、缺值/越界行为，列明确代码行号及**极短**非连续引文/表达式、评测器成员SHA；不运行MATLAB。若含外部依赖/隐藏代码或无法证明语义，标UNKNOWN，不补充脑补。frame-mAP是有真实预测scores才可算的指标，**本轮不能计算模型mAP**。

**3. 冻结三层分离状态和数据不变式**：A:`OFFICIAL_FRAME_COMPATIBILITY`官方分数评测所需的25时点label构造；B:`TIME_BOUNDARY_QUALITY`记录层数值类：端点不可解析、`start≥end`、start<0、完全在[0,length]、跨越视频末端(`0≤start<length<end`)、在域外启动(`start≥length`或其他)，互斥+flag重叠要分别统计；C:`P1/P2_SCIENCE_TRUTH`语义、物理实例、真实媒体PTS和来源独立。A通过**绝不能向B/C传播为PASS**。所有原始token留全分母，不能裁剪/更改CSV或以新命名伪装修正。

**4. 新通用纯stdlib`offline official-reference simulator`**：仅读固定SHA CSV的`id/actions/length`以及类表；对每个视频`j=0..24`按最终从ZIP证实的公式计算时间点和157类别布尔真值，仅聚合统计，不导出`video,class,frame`矩阵或任何score。跨同类动作按源脚本的合并规则实现，禁止把`0≤start<end≤length`当官方硬过滤。**数值精度/端点inclusion须有实际脚本证据**；如果读取真实代码失败，不能运行数据层“官方模拟器”。

**5. 合成对照先验（强制先过才能读真实数据）**：纯虚构样本覆盖短于length、end>length仍覆盖部分采样点、start≥length无采样点、等号端点、0/极短length、同类重复合并、不同类重叠、解析坏值/非有限、重复记录、25时点索引与last sample`24L/25`、二进制浮点与Decimal差异或明确不适用、错误ZIP脚本成员拒绝、输出泄漏/多表反推小格。任何不可解释模拟差异STOP。

**6. 真实原数据两种口径总量对照（只汇总）**：输出total train/test视频、原token/质量分母；在**旧strict interval** vs 经ZIP确认的**官方25时点标签**下，分别汇总：可映射动作记录数、因越界被strict拒绝但仍命中≥1采样点的token数、完全错过采样网格的token数、视频级有影响数、全体正label`(video,frame,class)`cell计数、两个构造口径的positive cell差异数与比例；先计算总分母再抑制小格，禁止展示单视频/单类/单时间标签或预测分数。**若未对真实ZIP公式建立置信，全部官方兼容数UNKNOWN**。

**7. 时间边界独立分层，保持质量红旗**：在不修改原端点基础上分`within`、`crosses_end`、`starts_after_end_of_video`、`invalid`及合法但官方25格未命中。特别报告`end>length`与`start≥length`的宏观分母以及标注可命中25点与否。即使官方可命中，视频外end仍是B层质量风险，可能有P1/P2顺序/边界混淆，不能将所有19,625“挽救”为真值；禁止使用时间戳缩放、钳位、平移、统一舍入、更换阈值来让数字更漂亮。

**8. P1/P2的保守影响边界**：旧严格P1=347组/P2=97,723对作为**冻结基线**；仅在合法范围/已知可采样的标注上列前后**记录级**数量、关联异常行及歧义桶，不自动推断新实例次序、负事件/语义、视觉可见性/物理共现。若原端点跨域，官方frame-compatible≠适合精确event instance QA。任何无法同口径比较的数要写`NOT_COMPARABLE`而非数字膨胀。没有媒体则P1/P2可靠科学真值仍HOLD。

**9. 可复算和隐私泄漏红队**：只可公开总代码源(不含数据)、测试、公式、官方脚本成员文件级SHA、非敏感宏观分母/差异；所有1–9正小值或可通过Train/Test/Total减法反推小格均隐藏。不得输出原脚本完整版、原CSV行、人物/视频ID、`script/descriptions`、帧级矩阵、确切小类别交叉表、本地绝对路径、任何source identity；不能把本地汇总JSON推GitHub。所有真实文件只读；如必须写临时中间只能停机报告，不扩大授权。合成测试可用本机临时文件，但不能接触原Windows科研资产。

**10. 分层PASS/HOLD及明确止损**：
- A:`OFFICIAL_LABEL_SAMPLING_COMPATIBILITY = VERIFIED / UNKNOWN / FAIL`，只表示本ZIP评测器文本与本地构造的一致性，不声称媒体评价可复现；
- B:`TIME_RANGE_QUALITY = DOCUMENTED_WITH_FLAGS / HOLD`，end越界保留风险，不宣称自动修复标注；
- C:`EVENT_TRUTH / NOVELTY / LONGVIDEO = HOLD / RETAIN0 / FAIL`，没有媒体和真实时钟桥接不给P1/P2问答GO；
- 最终明确`FRAME_EVALUATION_ALIGNMENT`是否足以作为**短域工程可比性合同**；不能证明则STOP本技术支线，恢复先前HOLD。不能为完成十项编造“修好了数据”。

## 只准5处公共交付

1. `docs/codex-artifacts/VLM-BATCH-012/official-evaluator-code-and-policy.md`：ZIP内评测器可核短代码依据、SHA、三层合同/UNKNOWN；不复制原.m全文。
2. `docs/codex-artifacts/VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md`：真实字段宏观分母、两口径映射/互斥质量层、P1/P2边界、风险与GO/NO-GO、源/时钟/长域缺口。
3. `prototypes/charades_official_time_alignment.py`：标准库合成+固定隔离CSV/ZIP只读分析器，无新HTTP/下载/视频/模型、无读取任意路径接口、不写原文件；最终程序不得输出敏感细节。
4. `prototypes/test_charades_official_time_alignment.py`：纯合成unittest，至少10个以上关键反例，先通过才可实际读取数据，实跑原CSV后不可基于真实数据调整规则。
5. 只向`docs/codex-results.md`末尾追加**一条**`### VLM-BATCH-012...`，逐项1—10 DONE/UNKNOWN/BLOCKED、CPU合成测试收据、是否真实只读、0HTTP数据/0GPU、明确的A/B/C科学层级。

不能更改已发布的010/011旧解析器、test、原ZIP/CSV、目录树或本地manifest、研究主目录、锁/环境/旧账本、ChatGPT管理的`docs/next-steps.md`和`docs/research-overview.md`、PR/Issue/原有README。发布前Git仅stage五处，核`git diff --cached --name-only`、仅上传脱敏内容；安全fast-forward后一个普通push，冲突STOP不force push。**0视频/帧/STA/Ego/新包、0CUDA/GPU/模型问答/评分推理、0执行.m/外部联系/手工标签、0公网发布受限数据**。完成后在原Codex聊天等待ChatGPT集中审查，不自行开放GPU或BATCH-013。
