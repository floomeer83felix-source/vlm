# VLM-CLOCK-BINDING-PROBE-038：输入可识别性先行的时间码绑定诊断

2026-10-22（北京时间）。ChatGPT研究负责人；本机Windows Codex执行。
**唯一READY / PUBLIC_PROBE_IMPLEMENTATION_ONLY，尚未执行。**
本README第6节用户实际发送的一条完整消息激活新私人配置/自有合成输入/条件GPU范围。
本合同与最新board明确取代037处置时“重设计期间0 READY”的历史状态，原C/D停投裁决不变。
这不是恢复036/037或原C/D实验；新问题及全部科学常量在
[研究协议](../../research-protocols/clock-visual-binding-probe-2026-10-22.md)冻结。

## 0. 价值与边界

只有一个目标：在可验证呈现的同像素输入中，检验时间码改变是否按任务规律影响答案；
三合法clock条件与逐条件文字算术control区分输入构造问题、算术控制失败和视觉—时间结合链的行为缺口。
没有宣称找到新算法/神经机制；NOVELTY=RETAIN0。
先CPU真实核输入；未识别干预则Qwen权重/GPU/generate0。
真实短合成模型结果也不等于自然长视频或论文贡献。

科学源文件明确8 world×3 clocks×2 channels=48槽。
12个192×288自有RGB帧、6个原生temporal块、24 V/24 O，
4种基础位置组×颜色互换为依赖重复，不报8独立来源/显著性。
原真实标注、frames、QA/gold、manifest/历史预测全部0open；
无需找到旧标注，也不能借本任务访问它们或签原文件隔离证明。

## 1. A–H同一父任务完成

| 项 | 工作与准入 | 交付事实 |
|---|---|---|
| A | 安全同步独立文档main，重读AGENTS、board/results/overview、本README/科学协议/037正式处置；确认038唯一未交付READY与用户完整新scope | 不依旧chat/旧授权/余额；无后台自动续跑 |
| B | 公共实现两个新小模块；只复用必要纯监督/只读policy函数，不改旧030/031等模块；stdio握手、一次新run/锁、48唯一槽、防重复、真实Job退出与资源上限 | 不机械重命名125k旧pilot/复制整套工程。无法以小实现可靠监督就HOLD，不弱化门 |
| C | 新suite最多2×60s，验证本轮数值真值/同像素/clock映射/48队列/终态及计分门的有效反例 | 只新tests，无旧suite/重复OS演示；不是模型效应或创新证明 |
| D | 新root中原生CPU processor输入暴露检验≤2×90s；只在实际API兼容失败且有确切源码依据时用第二次，最多一次局部兼容修复并用剩余新suite验证 | 每个V输入六timecodes正确、视觉tensor不随clock变、原生grid/324 tokens正确；缺一HOLD_INPUT、GPU0 |
| E | D全过后一次当前query/free门；单GPU worker加载已有Qwen3-VL-4B BF16/SDPA/local-only，48冻结槽各一次，600s总GPU包络 | 不重启模型、不重答、不根据已知成绩调prompt/marker/clock/条件；OOM/timeout结束并保留未执行 |
| F | 全48终态、唯一model PID/Job实测退出、queue/spec/code/model-config/实际输入绑定后，独立CPU一次从冻结程序spec计分 | 不用原annotation/scorer；不调用LLM judge，不把未执行记成模型答错 |
| G | 分开报告输入识别、V/O行为、clock响应/平移联合正确与仅关系一致、所有实施失败/未知；按协议固定解释 | 最多DEVELOPMENT_PROBE_OBSERVED，不能上调新颖性或自动扩样/训练 |
| H | 五处allowlist统一交付，一次普通安全push main后STOP | 不自动039、下载/原数据修复或新研究队列 |

如实现前已取得直接同因子设计的原始先例，报告DIRECT_DUPLICATE并关闭，不为完成GPU计数继续；
不再发广综述/多候选toy包。本任务无需另读数据集或外部联系。

## 2. 最小配置交接与本机权限

已知018隔离根下创建唯一全新integration_038；存在同名root/锁或旧038记录即STOP，
不删锁/改epoch，不实例化任何旧Journal。
父时钟≤1800s，所有CPU/GPU/等待/cleanup计入，不另起run重置。

只读integration_036中下列5个确切文件各≤1外部open：
- synthetic-startup-config.json（≤1MiB）：只取既有Qwen root、处理器配置参考；忽略SigLIP root与旧system/虚构题。
- runtime.json（≤1MiB）：只取原pytorch环境确切解释器/site/既有runtime，不枚举conda/盘符/环境。
- device-identity-reference.json（≤1MiB）：预期query device/3090 UUID/bus，仅私人绑定。
- startup-policy-3.json（≤1MiB）：仅承接已定位null-device/bytes路径兼容经验，不承接私人data权限或旧run准入。
- 036-ledger.jsonl（≤2MiB）：只读核hash chain、REAL_036/STOP、三bootstrap及无真实model/gold事实；不恢复旧epoch。
记录本轮读取size/stat/SHA；缺历史file-SHA不补造。036/private helper、frames、真实问题/标注reference、
原manifest/heads/候选/旧预测或任何更早root均不读。

