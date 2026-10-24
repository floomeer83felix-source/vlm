# 040 工程证据协议：可审计执行、强基线与故障对照

- 冻结日期：2026-10-24（北京时间）。
- 父任务：[VLM-ENGINEERING-EVIDENCE-040](../codex-artifacts/VLM-ENGINEERING-EVIDENCE-040/README.md)。
- 状态：**PROTOCOL_FROZEN / NOT_EXECUTED / ENGINEERING_NOVELTY_UNVERIFIED**。
- 本协议由研究负责人维护；执行者不得按观测结果修改任务、对照、分母或判据。

## 1. 本轮要回答的论文问题

用户同意把当前工作优先推进为工程/系统论文。候选主题为“资源受限环境下视觉语言模型实验的可审计执行与输入一致性验证”；题目不是已成立的创新或录用承诺。

本轮只检验一个工程命题：**把实际工作输入绑定、执行前持久消费、实际进程退出后的评分准入组合起来，能否在保留正常任务完成能力的同时，减少可重复触发的执行/评分合同违反，代价多少？已有标准技术能否同样实现？**

交付必须包含实际 OS 子进程、可核查的注入事件、强对照、组件消融、逐例数据和脱离旧私人目录的可复现入口。计数器模拟、手填状态、只测纯函数或“测试全绿”不能替代对照实测。本轮工作负载是公开程序生成的 SHA-256 计算，**不是模型推理、VLM准确率或 GPU 性能实验**；不可用它估计真实模型延迟收益。

## 2. 先例与比较边界

研究负责人已读取以下官方材料（访问日 2026-10-24），本轮无需再派一轮泛综述：

