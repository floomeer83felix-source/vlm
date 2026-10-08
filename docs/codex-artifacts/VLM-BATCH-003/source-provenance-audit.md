# VLM-BATCH-003 B：来源隔离与指纹覆盖静态审计

日期：2026-10-08，北京时间；main基线 `17a88e2`。只查小型聚合报告、清单结构及源组函数；未读取私有答案、逐题评分或完整身份映射，没有视频扫描／解码／全量媒体哈希。

## 1. 30 prepared、20 selected和450缺项

| 事实 | 本轮证据与限制 |
|---|---|
| 固定32源获取池中30 prepared、2失败，20 selected | `runs/fresh_gap_project_train_sources32/root_terminal_review.json`已有聚合收据；不是本轮重算资产哈希或恢复实验。30是准备成功资产数，20是选取的操作性组件数，不是真实事件数。不能用30−20推断“污染了10个源”。 |
| 789历史节点、339摘要、450缺项 | 固定manifest的`protected_nodes`、`protected_signatures`、`unavailable_protected`容器计数；按词法跳过身份值，仅统计条目。生成代码定义缺项为历史节点集合减现有摘要键集合。789来自此前固定partition全部组件成员的并集，当前阶段都按历史排除域处理。 |
| 339摘要的取得口径 | `fresh_gap_project_train_source_cpu.py::plan`只复用此前两个stage状态为prepared的signature路径／SHA；报告有339摘要、450缺项。不是339个独立事件或339个全部已验证的新源。 |
| 缺450为什么 | 意味着固定历史排除域中450个节点没有在这些stage取得可复用prepared指纹。旧解析器可用既有媒体／RGB64定位，否则保留unavailable；“没有摘要”不能等同未探索或没有关联。实现报告称多为heldout，但本輪不读私有映射，具体split分布、缺媒体／失败／未扫描原因比例**UNKNOWN**。 |
| 确认边界 | 聚合报告仍标真实源事件独立性未证明；本轮没有计算新指纹或补齐缺项，不保证至少40独立来源。 |

789、339、450是同一静态清单口径下的节点／摘要计数，非问题数、全项目视频总数或概率性覆盖保证。容器计数与生成代码吻合，不代表本轮重新逐节点比较原私有集合。

## 2. 字段及实际连接规则

| 字段 | 已见／UNKNOWN |
|---|---|
| 项目video/record ID、相对路径 | 定位字段存在；最新planned行有qid、relative_path、row ordinal／byte offsets等。只是定位与公开记录版本绑定，不能用文件名作为事件键。 |
| 媒体content SHA、expected bytes | 存在；用于内容字节别名及版本核对。不同SHA不证明不同源；相同SHA也只证明内容字节一致。 |
| dataset／annotation revision与SHA | 存在official_revision、annotation_path／SHA及项目partition角色；不等于上游原始源或同事件关系已认证。 |
| 原始provider/kind/source ID、parent | 旧协议要求有命名空间、类型、非空ID和可验证parent连接。旧finalizer实际可合并已核sha256 parent alias；最新固定32行未带通用provider/kind/parent证明。不能宣称该规则已覆盖所有语义源关系。 |
| clip范围、事件／场景／上传者 | 未见最新计划行保存可靠字段，**UNKNOWN**；时长字段不是clip在parent中的范围。 |
| 历史实验／保护角色 | 旧组件边及保护触达排除存在；项目train、校准／审计、封存／探索边界必须分别记录，不能调换。 |
| source_group_id | 由连接组件成员的有序内容SHA生成的哈希；是规则依赖的操作性键，不是语义事件身份证明。 |

静态连接规则：`source_isolation_finalize_cpu.py::components`对边做传递并集，组件触达任一保护成员则整组排除；`informative_lcs`按固定pHash相似和递增匹配序列建立潜在同源边。当前阈值是XOR popcount≤8、路径长度≥8且两侧不同匹配哈希各≥4；这里仅审源码，不运行或调整阈值。稀疏全帧pHash可能漏短重叠、裁剪、转码和同事件不同视角，也可能将相似场景过度合并。

## 3. 未来保守组键与污染屏蔽合同（未实现）

输入只含无答案来源元数据：namespace＋kind＋官方source ID、内容SHA、revision、parent／clip关系、历史角色及证据状态。不把qid、任务、模型正确性或上传文件名当分组依据。

```text
对同字节SHA加alias边；对已核typed官方parent/source键加源关系边；
对固定已核近重复结果加potential_same_source边，保持边的依据和版本；
做传递组件并集，任何成员触达历史探索/校准/审计/封存排除域则整组HOLD；
无源键或指纹覆盖不全：保持UNKNOWN，不发“fresh/独立”证书；
若任务需要保守大组，仅按已知来源线索形成并披露，不能凭空证明互异；
新队列、边、版本和组角色在看新结果前冻结，未知或失败不替补。
```

同上传者不必等于同事件，必要时可作保守上层聚类并披露有效样本数；不能通过字符串相同跨namespace误合并。新的同源证据不得重排旧封存角色：追加污染／失效记录，暂停相关组，禁止把确认集回流训练。

## 4. Toy示例与静态验收矩阵

仅为假想metadata，不是实际源、数据或执行测试：

| Toy关系 | 预期状态 |
|---|---|
| A与B字节不同，但同已核(provider,episode,id)且B为A的clip | 同保守组件；不能当两个独立来源 |
| B与C有已核潜在同源边，C属于保护角色 | A/B/C传递组件均HOLD，不只删C |
| D与A的ID字面相同，但provider不同且无验证映射 | 不靠字符串跨namespace连接；跨源关系UNKNOWN，不能因此认证独立 |
| E无真实源ID且其对应保护指纹缺失 | UNKNOWN／本阶段不入新探索；不得以不同SHA或未检出匹配放行 |
| F只有项目train标记，无上游parent／事件证明 | train角色可记录，来源独立性仍UNKNOWN |

验收需分别核：typed键来源、字节版本、parent/clip证据、历史排除域覆盖、传递污染、未知分母及冻结顺序；不使用答案或模型表现挑源。缺失签名、低信息量或未确认源关系按预注册保守规则阻塞，不通过新增媒体扫描把本静态审计变实验。

## 5. 处置与证据版本

审计**完成**，新来源独立性与探索污染全面排除仍**HOLD**。最多能作操作性grouped验证设计，不承诺≥40个真实独立来源。下一阶段需先在许可与版本成立后冻结无答案来源投影、排除域和残余覆盖政策，不能借本报告解封GPU或补跑历史实验。

新指纹／媒体哈希扫描／视频解码／模型QA／研究资产修改均0。未上传视频名、题ID、保护节点哈希表或源身份映射。

安全版本：`source_isolation_finalize_cpu.py` SHA256 `6d7c7edc2584a81c1e49b8667de84b5069ec73973206147e6547ef38aa13aee6`；`fresh_gap_project_train_source_cpu.py` `edea46ba0436c00f8d1a8455a463a94a86c36c10c56ac8c69383e2f02c70fb86`；旧隔离协议 `research/repositioning/source_isolation_protocol.json` `f1e5dd604a15627a5ee25aad859e702e2064c86dafb9b5e9b29f3f9049e4e4a0`。旧协议仅用于解释已存在规则，不给本轮下载或重新执行授权。
