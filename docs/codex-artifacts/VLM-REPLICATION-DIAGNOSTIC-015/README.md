# VLM-REPLICATION-DIAGNOSTIC-015｜首次两个HourVideo视频实验反号后的无GPU错误归因审计与科研GO/NO-GO

**2026-10-15｜唯一READY / USER_TRIGGERED_CPU_DIAGNOSTICS_ONLY。** 本轮需要用户在既有（或压缩后新交接）Codex聊天发**新的、有界只读审计指令**；README/GitHub更新不会启动后台工作。总目标：对013与014的真实成功GPU实验做**一次科学失败分析**，不把初始正差异当值得调参的机制，不凭第二段负差异直接断言SigLIP一般无效。**GPU / Qwen generate / SigLIP forward / 网络新视频和模型下载 / 环境安装 / 原始QA训练全部0**。原013/014结果已结案，不能重新调用模型或更改历史日志。

## 不得改变的两次真实证据

- [013真实收据 bf5e36a](https://github.com/floomeer83felix-source/vlm/commit/bf5e36ad216c33e6cb04d2493c9e5fce050f7713)：已手动官方demo、同UID合法gold，原43题nongold预冻结排6需额外图片→N37；uniform6/37=16.22%、SigLIP12/37=32.43%、差+16.22pp，both4/A-only2/B-only8/neither23，双侧exact McNemar p0.109375（**未显著**），INVALID4/3，Qwen generate74/74、GPU31.906s。
- [014真实收据 e7f654a](https://github.com/floomeer83felix-source/vlm/commit/e7f654a2acb93fed196da0ea4d361cb14bc1725f)：官方Sample中**与013不同canonical UID**的另一份合法v1/full_scale MP4 763.32MiB、视频约4226.83秒、金标29题nongold排除0→N29；uniform11/29=37.93%、SigLIP9/29=31.03%、差−6.90pp，both7/A-only4/B-only2/neither16，p0.6875（**未显著**），INVALID3/4，Qwen generate58/58、GPU25.344s。真实物理采集独立性、不可变发布版/精确时钟桥没有单独完成认证；都是`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、非正式HourVideo榜单。
- 两视频总共只是**2个潜在来源组**，37+29题不等于66独立物理视频；013已看结果的源为开发性探索，014公开Sample另一视频不是blind test。不能把两次的正确数粗暴合并成一个“官方66题准确率”，也不能根据已观察子组事后声称显著、等效、因果归因或科研创新（`NOVELTY=RETAIN0`）。014在同一冻结模型/prompt/帧数和解析器上**方向反转是事实**，目前不支持稳定的“SigLIP更好”结论。

## 前台CPU-only 3部分连续完成（一次父任务，不间断循环批准）

### A｜全部依赖公开收据的确定性一致性和稳健性审计（必须完成）

1. 从GitHub独立文档checkout安全ff-only同步main，确认唯一READY015、没有015旧结果，读AGENTS及013/014匿名收据、历史`route2-novelty-screen.md`与`mechanism-reset-2026-10-09.md`。不要把已结束014父任务新切回READY/复制旧实验。**标准Python库**或静态算术验证每个来源的paired四格、correct/N、invalid/NOT_RUN、生成次数/资源上限、exact McNemar两侧p，注明任何不一致；不生成看似基于多个独立组的p-value/置信区间。原始视频数量N_video=2，单新复制视频N_new=1，`RESULT_DIRECTION_FLIP`。
2. 审核两来源**可观测的实验差别**：013 dev标注37文本MCQ vs 014 public sample29、选帧query聚合PTS覆盖（013 mean3082.723s/总3597.9s vs014 mean3677.822s/总4226.7s，原始时间跨度不同不可直接按秒判原因）、uniform/query帧重合率、INVALID A/B、EOS/输出长度、推理耗时、来源时钟/发布与裁剪证书等级；**只提出混杂候选**，不可从聚合报告反推出逐题“SigLIP误检”或影像内容证据已定位。
3. 对前述先例如Q-Frame, Self-Adaptive Sampling, DIG2026, CVPR2026 RL Selector及VideoSEAL等已有公共项目文献只做**方法重复风险盘点**，本轮不发外网研究请求/不会假称已复核论文全文。区别“某视频更好”与“论文机制”的证明义务。作出明确`QUERY_SAMPLING_SUPERIORITY_NOT_ESTABLISHED`、`NOVELTY=RETAIN0`，停止再用这两来源调prompt/采样阈值/帧预算。

### B｜可选但高价值：只在用户当轮明确新许可下，使用**旧已生成的私有逐题结果**做离线非因果诊断

1. 用户可以明确授权读取**013与014各自原先已冻结的准确私有本机汇总/成对预测文件入口**（由以前同一Codex工作语境已知且已授权，若新会话不知道则须用户再指定*两个精确目录/文件*）。仅允许匹配已存在且已签名/受监督的`A/B`预测类别、问题匿名类别标签、所选48候选的时间覆盖及CPU选帧统计等**只读静态文件**；不得扫描整盘/下载目录/旧Part、不得读取完整视频、原问答答案或任何模型权重。本B在没有明确入口/权限时自动标`PRIVATE_ARTIFACTS_NOT_AUTHORIZED`并跳过，**但必须完成A与C，不能产出空报告**。
2. 如合法本地私有文件存在，CPU-only分两视频**仅做匿名类别层面**的错误剖析：A_correct/B_correct/A_invalid/B_invalid/B-only和A-only、question schema大类（有合法预先字段才用）及查询选帧相对uniform的归一化覆盖指标。不允许逐题输出/推测真实gold/UID/路径、少于5题可识别小类、答案文本、视频帧、具体源时间戳、prompt或完全回复。不得为了标出“原因”调用Qwen或对原片重新选帧；这些是**post-hoc探索性分层，严禁写成预注册因果证明**。如果旧档只有公有聚合结果，不制造逐题隐含数据。
3. 按明确安全前提公开仅大类计数，保留单片组织与最小可公布群大小；如果无私有合法类别不勉强输出子组。任何可识别敏感细节宁缺毋滥，B不构成本轮必需的用户额外凭证索取。

### C｜冷静科研决定与下一次GPU的硬门（必须完成）

1. 给出一份可证伪**下一研究路线**：第一优先新的独立合法HourVideo/Ego4D≥2–3个**真正新视频来源组**（不复用原demo或sample）及有gold的固定母集，或者寻找已批准不同公开有评测许可且长视频时轴已核的多视频样本。不能仅换模型或改随机种子重测旧013/014。
2. 冻结最基本的强对照计划：A uniform12；B original frozen SigLIP query12；将来**如文献与独立样本许可PASS**才可新增C（时间分层/语义多样性等已有强基线），而**新增C须新父任务/新GPU预算，不能偷用旧014权限**。区分真实视觉token相同、帧跨度/重合/成本，报告来源视频为统计聚类单位；不做来自N_video=2的可靠统计推断。**不能因为B在013更好而训练新selector/超参/LoRA**；只在有真实且可与现有源分离的合法训练集与已冻结独立测试数据时再考虑训练。
3. 对`NO_GO_SIGLIP_STABLE_ADVANTAGE`及`GO_REPLICATION_ONLY_IF_NEW_DATA`给出明确条件；如果资源/数据仍缺，建议暂停进一步GPU，避免盲试。结论须写出不论下次正/负如何都会报告全部视频的科研约束。论文主张“检索帧优于均匀”当前不成立，未来即使更多源结果较好也必须经现有强先例novelty筛查。

## 原始数据、安全和唯一交付

- 本父任务**0GPU、0模型生成/训练、0新媒体/模型HTTP/AWS、0环境改动、0原视频解码**；允许独立Git文档协调同步，不涉科研内容下载。窗口目标前台≤15分钟；若缺B私有文件仍继续A/C。对代码/数学复算仅已安装stdlib，不需要新包。不能做远端在线论文下载、PR merge或接触ChatGPT外部账户。
- 只允许Codex新增`docs/codex-artifacts/VLM-REPLICATION-DIAGNOSTIC-015/replication-failure-analysis.md`以及向`docs/codex-results.md`末尾追加恰一段`### VLM-REPLICATION-DIAGNOSTIC-015`，安全push main一次STOP。匿名仅公布已经公开的统计/合格聚合错误类型/证据等级/冻结下一步科学GO-NOGO。**不上传敏感UID、问题/答案原文、video文件名/路径、私有哈希、模型回复、来源重识别映射、旧运行脚本或视频截图**。旧所有父报告只读，`CLOCK_ZERO_ASSUMED_NOT_CERTIFIED`、`NOVELTY=RETAIN0`和Charades`FINAL_MEDIA_STOP`持续。
