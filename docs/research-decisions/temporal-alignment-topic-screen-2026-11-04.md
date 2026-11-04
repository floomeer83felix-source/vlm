# 算法创新方向重筛：从角色对比转为视觉时间对齐，但暂不立项真实实验

2026-11-04（北京时间）｜ChatGPT研究负责人｜承接084结案后用户“好的，继续”。**本文件是负责人独立完成的公开文献/研究问题筛查，不是Codex父任务085，不是运行结果，不授权GPU/媒体/新benchmark/模型前向。**

**当前判断：TEMPORAL_ALIGNMENT_IS_A_PLAUSIBLE_PROBLEM / ALGORITHM_CANDIDATE_NOT_YET_JUSTIFIED / GATE0_HOLD / ZERO_READY。**

## 1. 与项目真正相关的已知证据

1. [081](./post-081-negative-gate-and-cache-learnability-audit-2026-11-03.md)：多事件时序任务的小头train约50%，测试三臂六seed都144/288、全来源0/8，B0 REAL176/288；在普通baseline没拟合时，不得将新损失或新读出器的任何“结构差异”解释为算法创新。
2. [075](./post-075-review-and-full-model-visual-screen-2026-11-02.md)：小头的共享视频均值特征可不降反升，虽然逐项预测改变；不支持“真实视频特定顺序优势已建立”。
3. [084](./post-084-factorial-interaction-disposition-2026-11-04.md)：视频索引反转×角色交换的四项logit交互符号由定义强制，静态位置捷径也满足，同语义解耦会0/4。旧算子RETAIN0，不换名重启。
4. [063/068](./research-stop-and-083-pause-2026-11-03.md)：角色差分保留有限实证稿贡献；验证负差、已用开发集/同构造管线及绝对正确率弱都不能随新方向抹除。

## 2. 新近公开研究对路线的约束

以下为本次可核实的作者/出版方摘要和出版元数据，而**非全部方法正文复核**；“可能与我们的候选重叠”不等于已经证明等价。

