# VLM-REAL-PILOT-INTEGRATION-026｜一次性真实试点接入任务包 A–H

**2026-10-20｜PROPOSED_BUNDLE / PENDING_SINGLE_CPU_DATA_SCOPE_APPROVAL，非READY。**

用户要求“一次性多给一些任务”。本文件把八项相关工作合为一个父任务：
获一次整包授权、由用户在当前Codex会话触发后，连续完成可独立进行的子项，
统一提交一份父回执后停止。当前消息授权制定任务；**没有授权重新打开私人数据、
保留真实选项、写私人冻结记录或运行GPU**，因此本次规划不把026列READY。
用户明确批准下述A–H CPU数据范围后，由ChatGPT更新看板再触发执行；
普通“继续”不能替代尚未给出的新数据范围许可。不得自动启动027或真实GPU。

## 目标与研究位置

025已在[8342d4e](https://github.com/floomeer83felix-source/vlm/commit/8342d4e7a35e786106247895aeda2898ecf0a2cb)
交付公共接口，并在[4f2e373](https://github.com/floomeer83felix-source/vlm/commit/4f2e373d492816491df303041de0ac53817eb3e3)
验收。**本包补真实候选/输入交接和运行监督接入，不复跑025的30项测试、
023/024或任何旧QA。** 不再分拆盘点、parser、lock、scorer成多个微型父任务。

继续遵循[025冻结协议](../../research-protocols/temporal-distance-diagnostic-2026-10-20.md)，
包括原窄语法、48候选→12帧、C/D同两个锚点、四臂轮转与原分母规则。
本轮最多冻结4个候选源、每源1题，作为未来记录组隔离探索诊断的候选。
这不认证物理录制独立，不构成真实生成权限，亦不使真实QA任务READY。
[来源/结构审查](../../research-reviews/private-runner-structure-audit-2026-10-20.md)、
[nongold可行性审查](../../research-reviews/nongold-feasibility-audit-2026-10-20.md)和
[025接口限制](../VLM-TEMPORAL-EVIDENCE-ADAPTER-025/cpu-adapter-contract-receipt.md)
是本轮依据；不以旧预算或旧题数门代替新证据。

## 拟申请的一次性CPU数据范围

以下范围仅在用户明确批准整个026后成立：

- 只用现有私人Codex会话中用户已明确给出的017/018精确根目录，以及此前从授权源码
  恢复的两个精确入口（主dev标注、官方release-1 manifest）。不要求重复提供已知路径，
  不猜文件、不做目录扫描；缺失交接只记录缺少的引用类别，依赖项HOLD，其他安全项继续。
- 真实标注只流式读取来源/版本/时长/已知参与者分组、任务、题文、原始题序号、
  video UID一致性和候选成员关系。先做仅索引/结构的一遍，再做nongold screen的一遍；
  最多再对最终候选≤4题做一次inference投影，**只保留每题5个模型输入选项**。
  其他题的选项、全部正确答案、参考时间、canary和历史预测值始终词法跳过、不解码。
  遍历含gold的容器不等于只读取nongold字节；不复制原混合标注、不提前校验gold。
- 官方manifest仅保留必要的UID、来源/版本/时长、已知参与者/派生关系与声明文件大小/
  canonical版本字段。历史源排除只读此前已确知的精确manifest/roster入口中的
  UID、origin/participant分组、版本和已知派生关系字段；不得打开历史题文、选项、
  正确答案或预测正文。不能把旧源的不存在字段猜成空集合。
- 允许只读最多6份已确知的真实qualifier/runner/scorer源码，作文本/AST接入检查；
  不导入执行这些历史脚本。不得重新盘点整套模型/环境、读取权重或运行Torch/CUDA查询。
- 对候选媒体仅允许从既有精确授权引用或已核实的确定性本地映射取得路径并stat，
  不打开媒体正文、不probe/demux/decode/hash，不猜下载目录。未取得路径或文件缺失
  不转换为媒体下载授权。现时权利证据只复用已有明确记录；缺证据写UNKNOWN，不假称有效。
- 允许在 **`<AUTHORIZED_018_ROOT>/integration_026`** 创建唯一新的私人交付目录；
  这里的root是现有私聊已明确的018精确根，不是要求搜索。仅这个新子目录可写，
  原017/018所有文件和旧锁/账本保持只读。目录已存在、重解析链或身份冲突即停该写分支，
  不覆盖、不换后缀绕过。私人冻结manifest、题文/≤20个选项、摘要与worker接入代码
  只留在此目录，不入Git。授权创建本目录不授权其他私人文件写入。

### 固定CPU、读取与写入上限

| 项目 | 本包新上限 |
|---|---|
| 标注读取 | ≤3次open，每次文件≤4MiB；索引1/screen1/最终≤4题inference1，失败不重开 |
| 官方manifest | ≤1次open，文件≤8MiB |
| 精确历史源roster/manifest | ≤8个文件、各≤1MiB、各≤1次open；只投影上述分组字段 |
| 已确知历史源码 | ≤6个文件、各≤1MiB、各≤1次内容读取；AST-only |
| 全部研究输入正文 | 累计≤48MiB，含失败已消费读取；不靠重开重置 |
| 候选媒体stat | ≤4个确切本地媒体路径，正文0 |
| 私人新增交付 | 新目录内累计≤64个文件、总≤32MiB；不含任何媒体/权重/原混合gold容器 |
| 所有本包受控动态CPU子进程 | 每个≤120s；所有自有PID单调墙钟保守累计≤600s，嵌套计入、不退款 |
| 026新集成测试启动 | ≤2次；首轮失败后仅一次静态修订后的验证，025/历史测试启动0 |
| 测试fixture worker | 全部测试累计≤16次，每个≤5s；计入上述全包600s，只结束本包自己持有的child |
| 动态执行协调器 | 各受控执行窗口的协调器单调墙钟保守累计≤1200s；源码编辑/Git不属于窗口 |
| 禁止项 | 研究网络/下载0；真实gold值解码0；GPU/模型/训练0；安装/环境/权限配置变更0 |

每个受控窗口从启动协调器计到其自有child全部退出，不扣内部等待。
读取上限由唯一协调器记账，不拆脚本重新计数。无可靠自有子进程超时监督则动态项
NOT_RUN，继续静态交付；不扩大预算。普通Git协作不是研究下载或受控CPU时间。
除明确列出的≤4题选项外，不新增受保护数据范围；所有公开测试值必须人工虚构。

## 八项工作：一次触发，连续完成

| 子项 | 具体工作与交付证据 | 依赖/受阻处理 |
|---|---|---|
| A 精确交接与输入模式 | 安全同步公开文档checkout，读AGENTS/board/results/overview/本合同/025协议。核唯一READY=026、无已有026父结果。固定现有精确入口别名、代码版本和获准输入字段；用有界索引投影确认真实schema与原始索引，身份只留私人。 | 无入口不得扫描；记准确缺项，继续公共E/F/G及H的可完成部分。 |
| B 真实nongold筛选与来源排除 | 按025原语法逐题筛选，分别报实际总数、支持/不支持原因、旧源/相同origin/已知participant/已知派生排除数及未知项。对013/014/R1–R6做已知分组排除，不看历史表现或gold。 | 缺旧源映射、分组或权利证据时，把“文本候选”与“可执行候选”分开；不冒称独立/资格PASS，不恢复024的两源12题门。 |
| C 固定候选、选项与媒体成本 | 固定JSON原来源顺序和原始题序号；依序每源首个合格题、同origin/已知participant只取首源，最多4源各1题，不按选项/分数/结果挑选。screen资格先冻结再读取这≤4题的5选项；不合规选项记HOLD，不替换题。stat确切本地媒体，区分已有/缺失/未知；从已读manifest记录实际声明字节与版本。 | 少于4照实冻结；0或权利/映射不闭合则不得生成真实分母准确率，不开下载；来源证据未知者不能算“可执行合格N”。 |
| D 输入快照绑定与交接记录 | 建不可变私人manifest：候选键/原序号/来源分组、排除理由、nongold快照、版本、source order、四臂队列、每题选项状态、已知路径引用。对读流同一遍累计字节摘要+文件身份，留private，准备/评分约束同一可信输入。 | 不额外读取或复制混合gold原文件，不公示摘要/身份；stat前后相等只是辅助，不独立认证同一内容。真实scorer未来应在一次末期流结束后核对绑定，再发布结果；本轮不读真实gold。 |
| E 实际runner静态接入 | 以获准真实runner的AST为依据，在新私人目录生成接入副本/worker：nongold输入只来自冻结投影；025选帧/轮转原样接入；统一prompt、processor、decoder的原合同；选项不得进入事件分解/embedding输入，删除旧提前gold资格路径。列清实际符号映射、尚缺接入和风险。 | 不修改/运行旧runner，不导入模型。可做新接入代码AST/compile静态验证；缺精确源码则交付公共接口映射的未满足项，不能称真实接入完成。 |
| F 真实进程监督与持久防重试 | 新增stdlib supervisor：自己持有child句柄并wait/记录exit code；队列封闭后才交给独立CPU评分入口；原子排他锁、STARTED/TERMINAL及SCORING_CONSUMED持久化，失败/重启不退款重跑。generation只收nongold投影，不收原混合标注或gold opener。 | 本轮只启动虚构worker，不启动模型/scorer读真值。不得删除旧锁/杀别的job。worker代码与Python访问守卫不等于OS ACL：真实gold拒绝/权限隔离若未实证须单列UNKNOWN，不能用布尔receipt替代。 |
| G 026接入故障验证 | 仅测新数据接入/快照/进程监督链：真实nongold冻结可作CPU数据交接检查，但进程测试的题/选项/gold全虚构；验证child未退出零opener、own-child超时、持久锁跨进程拒绝重复、FAILED/NOT_RUN保留、输入绑定不符HOLD、评分失败仍消耗guard、旧STARTED不可重试。 | ≤2次新测试、≤16个fixture workers；不得重跑025 selector测试、历史模块或旧QA，不把fixture正确率写成真实效果。读真值0，真实生成0。 |
| H 一次总交付与真实执行提案 | 一份A–H状态回执、一份下一真实试点提案：填实际候选/可执行N、缺媒体数/声明字节、来源与权利缺口、真实接入/隔离状态，并据实际N列四臂≤16次Qwen的完整成本/边界提案。统一一个父结果、一份安全commit/push后STOP。 | 未知资源诚实UNKNOWN，不由历史预算“续用”或猜成本；没有实际证据就明确未具备真实READY条件，但仍交付本包已完成部分。不得自动另立资格/合成父任务。 |

### 来源、选帧与因果解释不得漂移

B/C用于未来 **RECORDED_GROUP_SEPARATION_ONLY /
PHYSICAL_RECORDING_INDEPENDENCE_UNKNOWN** 探索诊断。对已知旧来源组、已知参与者
与官方已知派生项执行排除；未知关系必须逐类说明，既不伪造严格物理独立，
也不以索取不存在的证书替代可操作的记录组核对。新研究口径的最终接受与真实研究
许可仍须在H所列实际证据和具体GPU/下载/评分范围上确认。

原JSON来源顺序与原题索引在任何新输出/选项观察前固定，C先冻结screen题键再读选项。
原窄语法无匹配时不放宽、不取别的任务标签补N。选项坏/媒体缺失不换题来改善结果；
区分筛选候选N与未来最终预先冻结N，所有变化/未满足项留痕，不假装已完成盲测。
不设新的真实结果驱动阈值/候选扩展，不回看旧gold/预测来调算法。

候选PTS/真实像素/实际visual tokens、event embedding、Qwen/processor运行与模型峰值
本轮均NOT_RUN；只能静态沿用合同，不能给ACTUAL_TOKEN_EQUAL或REAL_RUNNER_PASS。
48候选间隔粗、不认证事件实例/召回，CLOCK_ZERO_ASSUMED_NOT_CERTIFIED继续。
已见nongold的dev探索不叫完全未见题文预注册；小样本不支持显著性/泛化/创新宣称。

## 执行产物与准许修改范围（批准后）

公共执行交付最多以下六处，均不得带真实身份、题、选项、答案或私人路径/摘要：

1. `prototypes/temporal_pilot_prepare_026.py`：公共stdlib流投影/冻结/绑定接口，输入由调用者
   注入、无真实默认路径；复用025定义，不修改025。
2. `prototypes/temporal_pilot_supervisor_026.py`：公共stdlib监督/账本接口，无模型默认执行入口；
   真实worker/精确配置只能在新私人目录，真实操作仍受后续明确合同限制。
3. `prototypes/test_temporal_pilot_integration_026.py`：虚构进程/故障/绑定断言，不含真实样本。
4. `docs/codex-artifacts/VLM-REAL-PILOT-INTEGRATION-026/real-pilot-integration-receipt.md`：
   A–H各自PASS/PARTIAL/HOLD/NOT_RUN、真实候选汇总、失败/预算/残余限制。
5. `docs/codex-artifacts/VLM-REAL-PILOT-INTEGRATION-026/pilot-execution-proposal.md`：
   实际证据支持的未来执行范围、资源与待批准内容，不放行执行。
6. `docs/codex-results.md`：末尾仅一条 `### VLM-REAL-PILOT-INTEGRATION-026` 父结果。

私人新增目录只放本轮获准的冻结投影/精确输入引用/接入代码/本轮自有账本及fixture；
整份混合gold标注、真实gold、预测、媒体、权重不可拷入。所有新内容先检查脱敏再stage；
只提交上述allowlist，普通安全push一次，失败不静默重试，不动PR #1。
本README、025代码/协议、AGENTS、board/overview与历史结果都不是执行者可改路径。

## 继续规则、验收与停止

- 数据阶段有缺口，不意味着可隐瞒或猜输入；写HOLD后继续不依赖它的E/F/G/H部分。
  预算/隐私/环境守卫异常则停止对应动态分支；不为“做满八项”绕过权限。
- 本包不要求所有前置项PASS才允许做其余安全工作，也不把真实数据未知门整体提前终止。
  但未完成真实候选/实际runner映射时不能给整包REAL_INTEGRATION_PASS。
- 分别报告 DATA_HANDOFF、COHORT_SCREEN、SOURCE_GROUP_SCREEN、SNAPSHOT_BINDING、
  RUNNER_STATIC_INTEGRATION、SUPERVISOR_PROCESS_TESTS、REAL_PILOT_READINESS；
  最后一项本轮只能PREPARED_PROPOSAL或HOLD，不能把CPU完成冒称真实QA已跑。
- 026结束后STOP；025/024不重开。旧GPU、下载、gold额度一律不继承。
  CPU准备许可即便批准也不放行GPU、模型导入/推理/训练、媒体正文、研究网络或真实gold。

**本次只是八项任务规划，不创建空回执/结果，也不访问任何私人输入。
REAL_QA_EFFECT_UNKNOWN；NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；
Charades FINAL_MEDIA_STOP；TRAIN-GPU HOLD。**

## 一次性待批准授权文本

批准026 A–H一次性CPU整包：仅按上述精确入口与48MiB累计读取上限读取nongold数据、
≤4题各5个选项和旧源分组字段；允许在已知018根的唯一integration_026新目录写私有
冻结/接入记录，执行限额stdlib进程验证，完成可独立子项后一并提交停止。
不授权真实gold值、媒体正文、研究下载、模型/GPU、训练或环境/权限配置变更。
