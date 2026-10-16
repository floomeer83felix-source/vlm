# VLM-UNSEEN-SOURCE-STRATIFIED-018｜冻结R4–R6新视频三臂对照：Uniform / SigLIP top12 / SigLIP时间分层top12

**2026-10-16｜唯一READY / AWAIT_USER_NEW_R4_R5_R6_MEDIA_AND_FRESH_GPU_AUTHORIZATION（没有新视频之前不可执行模型）。** 017已在原冻结R1/R2/R3三段真实视频Qwen 230/230成功，source-equal B−A+4.18pp却有1片反向；现在不要对已经看过结果的013/014/R1–R3原五片视频调seed/prompt/选帧或重跑，不能用旧gold训练。此任务在**尚未测试的016预注册R4/R5/R6三条来源组**，一次性检验**已存在的时间分层检索强基线是否改变跨视频正确率/无效答案/成本/时间覆盖**。这是复用已有基线的对照实验，不是自称新发明或事后把旧+4.18pp升级为稳定优势。

## 现有证据与为何选新问题

- 参考[017真实匿名报告](../VLM-HOURVIDEO-NEW-SOURCES-017/new-sources-paired-receipt.md)：R1/2/3冻结N=39/39/37，Uniform correct10/5/14，question-only SigLIP top12 correct14/8/12；B−A **+10.26/+7.69/−5.41pp**，视频等权均值A25.43%/B29.61%/差+4.18pp、2正1负。Qwen230/230成功自然EOS，GPU阶段99.984s/torch分配峰9134.436MiB，未训练。两份历史公开sample[013](../VLM-HOURVIDEO-WHOLEVIDEO-QA-013/whole-video-provisional-qa-receipt.md)、[014](../VLM-HOURVIDEO-CROSSVIDEO-014/crossvideo-heldout-receipt.md)分别SigLIP +16.22pp/−6.90pp，五段观察视频共3正2负，**不支持稳定优越的概括**。
- 仍是`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`：UID、release1/canonical声明时长与成功读取的完整视频PTS不能独立证明源像素编辑版次/剪辑零点/annotation t0；真正来源群聚独立、gold标注语义、盲测试也未被独立认证。前五段都已观察，**不得用于本018的第三臂训练、选择参数/阈值、正式计分或预测后挑视频**。
- 新三条ID出自[016冻结匿名候选排序](../VLM-NEW-SOURCE-ROSTER-016/source-roster-anonymous.md)中的固定备用**R4=62.01min、36条结构非图像题；R5=59.76min、35条；R6=58.46min、34条**，记录来源组彼此不同、与旧五片排除记录组不一致，但物理采集完全独立仍UNKNOWN。总结构上界**105题**，每一来源的最终可评N须在GPU前按完全相同013/014/017规则验证。之前只在016本地私人回复明确提供过R1–R3 UID：**不得猜测R4–R6真实UID**。如果旧016本地有冻结的六候选私有映射则只读取指定那份；否则仅在用户重新明确授权的两个**精确**既有HourVideo dev与release1 manifest小文件上，CPU-only按016已记载的nongold确定性排序**原样重构**R4–R6。真实ID只在Codex私有会话展示，不上传公开Git。
- 由于第三臂 C 是在看到前五片结果之后提出的对照，现将它在**取得和评分任何R4–R6新来源前冻结**；不能据旧五片事后宣传为先前早已预注册，也不能因为新媒体量少就调整C的12 bins或B的12帧。它是已有方法的时序覆盖公平强对照，不构成`NOVELTY`证据。

## 模型/选帧预注册（所有三臂12帧，同48候选，保证公平）

- **A：原Uniform12**。与017同精确PTS/48个真实等距候选帧，取原协议相同12帧。
- **B：原SigLIP top12**。同SigLIP base F32，question-only文本（不拼答案、选项、relevant_timestamps），对48帧各算实际cosine，稳定排序全片取最大12，并按PTS排序。与013/014/017完全一致。
- **C：时间分层 SigLIP top12**：将与A/B**同一48个按PTS递增的候选**按候选序号划为12个连续且**严格每段4帧**的非重叠bins：候选index 0–3、4–7、…、44–47。每段从该4帧挑**相同question-only cosine最高者**，余同B稳定tie-break规则（cosine相同先候选原下标最小），得到12帧，按PTS排列；三臂Qwen输入都用同原processor/grid与标准prompt/64token确定性。C时间覆盖由结构强制，而非用gold/QA relevant timestamps启发；**不得更改bin数/权重、增递归挑帧或用旧评分调阈值**。
- 对每条源最多**3N**个Qwen3-VL-4B-Instruct BF16 forward/generate (three methods, 每个source N≤36/35/34)；满三片**总真实attempts≤315**，`do_sample=False`, `max_new_tokens=64`，同原单A–E输出限制、strict parser，INVALID/NOT_RUN全部计入预冻结N。为控制位置偏差按原题目顺序确定性轮换**ABC/BCA/CAB**（ordinal %3），并在下发模型前冻结；三臂同每道原问题、选项与query决不含gold。
- B与C共享同一次合法的48帧SigLIP图像features和每题文本embedding；记录共同检索成本并**透明区分两种计费假设**（共享前向的边际成本、单策略独立部署时必承担的SigLIP检索成本），不能说C免费得到检索或每个B/C独占两遍计算。三个方法均真实12个源帧，精确视觉grid/video tokens在运行时核对一致；timestamp tokens可随选帧不同。

