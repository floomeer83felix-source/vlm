# VLM-BATCH-013：前置工具阻塞与零传输收据

2026-10-09；基线main46bc361。**BLOCKED_EXISTING_FFPROBE_NOT_FOUND：真实媒体试点未启动。** 用户批准的≤2成员／GET正文≤64MiB／本地媒体临时≤128MiB范围不扩大，未安装工具或改用PyAV／其它探测路径。未请求官方13GB对象、镜像或独立MP4。

## 1. 授权、来源与本机预检

安全同步独立文档checkout，重新读取AGENTS、唯一READY任务、结果、方案A、原隔离协议及012分层结果，确认无本批既有回报。用户只允许CPU容器与packet时钟，不包括像素／音频观看、模型、GPU、整包或原科研环境。

原metadata ZIP/train/classes SHA全部匹配任务固定值；只做文件摘要，不选择／显示真实CSV行。新媒体路径仍按`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-MediaPilot\`冻结，现不存在；已存在祖先身份／无reparse检查PASS，与已知原metadata、文档Git和研究根不重合，磁盘≥512MiB。

**未通过工具门，所以没有创建新媒体根，也未进行云根复核或写权限测试；完整storage_preflight不能写PASS。** 已有源树只读，不覆盖或清理用户文件。

### 已有ffprobe检查的证据范围

| 检查 | 结果／限制 |
|---|---|
| PATH的Application解析 | 未找到ffprobe |
| 5个常见既有系统／包管理器位置 | 0个可用候选；未扫描原conda |
| 应用已登记依赖runtime的3个精确候选位置 | 0个；只读依赖定位信息，不下载或安装runtime |
| ffprobe -version／媒体调用 | 均未执行；CPU版本UNKNOWN |
| 最终工具前置 | BLOCKED；这不是全盘扫描后证明整机绝无ffprobe |

原科研conda／Python／Torch／CUDA未改，未安装ffmpeg、7zip、pip或工具。不能借“授权已给”跳过现有ffprobe要求，也不以index/FPS或模型估计替代packet PTS。

## 2—5. 实际访问与预算

本轮未冻结真实越界／对照候选，未创建任何私有选择映射。确定性规则的纯虚构测试已做，但没有读真实id/subject选择两例，更没有因服务器结果重挑。

官方480p候选仅作为[任务书规定URL](https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip)记录；**当前官网锚点、HEAD、ETag、Accept-Ranges、真实206及ZIP结构均未重新核验**。不能从历史链接存在或合成206推断实际可访问。

| 本轮实际资源 | 数量 |
|---|---:|
| 官方网页／媒体HEAD | 0 |
| HTTP Range GET／其它研究GET | **0／0** |
| HTTP正文实际读取（含失败） | **0B** |
| 本地媒体／临时媒体峰值与保留 | **0B／0B** |
| 最终视频数／part文件数 | **0／0** |
| 真实ZIP尾／中央目录／成员头／媒体数据读取 | 0 |
| 私有媒体ledger／选择／时钟文件 | 未创建 |

没有真实请求就无需假造持久化流量ledger；ledger实际写入安全性未验证，因此也不能放行网络。Git同步、应用依赖定位不计为媒体HTTP GET；没有把这些通信冒充为官方访问。

## 9. 合成安全验证与代码交付范围

新[标准库组件](../../../prototypes/charades_range_media_clock_pilot.py)和[合成测试](../../../prototypes/test_charades_range_media_clock_pilot.py)，本轮Python3.9.21、1次**16 PASS／0 FAIL/ERROR/SKIP，suite0.006秒**，不含启动。测试没有连接服务器或使用真实视频。

覆盖206精确范围／长度／ETag／identity编码、200先拒绝不读正文、跳域／跳转、全局跨请求预算与失败已读字节、12次上限／磁盘上限、截断、经典EOCD／central／local一致性、分卷／ZIP64／descriptor拒绝、traversal／设备名／大小写重复／symlink／加密、STORED/DEFLATE/CRC与膨胀限制、两成员唯一匹配、合成选择重复ID保护、仅packet ffprobe命令与去标识输出、缺工具不进入网络或存储。

**代码状态PARTIAL_FAIL_CLOSED_COMPONENTS**：经典非ZIP64子集和安全组件仅离线验证；ZIP64、数据描述符、未知extra明确STOP。入口先查既有工具；即使以后找到工具，仍有“协调器未放行”的明确终止门，未实现／发布为可自动执行的端到端媒体下载器。不能因16项通过把未实际核验的路径／官方锚点／ledger／成员落盘／ffprobe流程宣称PASS。需要新的受限实现审查才能释放后续阶段，不能直接重复本父任务。

这次真实操作在工具前置处停止；之后只完成合成安全组件及阻塞收据，不更换来源／存储／工具或试探网络。公共代码有固定官方域、预算与拒绝规则，不含真实样本映射、账户路径、视频byte／fingerprint或精确私有PTS。

## 10. 访问裁决与停止

`V1_MEDIA_ACCESS=BLOCKED_PRECONDITION`，不是Range已证实不支持；本条件试点当前NO_GO_THIS_EXECUTION，官方按需访问路径本身仍UNKNOWN。不得称“下载两例失败”或据此改走整包／镜像，因为实际GET一次也没有。

A继承012限域规则VERIFIED；V1时钟UNKNOWN，B/C继续HOLD。0GPU／模型／视频解码／画面观察／音频／新数据／环境与原研究资产改动／外部联系。只提交规定5处，push后停止，保留原聊天。
