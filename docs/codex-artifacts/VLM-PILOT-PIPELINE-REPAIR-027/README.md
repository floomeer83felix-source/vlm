# VLM-PILOT-PIPELINE-REPAIR-027｜工程修复、真实筛选与运行器交接整包

**2026-10-20｜唯一READY父任务；PUBLIC_REPAIR_CPU_ONLY。**
**私人数据阶段仅在用户向Codex新发本合同末尾的明确027 CPU范围指令后执行；
看板READY本身不授权私人读取。GPU、模型、真实gold值、媒体正文、研究下载均0。**

本任务依据用户“先把工作任务写进仓库，再给Codex执行指令”的要求下达。
用户一次发送末尾指令即可同时触发公共修复及所列限额CPU数据阶段，不需要先回复
批准、等待改看板、再发启动消息。若用户只说一般“继续”而未明确新数据范围，
只完成公共修复和虚构验证，真实阶段记SCOPE_NOT_GRANTED，其他安全子项继续。

## 一、要解决的实际问题

[026交付](https://github.com/floomeer83felix-source/vlm/commit/a17d7b5f48844360fd6aaf064dd502164954068c)
按PARTIAL结案：[回执](../VLM-REAL-PILOT-INTEGRATION-026/real-pilot-integration-receipt.md)及
[验收](https://github.com/floomeer83felix-source/vlm/commit/cc80ac65abf4c9cf24d149ae06323262dad6a21b)。
实际标注/一份runner打开时身份检查失败；协调器有未导入asdict和错误/计数不可恢复问题；
manifest真实header、013/014旧源引用与后端映射未闭合。进程fixture通过不等于这些已解决。

027是**有新明确范围的修复任务**，不是重跑026、再做资产盘点或另写一套selector。
允许定点修改026的两个公共工程模块；026原交付事实仍绑定a17d7b5，历史测试/报告不改。
不重跑025/026或013–024任何原测试/QA，不消耗或“恢复”旧任务额度。
[025科学协议](../../research-protocols/temporal-distance-diagnostic-2026-10-20.md)的语法、
来源顺序/原题索引、四臂、48→12、C/D两锚点、末期评分和分母规则保持冻结。

## 二、八项连续工作

| 子项 | 本轮必须完成的工作 | 验收边界 |
|---|---|---|
| A 同步与可执行协调器 | 安全同步独立文档checkout，重读AGENTS、board/results/overview、本合同、025协议及026两份报告；核唯一READY=027且无既有027父结果。将027协调器作为公开可审查源码提交，写清imports/相位/错误码/退出与预算路径；禁止靠临时字符串launcher串完整流程。 | checkout不干净/非安全FF即停；不能声称曾核过的026 READY检查PASS。协调器即使NameError/子阶段失败也留下可恢复的安全错误与非退款账本。 |
| B 身份检查根因与兼容修复 | 分开文件身份、内容稳定性和API字段差异；先用新建虚构文件在现有Python/Windows上验证，再修InputBudget。公开只报字段名差异掩码/稳定性结论，不报真实数值或路径。 | 不预设ctime是根因；不可直接忽略全部时间/身份字段或接受缺省0相等。保留链接/重解析拒绝、大小限制、同一文件证明、读前后变更拒绝、完整流摘要与不完整读取HOLD。 |
| C 持久输入预算和错误记录 | open计数/字节预扣在open前原子持久化；不同相位/子进程共用唯一027输入账本。失败不退款，重新启动只恢复已消费计数，不重试已失败输入。使用显式imports（如dataclasses.asdict）和安全phase/alias/reason/exception-kind/errno字段；不只保存stderr行数。 | 不创建新的InputBudget重置计数；不靠第二个文件别名或不同run_id绕过失败记录。持久记录失败则停止真实读取，不能边读边猜总额；原始trace/私有值不入公开报告。 |
| D 真实schema、manifest与旧源排除 | 在新数据范围下完成索引→screen；原语法不改。manifest先识别实际header并选唯一明确UID列映射，拒绝歧义/重复/缺列，不硬猜video_uid。仅从已知精确旧源记录/获准源码的定向AST字段恢复013/014/R1–R6与已知派生引用。 | 不扫描目录找输入、不全文件json.loads解码混合标注、不读旧QA/预测。缺映射如实分项UNKNOWN，不当空集合，不因缺013/014就跳过整份实际screen。 |
| E 候选冻结、选项与成本 | 按原JSON来源顺序/原题索引每源首个支持题，执行已知origin/participant/派生排除及组内去重，最多4源各1题；先冻结题键，再投影这≤4题各5选项。记录准确supported/unsupported/excluded/unknown与候选N，区分可执行N。仅stat有精确引用的候选媒体，并记录声明字节/版本/权利缺项。 | 选项坏、媒体缺失不替换题或调语法；0匹配就诚实给出原规则结果，不再以toy任务扩展此分支。权利/映射不全不冒称真实READY，0冻结≠0合格；不能用历史28来填写实测N。 |
| F 真实worker静态映射 | 用已确知runner AST与026已有nongold交接，补inputs(i,ids)的自由变量/closure/model/processor/decoder参数映射；在唯一新私人目录写接入副本，输入只来自冻结nongold，选项只用于最终prompt，不进入event/embedding。 | 不导入/执行旧runner、Torch或模型，不改原实验文件。列真实符号映射和缺失项；compile通过不等于运行成功、实际token相等或OS隔离认证。 |
| G 把监督与绑定接成一条链 | 以固定cohort/配置摘要绑定run identity，拒绝换名称重复启动。定点修现有监督接口：自有child的启动起算deadline、有限stdout/stderr与清理；将一次流绑定核验和027虚构批次评分实际放进独立CPU child，只有退出成功且绑定一致后才发布。 | 测试必须覆盖进程未退零opener、摘要错/半读不发布、独立scorer失败后guard仍消费、账本重启/alias防绕过与自有超时不误杀peer。不是把callback通过和另一个child启动通过分开冒充整体接通；真实gold仍0，OS权限拒绝仍须独立说明。 |
| H 一次交付 | 分项报告A–G实际状态、工程根因/修复、完整计数、真实schema/题数/候选/来源与权利缺口、backend静态映射，列证据支持的下一真实试点提案。仅一条027父结果、一次安全普通push后STOP。 | 无真实数据范围或某输入HOLD，继续独立公共修复/虚构验证和其他已准许工作；不再拆多个资格或盘点父任务，不自动028/GPU。 |

### B的技术要求：不能靠放松守卫取得PASS

[Python官方samestat说明](https://docs.python.org/3.9/library/os.path.html#os.path.samestat)
给出stat/fstat记录的同一文件比较；
[stat_result说明](https://docs.python.org/3.9/library/os.html#os.stat_result)
说明时间字段含义/精度受平台/文件系统影响。两者不是对本机失败字段的认证。

实现应分别保存path-stat与handle-fstat观测；用有依据且在现有运行时验证的同一文件
判断关联二者，再检查各自读前后稳定性、大小、流完整性和原始字节摘要。
若跨API元数据差异已得到复现，明确哪些字段用于身份、哪些用于各自稳定性，
不能只把五元组全等改成“长度相等即可”。有效身份不可取得、链接、替换、增长、
读中修改、未到完整容器末尾均应拒绝或HOLD。
samestat/摘要本身不认证媒体权利、恶意并发对抗或OS隔离。

先在027自有fixture验证未变文件、不同文件/路径替换、元数据差异、截断和半读。
可只修改自有fixture的内容/时间来造反例，不改任何真实输入。
保持现有Python3.9.21兼容；不得假定新版本才有的API参数、下载安装或切换环境。

## 三、私人数据阶段的新明确范围（仅由用户末尾指令激活）

### 准许精确入口及字段

沿用现有私人Codex会话中已经明确的017/018根和已恢复的两个精确入口：
主dev标注、官方release-1 manifest。只按此前精确引用或从准许源码中明确读取的
路径字面量定位，不扫描、glob、猜文件名或找替代副本；不让用户重复提供已保留路径。
确切引用已丢失时只标缺少类别，先完成其他安全工作；不能用找不到路径再次空跑整包。

- 标注：来源/版本/时长、必要UID/group/已知参与者、任务/题文/原索引和UID一致性；
  先索引，再screen，最后只对已冻结≤4题保留各5选项。
  所有正确答案、参考时间、canary、其他题选项始终词法跳过，不解码或提前校验。
  读取混合容器字节不等于只有nongold字节；允许同一投影流累计私有字节摘要，
  禁复制整份含gold原标注或额外重开来hash。
- 官方manifest：仅必要UID/版本/来源/时长、已知participant/派生关系、canonical声明大小。
  先据实际header选择明确映射，记录其依据；不动态猜字段或读无关私人映射。
- 旧源记录：只读已确知的013/014/R1–R6精确roster/manifest中的UID/group/version/已知派生
  字段；026已有nongold交接/输入receipt/源码AST记录可只读，但不能将零字节未完成receipt
  当有效snapshot，不能打开026/旧实验的题文、选项、正确答案、预测正文或混合原文件副本。
- 真实源码：最多6份已确知qualifier/runner/scorer，文本/定向AST-only。
  可从明确的排除UID/输入引用赋值中恢复交接，不能执行脚本或输出任意literal值。
- 媒体：只有≤4条经既有精确授权引用或核实的确定性映射取得的路径可stat，正文0；
  当前权利只用已有明确证据，未知照实记录，不读凭据/认证配置、不发网络认证请求。

### 私人输出与新预算

只可创建一次 **`<AUTHORIZED_018_ROOT>/integration_027`** 新目录；
root是已有私聊精确018根，不是搜索范围。旧integration_026及原实验文件、旧锁/账本只读。
新目录已存在或重解析/身份异常就停止该写分支，不换后缀、不清理旧目录。
真实冻结题/≤20选项/身份/路径/摘要/worker接入只留在新目录，不入Git。
只有公共修复模式时，虚构测试用文档checkout内新建的027 fixture目录，绝不进入实验根；
两个模式共享027总文件/字节/时间与fixture-worker计数，不各开一份额度。

| 类别 | 027新上限与失败规则 |
|---|---|
| 标注内容open | ≤3次，各角色索引/screen/inference各≤1次，文件≤4MiB；失败角色不重开 |
| 官方manifest | ≤1次内容open，文件≤8MiB；失败不重新下载或重开 |
| 精确旧源roster/manifest | ≤8个、各≤1MiB、各≤1次内容open |
| 026已知nongold交接/receipt/AST产物 | ≤8个、各≤1MiB、各≤1次内容open；无目录枚举 |
| 已确知真实源码 | ≤6份、各≤1MiB、各≤1次内容open；原旧tests/runner执行0 |
| 零正文诊断句柄 | 仅上次失败的标注与那一份确切runner，各额外≤1次，正文0；也预扣该文件statted大小、记open，不退额；优先在正式打开的同一handle取得诊断 |
| 研究输入累计 | **≤48MiB**保守预扣，实际读取另记；所有相位/PID共用一个持久账本，旧026余额不迁移 |
| 媒体 | ≤4个有确切引用的本地路径stat，正文/probe/demux/decode/hash均0 |
| 新增027本地输出 | 所有027输出合计≤128文件、≤32MiB；私有写仅上述新目录，公共模式虚构输出仅文档checkout自有目录 |
| 全部受控动态CPU | 自有每child≤120s，全部PID单调墙钟保守累计≤600s，嵌套计入；各协调器执行窗口累计≤1200s，不扣内部等待 |
| 027新验证 | ≤2次受监督suite启动；首轮失败只允许一次静态修订后验证；不得以self-test/CLI另开测试次数 |
| 虚构worker | 两次验证合计≤24次、各≤5s；持久预留失败不退款，均计入CPU总额 |
| 每child输出 | stdout/stderr各≤64KiB，超限停止自有child并记录；清理也受自有协调器deadline监督 |
| 禁止项 | GPU/模型导入或前向/训练0；真实gold值解码0；媒体正文0；研究网络/下载0；环境/ACL/包改变0 |

新增诊断/内容open是明确的027新范围，不是以026剩余额度绕过失败。
新验证先用人工虚构样本校验修复和相位联动，再进行已准许的真实读取；
真实输入失败不因为代码再修而额外重开。原始输入/schema不符只能用已获准保留的结构
诊断继续静态适配，不能通过重复open试错。缺授权时，真实open和私人写入一律0。

026第一次失败/计数失联也必须记入历史字段，但不能捏造精确旧用量。
本轮必须提供027自己的精确持久计数或明确保守已消费上界；若持久计数损坏则停止该
研究读取分支，不重置账本后继续。只对自己创建并持有的child/fixture作超时清理，
不查GPU、不删旧锁、不杀不明job。

## 四、公开执行allowlist与验收

仅允许以下七处执行交付：

1. `prototypes/temporal_pilot_prepare_026.py`：定点修身份、流绑定、manifest/schema、
   新预算接口所需处；不改变025语法/选帧，不重新实现一套研究算法。
2. `prototypes/temporal_pilot_supervisor_026.py`：定点修固定cohort identity、输出/时间界限、
   持久guard及独立CPU绑定评分链；不加入默认真实模型运行入口。
3. `prototypes/temporal_pilot_coordinator_027.py`：新增可审查的stdlib相位协调器，
   输入全由精确调用者注入、无真实路径默认值；公共fixture/明确CPU授权模式有清晰门。
4. `prototypes/test_temporal_pilot_repair_027.py`：只验证本轮修复的有意义失败见证与联动，
   人工虚构题/选项/gold，不能导入执行旧测试suite或读取真实数据以增加PASS数。
5. `docs/codex-artifacts/VLM-PILOT-PIPELINE-REPAIR-027/engineering-repair-receipt.md`：
   A–H分别状态、真实身份差异掩码/已定位与未知、失败/修订/启动次数、持久账本汇总、
   source/API兼容与进程/评分链实际边界。不得只报测试数。
6. `docs/codex-artifacts/VLM-PILOT-PIPELINE-REPAIR-027/real-cohort-handoff.md`：
   实际nongold计数/候选N与可执行N、来源排除及剩余缺项、接入映射状态和真实试点具体提案；
   私人身份/题/选项/摘要不公开，未做项不得用历史计数填充。
7. `docs/codex-results.md`：末尾只追加一条 `### VLM-PILOT-PIPELINE-REPAIR-027` 父结果。

027 README、025模块/协议、AGENTS、board/overview、旧测试、旧结果/报告都不可由执行者改。
027确可修两个026公共模块，这是本合同新下达的代码修复范围；不改026历史证据。
没有新私人范围时，本合同仍是可执行的公共工程修复任务，不因数据分支未获准而空交付。

报告分开给 IDENTITY_COMPATIBILITY、DURABLE_INPUT_BUDGET、COORDINATOR_RECOVERY、
REAL_SCREEN、SOURCE_EXCLUSION、COHORT_FREEZE、BACKEND_STATIC_BINDING、
ISOLATED_FIXTURE_SCORING 及 REAL_PILOT_READINESS 的状态。
公共测试通过不能替代真实schema/实际N/后端接入，CPU静态接入不能称ACTUAL_TOKEN_EQUAL
或真实OS gold隔离。真实pilot本轮不列READY；4源×1题×4臂只是上限，资源/当前权利/
媒体/数据范围/实际OS边界与GPU许可还需基于真实证据另行具体确认。
原025记录组探索与物理录制独立UNKNOWN、时间桥/事件实例UNKNOWN的研究限制均保留。

完成所有可独立的准许工作后，检查脱敏和staged allowlist，一次普通安全push main后STOP。
push失败不静默重试，不自动028，不用“还剩时间/槽位”做额外输入、测试或GPU。
**REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**

## 五、用户发给当前Codex会话的一次执行指令

继续027：安全同步GitHub文档仓库main，重新读取AGENTS.md、next-steps、codex-results、
research-overview及VLM-PILOT-PIPELINE-REPAIR-027/README，核唯一READY=027且未交付。

我明确授权本合同所列027新CPU数据范围：只用已有精确入口，限额只读真实nongold、
最多4题各5选项、旧源分组、必要源码和026已知nongold交接；只在已知018根的新
integration_027目录写027私人冻结/接入记录。全部读取、open、输出、CPU、验证与worker
次数严格按027合同计账；不沿用026余额，不重新执行026原任务或旧测试。
按合同连续完成A–H，某依赖受阻继续其余独立安全工作，统一提交一个父结果并安全push一次后停止。
GPU/模型、真实gold值、媒体正文、下载、安装和ACL修改均不授权。
