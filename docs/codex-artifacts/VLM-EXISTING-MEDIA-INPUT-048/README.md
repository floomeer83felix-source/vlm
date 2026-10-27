# 048已归档：有界输入失败报告验收，真实processor输入未取得

2026-10-27：[负责人验收](../../research-decisions/post-048-existing-media-input-disposition-2026-10-27.md)。
**ACCEPTED_BOUNDED_INPUT_FAILURE_REPORT / REAL_PROCESSOR_INPUT_NOT_QUALIFIED / CLOSED。**
两遍各43924显示帧的CPU解码与95帧准备有报告；processor依赖启动失败，load/calls0，
B0/P/N均NOT_RUN，完整输入和最终SHA稳定性UNKNOWN。25项fallback缺完整公开实现，复现范围受限。
048已消费，当前0 READY，不重跑、不自动049或追加本片启动修补/解码/模型任务。
以下合同保留历史，其中READY及启动指令失效。

# 048：现有单影片真实解码与CPU输入验收

2026-10-26。**CLOSED / NOT_RERUNNABLE**。父任务VLM-EXISTING-MEDIA-INPUT-048。
用户要求继续直到新任务，本包一次完成以下工程链，不继承任何旧任务预算。由用户在当前本地Codex聊天发送启动消息并附单个文件路径。

## 输入与依据

唯一媒体是用户此前明确指定给022的普通本地影片。参见[022匿名回执](../VLM-TRAIN-SOURCE-VERIFY-022/read-only-source-verification-receipt.md)：历史103909467B、WebM/VP9、480p、1465.597秒。当前存在性必须重新检查。只用启动消息中的精确路径，不搜盘、不猜同名、不查旧日志/私有根。缺路径、不是普通文件、祖先reparse/symlink或尺寸不符即停止。
processor目录只取当前聊天已知的确切本地目录字面值，丢失则UNKNOWN，不搜索旧配置恢复。

本片超出180–900秒科学窗口；只用于真实解码到输入的工程验证，不裁片、不改变原科学窗口、不计入6+2/64格。022的历史身份、训练权利、评测源独立性UNKNOWN不升级。
045只有程序RGB；046未取得媒体；047只有数学评分。本轮新增证据是实际媒体解码、共享RGB准备及实际完整processor输入关系，不是新机制或效果实验。

允许只读公开045核心prototypes/native_pts_adapter_045.py、046核心prototypes/holoassist_real_input_046.py作为参考，不运行旧入口。046下载器、MP4 atom限定和父子绝对时钟逻辑不得照搬。
可借prototypes/auditable_runner_040.py的Job平台监督，不运行040工作负载。
目标Transformers4.57.6 processing_qwen3_vl.py SHA256为efd8d64aaf608aad1ffb3e6d503d6a99e5227d007df95c1d9fa905d998cda4a9。使用现有pytorch环境和Torch2.5.1/NumPy1.26.4/PyAV/Pillow，不安装升级。

## 有界执行

安全同步main，重读AGENTS/看板/results/总览/本合同，核唯一未交付READY048。
新根为文档checkout同级vlm-private-048，存在即停；无reparse，≤64MiB/1024文件，初始空闲≥64MiB+2GiB。
视频原地只读，不复制、转码或保存帧/tensor正文。CPU线程≤4、Job RAM≤4GiB，CUDA隐藏且不初始化。
最多前后各一次流式SHA，各≤60秒，只证明本轮字节稳定性，不认证009历史身份。
媒体Python接口read返回总计≤1GiB，读前保守预扣，不能称物理磁盘字节精确计量。
完整顺序视频解码最多2遍，各≤600秒；不seek补帧，不解音频。F≤60000，单帧≤4096×2160。
processor阶段≤300秒，一次load，最多4次调用：1 B0 probe+正式B0/P/N各一次。
必要纯函数/拒绝单测初轮≤60秒，仅真实媒体开始前可有一次定位修复回归≤60秒。不新增合成研究矩阵或跑旧suite。
独立post-exit核查一次≤60秒；全部计算阶段outer累计≤1800秒，父从首次本轮操作起≤7200秒。
父用自己的单调时钟收紧阶段剩余额度；不跨解释器相减绝对perf_counter。阶段可在同一worker连续执行以保留RGB内存，由父阶段事件监督。到期只终止自己Job并核active0，退出不明即停。
媒体或正式输入失败后不修复重跑、不换片、不加额度。除GitHub协作外网络/下载0；权重、模型、forward/generate、GPU、训练、真实QA/标签/旧预测0。

