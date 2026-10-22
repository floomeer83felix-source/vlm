# 037：实际选择器反证与近邻复核

2026-10-22。**NO_GO_AS_CORE / DEV_DIAGNOSTIC_ONLY；NOVELTY=RETAIN0。**
公开证据基线 `1d14488`；本轮独立推导、静态调用链审查及四篇指定论文方法节阅读。
没有执行数值进程、旧合成见证或测试；下列新构造均为手工推导，不是运行结果。
私人路径stat/搜索/正文、模型、特征、GPU、训练、安装、环境修改均0。

## A：证据边界

已安全同步独立文档main，重读AGENTS、当前看板/results/overview及037合同与引用资料；
037是唯一未交付READY。[036收据](../VLM-DEV-REFERENCE-AND-STARTUP-036/reference-startup-and-real-run-receipt.md)
及[科学报告](../VLM-DEV-REFERENCE-AND-STARTUP-036/scientific-results.md)仅证明合成CPU启动恢复，
原标注引用未绑定，真实QA仍0、16槽NOT_RUN；不是选帧/模型效应为零。

[023实现](../../../prototypes/ordered_evidence_selector_023.py)是阈值0.70、AB/BA双方向、
最多四锚点及回退的合成算子；其[既有测试](../VLM-ORDERED-EVIDENCE-023/synthetic-order-falsification-receipt.md)
不能认证025。025是无阈值、恰好两锚点的另一算子。

## B：独立核对P1/P2/P3及反例搜索

