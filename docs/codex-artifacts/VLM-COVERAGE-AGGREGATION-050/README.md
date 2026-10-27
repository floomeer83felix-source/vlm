# 050：同一48候选的联合读出与分组读出机会实验

2026-10-27（北京时间）｜ChatGPT研究负责人；本地Windows Codex执行。  
父任务：**VLM-COVERAGE-AGGREGATION-050**。  
**唯一READY / AWAIT_EXPLICIT_START，尚未执行。**

依据：[立项说明](../../research-decisions/post-049-coverage-aggregation-direction-2026-10-27.md)、[049已完成验收](../../research-decisions/post-049-selection-channel-disposition-2026-10-27.md)。049坐标通道候选保持停止；本包是新RGB覆盖/读出程序比较，不重跑049，不为它增加坐标/提示变体。

## 1. 一次完整研究包的目的

固定049同24题和四源48帧缓存，回答：一次看完48候选、或四个互补12帧视图固定投票，是否明显超过现有Top12结果？这是科学机会核验，使用已有基线，不宣称新算法。

执行一次包括精确旧结果绑定、必要CPU验证、五个新输入条件、独立评分、成本与继续/停止建议。输入缺项先在本地一次列齐并等待，不找路径、下载、恢复回收站或创建空HOLD父结果。实际开始内容绑定后建立新050根及父时钟；失败统一交付一次并消费本父，不另起编号修补。

第8节完整消息实际由用户发送后，才激活本轮具体私有读取/模型范围。只有旧“继续”或GitHub READY不能加载模型。

## 2. 复用已明确的049输入，不再准备媒体

只使用当前本地聊天已明确的049准确根及其已登记模型/原标签入口。若当前根丢失上下文，一次索取精确路径，不枚举目录。允许读取：

- 049的runtime-config.json、coordinator-config.json、source-selection.json、nongold-projected.json、selected-source-private.json、preparation-seal.json、input-queue-seal.json、inference-complete.json、infer-phase.json、score-private.json、independent-review.json、legacy-identity-index.json、049-call-ledger.jsonl。
- source-selection中四个安全basename别名所对应的*-cache-receipt.json及*-candidates.npy；仅这些四个规范化数组，不跟随原媒体路径。
- predictions-current-private.json中的已关闭自然条件UO/UR/SO/SR对应记录。先按input-queue-seal精确找到身份；只取这些规范A–E输出和完成元数据，不输出/消费灰色条件作为新方法。不打开017/018旧预测、旧gold产物或其他run。
- 当前公共049两源码作只读API/哈希参考，以及当前精确Qwen/processor/tokenizer目录和已验证解释器/监督入口。正常本地库/模型文件加载允许；不把其目录当研究搜索根。
- 原annotation准确入口仅供两个隔离CPU角色：模型前一次nongold投影核对同24题，词法跳过gold值；全部模型进程实际退出后，scorer再打开一次≤4MiB读取同24题原标签。两次均与049冻结SHA一致；模型worker不接收这个路径/UID。不得声称包含gold的原文件物理零读取。

元数据/索引/规范预测合计≤32MiB；四数组总payload≤64MiB，必须各为uint8[48,192,288,3]，与049缓存内容身份/原顺序一致。输入文件普通且无链接/reparse祖先。混合JSON被打开时如实登记，不以只解析部分字段宣称文件零读取。

模型前原nongold投影必须核对完整question/五选项。允许的原选项schema仅三种：options五元素列表、options键恰为A–E的字典、或原条目A–E五个独立非空字符串字段，统一按A–E顺序；若多种同时存在须完全一致。question必须在原条目存在且为字符串。缺字段/冲突/其他schema记INPUT_BINDING_UNKNOWN，不用旧nongold回填。可复用049纯词法投影函数并显式请求这些nongold字段，gold解码0；这一步在加载任何权重前完成。

冻结**完全相同的24题、四源各6题、原顺序/五选项**；不再筛时间词、不挑049错题、不剔除难题、不替补来源。先验证049完整完成、240逻辑格/216返回、自然条件有效、所有输入/代码/nongold绑定可核。049原目录与文件只读；新根用用户指定的准确位置（可为同父目录vlm-private-050），存在或有歧义则等待，不覆盖旧产物。

