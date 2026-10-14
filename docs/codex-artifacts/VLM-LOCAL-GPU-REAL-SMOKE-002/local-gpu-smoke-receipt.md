# LOCAL-GPU-REAL-SMOKE-002：GPU上下文占用未能排除；CUDA与真实视频训练未执行

2026-10-14（北京时间）。**GPU_INFRA_HOLD / GPU_OCCUPANCY_UNRESOLVED**。首个基础设施执行器返回GPU_OCCUPIED_HOLD_COMPUTE_PROCESS：发送任何CUDA操作前，驱动进程查询发现已有GPU上下文，因此拒绝继续。后续仅只读核实目标设备和进程类别，没有重试CUDA。**本轮CUDA张量分配、backward、optimizer.step均0，未得到GPU_INFRA_PASS；B/C均NOT_RUN。**

## 启动与执行边界

独立公有docs原工作树干净，安全fetch/fast-forward main `7f559ce`，重新读取AGENTS、最新任务板/结果/总览、本任务README及上轮匿名收据，确认唯一READY为本父任务且无旧回报。使用现有pytorch环境，未修改Python/Torch/CUDA/PATH或安装依赖。新私人任务目录仅保存本轮代码、匿名计数与只读诊断，不触碰旧文件或STARTED预算。

优先A的单次执行器在网络审计阻断下运行：先只读检查此前已知的GPU OS命名互斥量是否存在，再取得本任务自己的互斥量、查询GPU计算进程；已有进程即拒绝CUDA。检查时已知命名对象不存在，本任务创建的对象在finally释放并关闭自己的句柄。没有解锁、删除或结束任何他人任务，也没有读取未知文件锁/原实验树。不能由此宣称全机所有可能的文件锁已检查。

因占用门在torch导入和CUDA初始化之前拒绝，本轮没有实际验证CUDA可用性、设备张量或梯度；前台执行器正常返回HOLD，不是训练成功或CUDA报错。用户授权明确存在，没有请求逐阶段重新批准。

## 实际占用证据与证据限制

在不运行CUDA、不读取媒体的前提下，对目标device index 0进行有限只读nvidia-smi核查。原始GPU设备ID/UUID、进程ID、完整进程名称/命令行均不公开。

| 项目 | 实际匿名结果 |
|---|---|
| 目标设备类别 | RTX3090 |
| 设备总显存 | 24,576MiB |
| 一次只读空闲显存快照 | 22,899MiB，约22.4GiB |
| 同时读到的利用率 | 3% |
| 目标进程查询条目数 | 30 |
| XML进程类型 | C+G 30；没有由此确认纯CUDA训练任务数 |
| 进程名元数据的有限分类 | 19个识别为常见桌面上下文；11个未分类；按既定名称模式识别出的常见计算应用0 |
| 读取进程命令行/数据内容 | 0；仅本轮已列出的有限PID对应名称元数据 |
| 结束已有GPU进程 | 0 |

**30个C+G不能等同于30个模型训练任务。** Windows混合图形/计算上下文、低利用率和充裕显存不足以单独证明排他空闲；0个命中常见计算程序名称也不证明没有冲突CUDA任务。11个上下文身份/活动用途仍未分类，不在执行中临时扩充桌面白名单来制造通过。

初始代码把非空计算进程列表作为保守拒绝门；补充只读诊断明确暴露了该门在混合上下文下的局限。最终应报**占用范围未排除**，不报GPU坏了、显存不足、torch.cuda.is_available=False、OOM或已证某个真实训练正在运行。CUDA的用户目标在本轮未实测完成。

## A/B/C实际执行计数

| 子阶段 | 本轮结果 |
|---|---|
| A已知OS互斥量与进程前检 | 执行；占用门HOLD，自己的互斥量已释放 |
| torch导入/CUDA可用性查询 | NOT_RUN / NOT_RUN |
| CUDA张量分配 | 0 |
| 基础设施forward/backward/optimizer更新 | 0 / 0 / 0，未使用≤2更新配额 |
| 本轮GPU试跑时间 | 0秒；nvidia-smi仅驱动状态查询，不作为GPU训练时间 |
| 任务峰值新增显存/有限loss/参数变化 | NOT_RUN；不把设备显存快照当任务峰值监测 |
| B旧part普通文件/大小/账本/SHA核验 | NOT_RUN；仅引用历史64–128MiB事实，未假称本轮再次验证 |
| B前缀/ffprobe/PyAV/OpenCV/真实帧/PTS | 全部NOT_RUN；不能认定缺moov或可解码 |
| 本地备用真实视频入口查找 | 0；没有扫描旧研究树、Downloads或全盘 |
| C真实视频梯度更新/训练 | 0 / NOT_RUN |
| 训练许可/时间窗/未来held-out排除核验 | NOT_RUN；未触碰原排除标记 |
| Qwen/SigLIP/外部模型/权重/checkpoint | 全部0 |

本合同A无法安全运行CUDA时要求父任务停止，因此未越级读取part或用合成张量冒充真实视频训练。不存在PARTIAL_REAL_VIDEO_GPU_TECH_SMOKE或LOCAL_REAL_VIDEO_GPU_TECH_SMOKE结果。

## 资源、隐私与交接

所有本轮限时准备采用time.monotonic，未用ISO/Git时间字符串计算经过时长。未触发任何进程超时终止或GPU时间上限。只建立一次A执行标记、未再次启动CUDA执行器；无后台任务。私人新增仅少量代码/聚合JSON/私有进程元数据，未创建媒体副本、特征或checkpoint，低于256MiB；旧part、8/8及STARTED/TERMINATED账本、旧监督器记录均未读写或退款。

AWS认证/S3/HTTP视频请求/GET/Range/续传、视频或权重下载均0；无GPU云/付费服务/新依赖/驱动或环境更新。授权Git文档同步与推送不称作所有互联网通信0。原JSON/QA/答案/UID/媒体URI、原部分视频与账本、真实帧、私有路径/哈希/进程ID/原日志或代码均不上传。

需要ChatGPT审查混合C+G上下文的占用判据，明确哪些显示上下文可证明不构成冲突、哪些真实CUDA任务必须等待；或由用户在本机确认设备可用于试跑后冻结新的任务。**本轮不自行退出系统应用、杀进程、放宽规则或重试本ID。** 只提交本收据及codex-results末尾一次记录，正常main push后STOP并保留聊天。不执行排队Qwen A/B、真实训练或其它任务。NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP、RELEASE_AND_CLOCK_BRIDGE_UNKNOWN保持。