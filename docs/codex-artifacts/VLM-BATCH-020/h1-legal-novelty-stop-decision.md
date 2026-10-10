# VLM-BATCH-020：H1与合法同版桥接联合止损

2026-10-10。八项公开静态审查已按授权范围交付；执行交付完成不等于ChatGPT验收、科研成功或实验准入。`NOVELTY=RETAIN0`，当前普通H1为`H1_NOVELTY_NO_GO`，Ego4D—HourVideo配对为`NO_GO_FOR_EXPERIMENT`。建议结束当前H1组合的算法立项及该配对的执行路线，保留公开负结果；不建议再为填空追加下载或旧媒体补救。

## 五门分别裁决

| 门 | 本轮状态与可核依据 | 什么证据缺失 / 当前停止条件 |
|---|---|---|
| LEGAL_PROVENANCE | HOLD / RESTRICTED。[权利报告](ego4d-hourvideo-license-and-version-bridge.md)分软件、媒体、标注、评估、训练与派生发布；Ego4D协议入口403，HourVideo明确禁训 | 正式许可对象/用途、派生标签构造与公开授权、伦理/机构约束未闭合；不能将代码许可作数据授权 |
| SAME_VERSION_TIMEBASE | UNKNOWN / MAPPING_NOT_PUBLICLY_CERTIFIED。Ego4D有字段及转换文档，HourVideo有公开辅助函数 | 源release、派生hash、实际trim/resample、QA/caption/evaluator原点没有公开认证闭环；字段存在不等于file-level同钟 |
| INDEPENDENT_GT | HOLD。NLQ有任务窗口，HourVideo有长QA作者声明 | 未核小时输入上的答案/证据/版本联合标签、漏标及歧义；NLQ最长20分钟不支持小时GT；Ego4D↔HourVideo同源不能彼此外测 |
| H1_NONTRIVIAL_DELTA | NO_GO（普通版本）。[强基线与反例报告](h1-strong-baselines-and-impossibility-redteam.md)给可模拟组合、风险对象与双世界限制 | 没有新算子/可认证非等价见证，未解决不可识别性；不因现有方法没有某项保证便自称原创 |
| COST_AND_BASELINE | HOLD / UNKNOWN。纸面B0–B5包含正确工程、鲁棒并集、COVER、筛选与VideoMind核查 | 未测本地开源小模型适配、全编码/候选/复查/校准成本与内存；作者模型结果不能当单卡实测 |

以上只到SCREEN_ONLY/HOLD/NO_GO。没有DATA_GO、GPU_GO或NOVELTY_GO。公开许可文字与纸面时间公式不能认证现实媒体、统计有效性或可发表机制。

## 残余筛选与杀死条件

**本轮不保留残余新问题（0项）**。此前泛称“时间不确定与QA风险联合控制”没有构造出不能由强基线模拟的操作。所读COVER全文已考虑非连通集合、依赖、分层校准及宽度筛选；一般非单调风险控制也有2026摘要先例。把这些限制命名成H1，或添加一个联合分数，均不形成独立创新。因此不填写H1_RESIDUAL_QUESTION_UNKNOWN来暗示已经找到研究空间。

若ChatGPT今后凭新公开证据重新立题，必须另有至少一项可审查的差异：同一信息和成本下，旧组合不能实现的新决策或性质，及可推翻的构造性见证。多给provenance/GT造成的改善首先归于信息增量；强基线必须获相同见证、候选、模型和预算。仅证明没有见证就不可识别，是必要条件分析，不是新恢复算法。此段不是下一任务提案或执行授权。

以下任一情况足以停止普通H1主张：收益全部来自offset工程修正；union+COVER+常规筛选输出等价；效应只是更大区间/更多复查成本/更低覆盖；条件风险用边际覆盖替代；版本见证、合法联合GT或可交换性条件无法认证；使用同源数据充独立外测。旧019“≥2pp、≥60%”是未做功效分析的纸面示例，本轮不采用为实测门槛、不预注册实验、不承诺统计保证。

## 八项收据与科学限定

| README步骤 | 执行状态 |
|---|---|
| 1 | DONE：干净独立公有docs checkout安全FF至7c70287，唯一020 READY、无既有020父结果；重读AGENTS/任务板/总览/结果/020合同及019四报告 |
| 2 | DONE（文本审查）/条款UNKNOWN：权利两层、用途与派生标签许可分列；完整Ego4D协议SOURCE_UNAVAILABLE，不签约、不换入口绕限 |
| 3 | DONE（纸面合同）/真实桥接UNKNOWN：命名空间、PTS/秒/frame、仿射和分段条件、版本/hash与QA时钟缺口分别列出 |
| 4 | DONE：H1观察、M/I、输出、接受条件联合损失及B0–B5零创新强基线；M/标签未认证不制造性能 |
| 5 | DONE：五必查先例证据分级；增补1项2026原摘要；双世界offset与同答案异证据反例及一般不可识别草图，无toy运行 |
| 6 | DONE / H1_NOVELTY_NO_GO：没有足以保留的单一残余创新问题，不强行填PASS；实验NO_GO |
| 7 | DONE：五门联合止损；同源、NLQ短clip、无独立GT、设备成本UNKNOWN均保留；建议结束当前组合 |
| 8 | DONE：三Markdown及唯一追加父回报；范围/隐私/链接检查，普通push后停止，由ChatGPT审查 |

证据方法沿用文献综述技能的原始来源、证据分级与反证结构；没有执行技能脚本、制图或PDF流程。本轮依据[官方Ego4D入口](https://ego4d-data.org/docs/start-here/)、[HourVideo README](https://github.com/keshik6/HourVideo)、[COVER v1 HTML](https://arxiv.org/html/2608.07434v1)等公开正文；完整清单、位置及不确定限定见另两报告。非穷尽综述，SOURCE_UNAVAILABLE不借PDF/镜像、受控数据实体或联系作者填补。

## 权限与停止

0媒体/帧/音频/字幕/标注/QA实体/模型/论文PDF文件获取，0私有科研资产/原实验树/视频/CSV/PTS/ledger访问，0研究脚本/测试/toy/ffprobe/模型/GPU/训练运行；未注册、登录、签协议、联系作者、使用付费API/云算力或安排后台任务。允许动作只有公有文档Git及Markdown维护、公开HTML检索阅读。0代码、实验环境、旧批报告或ChatGPT计划文件修改。

Charades FINAL_MEDIA_STOP和旧018 CLOCK_UNKNOWN不重解释，013–019不重跑。报告不提供QA选项、身份映射、个体时间或私人路径。正常push后停止本执行轮、保留聊天；不创建021，不修改任务板，由ChatGPT决定ACCEPT/REVISE/HOLD及是否结束研究方向。