## 真实时轴与选帧

第一遍CPU顺序解码至EOF，保存私有index/PTS/time_base/duration和尺寸表，不留像素数组。缺PTS、非正time_base、非严格递增显示PTS、解码错误或未到EOF即UNKNOWN。
令原始p_i=PTS×time_base，工程t_i=p_i-p_0，T_cov=t_(F-1)。要求F≥48且1200≤T_cov≤1800。
T_cov只是首末帧显示起点跨度，不是完整媒体endpoint；归零不是原始拍摄零点或标注桥。
B0/P共同索引i_j=round(j(F-1)/47)，精确ties-to-even。
N目标u_j=j T_cov/48，j=0..47，按明确工程显示保持约定[t_i,t_(i+1))选帧i；不推断最后帧时长、不认证编码duration/原科学强N资格。
实际正有限average_rate用于B0，不以F/T_cov替换。记录max|i_j/rate-t_i_j|，小偏移/CFR也继续，不造漂移。
冻结第一遍plan。第二遍顺序至EOF，逐帧核PTS/time_base/index，选两组索引并集≤96帧转RGB，固定bilinear等比letterbox到192×288黑边，ties-to-even尺寸和居中。只在内存保存，B0/P共享同一48帧数组。
前后stat/SHA或两遍时序变化即不合格；最终后检失败须降级已得输入，不能保留PASS。

## 实际processor边界

同一base、原生video模板和固定“Describe the video.”，无题目标签/臂名/来源身份。关闭二次采样/resize；共同CPU BF16视觉边界、int64文本，预期grid[[24,12,18]]/1296视觉tokens。
B0：实际F/rate/i_j，duration=T_cov工程声明。
P：完全相同RGB/metadata，单请求实例只覆盖原生_calculate_timestamps，核indices/fps/merge2，返回每对选中帧t的均值；不改最终tokens或安装库，不硬编码F96/T96。
N：对应RGB；表示层total_frames48、indices0..47、fps48/T_cov、duration=T_cov，用原生回调。实际源与表示层metadata分列。
probe通过后封存代码/plan/base身份，正式按B0/P/N各一次。记录实际回调、24个原生时码、tokenizer roundtrip。
所有实际返回字段纳入比较；P/B0视觉直接torch.equal，非时间文本一致，base方法/组件身份不变。额外字段不能忽略。
N也比较完整输入，不能仅凭RGB推断DIFF。分别报告未量化差、原生0.1秒格式差和完整输入等价类；相同就记INPUT_EQUIVALENT_AFTER_NATIVE_QUANTIZATION，不推断模型不敏感。
同视觉tokens不保证同总成本，三逻辑输入不是模型观测，实际模型调用0。

独立post-exit标准库读取器用私有冻结plan重算索引/时间公式、量化和三行状态/等价类/成本，不调用被测映射自证；原tensor等价仍是worker实测，不能冒称第二次独立tensor复现。
共享准备成本只记一次，outer与内含phase分列，不相加重复成本，不跨时钟域相减。

## 交付与停止

严格六处允许：
- prototypes/existing_media_input_048.py
- prototypes/test_existing_media_input_048.py
- 本目录real-media-input-receipt.md
- 本目录input-boundaries.csv：始终B0/P/N三行，未运行保留NOT_RUN
- 本目录execution-summary.json
- docs/codex-results.md末尾一条本父结果

公开只用A01/EQ1等匿名别名、聚合偏移、计数、grid/dtype/shape/token长度、相等布尔、阶段资源、安全错误枚举和代码SHA。
不得公开路径/filename/片名/URL、媒体/帧/输入身份hash、精确PTS/选帧序列/token IDs/完整时码或私有原始日志。完整审计仅本轮私有根，不读旧证据填空。异常转安全枚举后发布。
终态CPU_REAL_MEDIA_INPUT_PASS/PARTIAL_INPUT/INPUT_UNKNOWN/PREFLIGHT_BLOCKED，全部附REAL_SCIENTIFIC_COHORT_NOT_QUALIFIED / NO_MODEL_EXPERIMENT。保留失败和预算事实，不预填PASS。
核stage恰六处，旧results完整保留，一次普通push后停止。任一父回报消费048，不自动049/下载/GPU/投稿。NOVELTY=RETAIN0，旧停止结论保持。
