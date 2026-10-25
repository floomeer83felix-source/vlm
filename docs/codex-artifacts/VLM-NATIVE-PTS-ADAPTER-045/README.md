# 045已归档：限定CPU原型验收通过，执行轮已消费

2026-10-25：[负责人验收](../../research-decisions/post-045-native-pts-adapter-disposition-2026-10-25.md)已关闭045，当前0 READY。
9/9正式CPU槽通过，适用范围仍限定本96源帧/96秒夹具，真实媒体/任务效果未验证。
以下合同保留历史，旧唯一READY和启动语句均失效，不自动扩变体、下载或GPU。

# 045：精确PTS到原生Qwen时间码的CPU适配与输入边界验证

2026-10-25（北京时间）。**CLOSED / ACCEPTED_CPU_NATIVE_PTS_BOUNDARY_PROTOTYPE / NOT_RERUNNABLE。**
父任务：VLM-NATIVE-PTS-ADAPTER-045；唯一READY。用户本轮要求“继续直到下一任务”，负责人据此下达本次无媒体/无网络/无模型推理的CPU实现包。
这是[64格设计第4–5节](../../research-protocols/natural-video-clock-feasibility-design-2026-10-24.md)中尚未完成、可独立于下载推进的P接口工作。
044直连获取路线仍暂停；本包不换源下载、不续传、不恢复042–044，不创建新的图形时钟问答实验。

## 1. 目标与结论边界

实现一个隔离、单请求作用域的PTS适配层：**只改变处理器计算temporal patch时间的入口**，
保留原生时间码格式、tokenizer、图像/视频处理及最终BatchFeature路径。
在真实已安装Qwen3-VL processor上，核明P实际回调、原生时码/input_ids及BF16视觉输入是否符合预期。
这是组件实现/输入资格，不是新时间算法或模型效果；受控PTS表不充当自然VFR证据。
一个成功的CPU适配仍不解决真实8源、标签同钟、题目实例身份、强N基线或64格准入。NOVELTY=RETAIN0。

## 2. GitHub与本地输入范围

按AGENTS安全同步独立文档checkout，重读AGENTS/看板/总览/results/本README；确认唯一未交付READY045。
只读以下公共依据，不运行其旧任务、tests或主程序：
- Transformers v4.57.6的[processing_qwen3_vl.py](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/qwen3_vl/processing_qwen3_vl.py)，Git blob17bdd975eef337371aa763824edc7e6ec1987dbf。
  _calculate_timestamps(indices,video_fps,merge_size)由原生__call__调用，随后原生格式为“<time:.1f seconds>”。
- prototypes/cache_input_contract_041.py，blobbf763213b74a15db7dbb31bc29f7515be12cdb9b，仅参考本地processor加载、VideoMetadata、do_sample_frames=False及CPU边界签名写法；
  不导入/运行其ResponseCache、oracle、序列、suite或私有配置恢复逻辑。
- [041公开CPU收据](../VLM-CACHE-INPUT-QUALIFICATION-041/cache-input-results.md)、[当前设计](../../research-protocols/natural-video-clock-feasibility-design-2026-10-24.md)；
  040平台blob3e56faf30afea1bed850c085bceb2afcc4fb257c仅可复用Job/Process。不得运行040工作负载。
- 043/044回执只用于确认获取路线已停；不执行其传输器或读取任何旧私有根。

允许使用**当前本地Codex聊天已明确的既有Qwen3-VL-4B processor目录及既有pytorch解释器**，只正常读取processor/tokenizer配置与分词文件。
AutoProcessor须local_files_only=True、trust_remote_code=False；不加载AutoModel/权重，不重新下载任何资产。
不从旧039/041 runtime.json、旧helpers、账本或盘符/缓存目录扫描来恢复路径。若当前精确入口无法恢复，
只完成新公开适配/验证器实现与可做的标准库检查，真实processor部分NOT_RUN并统一回报，不另派找路径微包。
最多读取4个确切已安装processor相关源文件、合计≤4MiB核API/版本；不遍历site-packages或复制安装库。
版本/源码若不符本合同目标4.57.6，原样记API_VERSION_HOLD，不升级环境或追逐最新API。

