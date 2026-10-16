# VLM-TRAIN-HEAD-HARNESS-019｜一次交付可运行的离线时序头训练骨架（纯合成 CPU）

**2026-10-16｜唯一 READY / CODE_AND_SYNTHETIC_CPU_ONLY。** 018 已在 [0084d0b](https://github.com/floomeer83felix-source/vlm/commit/0084d0bbc1e76ce39c6ef1339ed5cb64eabb1434) 结案；ChatGPT 根据用户同意转向实际训练，把本项设为先行工程任务。**本 READY 只允许改公开文档 checkout 中列出的源码、对程序生成的合成特征做受限 CPU 自检；绝非真实视频、保护标注、模型权重访问、训练 GPU 或媒体下载许可。** Codex 必须在用户于活跃 Codex 聊天发来新执行消息后，安全同步 main、复核 AGENTS/任务状态和唯一结果条目，再执行；单次正常 push 后 STOP。

## 科学目标与反证逻辑

- 冻结一个最小实验目标：对预计算的视觉帧嵌入序列，通过**不直接输入绝对或相对时间戳**的两帧特征组合预测「短时间邻近」vs「远时距」，标签仅由**训练视频内部 PTS** 生成；训练头输出连续logit，不读取文本 QA、任何 gold、历史预测、dev 答案或评测视频。此为**自监督技术代理目标**，不能宣称新机制、真实事件先后推理或问答收益。
- 预备两类对照：相同架构与参数的未训练随机头；在冻结特征、训练时长、优化器与正负样本数下打乱训练邻近标签的负对照。只有未来真正获得合法、独立训练素材与新 GPU 授权，才可在**训练视频内部不重叠时间窗**实测二者；要声称长视频 QA 收益还需另行冻结独立 held-out 来源的问答评测，不可用 013–018 的 gold 训练、调参或选择 checkpoint。
- 时间可作生成训练 pair 的标签依据，但禁止把时间位置、pair采样ID或相邻抽帧索引当预测特征。冻结 source-group 划分接口，显式阻止已知重叠来源进入 train/held-out；未知物理来源独立性为 HOLD 而非 PASS。相邻帧视觉高度相似也可能是捷径，需在以后真实数据解释中留作 confound；此轮只验证代码合同。

## 本轮一次性执行包（按顺序，能独立完成的子项继续）

1. **原有资产只读定位（仓库内）**：仅查看 public repo 的现有相关 Python 原型和本 README 引用的训练合同：[TRAIN-PREP-001](../VLM-HOURVIDEO-TRAIN-PREP-001/README.md)、[TRAIN-GPU-001](../VLM-HOURVIDEO-TRAIN-GPU-001/README.md)、[009现有长视频技术记录](../VLM-LOCAL-LONGVIDEO-009/README.md)。不读取任何私有媒体/路径/QA/答案/配置，也不因历史009使用过某视频就默认它具有新训练授权。禁止遍历原Windows研究工作区。
2. **实现唯一真实代码交付**：创建 `prototypes/vlm_train_head_019.py`：纯函数的单调实PTS校验、含来源组的train/validation隔离断言、严格确定性的邻近/远距 pair 构造和二分类均衡、仅视觉特征输入的 ≤2 层、参数≤1,000,000 temporal-pair head、AdamW CPU-only训练循环以及每次调用上限/finite loss/梯度/更新参数确证。不允许打开媒体或联网；输入为调用方直接传入的匿名数值数组/张量，不能按目录/UID搜索。代码必须有明确运行模式 `synthetic_cpu_only`，不能因载入模块而执行训练。没有显式安全模式则 fail closed；不设置任何绕过 GPU gate 的捷径。
3. **实现唯一合成测试交付**：创建 `prototypes/test_vlm_train_head_019.py`，只在固定 seed 构造的小型合成 embedding+PTS+来源组上运行。覆盖非递增/缺失PTS、空类别、时序极端边界、训练/验证时间窗泄漏、来源组泄漏、QA/gold字段拒绝/不进入前向、未训练与乱标签对照接口、预算封顶、参数确实更新、骨干无梯度、异常立即STOP，以及结果种子重现（如环境允许）。最多**16 个合成样本、每个试验≤12 CPU optimizer updates、整个套件CPU用时≤120秒**，不因GPU可用而使用GPU。用既有本地 Python/Torch；若PyTorch缺失，不能pip/install/download，只运行纯stdlib结构与安全门测试，明确 torch-specific SKIP 而非假装训练成功。
4. **冻结下次真实训练的接口合同而不运行**：文档写明真正进入 [TRAIN-PREP-001](../VLM-HOURVIDEO-TRAIN-PREP-001/README.md) 还需：用户另外提供确切已获训练许可本地视频入口和来源/物理隔离证据、CPU资格PASS、训练/评测源及时间窗映射冻结；进入[TRAIN-GPU-001](../VLM-HOURVIDEO-TRAIN-GPU-001/README.md)还需新的明确GPU许可，拟≤200步/≤60 GPU分钟、head≤1M、batch≤8、grad accum≤4、checkpoint≤256MiB、研究临时新增≤2GiB。旧GPU/媒体预算不能继承，不读取任何 013–018 gold 作为调参信号。电影或既有视频若未来被允许用于训练，须注明与Ego4D分布差异，不能凭模型代理loss证明HourVideo QA效果。

## 绝对禁止项与资源封顶

- **GPU/CUDA计算、模型推理/Qwen/SigLIP加载、真实视频抽帧与解码、打开私有数据/路径、AWS或网页研究下载、依赖安装、环境修改、后台任务、任何已有旧实验重跑：全部0。** 公共文档 checkout 的git fetch/push只用于代码协作，不算研究联网。
- CPU自检合成数组上限16条，测试进程硬超时120秒（要有安全监督；否则仅做安全静态检查），CPU真实optimizer updates总计≤12（各控制组单次可更小；不能用多个case绕过该总量），输入嵌入维度≤32，内存新增≤256MiB；无新checkpoint或受限资产落盘。若已有PyTorch只强制CPU；不得 `.cuda()`、`to("cuda")`、隐式自动设备选择或动CUDA显存。
- 所有公共提交仅限这份 README 已由ChatGPT预写、Codex新建的**两份** `prototypes/` Python 文件、`docs/codex-artifacts/VLM-TRAIN-HEAD-HARNESS-019/synthetic-cpu-harness-receipt.md` 与 `docs/codex-results.md` 末尾**恰一条** `### VLM-TRAIN-HEAD-HARNESS-019`。既有README不改、历史结果不覆、ChatGPT-owned next-steps/overview不碰。不提交私人来源身份、路径、QA、gold、embedding、模型、token、凭据、视频或原实验账本。
- 如安全限制或所需旧依赖不满足，明确 `SYNTHETIC_CPU_HARNESS_PARTIAL/HOLD`，保留已能安全完成的源码/纯std测试，不调整约束、不开GPU、不得新建后续父任务。

## 验收输出与停止

匿名收据必须有：源代码/合成测试通过或明确SKIP数、每种安全门测试结论、合成CPU实际更新数/是否真实 head 参数变化、CPU wall 与资源上界、对照输入/随机种子固定方式、train/eval隔离断言、哪些真实数据/训练环境仍UNKNOWN、对应下一阶段的明确 STOP/GO 必要条件。只有合成CPU运行通过才是 `TRAIN_HARNESS_SYNTHETIC_CPU_PASS`，不是 `TRAIN_CPU_PREFLIGHT_PASS` 或 `REAL_GPU_HEAD_TRAINING_COMPLETED`。GitHub普通main push一次，STOP等待ChatGPT审查；不得自动执行 TRAIN-PREP 或 TRAIN-GPU。科学结论始终 `NOVELTY=RETAIN0`、`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`，Charades `FINAL_MEDIA_STOP`。