至多2份Qwen确切config各≤1MiB（非权重）；至多3个有实际接口/异常依据的已安装确切模块各≤1MiB，
限processing_qwen3_vl.py、video_processing_qwen3_vl.py、video_utils.py。
总research文本≤12MiB（handoff最坏6＋config2＋source3=11MiB）。
正常既有runtime/CPU tokenizer/processor资产和**条件GPU时唯一Qwen模型权重**的local-only加载
另按执行角色记录，不能复制/下载/公开模型。CPU阶段模型权重0。
未找到确切Qwen root或runtime则HOLD，不扫描模型/个人目录。
普通Git协作网络允许；实验进程network、远端Hub/数据/模型/包下载0。

模型只接收本轮自有RGB/时间码/模板，不把world/clock/channel名称、gold/expected字段、
路径/文件名/清单/种子解释或旧研究信息放入模型可见prompt。
可以按固定科学spec创建程序真值，**不是新增人工真实证据标签**。
CPU资产/score与worker输入输出分目录；模型进程不读gold/score目录，
不声称能够阻止全机所有副本或恶意代码。真实原标注handle/probes为0且不签通过。

## 3. 新CPU输入门与固定生成

- 根下只生成协议的12帧数组，不保存/解码/生成MP4，不读任何旧帧；
  颜色位置、时钟G0/G1/G2、模板、truth、48槽、左旋执行顺序在模型加载前全部冻结。
- 原生AutoProcessor/VideoMetadata，do_sample_frames=False；
  192×288保持实际grid=[6,12,18]、324 video tokens；fps显式1，不接受默认24/自动重采样。
  以确切已安装源码决定已有API参数/metadata结构，不能安装新版本或照upstream猜参数。
- 实际CPU逐个构造24 V与24 O，及时释放临时tensor，不积攒48份完整tensor。
  V同world三clock原始RGB及视觉tensor全同、6个时间码逐一等于协议值；
  问题stem相同，时间码变化确实进入input_ids，相关长度/attention可随数字改变。
  O必须无visual tokens、操作数与对应clock一致。Torch CUDA初始化始终False。
- 记录实际本机处理器版本/确切source摘要、model/tokenizer/config/模板/spec/queue摘要，
  原始RGB、视觉部分、文本部分及完整模型输入的类型/shape/内容绑定；
  不只比较pair/indices、token数量或缺失的None值。
  worker重构的输入必须与CPU预冻结绑定匹配；最终dtype/转换约定明确。
- 不手改已生成input_ids或插假时间码补救原生暴露失败，不改变色块/任务/时间表让测试好看。
  第一失败仅有确切API兼容依据才用一次剩余修复，不能修改科学变量；
  第二次失败结束，无第三次新suite/CPU预检、额外startup演示或环境修复。

GPUworker仅一个，完整包络≤600s，包含加载/构造/哈希/全部调用/清理；
每槽STARTED先消费后generate，generate总≤48，任一已STARTED不再答；
RETURNED/INVALID/FAILED/NOT_RUN单独终态，实际return坏格式不重答。
固定Qwen3-VL-4B、BF16、SDPA、eval/inference_mode、seed19、do_sample=False、
max_new_tokens=16，batch size1，不开CoT/采样/beam/新模型或SigLIP；
没有额外warmup/模型探测forward或generate，48槽之外不做模型推理。
每槽独立新messages，不加入前槽回复或跨槽共享past_key_values/聊天历史；单次完整输入≤2048 tokens。
所有模型回答前后不得改科学配置/队列/生产代码；非确定性/实现疑点如实记录，不补测。

资源采用显存有界共享政策：
一次nvidia-smi≤10s核同3090/index0/UUID/bus、free≥20GiB，util/context仅记录；
该worker权重前一次torch free复核，load前allocator fraction18GiB、peak allocated≤18GiB，
Job RAM≤24GiB。无重query/等待低负载/kill peer。无CUDA/资源条件则NOT_RUN，不绕门。

## 4. 计分、资源及报告口径

模型完全退出后一次CPU scorer≤30s，只读本轮frozen程序truth和返回，不读原gold。
先消费score guard；部分失败/guard失败不重开评分，不手工代填。
核全部48槽/spec/queue/code/模型配置/输入receipt、STARTED与真实退出。
保留planned每condition=8/总48及四类终态，主配对统计附未知数量；
未执行不写成已观测错误，不筛“容易定位/算术正确”子集作主成绩。
O/V分层是事前控制，不是因输出挑样本。