| 文献（2025–2026） | 公开确认内容 | 对我们“创新”主张的限制 |
|---|---|---|
| [TempCloze, EMNLP Findings 2026](https://aclanthology.org/2026.findings-emnlp.651/) | 左右视频上下文中补选中间片段，来源内相似干扰项；将Semantic/Alignment/Progression拆开，Alignment薄弱 | “去除语言捷径、补中段、研究视觉时间对齐”本身是现有任务/基准，不是算法首创 |
| [EventLens: Event-Structure Reinforcement Learning, arXiv 2610.16172 (2026-10-12)](https://arxiv.org/abs/2610.16172) | 事件边界、进展判别及多事件关系恢复；时间反转/打乱；Qwen3-VL主干 | 用同类自监督排序/反转奖励训练Qwen3-VL已经有人做，不可复制为新方法。仅核公开摘要，未取得官方全文方法比对 |
| [Visual Jigsaw Post-Training, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3504a4fa45685d668ce92797fbbf1895-Abstract-Conference.html) | 打乱视觉片段并通过自监督顺序恢复强化视觉时序 | 视觉片段排序/验证奖励不是新训练目标 |
| [TimeBridge, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_TimeBridge_Self-Supervised_Video_Representation_Learning_via_Start-End_Joint_Embedding_and_CVPR_2026_paper.html) | 起止帧联合表示及中间帧预测以学习时序变换 | “从两侧边界预测中段/双向状态连续性”有近邻；单纯边界余弦和相似度打分不值得作为新算法 |
| [Foresee-to-Ground, ICML 2026](https://proceedings.mlr.press/v306/zheng26l.html) | 先识别再测量的可验证事件证据池和时间定位 | 显式事件片段证据/边界预测已有成熟路线 |
| [VideoComp, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/html/Kim_VideoComp_Advancing_Fine-Grained_Compositional_and_Temporal_Alignment_in_Video-Text_Models_CVPR_2025_paper.html) | 多事件视频文本对齐和重排、动作替换等受控负样本 | 多事件重排+难负例本身不足以证明新颖 |

**新结论**：这是有价值的**科学问题筛查**，不是确认存在尚无人做过的算法空白。若要在此方向发表“提出新算法”，必须经作者正文/代码近邻核对找到新的可操作算子，且对静态/语言/来源捷径有实质的可识别优势。

## 3. 下一阶段建议研究问题，不是已定算法

**问题H（待审）**：在来源/外观尽量控制、没有可利用文字选项捷径的多片段视频中，模型能否从左边界、候选中段和右边界的**方向性视觉状态转移**判断真正的时间衔接？这是否比静态外观、单侧近邻、片段全局特征或有序但无关的固定来源证据提供更多稳定且可外推的信息？

这不是“事件位置加一个attention”或“前后相似度加权”的新名字。现阶段不定义新头/新损失；先确认数据/任务/普通算法能可靠学会才允许提出差异化算子。

**只作为审查用的未来最低实验结构**（不授权执行）：

- **输入**：连续真实视频的`L / candidate-M / R`视频片段；中段4选1、同来源视觉相似干扰样本，严格禁止在模型/选择策略输入中暴露答案、标记时钟、原始片段ID、顺序真值、监督构造文件名。所有元数据归档在评分侧，且需有公开允许的训练/测试使用权限。
- **基础对照**：随机选1/4；只看candidate静态外观；只看L-M或M-R一侧边界；普通双侧时序打分；当前冻结Qwen表示的顺序保留readout；真实视频 vs 固定有序无关视频；边界索引打乱/时序倒放（仅在转换有语义且不泄漏标签时）。若对照本身无法在训练集拟合且接口原因未明，停止。
- **捷径检验**：candidate类别/外观、背景/摄影机/片长、视频源、候选排列序号和物理前后相邻关系各自单独预测的成绩。高于随机的线索必须记为可能混杂，不可据“答对率”声称运动理解。语言输入只保留中性候选号，并独立校验未泄漏。
- **科学指标**：四选一正确率、来源分组正确率/置信区间、新来源盲测、真实当前视频相比固定视频的变化、同源难负例上的增益；以物理录制/来源分组为统计单位。25%是均衡四选一理论随机参照，不能当资格通过门；数值目标/样本量及预算均标NEEDS_PRE_REGISTRATION。
- **资格优先**：确认素材获取合法、完整原始帧能用、源级独立性可核；普通强baseline能在预固定train-only上拟合且反捷径；才开展数据冻结和候选算子/代价对比；在首次查看未用验证/测试之前登记唯一成功门和停止门。既有081任务的原输入不是这个任务，不可拼成新研究已运行。
- **成本**：新基准下载、视频解码、Qwen新forward/CPU/GPU更新、人工标注/新许可均未审定，默认0且**必须单独申请新预算及用户授权**。不用一次大规模实验来替代资格核查。

## 4. 本轮拒绝继续的方案

- REJECT：旧062/070/081特征头再加loss、seed或更深attention，只因结构变了而宣称新算法。
- REJECT：084四项差分重新命名或“满足反向交换反对称”的证据当成理解能力。
- REJECT：直接把TempCloze/Visual Jigsaw/EventLens任务或TimeBridge双侧衔接换名当原创。
- NOT_YET_READY：提出训练候选，因为当前还没有获许可/可核源级资格的独立视觉时间对齐输入、没有经同条件正常拟合的baseline、没有区别于上述近邻的具体新算子。

## 5. 即时下一步和门控

**本轮可执行结论**：不创建085，不在main发布Codex READY，保留论文进度。下一次研究负责人动作应该是针对`H`验证三项**缺失条件**：（a）可用合法且源级独立的评价输入；（b）合理且能拟合的标准时序baseline；（c）与TimeBridge/VideoComp/EventLens等方法至少一个明确的非换名算子差异及专门失败反例。三项有任一不足时明确STOP，不以“多做任务”填空。

如果这三项仍无实质进展，算法分支暂停，优先向目标本科高校学报完成现有有限实证稿的投稿准备（当前稿件位于`docs/papers/frozen-role-order-study/revision-2026-11-03/`，待真实作者/单位/投稿格式、合规参考文献）。**论文投稿与算法突破是两种独立目标，不互相假装替代。**


## 6. 2026-11-04追加：TempCloze官方数据准入核查（负责人公开只读）

本次下一步判断又核对了[官方GitHub](https://github.com/CedricPei/Temporal-Cloze)、[作者Hugging Face数据卡](https://huggingface.co/datasets/CedPei/TempCloze)、[EMNLP Findings 2026论文页](https://aclanthology.org/2026.findings-emnlp.651/)：

- 官方任务确为左右视频片段之间的四选一中段恢复，1,521条，7个来源；作者代码和evaluation kit公开；Alignment干扰项包含Early/Late/Wide，Progression包含Reverse/Shuffle/Loop。
- 作者Hugging Face公开表呈现一个`test` split，1.52k行，字段为`source/id/gap_start/gap_end`；这些是指向原视频及缺失区间的**元数据**，不是已可直接合法下载全部媒体的自包含训练集。本次未访问、下载或使用媒体。
- 因此**不能将TempCloze公开test划分作为本研究训练数据，并同时把其结果当未触碰的独立test**。也不能从项目论文“7来源”推断现有私人资产已获合法使用权限、独立录制和train/test无泄漏。
- 如果后续考虑TempCloze为未触及的外部测试，必须先确认所需来源媒体的独立许可证/获取途径及访问身份和成本；训练源需另行确定且与该test的源录制/参与者/原始视频严格去重。**当前尚无合格train资产**，故不下达085、不授权任何媒体或模型调用。

**唯一具体下一门（DATA_GATE）**：负责人先提交一页来源资格表：候选训练集名称/授权证据/是否已有合法完整视频/物理录制独立键/与目标test源级去重规则/允许的最小train-only验证输入/不能获证处的STOP决定。若没有合法完整且可证明未泄漏的训练输入，结束此算法路线的数据立项，不把只看元数据变成新一轮Codex占位任务。通过DATA_GATE之后才讨论常规强baseline的单次拟合资格；候选新算子仍需独立经过方法去重GATE0。本追加不改变ZERO_READY。