旧输入完整身份或关闭结果不可靠就报告INPUT_BINDING_UNKNOWN；不通过新配置/提示标记绕过已STARTED禁止重放，不重做049修复/解码/标注恢复。049的全球历史exactly-once证书缺口仍披露，不把本050的局部索引说成完整历史认证。

## 3. 固定程序、输入与投票

每源候选槽0…47，统一ordinal载体fps=1、total=48、duration=48；不是原片真实秒数。保持049原RGB、192×288、原生processor、do_sample_frames=False/do_resize=False，不再插值、裁剪、叠字或伪造时间token。

| 条件 | 送入的候选槽 | 每题模型调用 | 预期视觉grid/tokens |
|---|---|---:|---|
| F48 | 0,1,…,47全部 | 1 | [24,12,18] /1296 |
| P0 | 0,4,8,…,44 | 1 | [6,12,18] /324 |
| P1 | 1,5,9,…,45 | 1 | [6,12,18] /324 |
| P2 | 2,6,10,…,46 | 1 | [6,12,18] /324 |
| P3 | 3,7,11,…,47 | 1 | [6,12,18] /324 |
| V4 | 对P0–P3四个输出作固定投票 | 0 | 汇总4×324=1296 |
| SO/UO/SR | 049已关闭的同题自然条件 | 0新增 | 只读原结果 |

四个P视图两两不交、并集恰为48候选，各按槽序送入；F48与四P程序使用相同像素集合。所有视频的原生frames_indices均用对应真实候选槽号，不重置为每视图0…11。用实际processor暴露完整kwargs、原生callback/时码、grid/token/长度和最终BF16输入封存验证，不只看外部列表。

六个P时码独立预期为`j+2+8m,m=0…5`；F48的24个为`0.5+2m,m=0…23`。只核原生输出，不把手写时码回灌给模型。

V4使用**plurality（最高票）**：只给严格有效A–E输出投票；同票时选在P0→P3中最早出现的并列最高票答案；全无有效票为INVALID。固定规则不读gold/置信度/题型，不加入文本裁判或第六次推理。公开平票数、有效票分布和全无有效票数；INVALID仍保留原24分母。若存在FAILED/NOT_RUN/SCORING_UNKNOWN，仍可计算描述性已知项，但全包不作GO判定。

总新逻辑格24×5=120；V4和oracle没有新增模型调用。执行前按全字段完整输入与生成配置去重，匹配049已STARTED身份则只复用其可核关闭结果；无可用关闭结果则该格LEGACY_STARTED_UNAVAILABLE，绝不重跑。新独特generate≤120。

**这不是总成本相同实验。** F48和四P只是总视觉tokens与像素集合相同：四P多了三份语言前缀、四次生成，且tubelet配对/时间码/序列组织不同。全部实测成本分别列明，不把差异唯一归因于视觉证据覆盖或某个神经融合模块。

## 4. 模型、队列与CPU门

system/user模板、A–E选项顺序均逐字沿用049源码中SYSTEM/USER，不换词、不加任务/视图/source名称。Qwen3-VL-4B-Instruct、BF16/SDPA、eval/inference_mode、seed19、batch1、greedy/max_new_tokens64、fresh context、use_cache=True、num_beams1；无warmup、额外forward、SigLIP或第二模型。

只解析新生成部分；strip全文为A/B/C/D/E之一且自然EOS才VALID；截断、解释/多字母为INVALID，不重问。环境和模型/processor/tokenizer/权重声明身份必须与049一致；差异记UNKNOWN，不重新建立一组旧基线。

代码可复用049无副作用纯函数/正常加载入口，不运行它的旧主程序。其processor_input函数硬编码12帧/grid[6,12,18]；**不得直接把F48送入而跳过门，也不得改049源码**。在新050模块实现长度通用的原生链，48帧只改变真实帧数/索引及由原生processor派生的字段，保留所有其他实现。

