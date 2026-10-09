# VLM-BATCH-006：路线2十项连续低成本科研任务包

**当前版：2026-10-09（取代本README此前的A/B/C三项划分）。** 唯一授权依据仍是主分支 `docs/next-steps.md` 中VLM-BATCH-006的**唯一READY父任务**。本次用户要求一次完成约10项：以下编号1—10都是**同一批内部子任务，不是10个额外READY任务**。同一个既有Codex聊天框执行，不需要每小项重新请示；最终一轮提交并停下，由ChatGPT集中科学审查。**不因任务变多而增加GPU/媒体/付费额度。**

## 执行前和版本保护

1. 只在独立GitHub**文档checkout**安全fetch并fast-forward main（本地未提交改动或冲突立即停）；重新阅读 `AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README及 `docs/route2-no-gold-preregistration.md`、`docs/route2-novelty-screen.md`。可复用VLM-001至005已审查摘要、尚未合并的PR#1只作为历史候选，不合并不修改。
2. 如果 `docs/codex-results.md` 已有 `### VLM-BATCH-006 ...` 的完成/部分完成/阻塞记录，**不得再次执行**；交ChatGPT验收。
3. 如果已经在旧三项协议下开始写作，本轮先核对工作树及已做内容，**不要覆盖未提交报告或擅自删除**；能够安全映射到新版十项再继续，否则停下报告冲突。源文档当前READY并不等于授权自动后台运行。
4. 路线2已取代路线1：不再要求**gold必要区间已覆盖**，不以任何参考区间标注进入选帧器；但合法QA评分答案可仅由终态**隔离评分器**读取。TRACE咨询草案保留UNSENT历史，不联系作者。
5. 本包任务原则：有证据就给可核验的静态路径、官方文献URL、接口与失败码；没有就**UNKNOWN/NO-GO**。旧实验负结果不可重跑、失效源不能暗中挑换，不为凑够十项写无依据大报告。

## 第一组：新颖性和科学可识别性（任务1—3）

**1. 直接先例全文方法/消融红队（文献审查）**  
优先Q-Frame(ICCV2025)、Self-Adaptive Sampling(MIF/MDF, NAACL2024)、DIG(CVPR2026)、Efficient Frame Selection via RL(CVPR2026)、2024 VideoQA Empirical Study；需要时再选不多于3项其他最直接工作。只读取**最多12个不同的官方或会议公开HTML页面**，每项记录query是否输入selector、frame/token预算、强对照、时间控制、统计样本单位、是否做selector-only或prompt-only消融和**证据级别**（方法/消融/仅摘要/未取得）。不能以「文献没写」等于「从未有人做过」。不下载PDF、论文压缩附件或研究数据。

**2. 路线2创新边界和新颖性否决**  
逐项对照主假设 `S_q` vs `S_t`、多样性 `S_d`、问题置换 `S_shuf` 与可选selector-only×prompt-only设计：哪些已被直接覆盖、哪些仅换名称/模型/数据、哪些尚待正式方法证据？每个可选差异点写出**一票否决的已发表先例**与需要新增何种证据。支持结论为 `REPLICATION_ONLY / CONDITIONAL_MEASUREMENT / POSSIBLE_DISTINCT_DESIGN / UNKNOWN`，不声称新算法和发表性。

**3. 可识别性与强反解释清单**  
区分：随机/固定策略的**总体效果** vs 「问题相似度/视觉注意力是因果机制」的无根据归因。列至少六项竞争解释及哪一个可测对照能减少该解释：时间bin内PTS漂移、内容/事件覆盖、清晰度/resize、实际视觉token/patch、query type/语言捷径、模型提示及检索器偏置。无法在现有协议分离的因素须标UNKNOWN或停止因果宣称，不设计靠结果挑题的追补实验。

**第一组输出**：`docs/codex-artifacts/VLM-BATCH-006/novelty-and-identifiability.md`，约2—4页，逐任务1/2/3标题。

## 第二组：现实可执行性和数据安全（任务4—7）

**4. 本地selector→frame→model接口静态追踪**  
仅在用户既有Windows研究工作区**小范围只读**检查先前报告指定的相关入口/函数/聚合schema（禁止全盘遍历）。画出 `question→SigLIP selector→candidate-frame keys→IMAGE12/Qwen3-VL-4B→answer` 的现状接口及能否控制selector-only的问题措辞，哪些路径还依赖 `index/FPS`；只写脱敏函数名、安全相对路径或schema指纹，缺代码权限记UNKNOWN。**禁止执行原研究脚本/处理器/媒体。**

**5. 新路线合法数据与隔离评分门**  
只用已审查的公开数据许可/本地聚合meta资料，不重新爬取旧404或下载真题。形成可追溯 `PASS / FAIL / UNKNOWN` 表：问答注释许可与源视频许可、可用QA评分和答案隔离、任务split、既有探索/封存排除、候选池与媒体修订。路线2不需要gold区间，但也不能把HF可见、历史20组或789节点当合法独立确认来源。

**6. 来源组、真实PTS和版本可审计性门**  
仅静态列明确必要字段与是否已有证据：typed source group/parent/clip、媒体SHA或revision、PTS/timebase、clip origin、帧唯一key、video-vs-frame-id、可能与旧保护源交叠、失败/缺失时的保守分组。**450份历史指纹缺项不是450个污染组**，不能重新哈希/遍历大批媒体或重用封存集；区分“可实施所需合同”和“目前已经实证”。

