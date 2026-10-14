# VLM-HOURVIDEO-TRAIN-GPU-001｜RTX3090第一轮真实梯度优化：有限自监督temporal head

**2026-10-14｜QUEUED / REQUIRES_EXPLICIT_GPU_TRAINING_AUTHORIZATION（非READY，不得执行）**。本合同是**真实GPU训练**而非GPU推理或CPU合成测试的预排阶段。必须先有已获授权的独立训练视频、数据隔离/训练用途证据、TRAIN-PREP-001实际PASS、RTX3090现有组件和用户**另行明确批准最多60 GPU分钟、最多200个optimizer updates**，ChatGPT把本项切为唯一READY，用户在**原Codex长会话**主动触发；否则0 GPU。前序MEDIA/AB所批次数、字节或GPU预算均不可继承。

## 训练目标、方法和上限

- 用训练视频的真实帧时间信息构造`TRAIN_HEAD_SELF_SUPERVISED`正负对（邻近vs远距离/时间扰动），基于**已在本机存在**的SigLIP等冻结视觉特征编码器，训练一个≤2层、≤1,000,000个可训练参数的temporal scoring / projection head。允许训练数据的真实帧解码与本地特征提取仅在本任务已批准的视频、时间窗和GPU总额度内；Qwen3-VL与视觉主干冻结，不以dev QA/正确答案/测试模型输出指导梯度。允许原有代码与软件栈，不安装新包、下载模型或更换GPU。**这确实执行backward+optimizer.step并核参数变化，但不是Qwen主干微调，也不等于论文机制或QA提升**。
- 仅一次冻结seed/数据切分/配置的完整run，max optimizer updates **200**、batch≤8、gradient accumulation≤4、最多60分钟RTX3090 GPU累计占用（包含特征编码、训练和无QA验证）、输出checkpoint≤256MiB、临时私有产物总新增≤2GiB、最多1个最终checkpoint（保留私有）、额外下载字节0、外部API/云GPU0。冻结的train-validation仅在独立训练视频的互斥时间窗；评测保留视频不用于训练/选checkpoint或调参。若预冻结配置难以执行则STOP而不是改seed/扩大样本/任意重启。
- 训练前要求独占可用设备且没有与他人GPU任务冲突；不终止/暂停他人进程，不改原conda pytorch/CUDA/Torch，不动旧科研账本/锁。安全失败关闭：OOM、NaN、失配、缺本地权重、时钟不可信、丢媒体、缺权限、超时、显存安全不足即STOP。持续记录实际steps、loss finite、参数数目/前后hash变化、GPU时长、峰值VRAM及是否走到了optimizer.step，不让异常后继续重试训练。
- **结果层级严格区分**：若真实数据+真实GPU+参数变化皆有证据为`REAL_GPU_HEAD_TRAINING_COMPLETED`；不足为`GPU_TRAIN_HOLD/PARTIAL`。不报告“Qwen已训练”、基准准确率提升、泛化性、科研创新或统计显著性；后续评估需独立许可且冻结模型与原AB基线公平复核。

## 交付

公共仅新增`docs/codex-artifacts/VLM-HOURVIDEO-TRAIN-GPU-001/real-gpu-training-receipt.md`与`docs/codex-results.md`末尾一条：按匿名聚合记录真实数据与设备、训练更新数、参数变化、损失始末、GPU分钟、峰值显存、失败与完整性门；**模型权重/checkpoint/视频/帧/特征、UID/QA/答案、源路径、个体样本日志、账号秘密一概不上传**。只可在本任务新私人目录保存checkpoint。一次main push后STOP。若要微调Qwen主干只能走另行批准的[TRAIN-LORA-001](../VLM-HOURVIDEO-TRAIN-LORA-001/README.md)。
