# 未评分入口准入报告

2026-10-31。结论：**OBSERVATION_QUALIFIED_UNSCORED_ITEM_TRANSFER_ENTRY**，可提出一个VIDHALLUC冻结旧头描述性迁移方案；**不是独立来源确认**。TempCompass及TimeBlind均无当前文法的直接入口。全模型/媒体/训练NOT_RUN；本报告不授予评估执行权限。

## 1 固定版本与完整分母

DyBench固定`fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405`，TimeBlind HF固定`bafceda3a2bd0e5128c390ec25fdc54e470a743d`，作者代码固定`03129551918c0830f3ee727485eb9cfb437e21e5`。仅获取合同指定JSON/JSONL、数据卡、作者README/tags/utils及各一页固定版本文件树；没有跟随页面中的安装、模型、克隆或LLM judge示例。公开入口见本目录[source-brief](source-brief.md)，所有原文/投影/成员身份只在新私有根。

DyBench共814行/407个名义两视频配对：Breakfast294行/147对、50Salads100行/50对全部排除，不重开其中未曾纳入的成员；剩余VIDHALLUC382行/191对、TempCompass38行/19对为观察候选，210=191+19。类型名只表明发布池，不证明原始录制独立。

| 分支 | 名义/完整配对 | 原Action1/2解析可用 | 解析失败 | 事件规范化不同且原tau闭包 | 拟新增评分 |
|---|---:|---:|---:|---:|---:|
| VIDHALLUC | 191/191 | 191 | 0 | 191 | 50对/200格 |
| TempCompass | 19/19 | 0 | 19 | 0 | 0；NO_DIRECT_ENTRY |

VIDHALLUC全部成员满足原original/reversed命名、两行同一问题、唯一成员与event_sequence字段。仅从原显式Action1/2保留事件原文，按060原before模板生成两问题；062 tau代码AST相同，逐题tau(tau(q))=q成立，未另造parser或利用答案决定问题方向。TempCompass19对不匹配同一结构，记EVENT_PARSE未决，而非作者标注错误、科学阴性或把其单事件自然语言改写成两事件。

## 2 观察资格、标签结构与选择严格分开

读取角色先保存原正文，立即生成仅含观察字段的投影。准入角色只用这些投影及无答案的标签索引，未读answer/candidates或旧模型结果。全部观察资格、固定规则与私有50对名单先封存，之后结构角色才读取本次公开publisher答案与候选项核标签关系。

VIDHALLUC191对的publisher两种次序标签与候选项均互补；固定已选50对全部通过，失败0、未知0。四格标签由两视频与确定生成的两问题形成，而不是用其他格预测翻转当前答案。没有按答案结构重新挑选成员。此结论为**PUBLISHER_COMPOSITE_QA**一致性，不等同逐成员剪接/动作/非重叠时间戳审核；本轮没有新的人工真值。公开答案已在读取和结构角色中可见，负责人此前也见过页面预览，不能称从未接触标签或新的完全盲测。

按最高可证来源键整体排序；本次元数据未给出原录制/参与者/摄像机映射，故退至“子来源命名空间＋两视频配对身份”的最低单位。用公开域标签VLM066/heldout/与私有组键的SHA256字节序排序，按上限50整体纳入；191个最低单位各含1实例，前50对固定，余141对仅因容量不纳入，不按语义难度或分数剔除。私有名单、排序键及hash均不公开。

选中50对有100个唯一视频身份、100条原模板问题，tau闭包并集仍为这100条问题。所选事件或生成问题与全部被排除的Breakfast/50Salads公开文本的字面重合均为0例；这是对全部旧类别的字面描述，**不是train84覆盖核对或语义未见证明**，不参与选择。既往任务公开范围没有对这两新子类进行模型评分，此次“未评分”依据为原公开任务/成员类别范围，而非私有预测盘点或物理预训练无暴露认证。

## 3 TimeBlind索引、题型与接口边界

JSONL共2400行，index为0–2399且逐行一致、无重复：yes_no1200行、multiple_choice1200行。Temporal_Relation标签有432个唯一行索引。官方utils的build_answers明确以index//4分组、index%4赋角色，顺序为q0_i0、q0_i1、q1_i0、q1_i1；get_tag_scores按排序索引四行分块。静态源码与实际索引块共同核验，而非只凭432除以4猜分组。

432行对应108个完整四格组：yes_no54组、多选54组。108组均满足两视频/两问题的q-major重复绑定，且与全局四索引块对齐；其公开精确视频配对键为108个、重复簇0。文件身份唯一不证明108个独立原始录制。tag是任务范围标记，不认证严格先后、非重叠或当前D文法。