依据[025源码L450–470](https://github.com/floomeer83felix-source/vlm/blob/1d14488/prototypes/temporal_evidence_adapter_025.py#L450)：
48个有限数值、严格递增PTS、q/a/b∈[-1,1]；R按(-q,PTS,index)全排序，T_m为前m项集合。
C在i≠j、D在i<j中按(-(a_i+b_j),i,j)取最小；以下“最优”均指实际数值加法及该tie。
两锚点H互异，F(H)=H∪first10(R去掉H)，输出按index即时间排序。

**P1成立。** x∈T10若非锚点，前面至多9个非锚点，必被补齐；若是锚点直接保留。
故T10⊆F，且|F|=12。C、D以及B=T12两两至少共享10帧，
replacement_distance=12−|交集|≤2，集合对称差≤4、Jaccard≥5/7。
此结论需要共同R和恰好两锚点；不是最多两个序列位置、patch或token变化的结论。

上界不能收紧为1：手工新构造PTS=i、q_i=1−i/48，未列a/b=-1，
a40=b20=1、a25=b30=0.9。C唯一最优(40,20)，D唯一最优(25,30)：
D中使用40或20的可行配对至多0，而(25,30)=1.8。
最终C=T10∪{20,40}，D=T10∪{25,30}，恰好替换2帧。
这是API合法数字，未声称可由同一真实SigLIP嵌入几何实现或具有现实发生率。

**P2成立且可加强为充要条件：F(H)=T12当且仅当H⊆T12。**
正向由锚点必入选；反向因T12恰好有10个非锚点，补齐即取尽。
因此C/D锚点均在T12时可有不同pair/目标值，却呈现完全相同12帧。
但“C/D集合相同 ⇒ 两组锚点均在T12”错误：同一外部锚点集合也能使两组相同。
pair角色交换后H不变，更直接保证F不变。既有三个见证未重跑。

进一步精确刻画补齐：E=H\T12，e=|E|；F保留E，并从T12删除e个
**排名最靠后的非锚点**。不能简化成“仅外部锚点决定结果”。手工反例：
同一R=0…47，H1={10,12}、H2={11,12}，同样E={12}，
F1={0…10,12}，F2={0…9,11,12}。内部锚点会保护截止边界元素。

**P3成立，包括同分。** D可行域包含于C；若C按确定tie取出的最优pair已经i<j，
D不可能有目标更好或同目标字典序更早的pair，否则C也应选它。
故pair、H、indices全部相同。D目标≤C目标仅为可行域包含性质。
其逆命题不成立：C向后仍可能经角色交换或补齐抵消得到相同indices。
没有发现推翻备忘录P1–P3的API合法反例；证明不依赖随机样本数。

## C：实际干预链及可核界限

以下为[公开worker](https://github.com/floomeer83felix-source/vlm/blob/1d14488/prototypes/development_worker_030.py#L170)
静态事实；本轮没有读取或执行私人helper。

| 层 | 公开传递/操作 | 可证与不可证 |
|---|---|---|
| 分数→pair | 同图像特征及question/event_a/event_b文本，归一化后点积；选项不进检索 | 改的是pair可行域，分数不是事件存在/实例认证 |
| pair→H→indices | pair排序去角色，再10补齐，再时间排序 | 角色、pair乃至H变化都可能不改变最终集合；D不把“先后关系”作为额外模型提示 |
| indices→helper | L198同一source/factory，L214调用helper(0,indices)，携带frames/times/duration等 | 未显式传arm/pair；私人factory完整实现、状态与真实输出未核，不可仅凭调用形式证明等输入 |
| helper→tensor | L215检grid/视觉token数，L217哈希tensor键、dtype、shape、连续字节 | 数量相同不等于内容相同；哈希在CUDA/BF16转换前，非最终设备tensor逐位认证 |
| tensor→generate | L219转换后，L228 greedy generate | 还需实际转换后输入、非tensor元数据、模型/config/状态绑定；代码存在不是实际调用或因果证据 |

不同indices可能取到重复像素或被processor映成相同视觉tensor；时间戳token仍可能不同。
反之只换两帧也会移动共享帧的序列位置、改变时间戳长度及Qwen时空patch组合，
不能把集合距离当tensor局部扰动大小。应分报像素/视觉tensor、文本与时间戳、完整输入绑定。
若实际完整输入相同却回答不同，优先查状态、非确定性或实现，不能归因于i<j。
worker末尾get(C)==get(D)可能在两键都缺失时比较None==None；因此必须先有双方实际
STARTED/输入绑定/终态，缺测不能记“tensor相同”。这里是静态边界提示，不修改代码。

## E：四个固定近邻

已读官方全文相关方法节，非以摘要替代；未运行/复现任何近邻，额外作者代码读取0。
下表比较属于本轮推断，不是论文对本项目的评价；预印本不推定正式发表。

| 原始依据 | 已覆盖与实质差异 | 额外成本及未证实部分 |
|---|---|---|
| [AKS v1 §3.2式(2)、§3.3](https://arxiv.org/html/2502.21271v1) | 相关性＋递归时间覆盖，TOP/BIN/ADA；025用事件对约束，无该自适应覆盖 | VL打分和层级分配；未复现，同48候选/12帧需另冻结公平适配。胜Uniform不足以超越此邻居 |
| [GenS §2.1–2.3，纸面17902–17903页](https://aclanthology.org/2025.findings-acl.921.pdf) | 训练Aria生成带置信度帧/区间，按置信度供QA；025为冻结SigLIP数字选择，非生成式检索 | 数据合成、采样器训练及额外视频模型推理；不同输入帧数/排序，不能冒称同成本基线，未复现 |
| [GCR v1 Methodology式(3)–(17)](https://arxiv.org/html/2608.01660v1) | 事件锚点/固定预算/覆盖/替换已有覆盖；其字幕ASR事件贴字、MMR和遗漏区medoid不同于两锚点＋q补齐 | 文本来源、渲染、相似度与修复成本；其query含选项，025检索不含；未复现，不是数学等价 |
| [Before It Fades v1 §3.1–3.3、§4式(2)–(3)](https://arxiv.org/html/2610.01595v1) | 反转对比、层间差异与最后token激活注入；025只改检索，不测内部时间表征 | 反向输入部分前向、层profile与注入；本项目均未做，不能借其机制结论或把所有间隔题套用答案翻转 |

最近邻之外仅剩待证的窄命题：**在相同两锚点/补齐与成本下，题目给定次序约束能产生
真实输入差异，并改善正确事件实例的证据保留及间隔作答，超出普通相关性/覆盖解释。**
目前既无此链的真实观测，也无同成本强邻居排除；保留为可失败假设，不保留核心创新。
决策与语义见[第二份报告](./scientific-decision-and-minimal-test.md)。
