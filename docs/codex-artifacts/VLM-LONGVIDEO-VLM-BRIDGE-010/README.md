# VLM-LONGVIDEO-VLM-BRIDGE-010｜正式研究桥接：在已有真实24分钟视频上有条件执行Qwen3-VL＋SigLIP A/B

**2026-10-14｜READY / USER_TRIGGERED_CONDITIONAL_REAL_VLM_INFERENCE（唯一READY；新的模型前向/GPU额度须由用户在原Codex长会话主动明确授权才可使用）。** 本任务首次从小型无语言的RGB时间顺序head，转向**真实视觉语言模型、相同问题、同帧预算下的长视频选帧对照**。冻结条件与指标，不随观察结果调题或挑seed；**仍不是HourVideo/Ego4D官方QA或方法科学优势证据**。本任务完全离线，使用用户已经明确授权的 **One Week (1920) 官方Commons 480p VP9本地完整视频**，不联网、不使用开发集QA、不操作旧受保护数据。

## 已验收的科学事实与为什么不能继续用时序小head作为结论

- [b11cb4e](https://github.com/floomeer83felix-source/vlm/commit/b11cb4e9fe49cf57536afc7c8665ce7780d6a05b)是**首次真实≥20分钟本机视频配对GPU实验验收通过**：480p VP9、ffprobe1,465.597s、PyAV真实完整解码43,924帧，489个采样时间点横跨1,465.464s；同影片前70%训练/后30%非重叠验证，同样128真帧/160固定验证pairs。RTX3090上uniform128和motion128**各100次**真实backward/optimizer.step，head24,705参数、总GPU1.938s；两组验证准确率**均为45.00%（差0百分点）**，首批loss0.689918/0.691118，末批0.779309/0.732843（不同batch，不能推断收敛）。**当前无运动优先优势证据，45%也不能推断跨影片显著低于随机**；同片后段并非独立heldout，未使用Qwen/SigLIP或HourVideo答案。该009已结案，不再重训更大同片RGB小头以寻找有利结果。
- 本机`Qwen3-VL-4B-Instruct`和`SigLIP`确切已授权模型/processor权重位置仍为`ASSET_ENTRY_UNKNOWN`；历史记录**没有证据证明其已经存在/缺失**。不因为CUDA 3090可以运行24,705参数就猜4B权重可载入24GB VRAM。**必须先CPU证实确切入口、静态身份、完整processor可用性**；若不齐，0 GPU前向、清楚`MODEL_ASSET_ENTRY_HOLD`并告诉用户需提供现成合法本机权重入口，不能自动下载或装依赖。

## 同一父任务依次执行——A/B是否运行完全由真实资格门决定

### A. 零网络CPU本机资产/视频资格（一个前置门、≤8分钟）

1. 在原同一Codex聊天安全同步独立GitHub文档checkout，重读AGENTS/唯一READY/历史结果、本任务README，确认010尚无历史收据。只读检查此前用户精确授权的**至多两个已知视频候选文件名**：优先 `D:\download\One_Week_(1920).webm.480p.vp9.webm`，仅当不存在才按用户上轮明确授权的备选`D:\download\One_Week_(1920).webm.480p.vp9`。**不枚举Downloads、不搜全盘、不得读取任何旧Charades/Ego4D.part及私人QA**。验证常规非reparse文件、封闭WebM、视频实际PTS≥1200s/容器及来源非冲突，仅限为重新使用一次数据所需的小范围CPU采样；已有009全片decode/只读SHA证据可复用，但本轮不重跑009的训练或全部decode以图“再次证明”。
2. 仅在上轮Codex聊天已明确标识且用户授权的**精确本机模型路径**、既有`HF_HOME`/缓存条目入口或现成用户给定模型配置入口（最多**2个模型根目录各一处**，不得遍历用户文件系统或递归搜索所有缓存）只读核静态manifest、config/processor/tokenizer和所需权重分片文件可用性。Qwen必须确切`Qwen3-VL-4B-Instruct`而不是相似Qwen2或任意4B聊天模型；SigLIP须有**配对文本/图像**相似度处理器和权重，避免图像单塔假冒query-aware选帧。通过已有包的离线模块spec/metadata确认torch/transformers及必要vision decoder接口存在，**不使用pip/conda、HF联网repo lookup、自动snapshot下载、远端推理API或盲目录搜索**。所有from_pretrained强制`local_files_only=True`与`HF_HUB_OFFLINE=1`，仅加载已授权本地来源，未就绪就`MODEL_ASSET_ENTRY_HOLD`（具体按ASSET_MISSING/PROCESSOR_MISSING/DEPENDENCY_MISSING等匿名枚举）。
3. CPU阶段仅报告模型身份/必要文件是否具备、现成CUDA环境包是否兼容（不会加载GPU模型），连一份合法模型目录都找不到就**本轮STOP、GPU0**；可以记录用户下一步需要给的**非敏感资产名称**，绝不能凭旧09只检测视频就称Qwen ready。
4. 在任何GPU模型加载之前由用户**在原Codex同一聊天明确授权**本任务“最多4次本机Qwen真正生成、SigLIP 48候选帧每题一轮排序、GPU累计≤40分钟/≤20GiB新框架显存、零网络”；如启动指令未包含这项资源授权，A可以进行但B仍`GPU_AUTH_HOLD`，不自动执行模型调用。

### B. 两个预注册无答案的真实电影问题，12帧对12帧（有条件的RTX3090单轮实验）

- 本轮两条固定**内容中性的英语指令**，无需人类标注或查看电影来挑题：
  - **P1**：`Summarize the main sequence of visible events in this video in chronological order. Mention only details supported by the images, and state uncertainty.`
  - **P2**：`Explain what visibly changes between the beginning, middle and end of this video, and describe evidence from the images without guessing.`
- 只读从视频单一PTS时轴严格均匀选最多48个候选真实RGB帧；校验每帧PTS finite/递增，覆盖≥1200秒。**A均匀臂**：从同48候选按固定等间距索引选**12帧**；**B查询相关臂**：对P1和P2分别用已授权SigLIP双塔text/image特征进行确定性余弦top12选择（去重、相似度排序后**按PTS升序**供Qwen），两个问题都固定同48候选；SigLIP候选帧视觉特征可以只生成一次，但其GPU与CPU总成本全部单独计入B。不可用随机/纯motion取代SigLIP却仍叫query-aware；如果SigLIP不能安全离线装载，**不运行Qwen A臂以免形成不完整配对结果**，报`MODEL_ASSET_ENTRY_HOLD`。
- Qwen3-VL-4B-Instruct 的模型权重/量化/processor、视觉分辨率、system prompt、token上限（每次≤192）、确定性decoding（do_sample=False）、输入12帧、同一问题内容在A/B保持完全一致，只变选帧策略。推理计数**两条问题×两组=最多4个本地Qwen generate**，以AB/BA固定交错顺序防系统顺序差异；不得增加warmup调用或用先前未经核验的生成当本次结果。主干`eval()`、`torch.inference_mode()`，**不训练任何head/adapter或修改checkpoint**，不取外部API，不使用真实电影事实答案或开发标签评测。
- 记录两个问题的实际输入可用性、**4次模型generate的尝试/成功类别**、相同输出长度计数、两臂候选覆盖PTS span、均匀/检索帧集交并比、B的图像/文字特征成本/耗时，Qwen模型加载/生成单次耗时、GPU累计耗时、实际`max_memory_allocated`。需要定量对照时只能比较**效率/时间覆盖/可运行性**；两条通用问题**没有标准答案**，不能报告“准确率”“B性能优于A”“统计显著”或由模型自身输出自评。
- 只允许现有本人Windows RTX3090、64GB RAM、当前conda `pytorch`环境（不新装包、下载、驱动更新/重置/杀进程）；模型若占显存太大、CUDA OOM/NaN/异常或显存抢占→安全停止，不重试/量化配置改动。GPU先做两个≥2秒间隔nvidia-smi状态快照，free≥8GiB/util≤30%、已知互斥锁和明显冲突计算任务0，获得本任务自身锁且不解除他人锁。**整轮GPU≤40分钟、从该任务开始新增PyTorch框架分配峰值≤20GiB、前台父任务≤55分钟**，单调墙钟且外层仅监督自己进程；若无法预先确认可执行的硬时间安全门，不上GPU。模型只加载既有确切已授权资产、可行才运行；一个机型成功的小head不能保证大型Qwen模型一定可用。

### C. 隔离、科学边界和单次匿名交付

- **仅在A阶段模型资产+推理许可+GPU资源及movie合法性真实全PASS时，才运行4次模型调用**。没有真实资产不装包、不下载、不提供假Qwen输出；若不符合走明确HOLD、让用户决定是否单独下载模型。真正Qwen推理完成也只是公开1920电影**无标准答案**的技术A/B，不能报告HourVideo官方题目准确率、Ego4D版本桥接或视觉因果理解已提升；以后要做这些必须另准备属于官方样本的匹配媒体/合法开发题和独立匹配版本证据。
- 不公开原影片、帧/缩略图、时间戳序列、题目之外的任何用户私有问答、生成的完整模型回答、私人模型路径/哈希/权重/日志、GPU进程身份、电影可唯一映射标签；只提交匿名聚合，且不能未经额外同意推送模型完整答复或视频。
- 最多两处文件：新增`docs/codex-artifacts/VLM-LONGVIDEO-VLM-BRIDGE-010/real-vlm-bridge-receipt.md`，并在`docs/codex-results.md`末尾恰好追加一条`### VLM-LONGVIDEO-VLM-BRIDGE-010`。报告A/B各PASS/HOLD阶段、模型来源/processor布尔、是否真实Qwen4/4调用、SigLIP检索vs uniform帧数与PTS覆盖、GPU秒/峰值VRAM/机器环境匿名类别，以及科学证据等级。一次正常push main后STOP；不修改旧实验看板/许可证、旧part或QA数据，`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`、HourVideo/Ego4D release/PTS bridge UNKNOWN不变。
