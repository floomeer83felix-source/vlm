# VLM-BATCH-008：可证伪问题与直接先例（任务5—7）

2026-10-09，main eb2c53f。**机制RETAIN 0**；最多保留P1/P2两个待资格核验的测量问题，不是新算法或已发现现象。没有读取实际区间、句子、真实答案，没有模型输出；以下阈值是待冻结的设计示例，不是已启动预注册实验。

## 5. P1：同类重复实例的错误时间绑定

**问题粒度**：同一个视频v、动作类别c、被独立语义依据指定的目标实例i，输出一个区间或明确拒答。比较错误绑定至另一个同类实例的比例，不能把“所有同类moments的检索”与“指定一次发生的定位”混为同一目标。若没有合法明确的目标指代，只能测试all-instance detection，不成立ordinal查询。

### 资格与分母先于看模型结果

1. 根据已许可、固定revision的区间记录找到同video/class的至少两条候选。先审重复行、连续动作分割、合并标注、不同actor/object、相同类名但不同语义；两条记录不自动是两个物理实例。
2. 采用半开区间设计I_i=[s_i,e_i)，须0≤s_i<e_i≤duration；官方端点约定及误差核定后才能落地。明确间隔s_j−e_i>δ，δ须来自注释精度／已审政策，不能按效果调。接触、同类重叠、嵌套、误差范围内近邻及实例切分不明者不进确定ordinal子集，保留资格失败数。
3. “first/second”真值额外需要该类目标域中的完整实例序列、主体／对象一致性和无未标中间实例；现固定类共识声明不足以提供这些保证。不能由未标造never，也不能自动将行序当时间次序。
4. 全合法资格源为计数框，按participant／session／video来源层冻结探索、校准、确认，模型表现不参与资格筛选。报告候选video-class组数、确定／歧义实例组、问题数及保守source组，**各数量均UNKNOWN**；66,500是总区间声明，不是重复资格分母。

### 指标与否决

对target I_i和输出J，tIoU(J,I)=|J∩I|/|J∪I|。示例固定阈值τ=0.5：若target未达τ，而另一个确定同类实例达τ且唯一best-match，则记**wrong-instance**；target命中、其它定位错、拒答、非法输出、技术失败另列。tie或边界不确定记AMBIGUOUS，不偷偷当正确。主分母为全部planned资格问题；可另报有效定位中的条件比例，但不能替换主分母。

拟主要效应是重复资格组与事前匹配单实例组的错误率差；匹配class、持续时间、目标相对位置、场景／主体、可见性等，其所需字段缺失保持UNKNOWN。差值是关联测量，重复与单实例组并非随机化，不能称重复“导致注意力错误”。目标身份正确但边界漂移、主体识别失败与同类交换分开。按保守source聚类，样本量／效应阈值／功效／置信区间参数均待真实资格数，不能承诺20源或旧实验吞吐。

强对照：同输入／同费用的标准TAD实例集合预测，再以合法查询规则绑定；语言定位CTRL式方法；合法多moment模型和明确all-instance任务上界。全量感知oracle只是分析上界，额外编码器／token／观测不能隐藏。冻结后如新策略有配对比较，纠错=基线错新策略对，误伤=基线对新策略错，均以全部planned计数，保留失败与拒答。

**P1反证条件**：无可复核同类不重叠实例；ordinal所需完整性缺失；只是同一连续动作拆行；目标文本本来容许多实例；匹配后无事前有用差异；强标准检索已解释该错误。前四项阻止P1测试，不通过编造问题补齐。当前判定**POTENTIAL_MEASUREMENT／IDENTIFIABILITY UNKNOWN**，不保留新机制。

## 6. P2：异类重叠与边界／归因混淆

多标签TAD的目标是category及所有区间；STA的目标是给定sentence的moment。两者分别评分，不能把类间并发与一个句子对应多moment混用。原Charades25点frame-mAP也不是本区间测量，见[标注合同](./annotation-and-join-contract.md)。

设计候选对为同video的异类I_A/I_B。定义overlap_ratio=|I_A∩I_B|/min(|I_A|,|I_B|)，另报tIoU。示例强重叠阈值γ=0.5；非重叠对要求相隔>δ；中间／端点不确定分层，不事后挑阈值。相同、包含、部分交叉分别报告；同类重叠回到P1歧义，不并入清楚异类对。label互斥性、主体不同、对象相似和注释完整性均需另审。

主测量可设为匹配非重叠对照后的target区间定位失败差；副指标为起点／终点有符号偏差、绝对偏差与duration归一化偏差、跨类别错误归因、漏检／重复检测。预测集与参考用冻结的一对一匹配，每参考／预测最多匹配一次；避免多输出重复命中同目标。仅讨论关系QA时必须有单独合法真值，不从tIoU直接生成无歧义自然语言答案。