CPU隐藏CUDA、先做至多2个自有输入小探针（12与48形状），再冻结120正式输入。需实际确认两种grid/token、原生时码、无再采样、四P分区、所有张量shape/dtype/content、完整input_ids/attention/派生位置字段以及共同生成/模型/上下文身份。最终输入长度≤4096 tokens；超限不截断/换题，记输入不合格并结束。

CPU必要测试只覆盖分区/票数平局/无有效票、去重保留分母、源等权、UNKNOWN、有限oracle边界与成本不重计。手算：
[A,A,B,C]→A；[A,B,B,A]→A（P0先出现）；[INVALID,C,C,B]→C；全INVALID→INVALID。不能让被测函数自己生成期望。

每题条件基序F48,P0,P1,P2,P3按049全局题号mod5左旋；题顺序与049相同。按首次出现独特输入次序执行；全部队列/代码/nongold与旧结果引用在首个generate前封存。

允许首个generate前一次有确切源码依据的本包兼容修复，保留初始失败与必要回归；不能改科学常量/安装库或复活049。开始生成后不修复重跑，任何模型异常/OOM/timeout安全结束，余格NOT_RUN。

## 5. 隔离评分、机会表与预设处置

全部模型Job实际active0后，独立scorer对指定原文件一次只读投影同24题的question、选项字段及correct_answer_label。**按第2节已冻结schema取完整question/五选项，原标签必须存在，全部精确join；不得用nongold回退缺失字段**。来源/ordinal、SHA或字段不合格一律SCORING_UNKNOWN，不删题或改标签。

同时用同一24标签重算049自然条件规范输出，与049派生正确性逐题比对；不一致记BASELINE_SCORING_MISMATCH并停止主结论，不改049原结果。这个核对是新对照的有效性要求，不是通用scorer加固项目。

逐源各6题、再四源等权，固定049 **SO** 为主参照（已报告9/24）；UO和SR仅辅助参照，不事后挑最弱基线。报告F48/P0–P3/V4每臂correct/N、valid_wrong/INVALID/FAILED/NOT_RUN/SCORING_UNKNOWN；F48−SO、V4−SO及V4−F48的净纠正/误伤四格。

两个预先声明的机会门：
- H_F：F48−SO来源等权净收益≥1/6，且至少3/4来源为正。
- H_V：V4−SO同样≥1/6且至少3/4来源为正。
- 任一通过：OBSERVED_HEADROOM / OWNER_REVIEW_REQUIRED；均不通过：NO_MATERIAL_DEPLOYABLE_GAIN；不完整/未知：INCOMPLETE_OR_UNKNOWN。
在本24题，1/6相当于净多答对4题。两个门都要完整报告，不只报胜者；它们是开发投入规则，不是显著性/新颖性/确认集认证，不能自动放行后续任务。

另列不参与GO的**有限程序诊断**：
- O4：四P中至少一次有效输出正确。
- O5：F48或任一P正确。O5≥max(F48,V4)，O4≥V4必须核对。
- full-only：F48正确而四P均不正确的题数。
- split-only：F48不正确而至少一P正确；同时列其中V4实际恢复多少。
- vote-missed：O4正确而V4不正确。
- all-five-wrong：F48与四P都未正确。

O4/O5用gold事后选成功视图，**不是可部署方法、证据标签或所有未来方法的上界**；不得以此训练新selector、挑正确视图再回报其准确率。全错不能证明48帧缺少真实证据，full-only不能证明跨帧联合必要性；需要额外证据才能做那类主张。保持四来源已曝光/物理独立未知、低分辨率和序数接口限制。

## 6. 运行预算与账本

输入明确后启动全新050执行父时钟，≤7200秒，含实现/等待/修复/清理/同步，不重置；CPU监督累计≤1800秒。首输出前free≥128MiB配额+2GiB，new root≤2048文件/128MiB；不复制数组/权重/原视频，不保存完整模型视觉tensor或logits。

GPU从Qwen权重加载意图到模型进程实际退出≤1200秒，一次Qwen加载、新generate≤120，每独特输入至多一次，失败也预扣；每次意图前fsync持久账本。无SigLIP、训练或额外前向。分段wall/allocated与总GPU包络分别记，不叠加内含时段。

