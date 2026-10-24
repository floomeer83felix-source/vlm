# 043：下载截止与持久记账修复（无网络CPU整包）

2026-10-24（北京时间）。**READY / CPU_OFFLINE_REPAIR_ONLY / NOT_RUN。**
父任务：VLM-FETCH-DEADLINE-ACCOUNTING-043；本包为唯一READY，042已消费，不重跑、不续传。
用户本轮原话为“一直继续下去，直到给出新的codex任务指令”；负责人据既有协作范围制定本次公开代码修复/本地CPU验证包。
无需再次确认本包内独立安全步骤；本许可不包括数据下载、真实媒体/标签、模型、GPU或后台续任务。

## 1. 修复目标与已知证据

042的[回执](../VLM-NATURAL-CLOCK-ADMISSION-042/clock-admission-receipt.md)与[16项汇总](../VLM-NATURAL-CLOCK-ADMISSION-042/candidate-clock-summary.csv)：
HEAD1/GET1均200，11534336B已持久化，首次下载Job实测913.25秒，完整媒体/时钟均0/16。
HEAD长度/ETag未留下可重建的持久记录，实际接收精确值UNKNOWN，该GET保守按≤4GiB记；不把失败请求记0或复用其余量。

本包只解决两个阻碍下一次有限获取的工程问题：
1. 阻塞连接/读取/写日志时仍有独立于worker的绝对截止与自有进程树回收证据。
2. HEAD校验、GET预留与意图在副作用之前持久化；中途进程退出后可离线重建元数据和保守字节责任，不依赖worker finally。

042公开代码在read之间检查deadline，监督循环还做目录配额读取；“单次read timeout”不是整个请求的绝对截止。
这些是源码与测量发现，**不声称已确定913.25秒中每段延迟的因果分解**。
修复用普通监督/写前日志即可，不重建040框架、不宣称新机制，不重开自然VFR或模型实验。

## 2. 起点、输入与隔离

按AGENTS先安全同步独立文档checkout，重读AGENTS、next-steps、research-overview、codex-results及本README。
确认恰一READY是043，且results无043的completed/partial/blocked记录；冲突或重复则STOP。
同一当前本地Codex聊天执行即可，不要求新环境/新聊天。

限定只读公共源码/报告：
| 路径 | 冻结Git blob |
|---|---|
| prototypes/epic_clock_admission_042.py | 62bc3ff492f07bcd4b872e17347311503f19f6c4 |
| prototypes/test_epic_clock_admission_042.py | 53e780fc619d7e2d2aa50a013709aba6d55bdbb4 |
| prototypes/auditable_runner_040.py | 3e56faf30afea1bed850c085bceb2afcc4fb257c |
| docs/codex-artifacts/VLM-NATURAL-CLOCK-ADMISSION-042/clock-admission-receipt.md | f2599e651a103c0db47a67ef2722098205d59f7c |
| docs/codex-artifacts/VLM-NATURAL-CLOCK-ADMISSION-042/candidate-clock-summary.csv | a20e00a0831bcaef491c6cf17c5b18702053ec5b |

可读042归档README和公开manifest定位合同，但不调用其中启动语句。
核Git原始LF字节身份，不因checkout CRLF转换改历史文件。
只准复用040的Job/Process底层平台能力及必要结构定义；不得执行其workload、旧tests、040/041/042主程序。
042源码只供审查，禁止通过其fetch/scan/suite/supervise角色启动旧工作。

新本地根固定为独立文档checkout同级的新目录`vlm-private-043`：存在即STOP，不覆盖/清理/探查旧043或042目录。
只检查该新根与必要父链非symlink/reparse及空闲空间，不扫描实验盘/home/下载目录。
既有Windows与Python/conda环境不变；标准库实现，不安装、导入Torch/av/Transformers或读取processor/权重。
不得读取042 partial、http-events、旧私有日志或重新查询HEAD来补缺失数据；公开回执已足够定位本次修复。

## 3. 连续执行的三个部分

