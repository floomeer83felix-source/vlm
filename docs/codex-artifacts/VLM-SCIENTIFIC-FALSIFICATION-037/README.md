# VLM-SCIENTIFIC-FALSIFICATION-037：先否证干预与贡献，再决定真实投入

2026-10-22（北京时间）。**唯一READY / PUBLIC_SCIENTIFIC_REVIEW_ONLY，尚未执行。**
用户要求后续优先科研价值。036已关闭为ACCEPTED_SYNTHETIC_STARTUP_RECOVERY /
CURRENT_REFERENCE_MISSING / REAL_QA_NOT_RUN；本任务不接续旧run或私人scope。

## 0. 唯一目标

独立审查[ChatGPT科研价值备忘录](../../research-reviews/scientific-value-and-intervention-2026-10-22.md)，
尽力找反例，给出“当前C/D是否值得作为论文核心、一次最小真实pilot究竟能判什么”的可执行结论。
科学判断可为STOP/PIVOT，不能以完成报告或测试PASS替代机制证据。
本轮不要求提出一个包装后的新算法；没有通过的核心贡献就明确RETAIN0。

真实分支仍需用户在私人本地Codex提供**当前原标注完整路径**，不需要JSON内容。
本任务可以独立完成；即使收到路径也不stat/open/搜索，不转GPU或重开036，
只标明PRIVATE_INPUT_PROVIDED供后续研究负责人判断，不公开路径。

## 1. A–H一包完成，按科学依赖顺序

| 项 | 要完成的科学工作 | 必须提交的结果 |
|---|---|---|
| A | 安全同步独立文档main，读AGENTS、当前board/results/overview、本任务与下列公开证据，确认037唯一未交付READY | 明确036只有真实合成CPU恢复、原QA仍0；023与025不是同一选择器 |
| B | 尝试推翻备忘录P1/P2/P3：从实际025 select_four证明或给API合法反例；核tie、两锚点、10补齐、时间排序前提 | Top10必含、最多2替换、Top12退化、C已向前则D相同的正确范围；若错误，给最小明确反例并纠正，不能照抄 |
| C | 审查干预究竟是否到达模型：公开worker传递indices/source/helper的路径，区分pair/anchor/set/tensor | 一张干预链表；指出私人helper未公开的可核界限。不能拿源字符串断言声称真实tensor已匹配 |
| D | 核对间隔题与先后题的语义：反转/交换事件/时间戳变化何时保持答案、改变答案或破坏前提 | 至少各一个抽象问题的语义推导；只虚构例子，不重标真实QA。未知不自动假定答案翻转 |
| E | 精读下列4个固定近邻的相关方法节，给共同点/实质差异/额外成本/尚未复现部分 | ≤4行关键近邻矩阵，引用确切§/式/官方代码；不能把相近当完全等价或以“i<j”直接认定创新 |
| F | 设计唯一最小可区分实验，写成待审批计划而非执行：H0/观测量/控制/完整分母/失败解释 | 分开“检索输入是否改变”和“模型时间推理是否改变”；不以仅胜Uniform或P2单例证实机制。保持冻结025/030，不在旧协议上悄悄改算法/题/阈值 |
| G | 给继续、降级诊断或停止/转向的条件，逐条对应证据缺口；审查下一轮工程工作是否直接解决必要科学观测 | 对当前C/D论文主张作NO_GO_AS_CORE或有依据的待验证判断；如保留方向，写清最近邻未覆盖的具体命题及可失败条件，不能只换名称 |
| H | 两份紧凑报告＋results唯一037父追加，一次普通安全push main后STOP | 不增加新运行框架、不修改科学实现/旧报告/规划，不自动038、GPU/训练/扩样/搜索 |

## 2. 只读公开证据

- [036启动收据](../VLM-DEV-REFERENCE-AND-STARTUP-036/reference-startup-and-real-run-receipt.md)
  与[科研结案](../VLM-DEV-REFERENCE-AND-STARTUP-036/scientific-results.md)。
- 上述ChatGPT科研备忘录、[025科学协议](../../research-protocols/temporal-distance-diagnostic-2026-10-20.md)、
  [030开发协议](../../research-protocols/development-temporal-diagnostic-2026-10-20.md)、
  [023报告](../VLM-ORDERED-EVIDENCE-023/synthetic-order-falsification-receipt.md)。
- 公开源码prototypes/temporal_evidence_adapter_025.py（select_four/Selection）、
  prototypes/development_worker_030.py（选帧→helper→tensor_binding→generate调用路径）、
  prototypes/ordered_evidence_selector_023.py（只用于解释差异）。
  不启动production pilot/worker，不import它们的执行路径，不读取任何私人factory/cache/runtime。