本次CPU范围允许Torch/Transformers/NumPy和现有processor/tokenizer本地配置；**模型权重正文、模型加载、forward/generate、CUDA初始化/GPU均0**。
不得读真实媒体/partial/帧、旧QA/gold/预测、动作标签或私人研究文件。
新根为文档checkout同级新目录`vlm-private-045`：存在即STOP，不复用/清理旧根；只核必要父链非symlink/reparse与空间。

## 3. 连续完成的实现与验证

### A. 独立适配模块与必要的拒绝规则

新增`prototypes/native_pts_adapter_045.py`。
建议以Qwen3VLProcessor隔离子类/包装实例实现，每次P请求持有不可变源index→PTS映射，
并在其_calculate_timestamps入口核**实际传入的indices/fps/merge_size**，用源索引查PTS后返回每patch首尾PTS的均值。
只支持本合同的单视频、48帧、merge_size=2；其他batch/长度/merge明确拒绝，不伪称通用支持。
可共享只读的既有tokenizer/image/video processor，但不可修改安装库、全局方法或base实例的类/方法。
基类配置身份前后应一致；本包验证串行请求隔离，不声称多线程/生产并发安全。

- 原始整数source indices与真实声明fps保留；不能用浮点假indices、改fps来凑PTS。
- P仅在时间计算入口干预，不手工拼视频placeholder、不改最终input_ids/attention_mask、不改聊天模板/视频内容或时码格式。
- 记录回调实际args、请求映射身份与返回未量化时刻；若原生链没调用它或indices被意外覆盖，就FAIL/UNKNOWN，不以传入metadata自证成功。
- 拒绝缺映射、非有限/负/非递增PTS、缺/非正fps、未知/错序index、非48帧/多视频/非2merge等非法输入；
  缺数据不能退回默认24fps、拟合原点、补时刻或悄悄使用上一个请求映射。
- 若复制上游代码片段，保留原Apache2.0声明/版本链接；不重分发tokenizer或模型文件。

新增`prototypes/test_native_pts_adapter_045.py`做与上述风险对应的标准库/纯计算检查，不重复041缓存或038–039模型问答。
正式前至多2次真实CPU processor探针，仅核构造/参数/回调接通；所有调用和失败计费。
最多一次根据公开源码可定位的接口兼容修复，保留初始错误；不得改下述刺激、预期或格式以迎合结果。
真实正式输入验证只封存后跑一次；不能看正式输出后改条件重跑。

### B. 固定受控输入（不是媒体）

固定F=96、统一原点0、T=96秒、fps=F/T=1；source index i=0..95。
48个选中indices_j=round(j*95/47)，j=0..47，精确有理数round-to-nearest/ties-to-even。
在内存直接生成48个192×288 RGB uint8：
RGB[j,y,x,c]=(17*indices_j+3*y+5*x+29*c) mod256。
四张时间表共用完全相同RGB/indices/fps/T：
- CFR：PTS_i=1000*i，time_base=1/1000，所有显示duration=1000ticks。
- A：前48个源duration=500ticks，后48个=1500ticks；PTS为此前duration累和，末显示结束96秒。
- B：前48个duration=1500，后48个=500；同样总时长96秒。
- Q：PTS_0=0，其余PTS_i=1000*i+10；duration为相邻差，末帧结束固定96000ticks。
  Q与CFR未量化时刻不同，但本配置原生一位小数时间码预期相同，必须诚实报告量化等价。

