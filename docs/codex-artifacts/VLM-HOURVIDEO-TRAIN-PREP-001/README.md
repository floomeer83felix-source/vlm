# VLM-HOURVIDEO-TRAIN-PREP-001｜真实训练前CPU资格、冻结实验目标与泄漏审查

**2026-10-14｜QUEUED / 未授权执行，非READY。** 在真实评测视频A/B收据与独立训练视频的合法来源/实际存在经审查后，才可转READY。此轮CPU只读+私有最小配置工作，不做GPU调用、解码受限数据之外的素材或训练，不安装依赖、下载模型/视频。用户须在原同一Codex会话触发。

## 不把工程可跑当成论文结果

1. 在原Windows RTX3090/64GiB现存环境**只读**审查PyTorch/CUDA可用标志、现有SigLIP/Qwen3-VL-4B模型权重/处理器、显存空闲及磁盘可用空间，不移植/升级conda环境、不打印私人路径、无GPU计算。不能保证RTX3090能加载或微调Qwen，不能把所需环境缺口隐式授权为pip或下载。
2. 核实真实**train-video 与 evaluation-video 在物理素材/采集源/UID/分割上隔离**、允许训练用途。冻结hold-out开发QA及已有AB-001结果，答案只用于最终评分，不可给优化器、蒸馏teacher、损失或挑checkpoint。若有独立官方train QA/说明，核实实际训练许可和train split；不批准额外标注获取。否则优先冻结 **TRAIN_HEAD_SELF_SUPERVISED**：仅在训练视频上构造时间邻近正对/远时间负对的自监督目标，训练一个小型temporal head（冻结既有视觉编码器和Qwen）；不把这种代理损失宣称为问答质量优化或长视频VLM机制创新。
3. 冻结单次运行合同：固定可核任务输入和train/validation时间窗（validation也是**训练视频内部**的非重叠时间窗，绝不用保留评测视频调参）；head结构≤2层、可训练参数≤1,000,000、随机种子固定、优化器AdamW、最多200步、batch≤8、梯度累计≤4、checkpoint上限≤256MiB、GPU训练总时间上限拟60分钟。正式数值须在GPU前另行授权，不是本CPU预检默认许可。loss曲线、分割/依赖、回滚与异常处理在私有配置中冻结，OOM/NaN/低空间/已有GPU任务冲突立即停止，不允许自增额度或杀其它进程。
4. 若存在合规独立**training QA**和实际可用微调软件，另记录`QWEN_LORA_CANDIDATE`，但严禁在本轮下载权重、建立量化依赖或执行LoRA；[TRAIN-LORA-001](../VLM-HOURVIDEO-TRAIN-LORA-001/README.md)是独立可选后续。若没有合规训练标签，就明确标`QWEN_LORA_DATA_HOLD`，不拿dev答案冒充训练资料。
5. preflight只得在限定已知私人目录读取必要元数据和代码接口，不搜索全盘、不重跑历史实验/QA、不得修改既有科研目录、训练ledger或删锁；所有私有信息不上Git。

## 公共输出

仅新增`docs/codex-artifacts/VLM-HOURVIDEO-TRAIN-PREP-001/cpu-training-readiness-receipt.md`和`docs/codex-results.md`末尾一条：给出任务模式、自监督是否可定义、实际素材分割证据等级、现有环境/权重可用性布尔、最小训练设定、资源预估、独立评测隔离、风险与STOP条件。通过只得到`TRAIN_CPU_PREFLIGHT_PASS`，**不表示GPU/训练已获许可**。推送一次即STOP，移交[TRAIN-GPU-001](../VLM-HOURVIDEO-TRAIN-GPU-001/README.md)。