输入只给合法任务说明、类别或sentence及批准后的视觉内容；不提供target边界、ordinal答案、重叠标签、参考相似度或未来回答给selector／prompt。annotation只用于事前资格构造与评分侧，需冻结双投影。匹配难度字段中的缺失保留，不通过模型判断补真值。本轮没有实施任何投影。

强基线必须包含多标签TAD的边界与实例联合预测、标准TMR及同成本固定观察基线；若仅用uniform或旧S_q/S_t比较，不足以建立新机制。一般“加边界head／更密采／图关系／两次核验”均有直接先例风险。

**P2反证条件**：无确定异类重叠资格；真实时间坐标不相容；定位错误可由粗采样、目标短、文字欠指明、可见性或注释误差解释；强TAD对照消除差异。配对更改的纠错／误伤和成本要完整报告，无观测输出当前均UNKNOWN。判定**已有TAD对象上的POTENTIAL_MEASUREMENT；新算法NO-GO**。

## 7. 六项直接先例：五个正式摘要＋一个方法预印本

未下载PDF；最多6论文页面。检索仅定位官方URL，搜索片段不升级为全文证据。以下覆盖是对已读内容的判断，缺失全文不能作新颖性clearance。

| 先例与官方URL | 实读层级／直接对象 | 对P1/P2/STA的裁决 |
|---|---|---|
| [Hollywood in Homes，ECCV2016](https://publications.ri.cmu.edu/hollywood-in-homes-crowdsourcing-data-collection-for-activity-understanding) | 正式机构摘要：短视频、类标签／区间／对象／描述，动作识别等baseline | 重复资格数量和ordinal协议未证；普通动作区间定位REPLICATION_ONLY |
| [Much Ado About Time，HCOMP2016](https://ojs.aaai.org/index.php/HCOMP/article/view/13290) | 正式摘要：时间数据多标签众包，共识降低成本但worker不完美 | “exhaustive”不等于无误物理真值；全部episode与边界过程正文UNKNOWN |
| [TALL，ICCV2017](https://openaccess.thecvf.com/content_iccv_2017/html/Gao_TALL_Temporal_Activity_ICCV_2017_paper.html) | 正式摘要：语言／clip匹配，alignment及boundary regression，提出STA | STA普通句子moment定位REPLICATION_ONLY；指定同类ordinal混淆的精确协议UNKNOWN |
| [Dual DETRs，CVPR2024](https://openaccess.thecvf.com/content/CVPR2024/html/Zhu_Dual_DETRs_for_Multi-Label_Temporal_Action_Detection_CVPR_2024_paper.html) | 正式摘要：multi-label TAD，instance/boundary两级query、联合初始化与互补修正 | P2计算对象已有直接方法。全文／Charades具体协议及结果本轮未实读，不冒充其消融已核 |
| [When One Moment Isn't Enough／FlashMMR](https://arxiv.org/html/2510.17218) | v1，2025-10-20，**方法HTML预印本；正式录用UNKNOWN**。§2/3.3/4/5：一query多moments、集合评估、边界及语义核验、multi/single目标分层 | P1的“首次提出同query多个片段／核验边界”NO-GO；指定实例交换与all-moment retrieval不同，独特价值仍UNKNOWN。论文对长度／标注／许可的声明未在数据侧验证 |
| [TIME，AAAI2026](https://ojs.aaai.org/index.php/AAAI/article/view/38002) | 正式摘要：Video-LLM五维时间理解、时间敏感任务与shortcut过滤 | 泛称新时序／排序评测不新；Charades实例筛选、是否排重复及顺序生成方法正文UNKNOWN，不用检索PDF片段补细节 |

FlashMMR的方法实读不提供STA权利，也不能证明本批Charades存在ordinal真值；其多moment数据声明不能给本项目来源／自然长视频确认集放行。其强方法的训练、特征、post-verification费用需未来同输入成本比较，本轮不复现。全部新Qwen模型换基座、按时长分层、加计数或报告新名字都不能消除对象重合。

### 总裁决

STA基本定位、异类重叠TAD、同query多moment是已有对象；作为新算法主张**NO-GO／REPLICATION_ONLY**。P1的指定实例误绑定和P2受控错误分解可暂列最多两项未验证测量，需要真实合法资格与强基线才有信息价值；本轮既没有证实错误现象，也没有发现可发表创新。**机制RETAIN 0，最终长视频论文GO继续HOLD。**
