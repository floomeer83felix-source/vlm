# VLM-ENGINEERING-EVIDENCE-040 — 工程论文的比较、消融与独立复现

- 日期：2026-10-24（北京时间）。
- 状态：**READY / PUBLIC_CPU_ENGINEERING_BUNDLE / NOT_EXECUTED**。
- 权威协议：[engineering-runner-comparison-2026-10-24.md](../../research-protocols/engineering-runner-comparison-2026-10-24.md)。
- 执行者：用户当前本地Codex。研究负责人下达协议，不把拟定任务当成本机已执行。
- 启动条件：最新main仅本父包READY、results没有本ID交付，且用户发送第6节完整新消息。远端READY不自行唤醒或继承GPU权限。

## 1. 目的与一次性工作范围

本轮承接用户“先按工程稿推进，再判断核心期刊机会”的方向。一次完成可复用public小工具、强基线、三组件消融、实际子进程故障对照、开销及干净目录复现，产出决定论文路线是否值得继续的证据。

本轮不依赖丢失的原标注、旧私人运行目录或近邻论文PDF；此前144逻辑格选帧信息通道候选**PARKED / NOT_READY**，其元数据输入交接暂缓，不在040索要路径或读取正文。038–039图形时钟变体及原C/D核心路线保持停止。新CPU故障负载不是继续那些VLM行为变体。

## 2. 有序A–H包（均 INCLUDED IN 040，不另成READY）

| 子任务 | 实际交付 |
|---|---|
| A 冻结与公平性 | 读协议、现有公共证据和必要公开代码；列六配置的真实差异、540格队列和独立oracle规则，先冻结再运行；指出实现无法支持的项。 |
| B 独立runner | 新stdlib-only auditable_runner_040.py：工作子程序、绑定收据、持久claim/ledger、生命周期、评分准入；同时实现B0和强SQLite B1配置，不导入旧私有/公共research执行链。可参考030公开Win32结构，但新模块运行时不导入030/025/026。 |
| C 有意义验证 | 新test_auditable_runner_040.py：公共API、真实跨进程竞争/异常退出、绑定差异及退出准入的关键行为；独立观察断言，不复制F validator充当oracle。允许开发调试，正式测量前最多2次完整suite、≤12个明确标记SMOKE格。 |
| D 故障benchmark | 新benchmark_auditable_runner_040.py：协议九家族×十重复×六配置=540格，一次正式测量。真实barrier/子进程/后代/exit17，保留失败和未送达；无模型。 |
| E 开销与组件归因 | 同case配对比较正常输入的wall、CPU/peak commit/输出；六配置完整家族表，三项消融能否解释差异；B1可能完全达到F的目标，不隐藏这一结果。 |
| F 干净目录复现 | 只复制三个新源文件，现有Python隔离模式执行help、一个正常例及12个指定小复现格；记录旧模块/私人依赖是否为0、成功与失败，不自称独立机器复现。 |
| G 论文价值裁决 | 写贡献/先例矩阵，区分官方工具文档对照与本轮自实现实测，按协议第7节给出可否继续工程论文的证据；不输出未经验证的录用概率。 |
| H 交付与结束 | 七处allowlist、完整逐格CSV及两报告，results仅一个040父追加含A–H状态；脱敏审查，一次普通安全push main后STOP。 |

A–C可修新源码以实现冻结科学定义；源码/队列/参数hash正式封存后，不修改继续测第二套结果。某独立配置/家族不支持可记UNKNOWN/UNSUPPORTED继续其他安全工作；无法保证本轮进程清理则停止所有执行。不要把单点不支持转成搜旧路径或又造一个HOLD占位包。

允许读取：当前main公开AGENTS、next-steps、results、overview、本README/协议、新三模块、030/039公开实现及以下两份历史执行证据：
- [018真实三臂收据](../VLM-UNSEEN-SOURCE-STRATIFIED-018/three-arm-new-source-receipt.md)；
- [039实际输入与运行收据](../VLM-CLOCK-COMPONENTS-039/component-input-and-run-receipt.md)。
这些只能证明既有推理曾执行和其当时成本，不能与040的CPU负载拼接成同一比较实验。可读现有stdlib相关源码定位API；无需全盘搜索或重新泛检索文献。无新增包/服务安装。

## 3. 执行与资源范围

仅在现有Windows/Python环境运行新公共CPU程序。用tempfile.mkdtemp创建全新040实验根；清洁复现另建一个新根。不得复用既有integration_0xx/模型根或旧任务账本。读取/执行新模块不等于授权导入Torch、Transformers、NumPy、模型processor、权重或CUDA。

| 项目 | 本轮上限/规则 |
|---|---|
| 父任务 | 5400s，从本轮同步/实现开始，包含等待与清理；不改run重置。超限保留partial，交付已完成证据。 |
| 执行包络 | 新suite累计≤240s（≤2×120s）；开发smoke累计≤120s、≤12格；正式benchmark≤900s；clean复制复现≤120s；初始化/清理预留120s；合计受监督wall≤1500s，另报实际Job user+kernel CPU，不把wall冒充CPU秒。 |
| 进程 | 每格工作组含至多2个工作进程及1个后代；每格外层watchdog≤5s，Job committed≤512MiB。调度/观察器与工作组分开计数；一次最多执行1格。登记后代用barrier释放，独立自退出上限2s。 |
| 反复调用 | 正式540格×冻结请求序列；工作入口总上限720次。额外只准≤12个开发SMOKE格及独立复现13格，分别计数；不得重跑正式坏例填表。 |
| 输出 | 两个新临时根合计≤10000文件/128MiB。首个输出前实测所在卷free≥128MiB+2GiB并记录；超出停止，不扫描/删除旧目录凑空间。 |
| 隔离/清理 | 所有运行的工作进程在执行主体前进入本轮Job、禁止breakaway；外包络不参与准入，独立保留fallback事实。只可结束本轮创建且归属可证的组，实际active0后结束；不碰用户其他进程/旧锁。 |
| 环境与研究资产 | GPU/模型/训练、真实QA/gold/标注/旧帧/旧预测/private helper、实验网络/数据下载/媒体解码、安装/新环境/永久系统修改均0。仅GitHub文档同步/安全push允许联网。 |