所有PTS仅是程序控制表，未解析容器/解码，也不证明自然录像的任何性质；T=96秒是API夹具，不是符合180–900秒准入的原录像。
不用字体、时钟图、文字叠字、音频或字幕，不保存RGB/tensor大块文件。
提示统一为system“You are a helpful assistant.”、user一个video项与“Describe the video.”；
沿原生apply_chat_template(tokenize=False,add_generation_prompt=True)，再真实processor调用。
输入video_metadata为total_num_frames=96、fps=1、duration=96、width288/height192及上述整数indices；
do_sample_frames=False、do_resize=False、return_tensors='pt'，不得让适配器代替原生tokenizer。
最终视觉float统一在CPU转BF16，整数不改；签名包括所有返回kwargs、dtype/shape/device/hash。
完整有效输入比较使用真实返回边界和共同base processor配置身份；fixture标签、外部PTS映射与适配器代码身份单独记，
不能混入边界hash制造等价输入的假差异，也不能从比较中漏掉实际返回kwargs。

### C. 封存后的9个实际CPU输入槽（一次，不补跑）

| 槽 | 路径/控制表 | 必查关系 |
|---|---|---|
| Q01 | 原生/CFR | native参照、grid与真实24个时码 |
| Q02 | P/CFR | 完整有效输入等于Q01，回调确实用本请求映射 |
| Q03 | 原生/A | 完整输入等于Q01；B0不会隐式读取本地PTS表 |
| Q04 | P/A | 视觉/网格与Q03逐元素相等，仅预期时码造成文本输入差异 |
| Q05 | P/B | 视觉等于Q04，时码按B表改变，不沿用A状态 |
| Q06 | 原生/A，置于适配后 | 完整输入仍等于Q03，base未被污染 |
| Q07 | P/A，再次显式提供A映射 | 完整输入等于Q04，不继承B |
| Q08 | 原生/Q | 完整输入等于Q01 |
| Q09 | P/Q | 完整输入等于Q08，未量化时刻差与最终量化等价分开 |

负责人独立有理数预计算的24个时码（仅设计算术，不是processor实测）：
- CFR/Q原生预期：1.0,5.0,9.0,13.0,17.0,21.0,25.0,29.0,33.0,37.0,41.0,45.0,50.0,54.0,58.0,62.0,66.0,70.0,74.0,78.0,82.0,86.0,90.0,94.0。
- P/A：0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,27.0,33.0,39.0,45.0,51.0,57.0,63.0,69.0,75.0,81.0,87.0,93.0。
- P/B：1.5,7.5,13.5,19.5,25.5,31.5,37.5,43.5,49.5,55.5,61.5,67.5,73.0,75.0,77.0,79.0,81.0,83.0,85.0,87.0,89.0,91.0,93.0,95.0。
P/Q量化后应等于CFR/Q原生，未量化差异仍记录。

所有视觉预期grid[[24,12,18]]，1296个视觉tokens；这只是本受控输入的接口预期，不代表同计算/任务质量。
用直接dtype/shape/torch.equal核B0/P BF16视觉与grid，不只比较hash或metadata。
用独立有理数首尾均值核24个回调时刻及实际原生输出时码；记录真实input_ids/attention等边界。
可decode最终input_ids以审计原生时间码、剔除仅已知timecode片段后比较其余文本完全相同；
decode只用于验证，不把重建文字/手工token回灌为P输入。
若tokenizer round-trip/特殊token导致无法确认“只有预期时码差异”，如实TEXT_DIFFERENCE_UNKNOWN，不跳过该门。
量化相同的完整输入是等价类，不能称两次独立模型证据；本轮所有9次预处理仍按实发生计费，不运行生成。

非法输入测试单列，不代替9槽。所有槽保留PASS/FAIL/NOT_RUN，失败不删、不放宽grid或变成不同分母。
真实入口不支持就如实报告，仍交可完成公开代码/纯计算部分；不扫描私有盘凑完整结果。

### D. 统一工程结果与剩余研究门

