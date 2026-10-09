# VLM-BATCH-012：官方采样与strict口径的三层宏观对照

2026-10-09，main72eee14。固定ZIP评测器文本和来源SHA已核，公式、float操作顺序及范围见[代码政策报告](./official-evaluator-code-and-policy.md)。**A采样合同VERIFIED（限说明范围）；B时间质量HOLD；C科学真值HOLD。** 不修改端点、计算模型mAP或声明“全部异常已修好”。

## 6. 全分母与25点正标签差异

strict：已知类、有限数字且0≤s<e≤L；official：按本ZIP的原s/e和先除后乘的25点，inclusive谓词构造每cell布尔标签。多同类记录只贡献一个cell；不能把cell数当token、事件或独立N。

| 记录／标签口径 | Train | Test | 合计 |
|---|---:|---:|---:|
| 视频行 | 7,985 | 1,863 | 9,848 |
| 原token | 49,809 | 16,691 | 66,500 |
| strict接受 | 35,211 | 11,664 | 46,875 |
| strict拒绝（原分母保留） | 14,598 | 5,027 | 19,625 |
| strict接受且official至少1点命中 | 35,211 | 11,664 | 46,875 |
| strict接受却miss全部25点 | 0 | 0 | 0 |
| 全label cell分母：行×25×157 | 31,341,125 | 7,312,275 | 38,653,400 |
| official正cell | **530,129** | **175,341** | **705,470** |
| strict构造正cell | **301,498** | **96,789** | **398,287** |
| official额外正cell | **228,631** | **78,552** | **307,183** |
| 额外／official正cell | 43.13% | 44.80% | **43.54%** |

strict cell集合是official集合子集，实跑检查通过；“差异”是官方参考标签构造差，不是模型正确率、mAP下降或视觉误判。strict并不等价于官方构造，该自加筛选会移去43.54%的official正cell。没有预测分数，**model mAP=NOT_COMPUTED**。

### 动作可映射与miss计数的保守披露

可映射动作token、完全miss token、strict拒绝但仍命中token及视频级有标签影响数均在本机计算，但其中有正小格／与原公开边际相减的小余项，因此对应宏观关联项也为**WITHHELD_LINKED_OR_COMPLEMENTARY**，不发布精确表或可恢复比例。Test完全miss及部分拒绝miss项为WITHHELD_LT10；非未运行，也不是0。

对**end>L且strict拒绝仍命中**，按预先1000宽度粗桶仅披露：Train[14,000,14,999]、Test[5,000,5,999]、整体[19,000,19,999]。这是粗桶上下限，不是精准计数或可用QA数；整体至少19,000条能在官方点网格中有标签贡献。记录命中不必增加cell，因为同类OR可能已覆盖它的全部命中点。

实际合法域内记录本轮均命中点，但合成反例证明短段可能完全miss；不能将这一个版本的0外推为网格全面捕捉动作。标签影响视频数隐匿不影响总正cell对照的宏观判定。

## 7. B层互斥质量与重叠flag

分类先检查质量无效（非finite／非正length／负start／s≥e等），再分within、0≤s<L<e的crosses_end、合法顺序但start≥L的starts_outside。边界等号按此冻结定义，不钳位；与源代码inclusive标签谓词是不同对象。

| 互斥记录质量类 | Train | Test | 总计 |
|---|---:|---:|---:|
| within | 35,211 | 11,664 | 46,875 |
| crosses_end | W | W | W |
| starts_outside（合法start<end的类别） | 0 | 0 | 0 |
| invalid | WITHHELD_LT10 | 0 | WITHHELD_LT10 |
| 原token分母 | 49,809 | 16,691 | 66,500 |

W为linked/complementary隐藏，与invalid等小格联动；原始互斥sum在隐藏前核等于token分母。非互斥flag end>L也为W；start≥L和start≥end有小正计数抑制。**starts_outside=0不表示所有start≥L为0**：先判invalid的记录可同时触发该flag。invalid记录本轮网格命中0，nomap小计数抑制；这不是官方强制过滤invalid的证据。

end>L依然是精确区间真值的质量红旗。official使用它只是点网格标签行为，未查媒体不能判断是裁剪／时间原点／注释误差。未将19,625条“救回为真实正确标注”；parseable／frame-compatible／精确边界可信分别判断。

## 8. P1/P2：限定合法且可采样的可比口径

仅比较①旧strict合法distinct区间、②同样strict且至少有official网格命中的原区间。两者使用原端点，不改边界，也不基于label序列反造实例；②只是记录级可比性核验，不是新算法／筛选优化。

| 几何资格 | 旧strict合计 | strict且grid-hit合计 |
|---|---:|---:|
| P1 gap>0组 | 347 | 347 |
| P1 gap>0.5组 | 313 | 313 |
| P1 gap>1组 | 288 | 288 |
| P1混合歧义组 | 76 | 76 |
| P2异类pair分母 | 142,498 | 142,498 |
| P2 overlap pair | 97,723 | 97,723 |
| P2 strong overlap pair | 73,513 | 73,513 |

这与within记录均grid-hit一致，不意味着旧strict是官方全部记录的合法过滤。P1 gap>0中270组、P2 overlap中67,280对位于另含strict拒绝token的行；原完整实例和跨段关系仍可能缺失。**纯official标签向精确实例P1/P2的扩大计数=NOT_COMPARABLE**：class/point OR标签不保留实例身份，跨域端点不能认证顺序或共现，不能用新“大数字”充科研真值。

## 9. 精度与公开安全

浮点使用源码先除后乘次序，没有时间舍入、缩放、平移或截断；质量保留Decimal规则。实际端到端MATLAB／媒体帧对齐未运行，其他数字域或解析格式可能UNKNOWN，不能声称全域bitwise重现。

所有小正格1—9、相关split/total、父项减子项能还原小余项者联动抑制。质量小格使crosses_end及其record命中／miss细目一起隐藏；range-hit仅给粗桶；隐匿值不能由完整边际／精确比例补出。原行、class/video/subject交叉表、25×class标签矩阵、score、原.m全文、私有路径及source identity均不进入GitHub；真实诊断只有一次，未按真实数据改规则。

## 10. 分层决定与停止

| 层与后续问题 | 本轮决定 |
|---|---|
| A OFFICIAL_LABEL_SAMPLING_COMPATIBILITY | **VERIFIED_WITHIN_STATED_SCOPE**；足以说明原strict过滤与官方源码label构造不等价，可作为后续短域工程标签政策说明，不是完整预测评测实跑 |
| B TIME_RANGE_QUALITY | **HOLD**；质量类型及flags得到文档化，视频外边界／同版媒体坐标未被修复 |
| C P1/P2_EVENT_TRUTH | **HOLD**；不得生成first/second、负事实或视觉关系真值，未知主体／实例／完整序列／真实PTS和自然来源 |
| 创新／长域／GPU | **RETAIN0／FAIL作为单独自然长域／BLOCKED** |

技术错配已定位：对官方frame-label对比，不能先套自加end≤L门；对精确event QA，不能把源码采样相容当成区间真实性。用户选择保留Charades不意味着已具备高水平论文创新或长时域真值。下一步若需模型／媒体或时间修订证明，由ChatGPT单独明确权限与科学门；本轮不派013、不扩大下载／评分。

本轮19合成方法1次全部PASS，suite0.007秒；之后固定CSV只读1次成功。0研究HTTP／新数据／媒体／STA／特征／模型／GPU／预测／真实解码，0执行.m，0修改原ZIP/CSV／隔离树／旧原型／manifest／原研究环境。只提交两报告、两新通用程序和一条父结果，push后停止并保留当前聊天。