对432个候选原问题逐条尝试未改的062 tau，兼容0、格式不兼容432；对全2400原问题的补充观察检查也为0。原记录无显式Action1/2或事件字段可直接沿用060生成规则，故DIRECT_FORMAT_COMPATIBLE=0，**关闭直接套用当前D的TimeBlind入口**。原生yes/no与多选格式也不能通过作者建议的回答后缀变成当前完整before模板；互补问题不是tau从当前问题派生的替代物。

结构角色起初只核yes/no值，得到54个互补组和54个原生多选未解释组；随后依据同一官方代码中A/B的原生二元映射，另列题型结构核验：yes/no54组、A/B54组均为对角互补，失败0。初始未解释状态保留，未改观察资格或0兼容结论。该结构一致性既不是严格before语义认证，也不是任何模型分数；没有重写多选题、换parser、调用judge或下载视频求解释。

## 4 来源、许可和可验证性分层

| 分支 | UNSCORED_ITEM_CANDIDATE | AVAILABLE_SOURCE_KEYS | DIRECT_FORMAT_COMPATIBLE | PUBLISHER_RELATION_EVIDENCE | PHYSICAL_SOURCE_INDEPENDENCE | 模型 |
|---|---|---|---|---|---|---|
| VIDHALLUC | 191观察候选，固定50 | source_category/subcategory为发布池；配对文件身份为最低单位，191键/0重复簇 | 191；选50 | 191互补一致；选50一致；成员构造/严格非重叠未知 | UNKNOWN | NOT_RUN |
| TempCompass | 19名义对，原事件结构未决 | 发布池及19个两视频文件身份；没有可证更高原录制键 | 0；19解析未决 | 未为不兼容题生成四格标签，NA | UNKNOWN | NOT_RUN |
| TimeBlind | 108名义四格组，不作为本配方可评估成员 | index为行；四索引组；108精确两视频键；没有原录制/厨房链 | 0/432原候选问题 | 原生题型108互补一致；严格before关系UNRESOLVED | UNKNOWN | NOT_RUN |

DyBench数据卡带MIT标签并说明配对反事实及事件顺序任务，但不能由该标签认证全部原视频权利或成员级拼接。TimeBlind卡说明限学术研究用途并保留侵权处理说明，未给出逐成员原录制链或可外推的全部视频授权。没有联系作者或请求访问。后续媒体使用条件须单独核准；当前来源未知不等于新条目一定无用途，但只可提出有限条目迁移描述。

固定DyBench文件树列出event_sequence媒体归档2783546023B，没有列出可直接请求的独立MP4。本轮没有打开归档/目录/成员，现有旧包的本机存在、身份及可复用性均UNKNOWN。TimeBlind文件树只取首个1000条目录页，响应给出后续页链接；未追页，996个已列MP4/3192915547B只是该页小计，不能报为全库。总媒体及所选成员解码字节未知，不读媒体补齐它们。

## 5 核验与结论

独立stdlib脚本从原始公开元数据重建814/407、子类分区、原解析/tau闭包、无答案投影、50对固定选择、TimeBlind2400行/432索引/108绑定及原生题型结构，8009项核对通过，没有import本审计器或研究模块。原文、投影、名单前后身份一致；初始准入源码可按后加静态详情函数的差分精确重建并匹配首次读取前身份，tau AST与原062一致。独立脚本首次漏掉私有组键的子来源命名空间而停止；修正核验公式后通过，未动名单/规则/答案或重新运行准入。

可行主入口仅VIDHALLUC50对，详见evaluation-proposal.md；它解决的是未评分条目上的冻结相对效果，不能修补原063绝对目标失败或宣称核心创新。TimeBlind与TempCompass本轮止于NO_DIRECT_ENTRY，不以另一个问题、人工改写或新头延续。所有推理、训练、媒体及旧私有资产读取仍为0。

固定公开入口：[DyBench](https://huggingface.co/datasets/ddz16/DyBench/tree/fc9a9e8dbd11107fa47f953f1367c0bcd2dbb405)、[TimeBlind数据](https://huggingface.co/datasets/BaiqiL/TimeBlind/tree/bafceda3a2bd0e5128c390ec25fdc54e470a743d)、[TimeBlind作者代码](https://github.com/Baiqi-Li/TimeBlind/tree/03129551918c0830f3ee727485eb9cfb437e21e5)。
