# VLM-WIN-CUDA-REAL-FRAME-003｜Windows RTX3090 的真实 CUDA 梯度执行＋本机真实视频帧技术试跑

**2026-10-14｜READY / USER_REQUESTED_IMMEDIATE_GPU_EXPERIMENT（唯一READY，零 AWS/媒体下载）。** 用户持续要求“快点开始实验，不要每次问”。本父任务一轮前台执行，纠正上一轮[VLM-LOCAL-GPU-REAL-SMOKE-002](../VLM-LOCAL-GPU-REAL-SMOKE-002/local-gpu-smoke-receipt.md)在Windows上的过严`C+G`门，而不是重跑它：此前[8d724a7](https://github.com/floomeer83felix-source/vlm/commit/8d724a7d2d55a05ae178b6640be4bc384107bc51)仅发现RTX3090/总24,576MiB、空闲22,899MiB、利用率3%、30个Windows混合`C+G`上下文，其中19个常见桌面、11个未知；torch CUDA在进入前被拒，真实GPU更新0，part解码也NOT_RUN。**`C+G`不代表独占CUDA训练，不能仅凭驱动进程列表非空拒绝所有微小CUDA计算；反过来空闲快照不能当作排他独占或不存在竞争的保证。** 新合同用非破坏性、低显存、现场测量的实际分级限制。

## 执行顺序：CPU与GPU两个诊断相互独立，符合门才进入真帧训练

**0. 既有工作空间与唯一任务门。** 在用户原同一Codex长会话安全同步独立GitHub docs checkout main，重新阅读AGENTS.md、docs/next-steps.md、历史结果及本合同，确认唯一READY和本ID没有旧报告。私有`pytorch`conda、模型、媒体、旧part和历史预算/STARTED/监督器等绝不改写；不查旧科研树、下载目录或全盘；禁止新增pip/conda/驱动/权重下载、外部训练服务/后台自动作业。单调时间`time.monotonic`或`Stopwatch`计墙钟，**不能使用字符串/时区转换的UTC墙钟计时**。若任务已存在历史报告，STOP不重跑。

**A. 本地真帧CPU检查（与GPU检查独立，故CUDA HOLD也必须照样做A）。** 只沿上一轮视频下载任务已经确定的**一个私有、本人任务拥有的`.part`确切入口**（不得公开路径），只读确认普通文件、无reparse/symlink、不在公共git checkout、大小仍约64–128MiB且≤256MiB，并结合上轮只读状态判定原账本仍`STARTED/TERMINATED`、完整视频尚未产生；**不得改、复制、rename、合并、清理part或旧账本，不得使用Range/GET续传**。使用本机现有`ffprobe`/PyAV/OpenCV的CPU接口限量探测，单工具最多1次≤45秒，CPU阶段累计≤6分钟，总解码帧≤256，RAM≤512MiB；仅当至少32个**真实**解码帧、正且严格单调的实际帧PTS、足够时间窗跨度可核时得到`LOCAL_PART_FRAME_PASS`，否则`PART_NOT_DECODEABLE`/`FRAME_PTS_UNVERIFIED`，不能因为MP4缺moov就拼凑/重封装/假定内容。其性质永远为**部分媒体**，不能说`ONE_OFFICIAL_MEDIA_ACQUIRED`。只读单一本地备用真视频仅在此前明确已授权的**精确入口**和训练用途可证时允许，绝不搜全盘或触碰Charades FINAL_MEDIA_STOP素材。**A不成功不妨碍B小CUDA基础设施实测。**

**B. RTX3090实际CUDA基础设施实验（优先保证执行）。** 仅用户原本机、现有`pytorch`环境：先只读核公开约束内已有任务互斥/会话的命名对象，不触碰他人锁、驱动/进程；获取本任务自身新互斥（非阻塞，已有同一任务则STOP）。对单块目标3090分别读取两个间隔≥2s的`nvidia-smi`目标GPU utilization/free-memory快照及GPU进程类型元数据，**不因Windows的混合`C+G`上下文列表非空本身STOP**；也不动态扩充进程名单制造“空闲”。要求现场两次均`free_mem≥8GiB`、`utilization≤30%`、没有**已正面确认**运行中的冲突训练CUDA任务、现有本任务锁与公开约定保护锁无冲突，且用户本机未指定设备禁止占用。如果探测数据不可得、已知重任务活跃/排他锁冲突或门不通过→`GPU_RESOURCE_HOLD`。11个未知Windows`C+G`上下文**不单凭身份未知判为独占计算任务**；如有明确冲突证据才HOLD。任何情况下绝不杀进程、禁用桌面/驱动或解除外部锁。
- 条件成立时，**真的导入torch、调用`torch.cuda.is_available()`并实际在cuda:0上分配小张量、跑一个固定随机种子的线性层MSE**；≤2次`loss.backward(); optimizer.step()`、检查参数数值变化/finite loss与torch`max_memory_allocated`；GPU时间≤2分钟，新占用显存峰值≤512MiB。发现OOM、NaN、驱动异常立刻STOP、不清空全局缓存/不复试。结果只可标`GPU_INFRA_PASS`（硬件真CUDA更新），不能标正式视频研究训练。即便A失败也必须在B资源门满足时执行，不让“没有视频”继续挡住CUDA验证。

**C. 条件真实视频GPU研究技术烟测。** 只有A解出≥32真实帧与可信PTS、可证明该文件私人签署条款**允许此用途的研究训练**、数据使用与未来评测分离，以及B的CUDA/小张量真实更新PASS时才启动。用仅从真实帧CPU抽出的低维RGB/颜色分布特征、非QA原文/答案训练时间顺序预测的小型head；≤2层、可训参数≤100,000，固定seed单run、batch≤8、真正`backward()+optimizer.step()`≤100步（不含B至多2步）、GPU总累计≤20分钟（含B，CPU不算GPU时间）、任务新增GPU峰值显存≤2GiB；真实视频至少32帧严格PTS且训练/验证按连续时间块隔离。有其它CUDA作业开始竞争、OOM/NaN或训练用途不可确认立即STOP，不能转向全合成帧并冒充真实视频训练；若part解码失败则只报告B`GPU_INFRA_PASS`，`REAL_FRAME_TRAINING_HOLD`。旧part与账本仍只读。若part源来自HourVideo dev UID，此UID及同物理采集源以后**不能再作为held-out正式问答评测**；不能以同一训练曝光素材报告科学收益。无需本地Qwen/SigLIP权重且**严禁**模型权重下载或主干训练。本任务GPU训练成功只能标`PARTIAL_REAL_VIDEO_GPU_TECH_SMOKE`，非Qwen微调、长视频正式QA准确率、显著改进或科研新颖性通过。

## 预算、提交与STOP

- 本轮前台≤30分钟，GPU累计≤20分钟；**AWS S3 metadata/媒体GET/Range/续传/任何视频新下载0，网络模型/API/GPU云0**。无新依赖，旧实验目录/锁/账本/模型/长视频part不变，不重跑历史父任务。安全前检和可控小型CUDA张量试验由用户本轮“快点开始实验”和先前技术试跑上限覆盖，但不赋予更大GPU或模型实验。
- 最多一次A（有限本机媒体检查）、一次B（独立CUDA实测）、一次C（有条件100步真实帧head）。**C未过门不重开B**。单轮正常Git提交仅新增`docs/codex-artifacts/VLM-WIN-CUDA-REAL-FRAME-003/windows-cuda-real-frame-receipt.md`与`docs/codex-results.md`末尾**恰好一条**`### VLM-WIN-CUDA-REAL-FRAME-003`匿名结果。A/B/C分别报告实做/NOT_RUN、匿名资源门、CUDA分配与更新次数、真实帧/PTS可用性、真实视频head updates/loss/显存/时间；不得公开PID/进程命令行、UUID、私有路径/媒体/part、UID或其hash、QA/答案、AWS secret/manifest映射、视频帧、权重、checkpoint/私人脚本和完整日志。一次正常push到main后STOP、不连续运行任何QUEUED阶段，保持`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`与发布PTS桥接UNKNOWN。
