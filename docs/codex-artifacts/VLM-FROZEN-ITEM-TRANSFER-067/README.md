# 067 固定VIDHALLUC条目的一次性冻结评估

2026-10-31（北京时间）｜ChatGPT研究负责人。**唯一条件READY：AWAITING_EXPLICIT_MEDIA_GPU_AUTHORIZATION。** [066验收](../../research-decisions/post-066-admission-and-frozen-transfer-2026-10-31.md)已完成；本合同可供批准，**尚未获得本轮媒体/GPU执行授权**。仅用户新消息明确批准067及本合同既有媒体/解码/一次冻结GPU范围后，才可一轮连续执行。一般“继续”、上轮成功或旧GPU余额不算授权；无明确授权时只报NEEDS_EXPLICIT_067_AUTHORIZATION，不建实验根、不消耗任务、不追加结果。授权后按下列阶段完成/有界停止、统一push后STOP，不中途追加授权/预算。

## 1 刷新与严格固定对象

安全同步独立文档main，完整读AGENTS、本合同、066验收/准入报告/提案，静态读原056头、060媒体/模型接口、062 tau与统计、063封存与当前看板/总览；results检索本ID，确认唯一尚未交付条件READY和本次明确用户授权。不得执行旧060/063主入口或恢复任何旧父包。

仅从当前明确handoff/闭合登记取得066精确根、063及其062/060/057精确引用、既有事件包、本地Qwen3-VL-4B-Instruct/既有conda pytorch与共享GPU锁/持久账本；不递归扫目录。066 admission-seal/原观察投影/名单与读取前代码身份闭合，原50对固定，类别VIDHALLUC、100V/100q/100tau闭包及066已闭合publisher结构摘要再次核对，**不重跑选择/哈希排序来更换名单**。观察输入与评分标签分离；原answer仅由评分角色在输出封存后解析，前期身份hash核验不解释答案值。公开题目答案已可见，不声称从未见标签/全新盲测。

允许只读必要的066封存/名单/原DyBench元数据/文件树和闭合记录，063代码/输入/输出seal与12个指定final state，062 normalizer及其原身份引用，060/057模型/processor/媒体身份与已闭合缓存manifest/相关调用账本；不读旧逐项预测/正确性、旧gold标签、训练计划/原始特征或无关私有文件。模型配置/tokenizer/原生代码及权重身份须与原合格模型一致，不因缺失换模型/环境。缺资产/身份/闭合或旧STARTED未决则BLOCKED，不扫描/下载/重建旧结果。

科学脚本、所有实际依赖/私有监督器/预算/ledger辅助及独立核验脚本，在首次媒体读取/研究消耗之前完整封存；固定成员/模型定义/统计/指标/预算同步记录。仅首次解码或Qwen STARTED较早者之前可修纯软件预检错误，保留成本并重封；研究开始后任何失败不得改名、续步或重试同一输入。原封存记录不追认修补。

## 2 媒体准入与CPU输入准备

**网络/新下载0。** 仅复用已登记固定`event_sequence_zip.body`，大小2783546023B。允许一次完整流式SHA256读取≤3GiB，匹配固定发布版LFS SHA256或既有已核内容SHA及原身份链；只记录新hash而没有原预期身份不能算匹配。发布目录Git oid与媒体LFS内容SHA不可混用；身份不足则STOP_ARCHIVE_IDENTITY。沿用原研究使用边界，不外推成全部原视频权利认证，不公开媒体。

ZIP目录只读≤16MiB/4096项，路径/重复/链接/加密/压缩比按既有安全规则；只映射066固定100个视频名，缺失/冲突不替换。仅这100成员允许抽取，单成员压缩≤32MiB、解压≤64MiB、ratio≤100；所选压缩读取累计≤512MiB、解压文件累计≤1GiB，写新067根，不覆盖旧包/缓存。完整大小/CRC一致后才解码。其余媒体不打开；预算不足报BLOCKED_INPUT而非换50对。

沿用057/060既有PyAV/NumPy的全时域12均匀中点、最近PTS/CFR与index-clock一致性规则，输出uint8[12,224,224,3]。只解码该100段，累计遍历≤200000帧；不按事件边界采样、不剪接、不手工标注/更高分辨率或新依赖。CPU媒体/输入准备监督累计≤900秒。输入失败记清实际成本和计划成员，不补样/重解码已消耗失败项。

