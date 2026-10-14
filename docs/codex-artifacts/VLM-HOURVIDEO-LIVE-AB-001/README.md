# VLM-HOURVIDEO-LIVE-AB-001｜RTX3090首次真实长视频A/B：2道配对QA、4次模型调用（预先排队，非READY）

**2026-10-13｜QUEUED / REAL_MEDIA_AND_GPU_AUTHORIZATION_HOLD。** 用户要求尽快正式开跑，所以把**可直接执行的单视频真实GPU小样本实验**提前设计好；本文件**不是GPU/模型/权重下载许可**，不能因用户表示急切而自启，不能在当前唯一READY的META-006或以后真实视频获取任务仍未结案时并行跑。只有ChatGPT验收上游[一段真实官方视频获取](../VLM-EGO4D-LIVE-MEDIA-002/README.md)，且实际媒体/版本/题目和模型资格通过，用户另行明确同意**4次前向、至多40分钟RTX3090 GPU时间**后才把本父任务设为唯一READY；仍须用户在原同一Codex长期会话发执行消息。

## 先确认实验可用，而非制造准确率

1. 前置：单段用户合法获得的真实原始canonical`full_scale` Ego4D视频，完整可读取、时长≥20min，本机私人文件/源UID映射受保护；对应HourVideo `dev_v1.0_annotations.json`中**同一video_uid**的至少2道有标准答案的开发QA，题目/答案只用于本机推理与正式评分，不用于训练或选帧排序。**UID命中官方Ego4D `v2_1`不是同版本/剪辑起点/PTS兼容的充分证据**：必须给出独立来源/发布版本或时间轴对齐的非泄漏验证；未验证则可只做**UNSCORED_REAL_VIDEO_SMOKE**（如果GPU仍被用户明确许可），不把问答结果当正式基准正确率。视频版本或QA转时间轴有疑义即不做`SCORED_AB`。
2. 在用户既有Windows RTX3090/64GB机器上使用当前预装、已许可的PyTorch/CUDA与**已经存在且本机可用**的`Qwen3-VL-4B-Instruct`和`SigLIP`或经用户另行许可的现存同等查询图像相似度模型；**本父任务禁止pip安装、下载模型权重、升级Torch/CUDA、驱动重置、训练/微调/蒸馏**。如果任一权重/处理器/依赖不存在或不能安全载入3090，提交`MODEL_ASSET_MISSING_HOLD`，不能自行下载大文件或切换不同模型冒称公平比较。没有足够VRAM就安全STOP，不杀别人的GPU进程。
3. 从已经明确对应的一段视频在私有内存中只解码所需帧，PTS以完整容器/视频时钟一致性审查为基准。只取**两道冻结的代表QA**，提问者给模型的文字应**A/B完全相同**，标准答案绝不进入任一推理prompt/检索rank特征。A组：在同一真实物理时轴上**均匀采12帧**；B组：对每道问题按query文本在同一长视频上**均匀预取最多48候选帧**，用本机已有SigLIP余弦相似度选12个唯一帧（按PTS/时间确定稳定顺序）；若SigLIP不存在**不能换成随机选帧还叫query aware**。全程相同Qwen3-VL-4B-Instruct权重/量化/视觉输入分辨率、输出格式、system/user prompt模板、token上限、温度0或确定性解码、评分算法；只变帧采样策略，不能在prompt里暴露A/B标签、选择seed、答案或评测正确性。
4. 一段视频×2题×2臂=**最多4次Qwen真实模型前向**（先AB后BA冻结交错次序，避免顺序系统偏差）；B组查询相关候选提取/特征推理时延**另计**，不得因A与B都输12帧就把总计算称相同。**GPU总时间最多40分钟**，wallclock/VRAM peak/帧抽样与selection CPU+GPU成本每题每臂独立统计；**预先冻结2道题、实验配置与代码指纹**，单个调用STARTED即计费，超时/异常不重试、未完成纳入固定分母4。允许最多2次GPU warmup调用**仅如果用户后续专门追加授权**，默认0。出现GPU不稳定/模型载入超过时间门即STOP。
5. 实际媒体、标注QA、文本模型输入输出、答案、UID和S3路径/账号/用户路径/视频片段/帧截图及私人日志都不得进入公有Git、任何聊天和模型外部API。**尽量全程本机离线运行模型**，不将用户受保护开发题发送远端第三方。代码可在已有private实验树外的单次私有隔离脚本运行，旧锁/ledger/研究状态和历史Charades/REAL-PILOT不得重写。不用于训练，仅对已经获准的开发题做评测。科学结果以`n=2 questions,n=1 video`诚实报告，不能声称统计显著/发表结论，更不得把样本测试伪称完整HourVideo benchmark。

## 真实统计/验收

允许的结果状态：`SCORED_REAL_AB_PILOT_2Q_1VIDEO`（必须真正同版/PTS已证且答案评分可信）、`UNSCORED_REAL_VIDEO_SMOKE`（运行真实模型但不能验证版本桥接）、或`MEDIA_VERSION/MODEL/GPU_HOLD`。匿名记录固定分母2配对问题，成功/错误/invalid/失败/未开始各类别；2×2配对四格仅限实际可评分时计算。报告真实4次以内模型调用、完整框架成本与候选/选帧耗时、GPU分钟和峰值显存、A/B同权重同prompt判据、timebase与版本边界、失败阶段，不能公开任何问题原文或UID、具体答案、视频、样本索引或模型推理文本。**不从n=2题推断显著性、模型优劣或创新性**；`NOVELTY=RETAIN0`继续。

公有结果最多两处：新增`docs/codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/real-ab-pilot-receipt.md`与`docs/codex-results.md`末尾恰好一条`### VLM-HOURVIDEO-LIVE-AB-001`。如需要新增通用公开、不含受保护代码可在后续获得新增allowlist批准，本轮不擅自改源；避免向公有Git提交可重识别采帧时刻表/私有模型输出。核`git diff --cached --name-only`只这两路径，正常main push一次STOP。该初次真实实验可决定是否值得申请下一步≥12段视频×24道配对QA扩大规模，但**12段的视频下载预算/24题×2模型调用的GPU许可均须新批**。

## GPU训练接力（仅规划、不自动授权）

这轮是真实视频**冻结基线推理**，不是训练。完成后的独立后续链为[额外训练视频DATA](../VLM-EGO4D-LIVE-TRAIN-MEDIA-001/README.md)→[CPU训练准备](../VLM-HOURVIDEO-TRAIN-PREP-001/README.md)→[有限真实RTX3090梯度训练](../VLM-HOURVIDEO-TRAIN-GPU-001/README.md)，以及可选独立授权的[Qwen LoRA](../VLM-HOURVIDEO-TRAIN-LORA-001/README.md)。详细看[端到端训练路线](../../gpu-training-roadmap-2026-10-14.md)。训练样本与本轮冻结评测视频/QA严格隔离，不能为了训练偷用开发集答案；以上均非READY，需分别过门及用户授权。