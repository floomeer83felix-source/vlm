# 长视频数据许可—时间合同—创新先例静态筛选：ChatGPT公开资料种子（2026-10-10）

> **状态：公开页面静态初筛，不是数据准入批准、真值验证或可发表创新结论。** 用户在BATCH018最终两例`CLOCK_UNKNOWN`且Charades媒体获取`FINAL_MEDIA_STOP`后，明确同意转向真正长视频数据集与创新机制**公开资料静态筛选**。仅打开官网、GitHub README/仓库源码可读页面、学术论文元数据/页面；**未下载媒体、标注ZIP/JSON、模型、数据集CLI或论文PDF文件；未运行任何本地代码、GPU或用户Windows研究环境；未注册、签署Ego4D协议、建立访问令牌。** 真实数据使用权需另行审核并获用户专门授权。

## A. 提名集合：用途和不可替代的许可证门

| 候选及权威入口（只读网页） | 长时域/任务：可核公开声明 | 时间轴与科学标注的证据/未知 | 权限、来源与暂定用途 |
|---|---|---|---|
| **Ego4D** [docs](https://ego4d-data.org/docs/) / [NLQ schema](https://ego4d-data.org/docs/data/annotations-schemas/) / [access](https://ego4d-data.org/docs/start-here/) | 总库约3600小时第一人称多任务，不等于每个NLQ样本持续一小时；**需分辨canonical video/clip与分布** | 官方schema显式`video_start_sec`/`clip_start_sec`、frame与原视频`video_start_pts`/`video_base_numerator`、视频分量/同步偏移；说明**字段存在**，但不证明每条媒体和标注物理真值已核 | 数据及标注必须先接受Ego4D协议才能取得；仓库[MIT](https://github.com/facebookresearch/Ego4d)是软件许可，**绝不代替视频数据协议**；潜在时间坐标研究首选静态深入 |
| **HourVideo** [官方GitHub](https://github.com/keshik6/HourVideo) | 500段来自Ego4D的真实egocentric录像，公开声称每段20–120分钟、12,976道五选一多任务QA；是真长视频评测候选 | QA不自动包含可验证事件`start/end`区间真值；与Ego4D原媒体版本、时间原点、视频切取与问答时间定位链须另查；不把QA答案当事件边界标签 | 官方`BENCHMARK DATA MUST NEVER BE USED IN TRAINING CORPORA`；受Ego4D源素材许可约束，**可评测不等于可训练**；是长时QA评测备选 |
| **LongVideoBench** [官方代码](https://github.com/longvideobench/LongVideoBench) / [loader](https://github.com/longvideobench/LongVideoBench/blob/main/longvideobench/longvideobench_dataset.py) / [论文](https://arxiv.org/abs/2407.15754) | 论文给3763个网页来源视频、6678题、时长可到1小时，关注跨片段指代与视频/字幕交错 | 数据加载器显式`duration`、`frame_timestamps`、字幕`starting_timestamp_for_subtitles`，是**潜在不同时间坐标**的重要静态红旗。仍需查视频同版与真实PTS、字幕偏移基准、题目引用区间真值 | 官方库CC-BY-NC-SA-4.0非商用；素材来自网页，**数据集license不自动转让第三方视频著作权**。适合作为跨模态时间偏移与长QA基准的静态候选 |
| **Video-MME** [官方README](https://github.com/MME-Benchmarks/Video-MME) | 900视频/254小时/2700QA；短(<2分)、中(4–15分)、长(30–60分)，最长1小时；字幕/音频设置受控 | 长视频分组为真实长域，但QA并非可证“一个事件准确发生/重复几次”的物理区间标注；需查长split、字幕和评测代码、公开视频链接失效及替换后版本偏移 | 官网明确仅学术研究、视频版权归原著作权人、未经批准不得再发布/复制/修改等；适合作外部QA泛化**而非默认可训练数据** |
| **MLVU** [官方README](https://github.com/JUNJIE99/MLVU) | 九类多任务长视频QA、单/多细节与整体理解；**尚未从官网证明具体逐视频长期分布/评测划分** | 标签由官方提供但QA/自由生成不等于物理时间标注；官网说明数据可能被版权删除请求替换成稀疏帧，需查版本连续性 | CC-BY-NC-SA 4.0、官方说**不拥有原素材视频版权**并经缩放/裁剪等改动；优先做版权和媒体版本阻塞审查 |
| **LVBench** [官方README](https://github.com/zai-org/LVBench) | 声称评估最长2小时长视频、多能力问答；逐条时间合同另证 | 视频从公开来源收集，标准是QA/多阶段人工质量控制，不保证明确时间边界GT；实际数据协议/源码需静态核查 | 数据集CC-BY-NC-SA-4.0、官方不拥有原视频版权；当前不允许跟随`video2dataset`或任何脚本抓取网址 |

**不能以EgoSchema作为本项目的最终“自然超长视频”主要证据**：其[官网](https://egoschema.github.io/index.html)明确每题3分钟视频片段（尽管强调更长的内在时序依赖及temporal certificate sets）。可作辅助短域对照，不能用“来自Ego4D”把3分钟替代20–120分钟输入的长时验证。

**优先级仅用于下一轮*查文档*而非准许拿数据**：Ego4D NLQ时间字段与HourVideo自然长视频组合值得最先核（但HourVideo来自Ego4D，**不是独立来源验证**）；LongVideoBench字幕偏移与长split次之；Video-MME独立评测候选；MLVU/LVBench版权与可重现实物映射疑虑更高。必须保留`LICENSE_UNKNOWN`、`TIMECLOCK_UNKNOWN`、`MEDIA_VERSION_UNKNOWN`，不可用推测填PASS。

## B. 显式排除已存在的创新

| 必须扣除的强先例 | 官方公开来源 | 已覆盖，不能再仅以此称创新 |
|---|---|---|
| [VideoTree, CVPR 2025](https://videotree2024.github.io/) | 论文/方法说明 | 查询自适应、分层树索引、粗到细选择关键帧/字幕描述及高效长视频QA |
| [ReWind, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/html/Diko_ReWind_Understanding_Long_Videos_with_Instructed_Learnable_Memory_CVPR_2025_paper.html) | IEEE/CVF Open Access | 指令相关动态可学习记忆、读写更新、记忆指导帧选择及长时QA/定位 |
| [VideoMind, ICLR 2026](https://videomind.github.io/) | 官方项目与论文 | planner/grounder/verifier/answerer时间证据代理及Chain-of-LoRA；“先定位再核答案”已有先例 |
| [Seeing Is Believing (EV²-Bench/DynamicSelect), AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38031) | [AAAI官方页面](https://ojs.aaai.org/index.php/AAAI/article/view/38031)（2026-03-14发表） | **时空视觉证据评价**与自适应语义选择/分层压缩；“证据可核查”已不是新颖性本身 |
| [LongVideoBench, NeurIPS 2024](https://arxiv.org/abs/2407.15754) | 论文 | 多时段referenced context的长视频指代推理基准；跨分钟信息并非空白 |
| [EgoSchema, 2023](https://arxiv.org/abs/2308.09126) | 论文 | 长时依赖的`temporal certificate sets`；仅引入“需要多个时刻支撑答案”并不充分原创 |

**不能预先宣称任何新方法已原创**。下列只是未来可能值得否证的**机制假说**，必须以相近方法差异、可观察独立证据、反例和低成本对照使其可证伪：

- **H1：坐标一致且可弃答的时间证据合同**。对canonical video/clip、media packet-PTS、字幕偏移/引用区间建立**显式变换与不确定性传播**；在映射不可识别、版本不匹配、只有单点证据时**拒答**，以`coverage@risk`、时间区间IoU及错误时钟鲁棒性评估。纯换算起止/ffprobe校验属于**工程基线而非机制创新**；若其增益只是做一遍正确时钟转换则`H1_NOVELTY=NO_GO`。需查已有calibrated/abstention/evidence prior art。
- **H2：带反事实对照的跨时段事件身份记忆**。在真长视频中区分同类重复动作的不同实例，以因果状态转换/实体绑定回答“第一次/最后一次/中间是否重来”；设计在视觉事件真实出现顺序、subtitle时间错位、跨分钟相似干扰下的预注册反例及纯文本泄漏对照。但VideoTree、ReWind、VideoMind已有记忆/分层/定位，不能声称记忆本身是原创；若数据没有多实例身份真值/适用伦理授权则`H2_EVALUATION=HOLD/NO_GO`。
- **H3：证据预算下的校准选择而非简单压缩**。以**独立**长视频时序证据、答案正确性和`abstain`联合度量，在固定等帧/token/实际Wallclock预算下评估保守风险/证据充分性和反事实稳定性。面对VideoTree、DynamicSelect、EV²-Bench等强先例必须证明新增必要成分；只提高QA accuracy或少量帧不是机制贡献。

## C. 下一静态筛选任务和不可越界条件

用户本轮只批准**公开资料静态筛选**。新[唯一READY任务VLM-BATCH-019](./codex-artifacts/VLM-BATCH-019/README.md)可由用户在原Codex聊天显式发起，但**只在公开README、许可/论文摘要、评测源代码及网页文档层审计**，不进行`git clone`、`wget`、`pip install`、`huggingface_hub.download`、读取HuggingFace private gated资源、完整数据manifest/QA标注文件下载、网页内抓取视频/字幕或调用任何模型；不可使用本地历史隔离CSV/视频或装好的ffprobe。Codex只发布**有链接、可追踪、允许UNKNOWN**的候选矩阵/先例矩阵/实验可行性纸面方案，任何“可下载/可训练/有真值”均需**实际条款明确文字**才能升级资格。ChatGPT在此阶段不创建新媒体/模型许可，时钟质量与科学真值历史HOLD、创新retain0仍保持。
