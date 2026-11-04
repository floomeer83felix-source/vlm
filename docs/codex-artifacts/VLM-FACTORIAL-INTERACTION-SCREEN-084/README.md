# 084｜先核可识别的“视频次序×问题角色”交互，不宣称算法已创新

2026-11-04（Asia/Singapore）｜ChatGPT 研究负责人｜**唯一 READY：PUBLIC_ONLY_FACTORIAL_INTERACTION_SCREEN**。

## 0. 立项性质和继承边界

用户于2026-11-04说“那就开始吧”，授权启动**新算法机制研究的第一阶段公开核查与合成诊断**，并不授权GPU、私有实验工作区、媒体、真实特征、模型forward或训练。旧083仍PAUSED_BY_OWNER/NOT_READY，不补做083、不复活069或081/082、不执行085。旧论文稿和原始实验表一律不改。公共仓库仅为文档协调层；不能从此访问私有Windows科研目录。

先安全刷新独立 GitHub 文档checkout的 main；读取 AGENTS.md、docs/next-steps.md、docs/codex-results.md、docs/research-overview.md 和本合同。只在唯一084 READY且尚无084交付时开始；不满足立即STOP。按AGENTS现有一父一执行规则，最终只允许一次脱敏交付并停止，无后台延续。

## 1. 已知失败和本次严格问题

- 063/068：冻结Qwen3-VL-4B的C/D角色文本视图在特定构造六seed有受限相对提升，50Salads均值5.00→17.67%、VIDHALLUC新条目1.33→12.33%；验证池为负、跨物理独立来源未知、绝对成绩偏低，D不是已证新机制。
- 070/075：强锚对照和固定视频控制限制语义定位/视频特定证据的归因；不同构造不可混合成一个排行榜。
- 081：另一个341,633参数头的三臂train/test近50%、源级全对0；082检查没有证明可学习性，也未找到已查范围的决定性绑定缺陷。两者不是全部输入函数都不可学的证明。
- 当前核心研究问题：冻结特征的可训练打分器是否**可能**保有时间顺序与问题角色的交互项？若能构造出交互，不等于语义时序理解、因果机制或新算法；若现有头交互弱也不等于原始特征完全无信息。

## 2. 预登记一个候选诊断算子，而非论文原创主张

对于任意**标量logit**打分函数 f(V,q)，V是按外部时间索引排序的冻结视频单元，q是合法两事件问题，τ(q)是**只从当前问题**严格交换事件角色的文本；R(V)只颠倒这组**已存视频时间单元索引**，且R²(V)=V。定义四角交互量：

I_f(V,q) = f(V,q) - f(V,τ(q)) - f(R(V),q) + f(R(V),τ(q)).

本算子是 difference-in-differences / 二因素交互投影的一种直接使用；**不是新数学公式、新反事实学习、对原始视频真正逆放或已证明时间推理**。只能在打分器已确立且真实推理确实可以只依赖当前视频+当前问题时谈可部署性；合成oracle角色/时间码仅用fixture验证数学。R(V)不重新视频解码/不重算Qwen，特征若内含原始时间上下文，R的行为不等同真实逆放。

必须通过代数或独立stdlib fixture证明的必要性质：
1. I_f(V,τ(q))=-I_f(V,q)，I_f(R(V),q)=-I_f(V,q)（基于τ²和R²），数值按固定浮点误差界检验。
2. 若 f(V,q)=a(V)+b(q)+c，则 I_f(V,q)=0；不能以零推断源特征没有信息。
3. 若 f(V,q)=s(V)r(q)，且s(RV)=-s(V)、r(τq)=-r(q)，则I_f=4s(V)r(q)；这个仅是构造实例，不是实数据效果。
4. 给出至少一个**假阳性**：静态捷径或身份相关交互也能满足相同对称性，所以不将符号响应等同正确事件定位。
5. 报告需要**四次小头logit评估**和τ的额外文本表示代价（若未缓存），不能声称与C/D端到端等成本；标量阈值化之前使用logit，禁止直接在0/1预测上作差。

本轮只考虑这个ONE_CANDIDATE（或RETAIN0），不借题加任意新头、注意力、损失或新训练。指出它与062问题表示差分、057/081监督正则、070因素化选择和CRPO反事实双分支的明确不同与重合；不能因算子文字不同就宣称创新。

## 3. 直接近邻一手查证：优先否定，允许RETAIN0

围绕数学结构、必要反事实、视觉语义定位、两个模态同时去偏，读**正文方法/公式**（有代码只取相关公开小文件），每篇写: 标题、URL/版本、方法节/关键公式、具体重合点、未读证据UNKNOWN。最多8篇，优先：

