# VLM-BATCH-003 C：G1无答案元数据与12帧条件技术合同

日期：2026-10-08，北京时间。仅据已验收的[VLM-002报告](../VLM-002/dataset-metadata-review.md)、本包[A](timestamp-contract-audit.md)／[B](source-provenance-audit.md)，以及[PR #1预注册草案](https://github.com/floomeer83felix-source/vlm/blob/df892ee7a2100c632d08cc4cacd25e3aa32d12e6/docs/next-hypothesis-preregistration.md)。PR为OPEN／DRAFT，head `df892ee7a2100c632d08cc4cacd25e3aa32d12e6`，文件Git blob `a197b7c8f006cf15ca1fb8be70fe48166102c4d7`；未合并，不是数据可用证书。

本轮无新增数据集检索／页面核查，未重复VLM-002的23响应或404；只获取任务仓库及明确引用的PR文档。没有创建可执行manifest或运行代码。

## 1. G1条件状态

“已证实”限已验收元数据报告的字段／版本事实；不表示本轮再核原始数据。作者声明、UNKNOWN和不满足不得升级为PASS。

| 条件 | VES-Bench | HERBench | CaST-Bench |
|---|---|---|---|
| 注释／媒体许可 | UNKNOWN／UNKNOWN | 已证实非商业数据声明；上游视频条款UNKNOWN | 已证实注释CC BY4.0；SAV媒体条款未核准 |
| 问答及证据schema | 文件目录已证实，问答区间字段UNKNOWN | 问答列已证实，嵌套支持字典UNKNOWN | evidence字符串列已证实，内层字段来自公开字典，实际记录未核 |
| 联合必要、三段不重叠 | 联合必要是作者声明，逐题段数UNKNOWN | ≥3线索是作者声明；用MRFS替代必要区间**不满足** | 因果链是作者声明；逐题≥3、不重叠及严格必要性UNKNOWN |
| 同版PTS／裁剪桥接 | UNKNOWN | UNKNOWN | UNKNOWN；mm:ss和逐秒框不是PTS |
| 历史／事件独立性 | UNKNOWN | UNKNOWN | UNKNOWN；视频文件数不是独立组数 |
| 12唯一源帧、两个外部背景池 | UNKNOWN | UNKNOWN | UNKNOWN |
| 评分隔离 | 未来必须独立，尚无新实现 | 同前；5选项需新审查 | 同前；6选项需新审查 |
| G1 | **HOLD** | **HOLD** | **HOLD** |

不承诺可行题数、k值、40独立源或干预效应。已知本地名义index/FPS路径及450缺项不会因选择另一数据集自动消失。

## 2. 无答案元数据投影：最小设计字段

此表是未来合同建议，不是已创建的新manifest；所有必须项UNKNOWN时阻塞对应对象，并保留原因。

| 字段／类型 | 必需性与追溯规则 |
|---|---|
| `record_id: string` | 必需，仅稳定定位；不由答案或表现筛选，不公开私有真实ID |
| `source_group_id: string`, `group_basis: enum` | 必需，按B的保守规则与证据版本；不能把单视频hash称事件独立 |
| `provenance_partition: enum`, `exclusion_status: enum` | 必需，原split／实验角色分开、历史探索／保护污染传递；test不得默称train |
| `dataset_revision`, `annotation_sha: string` | 必需，绑定官方声明及实际文件版本；schema metadata不是实际媒体证明 |
| `media_revision`, `video_sha`, `parent_media_ref: string/null` | 前二必需；parent关系所需时必需，字节与源语义版本分开 |
| `clip_time_origin`, `clip_offset`, `source_time_mapping: rational/object` | 桥接必需，含单位／原点／变换依据；未知不默填0，不裁剪或钳位端点 |
| `stream_index: int`, `time_base: rational`, `frame_pts: list[int]` | 运行映射必需；media元数据未准入时可仅列UNKNOWN；不以FPS补齐 |
| `reference_intervals: list[{start,end,unit,semantics}]` | 必需，原值、必要性依据、闭／半开与精度；关键帧替代区间须另审定义 |
| `candidate_frame_refs: list`, `anchor_refs: list` | 构造时必需，实际源帧命名空间、PTS/RGB绑定；当前未取样 |
| `question_public_ref`, `choice_schema` | 构造器依法可访问的公开文字定位／选项合同；不含正确选项 |
| `clock_status`, `failure_reason: enum/string/null` | 必需，缺失／冲突／失败保留；不补最近帧、不事后替换对象 |
| `duration`, `nominal_fps`, `resolution` | 可选诊断，不能替代PTS、桥接、源组或必要性证明 |

正答值、answer_index、逐题correct／后验和私有标签不进入投影。原文件若混有答案，需另获准的隔离投影程序，在解码值前跳过非允许字段，不能先读整套数据再删答案。参考注释是离线干预构造信息，不给回答模型或部署策略；gold单独交评分器，评分不影响采样／执行。

## 3. D1/D2固定12帧的前置不变量

继承PR草案的研究问题和角色，不把它批准为实现。D0是辅助部署基线；D1／D2为主配对，D3为辅助操作性诊断。本轮不新增模型调用或改其科学定义。

1. 问题、模型／处理器版本、输入像素和输出解析先冻结；同一题按来源规则入组，不能用正确性或SigLIP表现选择可用题。
2. 必要性依据、区间坐标和媒体版本成立，至少三个非重叠参考时段具备实际可接受帧；每锚点必须在其时段内。区间中心最近帧／可信参考关键帧优先规则来自草案，但坐标、容差及稳定tie仍需在真正协议里明确。
3. 记锚帧数为尚未知的k；需k<12、所有参考支持可覆盖。D1与D2的锚点ID、RGB和真实PTS完全相同；各臂恰好12个**唯一源帧**，不以重复提供或patch数充数。
4. 用全部参考区间的并集定义外部补集，边界与不确定度先声明；外部不等于语义无用，可能仍有未标注支持。两个符合草案的外部候选池和背景集合关系须预先核实，无法满足不通过相邻补帧或减少预算救援。
5. D1的其余12−k槽采用规定的中性均匀背景；D2使用区间外问题相似度排序；二者保持草案要求的相同时间分布／几何、时间顺序及预算可比。不能用grounding答案或事后模型分数构造“高干扰”集；不自行拟合阈值。
6. D3的预定区间移除需确认其他剩余帧也不覆盖该区间，且“必需”确有上游依据；否则只标构造不适用，不能解释为语义证据已移除。
7. 保存每臂提供槽／内部patch／显示时间与融合前源帧映射，覆盖按源PTS判定，不按双帧平均标签；token或实际成本差异必须报告，不能加dummy调用装作公平。
8. 参考数据、12帧集合和全部失败原因在看结果前冻结。执行中失败／空答计0，保留全计划分母；D1正确而D2失败必须计误伤。合法未购买规则与本诊断四臂不能混用。

不可执行环节：许可、逐题支持及必要性、媒体版本／PTS映射、完整来源隔离、两个背景池、处理器接口与预算均未获新实证。本合同不造k、帧列表、样本量、时间／显存上限。PR中的40–60组与240调用只是草案规划，不是本轮资源放行或科学功效保证。

## 4. 最多三项下一轮澄清建议（未执行）

1. **一份无答案字段与许可请求草案**：优先VES作者，询问注释和视频许可、正式问答split、参考区间定义／单位／必要性、裁剪／同版视频manifest。只请最小schema／版本资料，不索原答案。邮件／issue均未发送；若无授权／字典则维持HOLD。
2. **一项受限版本／来源投影审查**：需新任务授权与足够官方元数据，核parent／clip／revision及历史排除域、残余缺项政策；仅目录字段不解决跨事件独立性，不承诺40组。不扫描媒体或填平450缺项。
3. **纯合成时钟与构造合同验证**：若ChatGPT另行指派，使用A的纯有理时钟、toy来源和外部补集边界验证，不需GPU或视频；真实PTS/RGB/clip桥接测试仍须另一授权，不能用toy通过替代G1。

若三候选仍无法提供许可、可机械投影的支持字段和可信同版坐标，停止该固定覆盖诊断或由ChatGPT重定义其测量对象；不改成MRFS真值、不换保护旧题救援、不无限扩资料链。若数据合格但独立来源／外部池不足，只报告不足，不能降低三段、12唯一帧或来源门补样。

## 5. 裁决与资源

**条件技术合同完成，G1／新manifest／GPU继续HOLD。** 可建议下一轮低成本澄清，不替ChatGPT作创新保留／任务解封。未来新GPU至少仍需数据许可／桥接／隔离、明确功效与成本、锁持有核验、不可重放的持久账本和用户授权。

本轮新增数据集检索、视频／完整标注下载、模型QA、测试／解码执行和原资产修改均0。仅读取已批准报告、相关静态代码／聚合字段及固定PR文档，未合并PR #1。整包A/B/C提交后停止。
