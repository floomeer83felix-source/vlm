# Charades 原始视频时间边界核验：方案A最小媒体试点提案（2026-10-09）

> **阶段：USER_APPROVED_V1_TWO_VIDEO_MEDIA_PILOT / BATCH-013_READY / NOT_YET_EXECUTED.** 用户已明确批准**至多两段官方480p视频、所有GET正文总量≤64MiB、本地媒体/临时字节≤128MiB及现有CPU容器/Packet-PTS核验**。仅由用户在原Codex聊天主动启动[唯一READY BATCH-013](./codex-artifacts/VLM-BATCH-013/README.md)，经过安全/预算前置才可做最少量Range GET；目前**未下载视频，也未验证官方服务器206能力**。仍禁止13GB整包、画面/音频观看与抽帧、模型/GPU、原实验环境改动。原BATCH012只对齐官方frame-localization，不认证物理事件边界。

## 1. 目前确知的事实与入口限制

- [Charades官方数据页](https://prior.allenai.org/projects/charades)仅列**整包**`Data (scaled to 480p, 13 GB)`和`Data (original size) (55 GB)`、RGB frames (76 GB)，没有在页面上明确提供**按单个视频公开下载**的入口。官方480p锚点为`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip`，是**13GB整档案的URL**，不是已证明可单片读取的URL。第三方文档引用该URL并不构成另一个可用/获许可镜像。
- [官方README](https://prior.allenai.org/projects/data/charades/README.txt)声明原`Charades_v1.zip`使用H.264/MPEG-4 AVC mp4封装，原格式经过ffmpeg转码，保持原分辨率和帧率的表述涉及**原版本**；480p缩放版的精确时间轴/同源等价不能仅凭原版README推出；`length`是以秒计的视频长度。
- [官方Charades非商业许可](https://prior.allenai.org/projects/data/charades/license.txt)允许按条款科研使用，但禁止公开改造数据、向第三方分发；学术论文中的短片段或静帧只在确有必要及许可限定范围内允许。**本次不上传、不发表任何样本图片、视频、视频ID—subject映射、原CSV行、个人身份或可逆指纹**。
- 已验收[BATCH-012](./codex-artifacts/VLM-BATCH-012/three-tier-aggregate-and-go-no-go.md)：官方25点采样器与旧`end<=length`严格门不相同，差异307,183个正label cells；**A评测标签口径已限域核对**。原**B时间范围质量、C事件实例科学真值仍HOLD**。BATCH-011真实旧严格数据有19,625/66,500 token不通过，至少8,747条`end-length`处于(1,5]秒（按字段名义尺度），不能单凭字段判断责任在length还是标注。
- 官方大包**是否支持HTTPS Range 206、能否从ZIP末尾及中央目录安全解析指定成员、所需字节量、视频时钟/码流一致性**均UNKNOWN；没有实际检查授权之前不得假设可行。

## 2. 一个最小、可失败的试点，而非整库“修复”

**第一道目标（V1：格式/时钟可验证性）**：将CSV `length`与**同版480p媒体**容器报告的`format duration`、`start_time`、视频流`time_base`、`avg_frame_rate/r_frame_rate`和按PTS而非`frame index/FPS`计算的首/末可解码时点进行对照，区分媒体端点长度和动作端点的两个概念。容器metadata不自动等于真实物理动作终点；若VFR/音视频时间基/首PTS存在问题，明确UNKNOWN。

**最小试点样本：最多2个原视频**（**不是**随机声称能代表9,848部视频的统计调查）：

1. **越界案例（训练split）**：有`start<length<end`且`end-length`在(1,5]的动作；数值有效、文件映射唯一、无明显类表异常。确定性选取时优先覆盖`end`跨出CSV结束边界的可证问题。
2. **干净对照（训练split）**：合法`0<=start<end<=length`且整行无数值越界；尽量选择不同`subject`、可比视频时长，避免同源重复。若无法满足、找不到、没有单片媒体，对该对照标`NOT_AVAILABLE`而非代选其它数据。

**选择时序/私密性**：冻结原ZIP/CSV的SHA以及事先定义的算法、种子和两类候选规则，在现有本地隔离CSV中**只生成私有不公开的选择映射**；不得向GitHub写任何真实视频/subject ID、微型单元、原动作词或私有绝对路径、hash衍生源ID，也不从第三方公开列表反推匹配。**采样不是人工重标注、不得挑选最容易解释的两例**。如果视频不可取或许可不支持，STOP。

**第二道目标（V2：动作实例边界可见性）**：只有在V1表明媒体与CSV版本足以桥接、且用户**再次单独允许极小幅离线片段可视核对**后，才可针对真实动作的发生/完成区间作人工/自动视觉对照；目前**V2完全未授权**。V1不能通过metadata alone签发P1的“第一次/第二次”或P2的自然语言真值。

## 3. 已批准的V1媒体试点须满足的条件

**用户已批准下述最多2段视频的V1访问范围；具体实施以[已冻结的BATCH-013任务README](./codex-artifacts/VLM-BATCH-013/README.md)为准。** 禁止由此推断用户已批准13GB整包、画面内容核验或GPU。

- 原始官方**480p ZIP**中仅获取上述**最多2个MP4成员**，总服务器返回媒体/ZIP正文加起来**不超过64 MiB**，本地总媒体占用**不超过128 MiB**。只允许经过来源核实的官方 HTTPS URL 或同官方明示的真实独立媒体URL，**不允许13GB整包下载**。不安装任何下载工具、代理/网盘镜像/抓取爬虫或付费资源。
- 如果只有整个13GB ZIP URL，**本次获准**在符合[任务书](./codex-artifacts/VLM-BATCH-013/README.md)全部前置的条件下，以严格206、来源/重定向及总网络字节数限制执行小量HTTP Range，只针对ZIP尾部目录及上述两目标成员；**未获得视频画面查看或全包下载许可**。先`HEAD`或公开网页说明只能看大小/静态header，**不能证明Range及目标ZIP成员读取实际可行**；未来发现不支持206、返回200全档案、跳域、ZIP64不受支持、成员加密或大于预算，应在传输正文之前（或以绝对字节计数立即）`STOP`，**不退而下载整包**。
- 冻结目的为**最小来源可行性/时间钟核验**：独立Windows目录建议 `%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`（和已存在`Charades-v1-Metadata`及原RTX3090研究目录、公共docs checkout和云同步根隔离）。先查目录物理身份/no-junction/no-reparse、空间/预设预算、现有文件冲突、下载目标域、响应大小/重定向、字节指纹；未知即STOP，不移动到实验工作区。
- V1现已获准，**只用已存在的CPU ffprobe读取容器及视频packet-PTS元信息**；发现工具不存在或需安装/调整环境则STOP，不动`conda`/`torch`/`CUDA`或原研究环境。不输出/解码可视帧，不执行`-show_frames`、截图、播放、人工标注，也不将packet-PTS伪称已解码帧PTS。任何后续实际视觉动作边界核对仍需V2新授权。
- 原MP4永留隔离本地，必须有合法保留/删除方案（由用户决定后再执行，不能自动删除已存资料），零GitHub/第三方上传视频、缩略图、音频、完整字节、原注释和源ID；GitHub报告只可给**脱敏的类别化结论**（如`V1_CLOCK_MATCH / V1_CLOCK_MISMATCH / UNKNOWN`）和可验证的方法与总资源上限，不披露仅两例的可逆时长、class/ID/subject表。
- 若媒体PTS和CSV length匹配，但原annotation end晚于可播放结尾，得出的是“所选媒体版本与注释末端存在不匹配风险”，**不是**所有19,625条坏数据；若media PTS比CSV length长，可能是修订/字段差，需要追查来源，不得无证据改所有动作的时间单位或裁剪。即使2例成功，只证实该样本/版本/钟接口可试，**不能外推整个数据集**。

## 4. 授权已确认：执行门及未来V2授权

**用户本轮已经明确批准上文的有界V1获取与CPU容器/packet-PTS核验。** ChatGPT仅写GitHub协议/任务控制，尚未访问Windows或执行媒体Range GET、ffprobe；**VLM-BATCH-013为唯一READY，需用户在原Codex聊天主动发启动指令**。如Range/预算/ZIP结构或工具前置不通过，该任务按BLOCKED安全停止；不自动扩大下载。

**下一项需要另行批准的权限**只可能是V2：在V1获证确有必要且许可合规时，对极小视频片段做视觉观察/事件起止的科学核验。**这次V1授权不包含V2、GPU、原始视频公开、整包下载或自动BATCH014。** 若V1无法取得小量视频或时钟仍UNKNOWN，保持HOLD。

**重要停止条件**：用户当前已批准V1；但官方没有按需视频访问且无法在预算内安全获取→STOP，不擅自下载13GB；媒体/CSV时钟无法确定→`HOLD_TIME_CONTRACT`，且B/C不升级；两例无法解决语义→需要另行授权独立可视/标注证据或STOP；既有ACL2025 Perfect Times与AGQA等直接先例仍限制以简单Charades顺序QA宣称新算法。
