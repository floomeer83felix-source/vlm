# 080 修复下载进度通信，完成同一真实RGB对照实验

2026-11-03（北京时间）｜ChatGPT研究负责人。
**唯一READY：APPROVED_CONTINUATION_OF_UNFINISHED_078_SCOPE / AWAIT_FRESH_080_START。** [079验收](../../research-decisions/post-079-partial-review-and-progress-repair-2026-11-03.md)及[明确续作/扣账](./continuation-scope.md)安排同一已批准科学范围，不再申请相同媒体字节/GPU/4500更新；079关闭，不回写旧失败。一次父包从余下下载连续做至完整训练/评估，不单设日志审计任务。

## 1 同步、已有资产和修正范围

安全同步独立文档main，读AGENTS/看板/results/本合同/续作表，核唯一未交付READY。沿明确handoff精确定位079、078、076闭合根，均只读；不扫其它磁盘目录。无准确路径只等输入，不交空阻断包。复用079新reuse manifest、已绑定metadata、media-plan/observations/truth/relations、model-registration/processor-fixture/身份、原source packet、network request/member ledger及summary/Job/父闭合；078必要metadata来源和076原closed身份/输入账本沿已登记指针取，不读旧QA正确性/小头。对复用文件当前SHA/旧闭合seal关系如实记录，不把新hash冒称历史证书。

已有32源/20-4-8、29文本/138问、192符号变体、1152答案/2304关系维持；22987历史metadata核验/3556新绑定、12缓存文件stat身份和原36帧processor fixture已经通过，**不要重做这些成功fixture/选择构造/全权重hash**。允许新阶段所需已封存文件身份/必要stat核对，任何不连续STOP，不重选/补数。

