# VLM-BATCH-006：静态可执行性门（任务4—7）

2026-10-09；main基线328f450。仅读先前审计指定的少量代码片段及已批准报告，不读取真题、标准答案、评分值、源身份表、视频或模型内容；不执行原研究脚本。PASS限静态事实存在，不等于新运行通过。

## 4. selector→frame→answer接口

当前数据流：

    sample_video -> 64候选RGB/索引与名义时间
    原question -> Index.text/SigLIP -> q向量
    候选V与q -> weak_binding_policy.select(question_mmr12) -> 12 pool ranks
    ranks -> 原Frame -> process_inputs(IMAGE12, 原row.question/options)
    Qwen处理器 -> 单次合法选项前向 -> receipt -> 终态隔离scorer

| 相对函数／接口 | 实读事实 | 路线2缺口 |
|---|---|---|
| active_vlm/video.py::sample_video | 索引均匀候选池、Frame timestamp=index/FPS | 没有接入新队列真实PTS；索引均匀不等于VFR时间分层 |
| active_vlm/retrieval.py::SiglipRetriever、runner::Index.text | 图／文特征独立可编码；文本截断、padding和audit存在 | 未有新selector_query／answer_prompt的分离配置；截断可能影响措辞实验 |
| weak_binding_policy::select_initial/greedy/select | 64池中4个固定均匀rank＋4个MMR，随后再选4个，目标含0.7相关性−0.3冗余 | 当前question_mmr12并非纯相似度top-12；不能未经说明当作草案S_q |
| gap_defusion_fresh20_runner.py::prepare_one/process_inputs | 同一row.question同时送Index.text与最终提示；options只用于提示／绑定 | 组件函数层可分别接收文本，但当前入口未冻结selector-only、prompt-only或donor query字段 |
| QwenBackend::_messages/observe | 原题和选项入提示，按帧时间排序；基础backend支持2—26合法选项 | fresh20专用packing／QA限4选项；不能直接沿用为HER/CaST等新题接口 |
| runner输入audit | 留帧源key、RGB、N/FPS、选中rank、tensor／grid／视觉token、query audit | 不代表新来源／时钟／处理器已经通过；本轮未执行处理器 |

**H-S接口当前UNKNOWN／不直接就绪**：未来须显式绑定selector_query hash、answer_prompt hash、原问题版本、合法等义关系、donor来源及arm。selector-only仅替selector query、prompt-only固定真实帧和预处理；不得把同一row整体替换当正交设计。等义资料不存在时H-S不执行，不生成新人工／模型“等义标注”。

S_t应另冻真实PTS分层规则，S_d应冻问题无关多样性规则，不把旧role/query MMR当query-agnostic。S_shuf的donor来自依法可用且排除保护来源的文字，回答仍原题；其任务／语言差异是负对照限界，不是语义因果净化。本轮未改入口或实现selector。

## 5. 合法QA与评分隔离

证据沿用[VLM-002](../VLM-002/dataset-metadata-review.md)、[BATCH-003](../VLM-BATCH-003/g1-feasibility-contract.md)，不重复数据页面访问：

| 项目 | QA／媒体许可 | split／候选版本 | 新队列评分隔离与来源 |
|---|---|---|---|
| VES-Bench | UNKNOWN／UNKNOWN | revision和目录已见；问答schema/split仍UNKNOWN，视频folder的train不能替代QA split | UNKNOWN；非gated不是许可 |
| HERBench | 已见非商业CC BY-NC-SA声明／上游视频使用条件UNKNOWN | 官方列schema及test config已见、nested metadata未核 | 新队列隔离／历史污染／同媒体版本UNKNOWN |
| CaST-Bench | 注释CC BY4.0声明／SAV使用条件未核准 | 80题test元数据和56视频目录，不等于56独立来源 | 新队列隔离与来源UNKNOWN；6选项不能自动沿用旧4选项 |
| 本地MLVU等旧资产 | 存在性已审计，不作为本轮新的许可核准 | 已探索／封存角色有历史记录 | 不能用旧20来源当独立确认；新合法来源数UNKNOWN |