同原processor/tokenizer在CPU检查grid[6,14,14]、pixels[1176,1536]、纯文本≤128有效token、形状/有限性与原接口。q严格用066的原事件字符串模板，062 tau AST及闭包不变。保存100条问题无标签清单和当前V输入；不访问另一格预测或答案构造输入。12个旧头/normalizer通过原seal与形状/有限性检查，不拟合统计。

比较新媒体内容/RGB与已登记旧060/057缓存身份以及同接口Qwen输入账本，不能仅换mode/任务ID包装历史输入。若与旧同接口输入完全相同或STARTED未决，本包停止并报告INPUT_ALREADY_CONSUMED/UNKNOWN，不重新编码、不换成员；不在本包建立新的旧cache迁移分支。新100视频内部精确重复可先封存alias并复用同次闭合特征，仍保留全部50计划实例。未检出精确碰撞不证明物理来源或预训练独立。

## 3 单次冻结Qwen GPU阶段

仅全部输入/代码/标签角色/资产身份准入后开始。使用既有共享非阻塞GPU锁及持久账本，锁忙或free不足立即GPU_BUSY，不等待/轮询/杀他人进程。GPU信息命令至多1次，确认原单块RTX3090、free≥18GiB、设备身份。GPU监督外层**≤600秒**（含探测/单次加载/同步/卸载收尾），worker停止发新调用期限≤480秒、留清理时间；allocated峰**≤16GiB**、GPU Job RAM≤32GiB/active-process≤4。不得复用上一包时钟或额外预热。

既有Qwen3-VL-4B-Instruct只加载一次，local_files_only、无联网、eval/no_grad/所有参数冻结，原bfloat16/sdpa/processor/native实现不变。**最多100次V＋100次纯文本q＝200次特征高层调用**，分别也受子上限约束；B0/generate/其他问题或探针0。模型底层root/视觉/decoder/layer计数另报，不将高层200与底层forward混算。

V取decoder前主视觉merger的294×2560，按6×49×2560仅空间均值得[6,2560]；不用DeepStack/新层。h(q)取纯文本最后有效token最终hidden[2560]，CPU float32存储；同原接口，不添加/更换提示或截断超长文本。每个实际输入在调用前STARTED、完成同步/形状/有限性/预算检查后CLOSED；失败/超时/OOM不重试、不重载或改batch/精度。全部特征封存且主模型卸载、自有GPU Job实际active0后才CPU旧头预测。GPU阶段只读无答案输入，不读publisher标签。

## 4 12个旧头与2400正式单格

仅063六新seed137/263/419/557/733/911的C_NATIVE/D_NATIVE final state，原056 TemporalHead(2560,2560)、356673参数、严格logit>0。CPU float32/线程4，全部参数冻结、grad None，无loss/backward/optimizer；初始化构造不是新训练，不做软件warmup/探针头forward。原062各自train84的mu/标量RMS直接冻结，C=h(q)、D=[h(q)−h(tau(q))]/2后同原float64统计应用/float32视图；不读旧train特征重拟合。

每次predict仅当前V/q视图。每头50×4=200单格，共**2400新头forward、600个重复运行四格**；独立条目分母始终50，不叫600新实例或300独立来源。无N/HASH/新seed、投票/互补翻转、checkpoint选择或新B0。所有输出/账本/权重身份封存且预测Job actualactive0后才评分。CPU预测/评分/独立复核监督累计≤600秒。

固定12条件行、6条D−C配对：单项/视频对/问题对/四格正确数与率、五类输出模式/K0..K4、问题不敏感及缓存/新项/INVALID/FAILED/NOT_RUN/unknown/计划分母齐全。任何不完整/非CLOSED二元输出使相应准确统计和主结论NA/INCOMPLETE，不当有效错误、不删项或续跑。提前BLOCKED也交完整计划12行和NA，0模型调用不是0%准确率。

## 5 判定与四个可公开复算的均值区间

本包主问题仅为冻结D−C在固定未评分条目上的平均差。完整时，六seed平均四格D−C>0记`POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE`，≤0记`NO_POSITIVE_MEAN_ITEM_TRANSFER_DIFFERENCE`；每seed正/零/负与绝对准确率完整报告，不另设“新机制PASS”或修改063的20%失败结论。问题不敏感D−C正表示更差，不能替代答题。来源仍UNKNOWN，即使正也仅为条目迁移描述；任意结果后不在此池调参/扩样或选新头。

