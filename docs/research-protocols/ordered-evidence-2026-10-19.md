# 研究协议 H-EVIDENCE-ORDER-01｜固定12帧的多事件有序证据（候选假说，非创新结论）

**ChatGPT维护 · 2026-10-19 · FUTURE-BLIND-TEST-NOT-AUTHORIZED**

## 已有观察与研究缺口

- 017：三个已看来源共115题，SigLIP question-only Top12相对Uniform12的source-equal宏平均+4.18pp（2/3来源正），仅描述性。
- 018：另外三个已看来源共105题，Uniform12=30.36%、Top12=34.14%、12bin各top1=30.52%，Top12−Uniform12 +3.78pp，12bin−Top12 −3.62pp；强制覆盖并未得到一致提升。这不能证明“覆盖伤害准确率”的因果效应。
- 009旧GPU近远时间训练的双臂内部准确率都为45%；TRAIN-PREP纸面head使用abs(z_i-z_j)与z_i*z_j，交换两帧表示不变，因此**不能表达事件先后**。旧019/020没有新增成功动态optimizer。
- 017/018属于已见开发结果，真实媒体注释零点和严格原始拍摄来源独立性未完整认证；不能重新利用旧dev QA/gold/选择结果当未见test或调参集。

## 最接近的已有方法（不得重复包装为创新）

| 邻近工作 | 已有领域覆盖及与本假说的冲突 |
|---|---|
| AKS (CVPR 2025) | 题目相关性+视频时间覆盖联合选帧；只做时间bin不是新意 |
| GenS (ACL Findings 2025) | 问题相关长视频检索，已覆盖HourVideo；TopK相关帧不是新意 |
| ReQuest (2026) | 问题驱动+不确定性选择/时间分散；新门控并非自动创新 |
| Query-Conditioned Evidential Sampling (2026) | 题目条件证据重要性和对比打分 |
| NeuS-QA (AAAI 2026) | 时序逻辑、事件先后和神经符号推理 |
| VECTOR/MECoT (WACV 2026) | 显式事件顺序、帧打乱反例和多事件训练 |
| TimeLogic Challenge / Temporal Evidence Routing (2026) | 视觉证据定位、before/after/overlap逻辑运算 |

查阅锚点：
https://openaccess.thecvf.com/content/CVPR2025/html/Tang_Adaptive_Keyframe_Sampling_for_Long_Video_Understanding_CVPR_2025_paper.html
https://aclanthology.org/2025.findings-acl.921/
https://arxiv.org/abs/2607.01737
https://arxiv.org/abs/2604.01002
https://ojs.aaai.org/index.php/AAAI/article/view/37834
https://doi.org/10.1109/WACV61042.2026.00273
https://arxiv.org/abs/2606.01631

**新假说H1，尚未证实**：当问题确实需要观察两个事件并比较发生顺序时，在相同48候选/12帧、Qwen视觉324 tokens条件下，选择保留两个事件各自可支持的真实帧及可能的AB/BA关系，比只排序全局单事件相关性更稳健。不得从问题语句或模型概率**预先确定答案是AB还是BA**。这一理念仍可能与上述先例重合，需后续强基线/机制实证才能谈原创性。

## OEP-12：仅合成验证的初版算法

- Python标准库纯函数输入：48个唯一合成ID与严格有限升序的媒体相对PTS；三个长度48的纯合成[0,1]分数向量 sA（事件A支持）、sB（事件B支持）、sQ（整题相关性），事件分解是否可用的bool，固定k=12，合成tau=0.70。**不接收题文、选项、gold、真实UID或模型特征。** tau仅synthetic固定阈值；未来真实SigLIP score校准方式UNKNOWN，不能直接把0.70当真实cosine。
- 在i<j且两个方向事件分数均≥tau的不同帧中，分别取最优“事件A先/B后”与“事件B先/A后”有序对，按相应两事件分数之和降序，同分按(i,j)字典序固定。若某方向无可靠证据，标UNSUPPORTED、**不虚构**该方向；两方向都有可行对时最多保留四anchor（去重）。
- 剩余名额由sQ全局Top补至12：分数高优先，同分PTS早/原序号小优先；最终12帧按PTS排序。无支持方向/事件分解缺失时**精确退化为原sQ Top12**。选择器本身只能列证据候选，不得输出“AB已为真”、因果/事件身份等结论。
- 输入ID重复、PTS NaN/重复/倒序、长度错误/非法归一分数或候选数不足→HOLD并明确原因，绝不偷偷重排不合法时间、补帧或增大预算。对重复同类动作、伪相关和单帧同时支持A/B的混淆**保留负面限制**。
- 两个消融：原Global Top12，以及只保留两事件高分anchor但**不使用顺序约束**的unordered variant。比较Uniform12、旧018 12bin（未来实际实验才做）。事件拆解、归一和证据confidence在本023不实现/不可从old dev gold拟合。

## 023的最小反例单元测试（零真实数据）

至少12个独立合成测试：固定48/12唯一升序、同分确定性、global Top12精确退化、A先B而不能凭空有BA、B先A而不能凭空有AB、两种方向都存在、单高相关事件垄断sQ但A/B证据都被保留、两方向都缺的fallback、未分解fallback、时间交换使方向状态正确变化、旧对称head交换不变的纯算术反例、无效PTS和重复ID、NaN/长度边界、重复事件实例无法认证身份等。明确assert和失败示例；测试全部PASS只能说明合成代码性质，不是回答正确率或新颖性。

## 条件性的真实科研验证门（本轮未批准）

1. 未见、合法、与旧训练/评测物理拍摄组独立的未来评测来源。**R1–R6以及任何013–018旧题不能充当新盲测**，旧gold/逐题预测不允许调算法/阈值/种子/结束门。原009影片训练资格的身份/许可绑定、严格隔离现有HOLD不能继承通行证。未经授权也不获取新标签或下载媒体。
2. 建议正式预注册目标：至少8个独立source-group、120个合法未见双事件题（若不足则仅报告探索性结果，不作显著性/泛化主张）；主要比较 OEP-12 minus GlobalTop12 的source-equal macro accuracy，预设倾向门≥+5pp且source-block bootstrap 95% CI下界>0。这个门现在是**提议**，不是统计保证，需新盲测运行许可及冻结分组定义。
3. 真实相同48候选、12源帧与324 Qwen视觉tokens、公平seed/prompt/输出解析/逐源配对计数；附Uniform12、SigLIP Top12、原12bin、unordered消融、AKS，以及至少一种2026事件顺序近邻的可实现公平对照，否则不得宣称优于现有工作。事件子查询计算、双文本embedding、分数归一与选帧时间必须单独计入资源成本；不能假装检索免费。旧已观察组只可作为背景。
4. 若合法的独立视觉事件时间标签不可得，不能计算“真实双事件证据召回率”；只可报告**检索代理分数的anchor覆盖**。若时钟零点/物理源隔离未认证，维持相应UNKNOWN。非法输入、来源泄漏、检索使用答题gold、不同token预算均STOP。
5. 真实盲测没有稳定优势、强近邻超越不了、控制组下降明显、额外开销无法接受或顺序扰动测试未支持机制→报告负结论、停止扩大GPU，而非换seed找正结果。真实评测、训练、GPU或任何受限数据访问必须另行授权。

**科学状态**：NOVELTY=RETAIN0、CLOCK_ZERO_ASSUMED_NOT_CERTIFIED、Charades FINAL_MEDIA_STOP。
