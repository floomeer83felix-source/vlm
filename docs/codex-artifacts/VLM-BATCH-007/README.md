# VLM-BATCH-007｜核心机制重立题：10项有界、无GPU的否决式科学研究

> 当前用户**最新选择B：保持长视频VLM高水平论文目标，放弃已高度重合的选帧新算法路线**。本README须以 `docs/next-steps.md` 的唯一READY父任务状态为执行授权依据。日期2026-10-09；任务为**候选机制辨识**，不是自动宣告产生创新、新实验GO或投稿承诺。

## 必读／执行与重复防线

Codex继续在**原来唯一的同一个聊天框**执行。开始时对**独立文档Git仓库**安全fetch、fast-forward `main`，如有本地未提交内容或冲突则STOP不覆盖；重新读取：
- `AGENTS.md`, `docs/next-steps.md`, `docs/codex-results.md`, `docs/research-overview.md`;
- [机制重立题与直接先例](../../mechanism-reset-2026-10-09.md)，[原始负结果](../../research-progress-2026-10-08.md)，[上轮NO-GO](../VLM-BATCH-006/scientific-decision.md)，原BATCH-006的 `novelty-and-identifiability.md`；
- [当前研究草案](../../route2-no-gold-preregistration.md)只作被否决主比较的**历史对照**，不是本批执行依据；原路线1 TRACE 邮件/Issue草案继续UNSENT。

**若 `docs/codex-results.md` 已有任何 `### VLM-BATCH-007` 完成/部分/阻塞回报，即不得重跑本包**。最新任务看板出现多个READY、冲突或本地研究安全前置不符，直接STOP。

本轮允许**十个编号子任务在同一轮依次完成、一次集中提交，安全且相互独立部分无需中途审批**。顺序1→10，但每项缺证据记UNKNOWN/NO-GO继续独立项。必须按事实保持 **retain 0**，直到更严格创新和真实数据门另行通过。公开GitHub只提交下面指定的小型脱敏文本及两份纯合成标准库代码。

## I. 研究复位与直接先例（1—2）

**1｜负结果/已经否决的机制边界图（非新扫描）**  
仅用既有历史摘要，把旧100/300 QA、撤回、关系、密采、GAP7、Q-Frame/DIG式query-aware路线等**明确失败机制及可说/不可说结论**整理为紧凑「不可重投项→实际证据→什么*新状态或推断问题*才可能不同」矩阵。禁止打开旧评分答案/日志、重新执行QA或以旧20源充作确认集。给出≥5条一票否决的常见换名方式，避免给新三个候选包装旧策略。

