# BATCH-007｜三个互斥候选的机制契约（任务3—5）

**候选暂名，不是可发表方法注册。** 三者独立竞争；不合并graph＋三值＋agent。以下理想oracle性质不认证真实pixel完备。原QA答案、未来观察或受保护标签不进入state。独立真实许可／感知／成本门尚未通过。

## 任务3｜M1 开放世界负事实债务

| 同一评价字段 | 定义与边界 |
|---|---|
| **Input state** | S=(D,O,Ω,A,U)：D是明确媒体revision/source group、clip原点、真实PTS/timebase、时间区间／视野／实体量词域；O是evidence ID绑定的观测与可靠性条件；Ω为允许世界，A为显式公理；U为未观察／不可信支持，不是False。 |
| **Domain／blind spots** | “never/only/A前无B”必须先限定量词域、A是哪次发生和B身份。抽样时刻之间、遮挡、画外、未枚举对象、clip截断、版本或时间映射未知都在盲区。全encoded frames也不自动覆盖物理连续时间／相机外世界。 |
| **Predicate** | 非空Cons(O)={w∈Ω:w与所有可信O相容}；若所有w满足φ，TRUE；所有w否定φ，FALSE；混合UNKNOWN。Cons空是INCONSISTENT→UNKNOWN／故障，不准空集vacuity认证。never=∀t∈D ¬E(t)；only／before加入明确实体与时间量词。 |
| **Update** | 同version下新增可信观测后取相容交集、更新未覆盖域；未校准VLM陈述保持hypothesis而非硬事实。revision／时间／来源不相容不并库。不同证据冲突导致一致性故障，不能把较新陈述自动当真。 |
| **Return UNKNOWN** | 还有允许completion可在盲区发生事件，或量词／域／身份／时钟／感知可信性未知。未见positive绝不等于不存在。无正事件、覆盖不完整时不能输出never TRUE，除非另有独立且合法的排除公理；本toy无此额外公理。 |
| **Oracle assumptions** | 真实世界∈Ω；被使用的正／负观测真实；量词域、时间与可见范围穷尽，perception完备且sound；solver正确。现实VLM/检测器目前不满足这些已验证承诺。 |
| **Cost** | u个未知binary slots有2^u completions；显式枚举非免费。单一never在独立slots可用普通mask/positive账本O(|D|)符号计算。部署仍须支付域构建、全部相关pixel观察／感知、decode/IO、模型tokens/VRAM、版本与来源审计。full scan不能当12帧低成本方法。 |
| **Trivial baseline** | 普通三值partial-world monitor与本定义完全相同；恒UNKNOWN虽无假认证但determinate coverage=0，conditional selective risk未定义，不叫风险0。 |
| **Specific falsifier** | O=(0,?,0)的两世界(0,0,0)/(0,1,0)分别使never真/假。若仅O给never TRUE，立即否决。即使fullview报告(0,0)，actual(0,1)的false negative也破坏认证；false positive可错误反驳。 |
| **Direct prior／risk** | OWL2§2–3/4.4已有开放世界／显式负事实；Selective§2–3已有拒答与risk–coverage；NeuS本轮正文UNKNOWN，仅历史时序逻辑风险。当前是已有蕴含语义，不是新增观察算子。 |

**可保证的弱性质**：有限toy Ω={0,1}^T，只按partial slots约束，无额外排除公理。已见1→never FALSE；全slots完美观察且全0→TRUE；不完整且无1→UNKNOWN。这三条在公理内成立，不等于现实全视频事实。记录“未观察时间”有用，但不是独立创新。

“检测器假阴性上界”不能偷换成观察负值后的事件概率：P(det=0|E=1)与P(E=1|det=0)不同。若另行假设每slot在全部现有观测条件下的miss概率≤ε_t，可用Σ ε_t约束域内事件风险；它是**假设性概率风险**，不是TRUE证书，域外盲区仍UNKNOWN。本轮无此校准数据或有效数值，不用旧答案填ε。

## 任务4｜M2 来源依赖的可撤销断言

| 同一评价字段 | 定义与边界 |
|---|---|
| **Input state** | S=(D,E,J,R,C,H)：typed域D；不可变evidence E；AND-premise/OR-alternative justification超图J；revision/evidence有效guards R；未裁决冲突C；revision trace H。每叶绑定source group、canonical provenance、media revision、PTS区间、视野、断言和可信条件。 |
| **Domain／blind spots** | 每条推断的全部实际依赖必须显式。重复源副本不是独立支持；缺clip/PTS或身份映射不跨域合并；不同revision先分域，不默认矛盾或沿用旧支持。图外隐藏依赖、错误视觉事实不被图安全性解决。 |
| **Predicate** | grounded raw support仅从有效叶证据起算；每个J须全部前提，一个结论可有多个J。循环无base不能自支持。同域p与¬p未裁决则CONFLICT/UNKNOWN，冲突及只依赖它的证明不认证；保留独立无冲突替代证明。 |
| **Update** | 明确证据／version失效关闭对应叶或guard；新增矛盾保留双方、置冲突，不自动证明旧事实错误。取变化节点在**完整影响图**上的反向传递闭包（含互补／冲突与metadata guards），重算受影响cone；最后合格支持消失或相关冲突才撤销。 |
| **Return UNKNOWN** | 无合格support、支持／版本／时间冲突、依赖缺失、可靠性未证、环无base；不要explode推出任意结论。无关结论保持仅在完整影响图与纯冻结规则下成立。 |
| **Oracle assumptions** | 叶断言与校验guards可靠；identity/PTS/revision绑定正确；依赖完整、规则sound；替代支持确有效，source相关性不被冒充独立证据。真实事件图生成器无此已验证完整性。 |
| **Cost** | DAG符号closure按受影响节点／justification付费；显式proof families可指数增。记录建图、所有观察／感知、source归并、revision校验、IO/solver/token/VRAM费用；graph缓存不是免费视觉信息。当前规模、fan-out、wall未知。 |
| **Trivial baseline** | 普通AND/OR dependency cache：同typed keys、revision guards、冲突节点、闭包／重算。恒等编码＋更新归纳给∀S,δ₁:ₖ out_M2=out_cache，trace也可相同。经典TMS原文本轮UNKNOWN，不借错MIT链接背书。 |
| **Specific falsifier** | e1→p→a，e2→b；撤e1仅p/a失支持，b保持。加e3→p后撤e1，p/a应保留。“删全部descendants”错误；cache精确给相同行为。p/¬p同时可信不能以最新者洗白；同provenance副本失效须一起撤销。 |
| **Direct prior／risk** | ENTER§3.1–3.3/图2有event graph与缺信息更新；SEG§2.1–2.4/Alg1有typed事件图/检索；VideoStir仅历史概要。本轮未核这些系统同撤销公式；但显式cache模拟已否决当前新增算子主张。 |