交付说明：适配究竟接在哪个公开入口、实际回调/最终时码/视觉等价/全输入关系、
原生base与请求隔离、非法输入拒绝、所有实际调用/配置源码身份/CPU资源/失败。
CSV每槽一行，包含fixture、indices/PTS摘要、实际fps/merge、回调次数、24个原生时码、
raw/量化差、各key边界、视觉/完整签名、直接相等关系及状态。可公开自造输入对应的token IDs，私有配置正文与路径只留本地。

全部真实门通过最多报**CPU_NATIVE_PTS_ADAPTER_BOUNDARY_PASS / NATURAL_MEDIA_AND_TASK_EFFECT_UNKNOWN**；
只做了纯计算/接口未接通则IMPLEMENTATION_PARTIAL / REAL_PROCESSOR_NOT_RUN或BOUNDARY_HOLD。
不将该包称真实输入/媒体完整资格、自然VFR发现、模型不敏感或科研收益。
用回执明确哪些原设计门已缩小不确定性，哪些仍缺真实资产/时钟/标签/题目/强N基线；
素材入口仍暂停，没有这些资源不自动另派综述、假传输、找路径或合成行为变体。

## 4. 总预算与控制

- 单CPU正式worker，一次processor/tokenizer资产加载；可为每个P请求构建隔离processor实例，共享只读组件，不重复加载资产。
- 全包实际processor调用≤12（含失败/探针/正式9槽），探针≤2；未用额度不扩变体或复跑正式槽。
- 标准库/纯计算suite≤2×60秒；真实processor worker≤300秒；全部受监督执行累计≤600秒；父≤3600秒。
- Job RAM≤4GiB，CPU线程≤4；临时CUDA_VISIBLE_DEVICES为空、HF_HUB_OFFLINE/TRANSFORMERS_OFFLINE开启，
  local-only且trust_remote_code=False；只准is_initialized确认未初始化，不查设备或nvidia-smi。
- 进程内应用网络/子进程拒绝守卫、权重正文拒绝；既有运行库/配置/分词正常只读，
  仅本轮新根可写，TEMP/HF缓存指向新根；Git文档同步/允许的最终push除外。
- 新根≤64MiB/1024文件，首输出前空闲≥配额+2GiB；不保存RGB/整块视觉tensor或模型文件。
- 所有child执行前进自有非breakaway Job，计入失败/清理wall，实际active0才结案；只清理本轮所有权可证进程。
  不沿用042错误的监督磁盘轮询方式，不动旧锁/用户进程。归属或监督失效就停止后续进程，保留未知。
- 获取/媒体/解码/标签、模型权重/load/forward/generate、GPU、安装、环境迁移均0；不继承旧任务许可/预算。

## 5. Codex交付allowlist（仅五处）

1. 新增`prototypes/native_pts_adapter_045.py`。
2. 新增`prototypes/test_native_pts_adapter_045.py`。
3. 新增本目录`processor-boundary-receipt.md`。
4. 新增本目录`input-boundaries.csv`（固定9槽；探针/非法输入另在回执记全）。
5. 只在`docs/codex-results.md`末尾追加一条045父结果。

不改本README、看板/总览、旧模块/tests/收据、安装库或任何真实输入。
核实际stage仅上述路径，私有路径/配置/权重/真实媒体与答案不上Git；一次安全push main后STOP。
completed/partial/blocked父回报均消费045；不自动046/GPU/下载/Issue/PR/投稿，不派补跑以填齐本轮未知。

## 6. 用户一次启动消息

> 安全同步GitHub文档仓库main，重读AGENTS.md、任务看板、总览、codex-results及045 README，确认唯一尚未交付的READY父任务VLM-NATIVE-PTS-ADAPTER-045。按合同连续完成精确PTS适配、真实CPU processor输入验证及统一脱敏交付后停止。本轮只用当前聊天已明确的现有processor/tokenizer配置与Torch/Transformers/NumPy做CPU预处理；不读权重或旧私有根，不扫盘；应用网络/媒体/解码/标签/模型推理/GPU均0，不恢复044下载路线。
