> **2026-11-03已按部分交付验收关闭，不修写旧轮。** [48dd29c](https://github.com/floomeer83felix-source/vlm/commit/48dd29cb7946433bf6fb4092fce52a05e193e4a4)startup/复用/缓存身份/36帧processor PASS，1媒体完成；第6请求BODY本地state replace WinError5停止，锁持有者UNKNOWN。媒体全局SHA manifest未闭合、解码/GPU/训练0/科学INCOMPLETE。[验收](../../research-decisions/post-079-partial-review-and-progress-repair-2026-11-03.md)2747公开检查；新[080](../VLM-TIMESTAMPED-TRIPLES-FINISH-080/README.md)改追加journal、复用首源并一次恢复未完成下载/原训练，原byte/GPU/step预算累计不刷新。以下079合同按当时状态逐字保留，旧READY不授权重跑。

# 079 复用078合格数据，完成原批准的真实RGB对照训练

2026-11-02（北京时间）｜ChatGPT研究负责人。
**唯一READY：APPROVED_CONTINUATION_OF_UNFINISHED_078_SCOPE / AWAIT_FRESH_079_START。** [续作依据/预算](./continuation-scope.md)明确承接用户已批准且尚未执行的同一科学工作，不再申请相同媒体/GPU/训练范围。078按[部分验收](../../research-decisions/post-078-partial-review-and-authorized-completion-2026-11-02.md)关闭不修跑；本地新消息明确079后启动一次父包。

## 1 同步与已经完成的资产

安全同步独立文档main，读AGENTS/最新看板/results/本合同和续作依据，核唯一未交付READY；新独占079根，旧078/076根和日志只读。当前交付主干7d29576，078 metadata通过、没有媒体请求/权重load/GPU/真实训练STARTED。沿明确本地handoff取得078准确根，不扫其它目录。没有地址只等输入，不交空包，不以新ID重问已STARTED科学输入。

复用078封存metadata：summary、selected、answers、relations、独立22987报告、有序owner比对、必要code/Job/读账本，以及原包内source-registration/owner-selection/原annotation ZIP（用于固定32源fps/num_frames绑定）和076 model-registration/输入账本。只这些精确文件和原包；旧078根仅为累计quota可在该根内有界清点≤4096个文件stat，不递归其它研究目录，不读旧QA正确性。不要再跑原metadata构造或已通过head fixture。校验原ZIP390919B/SHA256950ae2f6766179743f27e512948730682e444eb1c235393d034e508081224cd2、078 metadata代码SHA及闭合seal；对已选32的观察/digest按顺序绑定原owner参考、1152标签/2304关系独立按固定排列重建核对（只验证，不重新选样）。所有reuse文件当前SHA登记新manifest，保留其原来源/闭合身份，不把当前hash冒称历史seal。

固定资格仍为2135视频/13644动作/2678合格段/1376候选/280eligible；选32源20/4/8、29文本/138问，192变体/1152答案/768FLIP+1536HOLD，压缩581426975B/解压579702574B/max71166131/70872100B、28139 metadata帧。任一绑定冲突STOP，不换样/改规则/重构填数。

## 2 先修执行封装，一次预检后直接真实阶段

078失败原因是模型注册阶段Job Accounting.active3>2；第三进程身份未知，不能编故事。079科学worker仍**1**，但owned Job active上限为**8**，用于既有runtime启动/框架辅助进程，绝不启动多训练worker/进程池/DataLoader worker。直接调用当前已有环境的绝对Python executable（按既有明确登记路径解析），不经`py`、`conda run`、`cmd /c`、PowerShell多重包装；不换环境/安装/重启/杀别人的进程。TOKENIZERS_PARALLELISM=false，Torch/BLAS intra4、interop1、codec1和native采样256保持。

真实payload前一次小型startup/依赖导入预检，记录PID/PPID、角色、可执行basename、创建时刻、Job Accounting.active、PIDlist population分别值、峰值/内存/退出；原始进程地址只在私有根，公开仅basename/角色汇总。限额配置后QueryInformationJobObject读回limit_flags/active8/memory/kill-on-close，supervisor20ms采样Accounting与PIDlist独立，不再相混；记录所有自己新子进程，不列别人的进程/命令行。辅助进程未知可在8以内如实标UNKNOWN，不擅自归为新增科学worker。实际>8或内存/deadline超限，先持久实际及PID证据，再只关闭自己Job。预检不是新研究父包，不做模型/真实媒体probe，不重跑078 head fixture。预正式payload前可修已记录语法/封装fixture，完整源码重封后才进入正式研究，不能用此例外重试科学数据。

079公开pipeline必须包含本轮实际supervisor/Job结构及计量实现（可以同文件内类），不能只交worker而把此次关键监督器藏在不可审查私有helper。保留旧078的错误记录，不将新阈值倒填旧任务合规。

## 3 注册身份：使用缓存内容hash，不再全权重hash

078注册强杀，hash实际读取/完成未知；按旧完整12GiB上界保守占用，079全权重hash新读**0**。旧076 `model-registration.json`已有graph/content-hash、每文件size/mtime及closed asset身份。调用只读[079 identity组件](../../../prototypes/timestamped_triples_079_identity.py)，LF SHA256 `89567c6d5d31166be0e319cf4837292c828d2c593c8d4d6d843fd154df7edf6c`；验证旧catalog封存身份、canonical graph hash、完整文件集合、当前每文件size/mtime和安装源码小hash。catalog注册总8887284080B；任何graph/stat/源码变动STOP，不自行fresh rehash。报告`CACHED_076_HASH_PLUS_UNCHANGED_STATS / NO_NEW_FULL_HASH`，明确不是新逐字节认证。

**不要直接重跑078 registration函数**，它会再hash全权重。新registration拆成缓存身份桥及第一次实际CPU processor-only36帧fixture，后者078从未完成，现在可在新code seal下执行一次。每个import前后、stat组开始/完成、processor开始/完成都有durable进度及当前自身PID角色；复制为新注册记录时保留旧graph/stat及缓存provenance，不伪报fresh hash8887284080B。首fixture必须核36帧grid[18,14,14]/pixels[3528,1536]/882token、单Yes/No、assistant首续写、同原native时间字段拆分/只读hook静态绑定，未过则不拿任何模型输入试探。

## 4 原科学设计完整执行，保持078数据/方法/门

下列完整规范按[原078合同（制定时固定版）](https://github.com/floomeer83felix-source/vlm/blob/259590c36b7c39e2c217158a68374c3c4a15ab08/docs/codex-artifacts/VLM-TIMESTAMPED-TRIPLES-TRAIN-078/README.md)第2–5节逐项适用，本合同仅对前述执行封装/身份/累计资源作明确覆盖；不能把只读历史READY解释为重跑078。实际未启动部分都在079一次执行：

1. 固定官方archive对象/generation1685446268139925/ETag，≤96精确Range/网络正文768MiB，必要固定generation query可用；206/Content-Range/Length/identity/版本/local ZIP64/method12/CRC/BZIP2全部核定，不整包、无redirect/retry/resume。connect15秒/header30秒/body240秒/inactivity60秒/累计1800秒原门，supervisor要覆盖连接阶段，不靠socket timeout冒充outer。
2. 32源各解码一次，codec显式1/真实PTS/12不同帧每段/均匀36帧12fps3秒，96真实RGB块→192真实排列，全部非pixel同时钟相同；不是latent排列。原100000帧/1800秒、aggregate解压640MiB/每member80MiB限制保持。不足/矛盾保持32分母STOP，不补帧/换源。
3. 同冻结本地Qwen/bf16/SDPA/完整Yes-No logit二选一，最多1428新root、一次load、GPU3600秒/allocated16GiB/Job32GiB、3480秒新调用截止，B0 REAL/BLACK/TEXT各1152逻辑项。只在同一B0前向hook捕获主merger V[18,2560]与TEXT当前q[2560]；分离特征重算0、generate0、主干backward0，已STARTED/CLOSED精确去重不得绕过。192pixels逐variant加载一次供六问复用，BLACK全局一份；旧QA/答案不读入训练。模型load前再核全catalog stat未变化。
4. A/I/S完全同341633参数/初始化/250步batch流，seed19/73/101/137/181/229；18配置4500真实CPU更新，AdamW及原λ0/0.25/0.25、I正确FLIP/HOLD、S(q+1)mod6相关target打乱、答案不变；无dev选择、只step250，train20监督隔离。必须保持078公开`head_class/relation/train/predict/metrics/scoring`科学函数等价（对比封存AST/参数），允许改持久I/O、根路径、进程封装和new registration，不添新的头或训练条件。
5. 一次预测REAL/BLACK/TRAIN_MEAN头输出62208逻辑项/actual最多25704，B0逻辑3456；原source36-all、native六问、无向相邻四格6FLIP+12HOLD/每源、固定V50%/0整组guard。隔离scorer/独立oracle不重放头/视频/Qwen；保留完整8源test与小样本/官方train开发划分、未知原始物理来源/可见性边界。
6. 原所有门不变：至少5/6 seed I源全对同时>A/S；六seed I源全对总≥12且对A/S净增各≥6；I单项/FLIP/HOLD均不低A/S、单项不低B0且源全对严格>B0，I源全对胜自己BLACK/MEAN且单项≥50%。全通过才保留候选，不通过关闭具体配方；unknown为INCOMPLETE。没有结果时不声称新机制/外部确认，不写论文/不自动080。

科学函数借用078源码不等于运行旧父包：新sealed079入口、新input/Job/ledger，与已经闭合且没有实际科学输入的078明确区分。原完整独立oracle尚未验证实际科学结果，079不能因metadata PASS省掉它。所有actual NEW/alias/分母/hook/steps/state/对照/资源独立核验代码必须预先封存，不在输出后补oracle。

## 5 资源扣账和持久计量

以[续作表](./continuation-scope.md)为授权/扣账准据。科学媒体/GPU/4500步无新额度：新CPU准入≤581.23秒、训练≤1796.25秒、预测评分review≤599.79秒；媒体/解码1800秒及GPU3600秒保持。metadata和head fixture已做不重跑。079父≤12000秒，078最终父时间单列；可读最终闭合则核总14400秒，缺失保留UNKNOWN不伪全面认证。起始free≥12GiB，两根078+079合计8GiB/4096文件/state64MiB；CPU Job16GiB/GPU32GiB、科学并发1、owned active8、native采样256。

078强杀前显式旧metadata/新prepared actual读量丢失，分别按原32MiB/12GiB上界保留；079只允许精确旧metadata新增8MiB、新prepared/中间件12GiB、media4GiB、新weight hash0。总保守旧metadata40MiB/prepared24GiB/hash12GiB不冒称actual；这是有界CPU/本地读取修复，并非追加研究数据范围。原076 cached model图/输入ledger、新078metadata/closedJob/progress和必要catalog均属于上述白名单，禁止旧QA结果/未指定根扫描。

每个角色读前持久预留本次最大size/累计上界，读后结算actual，强杀未结算记录reserved/actual UNKNOWN；stream/hash按有界chunk预留，file stat+limit检查要在read前，不能读完才发现超限。角色之间累计，临时未闭合计数不得归零；不把reserve当实际/物理IO，不重新hash旧未完成payload求补证。所有自有PID进度/异常计量durable；有正常exit的角色finish不替代强杀前进度。框架native隐式file reads/host/Git/物理IO/连续线程/硬disk覆盖未知明确写出，不扩张为科学失败或全面合规证书。

## 6 九处统一交付并停止

精确九处：`prototypes/timestamped_triples_train_079.py`（含实际Job/supervisor/worker与独立review，079 identity组件只读）；本目录`execution-receipt.md`、`admission-summary.json`、`baseline-summary.csv`、`head-summary.csv`、`paired-summary.csv`、`scientific-results.md`、`execution-summary.json`；`docs/codex-results.md`一次append。基线9行、头162行、配对42行原分母/NA规则不变。JSON/receipt含078资产reuse身份、累计与剩余、原实际停止/未认证项、新process tree/limit readback/CPU身份缓存provenance和全部科学实际数；无科学输出不能填0%或拿fixture替代。

无raw问题/GT/源ID/时间戳/成员映射、视频/RGB/feature/state/weights、私有路径/凭据进Git；公开只官方URL/revision/全局hash/汇总/必要可执行basename。旧078/076历史、负责人文件、metadata/identity组件只读。完成九处安全审查与一次普通push main后STOP，不自动080/补seed/换头/后台/写论文；同批准范围不再请示。负责人验收同回合给下一步。
