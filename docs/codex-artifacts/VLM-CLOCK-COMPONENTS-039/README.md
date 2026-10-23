# VLM-CLOCK-COMPONENTS-039：读出、间隔与输入呈现分量判别

2026-10-23（北京时间）。ChatGPT研究负责人；本地Windows Codex执行。
**唯一READY / PUBLIC_COMPONENT_PROBE_IMPLEMENTATION_ONLY，尚未执行。**
本README第6节用户实际发送的完整消息才激活本轮私人配置/自有合成/条件GPU范围。
GitHub编辑不唤醒Codex；038已交付关闭，不恢复其run或余额。
冻结科学源：[039分量对照协议](../../research-protocols/clock-binding-component-contrast-2026-10-23.md)；
来源：[038科学结果](../VLM-CLOCK-BINDING-PROBE-038/scientific-results.md)。

## 0. 这一包的科研目的

038终于观测到实际差距：视频间隔3/24，对应文字算术22/24，且实际输入门通过。
还不能区分读出/角色绑定/计算及呈现。039只做一轮能拆开这些解释的行为对照，
不重复旧准确率工程、不训练，不把数字叠字/跨任务一致性冒称新算法。

新几何4基础组×颜色互换=8依赖world、3clock、5独立任务，共120槽：
NG/NR原生视频间隔/时刻读出，SG/SR带时间码拼图间隔/时刻读出，OG文字算术。
48原生video、48image、24纯text；每个task/clock planned=8。
拼图与video均324视觉tokens是**待实际CPU验证**，不是同tensor/总token/FLOPs公平性证明。
新位置组合是探索性判别，不是独立自然来源或确认性holdout。
最多LOCAL_DIAGNOSTIC_ONLY；NOVELTY=RETAIN0，自然长视频效应仍UNKNOWN。

## 1. 同一父任务A–H

| 项 | 工作 | 准入与交付 |
|---|---|---|
| A | 安全同步独立文档main，重读AGENTS/board/results/overview、本合同/039科学协议和038两报告 | 039唯一未交付READY；记录本轮父时钟起点，不继承旧授权 |
| B | 两个新小模块，实现自有新world/位图拼图/固定120队列，最小复用已跑通的监督与绑定逻辑 | 新root/持久锁/hash-chain账本，角色隔离、Job退出和资源上限不弱化 |
| C | 新stdlib suite≤2×60s | 核新truth、正负clock差、角色互换、字体/像素界、120队列、严格解析及闭合/输入绑定拒绝有效反例；不跑旧suite |
| D | 实际CPU processor暴露≤2×90s | 检验科学协议第6节的全部120输入、native clocks/video和image grid/token/最终dtype；仅一次有源码依据API兼容修复 |
| E | D全部通过后一次query，单worker一次Qwen加载/120槽各一次 | GPU包络600s、无warmup/额外forward/重启/重答；不按成绩改科学常量 |
| F | 全模型实际退出、队列闭合与逐槽绑定后，独立CPU一次程序truth计分≤30s | 消费one-use scorer guard；原annotation/gold0open；未执行保留UNKNOWN |
| G | 完整120结果/15格主表、读出/角色/间隔及C/P配对、时钟关系和依赖组分布 | 区分联合正确/仅关系满足；正对照失败与普通混杂保留；无机制/新颖性升级 |
| H | 五处allowlist统一脱敏交付，一次普通安全push main后STOP | 不自动040、改prompt/font继续搜失败、加模型、恢复真实QA或训练 |

可只读复用038的纯函数/child policy/签名、030的Win32 Job/command/锁纯监督帮助、
既有resource XML parser。038视觉分区只有video keys，本轮须在新代码里正确支持image keys。
新positions/render/input/spec/queue由039自己定义；不调用038 init/coordinator/gpu/score，
不改旧模块全局量，不整套复制历史大型pilot，不实例化旧Journal/运行旧测试。
不能在本包可靠实现则HOLD并报告，不能改科学规范凑出运行。

## 2. 最小配置交接与隔离

在既知018隔离根内、与integration_038同级创建唯一新integration_039。
任何同名root/锁/039旧执行记录存在即STOP；不删锁/改epoch/自动续跑。
父时钟从本轮实际开始、含同步/实现/修复/等待/children/cleanup起计≤1800s，
不得另起协调器重置；可在已有公开交付中只读定位这一确切父根，不扫描磁盘。

**创建首个私人输出前**，在已知目标卷一次检查可用空间，
必须满足64MiB完整输出配额之外另有≥2GiB余量，精确free/required/时点随后写入本轮收据。
038漏了该前置检查，事后磁盘数值不能补证；本轮把检查嵌入科学run，不另开修复父任务。
输出无reparse，输入张量在内存逐槽构造/释放，不复制模型/媒体；
可保存≤1张本轮自有PNG预览用于像素QA，计入96文件/64MiB，不调字形。

