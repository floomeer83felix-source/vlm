# VLM-BATCH-006：预注册与纯合成统计（任务8—9）

2026-10-09；基线main328f450。使用路线2科学草案，不改草案、不读真题／标准答案，不执行实际scorer或历史实验。

## 8. 主效应、分母与功效合同

主要两臂为S_q与S_t，回答同一原题q。来源组g内n_g个预定问题先汇总d_g=mean_q(Y_q−Y_t)，主要Δ=mean_g(d_g)。H0:Δ=0，双侧H1:Δ≠0。如果每组题数不同，题目池平均值不是等来源组估计量；有效独立单位数不能由多个问题、重复seed或同视频clip扩充。

题目配对2×2：基线t错／q对=纠错R，t对／q错=误伤H，另稳定对／稳定错。每组先汇总gain/harm率，Δ=mean_group(gain_rate)−mean_group(harm_rate)。只有一题/组或等题数等权时，才可把主Δ直接写成简单计数(R−H)/n；toy另输出question_delta及原始2×2，防止混用分母。

### 失败／缺失与预先排除

- 计划冻结前，硬NG门或构造不适用可按事前规则排除并报告建样分母／原因；不能看模型结果决定谁进队列。
- 冻结后，失败／无效／构造失败／因预算未开始的planned arm按0保留，有独立技术状态；baseline正确而candidate失败必须计H。硬门失效应停止真实执行，不把失败的算术翻转叫语义效应。
- 丢失账本臂不等于“不正确”：toy拒绝缺臂。真实恢复须先审计并以有据的未开始／未知状态明确补全终态记录，绝不重播started前向；不得静默填0、删题或替补。
- donor/shuffle、diversity和可选H-S是辅助；若要独立假设检验需事前指定family／多重性，不挑最佳子群作主要结论。H-S无合法事前等义对则NOT_FEASIBLE。
- 探索与独立确认来源隔离，封存不能回流；失败与负结果保留。区间跨0不证明等效，样本均值非0不自动证明创新。

来源组cluster bootstrap应重采样组、保留组内结构，seed／次数及目标权重先冻；少组时区间可能不稳定。精确符号检验只针对合适的独立组／符号与其零假设，不能自动当均值Δ检验；置换／符号翻转需交换性或对称／随机化等条件。二元一题/组的discordant配对检验与多题组连续d_g并不相同，本轮没有计算真实CI或p值。

### 功效与资源：当前缺失的输入

| 未来输入 | 状态／为何需要 |
|---|---|
| 最小实际有用效应δ、等效性／拒绝容限 | UNKNOWN，不能依据旧最佳结果设置 |
| 新来源组数与组内题数、相关／权重 | UNKNOWN，独立性不可用视频数替代 |
| 配对不一致率、方向率及组d_g方差 | UNKNOWN，决定信号与有效功效，不从toy估计 |
| 显著性水平、检验／多重性、目标power | 未冻结，不虚构80%或样本数 |
| 建样失败率／允许拒绝率与missing处理 | UNKNOWN，必须与全计划分母和停止规则一致 |
| 每臂实际wall、GPU显存／token、selector费用 | UNKNOWN，不能将相同帧数当相同费用 |
| 探索／确认划分和独立验证规模 | UNKNOWN，不能沿用旧20源、40—60或240QA |

## 9. 可运行toy统计审计

[toy_route2_pairing.py](../../../prototypes/toy_route2_pairing.py)和[test_toy_route2_pairing.py](../../../prototypes/test_toy_route2_pairing.py)均TOY_ONLY。只有标准库、虚构分组和二元结果，无I/O、网络、研究源码或模型依赖，不修改旧toy_g1_contract。

输入为显式planned(group,question)以及每个arm的Outcome。拒绝空分母、重复计划／arm、跨组重复问题、未知arm／无效分数、不完整臂与非计划结果；非成功status必须显式score0，不自动从缺行制造0。输出有理数来源组Δ、分组gain/harm率、题目2×2、question_delta和技术status计数；real_source_independence始终UNKNOWN，NG_data_gate仍HOLD。

实际执行：既有Python3.9.21，独立文档checkout：

    python -B -m unittest discover -s prototypes -p "test_toy_route2_pairing.py" -v

**本轮1次，11项PASS、0FAIL、0ERROR、0SKIP；框架suite计时0.001秒**，不含启动／报告费用，没有不同环境重试。测试涉及：

1. 四个配对cells和完整分母。
2. 一题/来源时Δ=(R−H)/n，与组率代数一致。
3—4. 重复group/question/arm和重复计划强制失败。
5—7. 缺臂、−1/2/None/bool/非整数分数及空分母拒绝。
8. failed/invalid/not_started/construction_failed保留，baseline正确时计误伤。
9. 一个两题组全gain、另一个一题组harm：group Δ=0而question Δ=1/3，证明不能按题拆独立单位。
10—11. 同一题跨组重新标记、非计划结果与未知arm拒绝。

不运行真实策略，不读gold标签，不估12帧可行性、源独立性、模型语义或新颖性。toy已通过只验证当前合成算术／错误路径；不批准NG1—NG3。