## 执行边界：不拿数据、不自动开启GPU

1. **用户的第一步（无GPU）**：在已合法拥有有效官方Ego4D数据权限、网络/SSD预算明确的情况下，由用户在原/安全交接的Codex聊天私人核实R4/R5/R6冻结UID及官方v1/full_scale单UID CLI模板，仅自行手动下载。此README与GitHub修改**不授权Codex查远端大小、探S3、安装/启动CLI、读取未知敏感文件或访问整盘**。已记录候选R4–R6的容量/远端可用性UNKNOWN。若新UID精确映射在当前会话不可证则必须向用户询问既有16私有映射/两份准确授权小文件路径，不能猜。
2. **017之外的018正式启动门**：须用户明确给出三片中已成功且合法完整下载的MP4确切本机入口、对应冻结R4–R6的私人来源信息、已获准gold dev标注入口与**新一次本018独立 GPU 授权：最多315次本地Qwen generate、总GPU阶段≤40min、torch新增allocated峰≤20GiB、父任务单调墙钟≤90min**。未经同轮明确新授权，即使READY和已下载也不能调用模型。建议三片齐后一次跑；缺片只允许按原预定顺序做所有已取得且CPU门PASS的片，报告缺片为NOT_ACQUIRED与本次研究不完整，不换R7或R1–R3，**不因当前成绩决定补下哪片**。无一条新合法视频→不执行不产空HOLD、不碰GPU。
3. CPU-only从**已授权确切路径**只读每个全片：验证普通文件/非reparse、Ego4D`v1/full_scale`下载凭据来源及freeze ID、官方记录group有别于旧五片、容器stream video PTS/序列时长≥1200秒/有界视频首中尾解码与packet EOF、annotation/canonical stream匹配/原视频剪辑发布桥证据等级，绝不伪造remote字节证书。标签资格审查复用017**原完整nongold规则**：排显式image-task、文本外部辅助资源、非五选项及非法金标编码，N源≥10才推理；前置冻结每个N，全部gold仅隔离scorer读取；按每片标明`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`及未知的物理同源/crop/时钟，若实际无法可靠识别同UID同source则那片GPU0并报告`MEDIA_CONTENT_MAPPING_HOLD`。
4. GPU与错误处理沿用017安全工作流：新GPU两次快照free≥8GiB/util≤30%、全局自有锁/互斥、私有attempt ledger每次前fsync，网络0、模型本地已授权目录、0安装/0环境改动/0外网视频或权重请求。单父GPU40min以内，任何异常OOM/超时安全STOP、不kill其他进程、不重跑失败模型输出、不降预算/调强基线。禁止013–017旧模型推理复跑/旧隐私答案训练。
5. 完整推理exit后由独立gold scorer计分。**逐源每臂correct/N、valid_wrong、INVALID、NOT_RUN、paired A/B、B/C、A/C四格、每组真实token/grid、选帧实际源PTS跨度、时间bin占有率、frame overlap、SigLIP+Qwen各阶段wall/VRAM**；将每源结果的A/B/C方向全部公开，不根据胜者省略源。满足至少两个新的真实不同recorded-source片时才报告等视频权重**描述性**准确率与B−A、C−B；强调同真实来源可否独立、局限，**三视频绝不能为论文显著/算法创新背书**。新视频不能和旧视频混做“官方整体准确率”；历史5片只作已观察参照。
6. **交付**：正式执行时仅新增`docs/codex-artifacts/VLM-UNSEEN-SOURCE-STRATIFIED-018/three-arm-new-source-receipt.md`与`docs/codex-results.md`末尾**恰一条**`### VLM-UNSEEN-SOURCE-STRATIFIED-018`，匿名仅R4/R5/R6 +聚合，0私有UID、source映射、路径、问答/金标/预测正文/原始PTS、哈希、模型权重和视频帧，普通push main一次然后STOP。冻结旧实验、`NOVELTY=RETAIN0`、Charades`FINAL_MEDIA_STOP`；**不承诺统计显著或SOTA**。

这项任务的真正问题不是发明“分层选帧”，而是从既有两个基线向**可复现实验中的三个公平同帧数强对照**推进，为后续可能的可解释长期记忆/时序证据机制提供反例与代价上界。若未来仍只有已观察视频、没有可独立评估来源，应停止GPU而非在旧dev/public样本上反复调参。
