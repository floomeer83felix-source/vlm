# VLM-CC0-REAL-GPU-004｜真正的公开视频帧 → RTX3090 梯度训练，一轮完成

**2026-10-14｜READY / USER_REQUESTED_FAST_REAL_EXPERIMENT（唯一 READY；仅限本合同）；不是 HourVideo/Ego4D 正式 benchmark。** 用户多次要求尽快开始实验并表示不要反复确认。经[5ed644e实测](../VLM-WIN-CUDA-REAL-FRAME-003/windows-cuda-real-frame-receipt.md)，RTX3090 + torch 2.5.1/CUDA12.4 已**真正运行2次backward+optimizer.step**；历史Ego4D `.part` 已实测 `MISSING_MOOV`，真实可解码帧0，无法从它启动真视频训练。不能继续重复小合成CUDA测试或把残片伪装完整视频。本任务采用**另一份开放、许可来源可核、数量级仅几百KB至少于8MiB的真实拍摄短视频**完成完整工程链，以实证视频→解码/PTS→真实帧特征→GPU梯度的连接。此素材与HourVideo/Ego4D完全隔离，不代表第一视角长视频领域结果，不能拿其短片技术效果预测长时推理或科研创新。

## 唯一视频输入：MDN 公开共享资产

- 官方文档示例是开花实拍延时视频`flower.mp4`：固定 HTTPS URL `https://mdn.github.io/shared-assets/videos/flower.mp4`；来源 [MDN shared-assets 官方仓库](https://github.com/mdn/shared-assets)与[MDN HTML video 文档](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/video)；官方仓库接受的共享媒体需 CC0 或开放许可，原实例旧路径带 `/cc0-videos/flower.mp4`；参见[MDN 许可说明](https://github.com/mdn/shared-assets/blob/main/LICENSE.md)。执行前**CPU 零视频请求**仅核固定来源及许可不冲突。只在用途确认允许研究训练时执行；如果无法证明，记录 `SOURCE_LICENSE_HOLD`，不能换不明第三方镜像或取用户受保护媒体。
- **一次且至多一次普通 HTTPS GET**从**唯一域名`mdn.github.io`及固定完整路径**，不使用AWS/S3/profile或用户私有云配额。不发送HEAD探测/Range/重试；TLS验证、HTTPS、禁proxy继承、15秒连接与30秒读超时。开始请求前独立fsync持久`STARTED`，声明应用响应正文最大**8,388,608 B (8 MiB)**，若ContentLength可得必须≤此值；逐块≤64KiB流式读+硬上限校验，HTTP必须200、无内容编码/跨站重定向，不信服务器无限长度。链接有重定向至其他host则拒绝跟随；只能保存到**本父任务私有新目录**的专有`.part`，完整200响应正确结束、内容长度/原子rename后才视为视频完整。实际物理TLS/wire流量与应用body不同，不伪造严格wire流量上限。网络不通或超过限额则STOP、**不换视频或再GET**；不会替换为合成数组、旧Ego4D残片、Charades或HourVideo受保护视频。私人完整视频不会提交到GitHub。
- 下载之前先只读检测**已经由本任务归属且来源证据完整的同一CC0输入是否存在**，若存在安全复用，不额外请求。不可枚举用户 Downloads 或其他研究目录；若不存在才使用上述唯一小文件GET；本轮所有其它媒体/模型下载=0。保存文件私有SHA-256与来源许可证据，公共结果可仅记录`SOURCE_MDN_CC0`、下载字节范围与`LICENSE_PASS/UNKNOWN`。

## 真正可运行的训练程序已经在GitHub

- [`temporal_train.py`](./temporal_train.py)是**ChatGPT 已提交的真实可审查Python执行代码**（不只是路线合同）。Codex仅在自己的独立私人试验目录拿到这一份固定源码并由既有`pytorch`环境调用，例如 `python temporal_train.py --video <PRIVATE_LOCAL_CC0_VIDEO_PATH> --steps 80 --gpu-minutes 10`；脚本没有网络功能、不读取HourVideo QA、无权重下载与检查点输出。绝不能在公共Git目录创建敏感视频、`__pycache__`或私人训练日志。调用前在自己的私人运行目录AST/py_compile单次离线检查；遇明显缺陷可在**本轮私人副本**内安全修正（需匿名报告修补类别），公共源码不得由Codex修改。
- 真实PyAV解码帧/PTS严格递增后，将最多96帧按本身解码时间抽样，用OpenCV把**真实**RGB帧缩为8×8×3，按前75%与后25%**同视频不重叠时间块**分训练与小验证。CUDA上固定seed单个(384→64→1)二分类时序先后head，用真实帧特征构成顺序/倒序pair完成**≤80次真正的`backward()+optimizer.step()`**；trainable参数<100,000，模型权重全随机仅小head，GPU累计训练≤10分钟、训练分配峰值≤512MiB，私有CPU临时新增≤256MiB。不得假装Qwen/SigLIP前向或跨视频泛化。
- GPU使用已验证[5ed644e](../VLM-WIN-CUDA-REAL-FRAME-003/windows-cuda-real-frame-receipt.md)的**Windows混合C+G不等于独占计算进程**判据：在单轮两次≥2秒间隔只读free≥8GiB、util≤30%、已知命名互斥/外部明确冲突计算任务0的前提下，取得本任务自身非阻塞互斥后才能跑。不能杀任何用户进程、清别人的锁、改驱动/CUDA/conda、开云GPU。运行时time.monotonic上限≤10 GPU分钟（加必要CPU/下载本轮前台总≤25分钟），失败STOP、不重试训练或再下载。

## 必须交付真实更新，不冒称研究性能

- 只有**文件完整且PyAV真实解码≥32帧、PTS递增并跨≥1秒、有限实际训练loss、非零参数变化、至少1次真实CUDA optimizer.step** 才可称 `REAL_CC0_VIDEO_GPU_TECH_SMOKE`。上传脱敏报告聚合：源合法性/精确客户端应用下载总量或区间、完整容器/解码数量、时间跨度、梯度步数、参数变化、loss首尾、框架峰值显存、训练时间及同视频时间块验证准确率（**仅工程诊断**）。如源视频不存在/许可未知/解码不及门/GPU忙则逐项报告原因而不调用合成fallback。
- 不进行HourVideo开发集问答推理或得分、Ego4D video_UID映射、真人身份读取、训练/测试混用；当前正式独立训练媒体和HourVideo v1/v2 PTS桥接仍未知；`NOVELTY=RETAIN0`，Charades`FINAL_MEDIA_STOP`。**真实视频训练技术链完成后，也不能当做长视频VLM论文实验成功**。后续长视频和Qwen实验仍需要合规的独立真实训练素材、模型资产/版本时钟桥证据。
- Codex**只提交两处文件**：新增`docs/codex-artifacts/VLM-CC0-REAL-GPU-004/real-cc0-gpu-receipt.md` 与`docs/codex-results.md`末尾唯一`### VLM-CC0-REAL-GPU-004`。不得上传视频帧/片段、模型/权重/特征、私人绝对路径/账本/原日志、旧Ego4D UID/桶/key/凭据。正常push main后STOP，不执行QUEUED后续训练，不在后台运行，原同一Codex聊天保留。整个父任务执行只需用户在原Codex长期会话触发**一次**，无需为同一小公开GET和本机技术训练阶段分别询问。