**2｜2025—2026“机制级”先例红队（精确而非大量罗列）**  
重点查 [NeuS-QA AAAI2026](https://ojs.aaai.org/index.php/AAAI/article/view/37834)、[VideoHV-Agent CVPR2026](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Think_Then_Verify_A_Hypothesis-Verification_Multi-Agent_Framework_for_Long_Video_CVPR_2026_paper.html)、[VideoSEAL ICML2026](https://proceedings.mlr.press/v306/qiu26v.html)、[Open-o3-Video ICML2026](https://proceedings.mlr.press/v306/meng26e.html)、[CVPR2025 temporal consistency](https://openaccess.thecvf.com/content/CVPR2025/html/Jung_On_the_Consistency_of_Video_Large_Language_Models_in_Temporal_CVPR_2025_paper.html)、[ENTER](https://arxiv.org/abs/2501.14194)、[2026 SEG](https://arxiv.org/abs/2601.06097)及关键经典开放世界监控、Truth Maintenance与选择性预测先例。**最多10项不同的官方/会议公开文献页面或公开方法HTML**，不得下载PDF/模型/源码包、不能访问付费订阅全文；优先实读方法/公式/消融，摘要要标摘要证据。回答每个M1/M2/M3「是否已是已知特例/重命名、最相似操作算子、尚缺的证据」；缺正式全文写UNKNOWN、不能由此宣称未被研究。

**交付1**：`docs/codex-artifacts/VLM-BATCH-007/prior-art-and-rejected-directions.md`，约2—4页，包含任务1/2。

## II. 三种候选的严格机制/反例（3—5）

先读[机制候选总说明](../../mechanism-reset-2026-10-09.md)。**三个候选相互竞争，不许默认全合并**。对每个明确 `input state`、观察域/盲区、形式谓词、时间及源条件、状态更新算子、可部署费用、何时返回UNKNOWN、一个简单平凡baseline、直接文献重合、一个可以一票否决的特定反例。

**3｜M1：开放世界负事实的“证据债务”**  
只对「没有发生」「从未」「只有」「A前没有B」等**完整性要求**作严格区分；形式化三值TRUE/FALSE/UNKNOWN。明确未经覆盖的时间/视野、帧抽样和探测器假阴性对负结论的不可证明性；给出理想oracle下的条件保证与现实VLM不满足的边界。**禁止**把一帧看不到当视频永不存在、宣称已经数学证实全视频事实。

**4｜M2：依赖图上的可撤销断言**  
构造带 `media revision/PTS/source group/evidence ID` 的最小命题依赖图、局部撤销规则、不相干结论保持规则、可重复/共享源与矛盾输入处理；把经典Truth Maintenance System和VideoStir/结构化memory当最强基线。如果只是普通cache invalidation/重问，就按NO-GO，不要伪装成新算法。

**5｜M3：多候选答案的区分义务**  
将同一观测下仍一致的答案假设显式组成集合，给出允许观察/未知观察/能区分和不能区分的抽象映射；区分“诊断义务”与检索分数/最终答案，不用正确答案标签提前筛。直接对照VideoHV/PACE的discriminative clue及NeuS逻辑规则；若本质是已发表clue planner，只能复现/NO-GO。

**交付2**：`docs/codex-artifacts/VLM-BATCH-007/candidate-mechanism-specs.md`，约3—5页，按任务3/4/5分标题及**相同评价模板**，候选名只是暂名，不将其注册为可发表新方法。

## III. 可证伪理论与CPU纯符号反例（6—7）

**6｜非可辨识性/可验证性反例与失败边界**  
研究者应亲自构造**两个真实世界在观测集合O上完全一样但目标性质不同**的具体最小反例，形式论证仅由O不能可靠区分它们（不使用真实视频/图像/模型）。再构造至少两个直接否决例：平凡恒UNKNOWN可零false-certification但coverage=0；经典依赖缓存/普通时间逻辑能完全模仿M2/M3，则机制不新。输出明确量词、假设、可保证的弱性质与**绝不能保证的真实图像证书**。如发现候选在合理假设下退化为不可用，应标NO-GO。

**7｜标准库CPU小型穷举模型检查（真实运行，但仅toy）**  
在**文档Git checkout**仅新建两个自含小文件：`prototypes/toy_mechanism_counterexamples.py` 与 `prototypes/test_toy_mechanism_counterexamples.py`。约250行以内，**程序中生成的极小虚构二元时刻/事件状态**（例如2—4时间片、可观察mask）枚举所有一致的潜在世界，证明无覆盖时对全局never谓词必UNKNOWN、可见事件反驳never、全覆盖且完美toy感知才可给never真，以及错误地把未知补False会给假认证；对M2/M3可加简洁反例，但不得为数量装饰或扩张为真实video adapter。用标准库unittest ≥6用例，运行 `python -B -m unittest discover -s prototypes -p "test_toy_mechanism_counterexamples.py" -v`。记录版本、运行次数、测试数/PASS/FAIL/ERROR/SKIP、假设。**toy通过只说明有限状态逻辑，不代表创新、性能、真实感知、版权或新模型GO。** 如无法运行，报告真实原因、不得install/reconfigure；修复仅这两新toy文件、不删除失败断言。

**交付3**：`docs/codex-artifacts/VLM-BATCH-007/formal-limits-and-toy-results.md`，约2—3页，按任务6/7。

## IV. 现实实验承接与强基线（8—9）

**8｜可真实验证的数据、标签与证据类型门**  
仅复用已有许可审计/聚合schema和小范围只读本地函数；不得扫描整个媒体目录或触碰私人答案/真实评分/身份映射。逐候选写可测 `observed vs unobserved`、事件存在/不存在、论断撤销/冲突、可区分答案所需的**独立ground truth类型**；现有问答标签本身不能证明事件显式不存在或每帧检测完备。列**视频+QA许可、标签隔离、真实PTS/clip/版本、源独立、视觉检验器可用性、RTX3090资源**PASS/UNKNOWN/FAIL矩阵。如必需标签不可合法获得/无批准新增人工标注，判**NOT FEASIBLE**而非制造toy truth。

**9｜直接方法强基线、预注册与实测投入门**  
每个尚未NO-GO候选给**与其计算对象同等输入/成本**的最强直接baseline：NeuS逻辑验证、VideoSEAL answer authority、VideoHV假设检查/经典TMS/三值监控（按候选选择），而非仅比较uniform或旧GAP7。预定义最少一个主要效应和一个反证指标（错误肯定/过度拒答/无效更新/验证时间等），拟保留所有planned样本与失败、来源组聚类、独立确认集/功效所需未知输入、每个GPU/编码器/处理器/IO/token成本；预算**只列需要的参数而不承诺QA调用数**。如需手工新标签、解码版权视频或重训，标需新授权，不实施。

**交付4**：`docs/codex-artifacts/VLM-BATCH-007/feasibility-and-baselines.md`，约2—4页，按任务8/9。

## V. 一次最终科研否决决定（10）

**10｜独立候选排序与停止/下一步单点决策**  
列每个M1/M2/M3在**新颖性N、形式命题T、非平凡有效性U、可用合法标注D、工程成本B、可反证性F**六门的 `PASS / FAIL / UNKNOWN`及证据来源。对任何FAIL不得给“创新保留”；缺核心字段也不得“条件GO做GPU”。至多提**1个有条件待核的研究候选**，或**RETAIN 0 / STOP THIS PORTFOLIO**；如候选只得到UNKNOWN亦维持retain 0。下一轮最多3个**真正新增信息的行动项**（例如经授权的数据权利确认/特定强先例方法获取/有限本地fixture解码），标用户单独审批点，不自行创建READY下一包或触发GPU。

**交付5**：`docs/codex-artifacts/VLM-BATCH-007/downselect-and-stop-decision.md`，约1—2页。必须区分**任务交付ACCEPT**与**机制创新通过**两个完全不同的判断。

## 提交、红线、回报与停机

**只能一次提交总计8处变更**：
1. `docs/codex-artifacts/VLM-BATCH-007/prior-art-and-rejected-directions.md`
2. `docs/codex-artifacts/VLM-BATCH-007/candidate-mechanism-specs.md`
3. `docs/codex-artifacts/VLM-BATCH-007/formal-limits-and-toy-results.md`
4. `docs/codex-artifacts/VLM-BATCH-007/feasibility-and-baselines.md`
5. `docs/codex-artifacts/VLM-BATCH-007/downselect-and-stop-decision.md`
6. `prototypes/toy_mechanism_counterexamples.py`
7. `prototypes/test_toy_mechanism_counterexamples.py`
8. `docs/codex-results.md`仅在**末尾追加一条** `### VLM-BATCH-007 ...`父任务回报，逐项1—10的DONE/UNKNOWN/NO-GO、URL证据、toy执行收据、硬资源计数与附件链接。

绝不修改 `AGENTS.md`、`docs/next-steps.md`、`docs/research-overview.md`、研究方向草案、此前结果/旧toy、历史快照、未合并PR或其他任何文件；公开文本不得包含真实数据样本、答案、视频、完整受限身份映射、私有路径、凭据。**0 GPU/模型训练/QA/评分前向、0视频解码/导帧/媒体/模型/完整QA下载、0原Windows研究工作区/conda/CUDA/进程/锁/账本修改、0外部联系/Issue/付费API/手工标注、0旧实验重跑**。不新增自动轮询或新Codex聊天；仅允许上述toy CPU测试及少量官方公开论文方法HTML（10页上限）。

安全stage这8处并审查 `git diff --cached --name-only`、diff脱敏、是否存在旧任务回报；遇冲突不强推，停止说明。A/B/C等未知不强填，能安全继续则完成其余独立项。**成功push main后立即停止本轮**，在原聊天等ChatGPT审查与用户决定。不会因用户希望每轮10项而允许无证据凑PASS。