**最小边界**：只给同一日志e:p的两个世界，一个p真、一个是感知误报，图无法区分。非干扰／局部撤销是完整proof依赖下的形式性质，不是真实断言正确性。任务7仅测有限AND DAG toy与独立DFS baseline；**OR、cycles、冲突传播及真实source/version合同未由该toy实现或实测**，本完整定义不能借12tests说全通过。

## 任务5｜M3 答案不可区分集的证据义务

| 同一评价字段 | 定义与边界 |
|---|---|
| **Input state** | S=(q,D,O,Ω,J,Γ,a_q)：q及完整域metadata D；已验证O；预先合法世界Ω；权限/预算内观察J；各观察的可能outcome Γ_j(w)；答案语义映射a_q。未来outcome和正确答案标签不用于选择Ω。 |
| **Domain／blind spots** | 问题与候选答案本身不提供穷尽worlds。真实答案/世界可能遗漏时须保留OTHER／未建模状态；遮挡、画外、不可访问区间与unknown Γ不能补False，LLM top-k不能当穷尽可行集。 |
| **Predicate** | V={w∈Ω:w与O相容}；答案类C_α={w∈V:a_q(w)=α}。每允许观察j的块B_j,y={w∈V:y∈Γ_j(w)}。确定性完美观察形成partition；噪声Γ是set时块可重叠，为cover。 |
| **Pair obligation** | 对跨答案类记录尚存worldpairs与可测谓词／支持。令S_j(C)=∪_{w∈C}Γ_j(w)：两类support不交才保证单次区分；相交但有独占outcome只可能条件区分；support相同单次不能消类；Γ未知→mapping UNKNOWN，不声称物理不可识别。 |
| **Update** | 合法可信outcome y后V′=V∩B_j,y，重算答案类与剩余义务。未校准soft陈述不能硬删真实world。跨revision/PTS不相容→UNKNOWN。 |
| **Return UNKNOWN** | V非空且只有一个答案类才CERTIFIED_UNDER_ASSUMPTIONS；多类、OTHER、unknown Γ、无可分合法观察、预算／时间／source不明均UNKNOWN。V空是一致性故障，不凭空集认证。义务／clue不是最终答案真值。 |
| **Oracle assumptions** | 真实world在Ω，a_q忠实穷尽，Γ包含真实outcome，观察可信、typed时源域正确、solver正确；相关观察不当独立。像素→world/answer/support的这些映射目前没有可靠构造。 |
| **Cost** | p binary隐藏谓词可有2^p世界；n世界/m观察/k答案类/L outcomes的显式表及类对比较均随其增长。需支付世界建模、相容性求解、所有观察／视觉核验/IO/tokens；固定少帧不保证计算或感知成本低。 |
| **Trivial baseline** | 同Ω/Γ/a_q/solver与cost的强clue planner逐项生成同cross-class义务、support比较、交集更新与UNKNOWN；按历史长度归纳状态/输出相同。恒UNKNOWN coverage0；普通version-space消除亦可模拟。 |
| **Specific falsifier** | 两world仅隐藏slot不同：看该slot的完美oracle可区分；重看相同已见slot虽相关仍不能区分；若所有合法确定性观察序列都相同，强制回答至少错一world。Γ₀={0,?}, Γ₁={1,?}时?保留两类，不能假称完整partition。 |
| **Direct prior／risk** | VideoHV正式摘要直接覆盖hypothesis→discriminative clue→verification；VideoSEAL摘要有answer authority/pixel gate；PACE/TRACE/NeuS仅历史概要／NeuS本轮失败；精确公式是否已实现UNKNOWN，但同输入clue baseline归约否决当前结构区别。 |

噪声的单次support相同不等于所有重复／联合观察不可识别；后者需要合法序列的联合模型。此处不假定独立噪声、不承诺停止／感知证书。题材相关分数也不是可区分性证明；只靠更多额外标签、完备Ω、视觉调用或更高cost赢baseline，不是M3算子的贡献。

## 共同形式／真实边界

三者都要求先有真实world与观察可靠性；不能把生成caption、QA答对、帧字段或toy truth当公理已经满足。具体反例可否决错误规则；oracle正例只证明不恒UNKNOWN，不证明相对最强基线有效。**当前均无不可被匹配经典基线表示的新算子，暂不保留。** 数据／成本由[现实门报告](./feasibility-and-baselines.md)核，toy由[形式报告](./formal-limits-and-toy-results.md)单独记单位与真实执行，不自动转成创新PASS。
