# VLM 真实Ego4D → RTX3090 GPU训练：一次性任务路线（2026-10-14）

**目标：一次性把剩余工作排到真实GPU梯度训练及可选Qwen3-VL LoRA，而不是在每个结果回来后重新起草合同。** 这是规划与任务串联，**不是批量AWS下载/GPU权限**，也不会自动唤醒原Codex会话。严格遵循`AGENTS.md`的**同时仅一个READY**、已结案任务不可重跑、每轮只提交一份匿名收据与`codex-results.md`末尾一条。所有受限制视频、原JSON/QA/UID/答案/凭据、训练中间产物和权重仅留私人本机。

## 完整阶段顺序

| 阶段 | 合同 | 当前状态 | 本阶段真实交付/放行条件 | 新独立授权 |
|---|---|---|---|---|
| 1 | [VLM-EGO4D-AWS-META-006](./codex-artifacts/VLM-EGO4D-AWS-META-006/README.md) | **已结案：完整清单/50 UID PASS，canonical来源HOLD** | 已完成90秒timeout的4,653,141B全文GET且50/50 UID命中；随后canonical来源规则HOLD，媒体HEAD0，未获得视频大小 | 已完成独立许可并安全结案：3/7 S3 attempts；未用4次不继承，0视频GET/GPU |
| 1b | [VLM-EGO4D-AWS-META-007](./codex-artifacts/VLM-EGO4D-AWS-META-007/README.md) | **已结案：45个安全来源候选、2个媒体HEAD200，1段≤3.5GiB** | a85e66a真实执行：50 UID中45个固定官方来源合规、5个隔离；两个媒体HEAD200，身份可锁，恰1个≤3.5GiB；S3 7/7，无媒体GET | 原metadata许可已执行并结案；不得继承旧7次额度，媒体GET/GPU仍未授权 |
| 2 | [VLM-EGO4D-LIVE-MEDIA-002](./codex-artifacts/VLM-EGO4D-LIVE-MEDIA-002/README.md) | **已结案：网络前LIVE_TRANSFER_ENFORCEMENT_HOLD** | [3ef8559](https://github.com/floomeer83felix-source/vlm/commit/3ef855983c879ac34852ff9382ed57620409fd85)报告0/8 S3，0真实视频、GPU0；合同要求对所有wire/TLS总字节精确hard cap而现有SDK未实现 | 本任务已关闭不可重跑或继承0/8余额；已由下一个新父任务包替代 |
| 2b | [VLM-LIVE-VIDEO-GPU-START-001](./codex-artifacts/VLM-LIVE-VIDEO-GPU-START-001/README.md) | **已结案：S3 8/8、单媒体GET200但只有64–128MiB part，GPU0** | [7cb9c6b](https://github.com/floomeer83felix-source/vlm/commit/7cb9c6b815614e7695be2edc251f87d4b002626c)外层PowerShell UTC时区误算，实际约54min提前终止；不是AWS拒绝或75min真超时，0完整视频 | 本任务STARTED/8次发送预算保留，不退款、不重新GET/Range；GPU训练未运行 |
| 2c | [VLM-LOCAL-GPU-REAL-SMOKE-002](./codex-artifacts/VLM-LOCAL-GPU-REAL-SMOKE-002/README.md) | **已结案：Windows混合GPU C+G上下文过严阻塞，CUDA0** | [8d724a7](https://github.com/floomeer83felix-source/vlm/commit/8d724a7d2d55a05ae178b6640be4bc384107bc51)系统显示3090空闲22,899MiB/3%但30个C+G上下文直接触发HOLD，torch未启动；partial解码未测 | 不重跑；不能把30个桌面混合上下文误称30个训练任务，改为下一任务小CUDA实测 |
| 2d | [VLM-WIN-CUDA-REAL-FRAME-003](./codex-artifacts/VLM-WIN-CUDA-REAL-FRAME-003/README.md) | **已结案：GPU_INFRA_PASS，真视频帧0** | [5ed644e](https://github.com/floomeer83felix-source/vlm/commit/5ed644e51702253539254890e1b62fd4c3a76e8a) RTX3090真实执行2次CUDA backward+optimizer更新，loss1.067→0.671；旧Ego4D.part经ffprobe缺moov，0解码帧 | 不需再做GPU基本兼容性验证；禁止原part续传/恢复 |
| 2e | [VLM-CC0-REAL-GPU-004](./codex-artifacts/VLM-CC0-REAL-GPU-004/README.md) | **已验收：真实公开视频GPU训练80/80步PASS** | [8299653](https://github.com/floomeer83felix-source/vlm/commit/82996532ace47e520f97e2ba7b59130525d4246e) MDN官方实拍视频1,128,375B完整下载，真实75帧/4.938s，RTX3090上24,705参数80个优化步、权重实变；后段同clip准确率0.5417 | 工程技术链证明通过，但无长视频、Qwen或独立科学验证；不能重跑004 |
| 2f | [VLM-PD-LONGVIDEO-005](./codex-artifacts/VLM-PD-LONGVIDEO-005/README.md) | **唯一READY：≥20分钟真实公开长片、固定双臂时序采样A/B** | Commons 1920公有领域连续影片官方360p转码、完整获取后PyAV验证≥1200s真实PTS；同训练帧预算128/臂 uniform vs motion-prioritized，固定模型初始化/验证pair，最多各100真实GPU优化步 | 源metadata HTTPS GET≤1/body≤512KiB，官方VP9转码GET≤1/body≤96MiB，GPU合计≤12min；不涉及HourVideo保护数据及Qwen正式推理 |
| 3 | [VLM-HOURVIDEO-LIVE-AB-001](./codex-artifacts/VLM-HOURVIDEO-LIVE-AB-001/README.md) | QUEUED | 冻结评测视频和2道dev QA，对照 uniform12 vs query-aware12、最多4次真实Qwen前向，保留配对分母与成本；同版/PTS未知仅UNSCORED | 需另批RTX3090模型推理≤40 GPU分钟 |
| 4 | [VLM-EGO4D-LIVE-TRAIN-MEDIA-001](./codex-artifacts/VLM-EGO4D-LIVE-TRAIN-MEDIA-001/README.md) | QUEUED | 训练集**不同视频/物理来源**，授权可用于训练；已有合法本地训练视频优先，必要时新获取一段，不能训练/测试数据污染 | 若远程取新训练视频，需另批最多6次官方metadata+媒体HTTP、单媒体GET≤3.5GiB、媒体正文≤4GiB |
| 5 | [VLM-HOURVIDEO-TRAIN-PREP-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/README.md) | QUEUED | CPU只读冻结数据分割、损失和模型资产资格；评测答案只在最终评分用，train上用自监督时序正负对；不做GPU | 需任务READY，**本阶段不含GPU/下载** |
| 6 | [VLM-HOURVIDEO-TRAIN-GPU-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-GPU-001/README.md) | QUEUED | **实际运行backward+optimizer.step，最多200步，≤60 GPU分钟，训练≤1M参数temporal head**，私有checkpoint，记录真实参数变化/损失/显存；Qwen/SigLIP主干冻结 | 需另批**GPU训练**额度，且CPU preflight PASS |
| 7（可选） | [VLM-HOURVIDEO-TRAIN-LORA-001](./codex-artifacts/VLM-HOURVIDEO-TRAIN-LORA-001/README.md) | OPTIONAL QUEUED / DATA HOLD | 若独立合法train QA及现存可行LoRA依赖/权重全PASS，才在3090上微调Qwen3-VL-4B适配器；否则不得用dev QA补齐 | 需另批具体GPU微调合同（提案：1 run / ≤100 updates / ≤90 GPU分钟） |

**阶段6是实质GPU训练**，不是只跑推理。阶段7是更进一步的Qwen主干适配器训练，数据与3090/Windows依赖前置目前为UNKNOWN，不能保证能跑；不能把阶段6的head训练冒充Qwen LoRA。若只有一个合法评测视频、没有独立训练视频，则必须停在训练数据门，不用评测/dev答案做训练以迎合进度。

## 科学口径与停止条件

- META-007证实50/50 UID、45个安全候选、两个媒体HEAD200且一段≤3.5GiB；3ef8559仅0/8请求。最新7cb9c6b才实际完成8/8 S3尝试、唯一媒体GET200并私有部分落盘64–128MiB，但**因UTC外层计时错误在约54分钟提前终止，完整视频不存在、GPU更新0**；旧预扣不复活。发布/剪辑/PTS桥接及Qwen本机权重仍未证；当前`NOVELTY=RETAIN0`，Charades `FINAL_MEDIA_STOP`持续。
- 实验链要可证伪：训练前AB作固定不调参基线，独立训练素材不泄漏dev标签；训练loss下降只证明优化正常，不证明问答提升、泛化、创新、统计意义或论文录用。**需要后续新批准的独立held-out评测**才能比较训练收益，不能看训练结果后挑dev问题和旧历史forward。
- 如无合法额外train QA，优先真实temporal head自监督训练，只能交`REAL_GPU_HEAD_TRAINING_COMPLETED`级别的工程证据；不得叫`REAL_QWEN_LORA_PILOT`。如有训练QA和可行依赖，再走阶段7，仍不承诺3090可容纳。
- 本轮Ego4D批准窗口按用户提供的有效期至2026-10-26，但前述AWS合同更保守地限制北京时间2026-10-25 23:59后不再发送新的数据请求。超过窗口不得凭旧审批重启AWS。
- 各阶段都要求显式上限、当前READY、无旧报告、原Codex会话新的执行消息；任何必要条件UNKNOWN都写`HOLD/NOT_RUN`，不可擅自翻版本、加数据、安装包、拉权重、改环境、重试、转移旧预算，亦不可持续后台执行。公开仓库只做文档交接，不推送原Windows实验工作区。

## 启动方式（不是自动连续执行）

截至2026-10-14，[8299653](https://github.com/floomeer83felix-source/vlm/commit/82996532ace47e520f97e2ba7b59130525d4246e)已通过首个**真实公开视频→真实帧→RTX3090 80步gradient工程链**；短片5秒数据不能冒充长期QA科学证据。**唯一READY=VLM-PD-LONGVIDEO-005**，已直接提交公开公有领域1920影片官方360p转码[≤96MiB受控下载器](./codex-artifacts/VLM-PD-LONGVIDEO-005/fetch_commons_long.py)与[长时均匀对运动优先帧采样两臂代码](./codex-artifacts/VLM-PD-LONGVIDEO-005/long_temporal_ab.py)，目标真实PTS≥1200秒、训练各100更新、GPU≤12分钟、同段晚期验证。这是无QA的公有领域电影探索，不自动升级HourVideo准确率/跨视频泛化或Qwen训练。用户在原Codex聊天一条启动，按许可、HTTP/PTS及安全门执行，不重新下载Ego4D、不触碰dev答案；一次匿名推送后STOP。每阶段真实回报审查并转下一个唯一READY后再由用户在同一聊天说“继续下一轮唯一READY任务”；媒体GET、GPU推理、GPU训练和模型LoRA都必须有对应明确授权后方可切READY。该机制避免反复起草后续合同，但不自动跨越权限或数据正确性门槛。