### A. 实现最小独立修复模块

新增`prototypes/bounded_fetch_043.py`，只修请求生命周期与监督/回放，不复制视频扫描器或创建新科研框架。

**截止与回收**
- 一个attempt从Job/worker准备之前登记单一monotonic起点与绝对截止；进度、重试逻辑和每次read都不能重置它。
- 监督者独立于worker阻塞I/O；关键等待路径不得做目录枚举、磁盘日志/fsync、HTTP或等待worker finally。
  若复用040平台，须在新043层实现该等待策略，不改040源码。所有worker及其自有后代先分配受限Job再运行。
- 本轮短时故障验证：每case允许工作至起点+8秒；仍存活就发自有Job终止，起点+12秒内应确认active0，
  至+15秒内应完成该case受控收尾；启动耗时计入。提前正常退出也必须核整个Job active0。
  这些是事前验收阈值，不能因机器慢或测试失败临时加宽。
- 记录起点、最后活动、kill请求、active0、收尾、退出码/Job CPU/峰内存和实际wall。
  超过任何阈值原样记DEADLINE_VIOLATION；不能把调用kill的时刻写成已退出时刻，不能四舍五入成PASS。
- 工作截止与清理余量必须分列。未来900秒请求只可纸面映射为较早的工作截止+显式清理余量，
  **本包不跑900秒等待、不承诺操作系统任意调度下能保证精确900.000秒**。
- 自有组无法确认退出、监督计时失效或失控写入时，停止其余进程case；不按不确定PID杀其他作业。
  可以完成不再启动进程的静态说明，但整体不可PASS。

**持久元数据、计费与进程退出后回放**
- 先实现并固定写前状态顺序：attempt claim/配置 → HEAD发送意图 → HEAD结果与校验后长度/ETag（缺失亦显式记录）
  → 满额GET责任预留与GET发送意图 → GET响应校验 → 各块进展 → 终态。
  本地fsync/原子提交成功后才允许后继副作用；持久化失败就停止，不回退为仅内存计数。
- 保留URL身份或其固定引用、响应状态、声明长度、ETag、Content-Encoding、允许范围、单项/累计预留和事件序号。
  GET元数据不符时不调用body read；真实TLS/HTTP行为本轮未测，不能称网络兼容性已认证。
- 可用单worker追加日志+单独监督终态；不得让两个writer覆盖同一可变文件。
  最终回放须在active0后由独立角色读取持久数据，不使用已退出worker的result对象。
  末尾半条/损坏/缺序列要显式UNKNOWN并保留此前可信HEAD元数据，不能静默截尾当完整成功或重建出零耗用。
- before-GET预留整个已验证声明长度，而非仅已写盘块；进程中断或无法核销时保持该责任，不自动返还额度。
  记录“已持久进展下界、可证上界/完整预留、精确性状态”，明确区分read返回、写盘、日志落盘以及HTTP/TLS缓冲。
  **不把应用日志称网络线速/收包精确测量**，不能用最后完整块当全部已接收正文。
  无可靠声明长度时拒绝进入GET；不补猜042旧HEAD值或改其4GiB历史上界。
- 同attempt重复调用拒绝，状态UNKNOWN/FAILED/STARTED均已消费；监督失败设置本轮停止标志，禁止发下一个对象。
  不实现自动重试/Range/续传/换镜像/自动扩预算。

生产核心可通过注入transport/fixture接口验证，不能只测一个与修复核心无关的模型。
本轮所有入口只允许本地fake transport；子进程安装进程内网络拒绝守卫，禁socket创建/连接/解析/监听（含localhost）。
不得开本地HTTP服务、测试真实站点、调用042 fetch或访问媒体。守卫负例中被阻止的尝试单列，不能冒充实际HTTP发送。
这只是当前测试隔离，不改系统ACL、防火墙、代理或证书。

### B. 一次固定故障矩阵与独立回放

