# VLM-BATCH-004 C：G1去留条件与纯合成CPU测试

日期：2026-10-08，北京时间；任务基线main 0653586。仅依据本包README及已验收VLM-002／BATCH-003，不复查数据页面或读取研究工作区。**A/B/C完成，G1仍HOLD。**

## 1. A：可审阅、未发送的请求

[中英请求草案](ves-access-request.md)分开询问注释与视频的非商业研究／披露许可、无答案区间字典、媒体版本／裁剪时钟及parent／源组元数据。官方收件地址在已批准材料中未确认，保持UNKNOWN。没有猜邮箱、发送邮件／Issue／私信或索取整套视频与答案。

## 2. B：原型和实际执行记录

- [toy_g1_contract.py](../../../prototypes/toy_g1_contract.py)：标准库独立合同，无I/O、网络、视频或模型依赖。
- [test_toy_g1_contract.py](../../../prototypes/test_toy_g1_contract.py)：unittest，代码中生成的虚构小整数、toy身份和RGB标记，不读研究资产。
- 两文件均声明 TOY ONLY, NOT FOR REAL DATA OR MODEL USE，合计255行，接近约250行目标；未复制原研究源码。
- 解释器：既有conda pytorch的Python 3.9.21；未安装或变更环境。公开命令中的python指既有解释器，不披露个人安装路径。

实际命令：python -B -m unittest discover -s prototypes -p "test_toy_g1_contract.py" -v

工作目录为独立文档checkout；-B不写字节码。没有使用不同环境重试。

| 轮次 | 测试数 | 通过 | 失败 | error／跳过 | 框架suite计时 |
|---|---:|---:|---:|---:|---:|
| 首次 | 10 | 9 | 1 | 0／0 | 0.005秒 |
| 仅修正toy文件后 | 10 | 10 | 0 | 0／0 | 0.005秒 |

首次失败是错误码预期与校验顺序不符：用例同时改变所有帧尺寸，包括锚点，因此先得到ANCHOR_IDENTITY_MISMATCH，却期望PREPROCESS_MISMATCH。修正为只改变背景帧尺寸，单独验证预处理条件；同一toy模块另补区间形状与几何类型检查，缺来源用例增加coverage_known=False。原研究代码未改。计时仅为框架suite时间，不包括进程启动与报告开销，未知开销不填0。

## 3. 已测试的合同及边界

| 测试类别 | 合成断言 |
|---|---|
| VFR与非零原点 | PTS×有理时基，经显式clip原点、parent offset／scale得到精确分数，不用index/FPS |
| 未知时钟／版本 | 缺原点、空版本拒绝，不默填0 |
| 非单调／重复／缺PTS | 递减与相同PTS、重复源帧、缺PTS均按固定码拒绝 |
| 闭／半开与平均标签 | 明确端点；0和2秒都不在[0.9,1.1]，均值1秒不代表观察 |
| 来源传递保护 | typed namespace、内容别名、已核parent与潜在同源边传递；保护成员污染整组；不同namespace不靠ID字符串误合并 |
| 缺来源证据 | 缺typed ID或覆盖未知返回UNKNOWN，不同内容别名不认证事件独立 |
| 12唯一帧／锚点 | 缺帧、重复、锚点RGB变化和不同媒体版本拒绝 |
| 背景保护带／画质 | 背景进入保护带或预处理／尺寸差异拒绝 |
| token混杂 | 不等toy计数拒绝；相同toy计数仍TOKEN_BUDGET_UNKNOWN |
| 时间匹配 | 未给time bins为TEMPORAL_MATCH_UNVERIFIED；histogram不等拒绝；粗bin相同不证明bin内时间分布相同 |

测试方法可含多个断言，测试数仍是实际10项，不把断言数当独立样本。PASS_TOY_ONLY只表示虚构结构通过，**fairness=UNKNOWN、real_G1=HOLD、semantic_sufficiency=UNKNOWN始终保留**。typed ID及verified_parent是toy前提，不是实际官方来源证明。

未实现合法数据投影、真实PTS／RGB解码绑定、版本认证、实际视觉token测量、问题相似度排序、真实来源规模或效应估计。无文件／媒体入口；不能直接生成VLM-003正式manifest。

## 4. G1条件树与混杂门

1. 注释与底层视频的使用／披露许可均明确？否或UNKNOWN即HOLD；公开可访问不是许可。
2. 有合法无答案字典和可机械解析、必要性明确的支持区间？否或UNKNOWN即停止“已覆盖必需区间”的前提，不用MRFS或模型输出估计补真值。
3. 同revision媒体SHA、clip原点、实际PTS/timebase及标注坐标已验证？否或UNKNOWN即HOLD，toy不能替代媒体验证。
4. 历史探索／保护污染屏蔽及至少40个保守来源组有可审核独立性依据？否则HOLD；内容SHA、30 prepared／20 selected不能冒充事件数。
5. 原协议的三段等条件、12唯一源帧、锚点一致及两个外部背景池可构造？否则HOLD，不减少预算或补样。
6. 时间分布、画质／预处理、真实视觉token、评分隔离和实际成本合同成立？否则HOLD／报告混杂，不能把效应归因为“仅问题相似度”。
7. 条件满足也只是提交ChatGPT／用户审查；新任务、GPU锁／持久账本与实验授权仍需明确，不自动执行。

当前VES许可／实际区间schema未知；HER MRFS模型依赖，底层支持与视频许可未闭环；CaST声明区间／逐秒框不是PTS或三段联合必要性证明。三者G1 HOLD不被本轮推翻。

相同12帧和锚点仍可能存在时间bin／bin内跨度、画质、缩放、patch／token、叙事与未标注支持差异。区间外不能直接叫“无关”；粗bin检查通过也不保证仅相似度不同。真实处理器token、源视频时间与干预构造均UNKNOWN。

## 5. 最多三项后续建议

1. 用户审阅请求、确认官方联系渠道并单独授权发送。本轮未发送，不假定有回复或许可。
2. 若取得合法资料，另立有界无答案schema／来源版本投影任务；记录单位、边界、必要性、revision、parent与排除状态。不默认授权完整标注、版权媒体下载或解码。
3. 数据条件成立后另审真实时钟与视觉预算合同；媒体fixture／处理器验证和GPU前向各需具体授权。toy不自动升级，来源规模或功效不足仍HOLD。

若作者无法提供合法可信的无答案支持区间，停止以“已覆盖必需区间”为前提的诊断，交ChatGPT选择可靠合法数据或重新定义不依赖gold区间的可观测问题；不自行延长检索链或判断创新通过。

## 6. 资源与停止

实际CPU toy suite执行2轮；新模型／GPU／QA／训练／评分前向0，视频解码0，研究数据／模型／媒体下载0，外部联系0，原工作区／conda／CUDA／锁／账本修改0。仅文档checkout产生两个toy文件、两份报告及父任务摘要。没有定时器、Actions或后台续作。

完成提交即停止；G1、真实PTS、来源独立性、创新性及VLM-003／004不放行。