| 先例 | 已有能力/本轮处理 |
|---|---|
| [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) 与 [System Metrics](https://mlflow.org/docs/latest/ml/tracking/system-metrics/) | 已记录参数、代码版本、指标、产物与系统资源；“有日志/资源表”本身不是创新。 |
| [Ray Tune FailureConfig](https://docs.ray.io/en/latest/tune/api/doc/ray.tune.FailureConfig.html) | 支持配置失败恢复次数，0关闭恢复；恢复语义不能直接当作不可重复副作用的 at-most-once 证明。 |
| [lmms-eval commands](https://github.com/EvolvingLMMs-Lab/lmms-eval/blob/main/docs/getting-started/commands.md) | 已有逐样本日志、预测缓存、完整性检查等；文档还说明共享缓存与分运行目录。不能声称只有本项目能留存输入或缓存。 |
| [SQLite transactions](https://www.sqlite.org/lang_transaction.html) / [atomic commit](https://www.sqlite.org/atomiccommit.html) | 事务、唯一键和持久状态是必须面对的传统强方案；本轮实做 B1，而非只和裸脚本比较。 |
| [Python subprocess](https://docs.python.org/3/library/subprocess.html) / [Windows Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) | 进程监督、等待、超时和进程组管理已有标准工具，不能作为新机制命名。 |

前3项是**官方文档能力对照，未安装、未运行、未证明其不能扩展支持本协议**。B0/B1是本轮自实现的明确参考配置，不是 MLflow/Ray/lmms-eval 的替身性能。原先例 URL 和所读版本/访问日写入报告；动态 main 页面不冒充固定 release。新的有限主张是这套具体故障合同、验证材料及集成成本是否有工程用途，原创性仍待检验。

## 3. 六种配置：两项参照、完整方案及三项消融

所有配置共用同一工作子程序、负载字节、外部观察器、平台实现、资源外包络和队列。禁止为基线减少超时处理、忽略错误或故意写错结果。公平性审查先于正式运行。

| 标识 | 必须实现的配置 |
|---|---|
| B0 | 合理的 Python 子进程监督：显式 returncode 检查、直接子进程 timeout/kill/wait、原子写结果、检查返回key/计划manifest/code/config摘要、仅复用已成功完成的同 key 缓存；单次请求不隐式重试。没有持久的执行前消费、实际读取字节绑定或整个后代组退出准入。 |
| B1 | 强 SQLite 参照：每配置一个本地 DB，唯一逻辑 key；BEGIN IMMEDIATE 事务提交消费记录后才发起工作；同 key 不再消费；校验实际 payload/code/config 收据；实际子进程及后代组归零后才准入评分。synchronous=FULL、journal_mode=DELETE，明确处理 SQLITE_BUSY，不能把锁冲突算成功。 |
| F | 待检方案：每逻辑 key 一个原子排他创建的持久 claim，写入/fsync STARTED 后才发起工作；逐调用记录串联 key/code/config/实际 payload 摘要和终态；实际整组退出后准入一次评分。不依赖 SQLite 或旧研究目录。claim存在但记录不完整时保守UNKNOWN，不删除claim复跑。 |
| F-NOBIND | 与F相同，只取消“实际读取的 payload 字节摘要必须等于冻结输入”的准入检查；仍收集实际摘要供观察器判定，其他绑定/消费/退出条件不变。 |
| F-NOCONSUME | 与F相同，只取消持久的执行前排他消费；保留已完成缓存和其余检查；不偷偷加入其他等价的前置去重。 |
| F-NOEXIT | 与F相同，只取消评分准入时的实际整个工作进程组归零检查；清理与外部安全监督仍保留。 |

F与B1保护目标相同，仅持久表示/实现不同。**B1可能完全匹敌F，这必须作为“普通技术足以实现”的实质否定证据。** 原子文件、hash链、事务、输入摘要、一次评分均不单独宣称新算法。不得把文件方案更快预设为结论。

同一源码用明确策略配置选择，避免复制六套不一致的 worker。F与三个消融只允许表中单一行为差异；B0/B1的代码路径与设置公开。共享平台监督层可以复用；各自的存储逻辑不得冒用另一配置的结果。

语义是 **at-most-once admission/dispatch under tested process faults**。持久消费与外部计算没有同一原子事务：消费后崩溃可能损失完成机会，已执行但未留终态应UNKNOWN。不是 crash-safe exactly-once，不保证断电、磁盘损坏或恶意进程隔离。

## 4. 冻结负载与540格队列

每种配置执行同一90个逻辑例：9个家族×10次重复；共 **90×6=540个配置-案例格**。重复只反映本机调度/测量变化，不是10种独立系统或真实故障率样本。

共同工作：对同一 payload 连续做64次 SHA-256（每次对原payload，最终返回最后摘要），无sleep替代正常计算。payload为 SHAKE-256(UTF-8字符串 `VLM-040/v1/{family}/{rep}`) 按需输出指定字节数；rep=0..9。结果有格式、逻辑key、worker源码摘要、参数摘要、实际读取payload摘要和结果摘要。基线也有同样收据可用，是否强制检查由第3节定义。

| 家族 | payload | 冻结干预/判定证据 |
|---|---:|---|
| N1K | 1,024 B | 无故障正常完成。 |
| N64K | 65,536 B | 无故障正常完成。 |
| N1M | 1,048,576 B | 无故障正常完成；用于观察输入绑定成本随字节数变化。 |
| INPUT_DRIFT | 1,024 B | 预检之后、worker实际读取之前，在barrier处把最后一个字节 XOR 1；按实际读取字节计算，不能用预检摘要伪装实际值。禁止重做输入消掉故障。 |
| DUP_ACTIVE | 1,024 B | 第一工作已进入且被barrier暂挂时，独立第二调度进程对同key请求一次；随后共同释放。不能用单进程内存set替代跨进程竞争。 |
| CRASH_AFTER_WORK | 1,024 B | worker已执行并写独立观察事件，正常终态提交前 os._exit(17)；确认实际退出后由新的调度进程提出一次同key恢复请求。不能恢复已消费key或把缺失终态补成RETURNED。 |
| RECEIPT_MISMATCH | 1,024 B | worker正常退出后、监督者接收前，将输出收据的code摘要首个hex字符切换为另一个合法hex；结果数值不变。所有配置接收同样被改变的收据，不改某方案内部DB或claim。 |
| EARLY_SCORE | 1,024 B | worker提交完整RETURNED收据后仍在可验证barrier中活动；对同key请求一次评分准入，再释放/等待真实退出，若先前未准入则允许一次正常末尾请求。 |
| DESCENDANT_ALIVE | 1,024 B | worker创建一个本轮已登记的短生命周期后代，提交收据且自身退出；后代在barrier中仍存活，此时请求一次评分准入；释放后代并实测整组归零后，若先前未准入则允许一次正常末尾请求。 |

对 INPUT_DRIFT 和 RECEIPT_MISMATCH，拒绝后不修改输入/收据再提交。对 CRASH_AFTER_WORK，只允许表内一次恢复请求，没有第三次。其他家族没有恢复/补跑。正常成功缓存的既有结果不能执行第二次。所有请求与拒绝都留痕，不能用重复计算后只留最后结果。EARLY_SCORE和DESCENDANT_ALIVE的早期请求是非阻塞准入检查；观察器收到准入/拒绝事件后才释放barrier，禁止先等退出再把一次晚请求标为早请求。

执行顺序精确定义：rep从0到9，家族按表序；六配置基础顺序[B0,B1,F,F-NOBIND,F-NOCONSUME,F-NOEXIT]，每个(rep,family_index)左轮转(rep+family_index)%6。每一格自己的新存储空间/同一配置DB中的唯一key；跨配置仅配对，不共享结果缓存。

正式前输出完整540行planned队列、参数和三份实现源码摘要；正式测量开始后不改源码、阈值、顺序或选择哪些格纳入。操作nonce只用于新目录防混淆，不影响payload或配对。SQLite初始化、文件存储初始化分别单列成本，不把某配置初始化藏入/挪出计时来制造优势。

## 5. 外部观察器与真实故障

benchmark观察器不调用F的“eligible/valid”函数作真值。它独立生成原始payload期望摘要/结果、在受控barrier前后核验干预、记录所有调度请求、实际工作入口/完成事件及已登记进程/Job状态。每次worker调用写自己的观察事件文件，避免多个worker并发append伪造计数；这些oracle文件不给方案准入逻辑读。

工作子程序从实际读取并用于计算的同一bytes生成收据，不能只回显命令行里计划hash。外部程序知道原输入和明确翻转后的字节，可独立核对。收据不是恶意worker可信执行证明，本协议仅覆盖自有受控worker的所列进程故障。

故障触发需要**实际证据**：
- DUP_ACTIVE第二调度发生在第一实际工作入口之后、释放之前；
- CRASH实际exit17发生在工作完成事件之后、正常终态提交之前，恢复请求来自新进程；
- EARLY_SCORE时原worker实际仍活；DESCENDANT_ALIVE时原worker已退、登记后代实际仍活；
- INPUT_DRIFT实际读取摘要等于干预后字节且不同于计划；RECEIPT_MISMATCH被送达的收据字段确实改变。
仅收到“注入成功”布尔值、墙钟sleep推断或自报EXITED标志不足。故障没送达记 **INJECTION_NOT_DELIVERED**，整格仍在540分母，不计为防护成功；不得重抽一次删掉失败。

所有配置处在相同的外部Windows Job安全包络中，worker必须在运行用户代码前被纳入，禁止breakaway；观察器在包络之外。外包络只限制/清理本轮创建的工作组，不替方案作准入决定。B0若依靠外层清理才终止后代，标明fallback，不能算B0自身完成整组监督。无权查询/终止用户其他进程。平台能力不支持的格标UNSUPPORTED而非伪造观测；保留其余独立安全格。

## 6. 指标、计时与完整分母

每个540格至少公开：case/family/rep/profile、计划与实际调度数、工作进入/完成数、终态、注入送达状态、每次评分请求及准入、违规类型、整组归零证据类别、外层fallback、端到端wall/工作wall/Job CPU（可测时）/peak committed/输出字节、错误或NOT_RUN原因。不公开PID、用户名/完整路径/设备ID。

核心指标分别报告，不能合成一个“成功率”：
1. **准入违反格数及次数**：允许评分时，实际输入或绑定不合合同、结果错误、同key累计执行>1，或任一登记工作进程仍活。一次错误准入不能被后续正确拒绝冲销。结果摘要错误和输入错误分别列出；后续评分发现答错不使输入错误成为合法实验。
2. **重复执行**：同key实际工作入口>1的格数、总额外次数；STARTED记录数不能代替实际工作次数。
3. **可用性**：正常30格的合法完成/拒绝/未知/失败/未运行；另列DUP_ACTIVE、EARLY_SCORE、DESCENDANT_ALIVE这30个可安全完成故障格的合法最终完成。拒绝所有输入不能算有效方案。
4. **崩溃代价**：已工作但终态不明、被消费而不能恢复、0次实际工作却损失的机会分别报告（没有观测到也保留0）。不能把所有UNKNOWN算保护成功或真实故障率。
5. **开销**：正常3种大小各n=10，按同case配对报告F/B0与F/B1端到端差值/比值、median/min/max；如给经验p95，用nearest-rank且说明n=10不足估计生产尾延迟。包含输入读取/摘要、持久化、启动、等待和最终准入，不从端到端扣掉自认为“不相关”的成本。单列共享oracle与平台层，不能声称已扣除其真实开销。
6. **证据覆盖**：计划540、尝试、送达、完整可判定、INJECTION_NOT_DELIVERED、UNSUPPORTED、失败、NOT_RUN全部列出。分家族/配置表不缩分母。

正式队列只有一次。预检/开发smoke与正式数据分开保留；正式开始后遇实现bug不修改再补跑，只在可安全继续的独立格继续同一源码；受影响与未运行保留。确定输入不安全或无法清理自己的进程则停止执行阶段。不得为了完整漂亮表格自动开启第二轮。

## 7. 独立复现与本轮价值裁决

在另一个全新临时目录仅复制3个新public .py，清空PYTHONPATH、使用现有解释器的 -I -S 隔离模式；先验证help和1个正常例，再固定完成6配置×2家族(N1K、CRASH_AFTER_WORK)=12个小复现格。隔离模式可用importlib按__file__的同目录确切路径加载新模块，不能依赖cwd/PYTHONPATH或已安装包。不得import旧030/038/039及私人helper，不访问旧config、数据、模型或交接根。Windows实际测试就只称Windows已复现；“源码可移植”不等于Linux/macOS测过。独立目录不是独立研究者/机器复现。

结果报告给出逐项“候选贡献—已知技术—本轮实证—仍缺什么”矩阵：
- 实际输入/代码收据一致性；
- 执行消费与崩溃后的不确定性；
- 退出后评分准入与后代生命周期；
- 资源/运行成本及独立公共复现入口。

**预先规定的科研处置：**
- F如果正常任务大面积拒绝、故障未送达或证据不闭合：IMPLEMENTATION_OR_EVIDENCE_INCOMPLETE，不能据此证明工程优势。
- F优于B0且消融解释成立，只能说明这些已知机制在受控案例中有用。
- B1同样满足目标且F无清晰可重复成本/使用收益：**NO_DISTINCT_MECHANISM_EVIDENCE**，不得改名宣称新事务/新可靠性算法，停止继续堆框架包装创新。
- 即使F有可重复收益，也只是**ENGINEERING_CANDIDATE_SUPPORTED_ON_CPU_FAULT_HARNESS**；仍需之后由负责人决定真实推理接入、实际工具的公平比较和目标期刊适配。CPU假负载不替代这一证据。
- 无论结果如何，交付一次有完整负结果的基线/消融/开销研究即可结案。不得自动写“核心期刊可投”、造成功指标或在本轮扩成GPU/训练。