新增`prototypes/test_bounded_fetch_043.py`。先做与上述风险对应的纯逻辑检查（长度/编码/重复头、预算拒绝、状态机/截尾、固定截止不随进度重置），
再封存源码及配置，对以下12个case各执行一次。使用实际Windows自有Job/进程和受控本地fixture；纯虚拟时钟不能代替进程回收证据。
除正常/提前拒绝外，等待故障用有界sleep/barrier模拟，禁止忙循环压测；无需人为等满15秒。

| ID | 故障/路径 | 必查结果 |
|---|---|---|
| F01 | 正常完整小payload | 元数据与digest/终态可回放，active0；下界/上界与fixture一致 |
| F02 | fake connect阻塞 | 独立截止触发并清理；无GET/正文，不依赖worker超时返回 |
| F03 | HEAD已持久化、GET之前阻塞 | 强杀后仍恢复长度/ETag，GET0；不伪造成功 |
| F04 | GET元数据已持久化、首read阻塞 | 强杀后元数据仍在，保持GET责任预留，正文精确性不冒充0 |
| F05 | 慢速持续少量返回 | 有进展也不续绝对截止；持久下界正确，未知缓冲与预留保留 |
| F06 | read已返回一块、进展未持久化即os._exit | 回放不依赖finally，不漏算责任或把日志下界当全部接收 |
| F07 | 日志最后半条后退出 | 显式不完整/UNKNOWN，前缀HEAD信息仍可审计，禁止重发 |
| F08 | GET之前元数据fsync注入失败 | GET与body调用均0；不能以内存状态继续 |
| F09 | GET长度与HEAD不同 | 保留两份响应信息，不读body、不宣布成功、不自动下一对象 |
| F10 | worker日志/fsync阶段阻塞 | 监督不被该I/O拖住，按同一截止核active0 |
| F11 | 同attempt二次领取 | 第二次拒绝，fake transport无新增发送；不删除claim绕过 |
| F12 | 第一个对象UNKNOWN后尝试下一个 | 本轮停止标志生效，第二对象fake发送0，不重置责任 |

F01–F12是本地故障case ID，不是042的C01–C16媒体候选。
fixture小payload固定≤64KiB/对象，块≤16KiB；不用媒体字节或旧日志。
独立验证者只在worker组active0后读本轮fixture oracle/日志，对照冻结常量与真实fake调用轨迹；不得用被测最终status自证正确。
每case公开一行，12行分母不变；未运行/失败/超时保留，不删难例、不换阈值。附真实时间戳、kill/active0、元数据恢复、
fake发送/read数、持久下界/责任上界/精确性、重发拒绝、guard状态及明确PASS/FAIL/NOT_RUN。
涉及强杀的通过只表示该故障被正确处理，不能把故障当正常下载完成。

新suite和矩阵只允许一次初轮；若发现可定位实现错误，可在同包内修复后做至多一轮有理由的回归，
记录初轮所有失败/消费实例，在新case子目录重跑，不覆盖历史产物，不重跑042。
所有运行累计仍受总预算约束；预算不够就PARTIAL，不偷偷追加第三轮或更多压力测试。

### C. 统一回执与下一次获取的可行性交接

本包统一报告：
- 两项问题的源码级修改、实际12行证据、独立回放结果、源码/配置SHA、初轮与必要修复轮的全部实际资源与失败。
- 截止/持久记账在实测故障下是否通过，哪些只是公开代码静态结论，哪些真实HTTP/慢网/断电/跨机行为仍NOT_TESTED。
  fsync日志只按本轮进程退出模型验收，不声称电源故障/设备持久性保证或新颖事务机制。
- 在同一回执中写一份具体的“下一次获取是否值得执行/需什么新范围”交接：
  042旧attempt仍关闭，旧11MiB与≤4GiB责任原样保留，无需访问本地旧根；不得拿旧32GiB上限当新额度。
  可讨论原名单C02–C16作为尚未发送对象，但保留C01失败和16项原分母，不补第17源、不改科学门槛。
  发布文件大小仍UNKNOWN；11MiB/913.25秒仅是持久块/监督wall，不是可靠链路带宽或完成时间预测。
  不因043本地PASS就断言原900秒实际下载可行，不自行延长超时或批准新HEAD/GET。
  新的媒体范围须另由负责人审查、明确授权；本包只交可审查提案，不执行它。