**7. 公平比较、算力和混杂预算门**  
冻结12唯一源帧、候选池、FPS/PTS基准、问题/提示、处理器版本与生成上限；比较选帧计算成本（SigLIP）、实际patch/grid/token、分辨率、时间bin内漂移、解码/IO与独立计费。对无法实测的真实处理器token必须标 `UNKNOWN`，**不能**用「12帧相同」宣布计算完全匹配。只提未来收据字段与接受/拒绝逻辑，不调用模型或真实视频CPU解码。

**第二组输出**：`docs/codex-artifacts/VLM-BATCH-006/static-readiness-gates.md`，约2—4页，逐任务4/5/6/7标题，统一门矩阵。

## 第三组：统计合同及合成测试（任务8—9）

**8. 主效应、负对照、样本量与失败分母预注册复核**  
定义主要 `Δ=mean_group[Y(S_q,q)-Y(S_t,q)]`、零假设与双侧备择；说明若一组多个题应先做来源组内汇总，不把题当独立视频。列2×2纠错/误伤、失败/构造不合格/未开始的处理边界、停止不补样、确认集不可复用，以及聚类CI/精确配对检验适用条件。把最小有用效应、配对不一致率、独立来源组、每臂wall/GPU成本及允许拒绝率列为未来样本量计算的**UNKNOWN输入**；绝不直接沿用旧240QA预算或虚构功效。

**9. 实际可运行的纯合成CPU统计审计**  
仅在独立**文档checkout**新增Python标准库、无IO且显著声明 `TOY_ONLY` 的：
- `prototypes/toy_route2_pairing.py`（虚构source组/配对二元结果，显式验证group/arm完整性并计算Δ、纠错、误伤；不读真实数据）
- `prototypes/test_toy_route2_pairing.py`（至少6个unittest覆盖成对例子、重复group/arm、缺臂、无效分数、空分母、`Δ=(R-H)/n`代数，至少一个强制失败输入和来源组不能按问题拆开的案例）。

用现有Python解释器实际运行 `python -B -m unittest discover -s prototypes -p "test_toy_route2_pairing.py" -v`；不安装依赖、不改现有toy_g1_contract。限制原型与测试总量约200行，失败只修复这两个新文件，不为了通过删测试；命令、Python版本、测试数与PASS/FAIL/ERROR/SKIP写入第三组报告。toy**不**验证真实数据、能否选出12帧、语义或新颖性，不能给NG数据门PASS。

**第三组输出**：`docs/codex-artifacts/VLM-BATCH-006/prereg-and-toy-tests.md`，约1—3页，逐任务8/9标题。

## 第四组：决策闭环（任务10）

**10. 只有一个跨组GO/NO-GO科学决策**  
综合1—9的证据与不足，给出 `NG0 直接先例/创新性`、`NG1 合法QA与媒体及评分隔离`、`NG2 来源/真实PTS/预算/接口`、`NG3 预注册功效与独立验证` 的 `PASS/FAIL/UNKNOWN` 矩阵；结论只准在 `REPLICATION_ONLY / CONDITIONAL_RESEARCH / NO_GO_OR_PIVOT` 中选择并写理由。写出**最多3项真正新增信息的下一行动**和每项用户审批点（如真的需要媒体解码/下载、外部许可询问、GPU预算），以及如果论文方法已经做过相同因子试验则立刻NO-GO。无需替ChatGPT发明另一个READY包。

**第四组输出**：`docs/codex-artifacts/VLM-BATCH-006/scientific-decision.md`，约1—2页。

## 全局配额、安全与部分失败策略

- 10项**连续处理但不是10倍资料/计算配额**：最多12个不同官方公开论文页面；本地只读仅相关少数源码/schema；只运行任务9的toy CPU单测。不进行大量软件测试、整个媒体目录遍历、全文爬虫、GPU/模型、评分/标签读取。
- **0模型QA/推理/训练/评分前向、0视频解码/导帧/受限媒体或完整标注下载、0既有Windows研究源码/环境/conda/CUDA/进程/锁/账本变更、0对外Issue/邮件/申请、0PR合并、0新人工标注。**
- 实际总量有上限；遇公开页面无法获取、原研究权限不可用或某项无证据，用 `UNKNOWN/BLOCKED` 并**继续其他独立安全子任务**，不要反复重试404或扩大查询。碰到泄漏隐患/锁与权限冲突/Git冲突，则整轮停止。
- 只上传脱敏的简短结论与可追溯论文URL、公开函数/schema名字，不上传完整研究源码、真实题、答案、文件SHA身份清单、私人完整路径、token/媒体或付费材料。
- **只允许七处GitHub变更**：4份上面指定Markdown、2份新toy Python，以及**向 `docs/codex-results.md` 追加一条父任务 `### VLM-BATCH-006 ...`**。回报逐号列任务1—10的DONE/UNKNOWN/BLOCKED及四个附件路径，写真实toy测试收据、资源计数、NO-GO建议；不得修改任务书、研究总览、AGENTS、路线2草案、旧任务/旧原型或PR。
- GitHub提交前 `git diff --cached --name-only` 应只含以上7处，核对公开内容及基线；不得强推、覆盖Codex历史条目。**一次安全提交后停止当前执行轮，保留同一个Codex聊天框**，等待ChatGPT集中审查十项并规划下一步。
