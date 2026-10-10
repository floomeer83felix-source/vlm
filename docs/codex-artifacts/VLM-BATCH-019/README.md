# VLM-BATCH-019｜真正长视频资源、时间坐标与原创机制的公开资料静态审查

**2026-10-10｜唯一READY父任务，只许公开网页/已获公开入口的静态文本审查。** 用户在[BATCH018](../VLM-BATCH-018/two-case-pts-and-research-decision.md)最后的2段Charades媒体成功取得但两例`CLOCK_UNKNOWN`、科学B/C仍HOLD后，明确答复“好的”，同意**先做真正长视频数据集与创新机制的公开资料静态筛选**。它是新的**非媒体**科研计划，不是重启被终止的Charades媒体路线，绝不继承剩余下载额度。只有用户在**原持续Codex聊天**主动发送“执行唯一READY VLM-BATCH-019”才能开始；不能自动任务、背景下载、PR或GPU。

## 冻结范围与安全界限

**允许**：在**独立公有文档Git checkout**安全fast-forward到main，读取`AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、`docs/codex-results.md`、本README、ChatGPT[公开资料种子](../../long-video-static-screening-seed-2026-10-10.md)；通过普通浏览器或公开网页检索/阅读**官方项目页、公开GitHub README、LICENSE正文、网页呈现的dataloader/eval源码、论文公开摘要/HTML、官方FAQ/annotations schema/公开benchmark任务页**。可对官方直接证据做短摘录与URL/页内锚点、标注静态阅读日期及版本，不要复制大量版权正文。

**禁止**：任何视频/帧/字幕/音频、Ego4D NLQ标注JSON、HuggingFace数据仓库实体（包括数据集metadata zip、QA行、`.parquet`、`.tar`、`.mp4`）、模型/权重/论文PDF**文件**或大型材料的下载；`git clone`第三方仓库、安装依赖、执行第三方脚本、`pip`、`wget/curl`批量取资料、`yt-dlp`、签署Ego4D协议或请求AWS凭证/登陆受控资源、访问付费API/第三方云、训练/推理/CPU/GPU视频解码、本地`ffprobe`调用或读取前18批Windows私有Charades媒体/CSV/PTS/实验树、修改原Conda/环境/PATH/模型/账本/锁。**源码网页静态查看不等于执行。** 不提交原视频身份、QA个例/正确答案、私有路径和真实原样本文本。网络仅访问公开页面以阅读；任何网页触发自动下载/登录/数据仓库文件则取消请求，标UNKNOWN。

**科研状态永久沿用**：BATCH018`ACCEPTED_ENGINEERING / V1_CLOCK_UNKNOWN / FINAL_MEDIA_STOP`；Charades`A_OFFICIAL_FRAME_LABEL=VERIFIED_WITHIN_012_SCOPE`、`B_TIME_RANGE_QUALITY=HOLD`、`C_P1/P2_EVENT_TRUTH=HOLD`；`NOVELTY=RETAIN0`、`NATURAL_LONGVIDEO_FROM_CHARADES=FAIL`，GPU/更多视频仍`BLOCKED`。BATCH019不得将任何时间schema存在直接写作MEDIA_CLOCK_PASS，也不得将一个 benchmark 的QA答案理解为实例物理时间边界真值。

## 六个候选（仅初选，必须独立逐项核查）

1. **Ego4D NLQ / Episodic Memory**：公开[官方docs](https://ego4d-data.org/docs/)、[data schema](https://ego4d-data.org/docs/data/annotations-schemas/)、[start/许可协议](https://ego4d-data.org/docs/start-here/)；检查 canonical video vs clip `video_start_sec`/`clip_start_sec`，metadata的video`duration_sec`、`video_start_pts`、timebase numerator/denominator和video components；**Ego4D软件仓库MIT许可不等于数据许可**。自然真长时长度/各训练样本分布、准入协议、同版媒体/PTS映射仍要逐项证明。
2. **HourVideo**：[官方代码/限制](https://github.com/keshik6/HourVideo)；500条20–120分钟Ego4D来源影片/12,976多选QA的公开声明，QA物理区间真值不足；**不许用于训练语料**，需要处理与Ego4D的来源重叠以及原数据条款。
3. **LongVideoBench**：[官方代码](https://github.com/longvideobench/LongVideoBench)、[dataloader](https://github.com/longvideobench/LongVideoBench/blob/main/longvideobench/longvideobench_dataset.py)、[论文](https://arxiv.org/abs/2407.15754)；长视频最多1小时/跨时间引用QA；明确`starting_timestamp_for_subtitles`、video sampling frame timestamps、`duration`原点关系不应默认一致；版权来源于网页第三方，数据集license不自动许可所有媒体用途。
4. **Video-MME**：[官方README](https://github.com/MME-Benchmarks/Video-MME)；长split 30–60分钟、字幕多模态，反复检查原视频著作权/许可不再分发条款、是否提供物理时间定位真值。
5. **MLVU**：[官方README](https://github.com/JUNJIE99/MLVU)；多任务QA、官方非商用和第三方视频版权/删替风险，公开页面不支持具体时长分布时写UNKNOWN。
6. **LVBench**：[官方README](https://github.com/zai-org/LVBench)；最长2小时但原视频版权并非项目所有、video2dataset抓取并非允许本轮执行；区分原视频是否与公开可见meta版本一致。

同时标记[EgoSchema官网](https://egoschema.github.io/index.html) **3分钟/题**，只可能短域辅助对照，不能当本项目长视频分布的核心证据。可以额外静态检查1-2个新的真正长视频资源，但**先完成上述六个**；任何新增来源必须是学术官网/源码有可查权利与时间合同、且不需下载或注册才能取到可判的基本说明，不能为凑名单编时长。

## 先例门（不得忽略2026新文献）

至少核上述四篇与数据集自身prior art，不能将“证据”、“分层索引”、“记忆”、“时钟校准”单独称算法原创：
- [VideoTree CVPR2025](https://videotree2024.github.io/) 查询自适应分层/粗到细；
- [ReWind CVPR2025](https://openaccess.thecvf.com/content/CVPR2025/html/Diko_ReWind_Understanding_Long_Videos_with_Instructed_Learnable_Memory_CVPR_2025_paper.html) 指令条件动态可学习记忆；
- [VideoMind ICLR2026](https://videomind.github.io/) planner/grounder/verifier/answerer证据代理；
- [Seeing Is Believing: EV²-Bench/DynamicSelect AAAI2026](https://ojs.aaai.org/index.php/AAAI/article/view/38031) 时空证据评估与动态分层压缩；
- [LongVideoBench referred reasoning](https://arxiv.org/abs/2407.15754)，[EgoSchema temporal certificate sets](https://arxiv.org/abs/2308.09126)。
必要时再核准2025—2026年最近正式发表的校准/弃答与跨时段事件实体绑定工作，不能凭只有paper title宣称某创新空白。

## 8项任务，所有结论必须有原始公开来源URL与严格UNKNOWN

**1. 安全入口**：安全fast-forward公有文档main、先读`AGENTS.md`/board/results/README；只有019唯一READY且`docs/codex-results.md`没有任何`### VLM-BATCH-019`回报才开始。无唯一READY、checkout不干净、与Charades最后STOP冲突立即中止，不访问私人工作区。
**2. 许可链与版权分离矩阵**：六数据集逐项分为(a)论文/代码许可(b)标注访问条款(c)原媒体版权所有与再分发/训练/商用约束(d)注册/点击协议、地理和伦理边界，明确`VERIFIED_OFFICIAL_TEXT / UNKNOWN / RESTRICTED`。Ego4D代码MIT**不能**覆盖其数据访问协议，HourVideo benchmark train禁止明确单列；网页版权/访问不明确就`BLOCKED_DATA_LICENSE`，不能给许可层“可能没问题”的PASS。
**3. 真长时域与评测分布**：要官方源证明真实视频**20min、30min、60min及更久**分组/数量/截断情况，区分“整个库几千小时”与“每条被标QA片段/评测输入有多长”；需要同时记录来自同一基础语料的非独立性（HourVideo/Ego4D），不能把3min EgoSchema或Charades算自然小时。具体比例无官方声明时`DURATION_DISTRIBUTION_UNKNOWN`不编数。
**4. 时间坐标合同静态源代码级审计**：针对Ego4D video/clip/NLQ官方schema，LongVideoBench视频采样与字幕`starting_timestamp_for_subtitles`，HourVideo/Ego4D原媒体匹配与Video-MME媒体替换/字幕规则，明确时间原点/单位/PTS/timebase/版本、是否有局部or绝对标签区间/视觉事件身份标签、无media时`UNKNOWN`。画出文本公式和需要独立证据之处，不用sample IDs或任何真实标注下载，不把`duration`字段与ffprobe容器时长直接等同。
**5. 先例最近邻矩阵**：上述6项强先例逐一记录论文时间、声称的机制或benchmark范式、与拟议问题重叠的**具体哪个操作**、不可再主张创新的点；对2026证据化benchmark尤其严格，证据页缺正文时`UNKNOWN`，不推断。
**6. 预注册2-3项可证伪机制假说**：例如`H1`跨video/clip/PTS/subtitle时钟不确定性显式传播并风险可控弃答，`H2`跨分钟重复事件身份证据/反事实顺序稳定性，`H3`给定等token/帧/Wallclock预算的证据充分度和选择校准。每项必须写：独立数据源是否真的有GT、最近邻强先例、仅“工程转换/记忆/分层/验证/证据”为什么不能算创新、**具体可测改善与强反例**、空白/少量样本/失败时`NO_GO`触发器；`NOVELTY=RETAIN0`直到有实验和新颖性审查。
**7. 纸面可行性/停止门**：只给`SCREEN_ONLY_PRIO_1/2/3`而非`DOWNLOAD_APPROVED`；必须定义同时满足许可/视频时长/可验证time contract/可合法建立真值/强基线/生态伦理等前置才能以后请求**新**媒体/GPU许可；分清“用于QA评估”与“用于新时序事件真值科研”，不能让benchmark data进入training。**目前不发媒体、标签或模型的下载申请、不装新环境或安排GPU。**
**8. 脱敏5处交付与停止**：检查五处报告/引用链接和PRIVATE内容完全分离，普通git commit/push一次后停止在原Codex聊天，等待ChatGPT审核，不自动开BATCH-020/GPU/下载。任何网页不可得则报告`SOURCE_UNAVAILABLE`，不替第三方签协议、不用镜像或凭GPT记忆填PASS。

