# VLM-BATCH-008：来源、时钟与长视频差距（任务8—9）

2026-10-09，main eb2c53f。只读官方网页和已脱敏[BATCH-003来源审计](../VLM-BATCH-003/source-provenance-audit.md)、[时钟审计](../VLM-BATCH-003/timestamp-contract-audit.md)。未访问原Windows研究源码、媒体、身份表或账本；历史实现事实不能提升新数据的运行状态。

## 8. 来源独立与媒体时间准入

[Charades README](https://prior.allenai.org/projects/data/charades/README.txt)明确id、subject及scene字段；[官方项目](https://prior.allenai.org/projects/charades)称267用户。这些说明未来可做subject级保守分组，**目前没有实际subject-by-split映射或任何独立source数量**。不同video ID不等于不同人／session；267用户也不能当267独立试验。

| 群组／媒体条件 | 要求与保守政策 | 当前状态 |
|---|---|---|
| video | namespace+annotation ID+revision；内容SHA为字节alias证据 | ID定义可见，实际唯一／重复与SHA UNKNOWN |
| participant/subject | 同subject同一保守上层组，核原train/test角色；不同ID是否同人不能猜 | 字段定义可见，成员／跨split污染UNKNOWN |
| session/household/scene | session或同拍摄事件连接需独立来源依据；场景类别不是事件ID | session／家庭映射UNKNOWN；不得凭相似背景认证独立 |
| first/third view/variant | Charades-Ego视角配对、原版／480p／帧版等归同源；更换编码不成为fresh源 | 资源关系有声明，实际配对／媒体链UNKNOWN |
| 历史探索隔离 | 新队列在结果前冻结角色；已知共享源边传递传播HOLD；未知分组不洗白 | 不重用旧20操作性源，不读旧保护身份；新队列未建 |
| split | 原split保留并核源组件跨界；资格构造、校准、确认独立 | 文件角色已知，参与者层与session层隔离UNKNOWN |
| 媒体／标注绑定 | 注释revision、文件SHA、media SHA、stream、转码／clip parent与范围分别固定 | 网页v1说明不是包哈希／同版证明，UNKNOWN |
| PTS/timebase/clip origin | 保存实际展示帧整数PTS与有理time_base，声明clip/parent原点及变换；不使用DTS替代 | 无实际媒体，真实时钟UNKNOWN；不得fallback index/FPS |
| 帧与输入键 | media SHA+stream+展示索引+PTS/timebase+RGB摘要+preprocess revision；重复提供另记调用成本 | 仅未来合同，无帧生成或RGB检查 |
| 注释坐标桥接 | start/end单位、闭半开语义、误差与duration核验；偏移／缩放仅凭经核变换 | 文档字段不等于真实视频边界一致，UNKNOWN |

README称原媒体转码后保留原帧率，而官方RGB另经24fps滤镜。给定注释秒数，导帧索引／24不证明原始显示PTS；480p、原视频、官方RGB也不保证帧级一一对应。随机seek成功、时长差较小或标签舍入不能认证桥接。未知端点必须报边界不确定，不静默钳位至0/duration、去重或删除困难样本。

旧BATCH-003指出最新研究runner主要为index/FPS，历史PyAV及纯PTS原语另存在；**本轮不查看或运行它们**。789节点、339摘要、450缺项是旧封存清单口径，不能当Charades独立性、媒体可用性或污染数。本轮所能给的是新合同，不能声称新dataset adapter已可执行。

## 9. 约30秒材料与真正长视频目标

[ECCV2016机构摘要](https://publications.ri.cmu.edu/hollywood-in-homes-crowdsourcing-data-collection-for-activity-understanding)明确平均约30秒；这是全数据的论文声明，非本轮测得分布。平均不能排除长尾，但**没有经核自然长时域子集**。script驱动居家表演与自然长视频还有事件密度、剪辑、目的、视角和语言来源差异。

### Short-domain proof-of-concept可做什么

在许可／字段／资格／时钟／独立组和另行运行授权成立后，可检查：同类实例是否有可测资格，短时窗指定目标的定位误认，异类并发的边界／归因分解，受控数据处理与终态评分隔离。此类结果只能支持该短域上的测量；它不提供新机制、跨任务因果解释或跨模型通用性。

仅凭这些短片，无论tIoU多高，都不能证明自然长视频中的小时级记忆、远距跨段证据依赖、反复活动身份保持、长预算自适应收益、长期错误累积或部署节省。多个短片人工拼接可作为另行审查的受控合成stress test，**不能当独立自然长视频确认集**；拼接还是受限数据改造／披露问题，本轮没有此授权。

### 真正长时域外部验证需另获得的证据

| 条件 | 下一独立确认的要求；当前均未放行 |
|---|---|
| 自然连续时长 | 事前操作化长域，例如按≥5分钟、5–15/15–60/≥60分钟分层；这只是拟定研究阈值，不是通用定义。实际原始连续媒体时长／剪辑链和来源须验证，不能拿文件拼接长度充足 |
| 跨段推断 | 同一源内多个明确实例与足够间隔、上下文身份、跨段关联的独立真值；长输入不等于任务必须长程推理 |
| 权利与标签 | 媒体、文本／时间区间、评测及论文披露分别有适用许可，标注不是泛问答正确性替代；STA未知不外推为新长域授权 |
| 来源与角色 | participant/session/event层保守组、探索／校准／外部确认分离；多个同源clip不累加独立N |
| 时钟与版本 | 原始PTS、timebase、clip/parent映射、媒体和注释revision/SHA、边界误差核验 |
| 迁移与强baseline | 事先选择zero-shot或few-shot，后者公开训练来源／标签费用；同输入／资源下的TAD/TMR及合适VLM直接强对照，不能看外部结果再挑模型／阈值 |
| 可识别效果 | 实例交换／并发误差分解与全部失败分母，源组推断、功效与最小有用效应；区分时长、稀疏采样、目标短和语言歧义 |
| 预算与工程 | 合法解码、索引、特征、所有验证者／模型／processor tokens、重复帧、IO与失败恢复全成本；RTX3090存在不等于长域能运行或成本匹配 |

本轮方法文献FlashMMR提到更长媒体，但未取得其数据许可、实际media/clip范围、PTS和source证明，不升级为已可用长域。Ego4D申请仍未确认成功，本轮不重启申请／咨询。**LONGVIDEO作为Charades单独确认集FAIL；最终论文GO=HOLD。** 这不证明未来永远无合适长数据，只说明本批网页不足以提供独立长期结论。

所有真实资源门UNKNOWN：视频／注释获取、解码、GPU、原资产修改、外部联系均0。本报告不申请媒体或模型自动放行。
