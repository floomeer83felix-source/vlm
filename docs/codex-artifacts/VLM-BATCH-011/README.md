# VLM-BATCH-011｜已授权本地Charades CSV的时间合同冲突：10项有界只读核验

**创建2026-10-09，用户原授权的狭窄后续：仅对BATCH-010已合法下载并存于固定Windows隔离目录的原Charades train/test CSV做本地只读时间区间/来源资格诊断。绝不再次下载。** BATCH-010提交[8153a18](https://github.com/floomeer83felix-source/vlm/commit/8153a18af651afcbf0c5a455f3b61817e09755c0)已完成约定3处交付，但原66,500动作token中**19,625 (~29.5%)**不通过原`0≤start<end≤length`筛选，7,433/9,848 (~75.5%)视频行含至少一个失败，主因`end>length`。P1 gap>0组347、P2 overlap pairs97,723仅来自通过该数值合同的子集，不能当全集或语义真值。

**只读新一轮必须由用户在同一Codex聊天主动触发**，而非GitHub自动执行。确认远端main`docs/next-steps.md`仅`VLM-BATCH-011`为READY且`docs/codex-results.md`无同父结果；安全fast-forward独立文档Git checkout，读AGENTS、[原下载安全协议](../../charades-metadata-safety-protocol-2026-10-09.md)、[BATCH-010的download报告](../VLM-BATCH-010/download-and-schema.md)、[资格报告](../VLM-BATCH-010/qualification-and-decision.md)、原作者[Charades官方README](https://prior.allenai.org/projects/data/charades/README.txt)与[官网许可](https://prior.allenai.org/projects/data/charades/license.txt)。如果权限、原ZIP、目录身份/校验值或原CSV缺失、已有非本任务内容冲突、多个READY、现环境需改变，则STOP。不得试着恢复GPU工作区、扫描其它私人文件。

### 唯一本地数据落点（本轮读，不写，不下载）

`%LOCALAPPDATA%\VLM-Research-Isolated\Charades-v1-Metadata\`

使用该根下现有`extracted/Charades_v1_train.csv`和`extracted/Charades_v1_test.csv`以及`extracted/Charades_v1_classes.txt`。首先只读校验原ZIP/CSV的固定sha256（ZIP应`c616913ef79c2ddde06d9c562eae57bb8901d459d7568a0d27bf09cbf33ae866`，train`59273c6dc2139ec7eb95b980fd26bc8529774b1ede0602f6ca90b546ed12f0fc`，test`8b8b207b55fb95b949018027f69d83bd46cd844d15834f8f592ee8e7446173eb`）。**任何不符/不存在：停止，不自动重新下载/解压或覆盖。** 全程不写入原隔离树、CSV、manifest、下载ZIP；仅可在公共文档checkout写完全无数据的可重复使用诊断源码/合成单测及脱敏报告。Python`-B`，不安装依赖，不访问网络/视频，不执行ZIP的评测代码。诊断脚本**不接受任意目录/URL**，路径经已有`check_ancestors`物理身份/范围检查，只读打开固定CSV；不得遍历其它数据。

## 十项工作——目的在于判定时间合同，而不是换新算法

1. **授权/字节锚点**：复核仅原本地已取单包，CSV/ZIP SHA完全匹配，当前用户非商业约束及0额外GET/数据访问，记录可公开指纹；失败STOP。
2. **官方时间定义原文**：官方README`actions = class start end`三元组、`length = video length in seconds`、2017-02-27新增length列、官方帧级localize使用`time/25`采点；分`DOCUMENTED`/`INFERRED`/`UNKNOWN`，不能凭猜想把end>length归因于单位、数据错误或VFR。
3. **独立解析器交叉核对（合成先行）**：另写标准库只读`csv.DictReader`与Decimal统计器，复现原始66,500 token、train/test行及越界总数；将实际header、类表大小、split分母与010对照。不重用旧原型的范围判定函数作为“独立确证”；错误数与010不一致就STOP/REVISE，不偷改阈值以对齐。
4. **越界故障互斥主因**：将每token的`parse/time/class/negative/start≥end/end>length`建互斥优先级主因表，同时提供允许重叠的质量flag计数（需分别标注sum是否等于全分母）；其余细原因正小计数1—9抑制。不能把多个flag重复加成“不同坏token”。
5. **差额的匿名分层**：只输出全体与split宏观分布：`max(0, end-length)`的预注册桶`(0,0.1],(0.1,1],(1,5],(5,30],>30s`，比例`(end-length)/length`的`(0,0.01],(0.01,0.1],(0.1,1],>1`（若length非法则单列），`start>length`与`start≤length<end`的互斥计数；报告精确0和小cell`WITHHELD_LT10`。不打印最大值的对应样本，不给row/video/class/subject交叉表。
6. **高异常率来源结构检验**：按每视频异常token的宏观分布`0,1,2—3,4—7,8+`及valid/invalid总行分母，训练/测试是否相似（仅描述聚合事实）；原始length均值/中位数及官方30秒级范围，仅将其当CSV数字，不是媒体真实PTS。验证时间轴不可能从无视频观测单方面认证。
7. **P1资格敏感性、但不修正数据**：保留010已批准定义`(video,class)`下gap>0/0.5/1s和混合歧义；重新独立仅按`0≤start<end≤length`确认是否复现347及相应分母，并报告有invalid token的行中合格组数（大组允许报告，1—9抑制），避免用选择后的幸存子集假设全集完整。此项诊断不是新的主分析，不生成ordinal QA。
8. **P2资格敏感性、但不修正数据**：复现既有合法区间下97,723异类overlap pair及整行invalid关联的宏观计数；不得声称pair独立N或模型误判。若来源问题可能系统性影响时域关系，明确资格数为`PROVISIONAL`，不根据候选非零自动释放媒体。
9. **证据分级/公开前安全审查**：仅允许公开固定包文件哈希、CSV/header、公式、宏观桶（含完整分母）、字段间数值矛盾率、失败收据、官方公开URL；禁止上传原CSV行、action class/video/subject、原始script/descriptions、细粒度ID映射、真实本机路径或可逆表。需要展示异常例子时用自造toy值（明确SYNTHETIC），不得从数据导出一例。公开取值1—9统一WITHHELD，避免补数推回小单元；不公开多个能相减还原被抑制小格的边际表。
10. **是否建立可研究时间合同的明确裁决**：至少三类`DOCUMENTED`／`NUMERICALLY_OBSERVED`／`UNKNOWN`分别结论；若官方公开文本与实际原CSV冲突无法解释，设`HOLD_TIME_CONTRACT`；可讨论**未来需要的独立非敏感支持**但不得自行执行新数据获取、找作者邮件、媒体下载或实验。创新`RETAIN0`、自然长视频`FAIL`、真实媒体PTS`UNKNOWN`、GPU`BLOCKED`保持。不得因正常化/坐标缩放造PASS。

### 代码、提交与停止条件

允许新增**两份无真实数据的纯标准库Python**至公共GitHub docs checkout（代码写入前请确保函数没有联网/视频/任意外部文件读取能力）：
- `prototypes/charades_time_contract_diagnostic.py`：仅识别固定隔离目录CSV/官方类表的sha、宏观时间错误桶、严格既定P1/P2规则的独立复算；只输出去标识宏观数字，无任何原行或底层exceptions泄漏。禁止修改已有`prototypes/charades_metadata_audit.py`、已有ZIP/CSV和旧test。
- `prototypes/test_charades_time_contract_diagnostic.py`：**纯虚构数据**unittest至少8方法覆盖差额桶边界、并发重叠与间隔、坏长度/非有限、异常flag双计、train/test完整分母、小格隐匿、CSV header与Sha不符不下载、任何数据返回路径/ID泄漏防护。先运行该suite且PASS再读取真实CSV，失败STOP不得边修改边继续运行数据；仅在合成用例内修test和新脚本。

**GitHub只可提交5处文件**：`docs/codex-artifacts/VLM-BATCH-011/official-time-contract-and-data-integrity.md`、`docs/codex-artifacts/VLM-BATCH-011/aggregate-range-diagnostics-and-decision.md`、上述2个全通用std-lib脚本、`docs/codex-results.md`末尾一条`### VLM-BATCH-011 ...`总结果。不得提交原ZIP/CSV、临时中间结果、来源/视频/ID、私人绝对路径、敏感小群表，及不得修改ChatGPT管理的任务看板／总览、README、PR或历史记录。下载、写原数据、调用GPU、环境修改、原视频/STA、账号登录、外部联系、研究资产扫描全为0。

若无法实现纯聚合且不读/印真实单行，停机记录`BLOCKED`。安全stage核白名单，仅一次正常push后STOP，继续使用**同一个Codex聊天**。ChatGPT独立审查后才可决定下一步；本协议不设BATCH-012。