| 新资源 | 上限 |
|---|---|
| CPU | 累计≤480s；初始化30＋新suite2×60＋真实输入预检2×90＋query10＋scorer30＋收尾30=400s预约建议，其余计入余量 |
| 父 | ≤1800s，包括编辑修复等待/全部children/cleanup，旧时间不迁移 |
| GPU/model | 单worker≤600s，Qwen加载一次，48 generate总量、每槽≤1，≤16新tokens/调用；不重启/重答 |
| RAM/device | Job≤24GiB RAM，allocated≤18GiB，free≥20GiB准入，单设备/不干预peer |
| 私有输出 | integration_038≤96文件/64MiB、无reparse；输入张量主要在内存，不复制权重/媒体；精确预约另留2GiB磁盘余量 |
| 输入 | 5确切handoff、2 config、3确切runtime source，总≤12MiB；normal本地runtime/processor/条件Qwen资产分角色记录，不作为研究数据打开 |
| 外部真实研究数据/训练 | 标注/QA/gold/frames/manifest/source map/历史预测/下载/解码/训练/安装/永久环境或ACL/profile/凭据修改均0 |

报告必须包含：接口实际暴露PASS/HOLD、24 V与24 O每clock状态，
同像素和实际时间码见证、时钟响应/平移的联合正确与错误一致、
配对V/O及可/不可识别归因、4基础位置组/8依赖world、所有成本/异常/退出。
若进程未运行，不用预算上限冒充测量；无真正model return不生成性能表。
原程序化帧/时间表/整数结果可以公开以复核；私人路径、UID、硬件标识、权重hash和完整trace不公开。

按协议的四种结果解释，最多DEVELOPMENT_PROBE_OBSERVED；
没有自然长视频/独立来源/跨模型的实证，不报论文新机制/显著性或正式benchmark成绩。
原C/D保持NO_GO_AS_CORE；NOVELTY=RETAIN0、TRAIN-GPU HOLD、
CLOCK_ZERO_ASSUMED_NOT_CERTIFIED（原真实媒体历史）、Charades FINAL_MEDIA_STOP。
本轮自有源时间可解析定义，不能替旧真实视频认证时钟。

## 5. 公共allowlist（五处）

1. prototypes/clock_binding_probe_038.py：小型独立生成/spec/输入核验/单worker监督/score；
   旧模块只读复用必要纯函数，不机械搬整套历史pilot。
2. prototypes/test_clock_binding_probe_038.py：新纯CPU/stdlib组合见证，ML只在实际预检/worker内import。
3. docs/codex-artifacts/VLM-CLOCK-BINDING-PROBE-038/input-exposure-and-run-receipt.md。
4. docs/codex-artifacts/VLM-CLOCK-BINDING-PROBE-038/scientific-results.md。
5. docs/codex-results.md：末尾恰一个038父结果。

旧生产源码/科学协议/任务README/规划/旧tests或报告不改；不创建空真实QA回执。
仅一次普通安全push main后STOP，不自动039/扩刺激/加模型/训练。
push失败按AGENTS保留本地并回报，不静默重试。

## 6. 用户一次完整启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS、board/results/overview、
> VLM-CLOCK-BINDING-PROBE-038 README及时间码—视觉绑定科学协议，
> 确认038唯一未交付READY，按合同A–H一次完成。
> 我明确授权本轮全新自有合成诊断：只读合同5个036确切配置/关闭账本，
> 2个Qwen配置和至多3个确切runtime源码，总research文本≤12MiB；
> 新integration_038≤96文件/64MiB，不恢复旧run或余额。
> 使用协议固定8 world×3 clocks×2 channels共48槽，
> 12个192×288自有RGB帧，先真实CPU核原生timecodes/同像素/视觉tensor/grid/324 tokens，
> CPU≤480s/父≤1800s、新suite≤2×60s、输入预检≤2×90s，仅一次有源码依据的API兼容修复。
> CPU输入门未过，Qwen权重/GPU/generate0；不手改token或变更科学条件绕过。
> 过门后允许已有Qwen3-VL-4B BF16/SDPA/local-only单worker、一次加载，
> GPU总≤600s、最多48次全新generate、各槽≤1/max_new_tokens16/greedy/seed19。
> 一次当前query/free≥20GiB，allocated≤18GiB/Job RAM≤24GiB，util仅记录；
> 不重query、不重启或重答、不kill peer，OOM/timeout立即保留余槽未执行。
> 全模型Job/PID退出和48槽闭合后，一次CPU从本轮程序truth计分，
> 不用原annotation/真实QA/gold、旧frames/预测/manifest/source map或私有helper。
> 网络/下载/MP4/解码、训练、安装、永久环境/ACL/profile/凭据修改0；
> 旧C/D不恢复，结果最多开发探针现象，NOVELTY仍RETAIN0。
> 按五处allowlist交付代码、两报告和results一条父记录，
> 一次安全push main后STOP，不自动039或扩样/训练。