原科学完整规范以[制定时固定078合同](https://github.com/floomeer83felix-source/vlm/blob/259590c36b7c39e2c217158a68374c3c4a15ab08/docs/codex-artifacts/VLM-TIMESTAMPED-TRIPLES-TRAIN-078/README.md)第2–5节和[079续作](../VLM-TIMESTAMPED-TRIPLES-CONTINUE-079/README.md)相容内容为准。本080对进度journal、失败成员单次恢复、预算扣账和非科学修复作明确覆盖；不把历史READY当运行079许可。完整科学代码/数据/GT/模型/采样/架构/损失/seed/门在第一次正式080研究payload前封存；监督器、网络和独立oracle全部公开。

## 2 首先验证追加通信，彻底移除被观察状态文件replace

使用只读[080progress组件](../../../prototypes/timestamped_triples_080_progress.py)，LF SHA256 `0b12bfed5a2f74f4856ca841967d648fbd29fd3337e96d0a37ba7b0cf1d44140`。旧079 `state()`和监督器对`network-state.json`的写替换/读全文轮询必须整体替换，不只改worker。组件单writer独占新journal、sequence/job_id/前hash/内容hash链与fsync；reader按偏移校验完整newline记录，半行只保留上个完整deadline，完整损坏/错job/乱序不能忽略。Windows reader显式share READ|WRITE|DELETE；**不rename/replace/truncate/delete任何活跃观察的状态文件**，不在PermissionError时自动retry GET。

首次真实HTTP前，在本080内一次Windows并发fixture：reader持续持有handle、writer至少200次append、half-line停顿与补全、完整checksum损坏/错job/重复key、模拟replace永远PermissionError、fsync失败后writer禁止再写；验证`effective_deadline`无文件/半行不刷新额度，最后完整记录deadline仍有效。此fixture可用两个自有进程/读写线程，非科学样本/模型/媒体0，成本计准入538.83秒。负责人213本地检查只是portable分支，不能拿来冒称Windows共享API已实机通过。验证失败只在首次HTTP前修本类基础设施，不另开审计父包。

worker每GET前先把完整Range长度/请求号/累计body上界预留fsync，再CONNECT≤15秒；HEADERS及BODY写有效deadline。supervisor用`ProgressReader`和`effective_deadline`夹紧全局network累计截止、当前response outer和inactivity，不把缺失/半条状态变成IDLE/新的1800秒；初始bootstrap固定≤15秒。header outer30秒、body240秒、read inactivity60秒维持；监控20ms采样和OS覆盖边界如实列。FAILED先记异常/累计预留，再退出；不能用finally发布IDLE掩盖失败请求或吞完整校验异常。日志读取进程不是文件占用原因的既定结论，079精确锁持有者仍UNKNOWN。

## 3 恢复固定32媒体：首成员只读复用，余31一次获取

079已完成第1个媒体原MP4，uncompressed15770653B；其SHA在内存未全局seal。先用079 `media-ledger` CLOSED、原目录/源版本与精确本地路径绑定，**只读一次size/CRC并计算当前SHA**，写080新的reuse成员seal，说明SHA是在080测得、不是079历史SHA。实际字节不符/文件缺失则STOP，不代替下载。该源不得再HTTP获取或BZIP2解压；原根保持只读，080media manifest可引用原文件路径，后续实际decode计入正常一次source decode。

原第2成员response部分在内存，不能假定有可续传prefix。080明确允许其一次完整重新获取并重新核header/fields；然后30个未请求源各一次。不换任何源、排名、split、版本/标签。只原官方GCS archive对象（必要固定generation query允许）、generation1685446268139925/ETag/total28404087974，If-Match/206/精确Range/Length/identity/local ZIP64/method12/flags0/BZIP2EOF/size/CRC全部按原规范；无redirect/整archive下载/其它retry/resume。首次5 CLOSED206不代表第6 payload完成或all32媒体认证。

新≤93请求，旧6+新≤99；增加的3次仅覆盖这一个失败成员恢复/头部重核，已完成源不GET。跨079+080response body总≤805306368B；旧079应用读34690881B只是应用值，保守用全部已声明Range36263866B计费，080新body≤**769042502B**。其余31compressed565610565B，足够但余量不授权加源或重复GET。每请求STARTED/fsync保留完整目标长度上界，actual application与unknown socket/wire-prefetch分开，不以零覆盖未知。

每member MP4写完flush/fsync、CRC/size/新SHA完整验证后，立即写唯一`member-<group>-closed.json`并fsync，带源version/offset/CRC/size/内容SHA与代码seal；之后才CLOSED progress/下一源。每个seal只写新文件，不replace已被读文件；不再等32全部完成才存SHA。全部32齐后，独立从每member seal与source plan重建新global manifest，失败/未封存文件不混为CLOSED。部分或完整旧artifact绝不因新ID被当新请求额度。

## 4 准入通过即连续完成实际RGB、基线、特征与训练

1. 32源各一次decode，codec1、真实PTS及原0.1秒非重叠段、每段12不同真实frame/224RGB，96块→192真实RGB六排列，36帧/12fps/3秒统一runtime；原端点/采样/clock与prepared/相同input反GT检查保持。无latent排列、手工标签、补帧/换样；100000帧/1800秒原上限。processor对象可为正式prepare正常load，禁止再跑已通过软件fixture。全部source分母32固定。
2. 同一冻结Qwen/bf16/SDPA、完整Yes-No首续写二选一，REAL/BLACK/TEXT各1152逻辑项，最多1428新完整root/一次load/GPU3600秒/allocated16GiB/Job32GiB、3480秒停新调用。相同B0调用只读hook取V[18,2560]/q[2560]，无分离特征重算/主干梯度/generate。GPU前旧catalog当前stat/安装源码连续，cached hash不是鲜验内容认证；历史/本轮完整input与未决STARTED去重、GPU非阻塞锁/free门保持。
3. A/I/S同341633参数/初始state/batch流、seed19/73/101/137/181/229、250步/配置共18配置4500真实CPU更新，原CE与λ0/0.25/0.25 FLIP/HOLD及S(q+1)mod6关系target打乱，train20监督隔离，不选dev/seed/checkpoint、不读B0/测试答案。各角色科学worker1、Torch/BLAS4/interop1，owned active8/native采样256，旧通过head fixture不重放。
4. 仅最终状态一次REAL/BLACK/TRAIN_MEAN头预测，62208逻辑/最多25704实际eval，B0逻辑3456；保留9/162/42表、native/36-all/无向FLIP/HOLD四格和固定V50%/0整组guard、8源paired不确定性。全部预测/state/step/input/代码seals后隔离score与预封独立oracle，审计不重放Qwen/头/decode。
5. 原投入门完全保持：≥5/6 seed I源全对同时>A/S；I六seed源全对总≥12、对A/S净增各≥6；单项/FLIP/HOLD不低A/S、单项不低B0/源全对严格>B0；I胜自己固定V源全对且单项≥50%。完整全通过才保留候选；unknown INCOMPLETE，失败关闭此配方，不调参补seed/换控制。六核心函数`head_class/relation/train/predict/metrics/scoring`须与078/079本机AST等价并封存，不更换科学设计。

Perception Test全32是官方train开发划分20/4/8，原物理来源/参与者/预训练/可见性未知；timestamp段不是原子完成/唯一发生证明。079/080无模型成绩时不能声称答题收益/核心创新，过门也是小试点、外源验证与查新尚需后续，不写069论文。

## 5 一次有界非科学修复，避免把记账小错另拆父包

在本080内可**最多一次**修复journal/监控、持久I/O/成员seal或报告渲染等非科学实现错误：先持久失败/原code seal/已耗与未决状态，保存v1，修复版本用新文件/新版本seal并在下一未消费阶段前登记。六科学函数/采样/实际输入语义/GT/模型图/学习与评分/门不得改变；不能把修复伪称原版本已通过，也不能更改来源/Range/CRC检查绕过坏数据。

只继续尚未消费的工作；**绝不重问已STARTED QA、重做optimizer步或额外HTTP重取**。080唯一允许的重取是第3节明示的079第2成员一次恢复；93新请求/总byte/time/step约束一直累计。若下一阶段需要重放未决科学输入、失败下载已占尽请求许可、数据校验或预算失败，则照实STOP。此一次修复不需再次请示相同已批准范围；不是无限retry、后台或自动081。正式科学代码和完整审计仍必须在首个科学forward/训练前固定，不能看分数后补oracle。

## 6 扣账、闭合和九处交付

按[续作表](./continuation-scope.md)执行：CPU准备≤538.83秒、network≤1788.45秒、训练≤1796.25秒、预测/评分review≤599.52秒，解码1800秒/GPU3600秒未耗。old显式读余7292402B、新prepared余12881386093B，media显式读原4GiB含旧首成员size/CRC/SHA读取、新weight全hash0；078unknown仍保守预留不归零。078+079+080根合计8GiB/4096文件/checkpoint64MiB，free≥12GiB。取得078/079最终`parent-closed`实际时间，080≤12000秒且三次已执行parent合计≤14400秒，用户等待不计；如闭合证据不完整先明确缺口，不猜actual/新生额度。

旧根只读，读白名单明确；每次file/chunk读前持久reserve、读后settle，强杀未结算保留UNKNOWN/reserved。Job/process/readback/native/byte与lastseq deadline留审计，所有actualactive0退出，不能把Job累计total_processes当并发active。host/Git/native/physicalIO/快进程/连续quota覆盖边界继续如实列，不声称全面硬认证。只杀自己Job，不删旧锁/改环境/全盘扫描。

精确九处：`prototypes/timestamped_triples_train_080.py`（实际supervisor/worker/network恢复/独立oracle，新增progress组件只读）；本目录`execution-receipt.md`、`admission-summary.json`、`baseline-summary.csv`、`head-summary.csv`、`paired-summary.csv`、`scientific-results.md`、`execution-summary.json`；`docs/codex-results.md`一次append。报告含079首成员新seal来源、部分恢复/请求99上限/原byte扣账、Windowsjournal fixture、每成员持久hash、所有原科学矩阵/计量/门和一次infra版本链。NA与科学0分开，无raw QA/标签/源ID/时间戳/成员map/媒体/RGB/feature/weights/privatepath/凭据进Git，公开只必要汇总/官方URL/revision/全局hash。

同范围不再请示，准入通过即同轮完整下载/RGB/基线特征/4500更新/评估。九处安全审查及一次普通main push后STOP，不自动081/论文/补seed。负责人验收同回合给下一步。
