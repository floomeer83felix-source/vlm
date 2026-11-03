> **2026-11-03已按完整科学交付验收关闭，原门FAIL/STOP_THIS_RECIPE，不调参重跑。** [8ae75ef](https://github.com/floomeer83felix-source/vlm/commit/8ae75ef40616c80c8afaaeaa7f0842876c01e600)32媒体/192RGB、1428完整root/4500更新齐；I/A/S六seed测试均144/288和0/8源全对，B0 REAL176/288。[验收](../../research-decisions/post-081-negative-gate-and-cache-learnability-audit-2026-11-03.md)3056公开检查，父clock剔除26054秒依据未由公开记录认证/其余资源覆盖限制保留。唯一新[082](../VLM-TEMPORAL-LEARNABILITY-CACHE-082/README.md)只读feature/state/loss/原pred缓存诊断，CPU300秒，模型/头forward/训练/GPU0。以下081原合同按当时状态逐字保留，旧READY或未用quota不授权重跑。

# 081 4MiB持久分块下载，完成原真实RGB训练整包

2026-11-03（北京时间）｜ChatGPT研究负责人。
**唯一READY：APPROVED_CONTINUATION_OF_UNFINISHED_078_SCOPE / AWAIT_FRESH_081_START。** [080验收](../../research-decisions/post-080-partial-review-and-bounded-chunk-resume-2026-11-03.md)后按[明确扣账/分块恢复](./continuation-scope.md)继续原已批准科学工作，同byte/GPU/4500步范围不重复请示；原080正确遵守无retry边界停，081明确改变传输方法而不回写旧轮。

## 1 启动与复用：不再做已完成准入

安全同步独立文档main，读AGENTS/最新看板/results/本合同及续作表，核唯一未交付READY。沿明确handoff精确定位080、079、078与076，旧根只读；没有准确路径只等待，不扫盘/交空阻断包。复用080已认证metadata/media-plan/obs/truth/relations、model-registration/processor fixture、079/078源seal链、5个member closed seal和精确原文件、network Range/进度/读账本/Job/父闭合。只有这些登记文件及累计quota所需指定根stat，不查旧QA正确性/其它数据目录。

原32源20/4/8、29文本/138问、1152答案/2304关系（768FLIP/1536HOLD）、28139源metadata帧固定；22987/3556/head/processor36/Windowsjournal218成功结果都是历史资产，**不重跑**这些fixture/构造/全权重hash。只核复用文件SHA及closed identity连续，标新hash测量时间，不冒称历史seal。5媒体seal逐项对应固定source plan，当前stat/size/SHA/CRC一次有界读取核连续，合计raw78060287B；不符合则STOP，不网络替换已完成源。

旧080失败36,074,829B body仅收32,956,271B，partial只存RAM，不假设磁盘有可用prefix；复用5文件并获取source排名5..31的27个，不能以5个训练或改变test。剩余compressed503191554B。公开原目录CRC/ETag不是未观察内容hash认证，仍须所有新文件完整通过CRC/size/BZIP2EOF和实际SHA。

## 2 用已实现的stream组件处理普通断流，原总byte/time仍硬约束

调用只读[081 Range组件](../../../prototypes/timestamped_triples_081_ranges.py)，LF SHA256 `d0cac848be2c6a618d1f532539652186e4412a91be66985aa57f42315a2c81a3`。负责人69项/16情形模拟检查通过，非真实网络/Windows实机验证；本机在首个HTTP前用小假响应只核新adapter的EOF/timeout/IncompleteRead suffix恢复及local/identity不retry，成本入准备536.51秒。不要重做旧218 journal测试；复用固定[080progress](../../../prototypes/timestamped_triples_080_progress.py)及其已通过Windows共享分支，彻底无状态文件replace。

假响应fixture使用独立、明确NONLIVE的账本/临时part，不写正式HTTP账本、不增加真实GET或重置其21请求/134757960B起点；只有fixture CPU/私有根成本计入实际预算。

传输仅原`storage.googleapis.com/dm-perception-test/zip_data/train_videos.zip?generation=1685446268139925`对象，If-Match原ETag `"-CJXz5tD4nP8CEAE="`/total28404087974/identity编码。每次206/精确Content-Range/Length/generation/ETag由新client核定，任何身份/版本/status不符立即失败，不以retry换源。不HEAD/redirect/整archive/其它对象。local ZIP64/header/name/method12/flags0/CRC/sizes规则保留：每剩余member先30B local header，再exact filename+extra（≤131070B）。

为27媒体预封133个初始data chunk（每个≤4194304B）和54个local header/fields初始请求；source offset+已接收prefix必须映射同一原对象/原member。**每个原chunk最多初始+1次suffix恢复，额外body请求全局≤16；metadata最多初始+1次整小Range重取，全局额外≤8**。同chunk部分前缀继续增加时仍是同chunk的第2尝试，不能改chunk ID绕过。只有EOF/transport timeout/socket短读等可恢复；HTTP身份/CRC、local journal/写盘/fsync、quota失败不能误当网络重试。

新≤211请求、跨079+080+081≤232；原99→232是本合同明确的分块恢复修订，不能扩为额外源/byte。跨父正文Range charge≤805306368B，旧134757960B保守扣除，新≤**670548408B**。每次请求前必须通过已fsync的reserve ledger记录整个Range长度、全局请求号/charge/kind/retry，使用RangeBudget初始21请求/134757960B；不能给每member重建budget或复位恢复计数。metadata/data/status日志均公开实现，私有源路径/凭据不公开。重试2秒退避也入network≤1544.45秒，不再因第一次普通EOF就结束父任务。

真实HTTP adapter只做连接/响应，不在transport catch内暗藏本地文件错误。调用`on_connected`后更新HEADERS；soft socket connect≤10秒/read≤20秒，supervisor CONNECT15秒/header30秒/每4MiB body90秒/read inactivity30秒夹紧累计deadline，留出捕获timeout并恢复的时间差。每次read≤256KiB，不能用一次`read()`/chunks列表把整member存RAM。progress每次read前保留完整deadline；缺失/半行不刷新，校验损坏不忽略，末态FAILED不能伪转IDLE。

下载只写新081的compressed.part，接收块先记write reserve、写/flush/fsync，再append已连续prefix与SHA账本。`IncompleteRead.partial`在valid headers且不超Range时同样持久，然后只取缺口；不得丢弃已提交prefix/整member重下。文件tail未提交不能混作已验前缀；如需回收，只能在确认无writer时核intent/SHA后处理自己未完成part，旧根禁止truncate/delete/覆写。当前component在一次member调用内部恢复网络断流；意外进程终止若缺可信prefix/预算闭合，不能自作主张重启清账。

compressed complete后有界读取/计算实际compressed SHA，与接收账本比对，再做原BZIP2 EOF/无多余流/raw size/CRC和raw SHA，最大comp/raw各≤80MiB、aggregate raw≤640MiB。每新member immediately flush/fsync closed seal（source版本/offset/CRC/size/SHA/code）后下一源；最终32seal独立组成完整global media manifest，5旧媒体只引用原只读路径，不再GET/BZIP2。不完整part保留身份/prefix/预留/失败，不计CLOSED或悄悄丢弃样本。

同步修订实际HTTP adapter、stage预算/旧根累计映射、network-summary及独立bookkeeping事件schema：本组件用REQUEST_RESERVED/CLOSED/INCOMPLETE与PAYLOAD_COMMITTED，不可套用旧network080的15/93/99硬编码或要求每次HTTP都CLOSED。新请求数=全局requests−21，Range charge含旧134757960B，application bytes另列；首次真实HTTP前用小型假日志验证这些转换。科学六函数和评分门不变，网络计量oracle必须随新协议预封，而不是下载完成后临时修审计。

**已被成功恢复的请求INCOMPLETE不自动否决媒体或科学实验。** 独立核每member实际已提交字节按offset连续覆盖compressed范围、prefix SHA和磁盘SHA相同、重试/byte/time合规，最终32个member全CRC/size/BZIP2/版本seal闭合即可继续训练；原请求失败记录仍保留。不能因历史曾有EOF就把最终完整数据标为NOT_RUN，也不能把尚未闭合的partial冒充合格成员。

## 3 媒体齐后本轮直接做完整科学实验

以下同[原078制定时固定合同](https://github.com/floomeer83felix-source/vlm/blob/259590c36b7c39e2c217158a68374c3c4a15ab08/docs/codex-artifacts/VLM-TIMESTAMPED-TRIPLES-TRAIN-078/README.md)第2–5节及[080](../VLM-TIMESTAMPED-TRIPLES-FINISH-080/README.md)相容科学规范，传输/扣账被本合同明确覆盖：

1. 32源各一次真实PTS decode，codec1、单段12不同真实帧/224RGB、原非重叠/0.1秒gap/端点/最近PTS规则，96RGB块→192真实六排列，36frames/12fps/3秒统一runtime。不是latent排列，不新增标签/补帧/换源；100000帧/1800秒上限，准备所有REAL/BLACK同q非pixel逐字节相同，反GT同输入gate保持。没有GPU probe/已通过软件fixture重放。
2. 同本地冻结Qwen/bf16/SDPA/完整Yes-No首续写二选一，REAL/BLACK/TEXT各1152逻辑/最多1428新完整root、一次load/GPU3600秒/allocated16GiB/Job32GiB、3480秒新调用截止。只读hook在同B0 root捕获18×2560主merger V及TEXT q2560，分离feature forward0/主干backward0/generate0。cached076catalog/current-stat/小源码连续，不新增全weights hash；shared锁/free/历史与本轮input STARTED/CLOSED去重，不重问已消耗QA。
3. A/I/S同341633参数/initial state/batch流；seed19/73/101/137/181/229，每配置250步，共18配置4500真实CPU更新。CE与原λ0/.25/.25、I正确FLIP/HOLD/S(q+1)mod6破坏问题相关target，答案CE不改；train20监督隔离，不读B0/dev/test答案、不选超参/seed/checkpoint。六函数head_class/relation/train/predict/metrics/scoring同078/079/080本机AST等价，科学逻辑不变；持久I/O与明确封装修改单列。
4. 最终一次REAL/BLACK/TRAIN_MEAN头预测62208逻辑/actual≤25704，B0逻辑3456；9/162/42表保留train20/dev4/test8全部分母、native/源36-all/无向6FLIP+12HOLD四格、固定V50%/0整组软件guard及8源paired不确定性。原独立oracle预封、不import生产scorer/训练或重放模型/头/decode；所有输出/state/steps/aliases/input/版本和资源独立核验。
5. 原门不变：≥5/6 seed I源全对同时>A/S；六seed I源全对总≥12且对A/S净增各≥6；I单项/FLIP/HOLD不低A/S，单项不低B0且源全对严格>B0；I胜自身固定V源全对且单项≥50%。未知INCOMPLETE，完整未过关闭此配方，不改门/补seed/换控制。source全是官方train开发划分，录制/参与者/预训练/可见性/原子完成/唯一发生未知，不证外源/盲测/核心创新，不写论文。

## 4 计量、修复边界及交付

按[扣账表](./continuation-scope.md)：新准备≤536.51秒、network≤1544.45秒、CPU4500步≤1796.25秒、预测/评分review≤599.16秒；decode1800秒、GPU3600秒未耗。old/prepared/media显式read余6504611/12881150647/4279196643B，包含5旧视频验证/新part复核/decode，078未知旧上界保留，新全hash0。四根合计8GiB/4096文件/state64MiB、free≥12GiB；081从pre-sync≤12000秒且四父最终已执行时间合计≤14400秒，用户等待不计，先核旧final closure扣账。

一个科学worker、owned active8/readback、native采样256、Torch/BLAS4/interop1、codec1、CPU Job16GiB/GPU32GiB保持。普通传输retry由原version/range/partial ledger约束，全部计量，不因换进程/文件/父号清零。socket/native/wire预取/host/Git/连续配额覆盖未知如实保留，不将保守reserve当actual0或全OS认证。

080已用过的UTF8报告修复不消失；本081可最多一次新的**非科学**基础设施/报告修复，保留v1失败/源码/seal，v2在下一未消费阶段前登记。所有文本/源码/JSON/报告加载显式UTF8或UTF8-sig，不用Windows默认编码exec脚本。科学函数/GT/采样/模型图/评分/门不可变，不重放已STARTED QA/优化步；新HTTP仍受单chunk2尝试/16+8恢复/211新/总232/原byte时间限制，不能借infra例外再加GET。必要校验或恢复/预算耗尽仍STOP，保留partial，可复用证据不删。

精确九处：`prototypes/timestamped_triples_train_081.py`（完整真实HTTP adapter/预算/stream part/Job/supervisor/独立oracle，081ranges和既有progress/identity组件只读）；本目录`execution-receipt.md`、`admission-summary.json`、`baseline-summary.csv`、`head-summary.csv`、`paired-summary.csv`、`scientific-results.md`、`execution-summary.json`；`docs/codex-results.md`一次append。报告含新133+54分块计划、实际与恢复次数、prefix/SHA链、旧5seal连续、byte/time/请求跨父计量、科学表和门；NA不能填0%，不能拿假响应或metadata恒等式代替模型分数。公开不含raw QA/GT/源ID/时间戳/成员map/媒体/RGB/features/state/weights/私有路径/凭据，仅必要汇总/官方sourceURL/revision/全局hash。

授权已覆盖同科学范围，不再次请示。媒体齐后同轮连续RGB/基线兼feature/4500更新/评估；九处安全审查，一次普通main push后STOP，不自动082/论文/后台/另加实验。负责人验收同回合给下一步。
