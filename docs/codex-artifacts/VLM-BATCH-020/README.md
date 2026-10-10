# VLM-BATCH-020｜H1时间不确定性原创性反证 + Ego4D↔HourVideo合法同版桥接（公开静态限定）

**2026-10-10｜唯一READY父任务｜用户本轮“按你的建议”只授权先做公开网页/论文HTML的定向静态审查，绝非视频、标注、模型或GPU许可。** ChatGPT批准一个单轮、有停止门的Codex纯公开文本审查：①尽可能**否决**H1普通版本的新颖性；②核对Ego4D与HourVideo的权利链和同一媒体版本/时间坐标合同是否有公开证据。若无法闭合，返回UNKNOWN或NO_GO，**不为了产生新任务而发明创新**。必须在用户同一个持续Codex聊天主动发送下一轮指令才执行；更改GitHub文档不会自动启动Codex。

## 0. 启动授权、防重复与科研冻结

1. 只在与原Windows RTX3090研究树分开的**公有文档Git checkout**做安全`git status --short`、`git fetch origin main`，干净且可fast-forward才前进；不同步/脏目录即STOP，不reset/rebase/force推、不碰Windows私有资产。远端main为权威；重读`AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、`docs/codex-results.md`、本README及019四份报告。
2. 只有**恰好一个**`VLM-BATCH-020 READY`、且`docs/codex-results.md`没有`### VLM-BATCH-020`任何回报才能开始。其它READY/已有回报/资料矛盾即STOP。019及013–018全部结案不可重跑；特别Charades媒体`FINAL_MEDIA_STOP`。
3. 本轮是**纯静态官方网页/论文摘要或HTML**审查，完成任务包后按允许文件统一push一次即STOP，不能自行派发021或扩权。H1/H3仍是可证伪问题，不是科研创新；`NOVELTY=RETAIN0`、`MEDIA_CLOCK=UNKNOWN`、`EVENT_GT=HOLD`、`DOWNLOAD_APPROVED=NO`、`GPU=BLOCKED`。不能将BATCH018的两视频PTS未知结论重新解释成同钟已判定。

## 1. 允许与绝对禁止

**允许**：通过普通公开网页阅读官方Ego4D docs/schema/FAQ/使用协议的**公开HTML**、HourVideo项目README/LICENSE与GitHub公开代码网页、arXiv的abs/HTML、正式会议开放的论文HTML/元数据、必要的同期公开prior art和许可文字；用短摘录、精确官方URL/页面位置、访问日期、版本/commit（若网页可见）形成证据。只审查文字，不打开数据实体。

**禁止**：一切视频/音频/帧、字幕、Ego4D/HourVideo标注/QA行、JSON/parquet/tar/ZIP、媒体metadata包、论文PDF文件、模型和权重下载或拷贝；不得点击触发下载的数据仓库实体/HF dataset viewer、不得爬取样本/答案/源视频ID或构造身份映射；不得签署Ego4D数据协议、申请凭据、登录、发邮件/issue/联系作者或使用有偿/云API。不得clone第三方repo、安装依赖、运行论文/loader/任何脚本，禁止ffprobe、CPU/GPU视频解码、GPU/模型前向/训练及访问原Windows科研树/Charades视频、PTS和私有ledger。仅公有Git文档同步/提交属于允许Git动作。论文网页不可用则`SOURCE_UNAVAILABLE`，绝不绕至PDF/镜像补全。旧实验预算不复活，原工具包不读写。

## 2. 本任务主要官方线索（仅种子，须逐项原文核）

