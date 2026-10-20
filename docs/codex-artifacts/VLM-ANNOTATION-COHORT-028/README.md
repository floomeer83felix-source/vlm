# VLM-ANNOTATION-COHORT-028｜安全容器兼容诊断、真实筛选与独立旧源join

**2026-10-20｜唯一READY父任务 / PUBLIC_PARSER_CPU_ONLY，尚未执行。**
**私人阶段须用户新消息明确授权028 CPU范围，并明确接受下述窄容器profile；
一般“继续”只执行公共源码/虚构验证。GPU、模型、媒体正文、真实gold值及下载均0。**

## 1. 为什么是这一包

[027交付42776af](https://github.com/floomeer83felix-source/vlm/commit/42776af041a708d6ffd7e15a8ad011b79557f3fb)
已修复并观察到当前输入的ctime_ns跨API差异，完成持久输入预算及独立fixture评分链。
[027回执](../VLM-PILOT-PIPELINE-REPAIR-027/engineering-repair-receipt.md)报告14项新测试通过，
但真实标注索引在累计读取212992 raw bytes后INVALID_JSON。实际字符位置、token类别与
错误成因UNKNOWN；这不是已证明文件损坏、含NaN或没有合格题。

027 coordinator还把旧记录中的所有字符串与annotation universe相交，并在index失败后
向manifest请求空集合；该依赖导致零请求/零匹配，不能作为已完成旧源join。
028只解决这两个实际缺口并完成可行的真实候选交接；不重写监督器、不重复资产盘点、
不重跑025/026/027或任何旧suite/QA，不消耗旧任务剩余额度。

本包是当前输入路线的**最后一次有限容器兼容与筛选门**：
若实际输入仍不符合下面事先冻结的窄profile，记录明确错误类别后STOP该标注分支，
不自动029、不再以空资格/合成任务续命；独立旧源join等已准许工作仍完成。
若原窄题型语法匹配0，也不放宽语法补题。后续改数据来源/标注版本/研究口径需新决策。

## 2. 显式版本化的容器profile（不是默认宽松JSON）

025原协议和原历史结论保持不变；028新增**容器层**profile，明确改变兼容性假设，
不冒称旧025严格JSON门已通过。题型语法、两事件定义、原来源/题序、四臂、48→12、
C/D同两个锚点、预算和分母规则均不变。

[Python官方JSON文档](https://docs.python.org/3.9/library/json.html#infinite-and-nan-number-values)
说明标准库默认会接受JSON规范以外的NaN/Infinity/-Infinity。**这只是可预先定义的
兼容分歧，不是本机027错误的诊断结果。** 禁止为诊断而整文件json.load(s)，也禁止
strict=False、正则删内容、修改原文件、把错误值替换成null、最后一个重复键胜出或
忽略非法转义。

实现两个显式且固定的profile：

| profile | 精确行为 |
|---|---|
| STRICT_025（默认，旧调用行为保留） | 原严格词法规则，NaN/Infinity/-Infinity继续拒绝；重复键/非法语法等继续拒绝。 |
| SKIP_NONFINITE_028（须用户新消息明确接受） | **仅当当前值本来就不允许解码/保留**时，允许完整且大小写精确的裸token NaN、Infinity、-Infinity作为词法跳过；不转成Python float，不传给value decoder，不存原token或值。记录安全类别计数。其他任何非标准语法均拒绝。 |

- token必须有合法JSON值边界；NaNxxx、+Infinity、nan、undefined、注释、尾随逗号、
  非法控制字符/转义、畸形数、重复键、额外根值、深度/字节/字符串超限继续HOLD。
- token在获准保留的metadata/task/question/选项出现，返回ADMITTED_NONFINITE_HOLD，
  不生成值、不剪裁、不修补。未来batch gold若出现非canonical值，评分仍应HOLD并保持
  full planned N/UNKNOWN准确率；本轮只用虚构gold验证此接口，不读任何真实gold值。
- 合法字符串里的文字NaN等是普通字符串，不算非标准token。对象键仍只按严格JSON字符串
  解码以检查重复；非标准profile不能扩大字段白名单或解码任何保护/非batch值。
- 默认STRICT_025行为不变；私有manifest/plan/流receipt必须显式绑定选定profile及实现
  版本，未来末期scorer要采用同一profile，不能准备时兼容、评分时无记录地换规则。
- diagnostic只保留常量reason、parser state、字符类别、nesting与私有字符位置；
  **不能保存/打印原token、邻域、原题、选项、gold、canary或带doc的JSONDecodeError**。
  公开只报告汇总类别/计数，不报告私有路径、键、offset或摘要。
  解析字符位置与底层raw预读字节计数分列，不能把212992当精确错误字符位置。
- 完整投影必须到合法容器末尾/EOF并通过稳定性/完整流字节绑定；
  raw缓冲区已读满文件不等于解析已完成。保护值解码次数必须有仪器化反例验证。
- 真实新读取前冻结上述规则并用虚构样本验证；实际观察后不得扩大允许token集合、
  修改字段白名单、放宽语法/阈值或追加输入重开次数。

## 3. 一轮连续完成的六项工作

| 子项 | 工作 | 完成/受阻判断 |
|---|---|---|
| A 公共兼容与安全诊断 | 在现有streaming projector上做最小版本化扩展，严格默认不变，增加不含内容的状态/类别诊断；接口支持明确profile传递，不用动态import/猴子补丁。 | 旧严格门和新兼容门分别报告；本轮不能先验把NaN当真因。无法证明未解码边界则不读真实标注。 |
| B 新范围的一次索引与screen | 用户明确授权后，已知精确标注先一次index-only（零scalar保留），若完整则一次精确batch screen；同一profile、稳定输入绑定。保留实际source/question数、支持/不支持原因与profile差异类别。 | index失败不重开；screen失败不补开；错误不是三种窄兼容token就拒绝。不得整文件decoder、复制或清洗原标注。 |
| C 独立旧源join与证据保存 | 先按已知记录schema从旧源/027现成nongold记录提取真正UID/group字段，不把任意字符串都当UID；不要与annotation universe相交。先保存最小获准旧投影，再向官方manifest请求旧UID与已完成index UID的并集。 | 即使index失败，已知旧UID仍要完成独立manifest join。分别报requested/matched/missing/duplicate及013/014缺项，不把空请求叫零匹配失败或认证完整排除。 |
| D 固定候选、选项与成本交接 | 原025语法和来源顺序/原索引不变，已知origin/participant/派生排除与组内去重；最多4源各1题，先冻结screen键再投影该≤4题各5选项。记录实际候选N/可执行N及profile/权利/映射缺项；只stat有确切引用的候选媒体。 | 坏选项或媒体缺失不换题；不以历史28/1182补实际数，不将当前权利或013/014缺证当已通过。无file-size字段就UNKNOWN，不凭历史GPU额度猜成本。 |
| E 针对新边界的验证 | 新028 suite覆盖严格/兼容差异、零保护值decode、三个token完整边界与各类非法syntax、admitted非有限值拒绝、prefix/half-read/EOF、profile绑定、坏虚构gold full-N HOLD、index失败仍能独立旧join。 | ≤2次新suite，优先一次；不运行旧suite，不再重复进程/模型/selector证明。没有额外fixture worker需要，不启动模型/真实scorer。 |
| F 一次结案交付 | 一份安全词法/profile与CPU回执，一份实际cohort/旧源join/剩余证据交接，results末尾一条父结果，单次安全普通push后STOP。 | 输入仍不兼容则INPUT_CONTRACT_NO_GO_CURRENT_FILE；语法无候选则COHORT_RULE_NO_GO；真实候选成功也仅是CPU交接，不自动真实pilot READY。 |

028只复用027已经完成的身份/持久预算/worker静态映射与监督边界，不重复读取真实runner
或执行原factory。旧source记录缺013/014时明确记录；不要把历史引用丢失再做一轮目录盘点。
未来真实评测的记录组探索/物理独立UNKNOWN、clock/instance UNKNOWN限制保持。

## 4. 私人范围：仅在用户发出本合同末尾指令后成立

只使用当前私人Codex会话中既有两个精确入口（主dev标注、官方release-1 manifest）、
既有017/018根和已明确的旧源roster/manifest路径；不得扫描/glob/猜文件、读替代副本或
下载数据。不要求重复提交已保留路径；引用确已丢失时只报告缺少类别，继续独立安全项。

允许字段：
- 标注的UID一致性、来源/版本/时长/已知参与者group、任务/题文/原始题索引；
  最后仅冻结≤4题的各5个模型输入选项。其他选项、正确答案、参考时间、canary始终词法
  跳过，不解码。容器profile只识别上述三类裸非有限token并丢弃，不保留保护值。
- 官方manifest的必要UID/group/version/duration/participant/known-derivative/canonical字段；
  CSV其余cell不保留，不读取任何网络/凭据。027已证header为video_uid，仍检查本次实际schema。
- 旧源只投影UID/origin/participant/version/已知派生字段；不读旧题文/选项/gold/预测。
  可只读027已知精确输出中的nongold结构/预算receipt/输入引用，不进入其原始题文或源文件副本。
  027没有完整标注快照，其partial摘要只能作可比辅助，不当作完整输入证书。

唯一新的私有目录 **`<AUTHORIZED_018_ROOT>/integration_028`**，root沿用已知精确018根。
旧integration_026/027及所有原实验文件/锁/账本只读。新目录已存在、祖先重解析或身份冲突
则停该分支，不换后缀、不清理旧记录。私有投影/候选/选项/身份/profile/摘要只留新目录。
公共模式只在文档checkout自有新028 fixture目录工作；两个模式共用本包总预算。

| 类别 | 028新有限上限 |
|---|---|
| 标注内容open | index-only≤1、screen≤1、最终≤4题inference≤1；共≤3，每次文件≤4MiB，失败角色不重开 |
| 官方manifest | ≤1次open，文件≤8MiB；独立旧join与annotation join同一遍完成，不重复读 |
| 精确旧源roster/manifest | ≤8份、各≤1MiB、各≤1次内容open |
| 027已知nongold/receipt/输入引用 | ≤6份、各≤1MiB、各≤1次内容open；只需获准的结构/group/receipt字段 |
| 真实runner/model/env盘点 | 0；复用027静态交接，不导入/运行任何旧runner或读取权重 |
| 研究输入总额 | ≤48MiB保守预扣，实际读取另外精确记账；沿用已修复的持久预算机制但建立独立028账本，027余量0迁移 |
| 本地新增输出 | 全部028输出≤128文件/32MiB；不保存原混合gold容器、原token或原始错误邻域 |
| 媒体 | ≤4个确切引用的本地文件stat；正文/hash/probe/decode均0；没路径就UNKNOWN、不猜 |
| 新028验证 | ≤2次受监督suite、各自有child≤120s；首轮失败最多一次静态修订后的验证，旧suite启动0 |
| CPU与协调器 | 所有本包自有PID单调墙钟保守累计≤600s，单child≤120s；协调器受控窗口累计≤1200s，嵌套计入，不扣内部等待 |
| 额外fixture/model worker | 0；只需新suite与CPU投影/独立join子进程，已有监督测试不复跑 |
| 禁止 | 真实gold值/模型/Torch/GPU/训练/媒体正文/研究网络下载/安装/环境或ACL修改均0 |

先通过本轮虚构安全边界验证，才允许启用已被用户明确接受的profile和真实新读取。
同一输入/profile不因代码修订重试。持久计数损坏/打不开则停止读取，不新建账本清零。
必须把028改动留在公开可审查协调器，不靠临时launcher绕过root/phase计数。
可以参数化现有coordinator的027/028固定contract-id与各自新目录名；禁止任意run-id
解锁旧integration_027输入，旧任务journal不得重写。只枚举本轮新输出目录以核对预算。

## 5. 公开执行allowlist（八处）

1. `prototypes/temporal_evidence_adapter_025.py`：仅streaming词法层的默认严格/显式028窄profile、
   诊断与投影传参；**decompose/select_four/build_plan研究规则不改**。
2. `prototypes/temporal_evidence_scorer_025.py`：仅matching profile传递/绑定及新虚构gold边界；
   既有逻辑gate、one-shot guard、full-N与预测/gold canonical规则不改，真实gold调用0。
3. `prototypes/temporal_pilot_prepare_026.py`：profile传递和字段感知的旧源投影/独立join支持；
   不回退已验证的身份/流稳定性条件。
4. `prototypes/temporal_pilot_coordinator_027.py`：固定028模式/新root/独立ledger、相位profile绑定、
   持久化最小旧投影与去除错误universe依赖；旧027报告保留版本关联，不运行旧suite。
5. `prototypes/test_temporal_annotation_profile_028.py`：新增只针对上述修复的虚构断言。
6. `docs/codex-artifacts/VLM-ANNOTATION-COHORT-028/annotation-profile-receipt.md`：
   当前安全诊断/strict vs compat状态、解码仪器化、profile与EOF/字节绑定、失败/次数/计数。
7. `docs/codex-artifacts/VLM-ANNOTATION-COHORT-028/cohort-and-source-handoff.md`：
   实际schema/筛选/cohort/选项计数、独立old UID join、来源与权利/媒体成本缺项和决策。
8. `docs/codex-results.md`：末尾仅一条 `### VLM-ANNOTATION-COHORT-028`。

本README、025原研究协议、027历史回执/结果、AGENTS/board/overview、supervisor模块及旧测试
不在执行修改范围。028明确准许上述旧公共模块的定点修复，历史事实仍绑定原提交。
不得以“profile变了”为由重跑历史模型、改真实问题/选项/gold或宣称严格JSON认证。

分开报告 STRICT_CONTAINER、COMPAT_CONTAINER、NO_PROTECTED_VALUE_DECODE、
CURRENT_DIAGNOSTIC_CLASS、INDEX_SCREEN、INDEPENDENT_OLD_JOIN、COHORT_FREEZE、
PROFILE_BOUND_SCORING_FIXTURE、REAL_PILOT_READINESS。
真实输入未完整走过新profile时不能宣称已定位027历史根因；profile非标准token为0
也不自动认证历史同一输入。私有版本/摘要可辅助，不能扩大为来源权利/OS隔离证书。

检查脱敏/allowlist后，单次普通安全push main并STOP；失败不自动重试push，不自动029。
若输入无兼容路径或原题型规则无候选，明确NO_GO当前路线并提交独立已完成项；
真实候选成功则准备基于实际N的后续资源/媒体/当前权利方案，不能先批GPU再找数据。
**REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**

## 6. 用户一次发送给当前Codex的指令

执行VLM-ANNOTATION-COHORT-028。先安全同步main并重读AGENTS、next-steps、results、
overview及028 README，确认唯一READY=028且未交付。

我明确授权028合同内的新有限CPU数据范围及SKIP_NONFINITE_028容器profile：
只在本来就不保留的值上词法识别并丢弃NaN/Infinity/-Infinity，获准保留字段仍拒绝，
其他非法语法不放宽；这不是授权读取真实gold或修改原文件。只用已有精确入口，限额
只读nongold、≤4题各5选项、旧源group和027已知nongold交接；私有产物仅写已知018根的新
integration_028目录。输入≤48MiB、输出≤128文件/32MiB，open/CPU/测试次数按合同。

连续完成A–F；只运行新028验证，不重跑旧任务/测试，不用027余额。若输入不属冻结profile，
标注分支一次失败后停止，完成独立旧源join等安全工作，不自动另开修复父任务。
GPU/模型、真实gold值、媒体正文、下载、安装和ACL修改均0。统一一个父结果，安全push一次后STOP。