如果进程API初始化失败，先在C阶段修复或给出公开错误依据；不为了走通删实际组退出条件。所有正式队列格保留PLAN/ATTEMPT/RETURN/INVALID/FAILED/UNKNOWN/UNSUPPORTED/NOT_RUN等可区分状态。已消费后不执行与“根本没被调度”分开，不能把UNKNOWN改成成功。

CPU程序作用域只含新临时根；不需要用户填私人路径。故障注入仅限本轮自造bytes/收据和子进程；不破坏真实数据库、原资料或其他服务。Windows实际已测才说已测，其他OS不编造支持。

## 4. 报告内容与验收

engineering-results.md：
- 六配置实现/公平性与冻结hash、540完整分母、预检/smoke/正式/clean四类运行数量；
- 九家族×六配置的准入违反、重复执行、合法完成、未知/未送达/未运行；
- B0、B1、F与三项消融的配对正常成本；实际Job CPU和wall区分、peak commit/磁盘/清理/fallback；
- 真实注入和外部观察的方法，至少每故障家族一个可复核证据摘要；不能只写PASS；
- 协议缺口、失败、开发修复和第7节规定的保守裁决。

reproducibility-and-prior-art.md：
- 三文件公开CLI、现有Python要求、完整Windows复现命令；不写个人绝对路径；
- 新空目录的help/正常例/12格复现实际结果和旧依赖0或实际缺口；
- 官方工具文档与实测参考配置的区别、贡献/先例矩阵；
- 仍欠真实推理接入、跨机器复现、实际现成工具比较等证据，不宣称040已完成这些工作。

benchmark-rows.csv：
- 全540行，不筛好例；协议第6节规定逐格信息。复杂请求序列可用规范化短JSON字段或明确报告附件索引；公开数据必须足以重算汇总。
- 无PID/用户名/私人完整路径/原QA/gold/device ID；生成的公共case/数值/hash可公开。
- clean/smoke另在报告完整记录，不混入540行正式主表。

验收是“可核查、比较公平、能否定自身”的交付，不要求F一定优于B1。只证明普通组合有用不能升级核心机制；负结果照常交付，不扩任务寻找更有利故障。

## 5. 公共allowlist（恰七处）

1. prototypes/auditable_runner_040.py
2. prototypes/benchmark_auditable_runner_040.py
3. prototypes/test_auditable_runner_040.py
4. docs/codex-artifacts/VLM-ENGINEERING-EVIDENCE-040/engineering-results.md
5. docs/codex-artifacts/VLM-ENGINEERING-EVIDENCE-040/reproducibility-and-prior-art.md
6. docs/codex-artifacts/VLM-ENGINEERING-EVIDENCE-040/benchmark-rows.csv
7. docs/codex-results.md：末尾恰一个040父结果，原字节前缀不改。

不改本README、冻结协议、AGENTS、next-steps、overview、旧代码/tests/报告和历史记录。实现只用标准库，三个新模块足以运行；勿复制旧庞大项目或上传临时实验根。stage前查路径和内容，只一次安全push；若main已变按AGENTS处理，不force/reset/rebase/绕过冲突。交付STOP，不自行041、真实QA/GPU或论文投稿。

## 6. 用户完整启动消息

以下作为一条新消息发送当前本地Codex；若旧聊天已满，可开新聊天按GitHub-first交接。此消息激活整个A–H包，不需逐项再问。

~~~text
继续工程论文方向。安全同步独立GitHub文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md，及docs/codex-artifacts/VLM-ENGINEERING-EVIDENCE-040/README.md和docs/research-protocols/engineering-runner-comparison-2026-10-24.md。确认040是唯一尚未交付的READY父任务，连续完成A–H一整包。

我明确授权本轮仅用现有Windows/Python标准库：新建两个040临时根，实现独立runner、benchmark和关键验证，执行B0普通监督、B1强SQLite、F完整方案及三组件消融；固定九家族×十重复×六配置=540正式格，包含真实输入变化、跨进程重复调度、工作后异常退出、收据错配、过早评分及后代仍存活。先封存队列/源码/参数，再一次正式运行；保留全部失败、未送达、未知、未运行，不重跑坏例补表，不把CPU负载当模型推理。

按合同执行：父5400s，受监督wall合计1500s；suite≤2×120s，开发smoke≤12格/120s，正式benchmark≤900s/工作入口≤720次，clean复现≤120s；每格watchdog≤5s、工作组RAM≤512MiB，两个新根合计≤10000文件/128MiB，首输出前记录配额外≥2GiB余量。工作进程执行主体前纳入本轮Job，禁止breakaway，只清理本轮可证归属进程，实测active0；不动旧锁或其他用户进程。

完成三文件干净目录复现、540行完整数据、基线/消融/开销表和贡献/先例裁决。B1若同样达到目标必须如实写明，不预设F优越，不宣称exactly-once或核心期刊录用。144格选帧候选暂缓，本轮无需旧标注/私人路径。

GPU/模型/Torch/Transformers/processor/训练、真实QA/gold/原标注/旧帧/旧预测/private helper、实验网络/下载/媒体解码、安装/环境/永久系统修改均0。只按七处allowlist提交三新模块、两报告、完整CSV和codex-results一个040父追加；一次普通安全push main后STOP，不自动041或扩大范围。
~~~