路线2移除了gold证据区间要求，没有移除合法正确答案评分、媒体版权与来源门。允许的无答案投影包含问题／选项和来源元数据；正答与correct/posterior仅在终态独立scorer使用，不给selector或执行停止逻辑。

静态看到gap_defusion_fresh20_scorer.py::score先要求全部固定state和ledger终态，才读取private标签及校验绑定SHA；runner不读标签正文。这是**旧隔离路径存在PASS**，不是新路线端到端隔离通过。本轮未调用scorer、未打开标签或逐题输出。

## 6. 真实PTS、媒体与保守来源门

| 必需字段／条件 | 已有静态证据 | 新路线实证 |
|---|---|---|
| source_group typed namespace/parent/clip、历史role | 旧协议及组件规则存在；450摘要缺项有聚合口径 | UNKNOWN，缺失不认证独立，触达保护域整组件排除 |
| media SHA/revision、annotation/QA revision | 旧manifest与字节校验代码存在 | 新目标版及clip映射UNKNOWN，不同SHA不证明不同事件 |
| video stream、integer frame_pts、rational timebase | 历史PyAV和reference_pts模块存在 | 当前12帧链仍index/FPS；新媒体PTS/RGB绑定UNKNOWN |
| clip origin、source time变换 | 历史特定零点拒绝，不是通用变换 | UNKNOWN，不默填0、平移或夹断 |
| 唯一帧key | 当前以索引和媒体摘要等绑定；有unique rank守卫 | 新key应含media version/SHA＋stream＋实际展示帧身份；pool rank不是源帧 |
| 缺失／冲突／同事件关系 | 保守组件与unknown政策可设计 | 没有新签名、media扫描或≥40独立来源证明 |

沿用BATCH-003的789历史节点／339摘要／450缺项口径，450不是污染组数。来源未知不得通过更名、换split或抛弃失败换样本清除；确认集不能回流。旧pHash稀疏筛查有漏检与误合并，既有组件只是操作性单位。

本任务不要求gold支持区间，也不把clip metadata或FPS字段当真实PTS。不能从允许“无gold区间”推导媒体处理／下载已授权。

## 7. 帧数、token、时间和成本公平性

未来收据与接受／拒绝合同（未实现、未实测）：

- 固定同一合法候选宇宙的media revision／SHA、frame inventory、PTS、pool hash、策略版本／seed与tie；每臂12唯一源帧，源帧与提供槽／patch分开记。
- 分别记selector query、回答提示、选项、tokenizer截断、prompt及生成／解析上限，H-S只改指定路径。
- 留原几何、resize/crop、processed shapes、实际grid/patch/visual tokens、文本及总input tokens；仅12帧不能给TOKEN_BUDGET_PASS。真实证据缺失为UNKNOWN，明显不匹配不能解释为计算受控。
- 留时间bin定义／每bin计数、bin内PTS偏移／跨度、顺序；粗直方图相同不证细时钟相同。策略必然选择不同内容，不能逐帧内容净化成“纯相似度效应”。
- 逐臂从源hash/IO、decode、SigLIP图／文、selection、processor、forward、同步到checkpoint记录wall和残差；初始化／共享采集／评分另列，未测日志开销不填0。
- 同帧数不等同selector算力：S_t可能不需要SigLIP，S_q需要，S_d/shuf也按真实规则记账；不得dummy空跑补平成本或使用采集共享费用作为部署折扣。

当前真实token／新arm耗时均UNKNOWN，没有批准每臂wall/GPU或总调用预算。旧12帧／6993秒／240次草案数字不移用。本轮只核接口，未申请锁或创建正式manifest。

**统一门**：旧源码及静态隔离组件“存在”可PASS；新QA/媒体许可NG1、真实源/PTS/接口与预算NG2未通过。当前接口对真实PTS要求不满足，H-S分离配置缺失；新数据来源规模、token公平性和运行锁持有仍UNKNOWN。任务4—7已完成有界核查，不作实验GO。