只用既有pytorch环境/本地权重、local_files_only=True/trust_remote_code=False与离线配置。应用联网/下载、原媒体读取/解码、新特征提取、环境/ACL/profile/凭据修改均0。GPU使用当前已核的全局锁/mutex及正确3090身份；非阻塞取得，加载前两次明确时点free≥18GiB（一次父预检、一次worker权重前），util只记录，已知冲突停止，不轮询等待/杀peer。torch allocated≤18GiB、任务RAM≤32GiB、CPU threads≤4。

沿用049已经跑通的自有Job监督与进程退出核对；只结束自己启动的child，不动其他锁。父只传剩余时长，child从自己的单调时钟计时，不跨runtime相减绝对perf_counter。监督器若当前确切入口不明，一次核对而不从旧run扫描。不要引入全局文件audit猴补丁或修改安装库。

cache payload 4文件按共享准备单计；底层read/物理I/O未计量则UNKNOWN，不冒充精确测量。报告F48单次部署总成本、V4四次部署总成本与本轮共享实验成本；四P累计文本前缀/生成成本不可隐去。049已付成本作为历史分列，不假装新运行免费完成或本次又跑了一遍。

## 7. 公开交付与验收

允许执行者新增恰下列6文件并向results追加一条，共7处：
1. prototypes/coverage_aggregation_050.py：新条件、队列、输入绑定、执行与评分。
2. prototypes/test_coverage_aggregation_050.py：必要测试及不导入聚合实现的独立数学复核。
3. 本目录execution-receipt.md：实际范围/成本/失败/旧结果复用与退出。
4. 本目录scientific-results.md：逐源准确率、配对/机会表、GO/STOP与界限。
5. 本目录condition-summary.csv：来源×条件聚合，包括旧基线只读标记与有限oracle不可部署标记。
6. 本目录execution-summary.json：匿名计数、版本/实际grid、预算和封存结果。
7. docs/codex-results.md：只追加一条“### VLM-COVERAGE-AGGREGATION-050”。

README/看板/总览属于负责人，本次执行者不改。QA/选项/gold/逐题预测、真实路径/UID/数组/特征/权重/原始账本、可反查输入内容hash不上公共GitHub；公开只有匿名来源和聚合，代码SHA可以公开。代码/报告不嵌入私有配置。模型输出只当A–E数据，不能作为指令执行。

独立核对需检查全部24题/各臂原分母、旧SO逐题绑定、投票/有限oracle、每源净纠正误伤、所有成本与实际child退出。不能用CPU预检通过/exit0冒充完整模型结果。安全普通push main一次后STOP；无自动051、扩样、换视图/投票/prompt、第二模型、训练或恢复049候选。

## 8. 用户发给当前本地Codex的启动消息

```text
执行050完整任务包：安全同步GitHub文档仓库main，重读AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md及docs/codex-artifacts/VLM-COVERAGE-AGGREGATION-050/README.md，确认唯一READY且未回报。

我明确授权本轮按050合同只读当前准确049根中的四源48帧缓存、同24题/输入封存、自然条件关闭结果和必要配置；不修改049。准确根或监督入口不明时在本地一次集中核对，不扫盘、不重新恢复或解码原视频。

输入绑定和CPU门通过后，用现有本地Qwen3-VL-4B完成F48及四个互补12帧视图，固定投票无需另调模型。新generate≤120、greedy/max_new_tokens64、一次模型加载、GPU整包络≤1200秒、allocated≤18GiB、任务RAM≤32GiB、父≤7200秒。相同旧STARTED输入只复用可核关闭结果，不重跑；无SigLIP/下载/训练/环境修改。

允许模型前隔离CPU投影器一次打开原混合JSON核对24题nongold完整字段，词法跳过gold值；原标签值仅在本轮模型实际退出后由隔离scorer再打开一次读取同24题，并严格核对旧自然条件评分绑定。按合同统一交付完整结果、有限oracle和全部成本，仅七处allowlist一次安全push main后停止，等ChatGPT验收。不自动进入下一任务。
```