- 四个固定论文全文，只读官方网页/官方PDF；引用纸面位置，获取失败记UNKNOWN，不以摘要冒充全文：
  1. AKS：[arXiv2502.21271v1](https://arxiv.org/html/2502.21271v1)，§3；作者代码https://github.com/ncTimTang/AKS。
  2. GenS：[ACL2025 Findings921](https://aclanthology.org/2025.findings-acl.921.pdf)，§2；作者代码https://github.com/yaolinli/GenS。
  3. GCR：[arXiv2608.01660v1](https://arxiv.org/html/2608.01660v1)，Ground/Cover/Refine；预印本状态不冒称正式发表。
  4. Before It Fades：[arXiv2610.01595v1](https://arxiv.org/html/2610.01595v1)，§3–4；时间反转与表征干预。
  至多另读2个上述作者仓库中直接相关的确切代码文件，只为澄清一个方法点；
  不扩大综述/追全网，不取得数据、模型、媒体或运行其代码。

## 3. 计算与写入范围

这是公共科学复核，不是新软件测试任务。优先推导和反例；
ChatGPT备忘录里的3构造/100合成向量已计算，不能把原样重跑当新成果。
若发现具体未解决命题，可以最多一个受控stdlib CPU进程≤60s/累计CPU≤120s做新反例计算，
输入全为虚构数字，完整说明命题与穷举/构造范围；无可靠监督则只推导并标未计算。
不运行旧tests，不建新test suite、守护进程或私有目录，不为增加PASS数重复旧OS/启动演示。
不import torch/numpy/transformers/av，不读取运行时模型/原研究路径、manifest、标注、QA、gold、
source map、历史预测、真实特征或frames。GPU/CUDA、模型前向/权重、训练、安装、
环境/ACL/profile/凭据修改、私人metadata/目录枚举/正文、研究数据下载均0。
网络仅普通Git协作和上列固定公开论文/至多2确切作者源码；不发Issue/邮件或其他对外消息。

## 4. 报告与判据

只准三处变更：

1. docs/codex-artifacts/VLM-SCIENTIFIC-FALSIFICATION-037/mechanism-falsification-and-neighbors.md：
   定理/反例、适用条件、模型干预路径、4近邻关键比较。优先控制在约3000中文字，必要公式除外。
2. docs/codex-artifacts/VLM-SCIENTIFIC-FALSIFICATION-037/scientific-decision-and-minimal-test.md：
   问题语义、最小待审批实验、证据需求和GO/NO_GO/STOP条件，优先约2000中文字。
3. docs/codex-results.md：末尾恰一个037父结果，含各子项结论/有限计算是否执行、
   私人/GPU0及尚无真实效应证据，不新增虚构性能表。

不改ChatGPT备忘录/任务README/board/overview/协议、任何生产源码或旧tests/结果。
不建空“真实实验收据”，不把假设结果写为已测结果，不把报告本身认作新颖性通过。
必须明确回答：
- 当前C/D真正操纵的是哪一层？为何pair不同可能无模型输入变化？
- 已知A先B后的间隔题，能否检验未知先后关系理解？反转标签条件是什么？
- 哪个具体结果将否定继续扩大投入？哪个结果仍只支持工程/开发诊断？
- 当前最近邻之外的未证实主张是什么；没有充分依据时保留RETAIN0。

一次普通安全push main后STOP。真实分支等待用户私下给路径及后续新合同，
不自动发起任何038/搜索/模型/训练。REAL_QA_EFFECT_UNKNOWN；
NOVELTY=RETAIN0；CLOCK_ZERO_ASSUMED_NOT_CERTIFIED；TRAIN-GPU HOLD；
Charades FINAL_MEDIA_STOP。

## 5. 用户一次启动消息

> 安全同步独立GitHub文档仓库main，重读AGENTS.md、board/results/overview，
> 执行唯一未交付的VLM-SCIENTIFIC-FALSIFICATION-037，按README连续完成A–H。
> 本轮优先科研反证与投入决策：独立核对实际025选择器的Top10必含/最多2替换/补齐抵消，
> 审查pair到真实模型输入的干预链，区分间隔题与先后题的变换语义，
> 对照指定4篇原始论文，给出最小待审批实验和继续/降级/停止条件。
> 只读公开仓库与合同指定论文；不重跑已有合成见证，不增加运行框架或旧测试。
> 如有具体未解命题，至多一次≤60s的受控stdlib虚构数值计算，累计CPU≤120s。
> 私人路径stat/搜索/标注/QA/gold/frames/模型/特征/GPU/训练/安装/环境修改全部0；
> 即使我另给原标注路径，也只记录私人输入已提供，本任务不访问或转为真实运行。
> 仅两份科学报告及results一条037父追加，一次安全push main后STOP，不自动038。
