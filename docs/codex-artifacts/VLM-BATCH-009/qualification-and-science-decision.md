# VLM-BATCH-009：资格与科学停止决定（任务7—10）

2026-10-09，main71a24ab。**STOP_OR_UNKNOWN：下载前路径一致性复核失败**，详见[阻塞报告](./download-integrity-and-schema.md)。授权没有被扩大；未获取ZIP或CSV，未运行任何真实资格统计。提交的是受限任务执行记录，不是数据可用性或科研结果。

## 7. P1同类分离区间：全部真实计数UNKNOWN

| 记录层资格／分母 | 本轮真实值 |
|---|---|
| train/test行数及数值有效动作区间 | UNKNOWN |
| 同video/class的有效分组与≥2条distinct区间组 | UNKNOWN |
| 至少一对gap>0、>0.5、>1秒的组数及涉及视频 | UNKNOWN |
| 完全重复、相接、同类重叠、混合资格歧义及失败分母 | UNKNOWN |

新通用程序按Decimal处理数字，以同类别至少一对分离记录给组级资格；混合重叠／相接另记歧义，完全重复不增加distinct实例。重复ID的所有行阻塞资格，原行及异常分母仍保留。程序没有任何真实ID或数据，合成计数不能替代上表；不得将UNKNOWN写成候选0或非0。

即使未来获准取得非零记录资格，也不证实物理独立事件、完整同类序列、主体／对象一致性或自然语言first/second真值。本轮没有构造ordinal问题、negative、选择策略或模型输入。

## 8. P2异类重叠：全部真实计数UNKNOWN

计划规则为同video、不同class、distinct有效区间，交集>0及交集/min(duration)≥0.5；另列接触、包含、同类不适用和非法区间。pair数、video/class-pair组数、涉及视频及全部分母均**UNKNOWN**。合成测试中的重叠／包含正例只核逻辑；没有发现Charades实际并发，更没有确认边界漂移、因果或模型误认。

实际运行时仅允许总体聚合，正计数<10保守抑制，身份可链接微小组不公开；源行、video/subject映射、脚本及自由描述不进公共结果。本轮没有真实统计产物或任何可逆来源表，因此不披露伪造小cell。

## 9. 来源与时长：没有新证据

distinct subject、train/test subject交集、video重复、duration粗分箱和均值／中位数均UNKNOWN。官方267用户、平均约30秒只是[BATCH-008文档依据](../VLM-BATCH-008/temporal-provenance-and-longvideo-gap.md)，不是本轮CSV统计；不能以此填分母。没有真实媒体，PTS/timebase、clip原点／版本、不同视频的session／事件关联均UNKNOWN。固定存储复核失败也不能被“路径命名看似独立”替代。

## 10. 最终资格状态与权限边界

| 状态 | 本轮决定 |
|---|---|
| DATA_SCHEMA_VERIFIED/FAILED | **NOT_VERIFIED（UNKNOWN）**：没有CSV。不能把存储阻塞误写成CSV schema坏 |
| P1/P2_CANDIDATE_COUNTS | **UNKNOWN／NOT_RUN**，不是0样本、NO-GO样本或阳性现象 |
| PROVENANCE | UNKNOWN，无subject-by-split或实际源证据 |
| LONGVIDEO | Charades单独长域确认继续FAIL／最终论文HOLD，继承官方短域限界，不是新测时长 |
| NOVELTY | RETAIN 0，不以合成测试或下载授权提升机制门 |
| 本轮执行 | **BLOCKED_STORAGE_REALPATH_MISMATCH／NO_DOWNLOAD／STOP_OR_UNKNOWN** |

唯一需要先解决的新增事实，是安全协议指定路径为何未通过absolute/realpath一致性，以及在不换落点、不放松保护的情况下能否得到可审查的一致性证明。用户／ChatGPT可另行制定**只读Windows路径诊断**任务；本批没有展开私人绝对路径、做进一步诊断、更改检查或尝试新目录。任何后续取得数据必须有新的明确任务安排，不能重新执行已回报父任务或凭早期manifest的PASS跳过失败。

这是最多一项后续独立授权需求；**不建议直接授权视频／STA／GPU**，也不自动创建BATCH-010。前置未知未解决时元数据本身不能继续；即使解决，也仅恢复原有单包资格审查，不产生长视频／新算法许可。

资源：数据GET0、ZIP／CSV／模型／特征／媒体0字节，CPU合成suite2次（最后13 PASS），真实统计0，GPU／QA／真实解码／原研究目录／环境／锁／账本修改／外部联系／新标注／历史重跑均0。保留最小隔离准备状态；仅提交两报告、两新通用程序和父结果，push后停止，保持同一聊天供审查。
