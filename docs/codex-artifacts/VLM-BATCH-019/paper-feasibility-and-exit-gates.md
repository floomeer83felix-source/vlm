# VLM-BATCH-019：高水平期刊可行性与退出门

2026-10-10。**方向仍可研究，当前不具备新算法立项或高水平期刊成果承诺。** 只有公开静态证据：六候选都有关键门未闭合，六必查先例及五2026增补先例已覆盖普通“检索/记忆/证据/校准”版本。`NOVELTY=RETAIN0`，`DOWNLOAD_APPROVED=NO`，GPU/模型/私有资产访问仍BLOCKED。019完成不改变Charades018的FINAL_MEDIA_STOP、A限域验证或B/C HOLD。

## 六门独立裁决

| 门 | 本轮证据与状态 | 未来继续的必要条件/立即退出点 |
|---|---|---|
| LONG_DURATION | HourVideo20–120分钟、Video-MME30–60档、LongVideoBench15–60档、MLVU3分钟–2小时、LVBench历史v2长域已证；NLQ clip不是小时输入 | 同版评测输入≥20/30/60分钟的数量/覆盖真实可核，拒绝把库小时总量或3分钟QA当小时证据；不足则退出自然长域主张 |
| LEGAL_MEDIA | 官方限制文字已核，完整源媒体/派生真值许可未全部闭合；Ego4D协议访问RESTRICTED，网页不提供通用权利 | 精确对象和用途的标注/源媒体/再分发/训练/伦理权限闭合，之后才可单独向用户请求一批有界访问；未知不可先下载。HourVideo不可训练 |
| TIMEBASE | schema/字幕offset/采样公式可静态核，真实呈现PTS与同版关联UNKNOWN | 原点、单位、裁剪/重编码、版本hash、字幕映射可独立验证；正确工程换算作为基线，不拿字段存在认证同钟 |
| EVENT_GROUND_TRUTH | NLQ窗口语义已核，小时重复对象+事件实例联合真值未证；LVB引用帧创建过程已核、发布字段待证 | 可合法访问的独立实例/窗口/必要证据标签与可识别性成立；QA答案不能替物理事件边界，缺失即HOLD/NO_GO，不自批人工重标注 |
| PRIOR_ART | 普通H1/H2/H3均不够新；COVER/GEB/区间置信等2026工作必须进入强对照 | 明确新算子/假设及其不能被工程union/既有记忆/置信门模拟的证据，再独立验证。无差异或消融无解释则停止算法路线 |
| DEVICE_COST | 未检查原环境或跑模型；用户既有单卡3090/64GB约束仅沿历史，DEVICE_COST UNKNOWN | 同开源小模型、冻结输入/分辨率、全调用/预编码/重复帧/wallclock/峰值内存可实测且不需付费API/云GPU；无本机可比强基线则不宣称领先 |

## 仅公开文档深挖优先级

- `SCREEN_ONLY_PRIO_1`：Ego4D坐标/schema与HourVideo长域之间的合法同版桥接、H1强先例反证。NLQ常规clip只是定位辅助，HourVideo不能训练且非独立来源；此配对不是完整GO。
- `SCREEN_ONLY_PRIO_2`：LongVideoBench公开引用时刻发布合同与字幕偏移/真实帧时间差距；Video-MME只作潜在独立QA外测，先解版权与版本门。不能训练/换素材规避条件。
- `SCREEN_ONLY_PRIO_3`：LVBench最新v3统计/源媒体同版和MLVU删替规则审查；不因已有旧私有MLVU资产就回读或重跑。EgoSchema只作短域辅助。

优先级是未来继续查公开说明的顺序，不是当前任务追加、下载/签约申请或GPU计划。[许可/时长表](official-dataset-license-duration-matrix.md)、[坐标/真值合同](timebase-provenance-and-groundtruth-contracts.md)、[先例/假说反证](prior-art-and-falsifiable-mechanisms.md)提供逐项官方URL和UNKNOWN。

## 可发表性与停止

只报benchmark QA分数、改offset、正确读PTS、加caption记忆、提出新证据指标而无独立标签，均不足以支撑目标期刊的机制贡献。H2普通实体记忆当前直接NO_GO；H1/H3仅保留可否证诊断问题，不保留原创算法。未来若六门全部闭合并另获用户逐项许可，才可讨论独立数据/同模型强基线/公平成本和可信消融；当前不提交媒体、标注或模型获取申请。

未来推理协议须冻结输入模态：如沿RGB-only，字幕仅作离线坐标审查不能作为回答证据；要改为视频/字幕交错需新批准并给所有基线相同信息。HourVideo及任何评测保留集不进入模型/控制器训练，测试结果不用于改路线；基础来源重叠按视频/源家族而非文件名隔离。没有完整风险标签时不宣称统计保证。

本轮只有Markdown和公开网页静态阅读，未执行代码、实验、ffprobe、GPU、下载PDF/数据/模型、注册/签协议或访问私有资产。网页不可得保留SOURCE_UNAVAILABLE，不通过镜像、下载文件或引用GPT记忆填PASS。正常push后停止，保留原聊天等待ChatGPT科研验收，不自动BATCH-020。
