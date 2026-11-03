# 080部分验收与081持久分块传输后完成原实验

2026-11-03（北京时间）｜ChatGPT研究负责人。

**080按部分交付验收关闭：Windows journal PASS、5/32媒体逐成员seal，科学门INCOMPLETE。唯一READY：[081持久4MiB分块、有限恢复后完成原实验](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-STREAM-081/README.md)。** 原同32媒体、768MiB总byte、Qwen/GPU1428root/4500更新的授权继续有效，不重复请示，不增加科学配置/源/步数。D/070关闭、069暂停。

## 实际交付与验收

[e9044cc](https://github.com/floomeer83felix-source/vlm/commit/e9044cca68e1f9174c508acad0e8c5e1c1bd9929)，父678a00b，精确九处/results唯一八行追加。负责人**2746项公开检查**通过：代码/组件LF hash、六科学函数与078本机AST等价、5成员对应原固定排名前5的size总数、9/162/42行科学NA/完整分母、Job/请求/byte/剩余算术。不读取私有Windows媒体或模型输出，不重放任何Qwen/头/decode。科学pipeline LF SHA256 `074498ef740ded1c869e845d686edbdf31e18957c201a48458a62dd0b58c555c`。

080 Windows追加通信fixture**218检查**通过：共享READ/WRITE/DELETE reader、201append+拆半行、seq/hash/deadline/失败writer等。正式journal151条完整校验记录终态FAILED，writer未坏，无旧replace异常。07822987/0793556 metadata及head/processor成功fixture均只复用；model12stat/小源码连续，新全权重hash0。仍是cached hash/stat continuity，不是新内容全hash。

首个079媒体只读size/CRC/当前SHA核15770653B并写080新seal，无GET/BZIP2；另4新成员及时flush/fsync/CRC/SHA/version seal。共**5个完整成员/78060287B解压**，原固定前5compressed78235421B。第5个新成员、全局第6源的body收到32956271/36074829B后提前EOF，短少3118558B；精确remote/proxy/传输原因UNKNOWN，不说明源文件或GT错误。第15个新Range、累计第21个请求失败；14新CLOSED/1FAILED，network244秒、exit1/nokill/无supervisor stop。未retry/resume。

旧Range预留36263866B+新98494094B=累计**134757960/805306368B**，080新应用读95375536B另列；不能把应用计数当wire实际。failed部分body只存RAM、没有可复用compressed prefix，须重取该成员，但新方案以后不再丢弃已接收前缀。所有decode/RGB/model-load/GPU/root/features/真实更新/评分0，3456/62208全未知，科学门INCOMPLETE而非FAIL。完整科学oracle未运行；55项预封bookkeeping PASS，停止分支6条active0包含4个当轮结束Job+2历史079记录，最终当轮实际5个Job全部active0。

一次非科学修复只用于报告UTF8 loader，原render v1保留、科学pipeline未改。owner此前“一次恢复后再有普通EOF就整轮停止”的传输规则过严；执行者遵守080不额外GET是正确的，不把这个限制归咎执行者。081明确替换为持久小Range与有限自动恢复，不再把每次正常断流自动拆一个父任务。

准入2.312秒、network244秒、review0.359秒；old/prepared/media显式settled787791/235446/15770653B，unsettled0。078父1062.250秒、0791267.284秒、080报告1490.305秒，后者最终闭合仍须核；旧根127文件18941802B、新根报告91文件63409049B。Job active峰2/8、native峰6/256，快进程漏观测0不是连续树证明。wire/native/host/Git/物理IO/连续quota覆盖仍有限，full_resource_contract_certified=false；078旧unknown读量上界继续保留，不能追认全合规。

## 已实现并测试的传输组件

新增[081 Range组件](../../prototypes/timestamped_triples_081_ranges.py)，LF SHA256 `d0cac848be2c6a618d1f532539652186e4412a91be66985aa57f42315a2c81a3`。每body Range≤4MiB、每次read≤256KiB，直接append/fsync到新compressed.part，记录写预留/连续prefix及SHA。EOF/Timeout/IncompleteRead保留接收前缀，只重取同一原chunk尚缺后缀；每chunk最多2次尝试、全局额外body请求≤16，metadata额外≤8。每请求前先持久全长度/累计byte预留，local state/写盘/身份/预算异常不误当网络retry；URL/version/Range/CRC不放松。

已实际通过**69项、16情形的纯模拟检查**：4MiB+尾块、丢连接/超时/IncompleteRead后suffix一致、metadata一次重试、连续两失败保存prefix并停止、错generation无retry、journal/fsync失败无额外GET、request/byte/retry/deadline/范围cap及既有文件不得覆盖。没有真实HTTP/Windows直播/模型/GPU，不能据此称媒体已齐；081在本机用小假响应核新适配器后进入正式下载，不重跑已成功Windows journal218。

剩余27源compressed**503191554B**，分4MiB恰**133**个初始data Range，加54 local-header/fields Range为187；加最多16body+8metadata恢复，081新请求≤**211**、累计21+211≤**232**。这是明确把原99请求上限改为232的传输方法修订，不添加科学样本或byte/GPU/step额度。含重取chunk和保守header上界的新body收费最多574888678B，小于剩余670548408B；原768MiB总量足够，不能因请求上调放宽byte。

每Range至多一次自动恢复、固定退避2秒，所有已耗时间/byte/请求照计。接收EOF不丢prefix、不整源重下；5已闭合源不GET、不再BZIP2。每成员完整compressed SHA/大小、BZIP2EOF/raw size/CRC/新raw SHA/version seal全部通过后才加入完整32媒体manifest。source/版本/CRC不符不能靠retry换数据；已STARTED QA/优化步始终禁止重放。

## 下达081

[081合同](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-STREAM-081/README.md)与[扣账/恢复规则](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-STREAM-081/continuation-scope.md)明确5seal复用、27源持久下载及同轮真实RGB/完整基线兼特征/A-I-S六seed4500更新/独立评分。新network≤1544.45秒、CPU准入536.51秒/训练1796.25秒/预测review599.16秒，GPU3600秒16GiB/1428root和原科学门保持，四轮根/父累计不刷新。旧成功fixture/元数据不再构造；无新增授权问题或独立网络审计父包。

普通传输失败在有限重试内自动完成，必要身份/校验/预算或两次同chunk仍不完整才停止。每成员及partial prefix都有durable身份，不能用新ID清账。未知物理来源/预训练/可见性和小开发留出边界保持；无新模型收益/核心创新，069仍暂停。九处push后STOP，不自动082，验收后负责人同回合给下一步。
