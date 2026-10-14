# VLM-HOURVIDEO-TRAIN-LORA-001｜可选Qwen3-VL-4B参数高效微调真实训练门

**2026-10-14｜OPTIONAL_QUEUED / REQUIRES_TRAIN_QA_DATA_AND_NEW_GPU_AUTHORIZATION（非READY）**。此项是用户关心的**Qwen模型本体训练**候选，区别于TRAIN-GPU-001的真实小头训练。不能因为前一个头训练PASS就自动获得训练Qwen权限；若合法training QA、现有可用LoRA/QLoRA依赖或RTX3090可行性缺失，必须`LORA_HOLD`，无猜测下载，不替换模型。
 
1. **数据先过门**：至少有一份授权用于训练的独立train split，真实训练视频与训练问题/答案的使用许可明确；任何HourVideo dev_v1.0保留QA以及AB-001的评测QA、错误样本与答案不得进入训练、模型选择、prompt、teacher/伪标签、优化指标。必须有视频级/采集源级holdout并冻结合法validation split；完全没有训练监督时不能用dev答案填坑，此任务维持QUEUED/HOLD。
2. **工具和资产先过门**：本机现有Qwen3-VL-4B-Instruct、PyTorch/CUDA、可用PEFT/量化训练依赖和3090 24GiB显存是否真正能完成完整反向传播须先只读核验；不得pip装包、拉模型权重、改Torch/CUDA/driver或切付费云机。若4B全参数训练难以容纳3090，绝不尝试无界full fine-tune；仅允许既有合法LoRA/QLoRA。不得假设Windows下量化组件自动可用。
3. **未来需要单独批准具体资源合同才能转READY**：建议1次run、≤100 optimizer updates、≤90 GPU分钟、microbatch=1、梯度累计≤8、仅适配器参数可训练、私有adapter checkpoint≤512MiB、私有新增临时产物≤4GiB、无额外网络GET和外部API。失败即STOP、无自动重试；全程记录step/loss/VRAM/time及参数更新和异常，严格无dev答案泄漏。用户许可前这只是**上限提案而非执行许可**。
4. 即使训练成功，只能回报`REAL_QWEN_LORA_PILOT`与可验证的真实优化步数。无保留验证、公平对照、足量样本则不能宣称研究改进或论文贡献。

若获得上述证据并由ChatGPT/用户另批，Codex按唯一READY合同只交新增`docs/codex-artifacts/VLM-HOURVIDEO-TRAIN-LORA-001/qwen-lora-training-receipt.md`和`docs/codex-results.md`末尾一条，绝不上传权重、adapter、训练QA、媒体、特征、日志、密钥、私有路径。一次push后STOP。不继承TRAIN-GPU-001预算。
