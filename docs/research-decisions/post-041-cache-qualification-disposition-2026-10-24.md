# 041验收与工程论文处置

日期：2026-10-24（北京时间）。审查对象：[6bcee08](https://github.com/floomeer83felix-source/vlm/commit/6bcee080ce00c82041d4567ddc2707977d9ae067)。

**ACCEPTED_CPU_BOUNDARY_CONTRACT_REPRODUCED / LOCAL_COMPONENT_REGRESSION_ONLY。041关闭，不重跑；当前0 READY，042未立项；NOVELTY=RETAIN0。**

## 1. 验收范围与证据层级

已重新读取AGENTS、看板、执行结果、总览、041合同、冻结协议及立项依据。交付提交直接继承6298e2d，恰六处allowlist；codex-results保持此前全文，仅追加一个041父记录。两个新模块、两报告及完整CSV均已审阅。未修改执行者历史记录或冻结科学条件。

负责人在本轮使用独立标准库程序复算公开记录，没有导入交付的重算函数、processor或模型。复核了完整队列、72份边界收据、36对关系及576条查询的逐项语义与成本。对独立程序可核的结论如下：

- 9家族×4刺激×AB/BA×4配置的288序列完整且顺序、轮转、case唯一性一致；每行两次查询，无分母删减。
- 从全部kwargs摘要、声明generation及匿名processor配置身份重新计算72个完整H与视觉/文本分区H；全部一致。另由公开token IDs、全1 attention mask、原生grid重建int64字节摘要，全部一致。
- 12对相同/24对不同的公开逐tensor摘要关系与记录相符；video为[6,12,18]/324视觉tokens，image为[1,12,18]/54。FPS/shift两家族同视觉摘要、不同文本摘要；pixel/order家族相反。BF16视觉shape/dtype及六个原生时间码与协议一致。
- 逐查询核对oracle H、已准备H、返回标记、hit/miss/BYPASS、终态、backend/callback/processor/内容hash调用次数，及各阶段计时字段；均一致，无记录中的FAILED/UNSTABLE/RELATION_MISMATCH/NOT_RUN。

以上是公开证据的独立一致性复核，不是负责人再次实际运行Windows处理器或独立见证torch.equal、OS事件、磁盘/进程状态。原始视觉tensor未公开，不能声称负责人独立重建了其字节。直接tensor比较、真实processor执行和资源闭合以执行者交付为依据。

核对新模块与公开040平台模块SHA256均与收据一致；四个固定上游夹具的原始字节SHA256一致，未发现缓存算法被替换。协议收据中的ed5de82…是同一Git正文转为Windows CRLF后的SHA256；Git LF正文为fc19700…，差异已明确归因行尾，不视为科学协议改动。

## 2. 独立复算结果

每配置72序列、144查询。下表“正确”只指INPUT_SHA256标记与当前边界身份相符，不是Qwen答案正确率。

| 配置 | 正确新算 | 正确复用 | 不兼容复用 | 查询processor次数 | 同输入保守miss |
|---|---:|---:|---:|---:|---:|
| UPSTREAM固定身份 | 80 | 24 | 40 | 80 | 0 |
| SOURCE_NAMESPACE | 136 | 8 | 0 | 136 | 16 |
| EFFECTIVE_INPUT | 120 | 24 | 0 | 144 | 0 |
| NO_CACHE | 144 | 0 | 0 | 144 | 不适用：全部BYPASS |

40次不兼容复用来自VIDEO_PIXEL、VIDEO_ORDER、VIDEO_FPS、VIDEO_SHIFT、IMAGE_PIXEL各8次，均为第二查询命中并返回第一查询的标记；前置问题改变的TEXT_CONTROL已由上游隔离。40/144是本冻结合成队列的条件频数，不能当作自然故障率。

SOURCE_NAMESPACE对完整新RGB、metadata、问题及生成/processor配置支付144次内容身份计算；16次保守miss来自等价时间表示与整数/浮点FPS表示，不是正确性错误。EFFECTIVE_INPUT保留24次同边界复用，但每次都先实际预处理，144次调用含24次hit。不能免费借oracle或把backend miss数换算为GPU节省。

正式查询processor总计504；加正式oracle72为576。suite4、clean13及全轮593/720是执行者报告，计数加总一致，不混入576查询分母。

| 配置 | 预处理s | 边界序列化s | 原始内容hash s | key/序列化包含式s | SQLite C调用s | 查询wall总s |
|---|---:|---:|---:|---:|---:|---:|
| UPSTREAM | 0.351374 | 0.236352 | 0 | 0.021163 | 1.675842 | 7.781681 |
| SOURCE_NAMESPACE | 0.603837 | 0.383835 | 0.175608 | 0.027398 | 1.690240 | 9.387379 |
| EFFECTIVE_INPUT | 0.609967 | 0.405487 | 0 | 0.024727 | 1.710516 | 9.376988 |
| NO_CACHE | 0.622427 | 0.417174 | 0 | 0 | 0 | 5.508612 |

成本由CSV独立求和，与报告逐项一致。单次队列、sys.setprofile观察开销、SQLite反复开关及共享机器负载限制性能排序；包含式计时不可与query wall累加。本轮只有CPU标记backend，不证明模型推理提速或实际产品速度优势。

## 3. 实现、复现与资源限制

固定ResponseCache在callback前计算已有身份，hit跳过backend；上游前置文本、模型、任务和评测版本身份并非缺失。SOURCE/EFFECTIVE在两请求之间关闭并重开同一DB、更新task_fingerprints，是本轮明确干预；三个缓存配置采用相同生命周期。没有执行create()、完整lmms-eval CLI、其Qwen适配器或OmniCompass路径。

clean为同一Windows/Python/processor机器上的固定8序列16查询，报告13次实际预处理、与正式子集一致；沿用新正式oracle作比较参考，不能称独立机器、独立oracle或完整用户复现评估。公开命令仍需使用者创建根、队列、配置并提供授权runtime/processor定位，不是已验证的全自动复现安装包。

执行者报告suite/formal/clean均exit0、Job active0、自然退出、无kill；受监督wall96.704s，峰值Job commit1,185,935,360B，线程4、CUDA未初始化、权重及模型执行0。首输出前磁盘free432,658,755,584B，超过32MiB+2GiB；两根37文件/1,302,111B。这些收据按其明确范围接受，不冒充负责人本机重测。

保留两项测量缺口：输出规模是驻留快照，并非原子硬磁盘配额或累计写入遥测；Job CPU/峰值是分阶段值，并非逐查询Job采样。源码的Python审计hook、单次运行惯例和外层监督也不是对抗性隔离或跨主机防重入证明。因此本次验收不写“全部资源合同已获独立认证”。不为修饰报告另开补丁微包。

## 4. 科研与后续裁决

接受的命题是：**在显式保持旧身份而改变callback内容/合法时间metadata的组件接口条件下，旧响应确实可复用到不同的实际CPU边界输入；已有完整源命名空间在本轮全部控制上避免了这种复用。**

不可变task/doc_id/data约定下，静态身份可以合理；本轮刻意改变内容但保持身份，未证明受支持真实工作流中会合法发生未版本化输入变化。没有真实基准污染、Qwen答案变化、自然发生率或完整CLI缺陷证据。已有命名空间/全输入hash能处理观察到的案例，因此不能把增加hash、回归测试或输入绑定包装为新机制。

沿用冻结立项依据中的先例边界，不声称本轮新增穷尽文献检索，也不把未运行的vLLM/OmniCompass算作实测比较。041新增可审查的接口回归材料，**仍未解决工程核心期刊稿的核心贡献缺口**。

按事前停止条件关闭041；不追加合成缓存变体、GPU验证、自动042、上游Issue/PR或投稿。下一次立项须先有独立可核的真实合法工作流、在遵守现有版本/命名空间合同后仍存在的具体缺口，以及可测实际收益；这只是研究准入标准，不是已下达执行任务。

当前0 READY；144格选帧候选及路径交接继续PARKED。040 NO_DISTINCT_MECHANISM_EVIDENCE、算法NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、原C/D及038–039停止、TRAIN-GPU HOLD、历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP全部保持。

原始交付：[输入/缓存/成本报告](../codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/cache-input-results.md)、[288行CSV](../codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/cache-input-rows.csv)、[复现/价值报告](../codex-artifacts/VLM-CACHE-INPUT-QUALIFICATION-041/reproducibility-and-value.md)。