- 若结果不能支持下一次有界获取，明确REPAIR_PARTIAL或FETCH_ROUTE_STILL_HOLD，结束本包，不续空资格任务。

## 4. 硬预算与失败处理

| 项目 | 本包上限 |
|---|---|
| 应用网络 | 实际socket/HEAD/GET/Range/媒体正文全部0；Git文档同步与allowlist推送除外 |
| 环境与数据 | 标准库/既有Windows Python，安装/环境迁移0；真实媒体/av解码/标签/旧私有资产0 |
| 进程 | 单case顺序；同时活跃自有进程≤3；单组RAM≤512MiB，计算线程1，无忙循环/压力测试 |
| 每case | 工作截止8秒；active0截止12秒；受控收尾15秒，从准备前起算，不能重置 |
| 正式运行 | 12case初轮一次，必要且说明原因的修复回归至多一次；不是允许无条件重复 |
| 总受监督执行 | 新suite/所有case/回放累计wall≤600秒；父包从首次本地执行起≤1800秒 |
| 新根存储 | ≤32MiB/512文件（包含partial/日志/fixture）；起步空闲须≥配额+2GiB |
| 模型与GPU | Torch/processor/权重、forward/generate/训练/GPU均0 |

所有计量包括失败与终止；共享准备只计一次，不把Job CPU与父wall相加成假成本。
严格区分受监督峰内存、根目录驻留快照和实际硬约束；不把采样目录大小叫Windows卷配额证明。
只清理所有权可证的本轮Job；旧根/旧partial/旧锁不动。监督或所有权不明就STOP，完整保留未知项。
逻辑/静态独立部分可继续完成，只要不再启动不安全进程；实测门未过时不可报全部PASS。

## 5. GitHub交付allowlist（仅五处）

1. 新增`prototypes/bounded_fetch_043.py`。
2. 新增`prototypes/test_bounded_fetch_043.py`。
3. 新增本目录`deadline-accounting-receipt.md`（含下一获取交接，不另增占位提案）。
4. 新增本目录`fault-cases.csv`（12个固定case；如有修复轮，用run_id保留两轮而非覆盖）。
5. 仅在`docs/codex-results.md`末尾追加一条043父结果，链接报告和CSV，列明状态/实际资源/网络0/最终STOP。

不改本README、任务看板/总览、042代码/tests/回执/CSV/manifest、040/041或其他旧代码。
不上传本地私有路径、实际媒体/原标注、完整环境/凭据或旧源重识别映射。
检查实际stage diff仅上述文件后安全commit/push main一次（无force），随后STOP执行轮；
既报completed/partial/blocked即043已消费，不继承余量、不自动044、媒体下载、Issue/PR或投稿。

## 6. 验收与启动指令

只有新核心实际承担上述状态顺序/截止，12case与独立回放均达标、无未披露资源超额且应用网络0，才报
**OFFLINE_DEADLINE_ACCOUNTING_REPAIR_PASS / REAL_FETCH_UNTESTED**。
失败则保留FAIL/UNKNOWN/PARTIAL及完整分母，不用13项旧suite或纯逻辑PASS代替本轮实际进程证据。
无论PASS与否，都不改变NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN、042关闭、标签/模型/GPU及既有停止结论。

用户在当前本地Codex聊天发送：
> 安全同步GitHub文档仓库main，重读AGENTS.md、next-steps、research-overview、codex-results和043 README，确认唯一尚未交付的READY父任务VLM-FETCH-DEADLINE-ACCOUNTING-043。按合同连续完成下载截止与持久记账修复、固定本地故障矩阵及下一次获取交接，统一脱敏推送后停止。仅标准库CPU，应用网络/媒体/标签/模型/GPU均0，不重跑042或续传。
