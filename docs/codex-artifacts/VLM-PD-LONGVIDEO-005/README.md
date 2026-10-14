# VLM-PD-LONGVIDEO-005｜首个≥20分钟真实长视频与RTX3090等预算时序采样A/B（单轮）

**2026-10-14｜READY / USER_REQUESTED_CONTINUE_REAL_EXPERIMENT（唯一READY；只涵盖本有界公开数据与单轮GPU A/B）**。用户反复要求尽快实验且“不每次问我”。在[8299653](https://github.com/floomeer83felix-source/vlm/commit/82996532ace47e520f97e2ba7b59130525d4246e)中，上一轮MDN CC0公开5秒视频成功完整GET1,128,375B、PyAV 75帧/PTS4.938s、RTX3090 **80/80个真实optimizer更新**、24,705参数非零变化。这已完成一段短视频真实GPU技术链，但同clip验证只有54.17%，不能说明长视频或Qwen/HourVideo效果。**禁止重跑004或再把5秒视频冒充科研数据。** 本轮优先研究真实≥20min的时间跨度与相同训练算力下*均匀帧抽样 vs 运动优先采样*，但仍是一段非第一视角、无独立问答标注的公共影片，**不是HourVideo准确率、VLM问答比较或独立影片泛化证据**。

## 固定真实公开片源与可审核身份

- 仅 [Wikimedia Commons 官方公有领域电影《One Week》(1920)](https://commons.wikimedia.org/wiki/File:One_Week_(1920).webm)。页面记录来源公开、发行于1920年、**原片持续24分26秒、美国公有领域**，官方WebM原版132.11MB；官方TimedMediaHandler已提供较低码率的**VP9 360p 338kbps 转码**。本实验只允许这个固定**360p.vp9.webm**衍生版本，严禁下载132MB原版或其它候选、近似名称、镜像/视频平台/额外私有用户媒体。用户不需要自行寻找或上传任何源视频。
- 固定官方MediaWiki GET API（**一次**）`https://commons.wikimedia.org/w/api.php`，参数`action=query&format=json&formatversion=2&prop=videoinfo&viprop=derivatives|extmetadata|size|url&titles=File:One Week (1920).webm`（由`urllib.parse.urlencode`构造）。仅从唯一file title的`videoinfo[0].derivatives`读取**exact`360p.vp9.webm`**且extmetadata必须可证明Public Domain标记；若文件源、许可、衍生key或响应不可验证，**0视频GET，立即STOP**。固定衍生URL主机必须HTTPS`upload.wikimedia.org`且路径是`/wikipedia/commons/...`，不信页面任意URL或自动跳转。
- 实际取得最多**1次**已核准的官方公开WebM GET，仅360p转码版本，`0<ContentLength≤96MiB`，应用响应body累计≤100,663,296B，全部运行只允许**metadata GET≤1(≤512KiB)+video GET≤1(≤96MiB)**；TLS正常验证、禁止系统代理/301/302跳转、Range、续传、隐藏重试、DNS/URL替换，不请求AWS/Ego4D、HourVideo dev媒体、Charades或模型权重。对于响应body额度不伪称所有TLS/wire流量严格≤96MiB；失败不退款、不换原版。开新父任务私有空目录、旧账本/媒体不碰，网络前`STARTED`和每次请求前`fsync`持久计数。新私有part完整、校验EBML头与申明ContentLength后才原子rename为完成WebM。若获取耗时>10分钟/超预算则STOP，不重发。
- 已提交可运行[限定2次请求的下载脚本 `fetch_commons_long.py`](./fetch_commons_long.py)。执行器只从现有公共checkout读取这份源码，AST检测成功后复制到**本任务唯一私人运行目录**，示意`python fetch_commons_long.py --private-dir <PRIVATE_NEW_TASK_DIR>`。任何代码/元数据/来源不兼容都可以诚实HOLD，但不能悄悄扩大数据范围；若轻微工程Bug，可只在任务私有副本补丁并报告类别，不改GitHub公共源码、不新增另一个媒体请求。公共Git仓不存电影、帧、特征、旧私有账本或执行产物。

## 真实长时间跨度训练A/B：固定同预算两臂

- 已提交[真实视频 A/B 代码`long_temporal_ab.py`](./long_temporal_ab.py)，与新下载视频位于同一任务私人运行环境。离线AST检查后，**前台一次**执行，如`python long_temporal_ab.py --video <PRIVATE_NEW_TASK_DIR>/one-week-360p.webm --steps-per-arm 100 --gpu-minutes 12`。仅用既有PyAV/OpenCV/numpy/torch，CPU真正从解码PTS按约3s挑帧，最多100,000帧解码与560个保留样本；须取到**≥350个真实帧样本，且实际PTS跨度≥1200秒**，否则训练0。CPU抽样/解码需独立硬监督≤10分钟、避免无限帧迭代；不安装包或用ffmpeg重编码。
- 冻结**前70%时间窗口作为训练、后30%为同视频稍后时间块验证**，缓冲9s，两训练臂各**128个真实帧**：A在训练候选内等时间均匀选128；B在训练候选内按相邻帧RGB低分辨率变化幅度确定性挑最高128（排序恢复真实PTS）。验证在同一后段时间窗取70帧，对两臂**固定完全相同160对的时序先后验证pair**；训练pair seed/模型初始化完全一致。每臂模型384→64→1的小型顺序判别head、AdamW0.002，**最多100次真实backward+optimizer.step，2臂累计≤200更新/总GPU≤12分钟、框架峰值额外≤512MiB**。batch=16，梯度与loss须finite，记录参数变化、首尾loss、验证时序pair accuracy及时间/显存、同等硬件负载门；本段不训练Qwen/SigLIP，也没有受保护QA问题/答案参与，不能产出“query-aware”或长视频问答分数。
- 如[5ed644e](../VLM-WIN-CUDA-REAL-FRAME-003/windows-cuda-real-frame-receipt.md)同款Windows混合C+G非空，不单凭非空挡住CUDA；启动前固定两次≥2秒间隔nvidia-smi：均free≥8GiB、util≤30%，自有与约定协作GPU互斥锁不冲突、没有已证冲突训练进程，才占用本机RTX3090。禁止杀进程、清他人锁、开付费云GPU或覆盖Conda/驱动。若视频不完整/PTS不足/资源门失败，两个训练臂全部0，**不得用先前5秒花朵短视频或随机数组代替长视频A/B**。全任务前台≤25分钟，GPU≤12分钟，不后台跑。
- 尽管是24分钟真实连续电影，只能标`LONG_PUBLIC_VIDEO_TEMPORAL_AB_EXPLORATORY`，**不是HourVideo/Ego4D第一视角任务、不是视频QA、不是独立heldout影片**。单片后段验证有时间/视觉分布偏差，抽样难度与天气/场景/字幕混杂，提升若有也不说明方法可迁移。两臂使用相同训练步数、模型/特征数量和验证集；差异必须如实报告，不能根据观察调整seed或重复run挑最好。结果不能自动将`NOVELTY=RETAIN0`改为PASS。

## 唯一匿名收据和STOP

- 任务只允许新增`docs/codex-artifacts/VLM-PD-LONGVIDEO-005/public-domain-long-video-ab-receipt.md`与在`docs/codex-results.md`末尾唯一`### VLM-PD-LONGVIDEO-005`回报。汇报固定来源授权检查结果、2个真实HTTPS请求尝试/成功、独立响应body容量(仅合计/范围)、是否完整视频、ffprobe/真帧/PTS跨度，A/B每臂真实updates/样本数/参数变化/首尾loss/同video晚期验证结果/显存/计算时间及失败原因。不上传私有视频/帧、提取特征、执行脚本私有补丁、SHA路径、进程身份、原Ego4D账户/UID/QA、模型/权重/完整日志，公共脚本本身已公开。
- 本父任务**不包含**任何其它数据源、第二电影、Ego4D媒体重试、训练独立QA标签、Qwen模型权重下载/推理或LoRA。旧004及8/8 EGO4D账本始终不动，Charades `FINAL_MEDIA_STOP`、发布PTS bridge UNKNOWN与`NOVELTY=RETAIN0`保持。一次正常push main后STOP，原同一Codex长期会话不重建；本机必须由用户发一条新启动消息才会真的执行。
