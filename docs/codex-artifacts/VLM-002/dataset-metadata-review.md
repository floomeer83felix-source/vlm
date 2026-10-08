# VLM-002 公开证据数据集元数据核验

- 检查日期：2026-10-08，北京时间；依据 `main` commit `19a4e42` 的唯一 READY 任务。
- 范围：先核TRACE/VES-Bench、HERBench；两者的G1关键字段／许可仍不足以确认后，简查CaST-Bench。
- 新模型／QA／训练／评分前向、视频解码、视频／模型／压缩包／完整标注下载：均0。未读取本地答案、评分标签或保护身份映射，未修改研究工作区、环境、锁与旧账本。
- 实际访问：官方摘要／项目页面、README、USAGE_GUIDE、许可证、GitHub版本元数据、HF仓库文件目录及Dataset Viewer **info schema**；没有访问 `rows`／`first-rows` 或实际标注文件。
- **结论：元数据任务完成，G1数据门未通过，VLM-003／004建议HOLD。** VES-Bench与命题最匹配，可优先补核其许可与问答字段；CaST-Bench的公开字段字典最清楚，但不是已确认的长视频／三段联合必要样本；HERBench不能用MRFS代替参考证据区间。

## 1. 证据级别与汇总

“PASS”仅针对已列元数据条件，不表示实际样本、独立来源或PTS通过。“FAIL”表示本次指定接口未提供所需内容；不推定数据集全局不存在字段。“UNKNOWN”不作通过处理。

| 候选 | 标注／视频许可 | 实际schema证据 | 时间与媒体映射 | 三段／12帧／区间外池 | 总体建议 |
|---|---|---|---|---|---|
| VES-Bench | 标注和视频均UNKNOWN；HF无license card，所查GitHub根目录无许可证 | 公开文件目录确证Parquet与348个MP4；Viewer info仅有`video: Video`，未得到600题问答／区间schema | 官网声明提供源视频和观察记录；具体时间字段、单位、版本裁剪与PTS未知 | 联合必要证据集有官方声明；真实每题段数、不重叠、锚点和区间外池UNKNOWN | **HOLD G1**；优先许可＋无答案问答字典补核 |
| HERBench | 数据卡CC BY-NC-SA 4.0，非商业研究用途；代码MIT不能覆盖数据；视频沿各上游权利 | Viewer确证问答列与`metadata_json`字符串；详细数据字典链接404，未确认嵌套支持区间 | `duration`为秒；ID／path与revision存在，原视频版本、裁剪和真实PTS未知 | ≥3不重叠线索是作者设计声明；MRFS为模型／selector依赖指标，不能当逐题锚帧真值 | **HOLD G1**；需嵌套字典和上游视频条款 |
| CaST-Bench | 注释CC BY 4.0有明确声明；视频适用SAV原条款，本轮未核准其使用条件 | Viewer确证`evidence: string`；README提供内层区间／实例／逐秒框字典 | `mm:ss`区间＋整数秒框键；MP4与SAV实例引用可见，裁剪偏移、VFR／PTS未知 | 证据链并不保证每题≥3段不重叠；<12锚点及区间外池UNKNOWN | **HOLD G1**；可作字段明确的备选，不能当已合格长视频集合 |

## 2. 来源与版本