只读integration_038这四个确切文件，各至多1次外部正文open：
- runtime/config.json（≤1MiB）：只取已经使用的Qwen root、runtime python/site/path、device reference/token IDs。
- runtime/external-reads.json（≤1MiB）：只核038的两份Qwen config已有SHA/大小，不继承其数据权限。
- 038-ledger.jsonl（≤2MiB）：只读核hash chain、REAL_038、48唯一STARTED/终态、真实model exit/queue close/STOP。
- runtime/final-summary.json（≤1MiB）：核038实际退出/Job0和关闭状态，不当作本轮资源准入。

038模型响应可在已允许的关闭账本中遇见，仅作闭合核验；
不得据其重排/筛题/换新world。无须另开038 score/results.json、exposure/tensors或原始trace。
更早036/035 roots、真实数据/旧helper/frames等0open。
这些handoff只承接已成功本机执行配置与最小关闭证据，绝不恢复038。

额外research文本只限：
- 同一Qwen root的config.json、preprocessor_config.json，各≤1MiB、各一次，
  与038已记录SHA相符；如变更则HOLD，不另挑模型。只取本轮必需video/image token等配置。
- 至多4个确切已安装runtime源码，各≤1MiB、各一次：
  processing_qwen3_vl.py、video_processing_qwen3_vl.py、video_utils.py，
  以及**实际image processor类的唯一源文件**（由该类已加载module.__file__确定，无目录扫描）。
  只为实际输入API/形状核验；不批量读包。

research文本最坏5+2+4=11MiB，总≤12MiB。记录size/stat/SHA及用途；
正常既有runtime/tokenizer/processor资产的local-only加载按角色记录，
不假称这些常规runtime I/O字节都已计量。
CPU阶段Qwen权重0、无forward/CUDA初始化；只有D全过后的E允许唯一既有Qwen权重读取。
无SigLIP、新模型、Hub下载或新依赖。路径缺失/配置不符则HOLD，不扩路径搜索。
普通Git协作网络允许；实验进程network/download均0。

模型只见本轮自有RGB/原生时间码或规定拼图/模板；
自己的程序truth与score目录不向模型worker开放。
程序源码含公开合成规范不等于原真实标注获准打开；
本轮不对旧原标注handle/probe、真实媒体时钟或跨来源独立性签PASS。

## 3. 冻结执行、资源与终止

代码/spec/queue/config及实际CPU输入receipt在E前冻结，E起不得再改实现或科学条件。
独立每槽messages，不读前槽reply为输入；每槽一次STARTED预扣后调用，
STARTED即消费，返回格式错误不重答。

| 项 | 本轮硬上限 |
|---|---|
| CPU | 累计480s，初始化/本轮小suite/CPU input gate/query/scorer/cleanup均计入；预约建议60+120+180+10+30+30=430s |
| 父 | 1800s，包括实现、修复、等待、所有children和清理；不按新run重置 |
| 新suite/input gate | suite≤2×60s；真实input gate≤2×90s；第二次仅一次有确切源码依据的API兼容修复，科学常量不变 |
| GPU/model | 一个worker/一次load，完整监督Job≤600s含load/build/hash/120调用/cleanup；最多120 generate，各槽≤1 |
| 生成 | Qwen3-VL-4B，BF16/SDPA，eval/inference_mode，seed19，batch1，greedy，max_new_tokens16，input≤2048 |
| 设备 | 一次nvidia-smi≤10s核同3090/index/UUID/bus与free≥20GiB；worker权重前一次torch free≥20GiB；util/context只记录 |
| 显存/RAM | load前18GiB allocator约束，peak allocated≤18GiB，Job committed RAM≤24GiB |
| 私有输出 | integration_039≤96文件/64MiB，无reparse；启动前输出配额外≥2GiB磁盘余量 |
| 外部research文本 | 上述4 handoff/2 config/至多4源文件，总≤12MiB；正常runtime/processor/条件权重按角色加载 |
| 真研究数据及系统修改 | 原标注/QA/gold/旧frames/manifest/预测/source map/private helper、媒体/MP4/decode、训练、安装、永久环境/ACL/profile/凭据修改均0 |

资源采用有界共享，不要求空机器；不重query/等待降util/kill peer。
free不足、worker失败、OOM/timeout立即结束模型阶段；
所有已调用槽保留真实终态，剩余NOT_RUN，不重启模型或另开run补齐。
未运行/预算上限不能冒充实际测量。timeout须等监督Job/PID实际退出，不能靠标志文件假定退出。
一旦发生model阶段故障，不用剩余预算作其他forward。

只有全部120槽有可审终态（含NOT_RUN）且所有model PID/Job实际active0，
STARTED唯一、输入绑定/code/spec/queue/config对齐后才一次独立CPU评分。
one-use guard在读取程序truth前消费，失败不重开scorer/手工代填；原gold不参与。
若完整输入绑定未建立或退出不明，计分HOLD，可公开已合法取得的状态/合成回答，
不补造完整准确率；失败的对照不删除。