- CRPO (2026): https://arxiv.org/html/2605.21988v2 —— 反事实视频、问答关系flip/hold及双分支奖励；
- TimeBlind (2026): https://aclanthology.org/2026.emnlp-main.1923/ —— 配对视频与互补问法不是本项目首创；
- TOGA (ICCV 2025): https://openaccess.thecvf.com/content/ICCV2025/html/Gupta_TOGA_Temporally_Grounded_Open-Ended_Video_QA_with_Weak_Supervision_ICCV_2025_paper.html —— 问答与弱监督时间定位；
- NeuS-QA (AAAI 2026): https://ojs.aaai.org/index.php/AAAI/article/view/37834 —— 显式时间逻辑与事件证据；
- Counterfactual VQA (CVPR 2021): https://openaccess.thecvf.com/content/CVPR2021/html/Niu_Counterfactual_VQA_A_Cause-Effect_Look_at_Language_Bias_CVPR_2021_paper.html —— 推理时扣除语言偏差；
- Cross Modality Bias / Possible Worlds VQA (TMM 2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC11485245/ —— 视觉与语言双模态去偏；
- ETR (Mathematics 2026): https://www.mdpi.com/2227-7390/14/5/913 —— 问题驱动事件权重；
- Tracing the Arrow of Time (2026): https://arxiv.org/html/2605.07568v1 —— 冻结视觉特征时间信息路径。

不能以“未找到完全一样四项表达式”证明创新；如已有等价操作/因果解释或者不能提出超越近邻的可检验技术差异，结论RETAIN0 / NOT_NOVEL_ENOUGH且后续真实实验不立项。不能只读摘要作排他性声明。公开文本总实际读取上限20MiB（网络底层不可见说明UNKNOWN），不下载模型/代码仓库/数据。

## 4. 本轮唯一允许的可执行科学工作：纯合成、无训练

允许在 `prototypes/factorial_interaction_084.py` 和 `prototypes/test_factorial_interaction_084.py` 新建**纯Python stdlib**实现与unittest；不得import旧模型/torch、numpy、CUDA、Windows科研缓存或加载任何私有数据。合成fixture含两个视频时间顺序标签、互补问题两角色、纯additive scorer、严格乘性交互scorer、会欺骗公式的静态捷径scorer；显式检查正负互换、double involution、additive0、known interaction4x、假阳性反例、重复执行结果确定性。为避免人为构造过于容易，必须在报告中声明这是逻辑性质/软件门，不是实际特征能学的证据。没有合成例子能打破数据捷径就判假阳性设计不足并STOP，不修饰为PASS。

若一手文献确认同构已有，允许只写分析与纯合成否定结果；不为了保留新方法强行添加自创损失。测试只允许最多一次定位修正，保持失败记录；新科学训练与真实题forward 0。CPU累计≤90秒，进程内存≤512MiB，标准库单线程，父执行含查证和安全推送≤3600秒，受控输出新增≤1MiB。实际无外部用量证据则UNKNOWN。

## 5. 下一轮实验的**仅设计门**，不得执行

在`decisive-gates.md`中设计唯一下一阶段可学习性资格实验，明确：

- 拟申请新权限前，先**有独立正常拟合对照**：合成已知事件码（只作单测）→事前固定的极小train-only真实已存特征子集（需要未来单独授权），验证普通顺序保留baseline与候选是否可以拟合互补问法、完整排列；不得以旧081的未拟合基线判新法优劣。
- 严格区分三层结论：代数对称性成立；真实train-only能拟合；未接触的新来源上达到可报告的效果。前一层不认证后一层。
- 设计完全相同的参数/批流/训练步数/初始seed和非适用时说明；候选四调用成本计量；至少强普通时序读出、062 D、纯logit差分、四角交互、交互破坏负对照及固定视频控制。明示哪些同架构、哪些只是观察条件；不把候选与不匹配的控制硬算因果增益。
- 主要指标：单项、互补二问四格全对、FLIP/HOLD、source独立组、视频置换/当前视频与固定视频差异；低绝对值不能由形式对称性遮蔽。
- 下一轮预注册**停止优先**：正常baseline不能拟合train-only → 不许跑开发/test；候选在真实数据不胜合适强普通头或固定视频没有代价 → STOP；同源新条目不能充当独立基准确认。具体阈值、成本/授权缺数据则标NEEDS_PRE_REGISTRATION、不可自选。
- 需要GPU/模型调用、新媒体或真实特征读取时，列为PROPOSED_NOT_AUTHORIZED；**084不批准这些活动**。

## 6. 交付与工作边界

五个新文件+一条results（如确有执行），一次安全push到main：
1. `docs/codex-artifacts/VLM-FACTORIAL-INTERACTION-SCREEN-084/prior-art-and-mechanism.md`（最多一个候选或RETAIN0，含可检验与近邻）
2. `docs/codex-artifacts/VLM-FACTORIAL-INTERACTION-SCREEN-084/synthetic-report.md`（代码、unit结果与假阳性边界）
3. `docs/codex-artifacts/VLM-FACTORIAL-INTERACTION-SCREEN-084/decisive-gates.md`（下阶段仅设计，不授权）
4. `prototypes/factorial_interaction_084.py`
5. `prototypes/test_factorial_interaction_084.py`
6. `docs/codex-results.md`仅append 084唯一父项，状态 `PUBLIC_SCREEN_COMPLETE / NOVELTY_UNCONFIRMED`、`RETAIN0 / NO_JUSTIFIED_REAL_EXPERIMENT` 或 `BLOCKED`，不能写PASS_ALGORITHM。

执行回执在synthetic-report记录起点/终点、测试和实际预算及未知；6处之外不改任何文件，特别是AGENTS、旧083、next-steps、overview、旧纸稿、旧results、旧私有根。逐文件脱敏，杜绝用户路径、密钥、真实帧、权重、逐项标签或模型特征。不能从一个成功的数学夹具自动推进085。若目标数学诊断在近邻筛查后缺乏足够科研增量，负责人保留关闭路线权。