| 资源 | 已确认版本与元数据范围 |
|---|---|
| TRACE论文／主页 | [arXiv:2608.22516v1](https://arxiv.org/abs/2608.22516v1)、[作者项目](https://buaa-colalab.github.io/TRACE/)；仅摘要和主页，不下载PDF／全文大文件 |
| TRACE仓库 | [commit `1b60646dd37657e01b66060bc637742e5d4b5db7`](https://github.com/buaa-colalab/TRACE/tree/1b60646dd37657e01b66060bc637742e5d4b5db7)；实际根目录只有README与assets；README与该commit的Git blob匹配，方法实现标为coming soon |
| VES数据 | [HF revision `b1cdbb370ad866090e6fec82ccb9e699b10edbc7`](https://huggingface.co/datasets/buaaplay/VES-Bench/tree/b1cdbb370ad866090e6fec82ccb9e699b10edbc7)；API修改时间2026-06-06，`gated=false`；看到文件目录，不取得Parquet或MP4 |
| HER代码／说明 | [commit `fe66f377fd4a4a1689b97837129edbaacd489ebe`](https://github.com/DanBenAmi/HERBench/tree/fe66f377fd4a4a1689b97837129edbaacd489ebe)，代码MIT，README指向使用指南 |
| HER数据 | [revision `30b42e97180f2c7c0fdc3f2aed412ae04f0366ca`](https://huggingface.co/datasets/DanBenAmi/HERBench/tree/30b42e97180f2c7c0fdc3f2aed412ae04f0366ca)，API修改时间2026-06-06，公开且非gated；卡中v1.0.0描述清理后版本；三个config均声明test |
| CaST数据 | [revision `8628e6243f5c4be4f61f18849f92ba60b58e7f6e`](https://huggingface.co/datasets/wovenbytoyota-vai/CaST-Bench/tree/8628e6243f5c4be4f61f18849f92ba60b58e7f6e)，API修改时间2026-07-03，非gated；卡声明v1为部分发布、`test` split |
| CaST主页 | [Woven官方项目](https://woven-by-toyota.github.io/CaST-Bench/)；其评估仓库链接查询404。数据卡使用另一主页域名，本轮未据此假定两个站点文件完全同版 |

HF API中的revision与文件目录是实读版本信息。Viewer info没有返回对应数据revision，本轮没有证明其缓存与上述commit原子一致；Viewer的列类型／题数需由后续受审查的版本绑定再核对。

## 3. VES-Bench：语义匹配度高，但许可与实际区间字段未确认

[官方README](https://github.com/buaa-colalab/TRACE/blob/1b60646dd37657e01b66060bc637742e5d4b5db7/README.md)声明600题、348个长视频，任务包括顺序与计数；其证据集被定义为联合必要，覆盖评价分别检查每个区间至少1／2／3个解码帧。以上是作者文字定义，不是本轮逐题标注验证。

实际HF目录有 `VES-Bench.parquet` 与348个视频文件名。没有读取任何文件内容。官方主页还声明可回放观察时间戳；**这不等于真实PTS或同版本裁剪已实测通过**。

[Viewer info接口](https://datasets-server.huggingface.co/info?dataset=buaaplay%2FVES-Bench)实际返回videofolder builder、`video`列、`train` 348个examples。这个train是自动视频folder的查看器split，不能当600题的官方训练分区，也不能把348 examples当348个独立来源组。问答字段名、区间类型、秒／帧坐标、题目split和媒体版本校验字段仍UNKNOWN。本轮没有下载Parquet、读取footer或获取答案样本补齐缺口。

HF API `cardData=null`、所查根目录无LICENSE；论文的CC BY 4.0标记是论文许可，不能移用为注释或视频许可。网页和非gated状态均不代替使用授权。

**后续最小G1动作（建议，不执行）**：取得作者提供的无答案字段字典和注释／视频使用条款，明确问答split、各interval边界／单位、video来源标识、裁剪／转码版本及哈希；再由独立协议核查参考区间数量与外部候选时段。若只有完整含答案Parquet，不应在采样器中直接打开，需要新任务明确隔离的元数据投影。

## 4. HERBench：列schema可确认，参考支持仍藏在未核实的嵌套内容中

[固定revision README](https://huggingface.co/datasets/DanBenAmi/HERBench/blob/30b42e97180f2c7c0fdc3f2aed412ae04f0366ca/README.md)及[Viewer info](https://datasets-server.huggingface.co/info?dataset=DanBenAmi%2FHERBench)均提供问答列定义。实际info返回：`question_id`、`video_id`、`video_path`、`question`、`choices`、`answer`／`answer_index`／`answer_text`、`task_type`、`source_dataset`、`duration`、`resolution`、`metadata_json`。这里只读取**字段名称／类型**，没有读取答案值或行记录。

full/test有27631题，lite/test 2000题，lite_v2/test 1971题，均为服务器元数据而非本轮下载计数。README报告335视频，四类来源分项数量合计337；没有逐视频目录核对，不消解这个差异，更不把任一数当独立来源组数。官网“26K”与清理后card的27631也应按版本区分。

[使用指南](https://github.com/DanBenAmi/HERBench/blob/fe66f377fd4a4a1689b97837129edbaacd489ebe/USAGE_GUIDE.md)把MRFS定义为某模型与selector下首次答对所需帧数，可为0或undefined。因此均值约5.49不能用于推定每题有5.49个必需锚点，亦不能保证12帧足够。页面关于至少三个不重叠线索的设计声明，尚未在无答案schema里找到逐题区间／参考帧列表。

README所引 `data/README_DATA.md` 在已固定代码commit下返回404；HF文件清单也未列该字典。本轮不继续全文标注探索。`metadata_json`的内容结构、哪些任务有局部支持／全局不存在性需求仍UNKNOWN。

数据卡明确CC BY-NC-SA 4.0及非商业研究／教育范围；视频权利保留给WildTrack、HD-EPIC、PersonPath22与原平台等上游。代码MIT与视频授权分别处理，本轮未核各上游视频条款，故媒体使用条件不能标PASS。HF提供分片tar及校验清单路径，只看目录、未读取或下载；打包／分片不保证可单独取得同版本视频。

**12帧适配限制**：5选项不同于旧4选项运行器；目前未授权修改接口。全局缺失类问题不能把局部区间覆盖当事实充分性。后续最小动作是取得无答案嵌套数据字典、明确参考支持定义、媒体来源许可和clip时间原点；不要直接把现有test列改名为训练集。

## 5. CaST-Bench：备选的区间字典明确，但不足以放行目标实验

[固定revision数据卡](https://huggingface.co/datasets/wovenbytoyota-vai/CaST-Bench/blob/8628e6243f5c4be4f61f18849f92ba60b58e7f6e/README.md)明确区分注释CC BY 4.0与[SAV原视频条款](https://ai.meta.com/datasets/segment-anything-video/)。本轮只核数据卡对两类权利的说明，没有访问或接受SAV许可、下载视频。代码仓库404不推定代码永久不存在。

[Viewer info](https://datasets-server.huggingface.co/info?dataset=wovenbytoyota-vai%2FCaST-Bench)返回80题/test，列为 `video`、`question`、`question_type`、`scene_category`、`options`、`answer`、`evidence`。`evidence`实际类型是string，内层未实读；“可解码为对象数组”来自数据字典，不是本轮记录执行验证。

字典列出的内层字段：

- `evidence_start_time`／`evidence_end_time`：`mm:ss`字符串。
- `evidence_instance_id`：跟踪实例标识。
- `evidence_rationale`：该片段的因果贡献说明。
- `SAV_instance_id`：上游实例引用。
- `bboxes_in_range`：整数秒字符串键、框坐标字符串值。

不上传实例值、框、题目或答案。HF目录确见56个MP4路径，但这只是发布文件数，不能当80题的56个独立来源组；没有打开视频。字典规定6选项，旧4选项接口同样不可直接沿用。

项目称因果链、通过遮挡过滤和人工核验，不能据此推出每题所有区间都联合必要、至少三个互不重叠或适合长视频。逐秒框与整秒格式不是原视频帧ID／真实PTS；区间闭开端点、SAV全片还是裁剪片、偏移／转码、VFR及帧精度仍UNKNOWN。

**后续最小动作（建议）**：核SAV媒体许可与同版clip manifest；取得只含video ID／源版本／区间坐标及数量的隔离投影，确认是否实际有三段合格支持、持续时长与区间外候选池。不得因整套JSONL只有约138KB而下载完整含答案数据；本轮没有读取该文件。

## 6. 固定12帧诊断的共同限制

1. 需要逐题明确参考区间和必要性规范，不把高相关片段、预测理由或MRFS当“完整必要证据”。
2. 三段非重叠与锚帧少于12、预算内可覆盖及区间外候选池均未在实际无答案记录上验证；不承诺存在足够病例。
3. 同revision下同时列出注释与媒体不等于注释秒数已桥接真实PTS。未来需要clip起点、PTS timebase、VFR／裁剪／转码说明与哈希，当前均未实测。
4. video ID／文件名不能证明真实源独立。未来需上游来源ID、parent／clip关系和本地私有隔离比较；保护映射只能留本地，不公开。这一任务没有比较历史MLVU身份，**不承诺≥40个独立来源**。
5. 注释只用于离线实验设计，不能流入部署策略；答案只能进入隔离评分器。此次没有创建新manifest、采样器、控制器或调用账本。

## 7. 访问范围、失败与预算

- 受控直接来源请求23个响应，合计 **214936 bytes（约210 KiB）**；最大单个响应42968 bytes，未达到256 KiB单体或2 MiB直接响应预算上限。按实际读取的解压响应字节计量，没有用拆包读取大文档。
- 首次另有一次检索工具调用（三个定位query），仅用于找到官方入口；中介返回文本／其后端流量未独立字节计量，**不填0，也不把直接响应计数当全部网络流量精确证明**。结论只依据随后实际读取的官方页面／元数据。Git任务文档同步另属协作传输，不是数据集下载。
- 404三项：HER详细字典路径；CaST主页所指评估仓库API；该仓库main commit API。没有据404切换非官方源、访问整包或续查AGQA。
- 没有访问完整注释JSON／JSONL／Parquet，未取得逐题记录；没有媒体、模型、ZIP／tar或完整数据集下载。API目录与schema并不等于数据正文读取。
- 原环境、研究资产、锁、旧账本均未改；临时元数据缓存仅在独立文档checkout的未跟踪Git内部目录，不提交。仅发布本报告及结果摘要。

## 8. 处置建议

**任务交付完成；所有候选的G1均为HOLD／UNKNOWN，而非PASS。** VES-Bench优先，因为联合必要区间与长视频命题更接近；但注释／视频许可和真实问答区间字典是硬缺口。CaST-Bench可作明确区间格式的备选，但规模、独立性、三段条件及长视频适配未成立。HERBench的多证据设计有参考价值，MRFS不能取代区间支持。

是否另设有限元数据澄清任务由ChatGPT／用户决定。本轮不修改READY状态，不执行VLM-003／004，不合并PR #1，不重新开启后台续作，提交成功后停止。
