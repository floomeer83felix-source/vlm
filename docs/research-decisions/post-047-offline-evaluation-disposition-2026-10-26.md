# 047验收：固定数学夹具上的离线评分与核算软件通过

2026-10-26（北京时间）。
**ACCEPTED_OFFLINE_SOFTWARE_IN_FIXED_SCOPE / REAL_DATA_SCORER_NOT_QUALIFIED / 047_CLOSED。**
执行提交：[39fa753f9f3f3862bc26c3484cc934143e62e589](https://github.com/floomeer83felix-source/vlm/commit/39fa753f9f3f3862bc26c3484cc934143e62e589)。
047已消费，不重跑；当前0 READY，不自动048。

## 1. 验收范围

接受本次标准库计算库、synthetic-only CLI和固定夹具证据为一个已完成的软件准备组件。
严格区间解析、固定答案集合max单区间IoU、未知优先级、失败全分母、按源聚合、
声明输入类映射与共享/包含式成本在本轮登记范围内有一致证据。
不认证任意真实输入、标签时钟/题目语义、实际模型等价、时钟同步或生产鲁棒性，
也不把已有计算规则或回归夹具提升为新机制/论文核心贡献。

[统一回执](../codex-artifacts/VLM-OFFLINE-EVALUATION-047/offline-evaluation-receipt.md)、
[65行用例表](../codex-artifacts/VLM-OFFLINE-EVALUATION-047/contract-case-results.csv)、
[四网格及CLI证据](../codex-artifacts/VLM-OFFLINE-EVALUATION-047/fixture-grid-summaries.json)。

已刷新AGENTS/main/看板/results/总览/合同。相对a009b0d恰六个allowlist路径；
results旧正文逐字保留，仅追加9行一条047父回报。合同/fixture/旧实现/负责人规划未由执行者改动。
初suite60用例/148断言报告全通过，无修复/回归；另5个CLI核查通过、坏映射按预期拒绝，
独立post-exit执行者报告1128断言。65行不是65项自然研究实验，断言数不累加为样本量。

## 2. 负责人独立复算

只使用公开文件和标准库，不导入交付核心/tests、不重跑其suite/CLI，不访问Windows/私有根或任何真实标签/预测。
独立程序完成695项一致性断言；这也是公开材料复核，不是第二台机器实测或现场OS见证。

- 两源码语法可解析，按Git原字节独立核SHA256：
  核心6269fbdff13ea101db46d1bdd292f5f66fc45ace23966dabefc5a2dd58878825，
  tests4f9da867ef3c5f9a96e84303643c5a80873a2ff58ffdce223052c6b4e8e9588a。
- fixture仍为5485d7c097b74d78a002c4822c874386a6427faf5567e73c925216abba562063，
  24 parser+7 IoU+4网格+22故障+C01+X01/X02=60；CSV再加5 CLI=65，全部初轮状态/标记和顺序一致。
- 依据冻结构造规则及明确序列化口径重新构造五组25份CLI输入，
  plan/registry/classes/records/costs的全部25个字节SHA与封存相同。
  公开完整summary的5个JSON和5个cells.csv逐字节摘要均重建匹配；没有只比较摘要字符串。
- 独立从规则重建4×64=256格，包括复合ID、运行/评分状态、精确分值/hit、端点误差、
  raw响应hash、未知/JSON错误原因；与全部公开行相同。
- 重算每源两题均值、6 HIGH_OFFSET/2 CFR/全8源的分母/覆盖、主均值/未知、known子集、
  端点误差覆盖、P/N相对B0源差/正源数及纠正/误伤表，均匹配。
- 核G01声明48类/48条记录与64逻辑格，G02–G04为64；实际模型调用字段始终0、科学GO=NOT_GRANTED。
  这些是声明fixture身份，不是真实tensor或实际生成次数的独立证据。

| 夹具 | 可计分/64 | HIGH_OFFSET P−B0 | 正源 | 数值条件 |
|---|---:|---:|---:|---|
| G01 | 64 | 0 | 0 | false |
| G02 | 64 | 1/6 | 4 | true |
| G03 | 64 | 1/12 | 3 | false |
| G04 | 60 | UNKNOWN | UNKNOWN | null |

G02平均IoU改善时，高层12题在R@0.5下仍均正确，纠正/误伤均0；不能混称阈值纠正。
G03非法答案仍计0且分母不变；G04标签桥接未知4格未填0，主量/触发仍null。
BAD_MAP保留expected64，status=REJECTED_RESULT_MAP且scores/condition均null；exit0只表示拒绝结果已序列化。

共享cost C01独立核outer10、直接phase合计10、prepare被四处引用仍记2、内含letterbox1/2另列；
最终latency不为21/2或20。混时钟/缺成本/重叠的公开拒绝或未知字段与规则相符。
给clock_domain命名或文件hash封存不能证明实际时钟同步、数据真实性或标签隔离。

## 3. 资源和实现边界

七阶段父域start/active0差值逐项核对，和1.469秒≤180；
减suite0.250后，CLI及post-exit监督和1.219秒≤60。没有将相隔的实现/等待间隙算成CPU运行；
它仍在父预算中。峰Job14045184B<512MiB、各exit/active均0、kill=false，
父报告789.849秒<3600、61文件/510341B<512/16MiB，与公开记录相容。
初空闲348047507456B高于16MiB+2GiB所需2164260864B。
这些是执行者资源记录及可复算字段；驻留快照不认证卷级硬配额/累计写入峰值。
Git最终发布前的TLS refresh失败有保留且未重试；远端确为基于a009b0d的单一普通提交，没有丢失其他main变更。

源码同时限制可外推范围：
- validate_plan固定S01–S08/Q01–Q02、6+2及T=240；CLI强制本轮synthetic标记。
  库有显式接口，但没有任意180–900秒自然源/真实标签输入资格；不能直接改标记后投入真实评分。
- 当前固定夹具和登记字段故障有验证，不等于任意畸形JSON的全面类型加固。
  静态代码中registry_lookup对行直接调用.get，eligible也假定对象形状，
  相关异常层并未全部捕获AttributeError；不能声称任意损坏registry都必然输出SCORING_UNKNOWN。
  这不改变已独立重建的固定案例，但限制通用/生产使用结论。本轮不为扩大宣称追加补丁/用例任务。
- 未来真实标签只应在模型组全部退出后由独立受控scorer读取；047无模型进程，
  因而没有验证真实端到端标签隔离或外部资格声明的真实性。
- audit hook/路径及封存检查为本轮合作式约束，不是对抗性沙箱或恶意文件系统证明。
  物理记录、输入等价、source独立性和clock_domain均为外部声明，不能由本程序自行认证。

## 4. 后续裁决

**047按固定夹具软件范围验收通过并关闭，评分计算组件可保留。**
当前0 READY，不自动048、不再增加数学夹具/通用框架补丁以累加任务数，
不恢复046/044下载、旧资产扫描、真实标签读取、模型/GPU、训练或投稿。

下一实质研究步骤需要确切完整且可使用的原视频、来源/版本依据及可核既有题目/标签时钟入口。
准确私有路径可只留本地Codex；不得从“继续”推定旧文件状态、恢复私有日志或转移已消费额度。
真实素材的时钟/独立性、题目可识别/有效答案集、实际B0/P/N输入和强N行为仍未齐备，
8源/16题/64格真实实验仍HOLD；NOVELTY=RETAIN0、NATURAL_VIDEO_EFFECT_UNKNOWN及其它停止结论保持。
负责人本轮仅验收/归档/看板/总览/设计补充，执行代码、fixture、原始证据及codex-results保持。
