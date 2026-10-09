# VLM-BATCH-007：形式边界与toy模型检查（任务6—7）

2026-10-09；main基线3cbe50c。只使用程序内生成的虚构二元时间槽与依赖节点；没有视频、图像、实际问题、标签、模型或原研究源码。

## 6. 有量词的保证与不可辨识反例

取有限T={0,…,n−1}，世界w∈{0,1}^T，事件位1表示该槽内发生事件。观测O是partial assignment，未知用None；**已知位假设是覆盖整个槽、完美且可信的oracle判断**。C(O)为与已知位一致的世界，φ(w)=∀t,w(t)=0。

当C非空：所有w∈C满足φ才为TRUE，所有w∈C不满足φ才为FALSE，否则UNKNOWN。空／冲突状态不得以∀空集给TRUE，必须INVALID／UNKNOWN；本toy有效位赋值的C非空，另在answer_set空集路径显式拒绝。

### 双世界反例与条件结论

O=(0,None,0)时，w0=(0,0,0)与w1=(0,1,0)产生完全相同观测，但never分别真／假。因此：

- 对任意只以O输出二元断言的算法f，至少一个世界上f不正确；无额外排除假设时不能对所有世界保证准确判断。
- 若该O上认证never真，w1是假认证；认证never假，w0是错误反驳。随机算法也不能在这两个世界上都保证正确，等权双世界的强行二元判定正确概率至多1/2。
- 未全覆盖且没有已见正事件时，C包含全零与至少一个隐藏事件世界，必须UNKNOWN。
- 一个**可信且身份／时钟正确**的已见事件反驳never；全域完备覆盖且完美探测为全零时可以认证never真。不是“任一VLM说看见”即可信事件。

真实视频中未知还包含槽内短事件、遮挡、视野外、actor／identity、clip偏移与媒体版本。全覆盖toy槽不等于连续时间全域、像素可见性或实际探测完备。假阴性让full perceived(0,0)与actual(0,1)冲突，系统会错误TRUE；假阳性也使FALSE反驳错误。任何现实保证需另有感知／覆盖／域假设证据，本轮没有。

“A前没有B”“只有A”还需要真实时间边界、主体全集与可见性／身份合同；不能从这个单事件never原语推出所有负性自然语言问题已被解决。

### 平凡基线否决

1. 恒UNKNOWN在任何输入上不作错误认证，但确定输出coverage=0；不能拿零错误率单独证有效性。无认证样本时条件风险分母为0，不填写风险0。
2. M2的最小AND依赖图撤销：X0=invalid evidence，Xk+1=Xk∪{c:Deps(c)∩Xk非空}。有限图达到最小固定点；等于到invalid节点的依赖可达闭包。一个准确完整DAG上的普通cache reachability可逐输入复制输出，局部撤销本身不是新增算法区别。多justification／OR、冲突优先级、图本身错误与跨版本上下文仍需单独合同，toy没有实现它们。
3. M3世界集按合法观察结果划分。每个非空cell都只含同一target answer才算该观察可区分。O下观察槽1可以分两答案，槽0／2不能；未知结果None不筛假设。若允许动作只有{0,2}，所有可合法取得的记录仍同观测，不可解决。此算子是普通版本空间／判别clue规划，未体现与强基线的独特运算。

这些反例否决无条件视频事实证书以及仅换名的最小算子，不是证明所有可能开放世界或可撤销视觉推理均无价值。

## 7. 实际标准库CPU穷举与测试

仅新增[原型](../../../prototypes/toy_mechanism_counterexamples.py)和[测试](../../../prototypes/test_toy_mechanism_counterexamples.py)，TOY_ONLY、无I/O，只用itertools／collections／unittest。使用既有Python3.9.21，在独立文档checkout运行：

    python -B -m unittest discover -s prototypes -p "test_toy_mechanism_counterexamples.py" -v

**本轮1次，12项PASS，0FAIL／ERROR／SKIP，unittest suite计时0.007秒**，不含启动或报告开销；未安装依赖、未换环境或修改旧toy。

| 范围／单位 | 实际toy计数／断言 |
|---|---|
| n=2、3、4，每位None/0/1 | 9+27+81=117种观测模板 |
| 每模板枚举所有一致世界 | 16+64+256=336个世界—观测配对 |
| 三值分类模板 | TRUE3、FALSE89、UNKNOWN25 |
| 完美观测假设下 | 错误TRUE0、错误FALSE0，有限域soundness通过 |
| 故意错误的unknown→0 baseline | 89个世界—观测配对产生假never TRUE |
| 恒UNKNOWN | 确定输出0，不能以零错误认证宣称有效 |
| M2 toy DAG | 4个证据的16种invalid mask下，迭代闭包与独立DFS cache baseline相同；共享source invalid传播全部后代，无关节点不动 |
| M3 toy动作 | 区分／不区分、合法动作不可识别、未知不筛以及空世界集拒绝均被测试 |

89个FALSE模板与89个naive假认证配对**恰好数值相同但单位不同**，不能混用。所有计数是小型状态空间枚举，不是模型准确率、事件样本量、真实来源或视频覆盖统计。

其余用例：双世界不同目标、已见事件与full zero、全部incomplete no-positive组合、false positive／negative打破oracle、非法观测拒绝。测试不通过真实RGB验证任何假设。

## 处置

形式命题T可在所列有限域、可信感知／完整依赖假设下成立；真实感知、来源、版本、标签、预算、新颖性及非平凡基线优势没有由toy通过。M1最小三值entailment、M2缓存闭包、M3答案partition均有平凡／已知机制对照；不可用toy正例包装为新算法。

0真实模型／GPU／QA／评分，0视频解码／下载，0原实验工作区／环境／锁／账本修改，0历史重跑／人工标注／外部联系。当前所有现实证书均HOLD，最终六门与候选去留由本包第五报告集中判断。
