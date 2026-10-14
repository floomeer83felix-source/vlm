# VLM-PD-LONGVIDEO-006｜源自490d247的可审计校验修复＋单次长视频A/B（唯一父任务）

**2026-10-14｜READY / USER_REQUESTED_CONTINUE_REAL_EXPERIMENT（唯一READY，独立新请求上限）**。用户此前多次要求继续真实GPU实验、尽量不重复逐步审批。本任务只对**同一**官方公开1920年电影做一次全新有界尝试，冻结媒体长度/网络/GPU总限制；不复活先前005已消耗的1/1元数据GET或其私人账本。**GitHub上READY本身不会启动用户Windows PC；仍须用户在原Codex长期对话发送一次执行指令。**

## 已知事实和导致阻塞的真正诊断缺陷

- [Codex 490d247](https://github.com/floomeer83felix-source/vlm/commit/490d247fb191a03890d9a4d7daf369416f8f26b8)：官方Commons元数据HTTP200、应用正文3,155B、一次请求用完；**仅ValueError而无具体字段/校验分支记录**，电影下载0、GPU0。无法从此前匿名账本倒推“授权不合格”或“360p不存在”；不得自行恢复同一005任务的旧额度。
- 2026-10-14重新独立核验[官方Commons《One Week (1920).webm》页面](https://commons.wikimedia.org/wiki/File:One_Week_(1920).webm)：连续影片标示24分26秒、美国公有领域声明，VP9 360p转码状态Completed、约338kbps。**该页面独立证据并不是此前API字段实测，也不表示全球所有司法辖区均公有领域；只允许使用许可实际适用于用户研究用途的素材**。需要新任务用官方API核准确标题、授权字段与唯一转码地址。旧源页面或早先的文件名预测不得替代本轮实际源身份校验。
- 本次必须修复关键的失败可解释性：新代码在**每个**JSON schema/页面/许可/衍生key/官方HTTPS URL门失败时使用**稳定脱敏枚举reason_code**，而不是只吐出异常类；将所处阶段持久fsync在**新私人**账本，可公开仅给原因代码，**不能上传原metadata、完整URL/路径、原日志或私有实验资产**。

## 新任务优先执行已经写入GitHub的可运行代码

- ChatGPT已提交[**`fetch_commons_diagnostic.py`**](./fetch_commons_diagnostic.py)。它在**网络前**执行`--selftest`内置正常例与4个反例，检查自身能输出明确分支；本机只能将GitHub公开源码复制到该父任务新私有目录，AST/离线自检通过后方可发请求。若仍有脚本小Bug可在**私有副本**离线修正并披露匿名类别，不改原历史文件、不得重发已消耗请求或绕开许可。
- 元数据仍仅**1次**`https://commons.wikimedia.org/w/api.php`官方`videoinfo` HTTPS GET（总应用body≤512KiB）；目标唯一`File:One Week (1920).webm`、要`derivatives|extmetadata|size|url`，`formatversion=2`，禁自动代理/重定向/隐藏HTTP重试。严格只认匹配标题、无API`error/warnings`、唯一videoinfo，结构化版权字段可证美国公有领域，唯一`transcodekey=360p.vp9.webm`且`src` HTTPS`upload.wikimedia.org`官方`/wikipedia/commons/transcoded/`路径；不允许从正文正则猜地址、替换另一影片/转码，不因独立网页有PD声明就忽视当前API矛盾证据。
- **通过所有源/许可门后**才最多1次官方视频HTTPS GET，MediaBody`ContentLength≤96MiB`、应用响应body累计≤96MiB，单段原子落盘到全新私有任务目录，EBML容器头校验。若ContentLength不可信、源URL/版权条件不符、请求异常或超时必须`HOLD`，不发第二次请求、不Range、续传或回头取原版132MB。**总网络数据操作≤2个HTTP GET（metadata1+media1）**、meta≤512KiB、video≤96MiB，不借用旧005/其他AWS额度、不声称TLS/wire总字节精确封顶；`fsync`记录新父请求前预扣，时钟使用单调秒，媒体阶段累计≤10min。
- 公开素材美国公有领域标识不构成对所有地区的法律保证；若具体使用地/研究使用许可不能合理确立或版权存在冲突，`SOURCE_LICENSE_HOLD`。不通过则0媒体GET。全部AWS/Ego4D/Charades/HourVideo视频请求、受保护QA读取、Qwen/SigLIP下载与模型服务均**0**。

## 真实长视频阶段（与metadata源门连续执行）

只有上述影片完整得到并用PyAV实测**真实采样帧≥350、PTS时间跨度≥1200秒**（且帧可解码）才运行现有已审查[长时双臂脚本`long_temporal_ab.py`](../VLM-PD-LONGVIDEO-005/long_temporal_ab.py)，调用固定命令`python long_temporal_ab.py --video <PRIVATE_NEW_TASK_DIR>/one-week-360p.webm --steps-per-arm 100 --gpu-minutes 12`。**只读复制公共源码到全新私有父任务目录并做离线AST**，只在私人运行副本上修复明显迭代时钟/显存/异常处理Bug；不修改GitHub公共研究代码，不进行第二个电影GET，不替换为先前5秒花朵素材或合成数据。

- 真正的时间预算：CPU解码抽帧≤10分钟，GPU两臂累计≤12分钟，前台全任务≤25分钟，均使用`time.monotonic()`；可用原Codex监督器必须经离线时区/UTC转换/子进程超时复核。若缺少安全可核硬时间门就在CPU/媒体前停止，不等待超时后误杀他人进程。
- 保持**对照公平**：同片前70%时间训练、后30%时间块验证并有9s间隔缓冲；均匀128 vs 运动优先128真实训练帧，相同验证70帧/160固定pair、同样24,705参数head种子/损失和AdamW学习率、每臂100真实`backward(); optimizer.step()`。显式本机RTX3090资源双快照free≥8GiB、util≤30%、任务互斥/确定冲突门，Windows C+G上下文列表非空不单独禁用；不杀进程/改驱动/环境。
- 每臂真实optimizer更新≤100，两臂合计≤200，GPU累计≤12min/新增PyTorch分配≤512MiB，禁新增依赖/权重下载/推理大型Qwen。训练失败/PTS不能证实即HOLD，不能用5秒短片、合成样本或旧HourVideo测试标签补齐。A/B指标记录训练首尾loss、真实更新数/参数变化、同一晚段pair准确率、样本时钟跨度及运行耗时；若只跑了A组，应标`AB_INCOMPLETE`，不得暗示配对实验已完成。
- **统计口径只限同一部1920无问答影片的时间顺序分类技术探索**，不是Qwen-VL/HourVideo正式QA准确率、不是第一视角长视频 benchmark、更不是证明采样方法优越或论文创新。保持`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`，HourVideo dev↔Ego4D版次/PTS仍UNKNOWN。

## 一次匿名交付和停止

只新增`docs/codex-artifacts/VLM-PD-LONGVIDEO-006/diagnostic-long-video-ab-receipt.md`及在`docs/codex-results.md`尾部恰好一条`### VLM-PD-LONGVIDEO-006`。报告阶段、精确枚举reason_code（若HOLD）、源校验分类/两次GET实际数与响应字节汇总、是否完整媒体/样本PTS≥20min、两组独立真实GPU步数/loss/后段准确率/耗时/框架峰值、隔离执行与安全资源门；严禁公开原API JSON/未知路径/原URL查询/原电影字节、帧/特征/模型/权重/checkpoint、私人SHA、凭据、原本机状态日志或进程身份。不得改ChatGPT-owned看板/总览/旧结果或旧005源码，不转运用户私有科研工作区。按正常main push一次后STOP、保留原Codex长会话，无自动后续任务。