最高可证重采单位当前为50个两视频实例，每单位1例，不能将逐例正确性/匿名P01行上传。评分角色私下先求每实例跨六seed的答题差之和与不敏感差之和，各取值−6..6；**仅公开这两份13箱频数直方图，共26行，含零频箱**，不含实例ID/排序/映射或各seed的逐例向量。各直方图count合50、加权和与6配对表净值之和一致；保留同实例跨seed依赖，不能把300项摊作独立。

四个95%均值区间：答题与不敏感各两个条件轴，不额外做每seed区间或p值。配对单位轴固定六头：将相应13箱按−6..6展开成长度50的规范有序向量，Random55066一次生成10000个choices(range(50),k=50)；每draw的pp为100×sum(所抽seed-sum)/(6×50)。两种统计各按自己的规范向量求**边际**区间，不能解释为相同实际成员对齐的联合重抽样/交互。seed轴固定同50实例：六seed整套净差按137/263/419/557/733/911顺序，Random55067一次生成10000个choices(range(6),k=6)，求等权平均pp。2.5/97.5%分位线性position=(10000−1)p插值。点估计、四区间全部保留，两个轴不合为联合泛化认证。

若媒体在任何新模型输出前提供确证更高共享来源关系，不悄悄更换此统计或按分选聚类：STOP_SOURCE_DESIGN_MISMATCH，交事实再审。未取得更高关系时如实维持文件配对单位的条件解释。这个呈现设计是隐私与算术复核安排，不是新研究创新。全输出完整才计算直方图/区间，否则相应26/4行NA，不伪造零计数。

## 6 取证、成本与边界

独立核验不得import被测评分器/做任何头或Qwen forward、optimizer或再次解码；可只读CPU torch核实际特征/视图、12权重/normalizer及前后身份。由原publisher标签和全部私有预测重建12/6表、两直方图/4区间、固定成员/2400账本和全部停止/unknown；核decode/PТS/frame索引/processor输入、代码seal/模型身份、GPU调用/锁/Job闭合和真实预算。数学整数fixture可用，不能新做模型夹具。公开负责人复核限聚合/静态代码，不冒充私有或OS取证。

预算除前述媒体900、CPU预测评分复核600、GPU600秒外，资产/代码/其他CPU监督≤300秒；父≤10800秒含写作。CPU Job RAM≤8GiB、GPU Job≤32GiB，active-process≤4/线程4；新独占067根≤3GiB/2048文件、起始free≥4GiB，主模型权重不复制。原归档整包hash≤3GiB一次＋所选压缩读取≤512MiB另计；新特征/views逻辑读≤128MiB，12旧头及normalizer逻辑读≤64MiB，旧元数据/manifest/相关账本≤32MiB。必要模型权重完整身份hash≤12GiB一次另计、模型单次加载I/O另列；不递归哈希/复制模型目录。旧私有预测/正确性及训练标签/特征/计划读取0。

新root内媒体/processor缓存/特征/ledger/标签只私有保存，记录精确逻辑读/解压/张量净载荷和保守界，不将其伪称物理I/O或最终硬配额。所有失败/修复/已花成本和自有Job actualactive0/no kill保留；不得杀他人、删除旧锁/账本、重置计时或使用新ID重问已STARTED输入。环境/模型/依赖安装或迁移0，研究数据网络0，TimeBlind/TempCompass访问0，已用源重问0，主模型/小头训练0。前提不闭合或预算不足即安全停止，保留计划NA，不继承余量。

## 7 精确九处交付并停止

仅新增以下八文件并向results追加一次067父结果：

1. `prototypes/frozen_item_transfer_067.py`
2. 本目录`execution-receipt.md`
3. `scientific-results.md`
4. `condition-summary.csv`（12行）
5. `paired-summary.csv`（6行）
6. `mean-intervals.csv`（4行）
7. `difference-histogram.csv`（2指标×13箱＝26行；无逐例身份/向量）
8. `execution-summary.json`（完整/阻断状态、全部计划/实际调用与分母、资产/代码/媒体/模型范围、四区间、判定及所有限制/成本/未知）
9. `docs/codex-results.md`仅一次append

不上传原QA/事件/标签/逐项预测或正确性、数据/模型hash/私有路径/源映射、特征/视图/normalizer/权重/媒体；公共科学代码自身LF SHA可报。不得改原论文/PDF、旧结果/源码、规划或本README。核精确allowlist和append-only、普通安全push main后STOP，不自动068或投稿。负责人验收同回合给下一步，不以“必须继续”制造新机制。