- Ego4D [获取授权](https://ego4d-data.org/docs/start-here/)、[Annotation Schemas](https://ego4d-data.org/docs/data/annotations-schemas/)、[Videos](https://ego4d-data.org/docs/data/videos/)、[Episodic Memory](https://ego4d-data.org/docs/benchmarks/episodic-memory/)、[版本更新](https://ego4d-data.org/docs/updates/)：注意canonical video、component、canonical clip是三类对象，dataset协议与软件MIT分离；标准化30fps/剪辑不等于同文件packet PTS及标注原点已证明。
- HourVideo [官方README与Benchmark Data Usage Restrictions](https://github.com/keshik6/HourVideo)、[LICENSE网页](https://github.com/keshik6/HourVideo/blob/main/LICENSE)、[公开hv_utils源码网页](https://github.com/keshik6/HourVideo/blob/main/hourvideo/hv_utils.py)：源于Ego4D，500个20–120分钟只是作者描述，基准数据禁止进入训练；README与软件许可不可自动覆盖原视频/派生标注。不要打开开发集annotation JSON/HF QA实体。
- 强先例：[COVER 2026](https://arxiv.org/abs/2608.07434)、[Grounding with Confidence 2026](https://arxiv.org/abs/2609.39883)、[Explicit Abstention Knobs 2026](https://arxiv.org/abs/2601.00138)、[VideoMind](https://videomind.github.io/)、[EV²-Bench/DynamicSelect AAAI2026](https://ojs.aaai.org/index.php/AAAI/article/view/38031)。优先核现有方法的真实算子、风险定义、校准条件、可交换性/同源分组假设；如仅看摘要，注明摘要级，不猜论文未见章节。必要时检索2025–2026相邻先例最多另加3项，限原始公开网页。
- 019冻结依据：[许可与时长](../VLM-BATCH-019/official-dataset-license-duration-matrix.md)、[坐标来源/真值](../VLM-BATCH-019/timebase-provenance-and-groundtruth-contracts.md)、[先例与H1/H2/H3](../VLM-BATCH-019/prior-art-and-falsifiable-mechanisms.md)、[退出六门](../VLM-BATCH-019/paper-feasibility-and-exit-gates.md)。

## 3. 八项连续静态任务

1. **入口校验**：唯一READY/无020回报、干净公有docs、安全同步和历史冻结；不可走回Charades下载/ffprobe/GPU。
2. **权利链两层分开**：Ego4D正式协议入口/公开可见条款与HourVideo benchmark限制分别审计：软件、标注、源媒体、衍生时钟/新研究真值、训练/评估/再分发、商业/地域/伦理及Ego4D源视频双重授权。公开完整协议不可读就记`SOURCE_UNAVAILABLE/UNKNOWN`，不签字，不把“可论文阅读”误当“可拿媒体”。是否允许构造并公开新时间标签须单列。
3. **同版桥接的必要条件**：建立**仅纸面**的Ego4D canonical video→clip/component→HourVideo版本/裁剪/重采样/容器PTS→QA/字幕/评测时钟依赖图。精确写出字段、单位、起点、transform仿射/分段映射的成立条件和source version/hash证据缺口；区分公开schema存在与单文件同钟实测，不能编造媒体UID/样本/offset/FPS。如果HourVideo公开网页没有稳定源UID/clip版本/媒体转换语义，就标`MAPPING_NOT_PUBLICLY_CERTIFIED`，不进入QA实体验证。
4. **H1最强零创新基线**：规范H1可观察输入、集合M（版本/offset/映射不确定集）、区间I、输出（回答/证据区间/拒答）与联合错误定义。在现有基线组合下分别推导**确定性正确换算、映射集合像的并集、普通保守区间扩张、COVER后校准、常规答案置信弃答与VideoMind证据复查**可覆盖哪些所谓收益；不要把一堆现有算子的并排拼接当新算子。明确条件`M`与风险标签不公开时性能/覆盖不可识别。
5. **先例红队与形式反例**：对COVER、Grounding with Confidence、Explicit Abstention、VideoMind、EV²等逐项填“已证算子/仅标题或摘要/本项目重复点/尚需验证差异”，至多增加3篇原始先例。至少2个纸面双世界反例：同观测但不同time offset/trim；以及QA答案相同而证据时间或媒体版本不同。写出**一般不可能性**：无额外版本见证/监督时为何不可能在两个不可区分世界都认证正确，不自造有效GT。可给不可识别条件的证明草图，但不运行toy/模拟/代码。
6. **可检验的残余新问题筛选**：若H1普通机制被union+COVER+弃答完全覆盖，明确`H1_NOVELTY_NO_GO`；若尚存可能差异，只给`H1_RESIDUAL_QUESTION_UNKNOWN`，提出不超过**1个**需要新信息或新可证明性质的精确定义、强基线同输入、真实风险可测标签、与最强基线不能等价的构造性见证/可推翻条件。**不得写PASS**；原则上旧019的≥2pp/≥60%仅是纸面示例，不具功效依据、不承诺统计保证；无权利/GT/可交换性即`NO_GO_FOR_EXPERIMENT`。
7. **二门联合止损**：分别给`LEGAL_PROVENANCE`、`SAME_VERSION_TIMEBASE`、`INDEPENDENT_GT`、`H1_NONTRIVIAL_DELTA`、`COST_AND_BASELINE`证据状态。只有静态`SCREEN_ONLY`优先级或明确`NO_GO/HOLD`，不能给`DATA_GO/GPU_GO/NOVELTY_GO`。Ego4D和HourVideo共享基础来源，绝不能作为彼此独立外测；NLQ≤20min clip不支持小时GT。若权利/时钟/新算子均无可弥补公开证据，则建议结束本路线；不建议用旧媒体/新人工标注绕过。
8. **脱敏交付并停止**：四处输出（下节）、审核官方链接/证据等级与PRIVATE禁区。只有普通无force push；失败报告失败，不重复执行、不转到原科研目录。执行后等ChatGPT复核，不创建021。

## 4. 恰好四处允许的Codex交付

1. `docs/codex-artifacts/VLM-BATCH-020/ego4d-hourvideo-license-and-version-bridge.md`：两来源软件/标注/媒体/派生使用条款、source→canonical→HourVideo可审计合同与明确缺口，带日期、原始URL，`UNKNOWN/RESTRICTED`不粉饰。
2. `docs/codex-artifacts/VLM-BATCH-020/h1-strong-baselines-and-impossibility-redteam.md`：H1形式定义、COVER等最近邻逐行反证、union/置信/校准强零假说、两个双世界反例及必要的信息/证明缺口。
3. `docs/codex-artifacts/VLM-BATCH-020/h1-legal-novelty-stop-decision.md`：仅纸面证据门矩阵、唯一残余待否证问题（若存在）、杀死假说条件、合法/真值/独立性/设备前提、`SCREEN_ONLY/NO_GO/HOLD`严格区分。
4. `docs/codex-results.md`尾部**只追加一条**`### VLM-BATCH-020`：八项DONE/UNKNOWN/BLOCKED摘要、三报告链接、证据来源与缺失、所有0下载/私有/代码/GPU事实及`NOVELTY=RETAIN0`。

**除以上四处，Codex不允许修改任何文件**，包括本README、ChatGPT独占`docs/next-steps.md`/`docs/research-overview.md`、历史报告、`AGENTS.md`、源码/测试与旧结果段。Stage前核`git diff --cached --name-only`严格四处且无私人标识、QA片段、媒体信息、论文长正文。普通push main后立即停止；不能顺势执行任何后续工作。
