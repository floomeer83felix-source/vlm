# VLM-COMMONS-RANGE-008｜稳定官方240p视频分段206获取＋真实长视频双臂GPU试验

**2026-10-14｜READY / USER_TRIGGERED_BOUNDED_RANGE_CONTRACT（唯一READY，只有用户在原Codex长会话主动发含明确新额度的执行消息时才授权发送新请求）**。这是对[bf96378](https://github.com/floomeer83felix-source/vlm/commit/bf963786cb8d9c54dc82ce52c30f311932f7d94d)实际GET200、37,316,857B媒体读取在458,752B处发生socket read timeout的工程修正。并非重跑已结案的007，不继承或退款其GET1/1、完整37,316,857B预扣和旧part，且不做“扩大40秒read_timeout再次整段下载”这种不耐中断的设计。用户一直要求尽快继续真正长视频GPU实验；**新独立HTTP/Range预算需要由用户在原Codex聊天的本任务启动消息明确批准，本README或main READY本身不构成已触发下载**。没有那条用户主动执行消息，CPU离线检查以外一切网络/GPU操作为BLOCKED。

## 已验收证据（不可伪造成功）

007官方Commons API确证固定`File:One Week (1920).webm`、US Public Domain结构化字段PASS，`360p.vp9.webm`实际0项、`240p.vp9.webm`实际**恰1项**且API返回官方`https://upload.wikimedia.org/wikipedia/commons/transcoded/...`；视频GET200，响应body声明**37,316,857 B**(<96MiB)，成功读取/私人part仅**458,752 B**，HTTP read timeout；完整WebM、真实≥20min PTS、uniform/motion GPU更新均0。旧part/账本都保持只读，不通过重新标记STARTED或恢复旧007额度获下载许可。上一单短视频已真实GPU 80步成功，**CUDA并非阻碍**。MediaWiki第三方URL不能替代真实API官方字段。

## 一轮新独立资源/请求预算

- 数据源始终为**该同一部Commons官方公有领域1920影片的`240p.vp9.webm`转码**，严禁原版、其它变体/媒体、镜像、非Commons URL、AWS/Ego4D/Charades/HourVideo QA/权重/训练数据。只允许新单轮：**官方`commons.wikimedia.org`身份/版权/键核验元数据GET≤1，meta应用body≤512KiB；对从此API取得的原始官方网址`upload.wikimedia.org` HEAD≤1；对同一对象的 HTTP Range GET≤24次；无普通200整片GET**。HEAD必须200、ContentLength**严格=37,316,857B**、确有不可空且稳定的强ETag（弱ETag拒绝）、支持Ranges；否则**Range GET0**。每个Range GET必须**206**、严格`Content-Range: bytes X-Y/37316857`、精确预期body length/identity编码、与本轮HEAD的**强ETag完全一致**（请求同时带`If-Range`强ETag）、官方HTTPS相同资源/不重定向、不代理；任何200全体返回即拒绝并停止且**不得读取整个body**。若服务端不给强ETag/206/Accept-Ranges，则记录SOURCE_NOT_RANGE_SAFE_HOLD、0新媒体流量或仅该响应头，不猜、不覆盖。
- 固定分块**≤2MiB**，顺序offset从0到37,316,856；预计`ceil(37316857/2097152)=18`个完整区间，最多24 GET包括**同一失败区间的有限再次尝试≤1次**（但如果超时后接收内容或transport bytes无法合理控制须停止）；**累计所有媒体206 GET请求区间申明长度的保守预扣≤48MiB**（50,331,648B），**实际应用媒体body读取也≤48MiB**。metadata/body独立计；每次HTTP请求前追加阶段/offset/length/身份/剩余额度的**私人fsync STARTED**并不退款，哪怕响应超时，也把该请求区间整个长度计入预算。总发送≤1 meta + 1 HEAD +24 Range GET（包括所有失败）；禁止隐式SDK重试/重定向/代理/HEAD回退/LIST/STS/Range拼多个文件。HTTPS证书验证且原站点必须受信任。物理wire/TLS/transport buffering字节量不能严格认证为≤48MiB，不要混淆应用body与物理流量；若用户要求严格总物理wire cap而非应用body则STOP/0新请求。
- 仅原任务已知私有路径用于读取旧007.part的证据类别，可**不读取也不复用**旧part；本008默认从offset0到end**新建**唯一私有目录/新ledger/新`.part`，分块fsync后按offset写入。旧007的458,752B不能直接拼新Range响应、不能覆盖、rename、删除、校验重设旧ledger。仅在每段完整206返回、长度/ContentRange/ETag匹配后才将该段标记COMMITTED并且下一段开始；在同一个008父任务期间允许同个已失败区间最多一次同额度的重新获取但**不使用已损坏的半区间数据**。未完整则永久保持新part和STARTED状态，不上传、不在下一父任务自动继续。最终文件长度、头部EBML、SHA256与ffprobe真实时长合格后才atomic rename成独立完整媒体。本任务公开不得输出媒体URL/ETag/UID/私有路径。
- 网络稳定性：`connect timeout≤15s`、单次`read timeout≤120s`，在两次每次≤64KiB的流式读取间检查`time.monotonic()`，**同一媒体下载阶段壁钟≤75分钟**，外层独立监督必须能真正终止本任务自己的卡住的socket子进程且不得杀其它程序；没有可审核的硬75min监督器则0 Range GET，写`WALL_GUARD_UNPROVEN_HOLD`。使用Windows本地单调Stopwatch，离线模拟上轮UTC偏移来保证不再误算480分钟。下载链路如出现多个区间超时、连续低于最低进度且预算不足、总时间超75min、服务端不支持Range或文件改变→停止，不持续让Codex后台重试。媒体下载**一次前台会话**，不跨夜/无人看管。
- 在网络前优先用离线小字节合成**传输协议测试fixtures**（仅测试解析器，严禁将合成数组当视频或科学训练）：模拟206正常/Range拒绝后200/ContentRange错/ETag变化/短读/重复区间/首次超时+一次允许重试/累计预扣上限/monotonic硬超时；这些fixtures **0 HTTP和0 CUDA**。Codex可在008本人私人任务目录用现有Python标准库实现可审计单线程脚本，不装包；**本父合同授权编写并离线测试传输执行器源码，但公共仓库不能上传代码或私有ledger，只传匿名结果**。离线 fixtures 未全PASS则MEDIA GET0、STOP，不在实际下载时临时放宽身份/额度。

## 完整长片到手才进入RTX3090真实uniform vs motion A/B

- 仅当新媒体完整、官方许可满足实际本机研究用途且本机PyAV解码≥350个真实帧样本、可靠PTS跨度≥1200秒时，使用已冻结[long_temporal_ab.py](../VLM-PD-LONGVIDEO-005/long_temporal_ab.py)运行本地**均匀128帧 vs 运动变化优先128帧**，两臂各最多100次`backward()/optimizer.step()`，真实RTX3090累计GPU≤12分钟，head参数固定/seed与验证pair相同，训练前70%和晚段30%之间留9秒间隔，记录实际loss/steps/参数变化/同视频后段pair准确率、帧时间跨度、GPU时间和torch显存（框架allocated新增≤512MiB），绝不宣称Qwen3-VL推理或LoRA。CPU解码硬限≤10分钟、GPU资源两次空闲≥8GiB且util≤30%/互斥门PASS，任务**整体前台≤100分钟**；严禁云GPU、环境/驱动/依赖安装、杀别人的进程、重复跑004/005/006/007或用合成样本代替真实视频。
- 如任一阶段HOLD，所有下游都写NOT_RUN/0，不隐含GPU成功。即便双臂完成，本片是非第一视角公有领域戏剧电影，**只能是单影片的长跨度低维时序头工程探索，不是HourVideo/Ego4D问答准确率/跨影片泛化/统计显著性或论文方法创新**；`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`、HourVideo dev↔Ego4D发布/PTS桥接UNKNOWN仍保持。

## 交付、保密与STOP

仅可新增`docs/codex-artifacts/VLM-COMMONS-RANGE-008/chunked-long-video-ab-receipt.md`和`docs/codex-results.md`末尾恰好一条`### VLM-COMMONS-RANGE-008`。输出匿名：meta/HEAD/Range attempts、强ETag与206资格PASS/HOLD类别（不公开真实值）、已预扣区间bytes、成功写入字节/是否完整、段数/恢复次数/准确reason_code、下载时间/PTS实际跨度、GPU A/B每臂updates/loss/参数变化/同片晚段验证、框架显存/实际耗时。**不得上传私有视频/part/帧/特征/完整URL、ETag、源哈希、Windows路径、原始账本、视频身份衍生映射、GPU进程ID/训练权重、QA原文/答案与旧受保护科研成果**。一次正常main push后STOP、不自动启动下一个READY，原用户Codex聊天保持。