## 4. 报告与科研结案

component-input-and-run-receipt.md记录：handoff、API/source依据、CPU实际gate、
video/image真实grid与tokens、两类视觉绑定、完整生成数/退出/EOS/截断、
每阶段实际/预约成本/峰值/输出配额、磁盘**前置**证据和所有实施缺口。
scientific-results.md记录科学协议第7–8节全部项目，
至少全120状态/解析值、15格task×clock主表、三种gap配对、读出角色正确/互换/off-grid、
C/P全24格及基础组/颜色分布、clock局部响应和+60平移正确/仅关系一致/未知。
全部为自己的小型合成结果，可公开规范化数值；不公开私人路径/UID/device IDs/
权重hash/完整trace、真实QA或自然媒体。

不合并038/039为独立n，不按OG正确筛主表；
读出正确不证明另一prompt内部状态正确，拼图成功不定位原生神经模块。
NumPro式数值可视化和时序任务一致性均有先例；
本轮最多LOCAL_DIAGNOSTIC_ONLY，不报新benchmark/新机制/自然长域优势。
一次分量轮结束，不按有利成绩自动040/变font/调prompt/扩样；
仍混杂普通解释则建议停止合成变体投入，由研究负责人另行判断科学方向。
旧C/D NO_GO_AS_CORE、NOVELTY=RETAIN0、TRAIN-GPU HOLD、
历史CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP不变。

## 5. 公共allowlist（恰五处）

1. prototypes/clock_binding_components_039.py：小型独立新刺激/spec/input/单worker监督/score。
2. prototypes/test_clock_binding_components_039.py：本轮新stdlib组合见证；ML只在实际children加载。
3. docs/codex-artifacts/VLM-CLOCK-COMPONENTS-039/component-input-and-run-receipt.md。
4. docs/codex-artifacts/VLM-CLOCK-COMPONENTS-039/scientific-results.md。
5. docs/codex-results.md末尾恰一个039父结果。

Codex不改本README、科学协议、ChatGPT规划、旧源码/tests/报告或历史日志。
交付前核stage路径与脱敏，一次普通安全push main后STOP；
push失败按AGENTS保留本地并回报，不静默重试、rebase/reset/force。
任务为一个父包，无额外作者联络、Issue、后台监听或自动下一轮。

## 6. 用户完整启动消息

以下整段作为一条新消息发送给当前本地Codex；
如既有聊天已满可按AGENTS做GitHub-first交接，不继承任何旧run权限。

```text
安全同步独立GitHub文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md，以及VLM-CLOCK-COMPONENTS-039 README和clock-binding-component-contrast-2026-10-23科学协议。确认039是唯一尚未交付的READY父任务，按A–H同一包执行。

我明确授权本轮全新自有合成分量对照：只读合同指定的038四个确切配置/关闭收据文件、2个Qwen配置和至多4个确切已安装runtime源码，research文本总≤12MiB；只在既知隔离位置新建integration_039，≤96文件/64MiB，启动前检查并记录输出配额之外≥2GiB磁盘余量，不恢复038或其他旧run/余额。

固定四种新位置组合×两种颜色顺序×三clock×五任务，共120个全新槽：NG/NR原生视频间隔/有序时刻读出，SG/SR带时间码拼图间隔/读出，OG文字算术。科学协议中的像素、字体、prompt、解析和轮转队列均不变。先真实CPU验证原生六timecodes、最终BF16输入绑定、视频[6,12,18]及拼图[1,24,54]均324视觉tokens、OG无视觉；未全过则Qwen权重/GPU/generate0，不手改token或改科学条件绕门。

CPU累计≤480s、父任务≤1800s（含实现/等待/cleanup），新suite≤2×60s、实际输入预检≤2×90s，仅准一次有确切源码依据的API兼容修复。过门后允许既有Qwen3-VL-4B BF16/SDPA/local-only单worker、一次加载，GPU完整包络≤600s、总generate≤120、每槽≤1、max_new_tokens16、greedy、seed19、fresh context。一次当前query和worker权重前free复核均≥20GiB，allocated≤18GiB、Job RAM≤24GiB，util仅记录；不重query、不重启、不重答、不额外forward/warmup、不kill peer，OOM/timeout保留余槽NOT_RUN。

全部模型Job/PID实际退出、120槽闭合及输入/code/spec/queue/config绑定后，一次独立CPU从本轮程序真值计分。保留全部任务/clock分母、角色读出/直接间隔的配对差异及未知；拼图改善只解释为呈现敏感行为，不上调机制或创新结论。

原真实标注/QA/gold、旧frames/预测/manifest/source map/私有helper均0open；实验网络/下载/MP4/解码、训练、安装、永久环境/ACL/profile/凭据修改0。只按五处allowlist交付两个新模块、两报告和codex-results一个039父追加，一次普通安全push main后STOP，不自动040/扩样/训练。旧C/D不恢复，NOVELTY仍RETAIN0。
```