## GitHub只许5处交付（全Markdown静态研究，不运行代码）

1. `docs/codex-artifacts/VLM-BATCH-019/official-dataset-license-duration-matrix.md`：六数据集表，带单项官方URL、非商用/第三方媒体版权/训练限制/长时分组/取用手续和UNKNOWN。
2. `docs/codex-artifacts/VLM-BATCH-019/timebase-provenance-and-groundtruth-contracts.md`：最少Ego4D/HourVideo/LongVideoBench/Video-MME四对象坐标schema/评测源码核查，精确字段与不同时间基式子/证据缺口及只读URL。
3. `docs/codex-artifacts/VLM-BATCH-019/prior-art-and-falsifiable-mechanisms.md`：至少6篇先例、H1/H2/H3不构成现有先例复述的差异假设及NO_GO反证表；不声称已找到原创。
4. `docs/codex-artifacts/VLM-BATCH-019/paper-feasibility-and-exit-gates.md`：分`LONG_DURATION`、`LEGAL_MEDIA`、`TIMEBASE`、`EVENT_GROUND_TRUTH`、`PRIOR_ART`、`DEVICE_COST`六独立证据门、仅静态优先级/未来逐项授权询问、不能训练或下载的红线，1页量级可决策摘要。
5. `docs/codex-results.md`文件**末尾只追加一条**`### VLM-BATCH-019 ...`父回报：8任务DONE/BLOCKED/UNKNOWN、六候选和六先例覆盖、来源链接完整性、0媒体/annotation/模型/私人资产下载、0代码/ffprobe/GPU运行及预筛结论不升级历史真值。

**严禁**更改ChatGPT独占`docs/next-steps.md`/`docs/research-overview.md`、历史013–018任何报告、源码/测试、用户Windows原素材、前18批私有账本；不要提交新的`.py`、媒体下载脚本或复制第三方网页正文。只stage以上5处，`git diff --cached --name-only`确认敏感/许可证无问题，普通commit/push main后STOP（不force/PR/Issue、不自动下一轮）。**READY只是有界公开研究审查的执行许可，不代表任何候选已GO，更无权限拿数据。**
